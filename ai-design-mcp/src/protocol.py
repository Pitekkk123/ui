"""
JSON-RPC 2.0 transport for Model Context Protocol (MCP).
Handles stdio communication, message routing, and lifecycle.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine

logger = logging.getLogger("ai-design-mcp")


@dataclass
class MCPTool:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[..., Coroutine[Any, Any, Any]]


class MCPServer:
    """Minimal, spec-compliant MCP server over stdio (JSON-RPC 2.0)."""

    SERVER_NAME = "ai-design-mcp"
    SERVER_VERSION = "1.0.0"
    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self) -> None:
        self._tools: dict[str, MCPTool] = {}
        self._resources: dict[str, Any] = {}
        self._running = False

    # ── tool registration ──────────────────────────────────────────

    def tool(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
    ):
        """Decorator to register an MCP tool."""

        def decorator(fn: Callable[..., Coroutine[Any, Any, Any]]):
            self._tools[name] = MCPTool(
                name=name,
                description=description,
                input_schema=input_schema,
                handler=fn,
            )
            return fn

        return decorator

    def register_tool(self, tool: MCPTool) -> None:
        self._tools[tool.name] = tool

    # ── message handling ───────────────────────────────────────────

    async def _handle_message(self, msg: dict[str, Any]) -> dict[str, Any] | None:
        method = msg.get("method", "")
        msg_id = msg.get("id")
        params = msg.get("params", {})

        # Notifications (no id) — just acknowledge
        if msg_id is None:
            if method == "notifications/initialized":
                logger.info("Client initialized")
            return None

        if method == "initialize":
            return self._ok(msg_id, {
                "protocolVersion": self.PROTOCOL_VERSION,
                "capabilities": {
                    "tools": {"listChanged": False},
                },
                "serverInfo": {
                    "name": self.SERVER_NAME,
                    "version": self.SERVER_VERSION,
                },
            })

        if method == "tools/list":
            tools_list = []
            for t in self._tools.values():
                tools_list.append({
                    "name": t.name,
                    "description": t.description,
                    "inputSchema": t.input_schema,
                })
            return self._ok(msg_id, {"tools": tools_list})

        if method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            tool = self._tools.get(tool_name)
            if not tool:
                return self._error(msg_id, -32601, f"Unknown tool: {tool_name}")
            try:
                result = await tool.handler(arguments)
                # Wrap plain strings in content blocks
                if isinstance(result, str):
                    content = [{"type": "text", "text": result}]
                elif isinstance(result, dict):
                    content = [{"type": "text", "text": json.dumps(result, indent=2)}]
                elif isinstance(result, list):
                    content = result
                else:
                    content = [{"type": "text", "text": str(result)}]
                return self._ok(msg_id, {"content": content})
            except Exception as exc:
                logger.exception("Tool %s failed", tool_name)
                return self._ok(msg_id, {
                    "content": [{"type": "text", "text": f"Error: {exc}"}],
                    "isError": True,
                })

        if method == "ping":
            return self._ok(msg_id, {})

        return self._error(msg_id, -32601, f"Method not found: {method}")

    # ── JSON-RPC helpers ───────────────────────────────────────────

    @staticmethod
    def _ok(msg_id: Any, result: Any) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}

    @staticmethod
    def _error(msg_id: Any, code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}

    # ── stdio transport ────────────────────────────────────────────

    async def run_stdio(self) -> None:
        """Main loop: read JSON-RPC from stdin, write responses to stdout."""
        self._running = True
        logger.info("MCP server starting on stdio")

        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin.buffer)

        writer_transport, writer_protocol = await asyncio.get_event_loop().connect_write_pipe(
            asyncio.streams.FlowControlMixin, sys.stdout.buffer
        )
        writer = asyncio.StreamWriter(writer_transport, writer_protocol, None, asyncio.get_event_loop())

        buf = b""
        while self._running:
            try:
                chunk = await reader.read(65536)
                if not chunk:
                    break
                buf += chunk

                # Process complete lines
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        msg = json.loads(line)
                    except json.JSONDecodeError:
                        logger.warning("Invalid JSON: %s", line[:200])
                        continue

                    response = await self._handle_message(msg)
                    if response is not None:
                        out = json.dumps(response) + "\n"
                        writer.write(out.encode())
                        await writer.drain()

            except (asyncio.CancelledError, KeyboardInterrupt):
                break
            except Exception:
                logger.exception("Error in main loop")
                break

        logger.info("MCP server stopped")

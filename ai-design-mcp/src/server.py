"""
AI Design MCP Server — Main entry point.

Registers all tools and starts the stdio transport.
Replicates and extends the functionality of aidesigner.ai MCP with:
- generate_design: Create production-quality fintech UI
- refine_design: Iterate on designs with natural language
- analyze_screenshot: Vision-based UI decomposition (superior to AI Designer)
- analyze_design_system: Repo-aware framework/token detection
- generate_adoption_brief: Map designs to your framework
- list_designs: Browse previous design runs
- get_status: Server info and capabilities
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

# Configure logging to stderr (stdout is for JSON-RPC)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("ai-design-mcp")

from .protocol import MCPServer, MCPTool
from .design_system import DesignSystemAnalyzer
from .fintech_presets import (
    DASHBOARD_LAYOUT_TEMPLATES,
    FINTECH_COMPONENT_PATTERNS,
    FINTECH_DESIGN_TOKENS,
)


def create_server() -> MCPServer:
    """Create and configure the MCP server with all tools."""

    server = MCPServer()

    # Lazy-init these when first needed (requires ANTHROPIC_API_KEY)
    _generator = None
    _analyzer = None
    _adoption = None

    def _get_anthropic_client():
        import anthropic
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY environment variable is required. "
                "Set it before starting the server."
            )
        return anthropic.Anthropic(api_key=api_key)

    def _get_generator():
        nonlocal _generator
        if _generator is None:
            from .generator import DesignGenerator
            project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
            storage = os.path.join(project_root, ".aidesigner")
            _generator = DesignGenerator(_get_anthropic_client(), storage_dir=storage)
        return _generator

    def _get_analyzer():
        nonlocal _analyzer
        if _analyzer is None:
            from .screenshot_analyzer import ScreenshotAnalyzer
            _analyzer = ScreenshotAnalyzer(_get_anthropic_client())
        return _analyzer

    def _get_adoption():
        nonlocal _adoption
        if _adoption is None:
            from .adoption import AdoptionBriefGenerator
            _adoption = AdoptionBriefGenerator(_get_anthropic_client())
        return _adoption

    # ═══════════════════════════════════════════════════════════════
    # TOOL: generate_design
    # ═══════════════════════════════════════════════════════════════

    @server.tool(
        name="generate_design",
        description=(
            "Generate a complete, production-ready UI design as a standalone HTML document "
            "with Tailwind CSS. Optimized for fintech dashboards, banking apps, trading "
            "platforms, and financial web applications. Outputs award-winning quality HTML "
            "that can be previewed directly in a browser.\n\n"
            "Supports reference modes:\n"
            "- 'clone': Replicate a reference design pixel-for-pixel\n"
            "- 'enhance': Improve a reference while preserving its goals\n"
            "- 'inspire': Use a reference as creative inspiration\n\n"
            "Design presets: mercury (dark banking), stripe (light payments), "
            "ramp (modern expense), linear (dark premium)\n\n"
            "Layout templates: overview, analytics, accounts, trading"
        ),
        input_schema={
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": (
                        "Design description. Be specific about: layout, components, "
                        "data to display, color scheme, and target user. "
                        "Example: 'A fintech dashboard showing portfolio overview with "
                        "4 KPI cards, asset allocation donut chart, recent transactions "
                        "table, and a performance line chart. Dark theme.'"
                    ),
                },
                "viewport": {
                    "type": "string",
                    "enum": ["desktop", "mobile"],
                    "default": "desktop",
                    "description": "Target viewport for the design.",
                },
                "preset": {
                    "type": "string",
                    "enum": ["mercury", "stripe", "ramp", "linear"],
                    "default": "mercury",
                    "description": "Design system preset defining colors, typography, spacing.",
                },
                "template": {
                    "type": "string",
                    "enum": ["overview", "analytics", "accounts", "trading"],
                    "default": "overview",
                    "description": "Layout template defining the page structure.",
                },
                "reference_mode": {
                    "type": "string",
                    "enum": ["clone", "enhance", "inspire"],
                    "description": "How to use the reference_source. Required if reference_source is set.",
                },
                "reference_source": {
                    "type": "string",
                    "description": "URL or file path to reference design (screenshot/image/website).",
                },
            },
            "required": ["prompt"],
        },
    )
    async def generate_design(args: dict[str, Any]) -> str:
        gen = _get_generator()

        # If reference is an image, analyze it first
        screenshot_analysis = ""
        ref_mode = args.get("reference_mode")
        ref_source = args.get("reference_source")
        if ref_source and _is_image(ref_source):
            analyzer = _get_analyzer()
            result = await analyzer.analyze_image(
                ref_source,
                mode=ref_mode or "analyze",
            )
            screenshot_analysis = result.get("analysis", "")

        # Detect design system from project
        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        ds_analyzer = DesignSystemAnalyzer(project_root)
        ds_report = ds_analyzer.analyze()

        run = await gen.generate(
            prompt=args["prompt"],
            viewport=args.get("viewport", "desktop"),
            preset=args.get("preset", "mercury"),
            template=args.get("template", "overview"),
            reference_mode=ref_mode,
            reference_source=ref_source,
            design_system_context=ds_report.to_context_prompt(),
            screenshot_analysis=screenshot_analysis,
        )

        return json.dumps({
            "run_id": run.run_id,
            "html": run.html,
            "viewport": run.viewport,
            "preset": run.preset,
            "template": run.template,
            "created_at": run.created_at,
            "saved_to": str(gen.storage_dir / run.run_id),
            "preview_instructions": (
                f"Open {gen.storage_dir / run.run_id / 'design.html'} in a browser to preview. "
                "Or use: python -m http.server 8080 --directory .aidesigner"
            ),
        }, indent=2)

    # ═══════════════════════════════════════════════════════════════
    # TOOL: refine_design
    # ═══════════════════════════════════════════════════════════════

    @server.tool(
        name="refine_design",
        description=(
            "Iterate on a previous design with natural language feedback. "
            "Adjusts layout, colors, typography, spacing, or content without starting over. "
            "Preserves the design's structure and quality while applying targeted changes."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "run_id": {
                    "type": "string",
                    "description": "The run_id of the design to refine (from generate_design output).",
                },
                "feedback": {
                    "type": "string",
                    "description": (
                        "Natural language description of changes. "
                        "Example: 'Make the header more compact, change the chart from line to area, "
                        "add a date range picker above the table, use emerald for positive values.'"
                    ),
                },
                "reference_mode": {
                    "type": "string",
                    "enum": ["clone", "enhance", "inspire"],
                    "description": "Optional reference mode for the refinement.",
                },
                "reference_source": {
                    "type": "string",
                    "description": "Optional URL or image path for reference.",
                },
            },
            "required": ["run_id", "feedback"],
        },
    )
    async def refine_design(args: dict[str, Any]) -> str:
        gen = _get_generator()

        screenshot_analysis = ""
        ref_source = args.get("reference_source")
        if ref_source and _is_image(ref_source):
            analyzer = _get_analyzer()
            result = await analyzer.analyze_image(ref_source, mode=args.get("reference_mode", "analyze"))
            screenshot_analysis = result.get("analysis", "")

        run = await gen.refine(
            run_id=args["run_id"],
            feedback=args["feedback"],
            reference_mode=args.get("reference_mode"),
            reference_source=ref_source,
            screenshot_analysis=screenshot_analysis,
        )

        return json.dumps({
            "run_id": run.run_id,
            "html": run.html,
            "refined_from": run.refinement_of,
            "viewport": run.viewport,
            "created_at": run.created_at,
            "saved_to": str(gen.storage_dir / run.run_id),
        }, indent=2)

    # ═══════════════════════════════════════════════════════════════
    # TOOL: analyze_screenshot
    # ═══════════════════════════════════════════════════════════════

    @server.tool(
        name="analyze_screenshot",
        description=(
            "Analyze a UI screenshot or design image with Claude Opus 4.6 vision. "
            "Produces an exhaustive, structured design specification covering: "
            "layout architecture, color system (exact values), typography, component inventory, "
            "spacing rhythm, data visualization patterns, interactive elements, and "
            "fintech-specific elements (currency displays, KPIs, trading indicators).\n\n"
            "SUPERIOR to aidesigner.ai — provides exact Tailwind CSS class mappings and "
            "shadcn/ui component recommendations for every detected element.\n\n"
            "Modes:\n"
            "- 'analyze': Full design specification (default)\n"
            "- 'clone': Extract specs for pixel-perfect replication\n"
            "- 'enhance': Analyze + suggest improvements\n"
            "- 'inspire': Extract design principles and patterns"
        ),
        input_schema={
            "type": "object",
            "properties": {
                "image": {
                    "type": "string",
                    "description": (
                        "Path to screenshot/image file, URL, or base64-encoded image data. "
                        "Supports PNG, JPG, WebP, GIF."
                    ),
                },
                "mode": {
                    "type": "string",
                    "enum": ["analyze", "clone", "enhance", "inspire"],
                    "default": "analyze",
                    "description": "Analysis mode determining the depth and focus of the output.",
                },
                "context": {
                    "type": "string",
                    "description": "Additional context about the screenshot (e.g., 'This is a crypto trading dashboard').",
                },
                "images": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Multiple image paths/URLs for multi-screen analysis.",
                },
            },
            "required": [],
        },
    )
    async def analyze_screenshot(args: dict[str, Any]) -> str:
        analyzer = _get_analyzer()

        # Detect design system for context
        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        ds_analyzer = DesignSystemAnalyzer(project_root)
        ds_report = ds_analyzer.analyze()

        images = args.get("images", [])
        single_image = args.get("image", "")

        if images and len(images) > 1:
            result = await analyzer.analyze_multiple(
                images=images,
                mode=args.get("mode", "analyze"),
                context=args.get("context", ""),
            )
        elif single_image or (images and len(images) == 1):
            img = single_image or images[0]
            result = await analyzer.analyze_image(
                image_source=img,
                mode=args.get("mode", "analyze"),
                context=args.get("context", ""),
                design_system_context=ds_report.to_context_prompt(),
            )
        else:
            return json.dumps({"error": "Provide 'image' (single) or 'images' (multiple) parameter."})

        return json.dumps({
            "mode": result.get("mode"),
            "analysis": result.get("analysis"),
            "structured": result.get("structured"),
            "project_design_system": ds_report.to_dict(),
        }, indent=2, default=str)

    # ═══════════════════════════════════════════════════════════════
    # TOOL: analyze_design_system
    # ═══════════════════════════════════════════════════════════════

    @server.tool(
        name="analyze_design_system",
        description=(
            "Analyze the current project repository to detect its design system, "
            "framework, component libraries, CSS tokens, route structure, typography, "
            "color palette, and build tooling. Provides context for design generation "
            "that matches your existing codebase."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the project root. Defaults to current working directory.",
                },
            },
            "required": [],
        },
    )
    async def analyze_design_system(args: dict[str, Any]) -> str:
        project_root = args.get("project_path") or os.environ.get("PROJECT_ROOT", os.getcwd())
        analyzer = DesignSystemAnalyzer(project_root)
        report = analyzer.analyze()

        return json.dumps({
            "report": report.to_dict(),
            "summary": report.to_context_prompt(),
        }, indent=2, default=str)

    # ═══════════════════════════════════════════════════════════════
    # TOOL: generate_adoption_brief
    # ═══════════════════════════════════════════════════════════════

    @server.tool(
        name="generate_adoption_brief",
        description=(
            "Generate a structured adoption brief / porting guide that maps a generated "
            "HTML design to your project's framework. Identifies target route placement, "
            "CSS token mapping, component reuse opportunities, data requirements, "
            "interaction specifications, and step-by-step migration plan."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "run_id": {
                    "type": "string",
                    "description": "The run_id of a design to create an adoption brief for.",
                },
                "target_route": {
                    "type": "string",
                    "description": "Target route path (e.g., '/dashboard'). Auto-detected if not provided.",
                },
                "use_ai": {
                    "type": "boolean",
                    "default": True,
                    "description": "Use Claude Opus to generate a comprehensive brief (costs tokens). Set false for local analysis only.",
                },
            },
            "required": ["run_id"],
        },
    )
    async def generate_adoption_brief(args: dict[str, Any]) -> str:
        gen = _get_generator()
        adoption = _get_adoption()

        run_id = args["run_id"]
        run = gen._runs.get(run_id)
        if not run:
            run = await gen._load_run(run_id)
        if not run:
            return json.dumps({"error": f"Design run '{run_id}' not found."})

        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        ds_analyzer = DesignSystemAnalyzer(project_root)
        ds_report = ds_analyzer.analyze()

        if args.get("use_ai", True):
            brief = await adoption.generate_brief(
                html=run.html,
                design_system=ds_report,
                target_route=args.get("target_route", ""),
            )
        else:
            brief = adoption.generate_brief_local(
                html=run.html,
                design_system=ds_report,
                target_route=args.get("target_route", ""),
            )

        return json.dumps(brief, indent=2, default=str)

    # ═══════════════════════════════════════════════════════════════
    # TOOL: list_designs
    # ═══════════════════════════════════════════════════════════════

    @server.tool(
        name="list_designs",
        description="List all previously generated design runs with their metadata.",
        input_schema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )
    async def list_designs(args: dict[str, Any]) -> str:
        gen = _get_generator()
        runs = gen.list_runs()
        return json.dumps({
            "total": len(runs),
            "designs": runs,
        }, indent=2)

    # ═══════════════════════════════════════════════════════════════
    # TOOL: get_design_presets
    # ═══════════════════════════════════════════════════════════════

    @server.tool(
        name="get_design_presets",
        description=(
            "List available fintech design system presets and layout templates. "
            "Use this to discover preset names for generate_design."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "preset": {
                    "type": "string",
                    "description": "Get details for a specific preset. Omit to list all.",
                },
            },
            "required": [],
        },
    )
    async def get_design_presets(args: dict[str, Any]) -> str:
        preset_name = args.get("preset")
        if preset_name and preset_name in FINTECH_DESIGN_TOKENS:
            return json.dumps({
                "preset": FINTECH_DESIGN_TOKENS[preset_name],
                "templates": {k: {"name": v["name"], "description": v["description"]} for k, v in DASHBOARD_LAYOUT_TEMPLATES.items()},
                "components": list(FINTECH_COMPONENT_PATTERNS.keys()),
            }, indent=2)

        return json.dumps({
            "presets": {k: v["name"] for k, v in FINTECH_DESIGN_TOKENS.items()},
            "templates": {k: {"name": v["name"], "description": v["description"]} for k, v in DASHBOARD_LAYOUT_TEMPLATES.items()},
            "components": list(FINTECH_COMPONENT_PATTERNS.keys()),
        }, indent=2)

    # ═══════════════════════════════════════════════════════════════
    # TOOL: get_status
    # ═══════════════════════════════════════════════════════════════

    @server.tool(
        name="get_status",
        description="Get server status, capabilities, and configuration info.",
        input_schema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )
    async def get_status(args: dict[str, Any]) -> str:
        has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())

        return json.dumps({
            "server": "ai-design-mcp",
            "version": "1.0.0",
            "model": "claude-opus-4-6",
            "anthropic_api_key_configured": has_key,
            "project_root": project_root,
            "capabilities": {
                "generate_design": "Create production-quality fintech UI designs",
                "refine_design": "Iterate on designs with natural language",
                "analyze_screenshot": "Vision-based UI decomposition (Opus 4.6)",
                "analyze_design_system": "Repo-aware framework/token detection",
                "generate_adoption_brief": "Map designs to your framework",
                "list_designs": "Browse saved design runs",
                "get_design_presets": "List available design presets",
                "get_status": "Server info",
            },
            "design_presets": list(FINTECH_DESIGN_TOKENS.keys()),
            "layout_templates": list(DASHBOARD_LAYOUT_TEMPLATES.keys()),
        }, indent=2)

    return server


def _is_image(source: str) -> bool:
    """Check if the source looks like an image (not a URL to a webpage)."""
    source_lower = source.lower()
    image_exts = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg")
    if any(source_lower.endswith(ext) for ext in image_exts):
        return True
    if source_lower.startswith("data:image/"):
        return True
    if Path(source).suffix.lower() in image_exts:
        return True
    return False


def main():
    """Entry point for the MCP server."""
    server = create_server()
    try:
        asyncio.run(server.run_stdio())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

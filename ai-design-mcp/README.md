# AI Design MCP Server

Award-winning AI Design MCP Server for Claude Code — generates production-quality fintech UI, analyzes screenshots with Opus 4.6 vision, and maps designs to your framework.

## Features

| Tool | Description |
|------|-------------|
| `generate_design` | Create complete HTML+Tailwind fintech UI from text prompts |
| `refine_design` | Iterate with natural language feedback without starting over |
| `analyze_screenshot` | Vision-based UI decomposition — extracts exact colors, spacing, typography, components |
| `analyze_design_system` | Repo-aware detection of framework, libraries, CSS tokens, routes |
| `generate_adoption_brief` | Map generated designs to your framework (Next.js, React, Vue, etc.) |
| `list_designs` | Browse all saved design runs |
| `get_design_presets` | List fintech design presets and layout templates |
| `get_status` | Server capabilities and configuration |

### Reference Modes

- **clone** — Pixel-perfect replication of a reference
- **enhance** — Improve a design while preserving structure  
- **inspire** — Use a reference as creative inspiration

### Design Presets

- **mercury** — Dark banking (Mercury-style)
- **stripe** — Light payments (Stripe-style)
- **ramp** — Modern expense management (Ramp-style)
- **linear** — Dark premium (Linear-style)

### Layout Templates

- **overview** — Executive dashboard with KPIs, charts, activity feed
- **analytics** — Data deep-dive with filters and breakdowns
- **accounts** — Account cards, transactions, spending
- **trading** — Terminal with charts, order book, positions

## Setup

### 1. Install dependencies

```bash
cd ai-design-mcp
pip install -e .
```

### 2. Set your API key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 3. Configure Claude Code

Add to your `.claude/settings.json` or project settings:

```json
{
  "mcpServers": {
    "ai-design-mcp": {
      "command": "python3",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/ai-design-mcp",
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "PROJECT_ROOT": "/path/to/your/project"
      }
    }
  }
}
```

### 4. Run standalone (for testing)

```bash
cd ai-design-mcp
python3 -m src.server
```

## Usage Examples

### Generate a Dashboard

```
Use generate_design to create a fintech portfolio dashboard with:
- 4 KPI cards (total balance, monthly return, total assets, pending transfers)
- Performance line chart with 7D/1M/1Y toggle
- Recent transactions table with search and filters
- Asset allocation donut chart
Use the mercury preset and overview template.
```

### Analyze a Screenshot

```
Use analyze_screenshot on ./screenshot.png in clone mode 
to extract the exact design specification.
```

### Refine a Design

```
Use refine_design on run_id "2026-04-14T..." with feedback:
"Make the sidebar collapsible, change KPI trend colors to use 
emerald-500/rose-500, add skeleton loading states"
```

### Generate Adoption Brief

```
Use generate_adoption_brief for run_id "2026-04-14T..." 
targeting the /dashboard route.
```

## Architecture

```
ai-design-mcp/
├── src/
│   ├── __init__.py          # Package init
│   ├── server.py            # Main MCP server — tool registration + entry point
│   ├── protocol.py          # JSON-RPC 2.0 / MCP protocol handler (stdio)
│   ├── generator.py         # Design generator (Claude Opus 4.6)
│   ├── screenshot_analyzer.py  # Vision-based UI analyzer
│   ├── design_system.py     # Repo-aware design system detector
│   ├── adoption.py          # Adoption brief generator
│   └── fintech_presets.py   # Fintech design tokens & templates
├── pyproject.toml           # Python package config
├── claude_code_config.json  # Claude Code MCP configuration
└── README.md
```

## Requirements

- Python 3.10+
- `anthropic` SDK (for Claude Opus 4.6 API)
- `ANTHROPIC_API_KEY` environment variable

"""
Adoption Brief Generator — maps generated HTML designs to the target framework,
identifies route placement, CSS token mapping, and component reuse opportunities.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from .design_system import DesignSystemReport

logger = logging.getLogger("ai-design-mcp")


class AdoptionBriefGenerator:
    """Generate a structured porting guide from HTML design to target framework."""

    def __init__(self, anthropic_client):
        self.client = anthropic_client
        self.model = "claude-opus-4-6"

    async def generate_brief(
        self,
        html: str,
        design_system: DesignSystemReport,
        target_route: str = "",
        additional_context: str = "",
    ) -> dict[str, Any]:
        """Generate an adoption brief mapping the design to the project's stack."""

        prompt = self._build_prompt(html, design_system, target_route, additional_context)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            system="""\
You are a senior frontend architect. Produce a precise, actionable adoption brief \
that maps an HTML/Tailwind design to a specific framework. Output valid JSON only.\
""",
            messages=[{"role": "user", "content": prompt}],
        )

        raw = response.content[0].text
        return self._parse_brief(raw)

    def generate_brief_local(
        self,
        html: str,
        design_system: DesignSystemReport,
        target_route: str = "",
    ) -> dict[str, Any]:
        """Generate a basic adoption brief without calling the AI model (local analysis)."""
        brief: dict[str, Any] = {
            "framework": design_system.framework,
            "targetRoute": target_route or self._suggest_route(html, design_system),
            "components": [],
            "cssTokenMapping": {},
            "fileStructure": [],
            "imports": [],
            "notes": [],
        }

        # Detect components used in the HTML
        component_map = self._detect_html_components(html)
        brief["components"] = component_map

        # Map Tailwind classes to design tokens
        brief["cssTokenMapping"] = self._map_tokens(html, design_system)

        # Suggest file structure
        brief["fileStructure"] = self._suggest_file_structure(
            design_system.framework, target_route or "dashboard"
        )

        # Suggest imports
        brief["imports"] = self._suggest_imports(design_system, component_map)

        return brief

    def _build_prompt(
        self,
        html: str,
        design_system: DesignSystemReport,
        target_route: str,
        additional_context: str,
    ) -> str:
        return f"""\
## Task
Generate an adoption brief as JSON that maps this HTML design to the target framework.

## Design System Context
{design_system.to_context_prompt()}

## Target Route
{target_route or "Auto-detect from design content"}

## HTML Design to Adopt
```html
{html[:12000]}
```

## Additional Context
{additional_context}

## Required JSON Output Structure
{{
  "framework": "{design_system.framework}",
  "targetRoute": "/path/to/page",
  "routeType": "page | layout | component",
  "components": [
    {{
      "name": "ComponentName",
      "type": "shadcn/custom/layout",
      "shadcnComponent": "Card | Table | Button | null",
      "props": ["prop1", "prop2"],
      "children": ["ChildComponent"],
      "notes": "Implementation notes"
    }}
  ],
  "cssTokenMapping": {{
    "tailwind-class": "css-variable-or-token",
    "bg-zinc-900": "--background",
    "text-emerald-500": "--success"
  }},
  "fileStructure": [
    {{
      "path": "src/app/dashboard/page.tsx",
      "type": "page | component | hook | util",
      "description": "Main dashboard page"
    }}
  ],
  "imports": [
    {{
      "package": "@/components/ui/card",
      "items": ["Card", "CardContent", "CardHeader"]
    }}
  ],
  "dataRequirements": [
    {{
      "name": "dashboardMetrics",
      "type": "API | static | realtime",
      "shape": "{{ revenue: number, growth: number }}"
    }}
  ],
  "interactionSpec": [
    {{
      "element": "Time range selector",
      "action": "Click tab",
      "behavior": "Reload chart data for selected period",
      "stateChange": "selectedRange: '7d' | '1m' | '1y'"
    }}
  ],
  "accessibilityNotes": [
    "Add aria-label to icon-only buttons",
    "Ensure chart data is available in table form for screen readers"
  ],
  "estimatedComplexity": "low | medium | high",
  "estimatedComponents": 12,
  "migrationSteps": [
    "1. Create route file at /dashboard",
    "2. Set up data fetching with TanStack Query",
    "3. Build KPI card components",
    "..."
  ]
}}

Output ONLY the JSON object. No markdown, no explanation.\
"""

    def _parse_brief(self, raw: str) -> dict[str, Any]:
        raw = raw.strip()
        if raw.startswith("```json"):
            raw = raw[7:]
        if raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Try to find JSON in the response
            match = re.search(r"\{[\s\S]+\}", raw)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
            return {"error": "Failed to parse adoption brief", "raw": raw[:2000]}

    def _detect_html_components(self, html: str) -> list[dict[str, Any]]:
        """Detect UI components used in the HTML."""
        components = []
        patterns = {
            "Card": (r'class="[^"]*rounded-[xl2]*[^"]*border[^"]*bg-card', "Card container with border and background"),
            "Table": (r"<table", "Data table"),
            "Button": (r"<button", "Interactive button"),
            "Input": (r'<input[^>]*type="text"', "Text input field"),
            "Badge": (r'class="[^"]*rounded-full[^"]*px-[23]', "Status badge"),
            "Avatar": (r'class="[^"]*rounded-full[^"]*h-[89]', "User avatar"),
            "Chart": (r"chart|sparkline|graph", "Data visualization"),
            "Navigation": (r"<nav|sidebar", "Navigation component"),
            "KPI": (r"tabular-nums.*font-bold|font-bold.*tabular-nums", "KPI metric display"),
            "Dropdown": (r"dropdown|select", "Dropdown/select control"),
        }

        for name, (pattern, desc) in patterns.items():
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                components.append({
                    "name": name,
                    "type": "shadcn" if name in ("Card", "Table", "Button", "Input", "Badge", "Avatar") else "custom",
                    "count": len(matches),
                    "notes": desc,
                })

        return components

    def _map_tokens(self, html: str, design_system: DesignSystemReport) -> dict[str, str]:
        """Map Tailwind classes found in the HTML to design tokens."""
        mapping = {}
        # Find all Tailwind color classes
        color_classes = re.findall(r"(?:bg|text|border|ring|shadow)-(?:[\w]+-\d+)", html)
        for cls in set(color_classes):
            # Map to design token if available
            for category, tokens in design_system.css_tokens.items():
                for token in tokens:
                    token_name = token.split(":")[0].strip()
                    if any(part in cls for part in token_name.split("-")):
                        mapping[cls] = token_name
                        break
        return mapping

    def _suggest_route(self, html: str, design_system: DesignSystemReport) -> str:
        """Suggest a route path based on the HTML content."""
        html_lower = html.lower()
        if "dashboard" in html_lower:
            return "/dashboard"
        if "transaction" in html_lower:
            return "/transactions"
        if "account" in html_lower:
            return "/accounts"
        if "setting" in html_lower:
            return "/settings"
        if "analytics" in html_lower or "chart" in html_lower:
            return "/analytics"
        if "landing" in html_lower or "hero" in html_lower:
            return "/"
        return "/dashboard"

    def _suggest_file_structure(self, framework: str, route: str) -> list[dict[str, str]]:
        """Suggest file structure based on framework and route."""
        route_clean = route.strip("/") or "dashboard"

        if framework in ("Next.js", "React Router", "Remix"):
            return [
                {"path": f"src/app/{route_clean}/page.tsx", "type": "page", "description": f"Main {route_clean} page"},
                {"path": f"src/app/{route_clean}/layout.tsx", "type": "layout", "description": f"Layout for {route_clean}"},
                {"path": f"src/components/{route_clean}/kpi-cards.tsx", "type": "component", "description": "KPI card grid"},
                {"path": f"src/components/{route_clean}/data-table.tsx", "type": "component", "description": "Data table"},
                {"path": f"src/components/{route_clean}/chart-section.tsx", "type": "component", "description": "Chart visualization"},
                {"path": f"src/hooks/use-{route_clean}-data.ts", "type": "hook", "description": "Data fetching hook"},
            ]
        elif framework in ("Vue", "Nuxt"):
            return [
                {"path": f"pages/{route_clean}.vue", "type": "page", "description": f"Main {route_clean} page"},
                {"path": f"components/{route_clean}/KpiCards.vue", "type": "component", "description": "KPI cards"},
                {"path": f"components/{route_clean}/DataTable.vue", "type": "component", "description": "Data table"},
                {"path": f"composables/use{route_clean.title()}Data.ts", "type": "composable", "description": "Data composable"},
            ]
        else:
            return [
                {"path": f"src/pages/{route_clean}.tsx", "type": "page", "description": f"Main {route_clean} page"},
                {"path": f"src/components/{route_clean}/", "type": "directory", "description": "Component directory"},
            ]

    def _suggest_imports(
        self, design_system: DesignSystemReport, components: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Suggest package imports based on detected components and design system."""
        imports = []

        if "shadcn/ui" in design_system.component_library:
            shadcn_items = []
            for comp in components:
                if comp.get("type") == "shadcn":
                    shadcn_items.append(comp["name"])
            if shadcn_items:
                imports.append({
                    "package": "@/components/ui",
                    "items": shadcn_items,
                    "note": "shadcn/ui components",
                })

        if any(c["name"] == "Chart" for c in components):
            imports.append({
                "package": "recharts",
                "items": ["LineChart", "Line", "XAxis", "YAxis", "Tooltip", "ResponsiveContainer"],
                "note": "Chart library for data visualization",
            })

        icon_lib = design_system.icons_library
        if icon_lib == "Lucide":
            imports.append({
                "package": "lucide-react",
                "items": ["TrendingUp", "TrendingDown", "DollarSign", "ArrowUpRight", "MoreHorizontal"],
                "note": "Icon library",
            })

        return imports

"""
Screenshot & Image Analyzer — vision-based UI decomposition using Claude Opus 4.6.

Analyzes screenshots and images to produce structured, ultra-detailed UI descriptions
optimized for generating award-winning fintech dashboards and web applications.
"""

from __future__ import annotations

import base64
import io
import json
import logging
import mimetypes
from pathlib import Path
from typing import Any

logger = logging.getLogger("ai-design-mcp")


FINTECH_ANALYSIS_SYSTEM_PROMPT = """\
You are a world-class UI/UX analyst from an award-winning design studio specializing in \
fintech dashboards, banking platforms, trading interfaces, and financial web applications.

Your analysis must be exhaustive, precise, and immediately actionable for a frontend \
developer to recreate the design pixel-perfectly using Tailwind CSS and modern component \
libraries (shadcn/ui, Radix).

You think like a senior design engineer at Linear, Stripe, Mercury, or Ramp.\
"""

SCREENSHOT_ANALYSIS_PROMPT = """\
Analyze this UI screenshot with extreme precision. Produce a comprehensive design \
specification document covering every visual element.

## Required Analysis Sections

### 1. Layout Architecture
- Overall grid system (columns, rows, gap values)
- Container widths, max-widths, padding
- Sidebar width and behavior (collapsible? fixed? overlay?)
- Header height, sticky behavior
- Content area structure (cards, sections, panels)
- Z-index layering (modals, dropdowns, toasts, tooltips)
- Responsive breakpoints implied by the layout

### 2. Navigation Structure
- Primary navigation: type (sidebar/topbar/tabs), items, icons, active states
- Secondary navigation: breadcrumbs, tabs, sub-menus
- User menu / profile section
- Mobile navigation pattern (hamburger, bottom nav, drawer)

### 3. Color System (extract exact values)
- Background colors (page, card, sidebar, header)
- Text colors (primary, secondary, muted, disabled)
- Brand/accent colors (primary, secondary)
- Semantic colors (success, warning, error, info)
- Border colors, divider colors
- Gradient specifications (direction, stops)
- Dark mode indicators (if applicable)

### 4. Typography System
- Font family (sans-serif, monospace for data)
- Heading sizes (h1-h6) with weights and line-heights
- Body text sizes and weights
- Label/caption sizes
- Monospace usage (numbers, codes, amounts)
- Letter spacing and text transforms

### 5. Component Inventory
For EACH visible component, describe:
- Component type (card, table, chart, form, button, badge, avatar, etc.)
- Exact dimensions and spacing (padding, margin, gap)
- Border radius values
- Shadow specifications (offset, blur, spread, color)
- States visible (default, hover, active, disabled, selected)
- Content structure within the component
- Icon usage (name/type, size, color)

### 6. Data Visualization
- Chart types (line, bar, area, donut, sparkline, candlestick)
- Axis labels, legends, tooltips
- Color coding for data series
- Grid lines and tick marks
- Number formatting (currency, percentage, abbreviations)
- Real-time indicators (live dots, streaming data)

### 7. Spacing & Rhythm
- Base spacing unit (4px, 8px grid)
- Section spacing
- Card internal padding
- Form field spacing
- Table cell padding
- Gap between elements in flex/grid layouts

### 8. Interactive Elements
- Button hierarchy (primary, secondary, ghost, destructive)
- Button sizes and padding
- Input field styles (border, focus ring, placeholder color)
- Dropdown/select styles
- Toggle/switch components
- Checkbox/radio styles
- Hover/focus states described

### 9. Fintech-Specific Elements
- Currency displays (symbol placement, decimal formatting)
- Percentage changes (up/down indicators, color coding)
- Account/card displays
- Transaction lists (format, grouping)
- KPI cards (value, label, trend, sparkline)
- Status badges (pending, completed, failed)
- Security indicators (verified, encrypted)

### 10. Micro-interactions & Motion
- Transition durations visible (fast/medium/slow)
- Animation patterns (fade, slide, scale)
- Loading states (skeleton, spinner, shimmer)
- Progress indicators

### 11. Tailwind CSS Specification
Provide the EXACT Tailwind classes you would use to recreate key layout containers \
and components. Be specific with:
- Exact color classes (slate-900, zinc-50, emerald-500, etc.)
- Exact spacing (p-6, gap-4, space-y-3, etc.)
- Exact typography (text-sm, font-medium, tracking-tight, etc.)
- Exact border radius (rounded-xl, rounded-2xl, etc.)
- Exact shadows (shadow-sm, shadow-lg, etc.)

### 12. Recommended shadcn/ui Components
Map each UI element to the closest shadcn/ui component:
- Card, CardHeader, CardContent, CardFooter
- Table, TableHeader, TableRow, TableCell
- Button, Badge, Avatar
- Tabs, TabsList, TabsTrigger, TabsContent
- DropdownMenu, Select, Input, Label
- Sheet, Dialog, Popover, Tooltip
- Chart (Recharts wrapper)
- Separator, ScrollArea, Skeleton

Output your analysis as a structured JSON object with all sections above as keys.\
"""

REFERENCE_MODE_PROMPTS = {
    "clone": """\
Analyze this UI with the goal of EXACT REPLICATION. I need to clone this design \
pixel-for-pixel. Extract every measurement, color value, font size, spacing, and \
component specification so the recreation is indistinguishable from the original. \
Focus on precision over interpretation.

{base_prompt}\
""",
    "enhance": """\
Analyze this UI with the goal of ENHANCEMENT. The current design has good bones \
but needs to be elevated to award-winning quality. For each element, describe:
1. What it currently looks like (exact specification)
2. What specific improvements would make it world-class
3. Modern fintech design patterns that could replace dated elements

Keep the same information architecture and goals, but propose premium visual \
treatments, better spacing, refined typography, and polished micro-interactions.

{base_prompt}\
""",
    "inspire": """\
Analyze this UI as INSPIRATION for a new design. Extract the design principles, \
visual language, and patterns that make it effective — but do NOT copy it directly. \
Instead, identify:
1. Color palette strategy (not exact values, but the approach)
2. Layout patterns worth borrowing
3. Typography hierarchy approach
4. Component patterns and interactions worth adapting
5. What makes this design feel premium/professional
6. How to adapt these principles for a fintech context

{base_prompt}\
""",
}


class ScreenshotAnalyzer:
    """Analyze UI screenshots and images using Claude's vision capabilities."""

    def __init__(self, anthropic_client):
        self.client = anthropic_client
        self.model = "claude-opus-4-6"

    async def analyze_image(
        self,
        image_source: str,
        mode: str = "analyze",
        context: str = "",
        design_system_context: str = "",
    ) -> dict[str, Any]:
        """
        Analyze a UI screenshot or image.

        Args:
            image_source: File path to image, base64 string, or URL
            mode: 'analyze' | 'clone' | 'enhance' | 'inspire'
            context: Additional user context about the design
            design_system_context: Detected design system info to match
        """
        image_content = await self._prepare_image(image_source)

        prompt = self._build_prompt(mode, context, design_system_context)

        messages = [
            {
                "role": "user",
                "content": [
                    image_content,
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        response = await self._call_vision(messages)
        return self._parse_analysis(response, mode)

    async def analyze_multiple(
        self,
        images: list[str],
        mode: str = "analyze",
        context: str = "",
    ) -> dict[str, Any]:
        """Analyze multiple screenshots for comprehensive app understanding."""
        content_blocks = []
        for i, img_src in enumerate(images):
            img_content = await self._prepare_image(img_src)
            content_blocks.append(img_content)
            content_blocks.append({
                "type": "text",
                "text": f"[Screenshot {i + 1} of {len(images)}]",
            })

        content_blocks.append({
            "type": "text",
            "text": f"""\
Analyze ALL {len(images)} screenshots as parts of the SAME application.
Produce a unified design specification covering:
1. Consistent design language across all screens
2. Shared component patterns
3. Color and typography system used throughout
4. Navigation flow between screens
5. Individual screen breakdowns

{SCREENSHOT_ANALYSIS_PROMPT}

Additional context: {context}""",
        })

        messages = [{"role": "user", "content": content_blocks}]
        response = await self._call_vision(messages)
        return self._parse_analysis(response, mode)

    async def _prepare_image(self, source: str) -> dict[str, Any]:
        """Convert image source to Claude vision API format."""
        # Base64 encoded string
        if source.startswith("data:image/"):
            media_type, data = source.split(";base64,", 1)
            media_type = media_type.replace("data:", "")
            return {
                "type": "image",
                "source": {"type": "base64", "media_type": media_type, "data": data},
            }

        # URL
        if source.startswith("http://") or source.startswith("https://"):
            return {
                "type": "image",
                "source": {"type": "url", "url": source},
            }

        # File path
        path = Path(source).resolve()
        if path.exists():
            mime = mimetypes.guess_type(str(path))[0] or "image/png"
            data = base64.b64encode(path.read_bytes()).decode("utf-8")
            return {
                "type": "image",
                "source": {"type": "base64", "media_type": mime, "data": data},
            }

        # Assume raw base64
        return {
            "type": "image",
            "source": {"type": "base64", "media_type": "image/png", "data": source},
        }

    def _build_prompt(self, mode: str, context: str, design_system_context: str) -> str:
        if mode in REFERENCE_MODE_PROMPTS:
            prompt = REFERENCE_MODE_PROMPTS[mode].format(base_prompt=SCREENSHOT_ANALYSIS_PROMPT)
        else:
            prompt = SCREENSHOT_ANALYSIS_PROMPT

        if design_system_context:
            prompt += f"\n\n## Your Project's Design System\n{design_system_context}\n\nEnsure your analysis maps to the existing design system above."

        if context:
            prompt += f"\n\n## Additional Context\n{context}"

        return prompt

    async def _call_vision(self, messages: list[dict]) -> str:
        """Call Claude's vision API."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=16000,
                system=FINTECH_ANALYSIS_SYSTEM_PROMPT,
                messages=messages,
            )
            return response.content[0].text
        except Exception as e:
            logger.error("Vision API call failed: %s", e)
            raise

    def _parse_analysis(self, raw: str, mode: str) -> dict[str, Any]:
        """Parse the analysis response, extracting JSON if present."""
        # Try to extract JSON from the response
        json_match = None
        if "```json" in raw:
            start = raw.index("```json") + 7
            end = raw.index("```", start)
            json_match = raw[start:end].strip()
        elif raw.strip().startswith("{"):
            json_match = raw.strip()

        result = {
            "mode": mode,
            "analysis": raw,
        }

        if json_match:
            try:
                result["structured"] = json.loads(json_match)
            except json.JSONDecodeError:
                pass

        return result

"""
Design Generator — produces complete, production-quality HTML+Tailwind designs
using Claude Opus 4.6 with fintech-grade design system awareness.
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .fintech_presets import (
    DASHBOARD_LAYOUT_TEMPLATES,
    FINTECH_COMPONENT_PATTERNS,
    FINTECH_DESIGN_TOKENS,
    get_design_context,
)

logger = logging.getLogger("ai-design-mcp")


DESIGN_SYSTEM_PROMPT = """\
You are an elite UI engineer from an award-winning fintech design studio. You produce \
pixel-perfect, production-ready HTML with Tailwind CSS that rivals the quality of \
Mercury, Stripe, Linear, and Ramp.

## Your Design Principles
1. **Visual Hierarchy** — Every element has a clear purpose. Important data is prominent.
2. **Whitespace** — Generous padding and margins create breathing room. Never cramped.
3. **Typography** — Precise font sizes, weights, and spacing. Tabular nums for data.
4. **Color with Purpose** — Semantic colors for states. Subtle backgrounds. No rainbow.
5. **Micro-details** — Subtle borders, shadows, transitions. Polish that users feel.
6. **Data Density** — Show maximum information without clutter. Fintech users need data.
7. **Accessibility** — Proper contrast ratios, focus states, semantic HTML.

## Technical Requirements
- Output a COMPLETE, standalone HTML document
- Use Tailwind CSS via CDN (include the script tag)
- Include Inter font from Google Fonts
- All styles via Tailwind utility classes (no custom CSS unless absolutely necessary)
- Responsive design (works on desktop, adapts to mobile)
- Use real-looking placeholder data (realistic names, amounts, dates)
- Include SVG icons inline (Lucide icon style) — no external icon dependencies
- Proper HTML5 semantic elements (nav, main, aside, section, article)
- tabular-nums for all numerical/financial data
- Use CSS custom properties for the color theme (easy to customize)

## Output Format
Return ONLY the complete HTML document. No markdown, no explanation, no code fences.
Start with <!DOCTYPE html> and end with </html>.\
"""


@dataclass
class DesignRun:
    run_id: str
    prompt: str
    html: str
    viewport: str
    preset: str
    template: str
    created_at: str
    reference_mode: str | None = None
    reference_source: str | None = None
    refinement_of: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "prompt": self.prompt,
            "viewport": self.viewport,
            "preset": self.preset,
            "template": self.template,
            "created_at": self.created_at,
            "reference_mode": self.reference_mode,
            "reference_source": self.reference_source,
            "refinement_of": self.refinement_of,
            "metadata": self.metadata,
        }


class DesignGenerator:
    """Generate production-quality fintech UI designs using Claude Opus 4.6."""

    def __init__(self, anthropic_client, storage_dir: str | Path = ".aidesigner"):
        self.client = anthropic_client
        self.model = "claude-opus-4-6"
        self.storage_dir = Path(storage_dir).resolve()
        self._runs: dict[str, DesignRun] = {}

    async def generate(
        self,
        prompt: str,
        viewport: str = "desktop",
        preset: str = "mercury",
        template: str = "overview",
        reference_mode: str | None = None,
        reference_source: str | None = None,
        design_system_context: str = "",
        screenshot_analysis: str = "",
    ) -> DesignRun:
        """Generate a complete UI design from a prompt."""
        run_id = self._make_run_id(prompt)

        # Build the generation prompt
        user_prompt = self._build_prompt(
            prompt=prompt,
            viewport=viewport,
            preset=preset,
            template=template,
            reference_mode=reference_mode,
            reference_source=reference_source,
            design_system_context=design_system_context,
            screenshot_analysis=screenshot_analysis,
        )

        html = await self._call_model(user_prompt)
        html = self._clean_html(html)

        run = DesignRun(
            run_id=run_id,
            prompt=prompt,
            html=html,
            viewport=viewport,
            preset=preset,
            template=template,
            created_at=datetime.utcnow().isoformat() + "Z",
            reference_mode=reference_mode,
            reference_source=reference_source,
            metadata={"model": self.model, "tokens_used": len(html)},
        )

        self._runs[run_id] = run
        await self._save_run(run)
        return run

    async def refine(
        self,
        run_id: str,
        feedback: str,
        reference_mode: str | None = None,
        reference_source: str | None = None,
        screenshot_analysis: str = "",
    ) -> DesignRun:
        """Refine an existing design with natural language feedback."""
        original = self._runs.get(run_id)
        if not original:
            original = await self._load_run(run_id)
        if not original:
            raise ValueError(f"Design run '{run_id}' not found. Available: {list(self._runs.keys())}")

        new_run_id = self._make_run_id(feedback)

        refinement_prompt = f"""## Original Design
You previously generated this HTML design:

```html
{original.html}
```

## Refinement Request
The user wants the following changes:
{feedback}

## Instructions
- Apply ONLY the requested changes
- Preserve everything else exactly as-is
- Maintain the same design system, color scheme, and visual quality
- Keep the same structure unless explicitly asked to change it
- Output the COMPLETE updated HTML document
"""
        if reference_mode and reference_source:
            refinement_prompt += f"""
## Reference
Mode: {reference_mode}
The user provided a reference: {reference_source}
"""
        if screenshot_analysis:
            refinement_prompt += f"""
## Screenshot Analysis
{screenshot_analysis}
"""

        html = await self._call_model(refinement_prompt)
        html = self._clean_html(html)

        run = DesignRun(
            run_id=new_run_id,
            prompt=feedback,
            html=html,
            viewport=original.viewport,
            preset=original.preset,
            template=original.template,
            created_at=datetime.utcnow().isoformat() + "Z",
            reference_mode=reference_mode,
            reference_source=reference_source,
            refinement_of=run_id,
            metadata={"model": self.model, "tokens_used": len(html)},
        )

        self._runs[new_run_id] = run
        await self._save_run(run)
        return run

    def _build_prompt(
        self,
        prompt: str,
        viewport: str,
        preset: str,
        template: str,
        reference_mode: str | None,
        reference_source: str | None,
        design_system_context: str,
        screenshot_analysis: str,
    ) -> str:
        parts = [f"## Design Request\n{prompt}\n"]

        # Viewport
        if viewport == "mobile":
            parts.append("## Viewport: Mobile (375px width)\nDesign for mobile-first. Single column layout, touch-friendly tap targets (min 44px), bottom navigation pattern.\n")
        else:
            parts.append("## Viewport: Desktop (1440px width)\nDesign for desktop with optional responsive breakpoints. Full sidebar navigation, multi-column layouts.\n")

        # Design tokens
        parts.append(get_design_context(preset, template))

        # Reference mode
        if reference_mode and reference_source:
            mode_labels = {
                "clone": "CLONE — Replicate this design as closely as possible",
                "enhance": "ENHANCE — Improve this design while keeping the same structure and goals",
                "inspire": "INSPIRE — Use this as inspiration, create something original",
            }
            parts.append(f"\n## Reference Mode: {mode_labels.get(reference_mode, reference_mode)}\nReference: {reference_source}\n")

        # Screenshot analysis
        if screenshot_analysis:
            parts.append(f"\n## Screenshot Analysis (from vision)\n{screenshot_analysis}\n")

        # Project design system
        if design_system_context:
            parts.append(f"\n## Project Design System (auto-detected)\n{design_system_context}\nEnsure the generated design aligns with this existing design system.\n")

        # Component patterns available
        parts.append(f"\n## Available Component Patterns for Reference\n{chr(10).join(f'- {name}' for name in FINTECH_COMPONENT_PATTERNS)}\n")

        return "\n".join(parts)

    async def _call_model(self, user_prompt: str) -> str:
        """Call Claude to generate HTML."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=32000,
            system=DESIGN_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text

    @staticmethod
    def _clean_html(html: str) -> str:
        """Strip markdown code fences if the model wrapped the output."""
        html = html.strip()
        if html.startswith("```html"):
            html = html[7:]
        elif html.startswith("```"):
            html = html[3:]
        if html.endswith("```"):
            html = html[:-3]
        html = html.strip()

        # Ensure it starts with DOCTYPE
        if not html.lower().startswith("<!doctype"):
            html = "<!DOCTYPE html>\n" + html

        return html

    def _make_run_id(self, prompt: str) -> str:
        ts = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        slug = re.sub(r"[^a-z0-9]+", "-", prompt.lower()[:40]).strip("-")
        return f"{ts}-{slug}"

    async def _save_run(self, run: DesignRun) -> None:
        """Save design run to local storage."""
        run_dir = self.storage_dir / run.run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        html_path = run_dir / "design.html"
        html_path.write_text(run.html, encoding="utf-8")

        meta_path = run_dir / "metadata.json"
        meta_path.write_text(json.dumps(run.to_dict(), indent=2), encoding="utf-8")

        logger.info("Saved design run: %s -> %s", run.run_id, run_dir)

    async def _load_run(self, run_id: str) -> DesignRun | None:
        """Load a design run from local storage."""
        run_dir = self.storage_dir / run_id
        if not run_dir.exists():
            # Search by partial match
            for d in self.storage_dir.iterdir():
                if d.is_dir() and run_id in d.name:
                    run_dir = d
                    break
            else:
                return None

        html_path = run_dir / "design.html"
        meta_path = run_dir / "metadata.json"

        if not html_path.exists():
            return None

        html = html_path.read_text(encoding="utf-8")
        meta = {}
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))

        run = DesignRun(
            run_id=meta.get("run_id", run_id),
            prompt=meta.get("prompt", ""),
            html=html,
            viewport=meta.get("viewport", "desktop"),
            preset=meta.get("preset", "mercury"),
            template=meta.get("template", "overview"),
            created_at=meta.get("created_at", ""),
            reference_mode=meta.get("reference_mode"),
            reference_source=meta.get("reference_source"),
            refinement_of=meta.get("refinement_of"),
            metadata=meta.get("metadata", {}),
        )
        self._runs[run.run_id] = run
        return run

    def list_runs(self) -> list[dict[str, Any]]:
        """List all saved design runs."""
        runs = []
        if self.storage_dir.exists():
            for d in sorted(self.storage_dir.iterdir(), reverse=True):
                meta_path = d / "metadata.json"
                if meta_path.exists():
                    try:
                        runs.append(json.loads(meta_path.read_text(encoding="utf-8")))
                    except Exception:
                        pass
        return runs

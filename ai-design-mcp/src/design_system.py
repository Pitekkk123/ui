"""
Design System Analyzer — repo-aware detection of frameworks, component libraries,
CSS tokens, route structures, and design conventions.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class DesignSystemReport:
    framework: str = "unknown"
    framework_version: str = ""
    css_strategy: str = "plain"
    component_library: list[str] = field(default_factory=list)
    css_tokens: dict[str, list[str]] = field(default_factory=dict)
    routes: list[str] = field(default_factory=list)
    tailwind_config: dict[str, Any] | None = None
    typography: dict[str, str] = field(default_factory=dict)
    color_palette: list[str] = field(default_factory=list)
    breakpoints: dict[str, str] = field(default_factory=dict)
    icons_library: str = ""
    state_management: str = ""
    build_tool: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "framework": self.framework,
            "frameworkVersion": self.framework_version,
            "cssStrategy": self.css_strategy,
            "componentLibrary": self.component_library,
            "cssTokens": self.css_tokens,
            "routes": self.routes,
            "tailwindConfig": self.tailwind_config,
            "typography": self.typography,
            "colorPalette": self.color_palette,
            "breakpoints": self.breakpoints,
            "iconsLibrary": self.icons_library,
            "stateManagement": self.state_management,
            "buildTool": self.build_tool,
        }

    def to_context_prompt(self) -> str:
        """Generate a prompt-friendly summary for design generation."""
        lines = [
            "## Detected Design System Context",
            f"- **Framework**: {self.framework} {self.framework_version}".strip(),
            f"- **CSS Strategy**: {self.css_strategy}",
        ]
        if self.component_library:
            lines.append(f"- **Component Libraries**: {', '.join(self.component_library)}")
        if self.color_palette:
            lines.append(f"- **Color Palette**: {', '.join(self.color_palette[:12])}")
        if self.typography:
            lines.append(f"- **Typography**: {json.dumps(self.typography)}")
        if self.breakpoints:
            lines.append(f"- **Breakpoints**: {json.dumps(self.breakpoints)}")
        if self.icons_library:
            lines.append(f"- **Icons**: {self.icons_library}")
        if self.state_management:
            lines.append(f"- **State Management**: {self.state_management}")
        if self.tailwind_config:
            lines.append(f"- **Tailwind Custom Config**: detected")
        if self.routes:
            lines.append(f"- **Routes** ({len(self.routes)} detected): {', '.join(self.routes[:10])}")
        return "\n".join(lines)


class DesignSystemAnalyzer:
    """Analyze a repository to detect its design system, framework, and conventions."""

    # Package → framework mapping
    FRAMEWORK_MAP = {
        "next": "Next.js",
        "react": "React",
        "vue": "Vue",
        "nuxt": "Nuxt",
        "svelte": "Svelte",
        "@sveltejs/kit": "SvelteKit",
        "astro": "Astro",
        "@angular/core": "Angular",
        "solid-js": "Solid",
        "react-router": "React Router",
        "@tanstack/react-router": "TanStack Router",
        "@remix-run/react": "Remix",
    }

    COMPONENT_LIBS = {
        "@radix-ui": "Radix UI",
        "shadcn": "shadcn/ui",
        "@shadcn/ui": "shadcn/ui",
        "@mui/material": "Material UI",
        "@chakra-ui": "Chakra UI",
        "antd": "Ant Design",
        "@mantine/core": "Mantine",
        "flowbite": "Flowbite",
        "@headlessui": "Headless UI",
        "daisyui": "DaisyUI",
        "@tremor/react": "Tremor",
        "primereact": "PrimeReact",
        "@nextui-org/react": "NextUI",
    }

    CSS_STRATEGIES = {
        "tailwindcss": "Tailwind CSS",
        "styled-components": "Styled Components",
        "@emotion/react": "Emotion",
        "sass": "Sass/SCSS",
        "@vanilla-extract/css": "Vanilla Extract",
        "postcss": "PostCSS",
        "css-modules": "CSS Modules",
    }

    STATE_MGMT = {
        "zustand": "Zustand",
        "jotai": "Jotai",
        "recoil": "Recoil",
        "@reduxjs/toolkit": "Redux Toolkit",
        "redux": "Redux",
        "mobx": "MobX",
        "pinia": "Pinia",
        "vuex": "Vuex",
        "xstate": "XState",
        "@tanstack/react-query": "TanStack Query",
    }

    ICON_LIBS = {
        "lucide-react": "Lucide",
        "react-icons": "React Icons",
        "@heroicons/react": "Heroicons",
        "@phosphor-icons/react": "Phosphor",
        "@tabler/icons-react": "Tabler Icons",
        "iconify": "Iconify",
    }

    BUILD_TOOLS = {
        "vite": "Vite",
        "turbo": "Turborepo",
        "webpack": "Webpack",
        "esbuild": "esbuild",
        "tsup": "tsup",
        "rollup": "Rollup",
    }

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()

    def analyze(self) -> DesignSystemReport:
        report = DesignSystemReport()
        all_deps = self._collect_all_deps()
        if all_deps:
            self._detect_framework(report, all_deps)
            self._detect_component_libs(report, all_deps)
            self._detect_css_strategy(report, all_deps)
            self._detect_state_management(report, all_deps)
            self._detect_icons(report, all_deps)
            self._detect_build_tool(report, all_deps)

        self._detect_tailwind_config(report)
        self._detect_css_tokens(report)
        self._detect_routes(report)
        return report

    def _collect_all_deps(self) -> dict[str, str]:
        """Collect dependencies from root and monorepo sub-packages."""
        all_deps: dict[str, str] = {}

        # Root package.json
        root_pkg = self._read_single_package_json(self.root / "package.json")
        if root_pkg:
            all_deps.update(root_pkg.get("dependencies", {}))
            all_deps.update(root_pkg.get("devDependencies", {}))

        # Scan common monorepo sub-paths
        sub_paths = [
            "apps/web", "apps/v4", "apps/app", "apps/dashboard",
            "packages/ui", "packages/app", "packages/shadcn",
            "packages/design-system", "src",
        ]
        for sub in sub_paths:
            sub_pkg = self._read_single_package_json(self.root / sub / "package.json")
            if sub_pkg:
                all_deps.update(sub_pkg.get("dependencies", {}))
                all_deps.update(sub_pkg.get("devDependencies", {}))

        return all_deps

    def _read_single_package_json(self, path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _detect_framework(self, report: DesignSystemReport, deps: dict) -> None:
        for pkg, name in self.FRAMEWORK_MAP.items():
            if pkg in deps:
                report.framework = name
                version = deps[pkg]
                report.framework_version = version.lstrip("^~>=<")
                return

    def _detect_component_libs(self, report: DesignSystemReport, deps: dict) -> None:
        for pkg, name in self.COMPONENT_LIBS.items():
            for dep_key in deps:
                if dep_key == pkg or dep_key.startswith(pkg + "/"):
                    if name not in report.component_library:
                        report.component_library.append(name)

        # Check for shadcn by looking for components.json
        components_json = self.root / "components.json"
        if components_json.exists() and "shadcn/ui" not in report.component_library:
            report.component_library.append("shadcn/ui")

    def _detect_css_strategy(self, report: DesignSystemReport, deps: dict) -> None:
        for pkg, name in self.CSS_STRATEGIES.items():
            if pkg in deps:
                report.css_strategy = name
                return

    def _detect_state_management(self, report: DesignSystemReport, deps: dict) -> None:
        for pkg, name in self.STATE_MGMT.items():
            if pkg in deps:
                report.state_management = name
                return

    def _detect_icons(self, report: DesignSystemReport, deps: dict) -> None:
        for pkg, name in self.ICON_LIBS.items():
            if pkg in deps:
                report.icons_library = name
                return

    def _detect_build_tool(self, report: DesignSystemReport, deps: dict) -> None:
        for pkg, name in self.BUILD_TOOLS.items():
            if pkg in deps:
                report.build_tool = name
                return

    def _detect_tailwind_config(self, report: DesignSystemReport) -> None:
        tw_files = [
            "tailwind.config.js", "tailwind.config.ts",
            "tailwind.config.cjs", "tailwind.config.mjs",
        ]
        for f in tw_files:
            tw_path = self.root / f
            if tw_path.exists():
                content = tw_path.read_text(encoding="utf-8", errors="ignore")
                report.tailwind_config = {"file": f, "hasCustomTheme": "theme" in content}

                # Extract colors
                color_matches = re.findall(
                    r"['\"]?([\w-]+)['\"]?\s*:\s*['\"]?(#[0-9a-fA-F]{3,8})['\"]?",
                    content,
                )
                for name, hex_val in color_matches:
                    report.color_palette.append(f"{name}: {hex_val}")

                # Extract breakpoints
                bp_matches = re.findall(
                    r"['\"]?(sm|md|lg|xl|2xl|xs|3xl)['\"]?\s*:\s*['\"]?(\d+(?:px|rem|em))['\"]?",
                    content,
                )
                for bp_name, bp_val in bp_matches:
                    report.breakpoints[bp_name] = bp_val

                break

    def _detect_css_tokens(self, report: DesignSystemReport) -> None:
        """Scan CSS files for custom properties (design tokens)."""
        css_dirs = [
            self.root / "src" / "styles",
            self.root / "src" / "app",
            self.root / "app",
            self.root / "styles",
            self.root / "src",
        ]
        token_re = re.compile(r"--([\w-]+)\s*:\s*([^;]+);")

        for css_dir in css_dirs:
            if not css_dir.exists():
                continue
            for css_file in css_dir.rglob("*.css"):
                try:
                    content = css_file.read_text(encoding="utf-8", errors="ignore")
                    for match in token_re.finditer(content):
                        token_name = match.group(1)
                        token_val = match.group(2).strip()
                        category = self._categorize_token(token_name)
                        if category not in report.css_tokens:
                            report.css_tokens[category] = []
                        entry = f"--{token_name}: {token_val}"
                        if entry not in report.css_tokens[category]:
                            report.css_tokens[category].append(entry)

                        # Extract typography tokens
                        if "font" in token_name.lower():
                            report.typography[token_name] = token_val
                except Exception:
                    pass

    @staticmethod
    def _categorize_token(name: str) -> str:
        name_lower = name.lower()
        if any(k in name_lower for k in ("color", "bg", "foreground", "background", "primary", "secondary", "accent", "muted", "destructive", "border")):
            return "colors"
        if any(k in name_lower for k in ("font", "text", "heading", "body", "line-height", "letter-spacing")):
            return "typography"
        if any(k in name_lower for k in ("radius", "rounded")):
            return "radii"
        if any(k in name_lower for k in ("space", "gap", "padding", "margin", "size")):
            return "spacing"
        if any(k in name_lower for k in ("shadow", "elevation")):
            return "shadows"
        if any(k in name_lower for k in ("z-index", "layer")):
            return "layers"
        return "other"

    def _detect_routes(self, report: DesignSystemReport) -> None:
        """Detect routes from file-system routing (Next.js, Astro, etc.)."""
        route_dirs = [
            (self.root / "app", "App Router"),
            (self.root / "src" / "app", "App Router"),
            (self.root / "pages", "Pages Router"),
            (self.root / "src" / "pages", "Pages Router"),
            (self.root / "src" / "routes", "File Routes"),
        ]

        for route_dir, _style in route_dirs:
            if not route_dir.exists():
                continue
            for item in sorted(route_dir.rglob("*")):
                if item.is_file() and item.suffix in (".tsx", ".jsx", ".ts", ".js", ".astro", ".svelte", ".vue"):
                    rel = item.relative_to(route_dir)
                    route = "/" + str(rel.with_suffix("")).replace("\\", "/")
                    # Normalize Next.js conventions
                    route = route.replace("/page", "").replace("/layout", " [layout]")
                    route = route.replace("/loading", " [loading]").replace("/error", " [error]")
                    if route and route not in report.routes:
                        report.routes.append(route)
            break  # Use first found route dir

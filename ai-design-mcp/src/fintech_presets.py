"""
Fintech Design System Presets — award-winning design tokens, component patterns,
and layout templates for financial dashboards and web applications.
"""

from __future__ import annotations

FINTECH_DESIGN_TOKENS = {
    "mercury": {
        "name": "Mercury (Banking)",
        "colors": {
            "background": "#09090b",
            "surface": "#18181b",
            "surfaceRaised": "#27272a",
            "border": "#3f3f46",
            "borderSubtle": "#27272a",
            "textPrimary": "#fafafa",
            "textSecondary": "#a1a1aa",
            "textMuted": "#71717a",
            "primary": "#6366f1",
            "primaryHover": "#818cf8",
            "success": "#22c55e",
            "successMuted": "rgba(34,197,94,0.15)",
            "danger": "#ef4444",
            "dangerMuted": "rgba(239,68,68,0.15)",
            "warning": "#f59e0b",
            "info": "#3b82f6",
        },
        "typography": {
            "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
            "monoFamily": "'JetBrains Mono', 'SF Mono', monospace",
            "h1": "text-3xl font-bold tracking-tight",
            "h2": "text-2xl font-semibold tracking-tight",
            "h3": "text-lg font-semibold",
            "body": "text-sm font-normal",
            "caption": "text-xs font-medium text-zinc-500",
            "mono": "font-mono text-sm tabular-nums",
        },
        "spacing": {"base": "4px", "card": "p-6", "section": "space-y-6", "gap": "gap-4"},
        "radii": {"sm": "rounded-md", "md": "rounded-lg", "lg": "rounded-xl", "full": "rounded-full"},
        "shadows": {
            "card": "shadow-sm shadow-black/10",
            "elevated": "shadow-lg shadow-black/20",
            "glow": "shadow-lg shadow-indigo-500/10",
        },
    },
    "stripe": {
        "name": "Stripe (Payments)",
        "colors": {
            "background": "#f6f9fc",
            "surface": "#ffffff",
            "surfaceRaised": "#ffffff",
            "border": "#e3e8ee",
            "borderSubtle": "#f0f2f5",
            "textPrimary": "#1a1f36",
            "textSecondary": "#697386",
            "textMuted": "#8792a2",
            "primary": "#635bff",
            "primaryHover": "#7a73ff",
            "success": "#3ecf8e",
            "successMuted": "rgba(62,207,142,0.12)",
            "danger": "#ed5f74",
            "dangerMuted": "rgba(237,95,116,0.12)",
            "warning": "#f5be31",
            "info": "#5469d4",
        },
        "typography": {
            "fontFamily": "'Inter', -apple-system, sans-serif",
            "monoFamily": "'SF Mono', 'Fira Code', monospace",
            "h1": "text-3xl font-semibold tracking-tight text-slate-900",
            "h2": "text-xl font-semibold text-slate-800",
            "h3": "text-base font-medium text-slate-700",
            "body": "text-sm text-slate-600",
            "caption": "text-xs font-medium text-slate-400",
            "mono": "font-mono text-sm tabular-nums",
        },
        "spacing": {"base": "4px", "card": "p-6", "section": "space-y-8", "gap": "gap-6"},
        "radii": {"sm": "rounded-md", "md": "rounded-lg", "lg": "rounded-xl", "full": "rounded-full"},
        "shadows": {
            "card": "shadow-sm ring-1 ring-black/5",
            "elevated": "shadow-md ring-1 ring-black/5",
            "glow": "shadow-xl shadow-indigo-500/5",
        },
    },
    "ramp": {
        "name": "Ramp (Expense Management)",
        "colors": {
            "background": "#fafafa",
            "surface": "#ffffff",
            "surfaceRaised": "#ffffff",
            "border": "#e5e5e5",
            "borderSubtle": "#f5f5f5",
            "textPrimary": "#0a0a0a",
            "textSecondary": "#525252",
            "textMuted": "#a3a3a3",
            "primary": "#eab308",
            "primaryHover": "#facc15",
            "success": "#16a34a",
            "successMuted": "rgba(22,163,74,0.1)",
            "danger": "#dc2626",
            "dangerMuted": "rgba(220,38,38,0.1)",
            "warning": "#ea580c",
            "info": "#2563eb",
        },
        "typography": {
            "fontFamily": "'Inter', system-ui, sans-serif",
            "monoFamily": "'IBM Plex Mono', monospace",
            "h1": "text-4xl font-bold tracking-tighter",
            "h2": "text-2xl font-bold tracking-tight",
            "h3": "text-lg font-semibold",
            "body": "text-sm leading-relaxed",
            "caption": "text-xs font-medium uppercase tracking-wider text-neutral-500",
            "mono": "font-mono text-sm tabular-nums slashed-zero",
        },
        "spacing": {"base": "4px", "card": "p-5", "section": "space-y-6", "gap": "gap-5"},
        "radii": {"sm": "rounded", "md": "rounded-lg", "lg": "rounded-2xl", "full": "rounded-full"},
        "shadows": {
            "card": "shadow-sm border",
            "elevated": "shadow-lg",
            "glow": "shadow-xl shadow-yellow-500/5",
        },
    },
    "linear": {
        "name": "Linear (Dark Premium)",
        "colors": {
            "background": "#0a0a0a",
            "surface": "#141414",
            "surfaceRaised": "#1e1e1e",
            "border": "#2e2e2e",
            "borderSubtle": "#1e1e1e",
            "textPrimary": "#eeeeee",
            "textSecondary": "#9e9e9e",
            "textMuted": "#666666",
            "primary": "#5e6ad2",
            "primaryHover": "#7b84e0",
            "success": "#4dba87",
            "successMuted": "rgba(77,186,135,0.15)",
            "danger": "#e5484d",
            "dangerMuted": "rgba(229,72,77,0.15)",
            "warning": "#ffb224",
            "info": "#52a9ff",
        },
        "typography": {
            "fontFamily": "'Inter', -apple-system, sans-serif",
            "monoFamily": "'JetBrains Mono', monospace",
            "h1": "text-2xl font-medium",
            "h2": "text-lg font-medium",
            "h3": "text-sm font-medium",
            "body": "text-sm text-[#9e9e9e]",
            "caption": "text-xs text-[#666]",
            "mono": "font-mono text-xs tabular-nums",
        },
        "spacing": {"base": "4px", "card": "p-4", "section": "space-y-4", "gap": "gap-3"},
        "radii": {"sm": "rounded", "md": "rounded-lg", "lg": "rounded-xl", "full": "rounded-full"},
        "shadows": {
            "card": "shadow-none border border-[#2e2e2e]",
            "elevated": "shadow-xl shadow-black/50",
            "glow": "shadow-lg shadow-indigo-500/10",
        },
    },
}

FINTECH_COMPONENT_PATTERNS = {
    "kpi_card": """\
<!-- KPI Card -->
<div class="rounded-xl border bg-card p-6 space-y-2">
  <div class="flex items-center justify-between">
    <span class="text-xs font-medium text-muted-foreground uppercase tracking-wider">{{label}}</span>
    <svg class="h-4 w-4 text-muted-foreground"><!-- icon --></svg>
  </div>
  <div class="flex items-baseline gap-2">
    <span class="text-2xl font-bold tabular-nums tracking-tight">{{value}}</span>
    <span class="text-xs font-medium {{trend_color}} flex items-center gap-0.5">
      {{trend_icon}} {{trend_value}}
    </span>
  </div>
  <p class="text-xs text-muted-foreground">{{description}}</p>
</div>""",
    "transaction_row": """\
<!-- Transaction Row -->
<div class="flex items-center justify-between py-3 px-4 hover:bg-muted/50 transition-colors rounded-lg">
  <div class="flex items-center gap-3">
    <div class="h-9 w-9 rounded-full bg-muted flex items-center justify-center">
      <span class="text-sm">{{icon}}</span>
    </div>
    <div>
      <p class="text-sm font-medium">{{merchant}}</p>
      <p class="text-xs text-muted-foreground">{{category}} · {{date}}</p>
    </div>
  </div>
  <div class="text-right">
    <p class="text-sm font-semibold tabular-nums {{amount_color}}">{{amount}}</p>
    <p class="text-xs text-muted-foreground">{{status}}</p>
  </div>
</div>""",
    "chart_card": """\
<!-- Chart Card -->
<div class="rounded-xl border bg-card p-6 space-y-4">
  <div class="flex items-center justify-between">
    <div>
      <h3 class="text-sm font-medium">{{title}}</h3>
      <p class="text-2xl font-bold tabular-nums tracking-tight mt-1">{{value}}</p>
    </div>
    <div class="flex items-center gap-2">
      <button class="text-xs px-2.5 py-1 rounded-md bg-primary text-primary-foreground font-medium">7D</button>
      <button class="text-xs px-2.5 py-1 rounded-md text-muted-foreground hover:bg-muted">1M</button>
      <button class="text-xs px-2.5 py-1 rounded-md text-muted-foreground hover:bg-muted">1Y</button>
    </div>
  </div>
  <div class="h-[200px] w-full">
    <!-- Chart area: Recharts / D3 / Chart.js -->
    <div class="w-full h-full bg-gradient-to-b from-primary/10 to-transparent rounded-lg flex items-end">
      {{chart_placeholder}}
    </div>
  </div>
</div>""",
    "account_card": """\
<!-- Account Card -->
<div class="rounded-2xl bg-gradient-to-br from-primary to-primary/80 text-primary-foreground p-6 space-y-6 relative overflow-hidden">
  <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.1),transparent_50%)]"></div>
  <div class="relative">
    <p class="text-xs font-medium opacity-80">{{account_type}}</p>
    <p class="text-sm mt-1 opacity-90">{{account_name}}</p>
  </div>
  <div class="relative">
    <p class="text-3xl font-bold tabular-nums tracking-tight">{{balance}}</p>
    <p class="text-xs mt-1 opacity-70">Available balance</p>
  </div>
  <div class="relative flex justify-between items-end">
    <p class="text-sm font-mono tracking-widest opacity-80">•••• {{last_four}}</p>
    <div class="text-2xl font-bold opacity-80">{{card_brand}}</div>
  </div>
</div>""",
    "sidebar_nav": """\
<!-- Sidebar Navigation -->
<aside class="w-[260px] h-screen border-r bg-sidebar flex flex-col">
  <div class="p-4 border-b">
    <div class="flex items-center gap-2">
      <div class="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
        <span class="text-sm font-bold text-primary-foreground">{{logo}}</span>
      </div>
      <span class="text-sm font-semibold">{{app_name}}</span>
    </div>
  </div>
  <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
    {{nav_items}}
  </nav>
  <div class="p-3 border-t">
    <div class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-muted transition-colors">
      <div class="h-8 w-8 rounded-full bg-muted"></div>
      <div class="flex-1 min-w-0">
        <p class="text-sm font-medium truncate">{{user_name}}</p>
        <p class="text-xs text-muted-foreground truncate">{{user_email}}</p>
      </div>
    </div>
  </div>
</aside>""",
    "data_table": """\
<!-- Data Table -->
<div class="rounded-xl border bg-card overflow-hidden">
  <div class="flex items-center justify-between p-4 border-b">
    <h3 class="text-sm font-semibold">{{title}}</h3>
    <div class="flex items-center gap-2">
      <div class="relative">
        <input type="text" placeholder="Search..." class="h-8 w-[200px] rounded-md border bg-transparent px-3 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring" />
      </div>
      <button class="h-8 px-3 rounded-md border text-xs font-medium hover:bg-muted transition-colors">Filter</button>
      <button class="h-8 px-3 rounded-md bg-primary text-primary-foreground text-xs font-medium">Export</button>
    </div>
  </div>
  <table class="w-full">
    <thead>
      <tr class="border-b bg-muted/50">
        {{table_headers}}
      </tr>
    </thead>
    <tbody class="divide-y">
      {{table_rows}}
    </tbody>
  </table>
  <div class="flex items-center justify-between p-4 border-t">
    <p class="text-xs text-muted-foreground">Showing 1-10 of {{total}} results</p>
    <div class="flex items-center gap-1">
      {{pagination}}
    </div>
  </div>
</div>""",
}

DASHBOARD_LAYOUT_TEMPLATES = {
    "overview": {
        "name": "Executive Overview Dashboard",
        "description": "4 KPI cards on top, main chart center, recent activity sidebar",
        "grid": "grid grid-cols-12 gap-6",
        "sections": [
            {"name": "KPI Row", "span": "col-span-12", "layout": "grid grid-cols-4 gap-4"},
            {"name": "Main Chart", "span": "col-span-8", "layout": ""},
            {"name": "Activity Feed", "span": "col-span-4", "layout": "space-y-3"},
            {"name": "Data Table", "span": "col-span-12", "layout": ""},
        ],
    },
    "analytics": {
        "name": "Analytics Deep Dive",
        "description": "2-column charts with filters, dense data visualization",
        "grid": "grid grid-cols-12 gap-6",
        "sections": [
            {"name": "Filters Bar", "span": "col-span-12", "layout": "flex items-center gap-3"},
            {"name": "Primary Chart", "span": "col-span-7", "layout": ""},
            {"name": "Breakdown", "span": "col-span-5", "layout": "space-y-4"},
            {"name": "Chart Row", "span": "col-span-12", "layout": "grid grid-cols-3 gap-4"},
        ],
    },
    "accounts": {
        "name": "Accounts & Cards",
        "description": "Account cards, transaction list, spending breakdown",
        "grid": "grid grid-cols-12 gap-6",
        "sections": [
            {"name": "Account Cards", "span": "col-span-12", "layout": "grid grid-cols-3 gap-4"},
            {"name": "Transactions", "span": "col-span-8", "layout": ""},
            {"name": "Spending", "span": "col-span-4", "layout": "space-y-4"},
        ],
    },
    "trading": {
        "name": "Trading Terminal",
        "description": "Candlestick chart, order book, positions, watchlist",
        "grid": "grid grid-cols-12 gap-2",
        "sections": [
            {"name": "Toolbar", "span": "col-span-12", "layout": "flex items-center gap-2"},
            {"name": "Chart", "span": "col-span-8 row-span-2", "layout": ""},
            {"name": "Order Book", "span": "col-span-4", "layout": ""},
            {"name": "Positions", "span": "col-span-4", "layout": ""},
            {"name": "Trade Form", "span": "col-span-12", "layout": "grid grid-cols-2 gap-4"},
        ],
    },
}


def get_design_context(preset: str = "mercury", template: str = "overview") -> str:
    """Generate a rich design context string for the AI model."""
    tokens = FINTECH_DESIGN_TOKENS.get(preset, FINTECH_DESIGN_TOKENS["mercury"])
    layout = DASHBOARD_LAYOUT_TEMPLATES.get(template, DASHBOARD_LAYOUT_TEMPLATES["overview"])

    return f"""## Design System: {tokens['name']}

### Color Palette
{_format_dict(tokens['colors'])}

### Typography
{_format_dict(tokens['typography'])}

### Spacing
{_format_dict(tokens['spacing'])}

### Border Radius
{_format_dict(tokens['radii'])}

### Shadows
{_format_dict(tokens['shadows'])}

## Layout Template: {layout['name']}
{layout['description']}
Grid: `{layout['grid']}`

### Sections
{_format_sections(layout['sections'])}

## Available Component Patterns
{', '.join(FINTECH_COMPONENT_PATTERNS.keys())}
"""


def _format_dict(d: dict) -> str:
    return "\n".join(f"- **{k}**: `{v}`" for k, v in d.items())


def _format_sections(sections: list[dict]) -> str:
    return "\n".join(
        f"- **{s['name']}**: `{s['span']}` — layout: `{s['layout']}`"
        for s in sections
    )

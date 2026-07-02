# CLAUDE.md — ui (fork shadcn/ui) + DESIGN FOUNDRY OS

Fork `shadcn/ui` używany jako baza komponentowa do projektów UI operatora. Repo-level
instrukcje dla Claude Code.

## Struktura

- `apps/v4` — strona dokumentacji + registry (Next.js); `registry/` i `registry.json` = źródło
  komponentów, bloków i przykładów.
- `packages/shadcn` — CLI `shadcn`.
- `templates/` — szablony startowe (next, vite, astro, react-router, start; app i monorepo).
- `skills/shadcn` — skill upstream od mechaniki komponentów (kompozycja, formularze, styling,
  base vs radix, ikony). Utrzymuj zgodność z upstream przy synchronizacji.
- `.claude/skills/design-foundry-os` — konstytucja designu tego repo (niżej).

## Komendy

`pnpm install` → `pnpm v4:dev` (dokumentacja/registry, port 4000) • `pnpm check`
(lint + typecheck + format) • `pnpm test` • `pnpm registry:build` po zmianach w registry.
Package manager: **pnpm** (zob. `packageManager` w package.json).

Praca wizualna: **`/design`** (`.claude/commands/design.md`) — drzewko decyzyjne z polami
wyboru prowadzące od briefu do właściwego trybu; nie wymaga znajomości skilli.

## Design — DESIGN FOUNDRY OS (nadrzędne przy każdej pracy wizualnej)

**Słowo „design" (i każde zadanie, którego wynik się ogląda) → wczytaj NAJPIERW indeks pamięci
designu `.claude/skills/design-foundry-os/references/14_design_memory_index.md`** (katalog
kanoniczny: preferencje estetyczne, artefakty, toolchain, bramki), a zaraz po nim główną bazę
estetyczną `references/13_fintech_style_profile.md`. Standing directives operatora: **zawsze
proponuj najlepsze i najładniejsze rozwiązanie** (nie pierwsze poprawne) i **bezwzględnie unikaj
AI Slope** (rejestr `references/11` + bramka `references/04`, ≥2 sygnatury = redesign).

Każde zadanie, którego wynik jest oglądany (komponent, blok, motyw, strona, dashboard, demo,
prezentacja, grafika, redesign — także color-only), podlega konstytucji
`.claude/skills/design-foundry-os/references/00_constitution.md`; warstwę egzekucji definiuje
skill `design-foundry-os` (bramka anti-AI-slop, alignment gate, brief, obowiązkowe stany,
matryca urządzeń, adversarial review).

Zasady szczególne dla tego repo:

- **shadcn/ui = zachowanie, dostępność, primitives. Nigdy art direction.** Końcowy język
  wizualny produktu ma być własny — budowany tokenami, typografią, gridem, rytmem i skalą.
- Mechanika komponentów → skill `shadcn`; „co i po co powstaje oraz jak ma wyglądać" →
  DESIGN FOUNDRY OS. Nowy design system / DESIGN.md → skill `design-consultation`;
  projekty o wysokiej stawce → tryb turniejowy
  (`.claude/skills/design-foundry-os/references/10_master_system_prompt.md`).
- ≥2 sygnatury z automatycznej bramki odrzucenia (dark SaaS + neon, gradientowy headline,
  karta-w-karcie, badges wszędzie, modal-aplikacja, ściana checkboxów…) = redesign od podstaw,
  nie kosmetyka.
- Show, don't claim: „responsywne / dostępne / przetestowane" tylko po faktycznej weryfikacji;
  raportuj czego nie sprawdzono.

## Higiena zmian

- Nie zmieniaj plików upstream (komponenty, registry, CLI) przy zadaniach czysto
  instruktażowych; zmiany w registry zawsze przez `pnpm registry:build` + testy.
- Nie commituj sekretów ani realnych danych; dane przykładowe w demach oznaczaj jako
  przykładowe.
- Commituj logiczne kroki z jasnym opisem; PR jako draft.

## Język

Odpowiadaj po polsku; terminologię techniczną (registry, primitives, tokens, tree-shaking)
zostawiaj w oryginale. Kod, identyfikatory i komunikaty commitów — po angielsku, zgodnie
z konwencją upstream.

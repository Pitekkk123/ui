# CLAUDE.md — apps/v4

Dokumentacja i registry. Next.js 16.1.6 + React 19.2.3, app router, Turbopack, port **4000**.
Uzupełnia root `CLAUDE.md` — nie powtarza go.

## Uruchamianie

`pnpm v4:dev` z roota (albo `pnpm dev` tutaj) buduje registry, startuje watcher ikon i podnosi
Next na 4000. `pnpm preview` robi pełny przebieg: registry → build → start.

## Registry — źródło prawdy komponentów

`registry.json` ma 411 pozycji i jest manifestem; `registry/` trzyma ich kod.

- **Po każdej zmianie w `registry/` uruchom `pnpm registry:build`.** Ten skrypt najpierw buduje
  pakiet `shadcn` (`pnpm --filter=shadcn build`), potem generuje registry przez **bun** —
  bun jest twardą zależnością tego kroku, nie zamiennikiem pnpm.
- `pnpm validate:registries` waliduje manifest. Puszczaj je przed PR-em.
- `registry/__index__.tsx` i `registry/__blocks__.json` są **generowane** — nie edytuj ręcznie.

### Parzystość bases/base ↔ bases/radix

`registry/bases/base` i `registry/bases/radix` to rejestry równoległe. Zmiana po jednej stronie
wymaga tej samej zmiany behawioralnej i wizualnej po drugiej — rozjazd dopuszczalny tylko tam,
gdzie API faktycznie się różni (ścieżki importu, propsy Base UI vs Radix).

Reguła żyje w `.cursor/rules/registry-bases-parity.mdc` (doradczo, tylko w Cursorze) oraz jako
hook `PostToolUse`, który po edycji jednej strony wskazuje ścieżkę lustrzaną. Hook raportuje —
nie blokuje; decyzja o rozjeździe należy do Ciebie, ale trzeba ją uzasadnić.

## Treść

`content/` przechodzi przez `fumadocs-mdx` (`postinstall`). Po zmianach w strukturze treści
przeinstaluj albo puść build, żeby regenerować typy.

## Bramki

`pnpm typecheck` (tsc --noEmit) • `pnpm lint` (eslint z cache) • `pnpm format:check`.
Typecheck całego workspace'u odpala się też automatycznie na koniec tury (hook `Stop`).

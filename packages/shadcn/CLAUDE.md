# CLAUDE.md — packages/shadcn

CLI `shadcn`. Uzupełnia root `CLAUDE.md` — nie powtarza go.

## Build ma konsekwencje poza tym pakietem

`pnpm build` to **tsup** (ESM, minify, dts, `clean: true`) do `dist/`. Wejścia deklaruje
`tsup.config.ts`: `index`, `registry`, `schema`, `mcp`, `utils`, `icons`, `preset`.

Dwie rzeczy zależą od tego, czy `dist/` istnieje:

1. `apps/v4` → `registry:build` buduje ten pakiet jako pierwszy krok.
2. **Prettier całego repo.** `prettier-plugin-tailwindcss` rozwiązuje `shadcn/tailwind.css`
   przez exports tego pakietu, czyli przez `dist/`. Na świeżym klonie, przed pierwszym buildem,
   prettier pada na **każdym** pliku z `Can't resolve 'shadcn/tailwind.css'`. Lekarstwo:
   `pnpm --filter=shadcn build`. Hook formatujący wykrywa ten stan i mówi o nim wprost, zamiast
   milczeć.

## Struktura

`src/commands/` — `add`, `init`, `build`, `diff`, `migrate`, `search`, `view`, `info`, `docs`,
`apply`, `mcp`. `src/migrations/` — kodmody (radix, icons, rtl). `src/preflights/` — kontrole
przed wykonaniem komendy. `src/registry/`, `src/schema/`, `src/preset/`, `src/styles/`.

## Testy

65 plików `*.test.ts` obok kodu, vitest. `pnpm test` z roota wymaga działającego serwera v4
(`start-server-and-test` na 4000); tutaj `pnpm test` uruchamia sam pakiet.

Kodmody testuj na fixture'ach — `**/fixtures` jest wyłączone z workspace'u i z prettiera,
więc nie formatuj ich ani nie traktuj jako źródła.

# 14 — INDEKS PAMIĘCI DESIGNU (katalog kanoniczny — czytaj PIERWSZY na słowo „design")

**Punkt wejścia całej pamięci designowej operatora w repo `ui`.** Kiedy padnie słowo
**„design"** (albo gdy startuje jakiekolwiek zadanie, którego wynik się ogląda) — otwórz TEN
plik jako pierwszy, potem główną bazę estetyczną `references/13_fintech_style_profile.md`,
dopiero potem resztę. Ten dokument nic nie zastępuje; jest indeksem, klasyfikacją i skrótem do
wszystkiego, co zostało ustalone. Zmieniło się coś w ustaleniach designowych → zaktualizuj też
ten indeks.

## 0. Standing directives operatora (obowiązują zawsze, bez przypominania)

1. **„design" = wczytaj tę pamięć.** Na to słowo masz pod ręką: preferencje estetyczne (sekcja 3),
   pełny katalog artefaktów (sekcja 2), toolchain (sekcja 4), bramki jakości (sekcja 5).
2. **Zawsze proponuj najlepsze i najładniejsze rozwiązanie** — nie pierwsze poprawne, nie
   bezpieczne domyślne. Wyższa stawka → więcej koncepcji (standard 3, turniej 6).
3. **Unikaj AI Slope bezwzględnie** — rejestr `references/11_slop_signatures_registry.md` +
   bramka odrzucenia `references/04`. ≥2 sygnatury = redesign od podstaw, nie kosmetyka.
4. **Show, don't claim** — „responsywne / dostępne / przetestowane" tylko po faktycznej
   weryfikacji (`pnpm check` + `pnpm test`); zawsze rozdzielaj wykonane / przetestowane /
   niezweryfikowane.
5. **Perfekcja w każdym calu** — kolory wyliczone i zharmonizowane („estetyczna poezja", zero
   przypadkowych hexów); pięć regresji wykonawczych (sekcja 3.6) sprawdzasz przed KAŻDYM oddaniem.
6. Precedencja: **jawna decyzja operatora > konstytucja (references/00) > warianty 08/10 >
   skille > referencje**; rejestr sygnatur nadpisuje pojedyncze punkty konstytucji tam, gdzie
   zaznaczono (np. Inter ≠ głos marki).
7. **shadcn/ui = zachowanie, dostępność, primitives — NIGDY art direction.** Język wizualny
   buduj tokenami, typografią, gridem, rytmem, skalą.

## 1. Jak wejść (routing)

- **Wpisz `/design`** — drzewko pól wyboru prowadzi od zera do briefu i właściwego trybu; nie
  wymaga znajomości nazw.
- Tryby: szybka poprawka • standard (skill `design-foundry-os`, 3 koncepcje) • wysoka stawka
  (tryb turniejowy `references/10_master_system_prompt.md`, 6 koncepcji, panel ≥84/100) • nowy
  design system (skill `design-consultation` → DESIGN.md) • color-only.

## 2. Katalog artefaktów (co, gdzie, kiedy sięgać — skill `design-foundry-os/references/`)

| Plik | Zawartość | Sięgaj gdy |
|---|---|---|
| `14_design_memory_index.md` | **TEN indeks** — katalog + standing directives | na start każdej pracy wizualnej |
| `13_fintech_style_profile.md` | **GŁÓWNA BAZA ESTETYCZNA** operatora (+ profil fintech) | analizuj PIERWSZĄ przy każdym projekcie |
| `12_positive_references.md` | Seria pozytywna: Thorne, Instrument, BASIC/DEPT, Liquid Glass Studio | domyślny punkt wyjścia dla web |
| `11_slop_signatures_registry.md` | Rejestr slopu: 7 testów, 15 sygnatur → „co zamiast" | anti-slop na każdym etapie |
| `10_master_system_prompt.md` | Tryb turniejowy (6 koncepcji, panel ≥84/100, reconnaissance) | projekty flagowe / wysoka stawka |
| `09_uxui_web_brief.md` | Rozszerzony brief web (17 sekcji) | brief zadań webowych |
| `08_uxui_web_foundry.md` | Wariant web-only (22 sekcje) | zadania wyłącznie webowe |
| `04_acceptance_gates.md` | Bramka odrzucenia, adversarial review, testy, 20 pytań, Definition of Done | przed każdym oddaniem |
| `03_reference_dna.md` | Profile DNA (miks 60–70/20–30/≤10) | dobór referencji |
| `02_anti_references.md` | 6 studiów przypadku złych projektów | nauka antywzorców |
| `01_forbidden_ai_slop.md` | 12 grup bezwzględnych zakazów | katalog zakazów |
| `00_constitution.md` | Pełna konstytucja (38 sekcji) — nadrzędna | rozstrzyganie konfliktów |
| `05_device_matrix.md` | Viewporty, zoom, iPhone 16 Pro Max, iOS z Windows | testy responsywności |
| `06_task_brief_template.md` | Szablon briefu każdego zadania | start briefu |
| `07_toolchain.md` | Darmowy/tani toolchain + Claude-first minimal workflow | dobór narzędzi |

### Skille i komendy
- Skille: `design-foundry-os` (egzekucja konstytucji) • `design-consultation` (nowy design
  system → DESIGN.md) • `shadcn` (mechanika komponentów: kompozycja, formularze, warianty,
  tokeny semantyczne, CLI — „jak złożyć"; wygląd nadal spod FOUNDRY).
- Komendy: `/design` (router — drzewko pól wyboru).

## 3. Katalog preferencji estetycznych operatora (pamięć trwała — źródło: `references/13`)

Zindeksowana lista tego, co operatorowi „najbardziej odpowiada". Twarde wartości:
`references/13_fintech_style_profile.md` (części I–VI).

1. **Definicja sukcesu — Instrument × Oura** (`13` część II.5): typografia dwugłosowa (Source
   Serif Pro 600 w nagłówkach + Montserrat/Instrument Sans w UI), paleta atrament `#231f20` /
   granat `#425b76` / szałwia `#91a289` / brąz `#734e36`, rytm powierzchni zamiast ramek,
   editorial case-study, progressive disclosure.
2. **Glassmorphism / Liquid Glass — matowe szkło** (`13` część III.1): pod szkłem światło,
   kolor, sylwetki — nigdy detale; `blur 28–40px saturate 120–140%`, tint 8–14%; bokeh mile
   widziany; Liquid Glass (Fresnel) tylko dla małych kontrolek, frosted dla paneli treści.
3. **KRAWĘDZIE BEZ RAMEK — twarda reguła** (`13` część III.2): granica = zmiana powierzchni
   (inna jasność/temperatura tła obok) + cień + światło. Dozwolony jedynie 1px wewnętrzny
   highlight świetlny. Zakaz border/gradient-border/białej obwódki na kaflach — wszędzie.
4. **Pomarańczowy horyzont** (`13` część II.2): pozioma smuga światła jako atmosfera hero/
   przejść; nigdy kolor przycisków ani statusów.
5. **Haptyka i zachowania interakcji** (`13` część IV): fizyka press `scale(.985)` 120–160 ms;
   trzy stany koloru przycisku (hover = przesunięcie ODCIENIA); haptyka iOS impact/notification;
   przewijanie z momentum bez scroll-jackingu; rozwijanie 260–360 ms, zamykanie szybciej;
   pill-CTA dozwolony TYLKO z pełnymi 5 stanami; reduced-motion parytet.
6. **Regresje wykonawcze — obowiązkowe QA** (`13` część V, także w bramce `04`): (a) zero
   overflow liter poza kafelki na realnych treściach w KAŻDYM module; (b) tokeny odziedziczone
   w każdym nowym module, oba motywy; (c) brak degradacji fontów do stockowych; (d) test 5
   stanów każdego przycisku; (e) palety wyliczone i zharmonizowane.
7. **Materiały danych** (`13` część I, fintech): metal jako materiał DANYCH (nie ramek);
   teren 3D = zmienność/wolumen; aurora ziarnista jako tło/ambient; gradient-fill tylko jako
   wypełnienie serii; frosted studio jako wariant jasny.
8. **Wzorce pozytywne** (`references/12`): Thorne (organiczne neutrale, edukacja przed
   sprzedażą) • Instrument (monochromatyczna powściągliwość, typografia jako tożsamość) •
   BASIC/DEPT (ciemne tło jako materiał/ziarno, kontrolowana asymetria) • Liquid Glass Studio
   (produkt w użyciu jako hero, szkło z fizyką).

## 4. Toolchain (pełne: `references/07_toolchain.md`)

Claude-first minimal workflow + narzędzia zero/low-cost: Figma, Affinity, Blender, DaVinci
Resolve, Rive, Spline, reveal.js, PptxGenJS, Paged.js, GSAP public, UI Craft, Chrome/Playwright.
W repo `ui` dodatkowo: `pnpm v4:dev` (registry/dokumentacja, port 4000), `pnpm check`,
`pnpm test`, `pnpm registry:build`. Narzędzia wchodzą do gry, gdy mają funkcję — nigdy jako
dekoracja.

## 5. Bramki jakości / definicje sukcesu (pełne: `references/04`)

Definition of Done • bramka odrzucenia (≥2 z 22 sygnatur = redesign) • adversarial red-team
(PASS 0–1 / REDESIGN ≥2, test logo) • 20 pytań anti-slop • tryb turniejowy (średnia ≥84/100,
UX/a11y/wykonalność ≥80) • regresje operatora (sekcja 3.6) • `pnpm check` + `pnpm test` •
show-don't-claim.

## 6. Dziennik ustaleń tej sesji (trwały zapis decyzji)

- DESIGN FOUNDRY OS zainstalowany jako konstytucja (references/00) + skill + referencje.
- Warianty: WEB FOUNDRY (08), WEB BRIEF (09), tryb turniejowy (10); skill `design-consultation`.
- Rejestr slopu (11) i seria pozytywna (12) skatalogowane jako pamięć trwała.
- Profil fintech przepromowany do **GŁÓWNEJ BAZY ESTETYCZNEJ** (13), analizowanej pierwszą
  przy każdym projekcie; dołożone: definicja sukcesu Instrument×Oura (twarde wartości z HTML),
  matowość szkła, krawędzie bez ramek, pomarańczowy horyzont, warstwa haptyki/zachowań,
  pięć regresji wykonawczych jako obowiązkowe QA (wpisane też do bramki 04).
- `/design` = router (drzewko pól wyboru) — jedno wejście dla nie-designera.

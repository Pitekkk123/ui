---
description: Router designu DESIGN FOUNDRY OS — drzewko decyzyjne z polami wyboru ([ ] → [x]): co projektujesz, branża, stawka/tryb, DNA stylu, kolor, typografia, motion/3D, wykresy, platformy, eksporty. Prowadzi od zera do briefu i właściwego skilla bez pamiętania nazw. Argument (opcjonalny): krótki opis zadania.
---

Aktywuj skill `design-foundry-os`. **Najpierw wczytaj pamięć designu**: indeks
`references/14_design_memory_index.md` (katalog kanoniczny + standing directives: zawsze
najlepsze i najładniejsze rozwiązanie, bezwzględnie unikaj AI Slope) i główną bazę estetyczną
`references/13_fintech_style_profile.md`. Potem jesteś routerem designu: prowadzisz operatora
przez drzewko decyzyjne **krok po kroku**, po polsku, i na końcu sam wybierasz właściwą
procedurę. Operator nie musi znać żadnego skilla ani pliku.

Zadanie wstępne (jeśli podano): **$ARGUMENTS**

## Zasady interakcji

- Pytaj **sekwencyjnie** (jedno drzewko naraz), używając list pól wyboru w formacie
  `- [ ] opcja`. Operator odpowiada ptaszkami (`[x]`) lub po prostu tekstem — akceptuj oba.
- Gdy dostępne jest narzędzie klikalnych pytań (AskUserQuestion), użyj go zamiast tekstowych
  checkboxów (te same opcje; multiSelect tam, gdzie wybór wielokrotny). Fallback: listy `[ ]`.
- Jeżeli $ARGUMENTS lub wcześniejsza rozmowa już odpowiada na któreś pytanie — wypełnij je
  automatycznie, pokaż jako `[x]` i nie pytaj ponownie.
- Nie zadawaj wszystkich pytań naraz; maksymalnie 2 drzewka na wiadomość. Kroki 5–8 możesz
  scalić dla drobnych zadań. Dla „szybkiej poprawki" zadaj tylko kroki 1 i 9.

## Drzewko decyzyjne

**Krok 1 — Co projektujesz?** (jeden wybór)
- [ ] strona www / landing page
- [ ] web app / PWA
- [ ] dashboard / narzędzie analityczne
- [ ] aplikacja iOS
- [ ] aplikacja Android
- [ ] komponent / blok / formularz
- [ ] design system / brand / DESIGN.md
- [ ] logo / identyfikacja
- [ ] hero / grafika / ilustracja / 3D
- [ ] prezentacja HTML / PowerPoint
- [ ] raport PDF / infografika
- [ ] redesign istniejącego
- [ ] color-only redesign
- [ ] audyt designu istniejącego produktu

**Krok 2 — Branża / domena?** (jeden wybór + doprecyzowanie)
- [ ] finanse / trading / fintech → dołącz profil operatora `references/13_fintech_style_profile.md` (metal danych, aurora, gradient-fill; uwaga: Forbidden Outputs — bez sygnałów buy/sell, sizingu, stopów, targetów)
- [ ] medycyna / zdrowie (źródła, data, niepewność obowiązkowe)
- [ ] SaaS / narzędzie techniczne
- [ ] e-commerce / produkt fizyczny
- [ ] portfolio / studio / kultura
- [ ] edukacja / raporty / wiedza
- [ ] inna: ___

**Krok 3 — Stawka i tryb pracy?** (jeden wybór; decyduje o procedurze)
- [ ] szybka poprawka / drobna zmiana → wykonaj dokładnie zamówiony zakres (bez koncepcji)
- [ ] standardowy projekt → sekwencja 8 kroków skilla `design-foundry-os` (3 odmienne koncepcje)
- [ ] wysoka stawka / flagowy → tryb turniejowy `.claude/skills/design-foundry-os/references/10_master_system_prompt.md` (6 koncepcji, panel krytyków ≥84/100)
- [ ] nowy design system / brak DESIGN.md → skill `design-consultation` (konsultacja → preview → DESIGN.md)
- [ ] color-only → tryb COLOR_ONLY_REDESIGN (tylko tokeny; baseline + visual regression)

**Krok 4 — Styl / DNA?** (miks: główny + wspierający + akcent; potem 1 pytanie otwarte)
- [ ] Oura / Instrument — spokojna hierarchia danych, progressive disclosure
- [ ] Fantasy — odwaga koncepcyjna, kinowa sekwencja, mocna skala
- [ ] BASIC/DEPT — moduły, mocna fotografia, kontrolowana asymetria
- [ ] Thorne — organiczne neutrale, wiarygodność, edukacja przed sprzedażą
- [ ] BUCK — craft, materialność, autorski motion
- [ ] Apple HIG — jasność, ciągłość, systemowa dostępność
- Poziom eksperymentu 0–10: ___
- **Pytanie otwarte:** jaką JEDNĄ rzecz ma zapamiętać osoba widząca produkt pierwszy raz?
- (dla web domyślnie zastosuj język serii `references/12_positive_references.md`;
  ZAWSZE najpierw przejrzyj główną bazę estetyczną `references/13_fintech_style_profile.md`)

**Krok 5 — Kolorystyka?** (wybór wielokrotny, maks. „1 neutralna temperatura + 1 główny + 1 akcent")
- Neutrale: [ ] jasne ciepłe (bone/ivory/paper) [ ] ciemne z temperaturą (ink/graphite/deep navy — wymaga uzasadnienia)
- Akcent główny: [ ] shark blue [ ] sapphire [ ] petrol/teal [ ] sage [ ] copper [ ] oxblood/burgundy [ ] muted indigo [ ] własny: ___
- [ ] osobna paleta danych (sekwencyjna / dywergentna / kategorialna ≤6)
- Zakazane domyślnie: neonowy turkus, fioletowy gradient AI, gamingowa zieleń/czerwień, złoto=luksus

**Krok 6 — Typografia?** (jeden kierunek)
- [ ] neo-grotesk klasy Söhne / Neue Haas / Helvetica Now / Suisse (głos marki)
- [ ] techniczny — Space Grotesk
- [ ] editorial z uzasadnionym serifem (tylko z funkcją narracyjną)
- [ ] iOS — systemowe SF Pro + Dynamic Type
- Dane/mono: [ ] JetBrains Mono (tnum) [ ] inny mono: ___
- Uwaga trwała: Inter/Roboto/Arial NIE jako krój wiodący (rejestr sygnatur); Inter dopuszczalny tylko w gęstych tabelach danych

**Krok 7 — Motion i 3D?** (wybór wielokrotny; każde z funkcją i reduced-motion fallback)
- [ ] bez animacji / tylko stany
- [ ] subtelny funkcjonalny motion (CSS/WAAPI)
- [ ] orkiestracja GSAP (ScrollTrigger, Flip — lokalna dystrybucja gsap-public dostępna)
- [ ] mikrointerakcje Rive
- [ ] WebGL / Three.js / R3F — tylko gdy reprezentuje produkt/mechanizm/dane (dla danych rozważ Canvas 2D/SVG/shader)
- [ ] hero „produkt w użyciu" (wzorzec Liquid Glass Studio)

**Krok 8 — Dane i wykresy?** (wybór wielokrotny)
- [ ] linia / obszar [ ] słupki [ ] rozrzut [ ] heatmapa [ ] timeline / oś czasu
- [ ] graf / mapa zależności / diagram przepływu (architektura systemu — NIGDY fantasy command center)
- [ ] tabela danych (mono, tnum, sortowanie, długie nazwy)
- [ ] pasma niepewności / przedziały (obowiązkowe przy prognozach; podpis „projekcja, nie rekomendacja")
- Przy każdym wykresie: stan pusty / błędu / ładowania; tooltip z klawiatury; paleta danych ≠ paleta UI. Aktywuj skill `dataviz`, jeśli dostępny.

**Krok 9 — Platformy i eksporty?** (wybór wielokrotny)
- Platformy: [ ] desktop matrix (1280→1920 + zoom 100/125/200) [ ] iPhone 16 Pro Max (realny) [ ] tablet [ ] druk [ ] ekran prezentacyjny
- Eksporty: [ ] repo/kod [ ] pojedynczy HTML [ ] SVG [ ] PNG/WebP [ ] PPTX [ ] PDF [ ] MP4 [ ] Storybook [ ] design tokens [ ] raport QA

## Po drzewku (obowiązkowo)

1. Zbuduj brief: web → `references/09_uxui_web_brief.md`; pozostałe →
   `references/06_task_brief_template.md`. Pokaż wypełniony brief do akceptacji.
2. Poprowadź wybraną w kroku 3 procedurę (sekwencja / turniej / konsultacja / color-only).
3. Egzekwuj bramki: `references/04_acceptance_gates.md` + rejestr
   `references/11_slop_signatures_registry.md` (≥2 sygnatury = redesign; bez kosmetycznego retuszu)
   + części III–V bazy `references/13_fintech_style_profile.md` (krawędzie bez ramek,
   haptyka/zachowania, regresje operatora).
4. Raportuj wg „show, don't claim": co wykonano / przetestowano / czego nie zweryfikowano.

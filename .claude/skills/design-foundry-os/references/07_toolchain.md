# 07 — Toolchain (darmowy lub tani, wysoki poziom)

Zasada: każda zależność musi rozwiązywać konkretny problem, mieć akceptowalny koszt, być
utrzymywana, nie pogarszać bezpieczeństwa i nie narzucać generycznego wyglądu. Nie instaluj
niczego, bo jest modne. Największym ryzykiem nie jest brak programu, tylko budowanie
uniwersalnego generatora, zanim powstanie jeden wzorcowy produkt przechodzący wszystkie bramki.

## Zestaw podstawowy

| Obszar | Program | Priorytet | Koszt startowy |
|--------|---------|-----------|----------------|
| UI/UX | Figma Starter | bardzo wysoki | 0 |
| UI/UX open source | Penpot (backup / self-hosted) | wysoki | 0 |
| Wektor, zdjęcia, layout | Affinity (konto Canva) | bardzo wysoki | 0 |
| 3D i render | Blender | bardzo wysoki | 0 |
| Video, grading, VFX | DaVinci Resolve (+ Fusion) | bardzo wysoki | 0 |
| Ilustracja | Krita | średni | 0 |
| SVG (edycja techniczna) | Inkscape | średni | 0 |
| Kod | Visual Studio Code + Git + Node.js + pnpm | bardzo wysoki | 0 |
| Komponenty | Storybook | bardzo wysoki | 0 |
| Testy | Playwright + axe-core | bardzo wysoki | 0 |
| Interaktywne animacje | Rive (editor darmowy; eksport od planu Cadet) | wysoki | 0 / ~9 USD mies. |
| Interaktywne 3D (prototypy) | Spline | opcjonalny | plan startowy 0 |
| Prezentacje HTML | reveal.js | wysoki | 0 |
| PowerPoint z kodu | PptxGenJS (edytowalny tekst, tabele, natywne wykresy, Slide Masters) | wysoki | 0 |
| PDF z HTML | Paged.js + CSS Paged Media + Playwright do renderu | wysoki | 0 |

## Motion w kodzie

- **GSAP** — pełna dystrybucja publiczna (od przejęcia przez Webflow wszystkie pluginy „Club"
  są darmowe: ScrollTrigger, ScrollSmoother, SplitText, MorphSVG, DrawSVG, MotionPath, Flip,
  Draggable, Observer, CustomEase/Bounce/Wiggle, Physics2D…). Instalacja: `npm i gsap`;
  lokalna kopia dystrybucji `gsap-public` (src / esm / minified / UMD) jest dostępna u operatora.
  Używaj tylko z określoną funkcją (orientacja, ciągłość, feedback, narracja) — nigdy jako
  dekoracji domyślnej.
- **Three.js / React Three Fiber** — wyłącznie dla uzasadnionych scen (mechanizm, struktura,
  dane, świat marki) z budżetem wydajnościowym i fallbackiem.
- **Rive runtime** — web, iOS, Android, React Native; mikrointerakcje i komponenty reagujące
  na dane.

## Anty-slop tooling (agentowe)

- **UI Craft** (skills.smoothui.dev; u operatora paczka `uicraft_1.0.3_windows_arm64` —
  na ASUS ProArt x86-64 pobierz build Windows x64 albo zainstaluj jako skill) — design
  engineering system dla agentów kodujących: komenda `/craft`, 10-punktowy acceptance bar,
  scoreable critique (heurystyki Nielsena × prawa designu × persony), anti-slop gate na commit.
  Komplementarny wobec tego skilla: DESIGN FOUNDRY OS jest konstytucją, UI Craft może służyć
  jako dodatkowy niezależny weryfikator.

## Minimalny stos webowy

VS Code • Git • Node.js • pnpm • Next.js • React • TypeScript • CSS variables • Storybook •
Playwright • axe-core • GSAP • Rive • Three.js tylko w uzasadnionych miejscach.

## Kolejność instalacji

1. **Podstawy:** Figma Desktop, Affinity, VS Code, Git, Node.js, pnpm, Chrome/Edge, Firefox.
2. **Produkcja wizualna:** Blender, DaVinci Resolve, Krita, Spline, Rive.
3. **Web i testy:** Next.js, Storybook, Playwright, axe-core, GSAP (Three.js/R3F tylko
   do uzasadnionych scen).
4. **Mobile:** Expo Go na iPhonie, Expo CLI / EAS CLI na Windows, React Native, Rive runtime RN.
5. **Dokumenty:** reveal.js, PptxGenJS, Paged.js, PowerPoint do finalnego sprawdzenia PPTX
   (jeśli licencja).

## Budżet

- **Wariant praktycznie bezpłatny:** Figma Starter, Affinity, Blender, DaVinci Resolve, Penpot,
  Krita, VS Code, Git, Storybook, Playwright, Expo, reveal.js, PptxGenJS, Paged.js.
- **Dopłać dopiero za:** Rive Cadet (eksport produkcyjny), Figma Professional (biblioteki,
  współpraca), hosting, konto deweloperskie Apple przy publikacji, cloud build, licencjonowane
  fonty/fotografie/assety.
- **Nie kupuj na start:** Adobe Creative Cloud, Webflow, Framer, drogie 3D, biblioteki
  szablonów. Nie brakuje aplikacji — brakuje procesu selekcji, krytyki i testów.

## Pierwszy vertical slice (zanim powstanie „fabryka designu")

Produkt analityczny lub medyczny → living brief → profil Oura + Thorne + akcent BUCK →
pełny design system → web app → PWA → ekran iPhone 16 Pro Max → jedno interaktywne hero →
mikrointerakcje Rive → raport PDF → prezentacja HTML → edytowalny PowerPoint → Storybook →
Playwright → adversarial anti-AI-slop review. Dopiero gdy jeden produkt przejdzie wszystkie
bramki, uogólniaj proces.

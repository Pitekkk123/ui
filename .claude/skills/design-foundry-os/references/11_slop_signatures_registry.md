# 11 — Rejestr sygnatur AI slopu (pamięć trwała, punkt po punkcie)

Kompletny rejestr sygnatur z pakietu operatora `claude-code-foundry` (analiza ZIP, 2026-07).
Operator: „to jest AI slop — zapamiętać wszystkie sygnatury i za wszelką cenę takiego wyniku
nie produkować". Ten plik jest pamięcią trwałą projektu: **każda pozycja poniżej jest zakazana
domyślnie**; uzupełnia (nie zastępuje) katalog `01_forbidden_ai_slop.md` i bramki
`04_acceptance_gates.md`. Przy konflikcie „ładnie" vs „nie-slop" — wygrywa nie-slop.

## 1. Definicja operacyjna

AI slop = wynik, który **udaje jakość przez nagromadzenie rozpoznawalnych konwencji
generatywnych**, zamiast mieć jedną własną ideę, prawidłową hierarchię informacji i uzasadnione
interakcje. Powierzchownie „dopieszczony"; w rzeczywistości szablonowy, niewiarygodny, przenośny
do dowolnej firmy i szybko się starzeje.

## 2. Siedem testów operacyjnych (wynik jest slopem, jeśli KTÓRYKOLWIEK jest prawdziwy)

1. **Test logo** — po podmianie nazwy/logo mógłby należeć do dowolnego startupu.
2. **Test idei** — nie ma jednej rozpoznawalnej decyzji artystycznej; jest kolekcja trendów.
3. **Test funkcji** — efekt (gradient/glow/szkło/3D/animacja) nie pełni żadnej funkcji.
4. **Test hierarchii** — hierarchia trzyma się wyłącznie na obramowaniach i kapsułach.
5. **Test wiarygodności** — „premium" sugerowane wyglądem, nie proporcją/treścią/dowodami.
6. **Test treści** — widać surowy output modelu (Markdown, ściany tekstu, przypadkowy bold).
7. **Test platformy** — mobile jest zmniejszonym desktopem, nie zaprojektowany.

## 3. Piętnaście sygnatur głównych → co zamiast

| # | Sygnatura slopu | Co zamiast |
|---|---|---|
| 1 | Domyślne czarne/granatowe tło + neonowy turkus/fiolet/zieleń jako akcent | Tło wynika z marki i treści; jeden powściągliwy akcent z palety |
| 2 | Gradientowe słowo w ogromnym nagłówku | Hierarchia przez skalę, wagę, przestrzeń; jednolity kolor tekstu |
| 3 | Pigułka/pill nad nagłówkiem; badges/chips wszędzie (Pro, Beta, AI-powered, New, TAK/NIE) | Status czytelny bez kapsuł; etykieta tylko gdy niesie informację |
| 4 | Monokultura rounded cards; card-in-card; identyczny radius wszędzie | Przestrzeń/grid/oś/rytm/separator/gęstość najpierw; karta = realna jednostka funkcjonalna |
| 5 | Glassmorphism: blur na wszystkim, szkło na szkle, biały półprzezroczysty border jako hierarchia | Materiał z fizyką, fallback, Reduce Transparency, kontrast |
| 6 | Neonowe pseudo-premium: gradientowe bordery, glow wokół paneli, świecące ikony, trofea, złoto=luksus | Premium z proporcji/typografii/materiału/światła/fotografii |
| 7 | Fantasy command center: świątynie AI, magiczne wieże, złote przewody, postać patrząca na system | Architektura jako diagram przepływu / graf / sekwencja / mapa zależności / model danych |
| 8 | Generyczne hero: „Reimagine the future", kula 3D, unoszący się laptop, losowe particule, urządzenie pod kątem | Hero tłumaczy produkt w 1 s; reżyserowana scena |
| 9 | Modal jako aplikacja: wieloetapowy kreator w małym modalu, scroll w scrollu, gigantyczny X z glow | Pełna podstrona / side panel / split view / inspector / workspace |
| 10 | Ściana checkboxów: dziesiątki równorzędnych opcji bez hierarchii, presetów, wyszukiwania | Cel → rekomendowany profil → 3 kluczowe decyzje → podgląd → opcje eksperckie |
| 11 | Surowa treść modelu: widoczny Markdown, ściany tekstu, tekst przycięty przez kontener | Treść zredagowana osobno dla interfejsu |
| 12 | Generyczna apka finansowa: ciemne tło + tickery w losowych kolorach + sparkline w każdym wierszu + 8 pozycji dolnej nawigacji + serif „na premium" + cała apka w jednej karcie | Zaprojektowana hierarchia danych; sparkline tylko gdzie niesie sens; **nawigacja ≤5 pozycji** |
| 13 | Dekoracyjna animacja: reveal każdej sekcji, parallax bez funkcji, pulse, wirujące gradienty, blob/particles, layout shift na hover | Motion tylko: orientacja/ciągłość/feedback/przyczynowość/stan/hierarchia/narracja |
| 14 | Sztuczna wiarygodność: zaufanie z animowanych liczników, zielonych wyników, logotypów bez kontekstu | Wiarygodność ze źródeł, metodologii, zakresu niepewności, możliwości weryfikacji |
| 15 | Kopiowanie szablonów: wygląd Linear / typowy shadcn dashboard / motyw Tailwind / low-code admin | Headless = zachowanie; wygląd autorski |

## 4. Sygnatury szczegółowe per obszar

### Typografia

- Inter, Roboto, Arial, Fraunces jako **krój wiodący** — nadużywane, robią z projektu slop.
  **Nota precedencji operatora:** ta reguła jawnie nadpisuje wcześniejsze „preferuj Inter"
  z konstytucji §13. Inter dopuszczalny **wyłącznie** jako workhorse w bardzo gęstych tabelach
  danych, nigdy jako głos marki. Kierunki zamiast: neo-groteski klasy Söhne / Neue Haas
  Grotesk / Helvetica Now / ABC Diatype / Suisse Int'l; technicznie — Space Grotesk;
  mono z cyframi tablicowymi: JetBrains Mono / Söhne Mono / Commit Mono; iOS — systemowe SF Pro
  przez natywne style + Dynamic Type (nie webfont „dla charakteru").
- Serif użyty wyłącznie jako sygnał „premium".
- Ogromny hero-headline bez odpowiadającej mu treści.
- Uppercase w długich etykietach; przesadny letter-spacing.
- Zmniejszanie tekstu, żeby zmieścił się w panelu (zamiast przeprojektowania panelu).
- Więcej niż dwie rodziny fontów; druga bez uzasadnienia narracyjnego/funkcjonalnego.
- 6 wag statycznych, gdy wystarczy jeden plik variable; brak podzbioru z polskimi znakami.
- Brak cyfr tablicowych (`tabular-nums`) tam, gdzie liczby się zmieniają lub układają w kolumny.
- Wiersz tekstu ciągłego bez kontroli długości (cel: 60–75ch); body poniżej 16px na mobile.

### Kolor

- Jaskrawy neonowy turkus; **domyślny fioletowy gradient AI**; gamingowa zieleń/czerwień.
- Kolorowy glow jako hierarchia.
- Czysta biel na czystej czerni jako **jedyna** koncepcja.
- Złoto jako automatyczny symbol luksusu.
- Tęczowe palety danych; te same kolory dla UI i danych (dane = osobny zestaw:
  sekwencyjny / dywergentny / kategorialny ≤6 serii, rozróżnialny w deuteranopii).
- Kolor jako jedyny nośnik znaczenia (zawsze dubluj ikoną/kształtem/etykietą).
- Więcej niż: jedna temperatura neutralna + jeden kolor główny + jeden akcent (maks. dwa akcenty).

### Materiał i światło

- Glow jako zamiennik światła; świetlna aureola wokół każdego panelu.
- Szkło na szkle; blur na wszystkich powierzchniach; przezroczystość pod długim tekstem.
- Biały półprzezroczysty border jako główna hierarchia; gradientowe bordery.
- Pseudo-Liquid-Glass złożony wyłącznie z `backdrop-filter`.
- Ten sam materiał dla każdej roli (nawigacja ≠ treść ≠ wykres ≠ formularz ≠ tło ≠ przycisk).
- Szeroki neonowy halo zamiast krótkiego, miękkiego cienia kontaktowego.
- Brak jednego spójnego źródła światła; brak fallbacku i Reduce Transparency.

### Motion

- Reveal każdej sekcji; parallax bez funkcji; unoszenie każdej karty; ciągłe pulsowanie.
- Wirujące gradienty; blob motion; dekoracyjne cząsteczki; layout shift na hover.
- Animacja opóźniająca działanie; **autokaruzele**; bounce „dla charakteru".
- Animowanie `top/left/width` zamiast `transform`/`opacity`; `will-change` na stałe.
- Brak obsługi `prefers-reduced-motion`; treść ukryta za animacją, która przy reduced-motion
  się nie wykona; hero bez pełnoprawnego statycznego key frame'a.

### 3D i hero

- Przypadkowe kule; orbity; chromowane pierścienie; szkło bez znaczenia; abstrakcyjna wstęga.
- Unoszący się laptop; telefon/urządzenie pod kątem; losowe particule; stockowy render.
- Metafora niewynikająca z produktu (generyczna = odrzuć przed kodem).
- Animacja ratująca słaby statyczny kadr (jeśli statyka nie robi wrażenia, animacja też nie).
- 3D tam, gdzie Canvas 2D / SVG / autorski shader byłby lżejszy i bardziej autorski.
- Hero, które w 1 sekundę nie mówi: co to, dla kogo, jaki problem, jaka korzyść, jaka akcja.

### Panele, karty, powierzchnie

- Karta jako domyślny kontener; każda informacja w osobnej kapsule; card-in-card.
- Jeden (lub nadmierny) radius wszędzie — zamiast 2–3 wartości wg roli.
- Obramowanie wokół każdej sekcji — zamiast 1–2 hairline'ów.
- Hierarchia, która padłaby bez obramowań (buduj: przestrzeń → grid → oś → rytm → typografia →
  powierzchnia → separator → gęstość → kontrast materiału — panel na końcu).

### Modale i ustawienia

- Modal większy niż viewport; scroll wewnątrz scrolla; wiele tabów w kapsułach.
- Aplikacja/kreator wieloetapowy w oknie dialogowym; gigantyczny X z glow.
- Ściana checkboxów; opcje krytyczne i marginalne o tej samej wadze wizualnej.
- Brak presetów, wyszukiwania i progressive disclosure w rozbudowanych ustawieniach.

### Nawigacja i mobile/iOS

- Osiem (lub więcej) równorzędnych pozycji nawigacji — cel: **≤5**.
- Kluczowe funkcje ukryte pod nieopisanymi ikonami.
- Informacja niesiona samym kolorem.
- Mobile jako zmniejszony desktop, nie zaprojektowany osobno; hit-target < 44×44.

### Assety, logo i wizualizacja danych

- Fałszywe „SVG" z tysiącami ścieżek (zwektoryzowane zdjęcie) — cięższe i gorsze niż dobrze
  skompresowany raster.
- Logo generyczne: litery z obwodami; mózgi AI; węzły sieci; orbitujące kule; tarcze fintech;
  świecące monogramy; znaki nieskończoności; gradientowe znaki bez własnej geometrii.
- Sparkline w każdym wierszu „bo można"; siatka wykresu o wysokim kontraście; tęcza serii.
- Prognoza bez pokazanej niepewności (pasma/przedziały + podpis „scenariusz/projekcja,
  nie rekomendacja").
- **Data slop**: wymyślone dane i metryki; dane przykładowe nieoznaczone.
- Wykres bez stanów pustego/błędu/ładowania; tooltip niedostępny z klawiatury.

### Treść

- Widoczny Markdown; ściany tekstu w kartach; surowy output modelu; przypadkowy bold.
- Tekst przycięty przez kontener; źródła wciśnięte w środek akapitu.

## 5. Werdykt czerwonej drużyny (procedura)

Policz sygnatury z bramki odrzucenia (`04_acceptance_gates.md`, sekcja A) na zrzutach wszystkich
kluczowych ekranów (desktop + mobile):

- **PASS** = 0–1 sygnatura; **REDESIGN** = ≥2 (przeprojektuj wskazane elementy od podstaw).
- **Kosmetyczny retusz projektu, który oblewa bramkę, jest zabroniony.**
- Test logo wykonuj wprost: napisz, do jakiej dowolnej firmy projekt mógłby należeć —
  jeśli umiesz to napisać wiarygodnie, to jest dowód slopu.
- Wskaż najsłabszy element: co pierwsze zdradza generatywne pochodzenie.
- Krytyk działa w osobnym kontekście, bez sentymentu do wykonanej pracy; negatywna odpowiedź
  w punkcie krytycznym (testy 1–6 z sekcji 2 oraz „czy wszystko realnie działa") = obowiązek
  przeprojektowania.

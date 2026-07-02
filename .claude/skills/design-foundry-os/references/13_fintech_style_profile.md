# 13 — GŁÓWNA BAZA ESTETYCZNA OPERATORA (+ profil fintech)

**Status: analizuj TEN plik jako PIERWSZY przy każdym projekcie wizualnym** (dyrektywa
operatora, 2026-07). To nie jest profil branżowy — to główna baza elementów stylu, które
operatorowi „najbardziej odpowiadają". Przy zadaniach **fintech** (wystarczy to słowo)
stosuj dodatkowo część I w pełni. Definicją sukcesu jest strona case study
**Instrument × Oura** (część II.5) — większość produktów operatora ma być miksem tego języka
z warstwą glassmorphism/Liquid Glass i akcentem pomarańczowego horyzontu.

Precedencja: jawna decyzja operatora per §1 konstytucji. Elementy normalnie zakazane
(metal, świecący gradient, bloom, pill-CTA) dozwolone WYŁĄCZNIE w rolach opisanych niżej.
Bez zmian: bramki funkcjonalne, stany, kontrast wyliczany, uczciwość danych;
rejestr slopu obowiązuje poza jawnie opisanymi wyjątkami.

---

## CZĘŚĆ I — Porcja fintech (5 referencji)

### I.1 Izometryczne karty z metalicznymi danymi (czerń + złoto/srebro)
1. Matowa, prawie czarna ceramika kart; krawędzie odcięte światłem, nie ramką.
2. **Metal jako materiał DANYCH**: złota/srebrna folia w słupkach i pierścieniach —
   metal koduje serie/stan, nigdy nie dekoruje ramek.
3. Złote hairline'y zamiast obramowań; mikro-etykiety mono uppercase; kafel z jedną
   wielką liczbą; ogromny oddech; izometria = język hero/marketingu.

### I.2 Teren danych 3D (czarna otchłań + świece)
Czarne tło absolutne; szklane tafle z ultradrobną siatką; **dane jako krajobraz**
(particle terrain = zmienność/wolumen — 3D z funkcją); świece zimno-błękitne;
**pomarańcz wyłącznie sygnałowo**; głębia 2–4 warstw.

### I.3 Aurora (ziarnista atmosfera świetlna)
Atramentowe pole + miękka ZIARNISTA poświata (krem/róż, widmowy rąbek teal/pomarańcz).
Język tła i ambientu (hero, stany puste, onboarding) — nie ramek, nie statusów.

### I.4 Szklana tafla ze świetlistym wypełnieniem danych
Świecący gradient (violet→magenta→amber→blue) **wyłącznie jako wypełnienie serii
danych**; odbicie na podłodze (fizyka); reszta wyciszona; bloom tylko na źródle światła.

### I.5 Frosted studio (jasna scena, ciemna karta-bohater)
Jasna scena studyjna z głębią ostrości; ciemna karta produktu w centrum; wokół kafle
matowego szkła z liczbami; czerwień/amber tylko jako kropki stanu; wielka wartość
jako dominanta typograficzna.

## CZĘŚĆ II — Porcja główna (4 referencje + strona-definicja sukcesu)

### II.1 Frosted contact (formularz na scenie z globem cząsteczkowym)
1. Ciemna scena z żywym tłem (particle globe) — pod szkłem widać ŚWIATŁO i KSZTAŁT,
   nigdy detale.
2. Panele z matowego szkła **bez ramek** — czytelne przez różnicę jasności powierzchni.
3. Pola formularza: ciemniejsze zagłębienia w szkle (inset), etykiety małe nad polem,
   placeholdery wyciszone; select z własnym chevronem.
4. Grupy funkcji w osobnych taflach (Formularz / Email / Call / Follow) — karta = realna
   jednostka zadaniowa.

### II.2 Pomarańczowy horyzont (ulubiony akcent operatora)
1. Czarne pole + pozioma SMUGA pomarańczowego światła (zachód nad horyzontem):
   gradient kierunkowy, ostry rdzeń → miękki spad; asymetryczny (gaśnie w prawo).
2. Rola: atmosfera hero/przejść sekcji, kierunkowe światło sceny, tło dla frosted glass;
   NIE kolor przycisków ani statusów (pomarańcz sygnałowy pozostaje osobno, punktowo).

### II.3 „Project Aurora" (mobilny fintech — wzorzec ekranu aplikacji)
1. Głęboki granat/czerń; scena za telefonem z aurorą niebiesko-pomarańczową (I.3+II.2).
2. Wykres jako bohater świetlny: niebieska linia z miękką poświatą pod krzywą.
3. Watchlista: rzeczywiste logotypy spółek, mono tnum ceny, mini-sparkline z funkcją
   (trend pozycji), zieleń/czerwień TYLKO w wartościach zmian.
4. **Panel „Evidence & Verification"** (Confidence 92% / Sources 128 Verified / Last
   updated 1m ago) — wzorzec wiarygodności: pewność, źródła, świeżość zawsze widoczne
   przy danych analitycznych.
5. Nawigacja dolna: **5 pozycji**, ikony + etykiety; segment czasu (1D/1W/…) jako
   spokojny segmented control, aktywny = wypełnienie, nie glow.
6. AI Recap jako zredagowana karta (tytuł-teza + 2 zdania + Read more) — nie surowy
   output modelu.

### II.4 Fora (landing — spokojna monumentalność)
1. Wielka, spokojna typografia zdaniowa („Your community is one sec away.") na czerni
   z temperaturą; zero gradientowych słów.
2. Produkt pokazany jako REALNY interfejs w bocznym panelu (lista Overview/Chat/Courses…),
   nie mockup pod kątem.
3. Krajobraz (wydmy o zmierzchu) jako przejście sekcji — fotografia buduje oddech.
4. Nawigacja: 5 pozycji + Login + jeden CTA; footer trzy kolumny, hairline'y.
5. Pill-CTA („Start for free", „Join now") — patrz reguła przycisków w części IV.

### II.5 Instrument × Oura — STRONA-DEFINICJA SUKCESU (z analizy kodu HTML)
Twarde wartości wyciągnięte z arkuszy strony:
1. **Typografia dwugłosowa**: nagłówki narracyjne SERIF — Source Serif Pro 600
   (h1 40 / h2 32 / h3 28 / h4 24 / blockquote 24); tekst i UI — humanist grotesk
   (Montserrat 400/600; przyciski hero — **Instrument Sans**). To zatwierdzony wyjątek
   od „serif tylko z funkcją": funkcją jest narracja editorial.
2. **Paleta**: atrament `#231f20` na bieli; ciepłe neutrale sekcji `#f4f0ec` /
   `#f6ece7`; głęboki granat `#425b76` (akcent/CTA); przygaszona zieleń `#415239`
   i szałwia `#91a289` (hover/active — zmiana ODCIENIA, nie jasności!); brąz `#734e36`
   (ikony); linie `#d7d9e3`. Sekcje rytmicznie zmieniają tło (biel → kość → czerń →
   kremowy róż) — **rytm powierzchni zamiast ramek**.
3. **Przyciski hero**: pill radius 30, granat-atrament `rgba(29,44,56)`, Instrument Sans,
   duży rozmiar (25px), hover → czerń, active → szarość: trzy JAWNE stany koloru.
4. **Struktura case study**: Challenge → Approach → Evolved Identity → System
   (semantic color) → Framework → Impact z metrykami; pełnoszerokie obrazy; interpretacja
   przed liczbą; progressive disclosure.
5. Karty bez radiusa (0px) i separacja kolorem tła — spójne z regułą krawędzi (część III).

## CZĘŚĆ III — Szkło: matowość i krawędzie (twarde ustalenia operatora)

1. **Matowość (frosted)**: pod szkłem widać światło, kolor i sylwetki — NIGDY tekst
   ani detale. Parametry wyjściowe web: `backdrop-filter: blur(28–40px)
   saturate(120–140%)`; mgła własna panelu: tint powierzchni 8–14% alpha (ciemny motyw:
   biel 6–10%; jasny: powierzchnia ciepła 60–80%). Bokeh tła jest pożądany — tło sceny
   może mieć własne punkty światła, które szkło rozmywa.
2. **KRAWĘDZIE BEZ RAMEK (twarda reguła)**: kafelek/panel NIE kończy się obrysem
   w mocniejszym kolorze. Granica = **zmiana powierzchni** (inna jasność/temperatura
   tła obok), cień kontaktowy i światło. Dozwolone jedynie: 1px WEWNĘTRZNY highlight
   świetlny (`inset 0 1px 0 rgba(255,255,255,.05–.12)`) jako fizyka górnej krawędzi —
   to światło, nie ramka. Zakaz: `border: 1px solid` w akcentowym/jaśniejszym kolorze
   wokół kafli, gradient-border, biała obwódka glassmorphism.
3. Fallbacki obowiązkowe: brak `backdrop-filter` → powierzchnia solidna z tintem;
   `prefers-reduced-transparency` → solid; kontrast treści na szkle zawsze wyliczony.
4. Liquid Glass (refrakcja/Fresnel — wzorzec Liquid Glass Studio) tylko dla małych
   kontrolek/nawigacji z fizyką; frosted (mat) dla paneli treści.

## CZĘŚĆ IV — Haptyka i zachowanie interakcji (warstwa stylu, obowiązkowa)

### Przyciski i klawisze
1. Konstrukcja profesjonalna: wysokość ≥44px; typografia 500–600; padding poziomy
   ≥1.25em; ikona tylko funkcjonalna; wyraźny stan disabled (obniżona zawartość,
   nie sama przezroczystość).
2. **Trzy stany koloru jak w II.5** (spoczynek → hover: przesunięcie ODCIENIA,
   np. granat→głęboka zieleń lub →czerń; active: trzeci, wyraźny krok). Nigdy sam
   `opacity` ani sam `transform`.
3. Fizyka press: `scale(.985)` + skrócenie cienia kontaktowego, 120–160 ms, ease-out;
   powrót 180–220 ms. Hover NIE powoduje skoku layoutu.
4. **Pill-CTA jest dozwolony** (język Instrument/Fora): świadomy, duży, z trzema stanami
   i pełną konstrukcją. AI-slopowy „pill" (mały, bez stanów, badge-podobny, stockowy
   font) pozostaje ZAKAZANY. Test: czy przycisk ma zaprojektowane 5 stanów
   (default/hover/active/focus/disabled)? Nie ma → nie oddawaj.
5. Haptyka (iOS/app): tap = impact light; potwierdzenie/przełącznik = impact medium;
   sukces/błąd operacji = notification success/error; długie przeciąganie = selection
   changed przy przekroczeniu progów. Web-Android: `navigator.vibrate(8–12)` tylko dla
   akcji potwierdzających, z poszanowaniem ustawień systemowych. Haptyka ZAWSZE
   sparowana z feedbackiem wizualnym (nie zastępuje go).

### Przewijanie
Naturalne momentum (żadnego scroll-jackingu); `scroll-snap` tylko dla galerii/kart
pełnoekranowych; sticky nagłówki kondensują się przy scrollu (wysokość i cień, 200 ms);
paski postępu czytania tylko w treściach długich; kotwice z `scroll-margin-top`.

### Rozwijanie (menu, akordeony, drawery)
Otwieranie 260–360 ms ease-out (wysokość/clip + treść fade-in z 40 ms opóźnieniem);
**zamykanie szybsze** (160–220 ms); chevron rotuje w tym samym czasie; focus wchodzi do
rozwiniętej treści; menu kontekstowe: origin transformacji w punkcie wywołania; drawer
mobilny z detentami i przeciągnięciem. Wszystko z parytetem reduced-motion (stan
natychmiastowy, bez utraty treści).

## CZĘŚĆ V — Regresje wykonawcze operatora (sprawdzaj ZAWSZE przed oddaniem)

Operator wskazał moje powtarzalne błędy — każdy punkt jest obowiązkowym testem QA:
1. **Overflow liter poza kafelki** — testuj długie polskie słowa i realne treści
   w KAŻDYM module (nie tylko pierwszym); zero przyciętego/wystającego tekstu.
2. **Niezamienione kolory w kolejnych modułach** — każdy nowy moduł/ekran dziedziczy
   tokeny; po dodaniu modułu audyt: żadnych hardkodów spoza systemu; oba motywy
   sprawdzone na NOWYM module.
3. **Degradacja fontów** — dalsze ekrany nie spadają do stockowych (Arial/Roboto/
   systemowe zamiast głosu marki); font-check każdego widoku: rodzina+waga zgodna
   z systemem.
4. **Przyciski-atrapy stylu** — każdy przycisk przechodzi test 5 stanów (IV.2/IV.4).
5. **Kolory „prawie"** — palety wyliczone (kontrast) i zharmonizowane (jedna temperatura
   neutralnych, akcenty z bazy); „estetyczna poezja" = zero przypadkowych hexów.
Spójność tych punktów sprawdzaj na zrzutach WSZYSTKICH zmienionych widoków, w obu
motywach, zanim zgłosisz ukończenie.

## CZĘŚĆ VI — Guardrails całości

1. Jeden bohater świetlny na ekran (gradient-fill serii ALBO metal ALBO horyzont —
   nie wszystko naraz).
2. Metal/gradient/bloom/horyzont świecą tylko tam, gdzie są dane, źródło światła
   albo atmosfera sceny — nigdy na ramkach, badge'ach, nagłówkach.
3. Krawędzie: część III.2 obowiązuje wszystkie powierzchnie (też poza szkłem).
4. Serif = tylko głos narracyjny (editorial, case study, storytelling) — UI operacyjne
   zostaje przy grotesku+mono.
5. Test logo, bramka ≥2 sygnatur i werdykt red-team — bez zmian.

# 13 — Profil stylu FINTECH (dyrektywa operatora)

**Trigger: słowo „fintech"** (dashboard, aplikacja, hero, landing finansowy). Wtedy — oprócz
całego systemu FOUNDRY (bramki, stany, brief, wzorce z `12_positive_references.md`) — obowiązuje
ten profil, zmapowany z referencji dostarczonych przez operatora (5 obrazów, 2026-07).

**Status precedencji:** to jawna decyzja operatora w rozumieniu §1 konstytucji (dozwolone
odstępstwo). Elementy normalnie zakazane (metaliczne złoto, świecący gradient, kontrolowany
bloom) są tu DOZWOLONE **wyłącznie w rolach opisanych niżej**. Nietknięte pozostają: bramki
funkcjonalne, stany, kontrast, uczciwość danych (Forbidden Outputs, niepewność prognoz,
oznaczanie danych przykładowych) oraz rejestr slopu poza jawnie wyłączonymi punktami
(nadal zakazane m.in.: badges wszędzie, karta-w-karcie, tęczowe palety UI, trofea,
8 pozycji nawigacji, pigułka nad hero).

---

## 1. Mapowanie referencji (sygnatury punkt po punkcie)

### R1 — Izometryczne karty z metalicznymi danymi (czerń + złoto/srebro)

1. Matowa, prawie czarna ceramika kart na ciemnym polu; krawędzie ledwo odcięte światłem.
2. **Metal jako materiał DANYCH**: słupki wykresów ze złotej i srebrnej folii (kierunkowy
   połysk), pierścień postępu złoto+srebro — metal koduje serie/stan, nie dekoruje ramek.
3. Hairline'y (cienkie złote linie) zamiast obramowań; zero wypełnionych ramek.
4. Mikro-etykiety mono uppercase o niskiej wadze; ogromny oddech; editorial spacing.
5. Kafel-liczba: jedna wielka wartość mono (np. „0.2") jako samodzielny moduł.
6. Kompozycja izometryczna zestawu kart — język HERO i materiałów marketingowych,
   nie ekranu operacyjnego.

### R2 — Teren danych 3D (czarna otchłań + świece)

1. Czarne tło absolutne; szklane tafle-warstwy z ultra-drobną siatką o niskim kontraście.
2. **Dane jako krajobraz**: ciemny, ziarnisty teren (particle terrain) wyrasta z płaszczyzny
   wykresu — 3D reprezentuje zmienność/wolumen, ma funkcję, nie jest kulą-ozdobą.
3. Świece zimno-biało-błękitne; **pomarańcz wyłącznie jako sygnał** (aktywne/istotne świece).
4. Drobne liczby osi w mono; panele boczne jako półprzezroczyste tafle.
5. Głębia sceny: 2–4 warstwy (tafla → teren → świece → HUD).

### R3 — Aurora (ziarnista atmosfera świetlna)

1. Granatowo-atramentowe pole + miękka, ZIARNISTA poświata (film grain) — krem/róż z wąskim
   widmowym rąbkiem (teal/pomarańcz).
2. To język TŁA i ambientu (hero, pusty stan, onboarding) — nie ramek ani statusów;
   światło ma źródło i kierunek, nie otacza paneli aureolą.
3. Ziarno spina materiał (anty-banding) — spójne z ziarnem Pracowni.

### R4 — Szklana tafla ze świetlistym wypełnieniem danych

1. Jedna szklana tafla w ciemnym studiu; odbicie na podłodze (fizyka światła).
2. **Świecący gradient (violet→magenta→amber→blue) WYŁĄCZNIE jako wypełnienie obszaru
   wykresu** — światło emituje SERIA DANYCH, nie tło, nie border, nie headline.
3. Reszta interfejsu wyciszona: drobny, przygaszony mono; jedna bohaterska seria.
4. Kontrolowany bloom tylko na fizycznie jasnym źródle (linia danych).

### R5 — Frosted studio (jasna scena, ciemna karta-bohater)

1. Jasna, neutralna scena studyjna (szarość z temperaturą); głębia ostrości (mgła planów).
2. **Ciemna karta produktu jako bohater** pośrodku; wokół kafle z MATOWEGO szkła
   (frosted) z pojedynczymi liczbami.
3. Akcenty: czerwień/amber tylko jako punktowe sygnały stanu (kropki, alert), nigdy pola.
4. Wielka cena/wartość jako dominanta typograficzna; wykres liniowy biały, cienki.
5. To wariant JASNY profilu — do materiałów app/marketing i trybu dokumentowego.

## 2. Synteza systemu fintech (jak tego używać)

- **Tła:** czerń/atrament z temperaturą (nie #000 flat) + opcjonalny ambient aurory (R3)
  w hero/stanach pustych; wariant jasny = frosted studio (R5). Ziarno globalne.
- **Materiały:** matowa ceramika kart (R1) • szkło z fizyką i odbiciem (R4) • metal
  foliowy złoto/srebro TYLKO jako wypełnienie elementów danych (R1) • frosted glass
  w scenie jasnej (R5). Różne role = różne materiały; bez szkła na szkle.
- **Kolor:** baza monochromatyczna; złoto `#C9A45C→#8C6B32` i srebro jako serie danych;
  zimny biało-błękit dla neutralnych danych; **pomarańcz/czerwień wyłącznie sygnałowo**
  (aktywna świeca, alert, kropka stanu); świecący gradient tylko jako fill serii (R4).
  Semantyka zysk/strata wg rejestru (sage/burgundy) albo metal+sygnał — nigdy gamingowa
  zieleń/czerwień jako dominanta.
- **Typografia:** grotesk (głos marki) + mono tabelaryczne dla WSZYSTKICH liczb; wielkie
  wartości jako dominanty; mikro-etykiety uppercase z szerokim trackingiem, niska waga.
- **Kompozycja:** hairline zamiast ramek; ogromny oddech; izometryczne zestawy kart (R1)
  i sceny z głębią (R2/R5) dla hero; ekran operacyjny pozostaje płaski, gęsty i czytelny.
- **Dynamika/motion:** powolny dryf świateł aurory (tło, ≤ subtelny); dane „rysują się"
  przy wejściu (linia/teren narasta); przejścia między warstwami głębi (Z), nie reveal
  sekcji; pełny reduced-motion fallback; 60 fps, transform/opacity.
- **Dobór wariantu:** dashboard operacyjny → czerń + metal, restrykcyjnie (R1/R2, zero
  bloom w tabelach) • hero/landing/marketing → teren 3D, gradient-fill, aurora (R2/R3/R4)
  • aplikacja mobilna → frosted light (R5) albo czerń dyżurowa; dualnie jak w Pracowni.
- **TickerLab:** kierunek z `frontend-design-tickerlab` (instytucjonalny terminal) pozostaje
  bazą dashboardu; ten profil dostarcza mu warstwę materiałową (metal danych, hairline,
  aurora w hero) — łączyć bez naruszania gęstości i czytelności tabel.

## 3. Guardrails (żeby ten język nie osunął się w slop)

1. Metal/gradient/bloom świecą **tylko tam, gdzie są dane albo źródło światła** — nigdy
   na ramkach, badge'ach, nagłówkach, przyciskach.
2. Jeden bohater świetlny na ekran (jedna seria z gradientem ALBO metaliczny zestaw —
   nie wszystko naraz).
3. Kontrast treści zawsze wyliczony (AA; dane ≥3:1); mikro-etykiety nie schodzą poniżej
   progu na czerni.
4. 3D tylko jako reprezentacja danych/mechanizmu (teren = zmienność), z budżetem,
   fallbackiem statycznym i reduced-motion.
5. Izometria = język materiałów marketingowych/hero; widoki robocze pozostają proste.
6. Test logo obowiązuje nadal: kompozycja + sygnatura (nić dowodu / metal danych +
   copper edge) mają czynić projekt nieprzenośnym.

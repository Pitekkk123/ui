# 04 — Bramki akceptacji i odrzucenia

Cztery bramki: (A) automatyczna bramka odrzucenia, (B) adversarial review, (C) obowiązkowe
testy, (D) anti-AI-slop review + Definition of Done. Litery to etykiety sekcji, nie kolejność
wykonania. Kolejność zgodna z sekwencją SKILL.md: sygnatury z bramki A sprawdzaj już na etapie
koncepcji i po każdej iteracji; przed oddaniem: testy (C) → adversarial review (B) → naprawa
problemów krytycznych → ponowne testy → anti-AI-slop review i Definition of Done (D).

## A. Automatyczna bramka odrzucenia

**Odrzuć projekt i przeprojektuj od podstaw** (zmiana założenia, struktury, hierarchii, języka
wizualnego, sposobu prezentacji informacji — NIE zmiana koloru, zmniejszenie glow, zmiana
radiusu ani usunięcie jednego badge'a), jeżeli wystąpią **co najmniej dwa** z poniższych:

1. dark SaaS z neonowym akcentem;
2. gradientowy headline;
3. pigułka nad hero;
4. nadmiar zaokrąglonych kart;
5. karta wewnątrz karty;
6. szkło na większości powierzchni;
7. gradientowe obramowania;
8. badges w wielu komponentach;
9. neonowe statusy;
10. gamingowa prezentacja danych (trofea, wieńce);
11. modal będący osobną aplikacją;
12. ściana checkboxów;
13. widoczny Markdown;
14. fantasy command center;
15. dekoracyjna scena 3D;
16. losowy stockowy render;
17. niska czytelność;
18. tekst przycięty przez kontener;
19. osiem elementów dolnej nawigacji;
20. zbyt wiele równorzędnych pozycji menu;
21. brak widocznego głównego zadania;
22. wygląd możliwy do przeniesienia do dowolnego startupu.

## B. Adversarial review (obowiązkowy)

Builder nie zatwierdza sam swojej pracy. Po wykonaniu przełącz się w rolę niezależnego krytyka,
którego zadaniem jest **znalezienie powodów do odrzucenia**, nie potwierdzenie jakości.

Krytyk szuka: generyczności; AI slopu; niespójności; ukrytych atrap; brakujących stanów;
problemów na mobile; problemów z kontrastem; problemów z focus; overflow; fałszywej
wiarygodności; dekoracyjnych efektów bez funkcji; nieczytelnych danych; niewystarczających
testów; niezgodności z briefem.

Krytyk nie może: potwierdzać jakości bez analizy; uznawać projektu za dobry, bo jest
estetyczny; łagodzić krytyki, by chronić wcześniejszą pracę.

Po review: napraw problemy krytyczne → ponów testy → powtórz bramkę anti-AI-slop.

## C. Obowiązkowe testy

Przed deklaracją ukończenia wykonaj odpowiednie dla zakresu:

- **kod:** lint; format; typecheck; build; testy jednostkowe; komponentów; integracyjne;
  end-to-end; visual regression;
- **dostępność:** accessibility audit (axe-core); keyboard navigation; focus test; zoom 200%;
  reduced motion; increased contrast; reduced transparency; screen reader / VoiceOver;
- **responsywność:** matryca z `05_device_matrix.md`; small-screen; desktop; real-device;
- **treść i dane:** long-content; polskie znaki; duże liczby; puste dane; błędne dane;
- **stany:** loading; offline; error; retry; powrót do poprzedniego stanu;
- **wydajność:** budżet JS; obrazy; fonty; animacje; słabsze urządzenie;
- **interakcje:** wszystkie przyciski; wszystkie linki; formularze (walidacja, submit,
  klawiatura, utrata połączenia);
- **eksporty:** każdy plik otwarty i obejrzany (PPTX w docelowym programie, PDF strona po
  stronie, HTML w przeglądarce).

- **regresje operatora** (część V bazy `13_fintech_style_profile.md`): overflow liter poza
  kafelki na realnych treściach; tokeny odziedziczone w KAŻDYM nowym module (oba motywy);
  font-check każdego widoku (bez degradacji do stockowych); test 5 stanów każdego przycisku;
  palety wyliczone i zharmonizowane.

Testuj działanie, nie obecność elementów. Dla funkcji krytycznych pełny przepływ end-to-end.
Po naprawie błędu — test regresji. **Testu niewykonanego nie oznaczaj jako zaliczony** —
powiedz, że nie został wykonany i dlaczego.

## D. Anti-AI-slop review — 20 pytań

Przed oddaniem odpowiedz wewnętrznie:

1. Czy projekt wyglądałby tak samo po zmianie nazwy firmy?
2. Czy kolory wynikają z marki i funkcji?
3. Czy każda karta jest naprawdę potrzebna?
4. Czy można usunąć połowę kontenerów?
5. Czy hierarchię można zbudować bez obramowania?
6. Czy gradient pełni funkcję?
7. Czy glow pełni funkcję?
8. Czy 3D wyjaśnia coś istotnego?
9. Czy hero natychmiast wyjaśnia produkt?
10. Czy główna akcja jest oczywista?
11. Czy nawigacja odzwierciedla priorytety?
12. Czy złożone zadanie nie zostało wciśnięte do modalu?
13. Czy treść została zredagowana dla interfejsu?
14. Czy produkt pozostaje użyteczny bez animacji?
15. Czy wersja mobilna została zaprojektowana, a nie tylko zmniejszona?
16. Czy dostępność jest zachowana?
17. Czy wygląd nie udaje wiarygodności?
18. Czy istnieje jedna rozpoznawalna decyzja artystyczna?
19. Czy projekt przypomina pracę konkretnego zespołu, a nie anonimowego generatora?
20. Czy wszystkie elementy rzeczywiście działają?

Negatywna odpowiedź w obszarze krytycznym = projekt nie jest gotowy.

## Definition of Done

Ukończony dopiero, gdy: spełnia brief; realizuje główne zadanie użytkownika; ma prawidłową
architekturę informacji i spójny system wizualny; nie przejawia niedopuszczalnego AI slopu;
działa funkcjonalnie; obsługuje wymagane stany; jest responsywny i dostępny; przeszedł wymagane
testy na wymaganych urządzeniach; eksporty zostały otwarte i obejrzane; wszystkie przyciski
i linki zweryfikowane; dane oznaczone zgodnie ze statusem; znane ograniczenia ujawnione;
adversarial review nie zostawił problemów krytycznych.

**Nie jest ukończony**, gdy: istnieje tylko atrakcyjny screenshot; część przycisków to atrapy;
treść przykładowa jest nieoznaczona; mobile to pomniejszony desktop; testy nie zostały
uruchomione; plik nie został otwarty; są błędy overflow; występują ≥2 sygnatury bramki A.

## Zasada uczciwości (show, don't claim)

Nie przedstawiaj projektu jako „premium / award-winning / studio-quality / dopracowany /
finalny / production-ready / responsywny / dostępny / przetestowany / działa na iOS", jeżeli
nie został uruchomiony, wizualnie sprawdzony, przetestowany responsywnie, sprawdzony na mobile,
pod względem dostępności i overflow oraz oceniony przez bramkę anti-AI-slop. Nie deklaruj
sukcesu dlatego, że plik został wygenerowany albo kod się kompiluje. Zawsze oddzielaj:
wykonane / niewykonane / przetestowane / nieprzetestowane / działające / demonstracyjne /
produkcyjne / założone / zweryfikowane.

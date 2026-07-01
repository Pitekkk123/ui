# 01 — Bezwzględny zakaz AI slopu (katalog sygnatur)

Stała dyrektywa wizualna. Obowiązuje przy każdym artefakcie oglądanym przez człowieka:
www, web app, PWA, mobile, dashboard, prezentacja HTML, PowerPoint, PDF, raport, obraz,
infografika, wideo, animacja, logo, hero, kafelek, panel, wykres, diagram, UI/UX,
redesign kolorystyczny, elementy osadzane.

**Zasada nadrzędna:** nie wolno tworzyć projektu przypominającego generyczny produkt
wygenerowany przez AI, szablon SaaS, mockup z Dribbble, dashboard low-code, gotowy motyw
Tailwind ani wizualizację udającą złożoność. Nie wolno usprawiedliwiać takiego wyniku słowami
„nowoczesny / futurystyczny / premium / technologiczny / AI-native / cinematic / glass /
immersive / award-winning". Jeżeli rozwiązanie jest generyczne, pozostaje generyczne
niezależnie od liczby efektów.

Wykrycie sygnatury = powód do odrzucenia koncepcji, nie do kosmetycznej poprawki
(patrz `04_acceptance_gates.md`).

## 1. Generyczny dark SaaS i fintech

Zakazane automatycznie:

- czarne lub ciemnogranatowe tło użyte bez uzasadnienia;
- neonowy turkus, fiolet, zieleń albo pomarańcz jako domyślny akcent;
- gradientowe słowo w ogromnym nagłówku;
- biała typografia na ciemnym tle bez rozwiniętej koncepcji;
- ten sam wygląd dla tradingu, AI, medycyny, SaaS i kryptowalut;
- zatłoczona top navigation;
- etykiety Pro, Beta, Starter, Featured, AI-powered;
- układ pill → hero → KPI box → form → cards;
- zielone procenty jako główna estetyka.

Dark mode wyłącznie, gdy wynika z warunków użytkowania, treści, marki, potrzeby ograniczenia
luminancji lub preferencji użytkownika. „Fintech" ≠ czerń, zieleń i wykresy. „AI" ≠ fiolet
i gradient. „Premium" ≠ złoto i glow.

## 2. Monokultura zaokrąglonych prostokątów

Zakazane:

- karta dla każdej informacji / każdego akapitu;
- karta wewnątrz karty, panel wewnątrz panelu;
- każdy filtr w kapsule, każdy status w badge;
- identyczny radius dla przycisków, paneli, pól i sekcji;
- obramowanie każdej sekcji;
- rounded rectangle jako podstawowy język całego produktu.

Najpierw hierarchia przez: typografię, pozycję, odstęp, grid, wyrównanie, kontrast powierzchni,
linię, rytm. Karta dopuszczalna tylko jako rzeczywista jednostka funkcjonalna (własny stan,
akcja, przenoszalność).

## 3. Badges, pills i status chips

Nie stosuj automatycznie kapsuł: Pro, Beta, New, Starter, Featured, Recommended, Advanced,
Moderate, AI-powered, TAK, NIE, WARN. Kapsuła nie jest podstawową gramatyką interfejsu.
Status przekazuj przez treść, pozycję, hierarchię, subtelny kolor, ikonę z etykietą i opis
konsekwencji. Każdy badge musi mieć konkretną funkcję informacyjną.

## 4. Nadużycie glassmorphismu

Zakazane: blur na wszystkich panelach; szkło na szkle; przezroczystość pod długim tekstem;
refleksy i refrakcja bez źródła światła; biała półprzezroczysta ramka jako główna hierarchia;
pseudo-Liquid-Glass złożony wyłącznie z `backdrop-filter` i białego borderu.

Materiał szklany wymaga: konkretnej roli, wiarygodnego światła, określonej relacji z tłem,
fallbacku bez przezroczystości, poprawnego kontrastu, wsparcia Reduce Transparency
i ograniczonego zakresu użycia.

## 5. Neonowe pseudo-premium

Zakazane: gradientowe bordery; fioletowe i niebieskie glowy; świecące ramki; aureole wokół
paneli; neonowe ikony; błyszczące rekomendacje; wieńce laurowe; trofea; gamingowe ekrany
wyników; złoto wyłącznie jako sygnał luksusu.

Wrażenie jakości ma wynikać z proporcji, typografii, materiałów, fotografii, kompozycji,
redakcji treści i dokładności wykonania.

## 6. Fantastyczne metafory systemów

Zakazane: świątynie AI; pałace wiedzy; magiczne wieże; steampunkowe fabryki; wielopiętrowe
centra dowodzenia; przewody energii; samotne postacie patrzące na system; pseudo-techniczne
tabliczki wokół ilustracji; metafory niepokazujące realnych zależności.

Architekturę systemu pokazuj jako: diagram przepływu, mapę zależności, graf, model danych,
warstwy, sekwencję, timeline, diagram stanów lub interaktywną wizualizację.

## 7. Generyczne hero

Zakazane: „Reimagine the future"; „Unlock your potential"; „The future of AI"; „Powered by AI"
bez konkretu; przypadkowa kula 3D; chromowany pierścień; abstrakcyjna wstęga; unoszący się
laptop; telefon pod kątem; losowe cząsteczki; ekran produktu bez kontekstu; badge nad
nagłówkiem bez funkcji.

Hero musi natychmiast wyjaśniać: czym jest produkt, dla kogo, jaki problem rozwiązuje,
co użytkownik może wykonać, jaka jest główna akcja i dlaczego produkt jest istotny.

## 8. Modal jako aplikacja

Zakazane: rozbudowana aplikacja w modalu; wieloetapowy kreator w małym oknie; modal większy
niż viewport; scroll wewnątrz scrolla; długa lista kart w modalu; taby w kapsułach; ogromny
przycisk zamknięcia; glow wokół X; wieloakapitowa dokumentacja w oknie dialogowym.

Złożone zadania dostają: pełną podstronę, dedykowany workspace, tryb pełnoekranowy lub panel
boczny — z zapisem stanu i możliwością powrotu.

## 9. Ściany checkboxów

Zakazane: dziesiątki równorzędnych opcji; dwie kolumny bez hierarchii; ustawienia bez opisu
konsekwencji; brak presetów; brak wyszukiwania; brak progressive disclosure; identyczny wygląd
funkcji krytycznej i marginalnej; konfiguracja całego systemu na jednym ekranie.

Sekwencja: wybór celu → rekomendowany profil → trzy najważniejsze decyzje → podgląd skutku →
opcjonalne ustawienia eksperckie. Pokazuj wpływ ustawienia, konflikty, wymagane dane, koszt
obliczeniowy, wartość domyślną i możliwość resetu.

## 10. Surowa treść modelu w UI

Zakazane: widoczne znaczniki Markdown; ściany tekstu w małych kartach; nieprzetworzone
odpowiedzi modelu; przypadkowe boldowanie; źródła wciśnięte w środek akapitu; tekst przycięty
bez kontroli; wieloakapitowa treść za wewnętrznym scrollem; log techniczny jako gotowa treść.

Treść musi być zredagowana, podzielona, opisana, ułożona według priorytetu, dopasowana do
powierzchni i wyposażona w źródła oraz kontekst, gdy są wymagane.

## 11. Sztuczna wiarygodność

Zakazane budowanie zaufania wyłącznie przez: wygląd premium, liczbę metryk, zielone wyniki,
logotypy partnerów bez kontekstu, pseudonaukowe ikony, tytuły ekspertów, plakietki
rekomendacji, animowane liczniki.

Wiarygodność wynika ze: źródeł, metodologii, daty danych, autorstwa, zakresu niepewności,
ograniczeń, możliwości audytu i reprodukowalności wyniku. Hipotezy nie przedstawiaj jako faktu;
fikcyjne metryki zawsze oznaczaj jako przykładowe.

## 12. Dekoracyjna animacja i dekoracyjne 3D

Zakazane: reveal każdej sekcji; losowy parallax; unoszenie każdej karty; ciągłe pulsowanie;
blob motion; wirujące gradienty; przypadkowe cząsteczki; layout shift na hover; animacja
opóźniająca dostęp do treści; kula/orbita/chromowany torus/abstrakcyjne szkło/unosząca się
rzeźba bez funkcji.

Animacja służy tylko: orientacji, ciągłości, feedbackowi, relacji przyczynowej, zmianie stanu,
hierarchii, narracji produktu — z celem, czasem trwania, warunkiem uruchomienia,
reduced-motion fallback i zachowaniem przy słabszej wydajności. 3D tylko, gdy reprezentuje
produkt, pokazuje mechanizm, wyjaśnia strukturę lub dane, buduje spójny świat marki i sensownie
reaguje na użytkownika — z budżetem wydajnościowym i statycznym fallbackiem.

# 02 — Anty-referencje: 6 studiów przypadku

Analiza rzeczywistych złych przykładów (zamiennik pliku `02_ANTI_REFERENCES.pdf` ze
screenshotami — pełny opis tekstowy jest bardziej niezawodny niż obrazy). Wszystkie pokazują
ten sam głębszy problem: **symulują jakość przez nagromadzenie konwencji kojarzonych
z technologią, premium, AI lub fintechem, zamiast zbudować klarowną architekturę informacji,
autorski język wizualny i poprawne interakcje.** Są szczególnie niebezpieczne, bo powierzchownie
wyglądają na „dopieszczone" — w rzeczywistości są szablonowe, mało wiarygodne i szybko się
starzeją.

## Przypadek 1 — Fantastyczna „świątynia AI" / command center

Wielopiętrowa budowla ze złotymi przewodami energii, fioletową mgłą, zieloną aurą, drobnymi
tabliczkami i monumentalną postacią; stylistyka steampunk/fantasy/game concept art.

Dlaczego złe:

- **udaje architekturę systemu** — nie pokazuje przepływu danych, zależności, kolejności
  działań, interfejsów, odpowiedzialności modułów, punktów kontroli ani błędów; to metafora
  zasłaniająca strukturę, nie struktura;
- **udaje złożoność** — mnogość pięter i świateł sugeruje ogromny system, ale nie dostarcza
  informacji (wizualny odpowiednik rozwlekłego tekstu, który brzmi technicznie, a niczego
  nie definiuje);
- **jest nieczytelne** — podpisy za małe, słabo skontrastowane, oderwane od opisywanych
  elementów;
- **jest generyczne** — tak wygląda każda grafika typu „AI operating system", „second brain",
  „agent command center", „knowledge palace"; zmieniają się nazwy pięter, kompozycja zostaje.

Zamiast tego: diagram przepływu, mapa zależności, oś czasu, graf, warstwy systemowe,
interaktywna wizualizacja, jasno opisane moduły.

## Przypadek 2 — Generyczny ciemny landing fintech/SaaS („Invest Like the Pros")

Granatowo-czarne tło, ogromny biały nagłówek z fragmentem w pomarańczowym gradiencie, kapsuła
nad nagłówkiem, zatłoczona nawigacja, etykiety Pro/Starter, boks „track record", wielka karta
formularza, pomarańczowy przycisk, cienkie jasne obramowania, wszystko wyśrodkowane.

Dlaczego złe:

- **brak indywidualności** — po usunięciu nazwy firmy ten sam layout reklamowałby narzędzie AI,
  krypto, SaaS, platformę tradingową, kurs inwestowania albo cyberbezpieczeństwo; design nie
  wynika z produktu;
- **nadużywa konwencji zaufania** — „Real Investors", „Public Data", „Track Record", liczniki,
  zielone wyniki produkują wrażenie wiarygodności, którego wygląd nie dowodzi;
- **zła hierarchia** — zbyt wiele równorzędnych pozycji nawigacji; nie wiadomo, od czego zacząć
  ani czym jest główny produkt;
- **szablon**: pill → headline → subtitle → KPI box → email form → cards.

## Przypadek 3 — Fioletowa neonowa tabela porównania modeli

Czarne tło, fioletowe poświaty, świecące obramowania, duże logotypy, statusowe kapsuły
TAK/NIE/ZALEŻY, trofeum, wieniec laurowy, plakietka „rekomendacja", ikona przy każdym nagłówku,
obramowane boksy, nadmiar tekstu i ozdób równocześnie.

Dlaczego złe:

- **gamifikuje analizę** — trofea i wieńce zamieniają analizę w ekran wyników gry; w raporcie
  liczą się kryteria, źródła, niepewność, ograniczenia, założenia i wyniki, nie dekoracyjny
  „zwycięzca";
- **kolor zastępuje treść** — jaskrawe TAK/NIE upraszczają problemy wymagające warunków,
  zakresów i poziomu pewności;
- **efekty udają premium** — glow, szkło i neon obniżają wiarygodność analityczną;
- **nadmierne kodowanie** — kolor + ikona + tekst + obramowanie + cień + glow + plakietka
  + ilustracja naraz; każdy element krzyczy.

Lepsza forma: spokojna tabela, precyzyjne kryteria, subtelne oznaczenia, pasek pewności lub
zakres, przypisy, sortowanie, jawne źródła, werdykt tekstowy z uzasadnieniem.

## Przypadek 4 — Generyczny mobilny screener finansowy

Czarne tło, serifowy nagłówek „premium", kapsuły kategorii, jeden wielki zaokrąglony panel,
kolorowe symbole tickerów, mini-sparkline przy każdym aktywie, dolna nawigacja z ośmioma
pozycjami, szare niskokontrastowe etykiety.

Dlaczego złe:

- **mockup z Dribbble, nie produkt** — nie odpowiada, jak wyszukiwać, sortować, obsłużyć setki
  instrumentów, błędy danych, długie nazwy, tryb dostępności, zmianę orientacji, widok
  szczegółu;
- **przepełniona dolna nawigacja** — osiem pozycji = brak priorytetyzacji funkcji;
- **niespójna typografia** — serif doklejony jako ozdobnik, nie wynika z produktu;
- **wszystko w kapsułach** — brak kontrastu między strukturą strony a treścią.

## Przypadek 5 — Modale „Signal setup" / „Playbooks" (najgorszy wzorzec zestawu)

Modal w centrum aplikacji, trzy zakładki jako kapsuły, gigantyczny przycisk zamknięcia,
karty w modalu i karty w kartach, ściany tekstu, plakietki Featured, tagi Swing/Moderate,
przycięta zawartość, wewnętrzny scroll, widoczne znaki Markdown `**`, za mały tekst.

Dlaczego złe:

- **modal próbuje być aplikacją** — modal nadaje się do potwierdzenia, krótkiej decyzji,
  prostego formularza, szybkiej edycji; nie do wieloetapowej konfiguracji systemu;
- **karty zastępują architekturę informacji** — zamiast wyszukiwania, filtrów, porównania,
  skróconych opisów, widoku szczegółowego i grupowania — każda strategia wrzucona w kolejną
  kartę;
- **treść niezaprojektowana** — surowy Markdown, długie akapity, przypadkowe źródła, brak
  redakcji;
- **nie skaluje się** — z każdą strategią modal jest dłuższy, trudniejszy do przeszukiwania,
  gorszy na mobile.

Lepszy wzorzec: pełna podstrona konfiguracji; lista z wyszukiwaniem; panel boczny szczegółów;
krótki opis w liście, szczegóły po rozwinięciu; porównanie strategii; zapisany stan;
podsumowanie skutków konfiguracji.

## Przypadek 6 — Ściany checkboxów w „Advanced Settings"

Dwie kolumny checkboxów, dziesiątki opcji, długi pionowy scroll, kapitalikowe nagłówki,
niewiele wyjaśnień, modal większy niż ekran, brak podsumowania wyboru.

Dlaczego złe:

- **przerzuca złożoność architektury na odbiorcę** — użytkownik musi rozumieć wszystkie
  wskaźniki, strategie, zależności, konflikty i sens każdej opcji;
- **brak progressive disclosure** — początkujący i ekspert widzą ten sam formularz; brak
  presetów, rekomendacji, profili, poziomów zaawansowania, podglądu wpływu;
- **brak priorytetów** — opcja marginalna wygląda tak samo ważnie jak krytyczna;
- **brak informacji o skutkach** — nie wiadomo, jak wybór wpłynie na wynik, czy opcje się
  wykluczają, jaki jest koszt obliczeniowy, czy dane są dostępne, co jest zalecane.

Lepsze rozwiązanie: wybór celu → rekomendowany profil → najważniejsze trzy decyzje →
podgląd działania → opcjonalne ustawienia eksperckie.

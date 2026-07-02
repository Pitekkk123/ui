# 05 — Matryca urządzeń i viewportów

## Desktop / laptop

Testuj co najmniej:

| Viewport (px CSS) | Uwagi |
|-------------------|-------|
| 1280 × 800 | najmniejszy sensowny laptop |
| 1366 × 768 | nadal bardzo popularny |
| 1440 × 900 | typowy MacBook-class |
| 1600 × 1000 | |
| 1920 × 1080 | standard FHD |
| 1920 × 1200 | 16:10 |
| rzeczywisty viewport głównego laptopa operatora | patrz niżej: ASUS ProArt |
| zoom przeglądarki 100% / 125% / 200% | obowiązkowo wszystkie trzy |

Nie projektuj wyłącznie pod fizyczną rozdzielczość ekranu — uwzględnij skalowanie systemowe.
Sprawdzaj: szerokość treści, overflow, sticky elements, viewport height, rozwinięte menu,
otwarte devtools, pasek systemowy, długi tekst, duże tabele, wiele kolumn.

### Stanowisko operatora: ASUS ProArt (16″ 4K OLED, RTX 5090, 64 GB RAM)

Panel fizyczny 3840 × 2400, ale Windows stosuje skalowanie — przeglądarka pracuje na znacznie
mniejszej liczbie pikseli CSS. **Nie traktuj 3840 × 2400 jako viewportu projektowego.**
Sprzęt wystarcza na Blender, DaVinci Resolve/Fusion, lokalny rendering i materiały 4K/8K —
ciężkie testy wydajnościowe wykonuj mimo to z throttlingiem CPU/GPU (użytkownicy nie mają
RTX 5090).

## iPhone 16 Pro Max (główne fizyczne urządzenie QA)

- ekran OLED 6,9″, 2868 × 1320 px fizycznych, P3, do 120 Hz;
- przybliżony viewport CSS w pionie: **440 × 956** — ale safe area jest dynamiczna
  (Dynamic Island, dolny obszar gestów, klawiatura);
- minimalne obszary dotyku: **≈44 × 44 pt**.

Testuj na rzeczywistym urządzeniu:

- orientacja pionowa i pozioma;
- Dynamic Type (większy tekst) i długie polskie napisy;
- VoiceOver; Reduce Motion; Increase Contrast; Reduce Transparency;
- aktywna klawiatura ekranowa;
- słabe połączenie i utrata połączenia;
- powrót aplikacji z tła, przerwanie sesji, przywrócenie stanu;
- deep links i cofanie w hierarchii nawigacji;
- jasny wygląd; ciemny tylko, gdy uzasadniony.

Zakazy iOS: osiem równorzędnych pozycji tab bara; nieopisane ikony kluczowych funkcji;
desktopowe hovery jako wymagana interakcja; bardzo małe kontrolki; informacja zależna tylko
od koloru.

## iOS z Windows — uczciwa ścieżka

- pełny pipeline SwiftUI wymaga Xcode, a Xcode wymaga macOS — **nie twierdź, że natywna
  aplikacja SwiftUI została lokalnie uruchomiona bez dostępu do macOS**;
- domyślna ścieżka prototypowa: **React Native + Expo** — projekt w Figma → implementacja RN →
  szybki test przez Expo Go na iPhone 16 Pro Max → development build i binaria przez EAS Build →
  publikacja przez EAS Submit (działa z Windows/Linux);
- zaawansowane funkcje (pełny SwiftUI, Live Activities, widżety, głębokie integracje,
  profilowanie, natywny Liquid Glass) → jawnie wskaż konieczność natywnego środowiska Apple;
  Mac staje się potrzebny przy zaawansowanym wdrożeniu i końcowym QA, nie przy pierwszym
  prototypie.

## Ekrany prezentacyjne i druk

- prezentacje: 16:9, czytelność z odległości, tryb pełnoekranowy, kontrola overflow na każdym
  slajdzie;
- PDF drukarski: format, marginesy, spady, łamanie stron, sieroty i wdowy — oglądany strona
  po stronie po wyrenderowaniu.

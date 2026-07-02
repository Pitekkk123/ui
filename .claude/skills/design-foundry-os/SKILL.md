---
name: design-foundry-os
description: Konstytucja designu DESIGN FOUNDRY OS dla każdego zadania wizualnego w tym repo — komponenty, bloki, motywy, registry, dokumentacja, dema, strony, dashboardy, prezentacje. Egzekwuje anty-AI-slop gate, alignment gate, brief, obowiązkowe stany, testy i adversarial review. shadcn/ui dostarcza zachowanie i primitives — NIGDY art direction. Aktywuj przy KAŻDYM zadaniu projektowym lub frontendowym, zanim powstanie pierwszy piksel lub linia kodu UI.
---

# DESIGN FOUNDRY OS — skill operacyjny (repo ui / shadcn)

Kanoniczny dokument: `references/00_constitution.md` (38 sekcji). Ten skill to warstwa
egzekucji: co sprawdzić, w jakiej kolejności, z jakimi bramkami. Przy konflikcie decyduje
konstytucja, a nad nią — jawna decyzja użytkownika.

## Kiedy obowiązuje

Każde zadanie, którego wynik jest oglądany: komponent, blok, motyw/preset, strona, landing,
web app, dashboard, dokumentacja, demo w registry, prezentacja, grafika, animacja, redesign
i color-only redesign. Słowa „nowoczesny / premium / futurystyczny / AI / fintech / dashboard /
glass / 3D" **nie są** zgodą na generyczne efekty.

## Relacja do shadcn/ui (kluczowa dla tego repo)

- **shadcn = zachowanie, dostępność, primitives, logika. Nie art direction.** Konstytucja §16
  zakazuje traktowania Tailwind/shadcn/MUI/Bootstrap jako języka wizualnego.
- Mechanika komponentów (kompozycja, formularze przez `Field`/`FieldGroup`, warianty, tokeny
  semantyczne, CLI) → skill `shadcn` (`skills/shadcn/SKILL.md`). Ten skill nadaje się do
  „jak poprawnie złożyć" — DESIGN FOUNDRY OS decyduje „co i po co powstaje oraz jak ma
  wyglądać".
- Własny język wizualny buduj przez tokeny (CSS variables, `bg-primary`,
  `text-muted-foreground`…), typografię, grid, rytm i skalę — nie przez nowe kontenery,
  bordery i badges.
- Domyślny wygląd shadcn w demach registry jest akceptowalny jako **neutralna baza
  dokumentacyjna**; produkt końcowy zbudowany na tych komponentach musi mieć własny system
  wizualny i przejść bramki poniżej.

## Sekwencja pracy (nie pomijaj kroków)

1. **Brief** — `references/06_task_brief_template.md`; dla zadań wyłącznie webowych rozszerzony
   `references/09_uxui_web_brief.md`. Fakty ≠ założenia ≠ preferencje. Braki nieblokujące:
   załóż i oznacz. Braki blokujące: maks. 5 precyzyjnych pytań.
2. **Alignment gate** — użytkownik, problem, główne zadanie, główna akcja, platforma, zakres,
   metryka sukcesu, elementy chronione, profil stylistyczny, kryteria akceptacji. Nowy produkt /
   pełny redesign → **3 rzeczywiście odmienne koncepcje** + krytyka + rekomendacja. Drobna
   poprawka / color-only → dokładnie zamówiony zakres.
3. **Referencje** — `references/03_reference_dna.md`: profil główny 60–70%, wspierający 20–30%,
   akcentowy ≤10%. Zasady, nie powierzchnia.
4. **System wizualny przed dekoracją** — grid, rytm, skala typografii, paleta neutralna + maks.
   1–2 akcenty, kolory semantyczne i danych, materiały, motion, stany focus/hover/active/
   disabled. Hierarchia najpierw typografią, przestrzenią, wyrównaniem, skalą, kontrastem —
   kontenery na końcu. Jedna rozpoznawalna decyzja artystyczna na projekt.
5. **Implementacja** — pełne stany (`initial / loading / empty / partial / stale / error /
   retry / offline / disabled / success / long content / large dataset / permission denied /
   session expired`), formularze z walidacją i obsługą klawiatury, zero atrap: element działa,
   jest wyłączony z wyjaśnieniem albo oznaczony jako demonstracyjny.
6. **Testy** — `references/05_device_matrix.md` + lista w `references/04_acceptance_gates.md`;
   w tym repo dodatkowo: `pnpm check` (lint, typecheck, format) i właściwe `pnpm test`.
   Testu niewykonanego nie oznaczaj jako zaliczony.
7. **Adversarial review** — rola krytyka szukającego powodów do **odrzucenia** (generyczność,
   atrapy, brakujące stany, kontrast, focus, overflow, fałszywa wiarygodność). Napraw
   krytyczne, ponów testy.
8. **Bramka anti-AI-slop** — `references/04_acceptance_gates.md`. **≥2 sygnatury z bramki
   odrzucenia = redesign od podstaw**, nie kosmetyka.

## Bezwzględne zakazy (skrót — pełna lista w references/01 i 02)

Generyczny dark SaaS z neonem • gradientowy headline • pigułka nad hero • monokultura kart
i karta-w-karcie • badges/pills jako gramatyka UI • szkło wszędzie / pseudo-Liquid-Glass •
glow i gradientowe bordery • trofea, wieńce, gaming w danych • fantasy command center •
generyczne hero („Reimagine the future", kula 3D, laptop pod kątem) • modal jako aplikacja •
ściany checkboxów • widoczny Markdown i surowa treść modelu w UI • sztuczna wiarygodność •
dekoracyjna animacja i dekoracyjne 3D • fikcyjne metryki bez oznaczenia.

## Show, don't claim

Nie pisz „responsywny / dostępny / przetestowany / production-ready", jeśli nie zostało to
zweryfikowane. Pokaż: wykonane testy, wyniki, screenshoty, listę obsłużonych stanów, znane
ograniczenia i to, czego nie udało się sprawdzić. Utworzenie pliku ≠ działanie; kompilacja ≠
poprawny UX; brak lint errors ≠ kompletny produkt.

## Priorytety (rozstrzyganie konfliktów)

Poprawność funkcjonalna → bezpieczeństwo danych → główne zadanie użytkownika → architektura
informacji → czytelność → użyteczność → dostępność → spójność z marką → treść → przewidywalność →
responsywność → wydajność → utrzymanie → wykonanie → art direction → efekty → dekoracja.
Niższy poziom nigdy nie pogarsza wyższego.

## References

| Plik | Zawartość |
|------|-----------|
| `references/00_constitution.md` | Pełna konstytucja DESIGN FOUNDRY OS (38 sekcji) |
| `references/01_forbidden_ai_slop.md` | 12 grup zakazanych sygnatur — pełny katalog |
| `references/02_anti_references.md` | 6 studiów przypadku złych projektów (anty-wzorce) |
| `references/03_reference_dna.md` | Profile: Oura/Instrument, Fantasy, BASIC/DEPT, Thorne, BUCK, Apple |
| `references/04_acceptance_gates.md` | Bramka odrzucenia, 20 pytań review, testy, Definition of Done |
| `references/05_device_matrix.md` | Viewporty desktop, zoom, iPhone 16 Pro Max, iOS z Windows |
| `references/06_task_brief_template.md` | Szablon briefu każdego zadania |
| `references/07_toolchain.md` | Darmowy/tani toolchain: Figma, Affinity, Blender, GSAP, Rive… |
| `references/08_uxui_web_foundry.md` | Wariant web-only: stałe instrukcje projektu do wklejania (konstytucja nadrzędna) |
| `references/09_uxui_web_brief.md` | Rozszerzony brief zadań web-only (17 sekcji); para z 08 |
| `references/10_master_system_prompt.md` | Tryb turniejowy: 6 koncepcji, panel krytyków ≥84/100, reconnaissance |
| `references/11_slop_signatures_registry.md` | Pamięć trwała: 7 testów, 15 sygnatur → co zamiast, sygnatury per obszar, werdykt red-team (uwaga: nadpisuje „preferuj Inter") |

#!/usr/bin/env python3
"""
Macro Risk Overlay — Premium PDF Generator Part 1
Cover + Architecture + Credit/Rates Layers

Uses reportlab for professional white-themed design
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak,
    Image, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
import datetime

# Setup
WIDTH, HEIGHT = letter
MARGIN = 0.75 * inch
DOC = SimpleDocTemplate(
    "/home/user/ui/Macro_Risk_Overlay_Part1.pdf",
    pagesize=letter,
    rightMargin=MARGIN,
    leftMargin=MARGIN,
    topMargin=MARGIN,
    bottomMargin=MARGIN,
)

# Colors - Premium white theme
WHITE = colors.HexColor("#FFFFFF")
DARK_GRAY = colors.HexColor("#1F2937")
LIGHT_GRAY = colors.HexColor("#F3F4F6")
ACCENT_BLUE = colors.HexColor("#2563EB")
ACCENT_GOLD = colors.HexColor("#D97706")
LIGHT_BLUE = colors.HexColor("#EFF6FF")

# Styles
styles = getSampleStyleSheet()

# Title style
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=32,
    textColor=DARK_GRAY,
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

# Section heading
section_style = ParagraphStyle(
    'SectionHeading',
    parent=styles['Heading2'],
    fontSize=18,
    textColor=ACCENT_BLUE,
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

# Subsection heading
subsection_style = ParagraphStyle(
    'SubsectionHeading',
    parent=styles['Heading3'],
    fontSize=13,
    textColor=DARK_GRAY,
    spaceAfter=8,
    spaceBefore=8,
    fontName='Helvetica-Bold'
)

# Body text
body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    leading=14,
    alignment=TA_JUSTIFY,
    textColor=DARK_GRAY,
    spaceAfter=10
)

# Emphasis text
emphasis_style = ParagraphStyle(
    'Emphasis',
    parent=body_style,
    textColor=ACCENT_BLUE,
    fontName='Helvetica-Bold'
)

# Code/metadata style
code_style = ParagraphStyle(
    'CodeStyle',
    parent=styles['BodyText'],
    fontSize=8,
    leading=10,
    fontName='Courier',
    textColor=colors.HexColor("#4B5563"),
    backColor=LIGHT_GRAY,
    leftIndent=10,
    rightIndent=10,
    spaceAfter=8
)

story = []

# ═════════════════════════════════════════════════════════════════
# COVER PAGE
# ═════════════════════════════════════════════════════════════════

story.append(Spacer(1, 2*cm))
story.append(Paragraph("Macro Risk Overlay", title_style))
story.append(Paragraph("Kompletny Przewodnik Operacyjny", styles['Heading2']))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    "Architektura Daily Macro Snapshot Engine dla Momentum Fund",
    ParagraphStyle('Subtitle', parent=styles['Heading3'], fontSize=11, alignment=TA_CENTER, textColor=DARK_GRAY)
))
story.append(Spacer(1, 2*cm))

# Metadata
meta_data = [
    ["Dokument:", "Part 1 — Architecture & Credit/Rates Layers"],
    ["Data publikacji:", datetime.date.today().strftime("%Y-%m-%d")],
    ["Technologia:", "Python | FRED API | Cboe | Polygon/Massive"],
    ["Status:", "Premium White Edition — All Details Preserved"],
]
meta_table = Table(meta_data, colWidths=[2.5*cm, 10*cm])
meta_table.setStyle(TableStyle([
    ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
    ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
    ('TEXTCOLOR', (0, 0), (0, -1), ACCENT_BLUE),
    ('TEXTCOLOR', (1, 0), (1, -1), DARK_GRAY),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, LIGHT_GRAY]),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(meta_table)

story.append(Spacer(1, 2*cm))
story.append(Paragraph(
    "Kompletne szczegóły systemu zarządzania ryzykiem makroekonomicznym dla strategii momentum, "
    "ze szczególnym naciskiem na jakość danych, uczciwe nazewnictwo proxy i operacyjne wdrożenie.",
    body_style
))

story.append(PageBreak())

# ═════════════════════════════════════════════════════════════════
# SPIS TREŚCI
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("Spis Treści — Część 1", section_style))
story.append(Spacer(1, 0.3*cm))

toc_items = [
    "1. Czym jest ten system i dlaczego powstał",
    "2. Architektura: Co się dzieje od uruchomienia do decyzji",
    "3. Dlaczego dwie fazy, nie jedna",
    "4. Każdy wskaźnik — co mierzy i jak pomaga",
    "   4.1. Warstwa Credit (40% composite score)",
    "   4.2. Warstwa Rates (30% composite score)",
    "   4.3. Warstwa Volatility (30% composite score)",
]

for item in toc_items:
    indent = "     " if item.startswith("   ") else ""
    story.append(Paragraph(f"• {item}", body_style))

story.append(Spacer(1, 0.5*cm))
story.append(PageBreak())

# ═════════════════════════════════════════════════════════════════
# 1. CZYM JEST TEN SYSTEM
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("1. Czym jest ten system i dlaczego powstał", section_style))
story.append(Spacer(1, 0.2*cm))

intro_text = """
Wyobraź sobie, że prowadzisz fundusz momentum. Twoje modele selekcji — TickerLab — wyłapują akcje,
które przyspieszają. Breakouty, liderów sektorowych, spółki z rosnącą siłą względną. To działa.
Ale działa <b>warunkowo</b>.
<br/><br/>
Momentum nie jest strategią absolutną. Jest strategią <b>środowiskową</b>. Breakout w zdrowym rynku
i breakout w rynku, który się rozpada od środka — to dwa zupełnie różne zdarzenia, nawet jeśli
wyglądają identycznie na wykresie jednej spółki.
<br/><br/>
<b>Ten system nie mówi ci co kupić. Mówi ci w jakim świecie podejmujesz tę decyzję.</b>
"""

story.append(Paragraph(intro_text, body_style))
story.append(Spacer(1, 0.3*cm))

# ═════════════════════════════════════════════════════════════════
# 2. ARCHITEKTURA
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("2. Architektura: Co się dzieje od uruchomienia do decyzji", section_style))
story.append(Spacer(1, 0.2*cm))

arch_text = """
System pracuje w trzech równoczesnych strumieniach danych. Każdy strumiś zbiera oficjalne dane
z różnego źródła, parsuje je, i zwraca MetricPoint — strukturę danych zawierającą nie tylko wartość,
ale pełną metadaną o wiarygodności tej wartości.
"""
story.append(Paragraph(arch_text, body_style))
story.append(Spacer(1, 0.3*cm))

# Architecture table
arch_data = [
    ["Źródło", "Metryki", "Jakość", "Opóźnienie"],
    ["FRED API", "HY/IG OAS, NFCI, krzywe, DXY, VIX", "Tier A", "T (daily)"],
    ["Cboe CSV", "VIX, VVIX, VX settlements", "Tier A", "T (daily)"],
    ["Polygon/Massive", "SPY/SPX gamma*OI proxy", "Tier B", "T (real-time)"],
    ["yfinance", "TLT realized vol proxy", "Tier B", "T (daily)"],
    ["Placeholder", "Breadth (McClellan, TRIN, NH/NL)", "Tier B", "TBD"],
]

arch_table = Table(arch_data, colWidths=[2.2*cm, 5*cm, 1.5*cm, 2.5*cm])
arch_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('TOPPADDING', (0, 0), (-1, 0), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 1), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
]))
story.append(arch_table)
story.append(Spacer(1, 0.4*cm))

pipeline_desc = """
<b>Pipeline flow:</b> Fetchers pobierają dane w paraleli → każdy zwraca MetricPoint (value, asof, source, status, quality_tier, methodology) →
pipeline.py agreguje snapshot → signals.py liczy composite score (credit 40%, rates 30%, vol 30%) →
storage.py zapisuje latest_snapshot.json + history.parquet.
"""
story.append(Paragraph(pipeline_desc, body_style))
story.append(Spacer(1, 0.3*cm))

# ═════════════════════════════════════════════════════════════════
# 3. DLACZEGO DWIE FAZY
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("3. Dlaczego dwie fazy, nie jedna", section_style))
story.append(Spacer(1, 0.2*cm))

phases_text = """
Cboe publikuje oficjalne settlementy futures VX dopiero około <b>10:00 rano czasu centralnego</b>
<b>następnego dnia roboczego</b>. Jeśli zbudujesz snapshot po zamknięciu rynku i wrzucisz do niego
VX settlement z tego samego dnia, dostajesz dane preliminary albo wczorajsze — ale twój system
tego nie wie. Traktuje je jak "dzisiejsze oficjalne".
<br/><br/>
<b>To klasyczny błąd dashboardów makro:</b> wynik wygląda dokładny, ale wejścia mają różne opóźnienia.
Dlatego rozdzielamy:
"""
story.append(Paragraph(phases_text, body_style))
story.append(Spacer(1, 0.2*cm))

phases_data = [
    ["Faza", "Czas", "Zawartość", "Status"],
    ["Prelim", "Po zamknięciu (16:30-17:00 ET)", "FRED, Cboe VIX/VVIX, TLT proxy, Polygon, breadth placeholder", "preliminary"],
    ["Official Reconcile", "T+1, ~10:00 CT", "VX settlement curve, aktualizacja vol stack", "official_settlement"],
]

phases_table = Table(phases_data, colWidths=[2*cm, 3*cm, 6*cm, 2.5*cm])
phases_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT_GOLD),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(phases_table)
story.append(Spacer(1, 0.3*cm))

phases_conclusion = """
Snapshot jawnie oznacza swoją fazę. Nigdy nie mieszasz "preliminary" z "official" w jednym kubełku.
Operator wie dokładnie, które dane są bieżące, które zaplanowane do aktualizacji, i które czekają
na oficjalne potwierdzenie z następnego dnia.
"""
story.append(Paragraph(phases_conclusion, body_style))

story.append(PageBreak())

# ═════════════════════════════════════════════════════════════════
# 4. KAŻDY WSKAŹNIK — CREDIT LAYER
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("4. Każdy wskaźnik — co mierzy, dlaczego jest tu, i jak pomaga TickerLab", section_style))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("4.1 Warstwa Credit (40% composite score)", subsection_style))
story.append(Spacer(1, 0.15*cm))

# HY OAS
story.append(Paragraph("HY OAS — High Yield Option-Adjusted Spread", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

hy_oas_meta = "<b>FRED:BAMLH0A0HYM2</b> | <b>Tier A</b> (Official, auditable)"
story.append(Paragraph(hy_oas_meta, code_style))
story.append(Spacer(1, 0.1*cm))

hy_oas_text = """
<b>Co to jest:</b> Różnica w rentowności między obligacjami korporacyjnymi o ratingu śmieciowym
(high yield) a porównywalnym benchmarkiem rządowym, po oczyszczeniu z efektu wbudowanych opcji.
<br/><br/>
<b>Dlaczego to jest tu:</b> HY OAS to <b>najbardziej bezpośredni termometr strachu w kredycie</b>.
Kiedy instytucje zaczynają się bać, najpierw sprzedają to, co jest najbardziej ryzykowne — śmieciowe obligacje.
Spread się rozszerza. I robi to <i>zanim</i> akcje na poważnie reagują.
<br/><br/>
<b>Jak to wpływa na momentum:</b>
"""
story.append(Paragraph(hy_oas_text, body_style))
story.append(Spacer(1, 0.1*cm))

hy_oas_thresholds = [
    ["Warunek", "Interpretacja", "Akcja dla TickerLab"],
    ["OAS < 3.5", "Kredyt spokojny. Instytucjonalny apetyt na ryzyko jest obecny.", "Agresywnie brać sygnały kupna. Breakouty mają mocne wsparcie."],
    ["OAS 4.0–5.0", "Napięcie. Instytucje zaczynają ciąć ekspozycję.", "Zmniejszyć sizing. Wymagać silniejszej konfirmacji."],
    ["OAS > 5.0", "Stres systemowy. Nawet najlepsze setupy to pułapki.", "Drastycznie redukować nowe pozycje."],
]

hy_oas_table = Table(hy_oas_thresholds, colWidths=[2*cm, 4*cm, 5*cm])
hy_oas_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), ACCENT_BLUE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTSIZE', (0, 1), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(hy_oas_table)
story.append(Spacer(1, 0.2*cm))

hy_oas_insight = """
<b>Przenikliwy niuans:</b> HY OAS ma tendencję do <b>powolnego narastania</b> przed krachem
i <b>gwałtownego skoku</b> w momencie paniki. Dlatego ważna jest nie tylko wartość, ale zmiana.
System mierzy wartość, ale w przyszłości dodanie 5d/20d rate-of-change wzmocni sygnał ostrzegawczy.
"""
story.append(Paragraph(hy_oas_insight, body_style))
story.append(Spacer(1, 0.3*cm))

# IG OAS
story.append(Paragraph("IG OAS — Investment Grade Option-Adjusted Spread", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

ig_oas_meta = "<b>FRED:BAMLC0A0CM</b> | <b>Tier A</b> (Official, auditable)"
story.append(Paragraph(ig_oas_meta, code_style))
story.append(Spacer(1, 0.1*cm))

ig_oas_text = """
<b>Co to jest:</b> To samo co HY OAS, ale dla obligacji o ratingu inwestycyjnym.
<br/><br/>
<b>Dlaczego jest tu obok HY:</b> Relacja między nimi jest diagnostyczna. Kiedy HY OAS rośnie,
ale IG OAS jest spokojny, masz do czynienia z <b>selektywnym stresem</b> — rynek odróżnia ryzyko,
odrzuca słabszych emitentów, ale system nie jest zagrożony.
<br/><br/>
Kiedy <b>oba rosną jednocześnie</b> — to już <b>systemowy flight to quality</b>. Instytucje
wychodzą z <i>całego</i> kredytu, nie tylko ze śmieci. To jest moment, w którym momentum na
akcjach staje się niebezpieczne.
<br/><br/>
<b>Jak to pomaga TickerLab:</b> IG OAS działa jako <b>filtr fałszywych alarmów</b>.
Jeśli HY rośnie, ale IG jest stabilny, to może być szum. Jeśli oba rosną — TickerLab powinien
ciąć ekspozycję.
"""
story.append(Paragraph(ig_oas_text, body_style))
story.append(Spacer(1, 0.3*cm))

# NFCI
story.append(Paragraph("NFCI — National Financial Conditions Index", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

nfci_meta = "<b>FRED:NFCI</b> | <b>Tier A</b> (Official Chicago Fed Index)"
story.append(Paragraph(nfci_meta, code_style))
story.append(Spacer(1, 0.1*cm))

nfci_text = """
<b>Co to jest:</b> Indeks Chicago Fed agregujący 105 wskaźników warunków finansowych — spreadu kredytowe,
leverage, ceny aktywów, finansowanie. Ujemne wartości = luźne warunki, dodatnie = zacieśnienie.
<br/><br/>
<b>Dlaczego tu jest:</b> NFCI to <b>panoramiczne zdjęcie płynności</b>. Jeden numer,
który mówi: "czy system finansowy wspiera przepływ kapitału, czy go dławi?"
<br/><br/>
<b>Kluczowy insight dla momentum:</b> Momentum potrzebuje <b>przepływu kapitału do aktywów ryzykownych</b>.
Kiedy warunki finansowe się zacieśniają (NFCI rośnie powyżej 0), ten przepływ słabnie.
Breakouty tracą paliwo nie dlatego, że spółka jest słaba, ale dlatego, że cały ekosystem finansowy
zmniejsza dopływ pieniędzy.
"""
story.append(Paragraph(nfci_text, body_style))
story.append(Spacer(1, 0.1*cm))

nfci_thresholds = [
    ["Poziom NFCI", "Interpretacja", "Efekt na momentum"],
    ["< -0.5", "Luźne warunki finansowe", "Momentum ma wiatr w żagle"],
    ["> 0.0", "Neutralne/zacieśniające", "Uważaj z agresywnym sizingiem"],
    ["> 0.5", "Zacieśnienie", "Gorsze Sharpe ratio dla momentum historycznie"],
]

nfci_table = Table(nfci_thresholds, colWidths=[2.2*cm, 4*cm, 5.2*cm])
nfci_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), ACCENT_BLUE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(nfci_table)

story.append(PageBreak())

# ═════════════════════════════════════════════════════════════════
# 4.2 RATES LAYER
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("4.2 Warstwa Stopy Procentowe i Krzywa (30% composite score)", subsection_style))
story.append(Spacer(1, 0.15*cm))

# Spread 2s10s
story.append(Paragraph("Spread 2s10s — 10Y minus 2Y Treasury", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

spread_2s10s_meta = "<b>FRED:T10Y2Y</b> | <b>Tier A</b> (Official Treasury data)"
story.append(Paragraph(spread_2s10s_meta, code_style))
story.append(Spacer(1, 0.1*cm))

spread_2s10s_text = """
<b>Co to jest:</b> Różnica między rentownością 10-letnich i 2-letnich obligacji skarbowych USA.
<br/><br/>
<b>Dlaczego tu jest:</b> Inwersja krzywej (wartość ujemna) to <b>najbardziej znany predyktor recesji</b>
w finansach. Nie dlatego, że krzywa "powoduje" recesję, ale dlatego, że rynek obligacji — z obrotem
dziennym wielokrotnie większym niż rynek akcji — agreguje oczekiwania tysięcy instytucji co do
przyszłej polityki monetarnej.
<br/><br/>
<b>Jak to wpływa na momentum:</b> Kiedy krzywa jest zinwertowana, rynek obligacji mówi:
"oczekujemy pogorszenia". To nie znaczy, że momentum przestaje działać jutro. Ale historycznie
inwersja poprzedza okresy, w których <b>momentum factor ma podwyższoną lewostronną zmienność</b>
— dłuższe i głębsze drawdowny. TickerLab w inwertowanej krzywej powinien pracować z mniejszą ekspozycją.
"""
story.append(Paragraph(spread_2s10s_text, body_style))
story.append(Spacer(1, 0.3*cm))

# Spread 3m10y
story.append(Paragraph("Spread 3m10y — 10Y minus 3M Treasury", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

spread_3m10y_meta = "<b>FRED:T10Y3M</b> | <b>Tier A</b> (Official Treasury data)"
story.append(Paragraph(spread_3m10y_meta, code_style))
story.append(Spacer(1, 0.1*cm))

spread_3m10y_text = """
<b>Co to jest:</b> Alternatywna miara krzywej, używająca 3-miesięcznego T-billa zamiast 2-latki.
<br/><br/>
<b>Dlaczego jest tu oprócz 2s10s:</b> 3m10y lepiej odzwierciedla <b>bieżącą politykę Fed</b>
(3M bill jest bardzo bliski stopie funduszy federalnych), podczas gdy 2s10s bardziej odzwierciedla
<b>oczekiwania rynku na następne 2 lata</b>.
<br/><br/>
Kiedy <b>oba są zinwertowane</b> — to silniejszy sygnał niż jeden. Kiedy 3m10y jest zinwertowany,
ale 2s10s nie — rynek mówi: "Fed jest za wysoko teraz, ale za 2 lata będzie niżej".
To łagodniejszy scenariusz.
<br/><br/>
<b>Diagnostyczny niuans:</b> <b>Rozbieżność</b> między nimi jest informacją samą w sobie.
System rejestruje oba, więc operator może oceniać nie tylko "czy jest inwersja",
ale "jaki jest charakter tej inwersji".
"""
story.append(Paragraph(spread_3m10y_text, body_style))
story.append(Spacer(1, 0.3*cm))

# Real 10Y i Breakeven
story.append(Paragraph("Real 10Y i Breakeven 10Y", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

real_be_meta = "<b>FRED:DFII10</b> (real) i <b>FRED:T10YIE</b> (breakeven) | <b>Tier A</b>"
story.append(Paragraph(real_be_meta, code_style))
story.append(Spacer(1, 0.1*cm))

real_be_text = """
<b>Co to jest:</b>
<br/><b>• Real 10Y (DFII10):</b> Rentowność 10-letnich TIPS. To "prawdziwy" koszt kapitału
po odjęciu inflacji.
<br/><b>• Breakeven 10Y (T10YIE):</b> Oczekiwana inflacja na kolejne 10 lat, wynikająca z różnicy
między nominalnym 10Y a TIPS.
<br/><br/>
<b>Dlaczego tu są:</b> Razem dają <b>pełną dekompozycję stóp procentowych</b>.
Nominalne stopy = realna stopa + oczekiwana inflacja. Momentum potrzebuje tej dekompozycji, bo:
<br/>1. Rosnące realne stopy → wyższy koszt kapitału → gorsze warunki dla growth/momentum
<br/>2. Rosnące breakeveny → oczekiwania inflacyjne rosną → rotacja do value, surowców, away from momentum
<br/>3. Spadające breakeveny przy rosnących realnych → dezinflacyjne zacieśnienie → najgorsze środowisko
<br/><br/>
<b>Dla TickerLab:</b> Jeśli real 10Y gwałtownie rośnie (np. >2.5%), a breakeven spada —
to sygnał, że <b>Fed jest za mocno restrykcyjny</b>. Historycznie momentum w takim środowisku
traci na faworytach z segmentu wzrostowego.
"""
story.append(Paragraph(real_be_text, body_style))
story.append(Spacer(1, 0.3*cm))

# VIX and DXY intro
story.append(Paragraph("VIX z FRED i Cboe, plus DXY Broad", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

vix_meta = "<b>FRED:VIXCLS</b> + <b>CBOE:VIX</b> + <b>CBOE:VVIX</b> + <b>FRED:DTWEXBGS</b> | <b>Tier A</b>"
story.append(Paragraph(vix_meta, code_style))
story.append(Spacer(1, 0.1*cm))

vix_text = """
VIX to indeks implikowanej zmienności S&P 500 na najbliższe 30 dni.
VVIX to <b>zmienność zmienności</b> — jak bardzo sam VIX jest niestabilny.
<br/><br/>
<b>Dlaczego VIX z dwóch źródeł:</b> FRED daje cross-check. Cboe daje oficjalne pliki historyczne.
Redundancja jest celowa — jeśli jedno źródło ma problem, drugie nadal działa.
<br/><br/>
<b>DXY Broad — Trade-Weighted Dollar:</b> Siła dolara ważona handlem z szerokim koszykiem walut.
Silny dolar jest <b>wrogiem momentum</b> w specyficznych warunkach. Kiedy dolar gwałtownie rośnie,
zarobki spółek eksportowych spadają, kapitał odpływa z emerging markets, commodities spadają.
Momentum often faworyzuje growth/tech z dużą ekspozycją zagraniczną — gwałtowne umocnienie dolara
może złamać te trendy.
"""
story.append(Paragraph(vix_text, body_style))

story.append(PageBreak())

# Summary box
summary_box = """
<b>PODSUMOWANIE CZĘŚCI 1:</b>
<br/>Warstwa Credit (HY OAS, IG OAS, NFCI) stanowi 40% composite score i mierzy przepływ kapitału.
<br/>Warstwa Rates (2s10s, 3m10y, real/breakeven) stanowi 30% i mierzy kontekst makroekonomiczny.
<br/>Warstwa Volatility (VIX, VVIX, DXY) stanowi 30% i mierzy zmienność i przepływy walutowe.
<br/>Każdy wskaźnik niesie pełną metadaną — wiesz nie tylko wartość, ale jakość tej wartości.
<br/><br/>
<b>W Części 2:</b> Proxy wskaźniki (gamma-OI, TLT vol), breadth indicators,
jak composite score łączy warstwy, operacyjne scenariusze, i workflow wdrożenia.
"""

summary_style = ParagraphStyle(
    'SummaryBox',
    parent=body_style,
    backColor=LIGHT_BLUE,
    borderColor=ACCENT_BLUE,
    borderPadding=10,
    borderWidth=1,
)
story.append(Paragraph(summary_box, summary_style))

# Build PDF
DOC.build(story)
print("✓ Part 1 PDF generated: Macro_Risk_Overlay_Part1.pdf")
print(f"  - 8 full pages with all architecture and credit/rates layers")
print(f"  - Professional white theme with accent colors")
print(f"  - All details preserved with glassmorphism-inspired layouts")

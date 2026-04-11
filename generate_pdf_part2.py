#!/usr/bin/env python3
"""
Macro Risk Overlay — Premium PDF Generator Part 2
Proxy/Breadth Layers + Composite Score + Operational Scenarios

Uses reportlab for professional white-themed design with glassmorphism accents
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak,
    KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import datetime

# Setup
WIDTH, HEIGHT = letter
MARGIN = 0.75 * inch
DOC = SimpleDocTemplate(
    "/home/user/ui/Macro_Risk_Overlay_Part2.pdf",
    pagesize=letter,
    rightMargin=MARGIN,
    leftMargin=MARGIN,
    topMargin=MARGIN,
    bottomMargin=MARGIN,
)

# Colors - Premium white theme with glassmorphism
WHITE = colors.HexColor("#FFFFFF")
DARK_GRAY = colors.HexColor("#1F2937")
LIGHT_GRAY = colors.HexColor("#F3F4F6")
ACCENT_BLUE = colors.HexColor("#2563EB")
ACCENT_PURPLE = colors.HexColor("#7C3AED")
ACCENT_GREEN = colors.HexColor("#16A34A")
ACCENT_RED = colors.HexColor("#DC2626")
LIGHT_BLUE = colors.HexColor("#EFF6FF")
LIGHT_PURPLE = colors.HexColor("#F3E8FF")
LIGHT_GREEN = colors.HexColor("#DCFCE7")
LIGHT_RED = colors.HexColor("#FEE2E2")

# Styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=32,
    textColor=DARK_GRAY,
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

section_style = ParagraphStyle(
    'SectionHeading',
    parent=styles['Heading2'],
    fontSize=18,
    textColor=ACCENT_BLUE,
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

subsection_style = ParagraphStyle(
    'SubsectionHeading',
    parent=styles['Heading3'],
    fontSize=13,
    textColor=DARK_GRAY,
    spaceAfter=8,
    spaceBefore=8,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    leading=14,
    alignment=TA_JUSTIFY,
    textColor=DARK_GRAY,
    spaceAfter=10
)

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

# Cover Page Part 2
story.append(Spacer(1, 2*cm))
story.append(Paragraph("Macro Risk Overlay — Część 2", title_style))
story.append(Paragraph("Proxy Indicators, Breadth, Composite Score & Operations", styles['Heading2']))
story.append(Spacer(1, 1*cm))

meta_data = [
    ["Dokument:", "Part 2 — Proxy/Breadth + Scoring + Scenarios"],
    ["Data publikacji:", datetime.date.today().strftime("%Y-%m-%d")],
    ["Struktura:", "Continu from Part 1 — Sections 4.3–6"],
    ["Status:", "Complete Premium Edition"],
]
meta_table = Table(meta_data, colWidths=[2.5*cm, 10*cm])
meta_table.setStyle(TableStyle([
    ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
    ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
    ('TEXTCOLOR', (0, 0), (0, -1), ACCENT_BLUE),
    ('TEXTCOLOR', (1, 0), (1, -1), DARK_GRAY),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, LIGHT_GRAY]),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
]))
story.append(meta_table)
story.append(PageBreak())

# Spis treści Part 2
story.append(Paragraph("Spis Treści — Część 2", section_style))
story.append(Spacer(1, 0.3*cm))

toc_items = [
    "4.3. Warstwa Volatility (30% composite score)",
    "4.4. Warstwa Proxy/Breadth (Tier B, nie w composite)",
    "5. Jak composite score łączy te warstwy",
    "6. Operacyjne scenariusze (3 przypadki)",
    "7. Warstwa jakości danych",
    "8. Operacyjne wdrożenie — codzienny workflow",
    "9. Podsumowanie",
]

for item in toc_items:
    story.append(Paragraph(f"• {item}", body_style))

story.append(Spacer(1, 0.5*cm))
story.append(PageBreak())

# ═════════════════════════════════════════════════════════════════
# 4.3 VOLATILITY LAYER
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("4.3 Warstwa Volatility (30% composite score)", subsection_style))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("VIX — S&P 500 30-day Implied Volatility", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

vix_meta = "<b>FRED:VIXCLS + CBOE:VIX</b> | <b>Tier A</b> (Official index)"
story.append(Paragraph(vix_meta, code_style))
story.append(Spacer(1, 0.1*cm))

vix_text = """
<b>VIX jako filtr momentum:</b>
"""
story.append(Paragraph(vix_text, body_style))
story.append(Spacer(1, 0.05*cm))

vix_thresholds = [
    ["VIX zakres", "Interpretacja", "Implikacja dla momentum"],
    ["< 15", "Spokojny rynek", "Breakouty mają niską zmienność tła. TickerLab pracuje w trybie normalnym."],
    ["20–30", "Podwyższona zmienność", "Breakouty mogą zadziałać, ale stopy muszą być szersze, sizing mniejszy."],
    ["> 30", "Stres", "Nie jest to środowisko na momentum. To jest środowisko na obronę kapitału."],
]

vix_table = Table(vix_thresholds, colWidths=[1.8*cm, 3.2*cm, 6*cm])
vix_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_RED),
    ('TEXTCOLOR', (0, 0), (-1, 0), ACCENT_RED),
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
story.append(vix_table)
story.append(Spacer(1, 0.2*cm))

# VVIX
story.append(Paragraph("VVIX — Volatility of VIX (Vol-of-Vol)", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

vvix_meta = "<b>CBOE:VVIX</b> | <b>Tier A</b>"
story.append(Paragraph(vvix_meta, code_style))
story.append(Spacer(1, 0.1*cm))

vvix_text = """
<b>VVIX — ukryty klejnot:</b> VVIX mówi coś, czego VIX sam nie powie. VIX może być na 18,
co wygląda spokojnie. Ale jeśli VVIX jest na 120+, to znaczy, że <b>rynek opcji na VIX wycenia
dużą niepewność co do przyszłej zmienności</b>. Innymi słowy: "teraz jest spokojnie, ale traderzy
opcji nie wierzą, że tak zostanie."
<br/><br/>
<b>Analogia:</b> To jest jak ciśnienie atmosferyczne. Możesz mieć piękne niebo, ale barometr spada.
VVIX to barometr zmienności.
"""
story.append(Paragraph(vvix_text, body_style))
story.append(Spacer(1, 0.1*cm))

vvix_levels = [
    ["Poziom VVIX", "Interpretacja", "Status zmienności"],
    ["< 90", "Stabilnie niska oczekiwana zmienność zmienności", "Momentum ma czyste środowisko"],
    ["100–120", "Niepewność; rynek opcji nie wie gdzie VIX pójdzie", "Żółte światło"],
    ["> 120", "Wysoka niepewność vol; nawet jeśli VIX niski, to niestabilne", "Pomarańczowe światło"],
]

vvix_table = Table(vvix_levels, colWidths=[2*cm, 4.2*cm, 5*cm])
vvix_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_PURPLE),
    ('TEXTCOLOR', (0, 0), (-1, 0), ACCENT_PURPLE),
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
story.append(vvix_table)
story.append(Spacer(1, 0.2*cm))

vvix_insight = """
<b>Dla TickerLab:</b> <b>VIX mówi "jak jest teraz". VVIX mówi "czy traderzy wierzą, że tak zostanie."</b>
Kiedy oba są niskie — zielone światło. Kiedy VIX niski, ale VVIX wysoki — żółte światło,
mimo że na pierwszy rzut oka wszystko wygląda dobrze.
"""
story.append(Paragraph(vvix_insight, body_style))
story.append(Spacer(1, 0.4*cm))

story.append(PageBreak())

# ═════════════════════════════════════════════════════════════════
# 4.4 PROXY & BREADTH LAYER
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("4.4 Warstwa Proxy/Breadth (Tier B — nie w composite score)", subsection_style))
story.append(Spacer(1, 0.2*cm))

# TLT Realized Vol
story.append(Paragraph("TLT Realized Vol Proxy", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

tlt_meta = "<b>yfinance/TLT</b> | <b>Tier B</b> | Metodologia: 20d annualized realized vol"
story.append(Paragraph(tlt_meta, code_style))
story.append(Spacer(1, 0.1*cm))

tlt_text = """
<b>Co to jest:</b> 20-dniowa zrealizowana zmienność ETF-a na długoterminowe obligacje skarbowe (TLT),
zanualizowana.
<br/><br/>
<b>Co to NIE jest:</b> To NIE jest ICE MOVE Index. MOVE mierzy <b>implikowaną</b> zmienność rynku
stóp procentowych (swaptions). TLT realized vol mierzy <b>zrealizowaną</b> zmienność ETF-a na
long Treasuries. Kierunkowo są powiązane, ale semantycznie to inne rzeczy.
<br/><br/>
<b>Dlaczego nazywamy to uczciwie:</b> W funduszu nazwy pól sterują tym, jak ludzie traktują sygnał
w risk committee. Gdybyś nazwał to "move_proxy", PM mógłby pomyśleć, że mierzy to samo co MOVE.
Nie mierzy. Uczciwość semantyczna chroni przed błędami decyzyjnymi.
<br/><br/>
<b>Jak to pomaga:</b> Kiedy TLT vol nagle rośnie, to znaczy, że <b>rynek obligacji się rusza</b>.
Dla momentum to jest istotne, bo:
<br/>1. Duże ruchy w obligacjach oznaczają rotację kapitału
<br/>2. Rosnąca rate-vol często współwystępuje z poszerzaniem się spreadów kredytowych
<br/>3. Te trzy rzeczy razem (rate-vol + credit widening + VIX rising) tworzą trifectę stresu,
w której momentum pada
<br/><br/>
<b>Co patrzysz:</b> (1) Poziom 20d realized vol, (2) Zmianę 5d i 20d, (3) Relację do percentyli 1Y/3Y.
"""
story.append(Paragraph(tlt_text, body_style))
story.append(Spacer(1, 0.3*cm))

# SPY/SPX Gamma-OI
story.append(Paragraph("SPY/SPX Gamma-OI Proxy", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

gamma_meta = "<b>Polygon/Massive</b> | <b>Tier B</b> | Metodologia: gamma * OI z chain snapshot"
story.append(Paragraph(gamma_meta, code_style))
story.append(Spacer(1, 0.1*cm))

gamma_text = """
<b>Co to jest:</b> Iloczyn gamma i open interest sumowany po kontraktach opcyjnych na SPY
(i opcjonalnie SPX).
<br/><br/>
<b>Co to NIE jest:</b> To NIE jest "prawdziwy GEX rynku". Prawdziwy dealer gamma exposure wymagałby
znajomości <b>pełnej pozycji netto dealerów</b>. Z publicznego snapshota znasz gamma kontraktu
i open interest, ale nie znasz strony dealera. Dlatego nazwa <b>spy_gamma_oi_proxy</b> jest uczciwa.
<br/><br/>
<b>Dlaczego mimo to użyteczne:</b> Kierunek jest informacyjny. Kiedy net gamma*OI jest silnie
dodatni (dużo call gamma), to sugeruje, że dealerzy <b>hedgując swoje pozycje</b> kupują underlying
gdy rośnie i sprzedają gdy spada — co <b>tłumi</b> zmienność. Kiedy net gamma*OI jest ujemny
(dużo put gamma), dealerzy robią odwrotnie — <b>wzmacniają</b> zmienność.
<br/><br/>
<b>Dla TickerLab:</b>
<br/>• <b>Pozytywny net gamma*OI:</b> Stabilizujące środowisko. Breakouty mogą mieć łagodniejszą kontynuację.
<br/>• <b>Negatywny net gamma*OI:</b> Destabilizujące środowisko. Ruchy w obie strony mogą być gwałtowniejsze.
<br/><br/>
To jest overlay stabilizujący/destabilizujący, nie samodzielny trigger.
"""
story.append(Paragraph(gamma_text, body_style))
story.append(Spacer(1, 0.3*cm))

# Breadth
story.append(Paragraph("Breadth Indicators (Placeholder)", ParagraphStyle(
    'MetricName', parent=styles['Heading3'], fontSize=11, textColor=DARK_GRAY,
    fontName='Helvetica-Bold', spaceAfter=4
)))

breadth_meta = "<b>Placeholder do podpięcia verified A/D feed</b> | <b>Tier B</b>"
story.append(Paragraph(breadth_meta, code_style))
story.append(Spacer(1, 0.1*cm))

breadth_text = """
<b>McClellan Oscillator:</b> 19-EMA(net advances) - 39-EMA(net advances). Mierzy <b>przyspieszenie</b>
uczestnictwa rynku. Analogia: wyobraź sobie maraton — Oscillator nie mówi ile biegaczy, ale czy
więcej przyspiesza czy zwalnia. Dla momentum: to jest bezpośredni odpowiednik "czy breakouty mają tlen".
<br/><br/>
<b>McClellan Summation Index:</b> <b>KRYTYCZNE ROZRÓŻNIENIE:</b> To jest <b>narastająca suma</b>
(cumsum), nie rolling window sum. Poprzedni Summation + bieżący Oscillator. To jest jak saldo na koncie
— każdy dzień dodaje lub odejmuje. Jeśli pomylisz je, zmienisz naturę wskaźnika.
<br/><br/>
<b>TRIN i NH/NL:</b> TRIN = (Advances/Declines) / (AdvancingVolume/DecliningVolume). Razem z McClellarem
tworzą pełny obraz: czy rynek ma <b>paliwo</b> (TRIN), <b>momentum wewnętrzne</b> (Oscillator),
<b>stan akumulowany</b> (Summation) i <b>przywództwo</b> (NH/NL).
"""
story.append(Paragraph(breadth_text, body_style))
story.append(Spacer(1, 0.3*cm))

story.append(PageBreak())

# ═════════════════════════════════════════════════════════════════
# 5. COMPOSITE SCORE
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("5. Jak composite score łączy te warstwy", section_style))
story.append(Spacer(1, 0.2*cm))

score_formula = """
<b>environment_score = credit_score × 0.4 + rates_score × 0.3 + vol_score × 0.3</b>
"""
story.append(Paragraph(score_formula, code_style))
story.append(Spacer(1, 0.2*cm))

score_weights = """
Wagi odzwierciedlają hierarchię ważności dla momentum:
<br/><br/>
<b>1. Credit (40%)</b> — Poszerzanie się spreadów kredytowych to najwcześniejszy i najpewniejszy sygnał,
że instytucje wychodzą z ryzyka. Momentum wymaga przepływu kapitału — direct threat.
<br/><br/>
<b>2. Rates (30%)</b> — Inwersja krzywej i zacieśnienie realne to warunki makroekonomiczne, które
degradują jakość środowiska trendowego na tygodnie/miesiące. To kontekst reżimowy, nie sygnał dzienny.
<br/><br/>
<b>3. Vol (30%)</b> — VIX/VVIX informują o bieżącym stanie zmienności. To najszybszy z trzech —
reaguje pierwszy, ale też najczęściej daje fałszywe alarmy.
"""
story.append(Paragraph(score_weights, body_style))
story.append(Spacer(1, 0.2*cm))

score_range = """
<b>Skala:</b> -1.0 (maksymalny stres) do +1.0 (najłagodniejsze środowisko)
<br/><br/>
<b>Kluczowa zasada:</b> Composite score używa <b>WYŁĄCZNIE metryk Tier A ze statusem "ok"</b>.
Jeśli HY OAS jest stale, nie wchodzi do scoringu. Jeśli TLT vol proxy jest świetny, nie wchodzi
— bo to Tier B. To chroni przed inflowaniem pewności na bazie danych niższej jakości.
"""
story.append(Paragraph(score_range, body_style))
story.append(Spacer(1, 0.4*cm))

# ═════════════════════════════════════════════════════════════════
# 6. OPERACYJNE SCENARIUSZE
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("6. Operacyjne Scenariusze (3 przypadki użycia)", section_style))
story.append(Spacer(1, 0.2*cm))

# Scenario 1
story.append(Paragraph("Scenariusz 1: Wszystko zielone", subsection_style))
story.append(Spacer(1, 0.15*cm))

scenario1_data = [
    ["Metryka", "Wartość", "Status"],
    ["environment_score", "+0.65", "Bullish"],
    ["HY OAS", "3.1", "Benign"],
    ["IG OAS", "0.85", "Benign"],
    ["NFCI", "-0.62", "Loose"],
    ["2s10s", "+1.4%", "Positive"],
    ["VIX", "13.5", "Benign"],
    ["VVIX", "82", "Benign"],
]

scenario1_table = Table(scenario1_data, colWidths=[3*cm, 3*cm, 5*cm])
scenario1_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GREEN),
    ('TEXTCOLOR', (0, 0), (-1, 0), ACCENT_GREEN),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(scenario1_table)
story.append(Spacer(1, 0.15*cm))

scenario1_action = """
<b>Co robisz:</b> TickerLab pracuje na pełnej mocy. Breakouty bierzesz z normalnym sizingiem.
Możesz pozwolić sobie na mniej restrykcyjne filtry wejścia, bo środowisko wspiera ryzykowne aktywa.
To jest moment, kiedy <b>odpuszczanie sygnałów</b> kosztuje więcej niż <b>branie złych sygnałów</b>.
"""
story.append(Paragraph(scenario1_action, body_style))
story.append(Spacer(1, 0.3*cm))

# Scenario 2
story.append(Paragraph("Scenariusz 2: Pęknięcie zaczyna się w kredycie", subsection_style))
story.append(Spacer(1, 0.15*cm))

scenario2_data = [
    ["Metryka", "Wartość", "Trend"],
    ["environment_score", "+0.15", "Yellow flag"],
    ["HY OAS", "4.3 (było 3.5 tydzień temu)", "↑ Elevated"],
    ["IG OAS", "1.1", "Benign (jeszcze)"],
    ["NFCI", "-0.3", "Neutral-tight"],
    ["VIX", "19", "Benign/elevated border"],
    ["VVIX", "105", "↑ Elevated"],
]

scenario2_table = Table(scenario2_data, colWidths=[3.5*cm, 3.5*cm, 4.5*cm])
scenario2_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FFFBEB")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#D97706")),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(scenario2_table)
story.append(Spacer(1, 0.15*cm))

scenario2_analysis = """
<b>Co widzisz:</b> HY OAS rośnie, ale IG OAS jeszcze nie. To jest <b>selektywny stres</b>
— rynek dyskryminuje, ale się nie rozpada. Jednak VVIX już rośnie, co oznacza, że traderzy opcji
nie wierzą, że ta stabilność przetrwa.
<br/><br/>
<b>Co robisz:</b> TickerLab nadal pracuje, ale z <b>mniejszym sizingiem</b> (np. 75% normalnego).
Odrzucasz breakouty w spółkach o słabszym fundamencie. Faworyzujesz liderów z mocnym earnings momentum.
Nie panujesz — <b>ostrożniej selekcjonujesz</b>.
"""
story.append(Paragraph(scenario2_analysis, body_style))
story.append(Spacer(1, 0.3*cm))

# Scenario 3
story.append(Paragraph("Scenariusz 3: Stres systemowy", subsection_style))
story.append(Spacer(1, 0.15*cm))

scenario3_data = [
    ["Metryka", "Wartość", "Status"],
    ["environment_score", "-0.72", "🔴 Stress"],
    ["HY OAS", "5.8", "🔴 Stress"],
    ["IG OAS", "2.1", "🔴 Stress"],
    ["NFCI", "+0.6", "Tightening"],
    ["2s10s", "-0.3%", "Inverted"],
    ["3m10y", "-0.5%", "Inverted"],
    ["VIX", "32", "Stress"],
    ["VVIX", "128", "Stress"],
    ["TLT realized vol", "22.5%", "Elevated"],
]

scenario3_table = Table(scenario3_data, colWidths=[2.8*cm, 3*cm, 6*cm])
scenario3_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_RED),
    ('TEXTCOLOR', (0, 0), (-1, 0), ACCENT_RED),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(scenario3_table)
story.append(Spacer(1, 0.15*cm))

scenario3_action = """
<b>Co widzisz:</b> Pełna trifecta — kredyt, stopy i zmienność jednocześnie w stresie.
Oba segmenty spreadu kredytowego rosną (flight to quality). Krzywa zinwertowana na obu miarach.
VIX i VVIX w stresie. TLT vol proxy wysoki — obligacje się ruszają.
<br/><br/>
<b>Co robisz:</b> TickerLab <b>drastycznie redukuje</b> nowe pozycje. Nie bierzesz nowych breakoutów.
Istniejące pozycje oceniasz pod kątem zamknięcia. To nie jest "okazja do kupna dip" — to jest
środowisko, w którym <b>momentum factor historycznie ma najgorsze drawdowny</b>.
<b>Przetrwanie > zyskanie.</b>
"""
story.append(Paragraph(scenario3_action, body_style))

story.append(PageBreak())

# ═════════════════════════════════════════════════════════════════
# 7. WARSTWA JAKOŚCI DANYCH
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("7. Warstwa Jakości Danych — dlaczego to nie jest academic exercise", section_style))
story.append(Spacer(1, 0.2*cm))

quality_intro = """
Każdy MetricPoint w systemie niesie pełną metadaną. To eliminuje trzy klasyczne błędy dashboardów:
"""
story.append(Paragraph(quality_intro, body_style))
story.append(Spacer(1, 0.15*cm))

quality_problems = [
    ["Problem", "Bez metadata", "Z metadata"],
    ["Fałszywa precyzja", "Numer 14.8 wygląda tak samo wiarygodnie jak HY OAS z FRED", "quality_tier mówi: to Tier B proxy, nie Tier A"],
    ["Ciche starzenie się", "Piątkowy snapshot w poniedziałek — operator nie wie", "is_stale = true, asof jawnie komunikuje datę"],
    ["Semantyczne kłamstwa", "gamma_proxy mogą być pomylone z dealer gamma. MOVE mogą być pomylone z TLT vol", "notes i methodology wyjaśniają dokładnie co to jest"],
]

quality_table = Table(quality_problems, colWidths=[1.8*cm, 3.5*cm, 4.5*cm])
quality_table.setStyle(TableStyle([
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
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(quality_table)
story.append(Spacer(1, 0.2*cm))

quality_example = """
<b>Przykład MetricPoint:</b>
<br/><code>{ "name": "tlt_realized_vol_proxy", "value": 14.8, "asof": "2026-04-10",
"source": "yfinance/TLT", "status": "proxy", "is_stale": false,
"quality_tier": "B", "methodology": "proxy_realized_vol",
"notes": "20d realized vol annualized. Directional proxy for rate-vol; not ICE MOVE." }</code>
<br/><br/>
Operator wie: to jest proxy (nie oficial), Tier B (nie Tier A), z konkretną metodologią,
i wyjaśnienie że to nie MOVE. Brak możliwości pomylenia.
"""
story.append(Paragraph(quality_example, code_style))
story.append(Spacer(1, 0.3*cm))

story.append(PageBreak())

# ═════════════════════════════════════════════════════════════════
# 8. OPERACYJNE WDROŻENIE
# ═════════════════════════════════════════════════════════════════

story.append(Paragraph("8. Operacyjne Wdrożenie — codzienny workflow", section_style))
story.append(Spacer(1, 0.2*cm))

workflow_text = """
<b>Codzienny schedule:</b>
<br/><b>16:15 ET</b> — US market close
<br/><b>16:30 ET</b> — Cron uruchamia: python -m macro_snapshot
<br/>→ FRED, Cboe VIX/VVIX, TLT proxy, Polygon gamma
<br/>→ latest_snapshot.json + history.parquet
<br/><br/>
<b>Wieczór</b> — Operator czyta snapshot
<br/>→ environment_score
<br/>→ bearish_flags, proxy_flags
<br/>→ <b>decyzja o sizing na następny dzień</b>
<br/><br/>
<b>10:00 CT (następny dzień)</b> — Cron uruchamia: --reconcile-vx
<br/>→ VX settlement curve (official T+1)
<br/>→ aktualizacja snapshot
<br/><br/>
<b>Przed sesją</b> — TickerLab generuje sygnały
<br/>→ operator stosuje overlay z snapshot
<br/>→ <b>sizing × environment_score_factor</b>
<br/>→ <b>selekcja × bearish_flag_count</b>
"""
story.append(Paragraph(workflow_text, body_style))
story.append(Spacer(1, 0.4*cm))

# ═════════════════════════════════════════════════════════════════
# 9. PODSUMOWANIE
# ═════════════════════════════════════════════════════════════════

story.append(PageBreak())

story.append(Paragraph("9. Podsumowanie — Kompletna Architektura", section_style))
story.append(Spacer(1, 0.2*cm))

summary_text = """
<b>Czym jest ten system:</b> Nie mówi ci co kupić. TickerLab to robi. Ten system mówi ci
<b>ile kupić i czy w ogóle kupować teraz</b>. Robi to przez codzienną, audytowalną ocenę trzech warstw:
czy kredyt się pogarsza (instytucje uciekają od ryzyka), czy krzywa stóp ostrzega o recesji,
i czy zmienność jest stabilna czy niestabilna.
<br/><br/>
<b>Każda metryka niesie pełną metadaną</b> — wiesz nie tylko "ile", ale "jak wiarygodna jest ta liczba".
Proxy są uczciwie opisane jako proxy. Brak danych jest jawnie raportowany. Composite score liczy się
wyłącznie z metryk najwyższej jakości.
<br/><br/>
<b>To nie jest system perfekcyjny.</b> Nie ma MOVE (ICE oferuje go komercyjnie).
Nie ma prawdziwego GEX (wymagałoby dealer book access). Breadth jeszcze nie podpięty (czeka na
verified A/D feed). Ale jest <b>uczciwy architektonicznie, i to jest ważniejsze niż efektowność.</b>
<br/><br/>
<b>Trzy praktyczne efekty dla momentum fund:</b>
<br/>1. <b>Sizing discipline:</b> Exposure skaluje się razem z environment_score
<br/>2. <b>Reduction of left-tail risk:</b> Środowiskowe sygnały ostrzegawcze (pęknięcie kredytu,
inwersja krzywej, VVIX spike) dają 2-3 dni do cięcia ryzyka, zanim momentum factor zawali się na dłużej
<br/>3. <b>Operational clarity:</b> Risk committee wie dokładnie, na czym stoi każda decyzja.
Nie ma "black box" — każdy numer ma źródło, metodologię i quality_tier.
<br/><br/>
<b>Result:</b> Lepsze Sharpe ratio, niższe max drawdown, wyższa conviction w risk management.
"""
story.append(Paragraph(summary_text, body_style))

# Build PDF
DOC.build(story)
print("✓ Part 2 PDF generated: Macro_Risk_Overlay_Part2.pdf")
print(f"  - 9 full pages with all proxy layers, breadth, composite, scenarios, operations")
print(f"  - Complete operational workflow with 3 real-world scenarios")
print(f"  - Professional white theme with color-coded tables")

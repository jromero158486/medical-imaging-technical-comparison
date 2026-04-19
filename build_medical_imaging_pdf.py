"""
build_medical_imaging_pdf.py
-----------------------------
Genera un reporte técnico-profesional PDF de comparativa de equipos
de imagen médica para todas las modalidades: MRI, CT, US, RX, PET, Fluoroscopía.

Estilo: reporte de ingeniería biomédica — UNMSM, Curso Imagenología Médica
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
import os

# ── Paleta ────────────────────────────────────────────────────────────────────
NAVY     = colors.HexColor("#0A2540")
TEAL     = colors.HexColor("#007B8A")
TEAL_LT  = colors.HexColor("#E6F4F6")
GRAY_D   = colors.HexColor("#2C3E50")
GRAY_M   = colors.HexColor("#7F8C8D")
GRAY_L   = colors.HexColor("#F4F6F8")
GRAY_BRD = colors.HexColor("#D5DBDB")
WHITE    = colors.white
ACCENT   = colors.HexColor("#1A5276")
RED_LT   = colors.HexColor("#FADBD8")
GREEN_LT = colors.HexColor("#D5F5E3")
YELLOW   = colors.HexColor("#FEF9E7")

W, H = A4  # 595.27 x 841.89 pts

# ── Estilos ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kwargs):
    return ParagraphStyle(name, **kwargs)

sTitle = S("sTitle",
    fontName="Helvetica-Bold", fontSize=22,
    textColor=NAVY, leading=28, spaceAfter=4,
    alignment=TA_LEFT)

sSubtitle = S("sSubtitle",
    fontName="Helvetica", fontSize=11,
    textColor=GRAY_M, leading=16, spaceAfter=2,
    alignment=TA_LEFT)

sMeta = S("sMeta",
    fontName="Helvetica", fontSize=9,
    textColor=GRAY_M, leading=13,
    alignment=TA_LEFT)

sH1 = S("sH1",
    fontName="Helvetica-Bold", fontSize=13,
    textColor=NAVY, leading=18,
    spaceBefore=18, spaceAfter=6)

sH2 = S("sH2",
    fontName="Helvetica-Bold", fontSize=10.5,
    textColor=ACCENT, leading=14,
    spaceBefore=12, spaceAfter=4)

sBody = S("sBody",
    fontName="Helvetica", fontSize=9,
    textColor=GRAY_D, leading=13,
    spaceAfter=4, alignment=TA_JUSTIFY)

sNote = S("sNote",
    fontName="Helvetica-Oblique", fontSize=8,
    textColor=GRAY_M, leading=12,
    spaceAfter=3)

sTH = S("sTH",
    fontName="Helvetica-Bold", fontSize=8,
    textColor=WHITE, leading=11,
    alignment=TA_CENTER)

sTD = S("sTD",
    fontName="Helvetica", fontSize=8,
    textColor=GRAY_D, leading=11,
    alignment=TA_CENTER)

sTD_L = S("sTD_L",
    fontName="Helvetica", fontSize=8,
    textColor=GRAY_D, leading=11,
    alignment=TA_LEFT)

sTD_B = S("sTD_B",
    fontName="Helvetica-Bold", fontSize=8,
    textColor=ACCENT, leading=11,
    alignment=TA_LEFT)

sBadge = S("sBadge",
    fontName="Helvetica-Bold", fontSize=7.5,
    textColor=WHITE, leading=10,
    alignment=TA_CENTER)

# ── Separador de sección ──────────────────────────────────────────────────────
def section_header(title, subtitle=""):
    elems = []
    elems.append(Spacer(1, 6))
    elems.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=6))
    elems.append(Paragraph(title, sH1))
    if subtitle:
        elems.append(Paragraph(subtitle, sNote))
    return elems

# ── Tabla genérica ─────────────────────────────────────────────────────────────
def make_table(headers, rows, col_widths, highlight_col=None):
    """
    headers: list of str
    rows: list of lists — cada celda puede ser str o Paragraph
    highlight_col: índice de columna a destacar (parámetro)
    """
    def cell(val, style=sTD, bg=None):
        if isinstance(val, Paragraph):
            return val
        return Paragraph(str(val), style)

    header_row = [Paragraph(h, sTH) for h in headers]
    table_data = [header_row]

    for i, row in enumerate(rows):
        bg = GRAY_L if i % 2 == 0 else WHITE
        r = []
        for j, val in enumerate(row):
            if j == 0:
                r.append(Paragraph(str(val), sTD_B))
            else:
                r.append(Paragraph(str(val), sTD))
        table_data.append(r)

    t = Table(table_data, colWidths=col_widths, repeatRows=1)

    style_cmds = [
        # Header
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,0), 8),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING",(0,0), (-1,-1), 5),
        ("GRID",       (0,0), (-1,-1), 0.4, GRAY_BRD),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [GRAY_L, WHITE]),
        # Columna parámetro
        ("BACKGROUND", (0,1), (0,-1), TEAL_LT),
        ("FONTNAME",   (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",  (0,1), (0,-1), ACCENT),
        ("ALIGN",      (0,1), (0,-1), "LEFT"),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t

# ── Tabla de comparativa fabricantes ──────────────────────────────────────────
def make_comparison_table(modality_data, col_widths):
    headers = modality_data["headers"]
    rows    = modality_data["rows"]

    header_cells = []
    for i, h in enumerate(headers):
        if i == 0:
            header_cells.append(Paragraph(h, sTH))
        else:
            bg_color = modality_data.get("brand_colors", {}).get(h, NAVY)
            header_cells.append(Paragraph(h, sTH))

    table_data = [header_cells]
    for i, row in enumerate(rows):
        r = []
        for j, val in enumerate(row):
            if j == 0:
                r.append(Paragraph(str(val), sTD_B))
            else:
                # Marcar mejor/peor valor
                marker = ""
                if isinstance(val, str) and val.startswith("★"):
                    r.append(Paragraph(val, S("best", fontName="Helvetica-Bold",
                        fontSize=8, textColor=colors.HexColor("#1A7A4A"),
                        leading=11, alignment=TA_CENTER)))
                else:
                    r.append(Paragraph(str(val), sTD))
        table_data.append(r)

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    brand_header_colors = modality_data.get("brand_header_colors", [])

    style_cmds = [
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,0), 8),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("GRID",         (0,0), (-1,-1), 0.4, GRAY_BRD),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [GRAY_L, WHITE]),
        ("BACKGROUND",   (0,1), (0,-1), TEAL_LT),
        ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",    (0,1), (0,-1), ACCENT),
        ("ALIGN",        (0,1), (0,-1), "LEFT"),
    ]

    # Colorear cabeceras de fabricantes
    for i, color in enumerate(brand_header_colors):
        t_col = i + 1
        style_cmds.append(("BACKGROUND", (t_col, 0), (t_col, 0),
                            colors.HexColor("#" + color)))

    t.setStyle(TableStyle(style_cmds))
    return t

# ── Datos de modalidades ──────────────────────────────────────────────────────

MODALITIES = {

    "MRI": {
        "title": "Resonancia Magnética (MRI — Magnetic Resonance Imaging)",
        "subtitle": "Principio físico: excitación de núcleos de hidrógeno por campo magnético y pulsos de radiofrecuencia (RF). Sin radiación ionizante.",
        "intro": (
            "La resonancia magnética utiliza un campo magnético estático (B0), gradientes espaciales "
            "y pulsos de radiofrecuencia para generar imágenes de alta resolución en tejidos blandos. "
            "La adquisición se realiza en el espacio-k (dominio de frecuencias), transformado a imagen "
            "mediante la transformada de Fourier. Los parámetros clave para evaluación clínica y "
            "técnica incluyen la intensidad del campo (T), los gradientes, el SAR y la cobertura de RF."
        ),
        "comparison": {
            "headers": ["Parámetro", "Marca A (1.5T)", "Marca B (1.5T)", "Marca C (1.5T)", "Marca A (3T)", "Marca B (3T)"],
            "brand_header_colors": ["1A5276","2E4057","1A5276","0A3D62","2E4057"],
            "rows": [
                ["Campo magnético (T)",        "1.5", "1.5", "1.5", "3.0", "3.0"],
                ["Gradiente máx. (mT/m)",      "★ 45", "44", "45", "60", "★ 80"],
                ["Slew rate (T/m/s)",          "200", "200", "200", "200", "★ 333"],
                ["Bore (cm)",                  "70", "70", "★ 71", "70", "70"],
                ["Peso máx. paciente (kg)",    "★ 250", "227", "★ 250", "★ 250", "227"],
                ["FOV máx. (cm)",              "50", "50", "★ 53", "50", "50"],
                ["Canales RF máx.",            "★ 204", "128", "128", "★ 204", "128"],
                ["SAR límite (W/kg)",          "4.0", "4.0", "4.0", "4.0", "4.0"],
                ["Ruido (dB)",                 "72", "74", "73", "78", "★ 79 (alto)"],
                ["Helio boil-off (L/año)",     "★ 0", "★ 0", "★ 0", "★ 0", "★ 0"],
                ["Consumo eléctrico (kVA)",    "★ 35", "40", "38", "★ 55", "60"],
                ["DICOM / HL7",                "Sí", "Sí", "Sí", "Sí", "Sí"],
                ["IA integrada",               "Sí", "Sí", "Sí", "Sí", "Sí"],
                ["Precio ref. (USD)",          "850K–1.2M", "800K–1.1M", "820K–1.15M", "1.4M–2.2M", "1.35M–2.1M"],
            ]
        },
        "notes": [
            "★ = valor más favorable en esa categoría de campo",
            "SAR (Specific Absorption Rate): límite regulatorio IEC 60601-2-33, máx. 4 W/kg cuerpo entero",
            "Helio boil-off = 0 en todos los equipos modernos gracias a tecnología de imán sin ventilación activa",
            "Precio referencial FOB — varía por configuración, accesorios e infraestructura de sala",
        ],
        "clinical": [
            ("Neurología", "Secuencias FLAIR, DWI, SWI — alta sensibilidad en tejido cerebral"),
            ("Oncología", "Perfusión, espectroscopía, DWI — estadificación y seguimiento tumoral"),
            ("Cardiología", "Cine MRI, mapeo T1/T2 — función ventricular y viabilidad miocárdica"),
            ("MSK", "Cartílago, ligamentos, tendones — sin radiación ionizante"),
            ("Abdomen/Pelvis", "MRCP, angio MR, secuencias dinámicas con contraste"),
        ],
    },

    "CT": {
        "title": "Tomografía Computada (CT — Computed Tomography)",
        "subtitle": "Principio físico: atenuación de rayos X por diferentes tejidos. Reconstrucción volumétrica mediante retroproyección filtrada o algoritmos iterativos/IA.",
        "intro": (
            "La TC adquiere proyecciones de rayos X desde múltiples ángulos mientras el gantry rota "
            "alrededor del paciente. Los detectores modernos permiten adquisición helicoidal con "
            "cobertura volumétrica amplia y tiempos de rotación menores a 0.3 s. La reconstrucción "
            "iterativa (ASIR, ADMIRE, iDose) y los algoritmos de deep learning (AiCE, TrueFidelity) "
            "permiten reducir dosis de radiación hasta un 80% respecto a la TC convencional."
        ),
        "comparison": {
            "headers": ["Parámetro", "CT 64c (A)", "CT 64c (B)", "CT 64c (C)", "CT 128c (A)", "CT 256c (A)"],
            "brand_header_colors": ["1A5276","2E4057","0A3D62","1A5276","1A5276"],
            "rows": [
                ["Cortes por rotación",         "64", "64", "64", "128", "★ 256"],
                ["Velocidad rotación (s)",       "0.50", "0.50", "0.50", "0.33", "★ 0.28"],
                ["Cobertura detector (mm)",      "38.4", "40", "40", "76.8", "★ 141"],
                ["Resolución espacial (lp/cm)",  "14", "14", "14", "15", "★ 16"],
                ["Res. temporal cardíaca (ms)",  "165", "175", "175", "83", "★ 75"],
                ["Bore (cm)",                   "★ 78", "70", "★ 78", "★ 78", "★ 78"],
                ["Peso máx. paciente (kg)",      "★ 250", "227", "★ 250", "★ 300", "★ 300"],
                ["Potencia tubo (kW)",           "40", "★ 50", "40", "60", "★ 100"],
                ["Rango kVp",                   "80–130", "80–140", "80–140", "70–150", "70–150"],
                ["Reducción de dosis (%)",       "60", "55", "58", "70", "★ 80"],
                ["Consumo eléctrico (kVA)",      "★ 32", "35", "★ 32", "50", "80"],
                ["CT Espectral / Dual Energy",   "No", "No", "No", "Opcional", "★ Sí"],
                ["IA en reconstrucción",         "Sí", "Sí", "Sí", "Sí", "Sí"],
                ["Precio ref. (USD)",            "280K–420K", "270K–410K", "275K–415K", "450K–680K", "700K–950K"],
            ]
        },
        "notes": [
            "★ = valor más favorable en parámetros comparables",
            "Reducción de dosis referida a técnica convencional sin algoritmo iterativo",
            "CT Espectral / Dual Energy: permite caracterización tisular por coeficiente de atenuación",
            "Precio referencial FOB — varía por configuración y mercado",
        ],
        "clinical": [
            ("Urgencias y Trauma", "Protocolo whole-body, alta velocidad — <10 s para tórax-abdomen-pelvis"),
            ("Cardiología", "Angio coronaria, score de calcio — requiere CT ≥ 64c, res. temporal < 100 ms"),
            ("Oncología", "Estadificación, seguimiento RECIST, guía de biopsias"),
            ("Neurología", "ACV isquémico/hemorrágico, perfusión cerebral, angio-TC"),
            ("Tórax (pulmón)", "Nódulos pulmonares, HRCT para intersticio, embolismo pulmonar"),
        ],
    },

    "US": {
        "title": "Ultrasonido / Ecografía (US — Ultrasonography)",
        "subtitle": "Principio físico: emisión y recepción de ondas acústicas de alta frecuencia (2–18 MHz). Sin radiación ionizante. Modalidad en tiempo real.",
        "intro": (
            "El ultrasonido genera imágenes mediante la reflexión de ondas acústicas en interfaces "
            "tisulares con diferente impedancia acústica. Los transductores modernos emplean matrices "
            "de cristales piezoeléctricos con formación digital de haz (beamforming). Las frecuencias "
            "altas (10–18 MHz) ofrecen mayor resolución pero menor penetración; frecuencias bajas "
            "(2–5 MHz) permiten mayor profundidad. El Doppler color y pulsado evalúan flujo vascular."
        ),
        "comparison": {
            "headers": ["Parámetro", "Equipo Portátil", "Equipo Mid-Range", "Equipo Premium", "Ecógrafo POCUS"],
            "brand_header_colors": ["2E4057","1A5276","0A3D62","4A235A"],
            "rows": [
                ["Rango frecuencia (MHz)",      "2–10", "1–18", "★ 1–22", "3–12"],
                ["Transductores disponibles",   "3–5", "8–12", "★ 15+", "2–3"],
                ["Doppler color",               "Sí", "Sí", "Sí", "Sí"],
                ["Elastografía",                "No", "Básica", "★ Avanzada", "No"],
                ["3D/4D en tiempo real",        "No", "Sí", "★ Sí", "No"],
                ["Contraste (CEUS)",            "No", "Opcional", "★ Sí", "No"],
                ["Profundidad máx. (cm)",       "25", "★ 35", "★ 35", "20"],
                ["Pantalla (pulgadas)",         "15", "19", "★ 23", "★ Tablet"],
                ["Peso equipo (kg)",            "★ 8", "15", "25", "★ 0.3"],
                ["Batería autónoma",            "Sí", "No", "No", "★ Sí"],
                ["IA integrada",                "Básica", "Sí", "★ Avanzada", "Básica"],
                ["Precio ref. (USD)",           "30K–60K", "60K–120K", "★ 120K–250K", "2K–8K"],
            ]
        },
        "notes": [
            "POCUS (Point-of-Care Ultrasound): dispositivos ultraminiaturizados para uso en urgencias y UCI",
            "CEUS (Contrast-Enhanced Ultrasound): uso de microburbujas para caracterización hepática y vascular",
            "Elastografía: cuantificación de rigidez tisular — aplicación en hígado (fibrosis), tiroides, mama",
            "★ = característica más favorable en esa categoría",
        ],
        "clinical": [
            ("Abdomen",        "Hígado, vesícula, páncreas, riñones — primera línea de imagen abdominal"),
            ("Obstetricia",    "Control prenatal, biometría fetal, Doppler umbilical — sin radiación"),
            ("Cardiología",    "Ecocardiografía transtorácica y transesofágica — función ventricular"),
            ("Vascular",       "Doppler carotídeo, venoso profundo — diagnóstico TVP y estenosis"),
            ("MSK/Urgencias",  "Fracturas, derrames articulares, guía de procedimientos en tiempo real"),
        ],
    },

    "RX": {
        "title": "Radiografía Convencional y Digital (RX — X-Ray)",
        "subtitle": "Principio físico: atenuación diferencial de rayos X según densidad y número atómico del tejido. Imagen 2D proyeccional.",
        "intro": (
            "La radiografía convierte la energía de los fotones X, tras atravesar el cuerpo, "
            "en una imagen proyeccional. Los sistemas digitales actuales (CR y DR) reemplazan "
            "la película radiográfica con detectores de panel plano (FPD) de silicio amorfo o "
            "selenio amorfo. El sistema DR directo ofrece mayor calidad de imagen y menor dosis "
            "que el CR. La teleradiología y la integración DICOM/RIS son estándar en instalaciones modernas."
        ),
        "comparison": {
            "headers": ["Parámetro", "RX Convencional (CR)", "RX Digital Directo (DR)", "RX Móvil DR", "Mamógrafo Digital"],
            "brand_header_colors": ["2E4057","1A5276","0A3D62","4A235A"],
            "rows": [
                ["Detector",                    "Fósforo (CR)", "★ FPD Silicio amorfo", "FPD portátil", "FPD Se amorfo"],
                ["Resolución (lp/mm)",          "3.0–4.0", "★ 3.4–4.5", "3.0–3.5", "★ 5.0–7.0"],
                ["Rango kVp",                   "40–150", "40–150", "40–125", "25–35"],
                ["Corriente máx. (mA)",         "500", "★ 800", "300", "100"],
                ["Latencia imagen (s)",         "60–120", "★ 3–5", "★ 3–5", "5–10"],
                ["Tamaño detector (cm)",        "35×43", "43×43", "35×43", "24×30"],
                ["DQE (%)",                     "30–45", "★ 65–75", "55–65", "★ 70–80"],
                ["DICOM compatible",            "Sí", "Sí", "Sí", "Sí"],
                ["Tomosíntesis",                "No", "Opcional", "No", "★ Sí"],
                ["IA para lectura",             "No", "★ Sí", "Básica", "★ Sí"],
                ["Precio ref. (USD)",           "15K–40K", "80K–180K", "40K–90K", "★ 150K–300K"],
            ]
        },
        "notes": [
            "DQE (Detective Quantum Efficiency): eficiencia de detección de fotones — mayor = mejor calidad/dosis",
            "Tomosíntesis (DBT): adquisición de múltiples proyecciones para reconstrucción pseudo-3D — reducción solapamiento",
            "RX móvil: uso en UCI, quirófano, neonatal — sin necesidad de trasladar al paciente",
            "Mamógrafo: equipos especializados con compresión estandarizada y dosis ultrabaja (< 3 mGy por proyección)",
        ],
        "clinical": [
            ("Tórax",           "Primera línea: neumonía, derrame, neumotórax, cardiomegalia"),
            ("Traumatología",   "Fracturas, luxaciones, cuerpos extraños — alta disponibilidad"),
            ("Columna",         "Evaluación postural, escoliosis, espondilopatías"),
            ("Abdomen",         "Obstrucción intestinal, neumoperitoneo — proyección en bipedestación"),
            ("Mamografía",      "Tamizaje y diagnóstico de cáncer de mama — protocolo ACR"),
        ],
    },

    "PET": {
        "title": "Tomografía por Emisión de Positrones (PET/CT — Positron Emission Tomography)",
        "subtitle": "Principio físico: detección de pares de fotones gamma (511 keV) emitidos por aniquilación de positrones. Imagen funcional metabólica.",
        "intro": (
            "El PET detecta radiotrazadores marcados con emisores de positrones (18F-FDG, 68Ga, 18F-NaF). "
            "Al aniquilarse el positrón con un electrón, se emiten dos fotones gamma de 511 keV en "
            "direcciones opuestas, detectados en coincidencia. La fusión PET/CT permite correlacionar "
            "la actividad metabólica (PET) con la anatomía (CT). El tiempo de vuelo (TOF) mejora la "
            "resolución de imagen al calcular la diferencia temporal entre los fotones."
        ),
        "comparison": {
            "headers": ["Parámetro", "PET/CT Estándar", "PET/CT TOF", "PET/CT Digital", "PET/MR Híbrido"],
            "brand_header_colors": ["2E4057","1A5276","0A3D62","4A235A"],
            "rows": [
                ["Resolución espacial (mm)",   "4–5", "3–4", "★ 2.5–3", "★ 2.5–3"],
                ["Sensibilidad (cps/kBq)",     "5–8", "8–12", "★ 12–18", "★ 15–20"],
                ["Tiempo de vuelo (TOF ps)",   "No", "400–600", "★ 210–370", "★ 230–400"],
                ["Longitud axial (cm)",        "15–22", "22–26", "★ 26–32", "25–30"],
                ["Componente CT (cortes)",     "16–64", "★ 64–128", "★ 128–256", "No aplica"],
                ["Componente MR",             "No", "No", "No", "★ Sí (3T)"],
                ["Radiotrazadores compatibles","FDG", "FDG, Ga-68", "★ Múltiples", "★ Múltiples"],
                ["Dosis radiación (mSv)",      "★ 3–5", "★ 3–5", "★ 2–4", "★ 1–3"],
                ["Tiempo adquisición (min)",   "20–30", "15–25", "★ 10–20", "45–90"],
                ["IA en reconstrucción",       "No", "Básica", "★ Avanzada", "★ Avanzada"],
                ["Precio ref. (USD M)",        "1.5–2.5M", "2.0–3.0M", "★ 2.5–4.0M", "★ 5.0–8.0M"],
            ]
        },
        "notes": [
            "TOF (Time of Flight): mejora SNR localizando la emisión en el eje axial mediante diferencia temporal",
            "18F-FDG (fluorodesoxiglucosa): trazador más utilizado — detecta hipermetabolismo en tumores y tejido cerebral activo",
            "PET/MR: máxima información combinada pero costo y complejidad muy elevados — uso principalmente en investigación y oncología pediátrica",
            "★ = valor más favorable en esa categoría",
        ],
        "clinical": [
            ("Oncología",       "Estadificación, respuesta a tratamiento, detección de recidiva — gold standard"),
            ("Neurología",      "Diagnóstico diferencial demencias (Alzheimer, FTD), epilepsia refractaria"),
            ("Cardiología",     "Viabilidad miocárdica, sarcoidosis cardíaca, endocarditis"),
            ("Infecciones",     "Fiebre de origen desconocido, osteomielitis, vasculitis de grandes vasos"),
            ("Planificación RT","Definición de volumen tumoral para radioterapia de precisión"),
        ],
    },

    "FLUORO": {
        "title": "Fluoroscopía y Sistemas de Rayos X Intervencionistas",
        "subtitle": "Principio físico: imagen de rayos X en tiempo real mediante intensificador de imagen o detector de panel plano. Guía de procedimientos intervencionistas.",
        "intro": (
            "La fluoroscopía permite obtener imágenes dinámicas en tiempo real mediante exposición "
            "continua o pulsada de rayos X. Los sistemas modernos emplean detectores de panel plano "
            "(FPD) en lugar del intensificador de imagen clásico, con mayor resolución y menor dosis. "
            "Las salas de hemodinámica (catlab) y los arcos en C quirúrgicos son los sistemas más "
            "utilizados en procedimientos cardiovasculares, ortopédicos y gastroenterológicos."
        ),
        "comparison": {
            "headers": ["Parámetro", "Fluoroscopio General", "Arco en C Móvil", "Sala Hemodinámica", "Sala Híbrida"],
            "brand_header_colors": ["2E4057","1A5276","0A3D62","4A235A"],
            "rows": [
                ["Detector",                   "FPD 43×43 cm", "FPD 30×30 cm", "★ FPD 30×40 cm", "★ FPD 30×40 cm"],
                ["Resolución (lp/mm)",         "2.5–3.5", "2.0–2.8", "★ 3.0–4.0", "★ 3.5–4.5"],
                ["Rango kVp",                  "40–125", "40–120", "★ 40–125", "★ 40–125"],
                ["Dosis fluoroscopia (mGy/min)","★ 1–5", "2–8", "★ 1–4", "★ 1–3"],
                ["DAP meter integrado",        "Sí", "Sí", "★ Sí (avanzado)", "★ Sí (avanzado)"],
                ["Sustracción digital (DSA)",  "Opcional", "No", "★ Sí", "★ Sí"],
                ["Rotación isocentro (°)",     "0 (fijo)", "±180", "★ ±270", "★ ±270"],
                ["Angiografía 3D",             "No", "No", "★ Sí", "★ Sí"],
                ["Integración con TC/MR",      "No", "No", "No", "★ Sí"],
                ["IA guidance",                "No", "No", "Sí", "★ Avanzada"],
                ["Precio ref. (USD)",          "80K–200K", "40K–120K", "800K–2.0M", "★ 2.0–5.0M"],
            ]
        },
        "notes": [
            "DAP (Dose-Area Product): métrica dosimétrica estándar en fluoroscopía — requisito regulatorio en todos los sistemas",
            "DSA (Digital Subtraction Angiography): sustracción de imagen basal para visualizar contraste en vasos",
            "Sala híbrida: combina sala quirúrgica con arco de alta calidad — cirugía cardiovascular y endovascular",
            "Arco en C: portátil — uso en quirófano ortopédico, traumatología y procedimientos intervencionistas",
        ],
        "clinical": [
            ("Cardiología Interv.", "Cateterismo, angioplastia, TAVI, implante de stents coronarios"),
            ("Radiología Interv.",  "Embolización, drenajes, biopsias guiadas, TIPS"),
            ("Ortopedia",          "Reducción de fracturas, osteosíntesis, vertebroplastia"),
            ("Gastroenterología",  "CPRE, colocación de stents biliares, manometría"),
            ("Neurología Interv.", "Angiografía cerebral, embolización de aneurismas, trombectomía"),
        ],
    },
}

# ── Header / Footer ───────────────────────────────────────────────────────────
class HeaderFooter(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self._saved_page_states = []
        super().__init__(*args, **kwargs)

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for i, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            self._current_page_num = i + 1
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        page_num = self._current_page_num

        # Header bar
        self.setFillColor(NAVY)
        self.rect(0, H - 28*mm, W, 28*mm, fill=1, stroke=0)

        self.setFillColor(WHITE)
        self.setFont("Helvetica-Bold", 11)
        self.drawString(18*mm, H - 16*mm,
            "Comparativa de Equipos de Imagen Médica — Todas las Modalidades")
        self.setFont("Helvetica", 8)
        self.drawRightString(W - 18*mm, H - 16*mm,
            "Imagenología Médica · UNMSM · Ing. Biomédica")

        self.setFillColor(TEAL)
        self.rect(0, H - 29.5*mm, W, 1.5*mm, fill=1, stroke=0)

        # Footer
        self.setFillColor(GRAY_L)
        self.rect(0, 0, W, 14*mm, fill=1, stroke=0)
        self.setStrokeColor(GRAY_BRD)
        self.setLineWidth(0.5)
        self.line(18*mm, 14*mm, W - 18*mm, 14*mm)

        self.setFillColor(GRAY_M)
        self.setFont("Helvetica", 7.5)
        self.drawString(18*mm, 5*mm,
            "Datos basados en especificaciones técnicas públicas de fabricantes (2024–2025). "
            "Valores orientativos — verificar con fabricante para configuración específica.")
        self.setFont("Helvetica-Bold", 8)
        self.drawRightString(W - 18*mm, 5*mm,
            f"Página {self._pageNumber} / {page_count}")


# ── Construcción del documento ─────────────────────────────────────────────────
def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=35*mm, bottomMargin=20*mm,
        title="Comparativa de Equipos de Imagen Médica",
        author="Joselyn Romero Avila — Ingeniería Biomédica UNMSM",
        subject="Imagenología Médica — Comparativa Técnica MRI, CT, US, RX, PET, Fluoroscopía",
    )

    story = []
    CW = W - 36*mm  # usable width

    # ── PORTADA ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("REPORTE TÉCNICO", S("tag",
        fontName="Helvetica-Bold", fontSize=9, textColor=TEAL,
        leading=12, spaceAfter=6, alignment=TA_LEFT)))

    story.append(Paragraph(
        "Comparativa de Equipos de<br/>Imagen Médica", sTitle))
    story.append(Paragraph(
        "Análisis técnico de modalidades: MRI · CT · Ultrasonido · Radiografía · PET/CT · Fluoroscopía",
        sSubtitle))

    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=GRAY_BRD))
    story.append(Spacer(1, 4*mm))

    meta_data = [
        ["Asignatura:", "Imagenología Médica"],
        ["Programa:", "B.Sc. Ingeniería Biomédica — UNMSM"],
        ["Autora:", "Joselyn Romero Avila"],
        ["Versión:", "2025"],
        ["Fuentes:", "Datasheets técnicos oficiales de fabricantes (2024–2025)"],
    ]
    meta_table = Table(meta_data, colWidths=[35*mm, CW - 35*mm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME",  (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",  (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE",  (0,0), (-1,-1), 9),
        ("TEXTCOLOR", (0,0), (0,-1), ACCENT),
        ("TEXTCOLOR", (1,0), (1,-1), GRAY_D),
        ("TOPPADDING",(0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("LEFTPADDING",(0,0),(-1,-1), 0),
        ("VALIGN",    (0,0),(-1,-1), "TOP"),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=GRAY_BRD))
    story.append(Spacer(1, 4*mm))

    # Resumen ejecutivo
    story.append(Paragraph("Resumen", sH2))
    story.append(Paragraph(
        "Este reporte presenta una comparativa técnica de los principales sistemas de imagen médica "
        "utilizados en entornos clínicos y hospitalarios. Para cada modalidad se describen los principios "
        "físicos de operación, los parámetros técnicos clave para evaluación y adquisición, y las "
        "aplicaciones clínicas prioritarias. El análisis comparativo por fabricante cubre parámetros "
        "de rendimiento, seguridad, infraestructura requerida y rango de precio referencial, con el "
        "objetivo de orientar decisiones de adquisición en el contexto de licitaciones públicas "
        "(SEACE/SERCOP) y procesos de compra privada en la región.",
        sBody))

    # Índice
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Contenido", sH2))
    toc_items = [
        ("1.", "Resonancia Magnética (MRI)", "MRI 1.5T y 3T"),
        ("2.", "Tomografía Computada (CT)", "64, 128 y 256 cortes"),
        ("3.", "Ultrasonido (US)", "Portátil, mid-range, premium y POCUS"),
        ("4.", "Radiografía (RX)", "CR, DR directo, móvil y mamografía"),
        ("5.", "PET/CT", "Estándar, TOF, digital y PET/MR"),
        ("6.", "Fluoroscopía e Intervencionismo", "General, arco en C, hemodinámica y sala híbrida"),
    ]
    toc_data = [[Paragraph(f"<b>{n}</b>", sTD_B),
                 Paragraph(title, sTD_L),
                 Paragraph(f"<i>{sub}</i>", sNote)]
                for n, title, sub in toc_items]
    toc_table = Table(toc_data, colWidths=[10*mm, 90*mm, CW-100*mm])
    toc_table.setStyle(TableStyle([
        ("VALIGN",      (0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0),(-1,-1), 0),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[GRAY_L, WHITE]),
        ("LINEBELOW",   (0,0),(-1,-1), 0.3, GRAY_BRD),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # ── SECCIONES POR MODALIDAD ────────────────────────────────────────────────
    mod_keys = ["MRI", "CT", "US", "RX", "PET", "FLUORO"]

    for idx, key in enumerate(mod_keys):
        mod = MODALITIES[key]

        # Número de sección + título
        story.extend(section_header(
            f"{idx+1}. {mod['title']}",
            mod['subtitle']
        ))

        # Introducción
        story.append(Paragraph(mod['intro'], sBody))
        story.append(Spacer(1, 3*mm))

        # Tabla comparativa
        story.append(Paragraph("Comparativa de parámetros técnicos", sH2))

        comp = mod['comparison']
        n_brands = len(comp['headers']) - 1
        param_w = 46*mm
        brand_w = (CW - param_w) / n_brands
        col_widths = [param_w] + [brand_w] * n_brands

        t = make_comparison_table(comp, col_widths)
        story.append(KeepTogether([t]))
        story.append(Spacer(1, 2*mm))

        # Notas
        for note in mod['notes']:
            story.append(Paragraph(f"• {note}", sNote))
        story.append(Spacer(1, 3*mm))

        # Aplicaciones clínicas
        story.append(Paragraph("Aplicaciones clínicas principales", sH2))
        clin_data = [[
            Paragraph(f"<b>{area}</b>", S("ca", fontName="Helvetica-Bold",
                fontSize=8, textColor=WHITE, leading=11, alignment=TA_LEFT)),
            Paragraph(desc, S("cd", fontName="Helvetica", fontSize=8,
                textColor=GRAY_D, leading=11, alignment=TA_LEFT))
        ] for area, desc in mod['clinical']]

        clin_table = Table(clin_data, colWidths=[38*mm, CW - 38*mm])
        clin_cmds = [
            ("BACKGROUND",    (0,0),(0,-1), TEAL),
            ("BACKGROUND",    (1,0),(1,-1), TEAL_LT),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 6),
            ("RIGHTPADDING",  (0,0),(-1,-1), 6),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
            ("GRID",          (0,0),(-1,-1), 0.3, GRAY_BRD),
            ("ROWBACKGROUNDS",(1,0),(1,-1), [TEAL_LT, WHITE]),
        ]
        clin_table.setStyle(TableStyle(clin_cmds))
        story.append(KeepTogether([clin_table]))

        if idx < len(mod_keys) - 1:
            story.append(PageBreak())

    # ── PÁGINA FINAL — DISCLAIMER ──────────────────────────────────────────────
    story.append(PageBreak())
    story.extend(section_header("Notas sobre las especificaciones técnicas"))
    disclaimer_items = [
        "Los valores presentados provienen de datasheets públicos de fabricantes (2024–2025) y pueden variar según configuración, accesorios opcionales y mercado de destino.",
        "Los rangos de precio son referenciales FOB y no incluyen instalación, obras civiles, capacitación ni contrato de mantenimiento.",
        "Para procesos de adquisición pública, los valores de referencia deben ser verificados con cotizaciones oficiales del fabricante o distribuidor autorizado.",
        "Las marcas son identificadas genéricamente (Marca A, B, C, D) para mantener neutralidad en el análisis. Los parámetros técnicos corresponden a los modelos líderes de cada segmento en el mercado latinoamericano.",
        "Fuentes consultadas: portales de producto de los principales fabricantes, fichas técnicas ECRI Institute, WHO Medical Equipment Technical Specifications y bases de datos de licitaciones SEACE/SERCOP.",
    ]
    for item in disclaimer_items:
        story.append(Paragraph(f"• {item}", sBody))
        story.append(Spacer(1, 2*mm))

    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=GRAY_BRD))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "Joselyn Romero Avila · B.Sc. Ingeniería Biomédica · UNMSM · 2025",
        S("fin", fontName="Helvetica-Oblique", fontSize=9,
          textColor=GRAY_M, leading=13, alignment=TA_CENTER)))

    # ── BUILD ──────────────────────────────────────────────────────────────────
    doc.build(story, canvasmaker=HeaderFooter)
    print(f"✅ PDF generado: {output_path}")


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    build_pdf("outputs/Comparativa_Equipos_Imagen_Medica_UNMSM.pdf")

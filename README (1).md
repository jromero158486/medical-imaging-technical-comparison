# 🏥 MRI & CT Technical Comparison — Siemens vs GE vs Philips vs Canon

> **Context:** Technical specification comparison tool built to support procurement decisions for MRI and CT equipment in public tenders (SEACE/SERCOP) and private acquisitions in Peru and Ecuador. Developed as part of the Public Investment Projects course at UNMSM.

🔗 **Live dashboard:** [jromero158486.github.io/mri-ct-technical-comparison](https://jromero158486.github.io/mri-ct-technical-comparison)

---

## 📋 What This Project Does

Evaluates **17 technical parameters** across 5 equipment segments:

| Segment | Models Compared | Price Range (USD) |
|---|---|---|
| MRI 1.5T | Siemens MAGNETOM Sola · GE SIGNA Artist · Philips Ingenia · Canon Vantage | $750K – $1.2M |
| MRI 3T | Siemens MAGNETOM Vida · GE SIGNA Premier · Philips Ingenia Elition | $1.35M – $2.2M |
| CT 64 slices | Siemens SOMATOM go.Up · GE Revolution EVO · Philips Incisive · Canon Aquilion | $265K – $420K |
| CT 128 slices | Siemens SOMATOM go.Top · GE Revolution Ascend · Philips Incisive 128 | $440K – $680K |
| CT 256 slices | Siemens Definition AS+ · GE Revolution HD · Philips IQon Spectral CT | $680K – $970K |

### Parameters evaluated

**MRI:** Field strength · Gradient amplitude · Slew rate · Bore diameter · Patient weight limit · FOV · RF channels · SAR · Noise level · Helium boil-off · Power consumption · DICOM/HL7 · AI features · Reference price

**CT:** Slices · Rotation speed · Detector coverage · Tube power · kVp range · Spatial resolution · Temporal resolution · Bore diameter · Patient weight · Dose reduction · Power consumption · DICOM · Spectral CT · AI features · Reference price

---

## 📁 Repository Structure

```
mri-ct-technical-comparison/
├── index.html                          # Interactive dashboard (GitHub Pages)
├── data/
│   └── specs.json                      # Technical specs database (all equipment)
├── scripts/
│   └── build_comparison_excel.py       # Generates formatted Excel comparison workbook
├── outputs/
│   └── MRI_CT_Technical_Comparison.xlsx  # Excel output (6 sheets)
└── README.md
```

---

## 🖥️ Interactive Dashboard

The `index.html` file is a standalone interactive comparison tool:

- **Executive Summary** — side-by-side overview of all 5 segments with procurement recommendations
- **Per-segment tabs** — full technical parameter table with best/worst value highlighting
- **Brand cards** — key differentiators and clinical applications per manufacturer
- **Color coding:**
  - 🟢 Green cell = best value in parameter
  - 🔴 Red cell = lowest value in parameter
  - **Bold** = Siemens Healthineers values

To use locally:
```bash
# Just open in browser — no server needed
open index.html
```

---

## 📊 Excel Workbook

The Excel file (`MRI_CT_Technical_Comparison.xlsx`) contains 6 sheets:

1. **Resumen_Ejecutivo** — executive summary table, all segments, procurement use cases
2. **MRI_1.5T** — full 17-parameter comparison, 4 manufacturers
3. **MRI_3T** — full 17-parameter comparison, 3 manufacturers
4. **CT_64slices** — full 15-parameter comparison, 4 manufacturers
5. **CT_128slices** — full 15-parameter comparison, 3 manufacturers
6. **CT_256slices** — full 15-parameter comparison, 3 manufacturers

**Features:**
- Color-coded by manufacturer (Siemens teal, GE purple, Philips blue, Canon red)
- Green/red highlighting for best/worst values per parameter
- Category separators (Core, Patient, Image, Safety, Operations, IT, Advanced, Commercial)
- Highlights and clinical applications sections per equipment
- Ready to use as Power BI data source

### Generate Excel from scratch:
```bash
pip install pandas openpyxl
python scripts/build_comparison_excel.py
```

---

## 🔬 Data Sources

All specifications sourced from **publicly available manufacturer datasheets**:

| Manufacturer | Source |
|---|---|
| Siemens Healthineers | healthcare.siemens.com/magnetic-resonance-imaging · /computed-tomography |
| GE Healthcare | gehealthcare.com/products/magnetic-resonance-imaging · /ct-scanning |
| Philips Healthcare | philips.com/healthcare/solutions/magnetic-resonance-imaging · /ct |
| Canon Medical | global.medical.canon/products/ct · /mri |

> ⚠️ **Disclaimer:** Specifications are from publicly available datasheets (2024–2025). Values may vary by configuration, accessories, and market. For procurement purposes, always request an official quote from the manufacturer.

---

## 🏛️ Relevance for Public Procurement (Peru & Ecuador)

This comparative analysis format mirrors the **technical specification response** used in:

- **SEACE (Peru)** — Licitaciones Públicas and Adjudicaciones Simplificadas for medical equipment
- **SERCOP (Ecuador)** — Licitaciones and Cotizaciones for health sector procurement
- **Private hospital RFQs** — Request for Quotation processes in private health networks

Key procurement parameters highlighted in this analysis:
- Reference price ranges (FOB) for budget planning
- DICOM/HL7 compliance (mandatory in most Peruvian public tenders)
- Dose reduction capabilities (MINSA regulatory requirement)
- Installation power requirements (infrastructure planning)
- Patient weight limits (bariatric patient protocols)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python + pandas | Data processing |
| openpyxl | Excel generation with professional formatting |
| Vanilla JS + HTML/CSS | Interactive dashboard (no frameworks, zero dependencies) |
| JSON | Structured specs database |

---

## 📌 Skills Demonstrated

- Technical specification analysis for clinical medical imaging equipment
- Competitive intelligence: Siemens vs GE vs Philips vs Canon
- Excel dashboard design for procurement support
- MRI physics knowledge: field strength, gradients, SAR, RF channels, space-k
- CT parameters: rotation speed, detector coverage, dual energy, dose reduction
- Public procurement process knowledge (SEACE/SERCOP)
- Python data pipeline + automated report generation

---

*Academic project — Joselyn Romero Avila · B.Sc. Biomedical Engineering · UNMSM · Public Investment Projects course*

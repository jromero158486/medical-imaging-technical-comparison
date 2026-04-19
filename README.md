# Comparativa Técnica de Sistemas de Imagen Médica
**Curso: Imagenología Médica | Ingeniería Biomédica — UNMSM | 2025**

Reporte técnico que analiza y compara los principales sistemas de adquisición de imagen médica utilizados en la práctica clínica. El documento abarca seis modalidades de diagnóstico por imagen, describiendo los fundamentos físicos de cada una y evaluando los parámetros técnicos relevantes para su selección, operación y uso clínico.

**[Reporte completo (PDF)](assets/Comparativa_Equipos_Imagen_Medica.pdf)**

---

## Objetivo

Desarrollar un análisis comparativo estructurado de los equipos de imagen médica más utilizados en el entorno clínico hospitalario, integrando conocimientos de física médica, instrumentación biomédica y criterios de evaluación técnica aplicados a la selección de equipos en el sistema de salud.

---

## Modalidades cubiertas

| # | Modalidad | Principio físico | Sistemas analizados |
|---|---|---|---|
| 1 | Resonancia Magnética (MRI) | Campo magnético + pulsos RF + espacio-k | 1.5T y 3T — 4 fabricantes |
| 2 | Tomografía Computada (CT) | Atenuación de rayos X + reconstrucción iterativa | 64, 128 y 256 cortes |
| 3 | Ultrasonido (US) | Reflexión de ondas acústicas (2–18 MHz) | Portátil, mid-range, premium, POCUS |
| 4 | Radiografía (RX) | Atenuación diferencial de rayos X | CR, DR directo, móvil, mamógrafo |
| 5 | PET/CT | Detección de pares gamma (511 keV) por aniquilación | Estándar, TOF, digital, PET/MR |
| 6 | Fluoroscopía | Imagen de rayos X en tiempo real | General, arco en C, hemodinámica, sala híbrida |

---

## Estructura del reporte

Cada sección incluye:

- **Fundamento físico** — principio de operación y bases del proceso de adquisición de imagen
- **Tabla comparativa de parámetros técnicos** — evaluación cuantitativa de los principales indicadores de rendimiento, seguridad e infraestructura requerida
- **Notas técnicas** — definiciones de términos clave (SAR, DQE, TOF, slew rate, CEUS, DAP, etc.)
- **Aplicaciones clínicas** — indicaciones por especialidad y contexto de uso

---

## Parámetros evaluados (selección)

**MRI:** Intensidad de campo (T) · Gradiente máximo (mT/m) · Slew rate (T/m/s) · Diámetro de bore · FOV · Canales RF · SAR · Nivel acústico · Consumo eléctrico · Compatibilidad DICOM/HL7

**CT:** Cortes por rotación · Velocidad de rotación (s) · Cobertura de detector (mm) · Resolución espacial (lp/cm) · Resolución temporal (ms) · Reducción de dosis (%) · CT espectral / dual energy

**US / RX / PET / Fluoroscopía:** parámetros específicos por modalidad detallados en el reporte

---

## Generación del documento

El reporte fue generado programáticamente en Python usando ReportLab:

```bash
pip install reportlab
python build_medical_imaging_pdf.py
```

---

## Fuentes

- Datasheets técnicos públicos de fabricantes de equipos médicos (2024–2025)
- ECRI Institute — Medical Equipment Technical Specifications
- WHO — Medical Devices Technical Series
- IEC 60601-2-33 (MRI), IEC 60601-1 (seguridad general equipos médicos)
- Bushberg et al., *The Essential Physics of Medical Imaging*, 3rd ed.
- Sprawls, *Physical Principles of Medical Imaging*, 2nd ed.

---

*Joselyn Romero Avila · B.Sc. Ingeniería Biomédica · UNMSM · 2025*

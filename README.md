# Comparativa Técnica de Sistemas de Imagen Médica
### Proyecto Final — Imagenología Médica
**B.Sc. Ingeniería Biomédica · Universidad Nacional Mayor de San Marcos (UNMSM) · 2025**

> Autora: Joselyn Romero Avila

**[Reporte completo (PDF)](assets/Comparativa_Imagen_Medica_UNMSM_LaTeX.pdf)**

---

## 1. Introducción

El diagnóstico por imagen constituye uno de los pilares fundamentales de la medicina moderna. La selección adecuada de un sistema de imagen médica requiere evaluar no solo sus capacidades clínicas, sino también sus parámetros técnicos de rendimiento, requerimientos de infraestructura, seguridad radiológica y costo-efectividad en el contexto de cada institución de salud.

En el Perú y Ecuador, los hospitales del sector público (EsSalud, MINSA, IESS) adquieren estos equipos mediante procesos de licitación pública regulados por el SEACE y SERCOP respectivamente. La correcta interpretación de las especificaciones técnicas en estos procesos es determinante para garantizar la adquisición de equipos adecuados a las necesidades clínicas y presupuestarias de cada institución.

Este reporte presenta una comparativa técnica estructurada de las seis principales modalidades de imagen médica utilizadas en entornos clínicos hospitalarios, con el objetivo de sistematizar los criterios de evaluación técnica aplicables a procesos de adquisición en el sistema de salud.

---

## 2. Objetivos

### Objetivo general
Desarrollar un análisis comparativo técnico de los principales sistemas de imagen médica utilizados en la práctica clínica, evaluando parámetros de rendimiento, seguridad e infraestructura para cada modalidad.

### Objetivos específicos
- Describir los principios físicos de operación de cada modalidad de imagen médica
- Identificar y definir los parámetros técnicos clave para la evaluación y selección de equipos
- Elaborar matrices comparativas cuantitativas por modalidad y tipo de equipo
- Relacionar las características técnicas de cada sistema con sus aplicaciones clínicas prioritarias
- Sistematizar criterios técnicos aplicables a procesos de adquisición pública y privada

---

## 3. Modalidades analizadas

| # | Modalidad | Principio físico | Equipos comparados |
|---|---|---|---|
| 1 | Resonancia Magnética (MRI) | Campo magnético estático + pulsos RF + espacio-k | 1.5T y 3T — 4 tipos de equipo |
| 2 | Tomografía Computada (CT) | Atenuación de rayos X + reconstrucción iterativa/IA | 64, 128 y 256 cortes |
| 3 | Ultrasonido (US) | Reflexión de ondas acústicas (2–18 MHz) | Portátil, mid-range, premium, POCUS |
| 4 | Radiografía (RX) | Atenuación diferencial de rayos X | CR, DR directo, RX móvil, mamógrafo digital |
| 5 | PET/CT | Detección en coincidencia de fotones gamma (511 keV) | Estándar, TOF, digital, PET/MR híbrido |
| 6 | Fluoroscopía e Intervencionismo | Imagen de rayos X en tiempo real (FPD/intensificador) | General, arco en C, sala de hemodinámica, sala híbrida |

---

## 4. Metodología

### 4.1 Selección de parámetros técnicos

Para cada modalidad se identificaron los parámetros técnicos más relevantes para la evaluación clínica y la adquisición de equipos, agrupados en las siguientes categorías:

- **Core / Rendimiento:** parámetros que determinan la calidad de imagen y la velocidad de adquisición
- **Paciente:** capacidad de carga, dimensiones del bore o gantry, accesibilidad
- **Seguridad:** dosis de radiación, SAR, DQE, niveles acústicos
- **Operación:** consumo eléctrico, requerimientos de infraestructura, consumibles
- **IT / Conectividad:** compatibilidad DICOM, integración con HIS/RIS, interoperabilidad HL7/FHIR
- **Avanzado:** capacidades de IA, modalidades especiales (dual energy, elastografía, TOF)
- **Comercial:** rango de precio referencial FOB

### 4.2 Fuentes de datos

Las especificaciones técnicas fueron obtenidas de fuentes públicas primarias:

- Datasheets y fichas técnicas oficiales publicadas en los portales de producto de los fabricantes (2024–2025)
- Especificaciones técnicas de la OMS para equipos de imagen médica (*WHO Medical Equipment Technical Specifications*)
- Base de datos técnicos del ECRI Institute
- Normativa técnica aplicable: IEC 60601-2-33 (MRI), IEC 60601-1 (seguridad general)

Los fabricantes son identificados genéricamente (Marca A, B, C, D) para mantener neutralidad en el análisis comparativo. Los valores corresponden a los modelos representativos del segmento de mercado latinoamericano (2024–2025).

### 4.3 Criterio de comparación

En cada tabla comparativa, la celda marcada con ★ indica el valor más favorable dentro de ese parámetro. Para parámetros donde mayor valor es mejor (gradiente, canales RF, reducción de dosis), ★ señala el máximo; para parámetros donde menor valor es mejor (ruido, consumo eléctrico, tiempo de rotación), ★ señala el mínimo. Los parámetros cualitativos o neutrales no se marcan.

### 4.4 Herramientas

El reporte fue redactado y formateado en **LaTeX** mediante **Overleaf**, utilizando los paquetes `booktabs`, `colortbl`, `tcolorbox`, `fancyhdr`, `titlesec` y `amssymb`. La elección de LaTeX responde a los estándares de documentación técnica en ingeniería biomédica y permite reproducibilidad total del documento.

```
Comparativa_Imagen_Medica_UNMSM.tex   ← fuente LaTeX
assets/
└── Comparativa_Imagen_Medica_UNMSM.pdf   ← PDF
```

Para compilar localmente:
```bash
pdflatex Comparativa_Imagen_Medica_UNMSM.tex
```

---

## 5. Resultados

### 5.1 Resonancia Magnética (MRI)
Los equipos de 1.5T representan la opción estándar para hospitales de mediana complejidad, con precios referenciales entre USD 750K–1.2M. Los equipos de 3T ofrecen mayor resolución de imagen (gradientes de hasta 80 mT/m, slew rate de 333 T/m/s) y son indicados para centros especializados en neurología avanzada, fMRI y cardiología. Todos los equipos modernos presentan helio boil-off nulo. El número de canales RF (hasta 204) es un diferenciador clave en la calidad de imagen obtenida.

### 5.2 Tomografía Computada (CT)
La CT de 64 cortes constituye la opción de mayor costo-efectividad para rutina clínica y urgencias (USD 265K–420K). La CT de 128 cortes es la opción óptima para hospitales de alta complejidad con programa de cardiología (resolución temporal < 90 ms). La CT de 256 cortes con dual energy está indicada en centros de referencia oncológicos y cardiovasculares. Los algoritmos de reconstrucción con IA reducen la dosis de radiación hasta un 80% respecto a la TC convencional.

### 5.3 Ultrasonido
El ultrasonido es la modalidad de mayor disponibilidad y menor costo, sin radiación ionizante. Los dispositivos POCUS (USD 2K–8K) permiten uso en el punto de atención (urgencias, UCI, obstetricia) con alta portabilidad. Los equipos premium incorporan elastografía avanzada y CEUS para caracterización tisular. La elección depende principalmente del volumen de pacientes y las especialidades a atender.

### 5.4 Radiografía Digital
Los sistemas DR directos (FPD) superan significativamente a los CR en DQE (65–75% vs 30–45%), latencia de imagen (3–5 s vs 60–120 s) y calidad diagnóstica, justificando su mayor costo en entornos de alto volumen. Los mamógrafos digitales con tomosíntesis representan el estándar actual para programas de tamizaje oncológico.

### 5.5 PET/CT
Los sistemas TOF y digitales ofrecen mejoras sustanciales en resolución espacial y sensibilidad respecto a los sistemas estándar, con tiempos de adquisición hasta 50% menores. El PET/MR híbrido ofrece la mayor información diagnóstica combinada pero su costo (USD 5–8M) limita su uso a centros de investigación y oncología pediátrica especializada.

### 5.6 Fluoroscopía e Intervencionismo
Las salas de hemodinámica y las salas híbridas representan la infraestructura más compleja y costosa (USD 800K–5M), pero son indispensables para los programas de cardiología e radiología intervencionistas. Los arcos en C móviles (USD 40K–120K) cubren las necesidades de ortopedia y procedimientos quirúrgicos guiados por imagen.

---

## 6. Conclusiones

- La selección de un sistema de imagen médica debe responder a un análisis integrado de las necesidades clínicas de la institución, el perfil epidemiológico de la población atendida, la infraestructura disponible y el presupuesto de adquisición y mantenimiento.
- Los parámetros técnicos presentados en este reporte constituyen una base objetiva para la elaboración de especificaciones técnicas en procesos de licitación pública (SEACE/SERCOP) y evaluación de propuestas de fabricantes.
- La integración DICOM/HL7 y la compatibilidad con sistemas de información hospitalaria (HIS/RIS/PACS) son requisitos transversales a todas las modalidades en entornos institucionales modernos.
- La incorporación de algoritmos de inteligencia artificial en reconstrucción de imagen (CT, MRI, RX, PET) representa la tendencia tecnológica más relevante del período 2022–2025, con impacto directo en la reducción de dosis y mejora de la calidad diagnóstica.
- Los rangos de precio presentados son referenciales FOB y deben complementarse con análisis de costo total de propiedad (TCO), incluyendo instalación, mantenimiento, capacitación y consumibles.

---

## 7. Referencias bibliográficas

1. Bushberg, J.T., Seibert, J.A., Leidholdt, E.M., Boone, J.M. *The Essential Physics of Medical Imaging*, 3rd ed. Lippincott Williams & Wilkins, 2011.
2. Sprawls, P. *Physical Principles of Medical Imaging*, 2nd ed. Medical Physics Publishing, 1995.
3. Westbrook, C., Roth, C.K., Talbot, J. *MRI in Practice*, 5th ed. Wiley-Blackwell, 2019.
4. Kalender, W.A. *Computed Tomography: Fundamentals, System Technology, Image Quality, Applications*, 3rd ed. Publicis, 2011.
5. IEC 60601-2-33:2010+AMD1:2013+AMD2:2015. *Particular requirements for the basic safety and essential performance of magnetic resonance equipment for medical diagnosis.*
6. IEC 60601-1:2005+AMD1:2012. *Medical electrical equipment — Part 1: General requirements for basic safety and essential performance.*
7. World Health Organization. *WHO Medical Equipment Technical Specifications.* WHO Press, 2011.
8. ECRI Institute. *Medical Equipment Comparison Reports* (2024–2025). Consultado en: ecri.org
9. Organismo Supervisor de las Contrataciones del Estado (OSCE). *Estándares técnicos para equipos de imagen médica — SEACE.* Lima, Perú.
10. Servicio Nacional de Contratación Pública (SERCOP). *Especificaciones técnicas referenciales — equipos médicos.* Quito, Ecuador.

---

*Joselyn Romero Avila · B.Sc. Ingeniería Biomédica · UNMSM · 2025*

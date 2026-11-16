---
title: "Documento de negocio"
subtitle: "Hábitos musicales, estado de ánimo, estrés académico y uso de IA en estudiantes de MAC, FES Acatlán"
lang: es-MX
---

## Registro de avances

| Fecha | Etapa | Entregables | Estado |
|-------|-------|-------------|--------|
| 2026-11-15 | Momento A: análisis y selección de documentos | `docs/momento_A.md`, `.docx` y `.pdf`; `notebooks/00_momento_A.ipynb`; `docs/matriz_relacion.csv`; `src/momento_a.py` | Concluido |
| 2026-11-15 | Momento A, ajuste de formato | Redacción en tono académico; versión en notebook ejecutado sin errores; exportación a Word y PDF con `src/exportar_docs.py` | Concluido |
| 2026-11-15 | Fase 0: definición del proyecto | Este documento (secciones 1 a 8), en `.md`, `.docx` y `.pdf` | Concluido |
| — | Fase 2: problemática, solución y KPI | Se agregará a este documento | Pendiente |

## 1. Antecedentes: resultado del Momento A

Antes de definir el proyecto se analizaron los seis cuestionarios disponibles para determinar cuáles son pertinentes para la pregunta de investigación. El análisis completo está en `docs/momento_A.pdf` y puede reproducirse con `notebooks/00_momento_A.ipynb`. Sus conclusiones condicionan la definición del proyecto:

- **Documentos seleccionados.** Se integrarán tres cuestionarios. El principal es *La música y su influencia en el estado de ánimo* (Documento 1). El complementario fuerte, *Entorno Universitario y Bienestar* (Documento 2), mide el bienestar directamente. El complementario medio, *Desempeño académico por el uso de IA* (Documento 3), aporta la variable moderadora.
- **Documentos descartados.** Se descartan *Test*, *Pelis y series* y *Relación Amor – Carrera*. Comparten la llave con los demás, pero no contienen variables relacionadas con la pregunta de investigación.
- **Tamaño de la muestra.** La integración por número de cuenta conserva **19 estudiantes**, todos de séptimo semestre de MAC.
- **Medición del estrés.** Ningún cuestionario incluye una escala de estrés. Se usarán indicadores indirectos: desánimo, irritabilidad, efecto percibido de la IA en la carga mental y música escuchada en momentos de estrés.

Por estos hallazgos, la pregunta y la hipótesis originales se mantienen en lo sustancial, pero en la sección 4 se **operacionalizan** con las variables que realmente existen en los datos.

## 2. Problemática

Los estudiantes de MAC en séptimo semestre enfrentan una carga académica alta, traslados largos y un uso creciente de herramientas de IA. Esto se refleja en estrés, alteraciones del sueño y cambios de ánimo. Aunque escuchan música cotidianamente, no se ha documentado qué hábitos musicales se asocian con un mejor estado de ánimo reportado ni cómo interactúan con el estrés académico y el uso de IA.

**Validación con los datos.** Los cuestionarios contienen evidencia de cada elemento de la problemática. El Documento 2 registra tiempos de traslado, calidad del sueño, desánimo e irritabilidad; el Documento 3, horas diarias de uso de IA y su efecto percibido en el estrés; el Documento 1, los hábitos de escucha y el cambio de ánimo atribuido a la música. La única afirmación que los datos no permiten verificar de forma directa es el carácter *creciente* del uso de IA, porque no hay mediciones repetidas en el tiempo. Solo puede aproximarse con el semestre en que cada estudiante empezó a usar estas herramientas.

## 3. Objetivos

### 3.1 Objetivo general

Identificar qué hábitos musicales (género, duración, momento y contexto de escucha) se asocian con un mejor estado de ánimo reportado por estudiantes de séptimo semestre de MAC, y describir cómo se relacionan esos hábitos con indicadores de estrés académico, sueño y uso de herramientas de IA.

### 3.2 Objetivos específicos

1. **Depurar e integrar** los tres cuestionarios seleccionados. Esto incluye codificar las respuestas abiertas en variables cuantitativas y categóricas con reglas documentadas y reproducibles (Fases 3 y 4).
2. **Describir** los hábitos musicales de la población: géneros predominantes, horas diarias de escucha, momentos, actividades y plataformas (Fase 4).
3. **Medir la asociación** entre los hábitos musicales y el estado de ánimo reportado, usando correlación de Spearman y pruebas de independencia ji-cuadrada o exacta de Fisher (Fase 4).
4. **Contrastar** el ánimo atribuido a la música con los indicadores generales de bienestar (desánimo, irritabilidad, sueño, concentración) y con el uso de IA (Fase 4).
5. **Segmentar** a los estudiantes en perfiles de hábitos y bienestar mediante agrupamiento no supervisado (K-Means o DBSCAN, con PCA para visualizar). Si la variable lo permite, **estimar** un modelo de clasificación de "mejora de ánimo" y compararlo contra una línea base (Fase 5).
6. **Comunicar** los resultados en un tablero interactivo dirigido a estudiantes, tutores y coordinación (Fase 6) y en documentación técnica y de negocio (Fase 7).

## 4. Pregunta de investigación e hipótesis

### 4.1 Pregunta

¿Qué hábitos musicales se asocian con un mejor estado de ánimo reportado en estudiantes de MAC, y cómo se relacionan con su nivel de estrés académico y su uso de IA?

### 4.2 Hipótesis general

Ciertos géneros, momentos y frecuencias de escucha se asocian con un estado de ánimo más positivo y con menores indicadores de estrés, y el uso de IA puede moderar esta relación.

### 4.3 Hipótesis operacionales

| Clave | Hipótesis | Variables (documento) | Prueba prevista |
|-------|-----------|-----------------------|-----------------|
| H1 | Los estudiantes que reportan que la música mejora su ánimo presentan menor frecuencia de desánimo e irritabilidad. | Mejora de ánimo (Doc 1, P5); desánimo e irritabilidad (Doc 2, P10 y P11) | Mann-Whitney U / Spearman |
| H2 | Más horas diarias de escucha y escuchar música durante el estudio o el traslado se asocian con mejora de ánimo y con mayor concentración percibida. | Horas (Doc 1, P2); momentos (P3); concentración (P10; Doc 2, P16) | Spearman / ji-cuadrada o Fisher |
| H3 | Algunos grupos de géneros musicales se asocian más que otros con estados positivos (tranquilidad, motivación). | Género predominante (Doc 1, P1 y P6); mejora de ánimo (P5) | Ji-cuadrada o Fisher |
| H4 | La relación entre hábitos musicales y ánimo difiere según la intensidad o la modalidad de uso de IA (guía frente a atajo). | Horas de IA (Doc 3, P12); modalidad (P15); efecto en el estrés (P9) | Comparación estratificada (exploratoria) |

Con 19 observaciones, la potencia estadística es baja. Por eso H4 se evaluará solo de forma **exploratoria y descriptiva** (comparación por estratos), sin pretender probar formalmente un efecto de interacción. Ninguna hipótesis se interpretará en términos causales.

## 5. Alcance

| Nivel | Qué incluye | Fase |
|-------|-------------|------|
| **Descriptivo** | Perfil de hábitos musicales, bienestar y uso de IA; indicadores clave por perfil | 4 y 6 |
| **Exploratorio** | Asociaciones bivariadas, contraste entre fuentes y segmentación en perfiles | 4 y 5 |
| **Predictivo condicional** | Clasificación de "mejora de ánimo", **solo si** la etiqueta derivada del texto libre tiene suficiente variabilidad (al menos 4 casos en la clase minoritaria) y el modelo supera la línea base | 5 |

**Fuera del alcance:**

- Inferencias causales.
- Generalizar a otros semestres, carreras o planteles, porque la población es exclusivamente de séptimo semestre de MAC.
- Diagnósticos clínicos de estrés, ansiedad o depresión.
- Integrar los documentos descartados en el Momento A.

## 6. Partes interesadas

| Parte interesada | Interés | Uso esperado de los resultados |
|------------------|---------|--------------------------------|
| Estudiantes de MAC | Conocer qué hábitos de escucha se asocian con un mejor ánimo y una mejor concentración | Autorregular sus hábitos de estudio y descanso |
| Tutores académicos | Identificar perfiles con indicadores de bienestar bajos | Orientar acompañamiento y canalización oportuna |
| Coordinación de MAC | Tener un panorama del bienestar y del uso de IA en el semestre terminal | Diseñar actividades de bienestar y lineamientos sobre el uso de IA |
| Equipo del proyecto y docente del curso | Aplicar el ciclo completo de ciencia de datos | Evaluar la calidad metodológica y la reproducibilidad |

## 7. Criterios de éxito

| Dimensión | Criterio | Verificación |
|-----------|----------|--------------|
| Datos | Los tres documentos quedan limpios e integrados por número de cuenta, con los registros conservados y perdidos reportados | `data/processed/`, Fase 4 |
| Datos | Todas las variables de las hipótesis se codifican con reglas explícitas y una bitácora de decisiones; los valores no codificables se reportan como faltantes, nunca se inventan | `notebooks/01_limpieza.ipynb` |
| Análisis | Cada hipótesis H1 a H4 se evalúa con estadístico, valor *p* (o descripción, en H4) y tamaño de efecto | `notebooks/02_eda.ipynb` |
| Modelado | El agrupamiento produce perfiles interpretables, con coeficiente de silueta reportado (≥ 0.25 como referencia de estructura razonable) | `notebooks/03_modelado.ipynb` |
| Modelado | Si se estima el modelo supervisado, se compara con una línea base (clase mayoritaria) usando validación cruzada y F1. Si no la supera, se reporta como resultado y no se oculta | `notebooks/03_modelado.ipynb` |
| Producto | El tablero se ejecuta con `streamlit run app/app.py` y muestra los KPI con filtros | `app/app.py` |
| Comunicación | Documentos técnico y de negocio completos en `.md`, `.docx` y `.pdf`; repositorio reproducible con datos anonimizados | `docs/`, `README.md` |

## 8. Supuestos y restricciones

- Las respuestas son **auto-reportadas** y pueden estar sesgadas por deseabilidad social o por la interpretación personal de cada pregunta.
- Casi todas las variables provienen de **texto libre**, así que su codificación implica decisiones del equipo que deben documentarse y que podrían influir en los resultados.
- Los números de cuenta y correos son datos personales. Se **anonimizarán** antes de versionar el proyecto en Git y los datos crudos no se publicarán.
- El análisis se hace en Python (pandas, scipy, scikit-learn, plotly, streamlit) dentro de un entorno virtual con dependencias fijadas en `requirements.txt`.

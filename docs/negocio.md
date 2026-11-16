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
| 2026-11-15 | Fase 1: inventario y selección | `docs/tecnico.md`, `.docx` y `.pdf` (matriz, justificación, perfil y diccionario de variables); `notebooks/00_perfil_aceptados.ipynb`; `docs/diccionario_variables.csv`; estructura de carpetas, `requirements.txt`, `.gitignore`, `README.md`; repositorio Git con un commit por etapa | Concluido |
| 2026-11-15 | Fase 2: problemática y solución propuesta | Sección 9 de este documento: árbol de problemas, diseño del tablero, cinco KPI con su cálculo, matriz KPI–hipótesis–audiencia y riesgos | Concluido |
| 2026-11-15 | Fase 3: limpieza individual | `notebooks/01_limpieza.ipynb` (ejecutado sin errores, con bitácora de 15 decisiones); `src/limpieza.py` y `src/codificacion.py`; conjuntos `_clean` en `data/processed/` (seudonimizados, fuera de Git); `docs/variables_codificadas.csv`; sección 4 de `docs/tecnico.md` | Concluido |

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

## 9. Fase 2 — Problemática y solución propuesta

Esta sección retoma la problemática y la pregunta de investigación (secciones 2 y 4) y las convierte en una propuesta de solución: un tablero analítico y un conjunto de indicadores clave de desempeño (KPI). Para cada indicador se precisa su definición, la variable de origen y la regla de cálculo, de modo que puedan construirse sin ambigüedad después de la limpieza (Fase 3).

### 9.1 Problemática

La problemática se organiza como un **árbol de problemas**: abajo, las condiciones de contexto; en el centro, el problema; arriba, sus efectos. Cada elemento se vincula con la variable que lo mide, para que el planteamiento sea verificable con los datos disponibles.

| Nivel | Elemento | Variable que lo mide |
|-------|----------|----------------------|
| Contexto | Carga académica del semestre terminal | Población de 7.º semestre (`b_semestre`); motivos para usar IA (`ia_motivo`) |
| Contexto | Traslados largos | Tiempo de traslado (`b_traslado_min`) y su impacto en el ánimo (`b_traslado_impacto`) |
| Contexto | Uso extendido de herramientas de IA | Horas diarias (`ia_horas_dia`), semestre de inicio (`ia_semestre_inicio`) |
| Efecto | Estrés y malestar emocional | Desánimo (`b_desanimo`), irritabilidad (`b_irritabilidad`), efecto de la IA en el estrés (`ia_estres`) |
| Efecto | Alteraciones del sueño y de la concentración | `b_sueno_calidad`, `b_concentracion_dif` |
| **Problema central** | La música forma parte de la rutina diaria, pero no se sabe qué hábitos de escucha acompañan un mejor estado de ánimo ni cómo se relacionan con el estrés y el uso de IA | Hábitos musicales (`m_*`) y cambio de ánimo percibido (`m_animo_antes_despues`) |

El árbol describe **relaciones que se exploran**, no cadenas causales demostradas. Con datos transversales y auto-reportados solo es posible identificar asociaciones.

### 9.2 Pregunta e hipótesis

La pregunta de investigación y las hipótesis operacionales H1 a H4 se mantienen como se definieron en la sección 4. Cada indicador de la sección 9.4 se asocia con al menos una de ellas, de modo que el tablero muestra de forma directa la evidencia que se usa para evaluarlas.

### 9.3 Solución propuesta: tablero analítico

**Descripción.** Una aplicación web interactiva en Streamlit (`app/app.py`), con gráficas de Plotly, que presenta los indicadores clave y permite filtrar a los estudiantes según sus hábitos musicales, su nivel de estrés y su uso de IA. El tablero se alimenta del conjunto integrado y anonimizado que se generará en la Fase 4 (`data/processed/`) y no muestra respuestas individuales ni identificadores.

**Preguntas que debe responder cada audiencia:**

| Audiencia | Pregunta guía | Vista del tablero |
|-----------|---------------|-------------------|
| Estudiantes | ¿Qué hábitos de escucha reportan quienes dicen sentirse mejor con la música? | Resumen de KPI; géneros y momentos de escucha |
| Tutores | ¿Qué perfiles concentran más indicadores de estrés o desánimo? | Estrés por perfil de hábitos; perfiles del agrupamiento (Fase 5) |
| Coordinación de MAC | ¿Cómo se relaciona el uso de IA con el bienestar del grupo? | Uso de IA por perfil de bienestar |

**Estructura propuesta:**

1. **Resumen.** Tarjetas con los cinco KPI y el tamaño de la muestra filtrada.
2. **Hábitos musicales.** Géneros predominantes, distribución de horas de escucha, momentos y plataformas.
3. **Música y bienestar.** Porcentaje de mejora de ánimo por género y por momento de escucha; índice de estrés por perfil de hábitos.
4. **Uso de IA.** Horas de IA y modalidad de uso (guía, atajo o ambas) por perfil de bienestar.
5. **Perfiles.** Resultado del agrupamiento de la Fase 5 en el plano de componentes principales.
6. **Notas metodológicas.** Tamaño muestral, carácter auto-reportado de los datos y advertencia de no causalidad.

**Filtros:**

| Filtro | Variable | Observación |
|--------|----------|-------------|
| Género musical | Grupo de `m_genero_frecuente` | El género de la persona no se incluye: solo existe en un documento rechazado |
| Semestre | `b_semestre` | Hoy tiene un solo valor (7.º). Se conserva para cuando se agreguen otros semestres |
| Horas de escucha | `m_horas_dia` (control deslizante) | — |
| Nivel de estrés | Nivel del índice de estrés percibido (bajo, medio, alto) | Ver KPI 4 |
| Uso de IA | Modalidad (`ia_guia_vs_atajo`) | Filtro adicional al solicitado; sirve a H4 |

**Protección contra la reidentificación.** Con 19 estudiantes, una combinación de filtros podría aislar a una sola persona. Por eso, cuando la selección tenga **menos de 3 estudiantes**, el tablero ocultará los indicadores y lo indicará con un aviso.

**Alternativa descartada.** Se consideró entregar los resultados solo como un reporte estático en PDF. Se prefirió el tablero porque permite a cada audiencia explorar el subgrupo que le interesa. Aun así, el documento técnico conservará las tablas y figuras principales para quien no use la aplicación.

### 9.4 Indicadores clave (KPI)

Para que todos los KPI se calculen igual, primero se definen dos constructos derivados:

- **Índice de estrés percibido (IEP).** Promedio de `b_desanimo` y `b_irritabilidad`, ambas codificadas de 0 (nunca) a 4 (muy frecuentemente). El IEP va de 0 a 4. Se clasifica como **bajo** (< 1.5), **medio** (1.5 a 2.5) o **alto** (> 2.5). Es un indicador **indirecto**: los cuestionarios no incluyen un instrumento validado de estrés.
- **Perfil de hábitos musicales.** Se usarán los grupos del agrupamiento de la Fase 5. Mientras no estén disponibles, o si no resultan interpretables, se usará un perfil por intensidad de escucha: **baja** (< 2 h/día), **media** (2 a 4 h/día) o **alta** (> 4 h/día).

| # | KPI | Definición y cálculo | Variables (documento) | Desagregación | Visualización | Hipótesis |
|---|-----|----------------------|-----------------------|---------------|---------------|-----------|
| 1 | **% de estudiantes que reportan mejora de ánimo con música** | Estudiantes con `mejora_animo = 1` ÷ estudiantes con respuesta válida × 100 | `m_animo_antes_despues` → `mejora_animo` (Doc 1) | Por género musical, momento de escucha y nivel de IEP | Tarjeta y barras | H1, H3, H4 |
| 2 | **Horas promedio de escucha por perfil** | Media y mediana de `m_horas_dia` en cada perfil de hábitos o de bienestar | `m_horas_dia` (Doc 1) | Por perfil, nivel de IEP y mejora de ánimo | Tarjeta y diagrama de caja | H2 |
| 3 | **Géneros más asociados a bienestar** | Para cada grupo de géneros con al menos 3 estudiantes: % con mejora de ánimo y IEP medio. Se ordenan por % de mejora | `m_genero_frecuente`, `m_generos_emocion` (Doc 1); IEP (Doc 2) | Por grupo de género | Barras ordenadas | H3 |
| 4 | **Nivel de estrés por perfil de hábitos musicales** | Media del IEP y distribución de sus niveles en cada perfil de hábitos | IEP (Doc 2); perfil (Doc 1) | Por perfil y momento de escucha | Barras apiladas | H1, H2 |
| 5 | **Uso de IA por perfil de bienestar** | Media de `ia_horas_dia` y % de uso como guía, atajo o ambas en cada nivel de IEP | `ia_horas_dia`, `ia_guia_vs_atajo`, `ia_estres` (Doc 3); IEP (Doc 2) | Por nivel de IEP y mejora de ánimo | Barras agrupadas | H4 |

**Reglas comunes:**

- Cada KPI se calcula con los estudiantes que tienen datos en todos los documentos que usa. Los KPI 1 y 2 usan solo el Documento 1 (hasta 24 casos con la cuenta válida). Los KPI 3, 4 y 5 usan el núcleo integrado de 19 estudiantes. El tablero mostrará siempre el *n* de cada indicador.
- Los porcentajes se acompañan del conteo absoluto, con el formato "X % (k de n)". Con muestras tan pequeñas, un solo estudiante puede mover el porcentaje más de 5 puntos.
- No se reportan categorías con menos de 3 estudiantes; se agrupan como "otros".
- Si una respuesta no puede codificarse con las reglas de la Fase 3, se trata como faltante y se excluye del KPI correspondiente. Nunca se imputa un valor para un indicador.

### 9.5 Relación entre indicadores, hipótesis y audiencias

| KPI | H1 | H2 | H3 | H4 | Estudiantes | Tutores | Coordinación |
|-----|:--:|:--:|:--:|:--:|:-----------:|:-------:|:------------:|
| 1. % mejora de ánimo | ✓ | | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2. Horas por perfil | | ✓ | | | ✓ | ✓ | |
| 3. Géneros y bienestar | | | ✓ | | ✓ | | |
| 4. Estrés por perfil | ✓ | ✓ | | | | ✓ | ✓ |
| 5. IA por bienestar | | | | ✓ | | ✓ | ✓ |

Las cuatro hipótesis y las tres audiencias quedan cubiertas por al menos un indicador.

### 9.6 Riesgos de la solución

| Riesgo | Efecto | Mitigación |
|--------|--------|------------|
| Poca variabilidad en la mejora de ánimo (casi todos reportan mejora) | KPI 1 poco informativo; modelo supervisado inviable | Se reporta el resultado tal cual; el análisis se apoya en el IEP y en el agrupamiento |
| Codificación ambigua del texto libre | Clasificación inconsistente de géneros, momentos u horas | Reglas explícitas en la Fase 3, revisión manual de casos dudosos y bitácora de decisiones |
| Muestra pequeña | Indicadores inestables y riesgo de reidentificación | Mostrar siempre *n*, umbral mínimo de 3 estudiantes por categoría y por filtro |
| El IEP no es un instrumento validado | Se podría sobreinterpretar como medida clínica de estrés | Etiquetarlo como "indicador indirecto" en el tablero y en los documentos |

### 9.7 Criterio de aceptación de la fase

- [x] Problemática redactada y vinculada con variables medibles (9.1).
- [x] Pregunta e hipótesis enlazadas con los indicadores (9.2 y 9.5).
- [x] Solución descrita: audiencias, vistas, filtros y protección de datos (9.3).
- [x] Cinco KPI definidos con fórmula, fuente, desagregación y visualización (9.4).

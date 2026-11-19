---
title: "Documento de negocio"
subtitle: "Hábitos musicales, estado de ánimo, estrés académico y uso de IA en estudiantes de MAC, FES Acatlán"
lang: es-MX
---

## Registro de avances

| Fecha | Etapa | Entregables | Estado |
|-------|-------|-------------|--------|
| 2026-11-15 | Momento A: análisis y selección de documentos | Sección 1 de este documento; `notebooks/00_analisis_documentos.ipynb`; `src/analisis_documentos.py`; `docs/matriz_relacion.csv` | Concluido |
| 2026-11-15 | Momento A, ajuste de formato | Redacción en tono académico; versión en notebook ejecutado sin errores; exportación a Word y PDF con `src/exportar_docs.py` | Concluido |
| 2026-11-15 | Fase 0: definición del proyecto | Este documento (secciones 1 a 8), en `.md`, `.docx` y `.pdf` | Concluido |
| 2026-11-15 | Fase 1: inventario y selección | `docs/tecnico.md`, `.docx` y `.pdf` (matriz, justificación, perfil y diccionario de variables); `notebooks/00_perfil_aceptados.ipynb`; `docs/diccionario_variables.csv`; estructura de carpetas, `requirements.txt`, `.gitignore`, `README.md`; repositorio Git con un commit por etapa | Concluido |
| 2026-11-15 | Fase 2: problemática y solución propuesta | Sección 9 de este documento: árbol de problemas, diseño del tablero, cinco KPI con su cálculo, matriz KPI–hipótesis–audiencia y riesgos | Concluido |
| 2026-11-15 | Fase 3: limpieza individual | `notebooks/01_limpieza.ipynb` (ejecutado sin errores, con bitácora de 15 decisiones); `src/limpieza.py` y `src/codificacion.py`; conjuntos `_clean` en `data/processed/` (seudonimizados, fuera de Git); `docs/variables_codificadas.csv`; sección 4 de `docs/tecnico.md` | Concluido |
| 2026-11-15 | Fase 4: integración y EDA | `notebooks/02_eda.ipynb` (ejecutado sin errores); conjuntos integrados (n = 19 y n = 24) en `data/processed/`; 23 pruebas de hipótesis con corrección de Benjamini-Hochberg (`docs/pruebas_hipotesis.csv`); 9 figuras en `docs/figuras/`; KPI preliminares; sección 5 de `docs/tecnico.md` | Concluido |
| 2026-11-15 | Fase 5: modelado | `notebooks/03_modelado.ipynb` (ejecutado sin errores); 3 perfiles por K-Means (silueta 0.28) contrastados con Ward, DBSCAN, bootstrap y sensibilidad; modelo supervisado descartado con justificación; `data/processed/perfiles.csv`; 4 figuras; sección 6 de `docs/tecnico.md` | Concluido |
| 2026-11-15 | Fase 6: tablero analítico | `app/app.py` (Streamlit + Plotly) con los 5 KPI, filtros por género, semestre, horas, estrés y uso de IA, 6 vistas y umbral de anonimato de 3 estudiantes; `src/tablero.py`; probado con `AppTest` y en el navegador; sección 7 de `docs/tecnico.md` | Concluido |
| 2026-11-15 | Fase 7: documentación y Git | Análisis de texto con NLTK y figura con seaborn; conclusiones, criterios de éxito y reproducibilidad (`docs/tecnico.md` §8 y §9); resultados y recomendaciones (sección 10); README final; re-ejecución completa del pipeline; documentos en `.md`, `.docx` y `.pdf`; repositorio con un commit por etapa | Concluido |
| 2026-11-15 | Ajuste: clasificaciones en el tablero | Artistas (NLTK), plataformas, características de una canción, géneros por emoción, y fases y motivos de uso de IA en `app/app.py` y `src/tablero.py`; documentado en `docs/tecnico.md` §7 | Concluido |
| 2026-11-15 | Ajuste: publicación del tablero | Carga de datos desde un secreto de Streamlit (`src/preparar_despliegue.py`), `app/requirements.txt` ligero e instrucciones de despliegue en Streamlit Community Cloud (README y `docs/tecnico.md` §7.5); los datos siguen fuera del repositorio | Concluido |
| 2026-11-18 | Momento A: replanteamiento e integración | El Momento A se replantea desde cero (de los datos a la pregunta: inventario, población común, mapa de temas y primeras señales) y se integra como sección 1 de este documento. El notebook pasa a `00_analisis_documentos.ipynb` y el módulo a `src/analisis_documentos.py`; se eliminan los archivos `docs/momento_A.*`. La carpeta `docs/` deja de subirse a Git, salvo las figuras | Concluido |

## 1. Antecedentes: Momento A — de los datos a la pregunta de investigación

### 1.1 Punto de inicio

El proyecto no partió de una pregunta definida, sino de un conjunto de datos: **seis cuestionarios** recolectados con Google Forms entre septiembre y noviembre de 2026. El Momento A responde, en este orden:

1. ¿Qué contiene cada cuestionario y quién lo respondió?
2. ¿Qué tema pueden sostener los datos, es decir, qué se mide en más de un cuestionario y para las mismas personas?
3. Una vez definido el tema, ¿qué cuestionarios sirven para estudiarlo y cuáles no?

El análisis se reproduce en `notebooks/00_analisis_documentos.ipynb`, con las funciones de `src/analisis_documentos.py`. Ningún resultado muestra números de cuenta ni correos.

### 1.2 Qué contiene cada cuestionario

| # | Cuestionario | Respuestas | Preguntas | Periodo | Llave | Tema |
|---|--------------|-----------:|----------:|---------|-------|------|
| 1 | La música y su influencia en el estado de ánimo | 24 | 16 | 29 oct – 11 nov | Número de cuenta | Hábitos musicales y su efecto en el ánimo, la energía, la concentración y el sueño |
| 2 | Entorno Universitario y Bienestar | 19 | 15 | 1 – 3 nov | Número de cuenta | Sueño, desánimo, irritabilidad, concentración, apoyo social y traslados |
| 3 | Desempeño académico por el uso de IA | 24 | 16 | 30 oct – 11 nov | Número de cuenta | Uso académico de la IA y su efecto en el estrés |
| 4 | Test | 25 | 15 | 4 sep – 11 nov | Correo y número de cuenta | Personalidad, pasatiempos y toma de decisiones |
| 5 | Pelis y series | 21 | 15 | 30 oct – 4 nov | Número de cuenta | Gustos de cine y series |
| 6 | Relación Amor – Carrera | 21 | 19 | 12 oct – 13 nov | Solo correo | Concepciones sobre la pareja |

Casi todas las preguntas son abiertas: los estudiantes respondieron con sus propias palabras, incluso cuando se preguntaban horas o edades.

### 1.3 Quién los respondió

| | Doc 1 | Doc 2 | Doc 3 | Doc 4 | Doc 5 | Doc 6 |
|---|---:|---:|---:|---:|---:|---:|
| **Doc 1** | 24 | 19 | 23 | 23 | 21 | 20 |
| **Doc 2** | 19 | 19 | 19 | 19 | 19 | 19 |
| **Doc 3** | 23 | 19 | 24 | 24 | 21 | 20 |

*Estudiantes en común entre pares de documentos (extracto).*

En total participaron 26 estudiantes distintos, y los seis cuestionarios los respondió **prácticamente el mismo grupo**. Los que preguntan carrera y semestre lo confirman: todos cursan **7.º semestre**, y 18 de 19 escribieron explícitamente Matemáticas Aplicadas y Computación. Esto es clave: como son las mismas personas, los temas de distintos cuestionarios **se pueden cruzar**, que es la condición para estudiar relaciones entre ellos.

### 1.4 Qué temas sostienen los datos

Se clasificaron los enunciados de todas las preguntas por tema, buscando palabras clave en texto sin acentos. Una pregunta puede tocar más de un tema:

| Tema | Doc 1 | Doc 2 | Doc 3 | Doc 4 | Doc 5 | Doc 6 |
|------|------:|------:|------:|------:|------:|------:|
| Música | **16** | 0 | 0 | 0 | 0 | 1 |
| **Bienestar emocional (ánimo, estrés o sueño)** | **8** | **4** | **1** | 0 | 0 | 0 |
| Concentración y desempeño | 1 | 2 | 6 | 0 | 0 | 0 |
| Inteligencia artificial | 0 | 0 | **15** | 0 | 0 | 0 |
| Contexto (carrera, semestre, traslado) | 0 | 7 | 1 | 0 | 0 | 5 |
| Cine y series | 0 | 0 | 0 | 1 | **13** | 1 |
| Pareja | 0 | 0 | 0 | 0 | 0 | **11** |
| Personalidad y ocio | 0 | 0 | 0 | **8** | 0 | 0 |

**Lectura:**

- **Temas sin conexión.** Cine y series, pareja y personalidad se concentran cada uno en un cuestionario (5, 6 y 4) y no se conectan con ninguna medida de bienestar.
- **El eje común.** El **bienestar emocional** es lo único que une a tres cuestionarios: el efecto de la música en el ánimo y el sueño (Doc 1); el desánimo, la irritabilidad y el sueño (Doc 2), y el efecto de la IA en el estrés y la carga mental (Doc 3).
- **Dos hábitos medidos a fondo.** Los otros dos temas que se miden con detalle son hábitos cotidianos: **escuchar música** (16 preguntas en el Doc 1) y **usar IA** (15 preguntas en el Doc 3). Los dos están ligados al bienestar desde sus propias preguntas.
- **El contexto.** El Documento 2 aporta el contexto universitario: carrera, semestre, traslados y con quién viven.

El tema que los datos pueden sostener es, por lo tanto, **el bienestar emocional de los estudiantes y su relación con escuchar música y con usar IA**.

### 1.5 Primeras señales en las respuestas

Antes de limpiar los datos se hizo una lectura rápida de las respuestas abiertas, contando las que contienen ciertas palabras. Son aproximaciones; en la Fase 3 cada respuesta se codifica con reglas revisadas una por una.

| Señal | Documento | Respuestas | % |
|-------|-----------|-----------:|--:|
| Traslado de 1 hora o más | 2 | 11 de 19 | 58 |
| Desánimo frecuente | 2 | 10 de 19 | 53 |
| Problemas de sueño (malo, poco o irregular) | 2 | 12 de 19 | 63 |
| Recurre a la IA por tiempo o carga académica | 3 | 12 de 24 | 50 |
| Dice que la IA reduce su estrés | 3 | 20 de 24 | 83 |
| Escucha música a diario | 1 | 23 de 24 | 96 |
| Escucha música en el traslado | 1 | 16 de 24 | 67 |
| Describe que la música mejora su ánimo | 1 | 17 de 24 | 71 |

Las señales dibujan un grupo con **malestar frecuente** (desánimo y mal sueño), presionado por la **carga académica** y los **traslados largos**, que **usa la IA** en parte para aliviar esa carga y que **escucha música todos los días**, muchas veces durante el trayecto y para sentirse mejor. Lo que no se ha documentado es cómo se relacionan estas piezas.

### 1.6 Punto de partida del proyecto

De ese análisis surge la pregunta que guía el proyecto:

> Este proyecto busca identificar qué hábitos musicales se asocian con un mejor estado de ánimo reportado en estudiantes de Matemáticas Aplicadas y Computación (MAC) de la FES Acatlán, UNAM, y cómo se relacionan con su nivel de estrés académico y su uso de herramientas de inteligencia artificial (IA). Hay seis cuestionarios disponibles, recolectados con Google Forms entre septiembre y noviembre de 2026. Antes de limpiar o modelar cualquier dato hace falta decidir cuáles son pertinentes para la pregunta de investigación. Este documento presenta ese análisis previo, denominado Momento A. Describe cada fuente, evalúa su relación con la pregunta y justifica qué documentos se integran al estudio y cuáles se descartan.

**Por qué esta pregunta y no otra.** Es la única que cumple tres condiciones a la vez:

1. **Se puede medir:** la música y la IA tienen cuestionarios completos, y el bienestar se mide en tres de ellos.
2. **Se puede cruzar:** los mismos estudiantes respondieron los cuestionarios necesarios.
3. **Es relevante para el grupo:** las primeras señales muestran malestar, carga académica y traslados largos, y la música y la IA aparecen como formas cotidianas de sobrellevarlos.

Una pregunta sobre cine, pareja o personalidad no podría vincularse con el bienestar, porque esos cuestionarios no lo miden.

### 1.7 Selección de los documentos

Con la pregunta definida, un documento se **acepta** si cumple dos condiciones:

1. Contiene variables de la pregunta: música, estado de ánimo, estrés, sueño, concentración o uso de IA.
2. Comparte la llave *número de cuenta* con los demás.

Se **rechaza** si no aporta variables de la pregunta, si su llave es incompatible o si solo añadiría ruido. Como todos comparten estudiantes (sección 1.3), la llave no descarta a ninguno y la decisión depende del tema.

| Documento | ¿Relación con música, ánimo, estrés o IA? | Preguntas del tema | Llave compatible | Veredicto |
|-----------|-------------------------------------------|-------------------:|------------------|-----------|
| 1. Música y ánimo | Sí, directa | 26 | Sí | **Aceptar (principal)** |
| 2. Entorno universitario y bienestar | Sí: ánimo, sueño, concentración y estrés indirecto | 6 | Sí | **Aceptar (complementario fuerte)** |
| 3. Desempeño por uso de IA | Sí: IA y estrés académico | 22 | Sí | **Aceptar (complementario medio)** |
| 4. Test | Marginal | 0 | Sí, con un duplicado | **Rechazar** |
| 5. Pelis y series | No | 0 | Sí | **Rechazar** |
| 6. Relación amor–carrera | No | 1 | Solo derivada del correo | **Rechazar** |

La matriz completa, con temas y variables clave, está en `docs/matriz_relacion.csv`.

**Por qué se aceptan:**

- **Documento 1 (principal).** Es el único que mide la variable central, los hábitos musicales (género, horas, momentos y plataforma), junto con el cambio de ánimo atribuido a la música.
- **Documento 2 (complementario fuerte).** Mide el bienestar directamente (desánimo, irritabilidad, sueño y concentración) sin hacer referencia a la música. Eso permite contrastar el ánimo atribuido a la música con el ánimo general reportado. Además aporta el contexto: semestre, edad y traslados.
- **Documento 3 (complementario medio).** Aporta la variable moderadora, el uso de IA (horas y modalidad), y un indicador de estrés académico.

**Por qué se descartan:**

- **Documento 4 (Test).** Describe personalidad y preferencias; no mide ánimo, estrés, sueño ni IA, y contiene un registro duplicado.
- **Documento 5 (Pelis y series).** Trata del consumo audiovisual, un tema ajeno a la pregunta.
- **Documento 6 (Relación amor–carrera).** Trata de concepciones sobre la pareja, que no equivalen al estado de ánimo. Además, su llave solo existe dentro del correo, un dato personal adicional.

Integrarlos no aumentaría la muestra (seguiría en 19 estudiantes) y sí agregaría unas cincuenta variables de texto sin relación con la pregunta.

### 1.8 Consideraciones para las fases siguientes

1. **Tamaño muestral.** El núcleo que respondió los tres documentos aceptados es de **19 estudiantes**, así que los resultados serán exploratorios.
2. **Medición del estrés.** Ningún cuestionario tiene una escala de estrés. Se usarán indicadores indirectos: desánimo, irritabilidad, efecto percibido de la IA en la carga mental y música escuchada en momentos de estrés.
3. **Variables constantes.** Todos cursan 7.º semestre, y el "género" del tablero se interpretará como género musical, porque el sexo solo aparece en el Documento 4, que se rechazó.
4. **Calidad de los datos.** Hay una cuenta de 10 dígitos en el Documento 1, un duplicado en el 4 y un participante sin respuestas en el 6. Se atienden en la Fase 3.
5. **Datos observacionales.** Las respuestas son auto-reportadas, así que los hallazgos describirán asociaciones, no causas.

En la sección 4 la pregunta se **operacionaliza** con las variables que existen en los datos.

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

*Ampliación posterior:* el resumen, la vista de hábitos y la de IA incluyen **clasificaciones complementarias**: artistas más mencionados, plataformas, características de una canción que influyen en las emociones, géneros asociados a emociones, y fases y motivos de uso de la IA. Solo se muestran opciones mencionadas por al menos 2 estudiantes de la selección.
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

## 10. Resultados y recomendaciones

Esta sección resume, para las partes interesadas, lo que el proyecto encontró y cómo puede usarse. El detalle metodológico está en `docs/tecnico.pdf` y los datos pueden explorarse en el tablero (`streamlit run app/app.py`).

### 10.1 Respuesta a la pregunta

> ¿Qué hábitos musicales se asocian con un mejor estado de ánimo reportado en estudiantes de MAC, y cómo se relacionan con su nivel de estrés académico y su uso de IA?

- **La música se percibe como un apoyo inmediato.** El 85 % de los estudiantes reporta que la música mejora su ánimo, y quienes lo reportan escuchan más horas al día. La escuchan sobre todo en los **traslados** (75 %), al estudiar y al hacer ejercicio. **No apareció un género ni un momento** de escucha que se asocie con más bienestar.
- **Ese apoyo no se refleja en el estrés general.** Los indicadores de bienestar (desánimo, irritabilidad, sueño) no varían con los hábitos musicales. La música parece ayudar en el momento, no cambiar el estado de ánimo de fondo.
- **En la IA importa más el cómo que el cuánto.** Quienes usan la IA **como guía para aprender** reportan menos estrés que quienes la usan también o solo como atajo. Las horas de uso no marcan diferencia.
- **El contexto pesa.** Los traslados más largos se asocian con peor calidad de sueño, y el 78 % del grupo muestra un nivel de estrés percibido medio o alto.

Son **asociaciones exploratorias**. Con alrededor de 19 estudiantes, ninguna se confirma estadísticamente tras corregir por comparaciones múltiples, y los datos no permiten afirmar que un hábito *cause* un cambio en el ánimo o el estrés.

### 10.2 Indicadores clave (valores finales)

| KPI | Valor |
|-----|-------|
| 1. % que reporta mejora de ánimo con música | **85 %** (17 de 20) |
| 2. Horas de escucha por perfil (mediana) | Escucha intensiva 5 h · Estrés alto 2.25 h · IA como guía 1.5 h |
| 3. Géneros más asociados a bienestar | Sin diferencias significativas; urbano 100 % (n = 3), pop 83 % (n = 6), rock/metal 67 % (n = 4) de mejora en el núcleo |
| 4. Estrés por perfil de hábitos (IEP medio) | Estrés alto 3.25 · Escucha intensiva 2.4 · IA como guía 1.5 |
| 5. Uso de IA como guía por nivel de estrés | Bajo 75 % · Medio 22 % · Alto 0 % |

### 10.3 Perfiles de estudiantes

| Perfil | Rasgos | Qué sugiere |
|--------|--------|-------------|
| **Escucha intensiva** (6) | Mucha música; la percibe útil para concentrarse; traslados largos | La música acompaña trayectos largos; el estrés es medio |
| **Estrés alto** (6) | Estrés alto; la música lo distrae al estudiar; solo la mitad siente mejora con música | Grupo prioritario para acompañamiento |
| **IA como guía, estrés bajo** (5) | Usa la IA para aprender; poco tiempo de IA y de música | Patrón de uso de IA asociado con bienestar |

Los perfiles son una guía descriptiva: con otros datos podrían reorganizarse.

### 10.4 Recomendaciones

Las recomendaciones se derivan de asociaciones, por lo que se proponen como **acciones de bajo costo para probar y evaluar**, no como intervenciones de efecto comprobado.

**Para estudiantes:**

- Usar la música de forma intencional donde la reportan útil sus compañeros (traslados, ejercicio, tareas sencillas). Si les distrae al estudiar, como reporta el perfil de estrés alto, conviene probar el silencio en tareas de alta concentración.
- Usar la IA como guía para comprender (pedir explicaciones y verificar con otras fuentes) en lugar de solo como atajo para terminar.

**Para tutores:**

- Prestar atención a señales del perfil de estrés alto: desánimo frecuente, irritabilidad y dificultad para concentrarse.
- Usar el tablero como apoyo para conversar sobre hábitos de estudio, no como diagnóstico.

**Para la coordinación de MAC:**

- Considerar talleres breves sobre el **uso de la IA como herramienta de aprendizaje** (cómo preguntar, verificar y comprender), dado que esa modalidad se asocia con menos estrés.
- Tener en cuenta el peso de los traslados en el sueño al planear horarios y actividades.
- Para medir el efecto de cualquier acción, repetir el levantamiento con preguntas cerradas e instrumentos validados (por ejemplo, la Escala de Estrés Percibido), con más estudiantes y en más de un momento del semestre.

### 10.5 Criterios de éxito

Los criterios de éxito de la sección 7 se cumplieron:

- datos integrados con pérdidas reportadas;
- variables codificadas con reglas documentadas y sin imputación;
- hipótesis evaluadas con efecto y corrección por comparaciones múltiples;
- perfiles con silueta de 0.28;
- modelo supervisado evaluado y descartado con justificación;
- tablero funcional;
- documentación completa en tres formatos.

El estado de cada criterio se detalla en `docs/tecnico.md` §8.

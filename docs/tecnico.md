---
title: "Documento técnico"
subtitle: "Hábitos musicales, estado de ánimo, estrés académico y uso de IA en estudiantes de MAC, FES Acatlán"
lang: es-MX
---

## 1. Introducción

Este documento registra las decisiones metodológicas y los resultados técnicos del proyecto. La definición del problema, los objetivos, las hipótesis y los criterios de éxito están en el documento de negocio (`docs/negocio.md`). Este documento se complementa fase por fase. La versión actual cubre la **Fase 1: inventario y selección de fuentes**, que consolida el Momento A, y la **Fase 3: limpieza individual**.

## 2. Entorno de trabajo y organización del proyecto

### 2.1 Estructura de carpetas

| Carpeta o archivo | Contenido |
|-------------------|-----------|
| `data/raw/` | Los tres documentos aceptados, en su forma original. No se versiona. |
| `data/excluded/` | Los tres documentos rechazados en el Momento A. Se conservan pero no se usan. No se versiona. |
| `data/processed/` | Conjuntos limpios e integrados (Fases 3 y 4). No se versiona. |
| `notebooks/` | `00_momento_A`, `00_perfil_aceptados`, `01_limpieza`; después `02_eda`, `03_modelado`. |
| `src/` | Código reutilizable: `datos.py` (rutas, carga y perfilado), `diccionario.py` (diccionario de variables), `limpieza.py` y `codificacion.py` (limpieza y reglas de codificación), `anexos.py`, `momento_a.py`, `exportar_docs.py`. |
| `app/` | Tablero en Streamlit (Fase 6). |
| `docs/` | Documentos técnico y de negocio en `.md`, `.docx` y `.pdf`; matriz de relación y diccionario de variables en `.csv`. |

### 2.2 Reproducibilidad

El análisis se hace en Python 3.14 dentro de un entorno virtual (`.venv`), con versiones fijadas en `requirements.txt`. Las semillas aleatorias se fijan con `numpy.random.seed(42)`. Los cuadernos se ejecutan completos, sin errores, antes de cada entrega. Los documentos se convierten a Word y PDF con `src/exportar_docs.py`, que usa pandoc. Como el equipo de desarrollo no tiene un motor LaTeX, el PDF se obtiene imprimiendo el HTML generado por pandoc con Microsoft Edge en modo *headless*; si `xelatex` está disponible, el script lo usa automáticamente.

### 2.3 Protección de datos personales

Los cuestionarios contienen números de cuenta y, en algunos casos, correos institucionales. Para protegerlos se tomaron tres medidas:

1. La carpeta `data/` está excluida de Git (`.gitignore`), así que ningún dato crudo o procesado se publica.
2. Los cuadernos solo muestran conteos y estadísticos agregados. Antes de cada commit se verifica que no contengan secuencias de 9 o 10 dígitos.
3. Desde la Fase 3, el número de cuenta se reemplaza por un seudónimo (HMAC-SHA256 con clave secreta en `data/raw/`) antes de guardar los conjuntos procesados.

## 3. Fase 1 — Inventario y selección de fuentes

### 3.1 Inventario inicial

Se recibieron seis cuestionarios aplicados con Google Forms a estudiantes de MAC. El análisis completo de los seis está en `docs/momento_A.pdf` (cuaderno `00_momento_A.ipynb`).

| # | Documento | Registros × variables | Llave | Tema central |
|---|-----------|----------------------|-------|--------------|
| 1 | La música y su influencia en el estado de ánimo | 24 × 18 | Número de cuenta | Hábitos musicales y efecto percibido en el ánimo |
| 2 | Entorno Universitario y Bienestar | 19 × 17 | Número de cuenta | Bienestar: sueño, desánimo, irritabilidad, concentración |
| 3 | Desempeño académico por el uso de IA | 24 × 18 | Número de cuenta | Uso académico de la IA y su efecto en el estrés |
| 4 | Test | 25 × 18 | Correo y número de cuenta | Personalidad y preferencias |
| 5 | Pelis y series | 21 × 17 | Número de cuenta | Preferencias audiovisuales |
| 6 | Relación Amor – Carrera | 21 × 21 | Solo correo | Concepciones de pareja |

### 3.2 Criterios y matriz de relación

Un documento se acepta si contiene variables relacionadas con la pregunta de investigación (música, ánimo, estrés, sueño, concentración o IA) y comparte la llave *número de cuenta* con los demás aceptados. Se rechaza si no cumple el primer criterio, si su llave es incompatible o si su inclusión aporta ruido sin señal.

Los seis cuestionarios fueron respondidos prácticamente por el mismo grupo, así que la llave resultó compatible en todos. La decisión dependió entonces de la pertinencia temática. Para evaluarla de forma verificable, se normalizaron los enunciados de las preguntas y se contaron los que aluden a los constructos de la investigación: 26 en el Documento 1, 16 en el 3, 5 en el 2, 1 en el 6 y ninguno en el 4 ni en el 5.

| Documento | ¿Relación con música, ánimo, estrés o IA? | Llave compatible | Veredicto |
|-----------|------------------------------------------|------------------|-----------|
| 1. Música y ánimo | Sí, directa | Sí | **Aceptar (principal)** |
| 2. Entorno universitario y bienestar | Sí: ánimo, sueño, concentración y estrés indirecto | Sí | **Aceptar (complementario fuerte)** |
| 3. Desempeño por uso de IA | Sí: IA y estrés académico | Sí | **Aceptar (complementario medio)** |
| 4. Test | Marginal | Sí, con un duplicado | **Rechazar** |
| 5. Pelis y series | No | Sí | **Rechazar** |
| 6. Relación amor–carrera | No | Solo derivada del correo | **Rechazar** |

La matriz completa, con temas y variables clave, está en `docs/matriz_relacion.csv`.

### 3.3 Justificación

La pregunta de investigación tiene tres componentes: hábitos musicales y ánimo, estrés y sueño, y uso de IA. El Documento 1 es el único que mide la variable central (los hábitos musicales) y el cambio de ánimo atribuido a la música. El Documento 2 mide el bienestar sin hacer referencia a la música, lo que permite contrastar dos fuentes de auto-reporte. El Documento 3 aporta la variable moderadora. Los documentos rechazados no cubren ninguno de los tres componentes. Integrarlos no aumentaría la muestra, que seguiría siendo de 19 registros, y sí agregaría unas cincuenta variables de texto sin relación con la pregunta.

### 3.4 Perfil de los documentos aceptados

Los tres documentos aceptados se trasladaron a `data/raw/` sin modificaciones y se perfilaron con `pandas` (cuaderno `00_perfil_aceptados.ipynb`).

| Indicador | Doc 1. Música | Doc 2. Bienestar | Doc 3. IA |
|-----------|-------------:|-----------------:|----------:|
| Registros | 24 | 19 | 24 |
| Variables | 18 | 17 | 18 |
| Variables de contenido (sin fecha ni cuenta) | 16 | 15 | 16 |
| Variables de contenido con más de 80 % de valores únicos | 16 | 11 | 16 |
| Longitud media de respuesta (palabras) | 10.0 | 4.6 | 11.3 |
| Celdas vacías | 1 | 0 | 2 |
| Filas duplicadas | 0 | 0 | 0 |
| Cuentas duplicadas | 0 | 0 | 0 |
| Cuentas con longitud distinta de 9 dígitos | 1 | 0 | 0 |
| Periodo de recolección | 29 oct – 11 nov 2026 | 1 – 3 nov 2026 | 30 oct – 11 nov 2026 |
| Estudiantes en el núcleo 1 ∩ 2 ∩ 3 | 19 | 19 | 19 |

Los datos tienen buena integridad estructural: no hay duplicados y los faltantes son mínimos (tres celdas en total). La dificultad principal está en la **forma de las respuestas**: 43 de las 47 variables de contenido tienen una redacción distinta en más del 80 % de los casos. Incluso las variables conceptualmente numéricas, como las horas de escucha, las horas de uso de IA, la edad o el tiempo de traslado, se capturaron como texto. El Documento 2 tiene respuestas más breves (4.6 palabras en promedio), lo que facilitará codificarlo en escalas ordinales.

La integración por intersección conservará 19 estudiantes. Se perderán 5 registros del Documento 1 y 5 del Documento 3, todos por no haber respondido el Documento 2; uno de los del Documento 1 es, además, el de la cuenta con formato inválido. Los Documentos 1 y 3 comparten 23 estudiantes, por lo que los análisis que solo involucren música e IA podrán usar una muestra mayor.

### 3.5 Diccionario de variables

A cada columna se le asignó un nombre corto con prefijo por documento (`m_` música, `b_` bienestar, `ia_` inteligencia artificial), una forma de respuesta, una codificación prevista para la Fase 3 y un uso analítico. El renombrado se aplica por posición y la función de carga (`src/datos.py::cargar`) verifica que el número de columnas coincida con el diccionario, para evitar asignaciones silenciosas incorrectas.

| Forma de respuesta | Doc 1 | Doc 2 | Doc 3 | Total |
|--------------------|------:|------:|------:|------:|
| Texto libre | 6 | 1 | 9 | 16 |
| Ordinal en texto | 4 | 7 | 0 | 11 |
| Numérica en texto | 1 | 3 | 2 | 6 |
| Multirrespuesta en texto | 3 | 0 | 2 | 5 |
| Categórica en texto | 0 | 2 | 1 | 3 |
| Sí/No con explicación | 1 | 0 | 2 | 3 |
| Likert en texto | 0 | 2 | 0 | 2 |
| Lista en texto | 1 | 0 | 0 | 1 |
| **Total** | **16** | **15** | **16** | **47** |

Las hipótesis quedan operacionalizadas con las siguientes variables:

| Hipótesis | Variables |
|-----------|-----------|
| H1. Mejora de ánimo con música y menor desánimo e irritabilidad | `m_animo_antes_despues`, `m_maneja_emociones`, `b_desanimo`, `b_irritabilidad` |
| H2. Horas y momentos de escucha frente a ánimo, concentración y sueño | `m_horas_dia`, `m_momentos`, `m_energia`, `m_concentracion`, `m_sueno`, `b_sueno_calidad`, `b_concentracion_dif` |
| H3. Géneros musicales y estados positivos | `m_genero_frecuente`, `m_generos_emocion` |
| H4. Moderación por uso de IA | `m_animo_antes_despues`, `ia_horas_dia`, `ia_guia_vs_atajo`, `ia_estres`, `ia_independencia` |

Cuatro variables de texto libre sin papel en las hipótesis no se codificarán: artistas favoritos, cambio en la forma de estudiar, proceso de verificación de la información y reglas personales de uso de la IA. Se reservan para un análisis descriptivo de texto con NLP. El diccionario completo está en el Anexo A y en `docs/diccionario_variables.csv`.

### 3.6 Criterio de aceptación de la fase

- [x] Matriz de relación y justificación de la selección documentadas (secciones 3.2 y 3.3).
- [x] Los tres documentos aceptados se leen y perfilan con `pandas` mediante funciones reutilizables (`src/datos.py`).
- [x] Datos crudos organizados en `data/raw/` y protegidos de Git.
- [x] Diccionario de variables con regla de codificación y uso para cada pregunta.

## 4. Fase 3 — Limpieza individual

### 4.1 Objetivo y principios

El objetivo de esta fase es depurar por separado cada documento aceptado y convertir sus respuestas abiertas en variables analizables, sin integrarlos todavía. El procedimiento está en `notebooks/01_limpieza.ipynb`, y las reglas en `src/limpieza.py` (funciones generales) y `src/codificacion.py` (reglas por documento). Se siguieron cuatro principios:

1. **Reglas explícitas.** Cada variable se codifica con una lista ordenada de expresiones regulares sobre texto normalizado. La primera regla que coincide asigna el valor, y las más específicas (negaciones, matices) van primero.
2. **No inventar datos.** Si una respuesta no permite asignar un valor sin suponer información, se registra como faltante. No se imputa ningún valor.
3. **Marcar en lugar de eliminar.** Los atípicos y las respuestas sospechosas se señalan con banderas, para que su exclusión sea una decisión explícita del análisis.
4. **Validación exhaustiva.** Antes de fijar las reglas, se revisó cada respuesta junto a su código asignado. Esta revisión llevó a corregir tres reglas antes de la versión final: una errata en el nombre de la carrera, una negación interna en la pregunta de alimentación y una errata en "desayunar".

### 4.2 Procedimiento común

- **Normalización.** Descomposición Unicode NFKD, eliminación de diacríticos, minúsculas y unificación de espacios y saltos de línea (`unicodedata`, `re`).
- **Estandarización de duraciones.** Los números escritos se convierten a dígitos ("una", "veinticuatro", "media"). Además: un rango se resume en su punto medio ("2-3 h" → 2.5); "x o más" se toma como x, su cota inferior; "menos de 1" vale 0.5; los minutos se convierten a fracción de hora.
- **Escalas ordinales y Likert.** Las expresiones verbales se ubican en escalas de 0 a 4, 0 a 3, 0 a 2 o −1 a 1, según la variable. Las calificaciones x/10 se reescalan a la escala correspondiente.
- **Llave y anonimato.** La cuenta de 10 dígitos del Documento 1 se corrigió porque, al borrar un dígito, coincidía de forma única con la cuenta sin pareja del Documento 3. Después, el número de cuenta se sustituyó por un seudónimo: HMAC-SHA256 con una clave secreta guardada fuera de Git, truncado a 12 caracteres. El seudónimo es el mismo en los tres documentos e irreversible sin la clave.

### 4.3 Resultados por documento

| Indicador | Doc 1. Música | Doc 2. Bienestar | Doc 3. IA |
|-----------|-------------:|-----------------:|----------:|
| Registros conservados | 24 de 24 | 19 de 19 | 24 de 24 |
| Variables en el archivo limpio | 53 | 37 | 45 |
| Variables derivadas (codificadas, banderas y calidad) | 35 | 20 | 27 |
| Faltantes de origen | 1 | 0 | 2 |
| Archivo | `doc1_musica_clean.csv` | `doc2_bienestar_clean.csv` | `doc3_ia_clean.csv` |

No se eliminó ningún registro. La lista de variables derivadas, con sus válidos y faltantes, está en `docs/variables_codificadas.csv`.

**Distribuciones de las variables clave:**

| Variable | Válidos | Distribución |
|----------|--------:|--------------|
| `mejora_animo` (Doc 1) | 20 | Mejora: 17 · Sin cambio: 3 |
| `m_horas` (Doc 1) | 24 | Mediana 4 h (Q1 2.4 · Q3 5.5); mín. 0, máx. 15 |
| `m_horas_nivel` (Doc 1) | 24 | Baja: 5 · Media: 9 · Alta: 10 |
| `m_genero_grupo` (Doc 1) | 24 | Rock/metal: 8 · Pop: 6 · Electrónica: 3 · Urbano: 3 · Regional: 2 · Variado: 1 · No escucha: 1 |
| `m_concentracion_cod` (Doc 1) | 23 | Distrae: 7 · Depende: 5 · Ayuda: 11 |
| `iep` (Doc 2) | 18 | Bajo: 4 · Medio: 9 · Alto: 5 |
| `b_sueno_calidad_cod` (Doc 2) | 19 | Mala: 5 · Algo mala: 6 · Regular: 5 · Buena: 3 |
| `ia_horas` (Doc 3) | 24 | Mediana 1.5 h (Q1 1 · Q3 2); mín. 0.08, máx. 8 |
| `ia_guia_vs_atajo_cod` (Doc 3) | 23 | Guía: 8 · Ambas: 13 · Atajo: 2 |
| `ia_estres_cod` (Doc 3) | 24 | Aumenta: 1 · Sin efecto: 3 · Disminuye: 20 |

**Faltantes generados por la codificación.** Las respuestas que describen un estado sin comparar el antes y el después no se cuentan como mejora de ánimo: "bueno", "muy bueno" y "mejorable" (4 casos). Tampoco se codificaron:

- una frecuencia de desánimo sin periodo ("5 veces"), por lo que ese estudiante no tiene IEP;
- dos niveles de interés sin escala ("4" y "se sigue manteniendo estable");
- una carrera no especificada ("UNAM");
- algunas respuestas sobre la IA sin dirección clara (entre 1 y 5 por variable).

### 4.4 Valores atípicos

Se aplicó el criterio del rango intercuartílico (fuera de Q1 − 1.5·IQR o de Q3 + 1.5·IQR):

| Variable | Límite superior | Valores atípicos |
|----------|----------------:|------------------|
| `m_horas` | 10.2 h | 15 h |
| `b_traslado_min_cod` | 135 min | 360 min |
| `ia_horas` | 3.5 h | 4, 6 y 8 h (la de 8 h incluye uso en el trabajo) |
| `b_edad_cod` | 26 años | ninguno |

Ningún atípico se eliminó. Son auto-reportes posibles, por ejemplo música de fondo durante toda la jornada o un traslado excepcionalmente largo. Los indicadores reportarán la mediana junto con la media.

### 4.5 Respuestas copiadas

Para cada estudiante se contaron las respuestas abiertas de al menos cinco palabras idénticas a la de otro estudiante. Un registro del Documento 3 tiene 4 coincidencias de este tipo y comparte seudónimo con un registro del Documento 1. Ese estudiante quedó marcado con `sospecha_copia = 1` y se conservó. No pertenece al núcleo de 19, así que solo afectará los análisis que usen los Documentos 1 y 3 sin el 2; para esos se reportará un análisis de sensibilidad.

### 4.6 Implicaciones para las fases siguientes

1. **El modelado supervisado no es viable con la etiqueta prevista.** `mejora_animo` tiene solo 3 casos negativos, menos que el mínimo de 4 fijado en `docs/negocio.md` §5. La Fase 5 se centrará en el agrupamiento no supervisado, y el KPI 1 deberá leerse junto con su *n*.
2. **`ia_estres_cod` está muy concentrada** (20 de 24 casos en "disminuye"), así que tendrá poco poder para distinguir grupos. Para H4 tendrán más peso las horas de IA y la modalidad de uso.
3. **La categoría "atajo" tiene 2 casos.** En los indicadores se agrupará con "ambas", conforme a la regla de mínimo 3 casos.
4. **El semestre es constante (7 en los 19 casos)**, lo que confirma que el filtro por semestre del tablero solo tendrá valor si se agregan datos de otros semestres.

### 4.7 Criterio de aceptación de la fase

- [x] Diagnóstico de forma, tipos, faltantes y duplicados para cada documento.
- [x] Texto normalizado (NFKD, `re`) y respuestas Likert y ordinales codificadas con reglas documentadas.
- [x] Horas y minutos estandarizados con expresiones regulares y `apply`/`map`.
- [x] Faltantes tratados con justificación y sin imputación; atípicos detectados y marcados.
- [x] Conjuntos guardados en `data/processed/` con sufijo `_clean`, sin números de cuenta.
- [x] Bitácora de decisiones en el cuaderno (sección 9).

## Anexo A. Diccionario de variables

<!-- anexo:diccionario -->
|   Doc | P   | Variable               | Pregunta                                                        | Respuesta                | Codificación prevista                                              | Uso                                    |
|------:|:----|:-----------------------|:----------------------------------------------------------------|:-------------------------|:-------------------------------------------------------------------|:---------------------------------------|
|     1 | -   | marca_temporal         | Marca temporal                                                  | Fecha y hora             | datetime                                                           | Control                                |
|     1 | -   | cuenta                 | Número de cuenta                                                | Entero                   | Llave; se anonimiza con hash                                       | Llave                                  |
|     1 | P1  | m_genero_frecuente     | Tipo de música que escucha con mayor frecuencia y por qué       | Texto libre              | Grupo de género musical (palabras clave)                           | H3, KPI géneros, filtro                |
|     1 | P2  | m_horas_dia            | Tiempo diario dedicado a escuchar música                        | Numérica en texto        | Horas (float) con regex                                            | H2, KPI horas                          |
|     1 | P3  | m_momentos             | Momentos del día y actividades mientras escucha                 | Multirrespuesta en texto | Banderas: estudio, traslado, ejercicio, descanso, trabajo          | H2                                     |
|     1 | P4  | m_plataforma           | Plataformas o dispositivos de escucha                           | Multirrespuesta en texto | Banderas: Spotify, YouTube, otras                                  | Descriptivo                            |
|     1 | P5  | m_animo_antes_despues  | Estado de ánimo antes y después de escuchar música favorita     | Texto libre              | Etiqueta binaria mejora_animo (sí/no)                              | H1-H4, variable objetivo, KPI % mejora |
|     1 | P6  | m_generos_emocion      | Géneros que lo hacen sentir feliz, tranquilo, triste o motivado | Texto libre              | Banderas de género                                                 | H3                                     |
|     1 | P7  | m_experiencia          | Experiencia en que una canción cambió su ánimo                  | Texto libre              | Bandera: reporta experiencia (sí/no)                               | Descriptivo                            |
|     1 | P8  | m_musica_estres        | Música que escucha cuando está triste o estresado               | Texto libre              | Grupo de género / tipo de uso                                      | Indicador indirecto de estrés          |
|     1 | P9  | m_energia              | Influencia de la música en energía y motivación                 | Ordinal en texto         | 0 no influye, 1 algo, 2 mucho                                      | H2                                     |
|     1 | P10 | m_concentracion        | Influencia de la música en la concentración                     | Ordinal en texto         | -1 distrae, 0 neutro, 1 ayuda                                      | H2                                     |
|     1 | P11 | m_sueno                | Influencia de la música en el descanso o el sueño               | Ordinal en texto         | -1 perjudica, 0 neutro, 1 ayuda                                    | H2                                     |
|     1 | P12 | m_con_vs_sin           | Diferencias entre actividad con música y en silencio            | Texto libre              | -1 peor, 0 igual, 1 mejor con música                               | Descriptivo                            |
|     1 | P13 | m_caracteristicas      | Características de la canción que influyen en emociones         | Multirrespuesta en texto | Banderas: ritmo, letra, volumen, otras                             | Descriptivo                            |
|     1 | P14 | m_maneja_emociones     | ¿La música ayuda a manejar emociones negativas?                 | Sí/No con explicación    | Binaria                                                            | H1                                     |
|     1 | P15 | m_importancia          | Importancia de la música en su vida y bienestar                 | Ordinal en texto         | 0 baja, 1 media, 2 alta                                            | Perfilado                              |
|     1 | P16 | m_artistas             | Cinco artistas más escuchados                                   | Lista en texto           | No se modela (solo NLP descriptivo)                                | Descriptivo                            |
|     2 | -   | marca_temporal         | Marca temporal                                                  | Texto (fecha GMT-6)      | datetime                                                           | Control                                |
|     2 | -   | cuenta                 | Número de cuenta                                                | Entero                   | Llave; se anonimiza con hash                                       | Llave                                  |
|     2 | P2  | b_carrera              | Carrera que cursa                                               | Categórica en texto      | Normalizar a 'MAC' (validación)                                    | Filtro de población                    |
|     2 | P3  | b_semestre             | Semestre                                                        | Numérica en texto        | Entero                                                             | Filtro (constante = 7)                 |
|     2 | P4  | b_edad                 | Edad                                                            | Numérica en texto        | Entero (incluye números escritos)                                  | Contexto                               |
|     2 | P5  | b_convivencia          | Con quién vive en el periodo de clases                          | Categórica en texto      | familia / solo / otros                                             | Contexto                               |
|     2 | P6  | b_traslado_min         | Tiempo de traslado casa-universidad                             | Numérica en texto        | Minutos (float) con regex                                          | Contexto, problemática                 |
|     2 | P7  | b_ambiente_hogar       | Ambiente y convivencia en el hogar                              | Ordinal en texto         | 0 conflictivo, 1 normal, 2 tranquilo                               | Contexto                               |
|     2 | P8  | b_sueno_calidad        | Calidad del descanso y horarios de sueño                        | Ordinal en texto         | 0 mala a 3 buena                                                   | H2, bienestar                          |
|     2 | P9  | b_espacio_estudio      | Tranquilidad o espacio en casa para estudiar                    | Ordinal en texto         | 0 poco, 1 medio, 2 mucho                                           | Contexto                               |
|     2 | P10 | b_desanimo             | Frecuencia de sentirse decaído o desmotivado                    | Likert en texto          | 0 nunca a 4 muy frecuentemente                                     | H1, indicador indirecto de estrés      |
|     2 | P11 | b_irritabilidad        | Facilidad para perder la paciencia o irritarse                  | Likert en texto          | 0 nunca a 4 muy fácilmente                                         | H1, indicador indirecto de estrés      |
|     2 | P12 | b_apoyo_social         | Nivel de apoyo de familia, amigos o compañeros                  | Ordinal en texto         | 0 bajo a 3 alto                                                    | Contexto                               |
|     2 | P13 | b_traslado_impacto     | Impacto de los traslados en el estado de ánimo                  | Ordinal en texto         | 0 ninguno a 3 alto                                                 | Problemática                           |
|     2 | P14 | b_interes              | Interés y disfrute por materias y actividades                   | Ordinal en texto         | 0 bajo a 2 alto                                                    | Bienestar                              |
|     2 | P15 | b_alimentacion         | Cambios en alimentación o apetito                               | Texto libre              | Binaria: reporta cambio negativo                                   | Bienestar                              |
|     2 | P16 | b_concentracion_dif    | Dificultad para concentrarse                                    | Ordinal en texto         | 0 ninguna a 3 mucha                                                | H2, bienestar                          |
|     3 | -   | marca_temporal         | Marca temporal                                                  | Texto (fecha GMT-6)      | datetime                                                           | Control                                |
|     3 | -   | cuenta                 | Número de cuenta                                                | Entero                   | Llave; se anonimiza con hash                                       | Llave                                  |
|     3 | P2  | ia_herramientas        | Herramientas de IA que utiliza y frecuencia                     | Multirrespuesta en texto | Banderas: ChatGPT, Gemini, otras; n.º de herramientas              | Descriptivo, KPI                       |
|     3 | P3  | ia_fase_uso            | Fase del estudio en que más usa la IA                           | Multirrespuesta en texto | Banderas: investigación, estructura, redacción, corrección, repaso | Descriptivo                            |
|     3 | P4  | ia_cambio_estudio      | Cómo cambió su estudio con la IA                                | Texto libre              | No se modela (NLP descriptivo)                                     | Descriptivo                            |
|     3 | P5  | ia_verificacion        | Proceso para verificar la información                           | Texto libre              | No se modela (NLP descriptivo)                                     | Descriptivo                            |
|     3 | P6  | ia_impacto_tiempo      | Impacto en el tiempo dedicado a tareas                          | Texto libre              | -1 más tiempo, 0 igual, 1 menos tiempo                             | Descriptivo                            |
|     3 | P7  | ia_calificaciones      | Diferencias en calificaciones o retroalimentación               | Texto libre              | -1 empeoran, 0 igual, 1 mejoran                                    | Descriptivo                            |
|     3 | P8  | ia_independencia       | La IA fortalece o debilita la resolución independiente          | Texto libre              | -1 debilita, 0 depende, 1 fortalece                                | H4                                     |
|     3 | P9  | ia_estres              | Influencia de la IA en el estrés o carga mental                 | Texto libre              | -1 aumenta, 0 sin efecto, 1 disminuye                              | H4, indicador indirecto de estrés      |
|     3 | P10 | ia_reglas              | Reglas o límites personales de uso                              | Texto libre              | No se modela (NLP descriptivo)                                     | Descriptivo                            |
|     3 | P11 | ia_pensamiento_critico | Efecto en pensamiento crítico y comprensión                     | Texto libre              | -1 afecta, 0 depende, 1 mejora                                     | Descriptivo                            |
|     3 | P12 | ia_horas_dia           | Horas diarias de uso de IA                                      | Numérica en texto        | Horas (float) con regex                                            | H4, KPI uso de IA                      |
|     3 | P13 | ia_semestre_inicio     | Semestre en que empezó a usar IA                                | Numérica en texto        | Entero (semestre)                                                  | Aproximación a uso creciente           |
|     3 | P14 | ia_reemplazo_laboral   | ¿La IA podría reemplazarlo laboralmente?                        | Sí/No con explicación    | sí / no / parcial                                                  | Descriptivo                            |
|     3 | P15 | ia_guia_vs_atajo       | Usa la IA como guía o como atajo                                | Categórica en texto      | guía / atajo / ambas                                               | H4                                     |
|     3 | P16 | ia_motivo              | Motivo principal para recurrir a la IA                          | Texto libre              | Categoría: comprensión / tiempo / otro                             | Descriptivo                            |
|     3 | P17 | ia_otros_usos          | Usos de la IA fuera de lo académico                             | Sí/No con explicación    | Binaria                                                            | Descriptivo                            |
<!-- /anexo -->

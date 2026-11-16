---
title: "Momento A — Análisis y selección justificada de las fuentes de datos"
subtitle: "Hábitos musicales, estado de ánimo, estrés académico y uso de IA en estudiantes de MAC, FES Acatlán"
lang: es-MX
---

## 1. Introducción

Este proyecto busca identificar qué hábitos musicales se asocian con un mejor estado de ánimo reportado en estudiantes de Matemáticas Aplicadas y Computación (MAC) de la FES Acatlán, UNAM, y cómo se relacionan con su nivel de estrés académico y su uso de herramientas de inteligencia artificial (IA). Hay seis cuestionarios disponibles, recolectados con Google Forms entre septiembre y noviembre de 2026. Antes de limpiar o modelar cualquier dato hace falta decidir cuáles son pertinentes para la pregunta de investigación. Este documento presenta ese análisis previo, denominado *Momento A*. Describe cada fuente, evalúa su relación con la pregunta y justifica qué documentos se integran al estudio y cuáles se descartan.

<!-- code:setup -->

## 2. Objetivo

Seleccionar de manera justificada y reproducible el subconjunto de documentos que se integrará en las fases posteriores. El criterio es que cada documento aporte variables relevantes para la pregunta de investigación y pueda vincularse con los demás mediante el número de cuenta.

## 3. Metodología

### 3.1 Fuentes

| # | Archivo | Formato |
|---|---------|---------|
| 1 | La música y su influencia en el estado de ánimo (respuestas) | .xlsx |
| 2 | Cuestionario: Entorno Universitario y Bienestar | .csv |
| 3 | Desempeño académico por el uso de IA | .csv |
| 4 | Test (Respuestas) | .xlsx |
| 5 | Pelis y series (Respuestas) | .xlsx |
| 6 | Relación Amor – Carrera (Respuestas) | .xlsx |

### 3.2 Procedimiento

Cada archivo se leyó con `pandas` (`read_csv` y `read_excel`). De cada documento se registraron el número de registros y de variables, el tipo de dato, los valores nulos por columna y la llave de identificación. Para medir la compatibilidad entre documentos se calculó la intersección de números de cuenta para cada par. En el Documento 6, que no pide el número de cuenta, la llave se obtuvo del prefijo numérico del correo institucional (`cuenta@pcpuma.acatlan.unam.mx`). Ningún resultado muestra números de cuenta ni correos, para preservar el anonimato de los participantes.

### 3.3 Criterios de selección

Un documento se **acepta** si cumple dos condiciones:

1. Contiene variables relacionadas con la pregunta: música, estado de ánimo, estrés, sueño, concentración o uso de IA.
2. Comparte la llave *número de cuenta* con los demás documentos aceptados.

Se **rechaza** si no contiene variables de la pregunta, si su llave es incompatible o si incluirlo añadiría ruido sin señal.

## 4. Resultados

### 4.1 Perfil descriptivo de los documentos

<!-- code:perfil -->

| # | Registros × variables | Tipos de dato | Nulos | Llave | Tema central |
|---|----------------------|---------------|-------|-------|--------------|
| 1 | 24 × 18 | Marca temporal (fecha), cuenta (entero), 16 de texto libre | 1 (pregunta 3) | Número de cuenta | Hábitos musicales y su efecto percibido en ánimo, energía, concentración y sueño |
| 2 | 19 × 17 | Marca temporal (texto), cuenta (entero), 15 de texto libre | 0 | Número de cuenta | Bienestar: sueño, desánimo, irritabilidad, concentración, apetito, apoyo social y traslados |
| 3 | 24 × 18 | Marca temporal (texto), cuenta (entero), 16 de texto libre | 2 | Número de cuenta | Uso académico de IA, horas diarias y efecto percibido en el estrés |
| 4 | 25 × 18 | Marca temporal (fecha), correo, cuenta (entero), 15 de texto libre | 2 | Correo y número de cuenta | Rasgos de personalidad y preferencias personales |
| 5 | 21 × 17 | Marca temporal (fecha), cuenta (entero), 15 de texto libre | 0 | Número de cuenta | Preferencias de cine y series |
| 6 | 21 × 21 | Marca temporal (fecha), correo, 2 numéricas, 17 de texto | 1 por columna | Solo correo | Concepciones sobre relaciones de pareja |

En los seis documentos predomina el texto libre: incluso las preguntas cuantitativas, como las horas de escucha o de uso de IA, se respondieron en lenguaje natural ("una hora y media", "2-3 h"). En el Documento 2, el 100 % de los participantes cursa séptimo semestre de MAC, aunque con al menos diez formas distintas de escribirlo ("MAC", "Septimo", "7mo semestre", entre otras).

<!-- code:detalle -->

### 4.2 Compatibilidad de la llave de identificación

<!-- code:llaves -->

| | Doc 1 | Doc 2 | Doc 3 | Doc 4 | Doc 5 | Doc 6 |
|---|---:|---:|---:|---:|---:|---:|
| **Doc 1** | 24 | 19 | 23 | 23 | 21 | 20 |
| **Doc 2** | 19 | 19 | 19 | 19 | 19 | 19 |
| **Doc 3** | 23 | 19 | 24 | 24 | 21 | 20 |

*Tabla 2. Número de cuentas compartidas entre pares de documentos (extracto).*

El análisis muestra que los seis cuestionarios los respondió prácticamente el mismo grupo de estudiantes, así que **la llave es compatible en todos los documentos**. Por lo tanto, el segundo criterio no permite descartar ninguno, y la decisión depende del primero: la pertinencia temática. La intersección de los Documentos 1, 2 y 3 es de **19 registros**; el Documento 2 es el que limita el tamaño, porque solo tiene 19 respuestas.

<!-- code:calidad -->

También se encontraron tres problemas de calidad que se atenderán en la Fase 3:

- En el Documento 1, un número de cuenta tiene diez dígitos, probablemente por un error de captura, y no coincide con ningún otro documento.
- En el Documento 4, un participante respondió dos veces.
- En el Documento 6, un participante rechazó participar y por eso no tiene respuestas.

### 4.3 Matriz de relación

<!-- code:matriz -->

Para respaldar el criterio temático con evidencia verificable, se normalizaron los enunciados de todas las preguntas (minúsculas y sin acentos) y se contaron los que aluden a cada constructo de la pregunta de investigación. El Documento 1 tiene 26 coincidencias, el Documento 3 tiene 16 (15 de ellas sobre IA) y el Documento 2 tiene 5 (ánimo, sueño y concentración). Los Documentos 4 y 5 no tienen ninguna, y el Documento 6 solo tiene una: la pregunta sobre la canción, película o libro que describe la idea del amor, que no mide hábitos de escucha. A partir de esta evidencia se construyó la matriz de relación:

| Documento | Tema central | Variables clave | ¿Se relaciona con música, ánimo, estrés o IA? | Llave compatible | Veredicto |
|-----------|--------------|-----------------|---------------------------------------------|------------------|-----------|
| 1. Música y ánimo | Hábitos musicales y su efecto en el ánimo | Género más escuchado, horas diarias, momentos y actividades de escucha, plataforma, ánimo antes y después, géneros por emoción, música ante el estrés, energía, concentración, sueño | Sí, de forma directa | Sí | **Aceptar (principal)** |
| 2. Entorno universitario y bienestar | Bienestar emocional y contexto | Desánimo, irritabilidad, calidad del sueño, concentración, apetito, apoyo social, tiempo de traslado y su impacto en el ánimo | Sí: ánimo, sueño, concentración y estrés indirecto | Sí | **Aceptar (complementario fuerte)** |
| 3. Desempeño por uso de IA | Uso académico de la IA | Horas diarias de IA, herramientas, efecto en el estrés, dependencia, uso como guía o como atajo | Sí: IA y estrés académico | Sí | **Aceptar (complementario medio)** |
| 4. Test | Personalidad y preferencias | Pasatiempo, deporte, sociabilidad, toma de decisiones, organización del tiempo, sexo | Solo marginalmente | Sí, con un duplicado | **Rechazar** |
| 5. Pelis y series | Preferencias audiovisuales | Películas, series, actores favoritos y sobrevalorados | No | Sí | **Rechazar** |
| 6. Relación amor–carrera | Concepciones de pareja | Situación sentimental, valores, señales de alerta, cita ideal | No | Solo derivada del correo | **Rechazar** |

## 5. Discusión

La pregunta de investigación tiene tres componentes: (a) la relación entre hábitos musicales y estado de ánimo, (b) su vínculo con el estrés y el sueño, y (c) el papel del uso de IA. Los documentos aceptados se complementan, porque cada uno cubre principalmente un componente distinto.

El **Documento 1** es la fuente **principal**. Es el único que mide la variable central del estudio, los hábitos musicales (género, duración, momento y plataforma de escucha), junto con el cambio de ánimo antes y después de escuchar música. De esa última pregunta se puede derivar una etiqueta binaria de "mejora de ánimo" para el análisis supervisado.

El **Documento 2** es un **complemento fuerte**. Mide el bienestar directamente (desánimo, irritabilidad, sueño y concentración) sin hacer referencia a la música. Esto es valioso metodológicamente: permite contrastar el ánimo atribuido a la música con el ánimo general reportado y reduce la dependencia de una sola medida de auto-reporte. Además incluye variables de contexto que forman parte de la problemática, como el semestre, la edad y el tiempo de traslado.

El **Documento 3** es un **complemento medio**. Aporta la variable moderadora de la hipótesis, el uso de IA (horas diarias y modalidad de uso), y un indicador de estrés académico relacionado con la IA.

Los documentos rechazados no aportan a ninguno de los tres componentes:

- El **Documento 4** (Test) describe rasgos de personalidad y preferencias generales. No incluye medidas de ánimo, estrés, sueño ni uso de IA, y la música solo aparece de forma incidental como pasatiempo. Además contiene un registro duplicado.
- El **Documento 5** (Pelis y series) trata sobre el consumo audiovisual de ficción, un tema ajeno a la pregunta.
- El **Documento 6** (Relación amor–carrera) aborda concepciones sobre relaciones de pareja, que no equivalen al estado de ánimo. Además, su llave solo existe dentro del correo institucional, lo que obligaría a procesar un dato personal adicional sin beneficio analítico.

Integrar los documentos rechazados no aumentaría la muestra, que seguiría siendo de 19 registros. En cambio, agregaría alrededor de cincuenta variables de texto libre sin relación con la pregunta. Con una muestra tan pequeña, esa dimensionalidad adicional aumentaría el riesgo de sobreajuste y añadiría ruido al análisis de agrupamiento.

## 6. Conclusión

Con base en los criterios de pertinencia temática y compatibilidad de llave, el estudio integrará los **Documentos 1, 2 y 3**:

- **Principal:** Documento 1, *La música y su influencia en el estado de ánimo*.
- **Complementario fuerte:** Documento 2, *Entorno Universitario y Bienestar*.
- **Complementario medio:** Documento 3, *Desempeño académico por el uso de IA*.

Se **rechazan** los Documentos 4 (*Test*), 5 (*Pelis y series*) y 6 (*Relación Amor – Carrera*) porque no contienen variables vinculadas con la pregunta de investigación. Los tres comparten la llave con los demás, así que el rechazo se debe exclusivamente a su falta de pertinencia temática.

## 7. Consideraciones para las fases siguientes

La revisión de los datos reales frente a la problemática planteada deja varias observaciones que conviene tener en cuenta desde ahora:

1. **Tamaño muestral.** La integración por intersección conserva 19 de los 24 registros del Documento 1. Con este tamaño, los resultados son exploratorios y tienen poca potencia estadística.
2. **Medición del estrés.** Ningún cuestionario tiene una escala de estrés propiamente dicha. Se usarán indicadores indirectos: la irritabilidad y el desánimo (Documento 2), el efecto percibido de la IA en el estrés (Documento 3) y la música que se escucha en momentos de estrés (Documento 1).
3. **Variables constantes.** Todos los participantes cursan séptimo semestre, así que un filtro por semestre en el tablero no distinguiría entre grupos. El filtro por "género" se interpretará como género musical, porque el sexo de los participantes solo aparece en el Documento 4, que se rechazó.
4. **Uso "creciente" de IA.** No hay mediciones repetidas en el tiempo. La tendencia solo puede aproximarse con el semestre en que cada estudiante empezó a usar estas herramientas.
5. **Naturaleza de los datos.** Las respuestas son auto-reportadas y observacionales, así que los hallazgos describirán asociaciones y no relaciones causales.

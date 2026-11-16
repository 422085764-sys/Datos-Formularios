# Hábitos musicales, estado de ánimo, estrés académico y uso de IA en estudiantes de MAC

Proyecto escolar de ciencia de datos con estudiantes de séptimo semestre de Matemáticas Aplicadas y Computación (MAC), FES Acatlán, UNAM. A partir de cuestionarios aplicados al grupo, responde:

> ¿Qué hábitos musicales se asocian con un mejor estado de ánimo reportado en estudiantes de MAC, y cómo se relacionan con su nivel de estrés académico y su uso de IA?

El proyecto cubre el ciclo completo:

1. Selección justificada de fuentes.
2. Limpieza y codificación de texto libre.
3. Integración y análisis exploratorio con pruebas estadísticas.
4. Agrupamiento en perfiles.
5. Tablero interactivo.
6. Documentación técnica y de negocio.

## Resultados principales

- **El 85 % reporta que la música mejora su ánimo** (17 de 20). Quienes lo reportan escuchan más horas: mediana de 5 h frente a 1.5 h. La música se escucha sobre todo en los traslados (75 %).
- **Ningún género ni momento de escucha** se asocia con más bienestar. Los beneficios atribuidos a la música **no se reflejan** en los indicadores generales de desánimo, irritabilidad o sueño: el efecto parece situacional.
- **Usar la IA como guía para aprender** se asocia con menos estrés percibido (IEP mediano 1.0 frente a 2.5). Las horas de uso de IA no marcan diferencia.
- **Los traslados más largos** se asocian con peor calidad de sueño (ρ = −0.51).
- **Tres perfiles de estudiantes** (K-Means, silueta de 0.28): escucha intensiva, estrés alto, e IA como guía con estrés bajo.
- **Preferencias:** Bad Bunny es el artista más mencionado (4 de 24), YouTube la plataforma más usada (13), el ritmo lo que más influye de una canción (19) y la investigación o resolución de dudas el uso principal de la IA (16).

Los datos son observacionales y auto-reportados (n = 19 en el núcleo integrado, 24 en música + IA). Los resultados son **asociaciones exploratorias**: ninguna supera la corrección por comparaciones múltiples y no implican causalidad. Ver `docs/tecnico.pdf` y `docs/negocio.pdf`.

## Estructura

```
├── data/                 # no se versiona (contiene números de cuenta)
│   ├── raw/              # 3 cuestionarios aceptados + clave del seudónimo
│   ├── processed/        # datos limpios, integrados y perfiles (seudonimizados)
│   └── excluded/         # 3 cuestionarios rechazados en el Momento A
├── notebooks/
│   ├── 00_momento_A.ipynb          # análisis y selección de los 6 documentos
│   ├── 00_perfil_aceptados.ipynb   # Fase 1: inventario, perfil y diccionario
│   ├── 01_limpieza.ipynb           # Fase 3: limpieza y codificación
│   ├── 02_eda.ipynb                # Fase 4: integración, EDA, hipótesis y texto
│   └── 03_modelado.ipynb           # Fase 5: perfiles (K-Means, PCA, DBSCAN)
├── src/
│   ├── datos.py, diccionario.py    # rutas, carga y diccionario de variables
│   ├── limpieza.py, codificacion.py# normalización y reglas de codificación
│   ├── integracion.py, eda.py      # unión de documentos y pruebas estadísticas
│   ├── texto.py                    # análisis de texto con NLTK
│   ├── graficos.py                 # figuras con paleta apta para daltonismo
│   ├── modelado.py                 # agrupamiento, estabilidad y PCA
│   ├── tablero.py                  # KPI del tablero
│   └── momento_a.py, anexos.py, exportar_docs.py
├── app/app.py            # tablero Streamlit + Plotly (KPI, perfiles y clasificaciones: artistas, plataformas, uso de IA)
├── docs/
│   ├── tecnico.{md,docx,pdf}       # método y resultados
│   ├── negocio.{md,docx,pdf}       # problemática, KPI y recomendaciones
│   ├── momento_A.{md,docx,pdf}     # selección de fuentes
│   ├── figuras/                    # figuras del documento técnico
│   └── *.csv                       # matriz, diccionario, variables y pruebas
├── requirements.txt
└── README.md
```

## Instalación

Requiere Python 3.14. En Windows, el lanzador es `py`.

```bash
py -m venv .venv
```

```bash
.venv/Scripts/python -m pip install -r requirements.txt
```

Los datos no forman parte del repositorio. Hay que colocar los tres cuestionarios aceptados en `data/raw/` y, para reproducir el Momento A, los tres rechazados en `data/excluded/`. La primera ejecución de la limpieza crea la clave del seudónimo en `data/raw/.clave_seudonimo`. Para obtener los mismos identificadores en otra máquina, hay que copiar esa clave.

## Ejecución

Los cuadernos se ejecutan en orden desde `notebooks/`. En Windows hace falta `PYTHONUTF8=1`: sin esa variable, `jupyter-execute` lee el `.ipynb` con la codificación del sistema y corrompe los acentos del código.

```bash
cd notebooks && PYTHONUTF8=1 ../.venv/Scripts/jupyter-execute --inplace 00_momento_A.ipynb 00_perfil_aceptados.ipynb 01_limpieza.ipynb 02_eda.ipynb 03_modelado.ipynb
```

Tablero interactivo (requiere haber ejecutado los cuadernos 01 a 03):

```bash
.venv/Scripts/streamlit run app/app.py
```

Regenerar el anexo del diccionario y los documentos en Word y PDF. El script usa el pandoc incluido en `pypandoc_binary`; genera el PDF con `xelatex` si está instalado y, si no, con Microsoft Edge en modo *headless*.

```bash
.venv/Scripts/python src/anexos.py
```

```bash
.venv/Scripts/python src/exportar_docs.py docs/tecnico.md docs/negocio.md docs/momento_A.md
```

## Herramientas

pandas, numpy, scipy.stats, scikit-learn, matplotlib, seaborn, plotly, nltk, streamlit, nbformat/nbclient, pandoc (`pypandoc_binary`) y Git. Las versiones exactas están en `requirements.txt`. No se usaron ydata-profiling ni pandera, que eran opcionales: el perfilado y la validación de estructura se implementaron en `src/datos.py`.

## Privacidad

- Los números de cuenta se sustituyen por un seudónimo HMAC-SHA256 con clave secreta, que no se versiona.
- La carpeta `data/` está excluida de Git.
- Los cuadernos y el tablero muestran solo información agregada y ocultan cualquier selección con menos de 3 estudiantes.

## Curso y autores

- Curso: Sistemas Inteligentes — FES Acatlán, UNAM.
- Autores: *por completar*.

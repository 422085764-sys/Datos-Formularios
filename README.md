# Hábitos musicales, estado de ánimo, estrés académico y uso de IA en estudiantes de MAC

Proyecto escolar de ciencia de datos con estudiantes de séptimo semestre de Matemáticas Aplicadas y Computación (MAC), FES Acatlán, UNAM. Integra tres cuestionarios para responder:

> ¿Qué hábitos musicales se asocian con un mejor estado de ánimo reportado en estudiantes de MAC, y cómo se relacionan con su nivel de estrés académico y su uso de IA?

Los datos son observacionales y auto-reportados (n = 19 tras la integración): los resultados describen asociaciones, no relaciones causales.

## Estado del proyecto

| Etapa | Estado | Entregables |
|-------|--------|-------------|
| Momento A: selección de documentos | ✅ | `docs/momento_A.*`, `notebooks/00_momento_A.ipynb` |
| Fase 0: definición del proyecto | ✅ | `docs/negocio.*` |
| Fase 1: inventario y selección | ✅ | `docs/tecnico.*`, `notebooks/00_perfil_aceptados.ipynb`, `docs/diccionario_variables.csv` |
| Fase 2: problemática, solución y KPI | ⏳ | `docs/negocio.md` |
| Fase 3: limpieza | ⏳ | `notebooks/01_limpieza.ipynb` |
| Fase 4: integración y EDA | ⏳ | `notebooks/02_eda.ipynb` |
| Fase 5: modelado | ⏳ | `notebooks/03_modelado.ipynb` |
| Fase 6: tablero | ⏳ | `app/app.py` |
| Fase 7: documentación final | ⏳ | `docs/`, este README |

## Estructura

```
├── data/
│   ├── raw/          # 3 documentos aceptados (no se versiona)
│   ├── processed/    # datos limpios e integrados (no se versiona)
│   └── excluded/     # 3 documentos rechazados en el Momento A (no se versiona)
├── notebooks/        # 00_momento_A, 00_perfil_aceptados, 01_limpieza, 02_eda, 03_modelado
├── src/              # datos.py, diccionario.py, momento_a.py, anexos.py, exportar_docs.py
├── app/              # tablero Streamlit
├── docs/             # tecnico y negocio (.md/.docx/.pdf), matriz y diccionario (.csv)
├── requirements.txt
└── README.md
```

## Instalación

Requiere Python 3.14. En Windows el lanzador es `py`.

```bash
py -m venv .venv
```

```bash
.venv/Scripts/python -m pip install -r requirements.txt
```

Los datos no forman parte del repositorio porque contienen números de cuenta. Hay que colocar los tres archivos originales en `data/raw/`.

## Ejecución

Ejecutar los cuadernos desde la carpeta `notebooks/`. En Windows, `PYTHONUTF8=1` es necesario: sin esa variable, `jupyter-execute` lee el `.ipynb` con la codificación del sistema y corrompe los acentos del código.

```bash
cd notebooks && PYTHONUTF8=1 ../.venv/Scripts/jupyter-execute --inplace 00_momento_A.ipynb 00_perfil_aceptados.ipynb
```

Regenerar los documentos en Word y PDF (usa pandoc incluido en `pypandoc_binary`; PDF con xelatex si existe, si no con Microsoft Edge):

```bash
.venv/Scripts/python src/exportar_docs.py docs/tecnico.md docs/negocio.md docs/momento_A.md
```

## Curso y autores

- Curso: Sistemas Inteligentes — FES Acatlán, UNAM.
- Autores: *por completar*.

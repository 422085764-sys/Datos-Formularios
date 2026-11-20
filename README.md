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

Los datos son observacionales y auto-reportados (n = 19 en el núcleo integrado, 24 en música + IA). Los resultados son **asociaciones exploratorias**: ninguna supera la corrección por comparaciones múltiples y no implican causalidad. Ver `docs/tecnico.pdf` y `docs/negocio.pdf`, que sí se suben a Git.

## Estructura

```
├── data/                 # datos del proyecto (sí se versionan)
│   ├── raw/              # 3 cuestionarios aceptados
│   ├── processed/        # datos limpios, integrados y perfiles
│   └── excluded/         # 3 cuestionarios rechazados en el Momento A
├── notebooks/
│   ├── 00_analisis_documentos.ipynb # Momento A: de los 6 documentos a la pregunta
│   ├── 00_perfil_aceptados.ipynb   # Fase 1: inventario, perfil y diccionario
│   ├── 01_limpieza.ipynb           # Fase 3: limpieza y codificación
│   ├── 02_eda.ipynb                # Fase 4: integración, EDA, hipótesis y texto
│   └── 03_modelado.ipynb           # Fase 5: perfiles (K-Means, PCA, DBSCAN)
├── src/
│   ├── datos.py, diccionario.py    # rutas, carga y diccionario de variables
│   ├── limpieza.py                 # normalización 
│   ├── integracion.py, eda.py      # unión de documentos y pruebas estadísticas
│   ├── texto.py                    # análisis de texto con NLTK
│   ├── graficos.py                 # figuras con paleta apta para daltonismo
│   ├── modelado.py                 # agrupamiento, estabilidad y PCA
│   ├── tablero.py                  # KPI del tablero
│   └── analisis_documentos.py, anexos.py, exportar_docs.py
├── app/app.py            # tablero Streamlit + Plotly (KPI, perfiles y clasificaciones: artistas, plataformas, uso de IA)
├── docs/                 # en Git: PDF técnico y de negocio, CSV y figuras
│   ├── tecnico.pdf       # método y resultados
│   ├── negocio.pdf      # Análisis, problemática, KPI y recomendaciones
│   ├── figuras/                    # figuras del documento técnico (sí se versionan)
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
#Activamos el entorno
venv\Scripts\activate 

pip install -r requirements.txt

```

Los datos forman parte del repositorio (ver [`data/README.md`](data/README.md)): los tres cuestionarios aceptados están en `data/raw/`, los tres rechazados del Momento A en `data/excluded/` y los conjuntos generados en `data/processed/`. Al clonar el repositorio, los cuadernos se pueden ejecutar sin copiar ningún archivo adicional.

## Ejecución

Los cuadernos se ejecutan en orden desde `notebooks/`. En Windows hace falta `PYTHONUTF8=1`: sin esa variable, `jupyter-execute` lee el `.ipynb` con la codificación del sistema y corrompe los acentos del código.

```bash
cd notebooks && PYTHONUTF8=1 ../.venv/Scripts/jupyter-execute --inplace 00_analisis_documentos.ipynb 00_perfil_aceptados.ipynb 01_limpieza.ipynb 02_eda.ipynb 03_modelado.ipynb
```

Tablero interactivo (requiere haber ejecutado los cuadernos 01 a 03):

```bash
.venv/Scripts/streamlit run app/app.py
```


## Publicar el tablero (Streamlit Community Cloud)

Como `data/processed/` está en el repositorio, el tablero en la nube lee esos datos directamente. De forma opcional, se le puede entregar un conjunto mínimo como *secreto* de Streamlit, que vive en la configuración de la app y la app usa solo si no encuentra `data/processed/`. Ese conjunto tiene:

- solo las 49 columnas que usa el tablero;
- un número consecutivo en orden aleatorio en lugar del número de cuenta;
- ninguna respuesta abierta, salvo los nombres de artistas normalizados.

1. Genera el secreto en tu equipo, después de ejecutar los cuadernos 01 a 03:

   ```bash
   .venv/Scripts/python src/preparar_despliegue.py
   ```

   Crea `.streamlit/secrets.toml`, que está excluido de Git.
2. Entra a [share.streamlit.io](https://share.streamlit.io) con tu cuenta de GitHub y elige **Create app → Yup, I have an app**.
3. Llena los campos: repositorio `Datos-Formularios`, rama `main` y archivo principal `app/app.py`. Si quieres, elige también un subdominio para la URL.
4. En **Advanced settings**:
   - elige la versión de Python más reciente disponible (el proyecto usa 3.14);
   - en **Secrets**, pega **todo** el contenido de `.streamlit/secrets.toml`.
5. Pulsa **Deploy**. Las dependencias se instalan desde `app/requirements.txt`, una versión ligera con solo lo que usa el tablero.

**Quién puede verlo:**

- **Repositorio público:** la app es pública; cualquiera con el enlace la ve.
- **Repositorio privado:** la app es privada y solo la ven las personas que invites por correo (botón **Share** → *Invite viewers*). Community Cloud permite una sola app privada a la vez.

En ambos casos el tablero solo muestra cifras agregadas y oculta cualquier selección con menos de 3 estudiantes.

**Alternativa sin publicar nada** (por ejemplo, para presentarlo en clase): ejecuta `streamlit run app/app.py` y comparte la *Network URL* que muestra la terminal (`http://192.168.x.x:8501`). Solo funciona para personas conectadas a la misma red y mientras tu equipo tenga la app abierta.

## Herramientas

pandas, numpy, scipy.stats, scikit-learn, matplotlib, seaborn, plotly, nltk, streamlit, nbformat/nbclient, pandoc (`pypandoc_binary`) y Git. Las versiones exactas están en `requirements.txt`. No se usaron ydata-profiling ni pandera, que eran opcionales: el perfilado y la validación de estructura se implementaron en `src/datos.py`.

## Antes de subir cambios a GitHub

Revisa qué se subiría y si hay datos personales. El script lista los commits pendientes, los archivos nuevos o modificados y lo que protege el `.gitignore`. Termina con error si encuentra datos, secretos, números de cuenta o correos:

```bash
.venv/Scripts/python scripts/revisar_antes_de_subir.py --historial
```

`scripts/reescribir_historial.sh` limpia el historial de commits. Quita las líneas `Co-Authored-By` y, opcionalmente, cambia el correo de autor por tu correo *noreply* de GitHub (Settings → Emails). Primero crea un respaldo y no sube nada; al final indica el `git push --force-with-lease` que debes ejecutar:

```bash
bash scripts/reescribir_historial.sh --simular --email TU_ID+usuario@users.noreply.github.com
```

## Privacidad

- Los datos (crudos y procesados) se versionan en `data/`; el número de cuenta es la llave que une los tres cuestionarios.
- Los documentos, los cuadernos y el tablero muestran solo información agregada y ocultan cualquier selección con menos de 3 estudiantes.

## Curso y autores

- Curso: Sistemas Inteligentes — FES Acatlán, UNAM.
- Autores: 
   -    Franco Mitzi Natalie Gabrielle
   -    García Nazario Carlos Yahir
   -    Hernández Sandoval Kevin Odin
   -    Montoya Santiago Francisco

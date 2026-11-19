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

Los datos son observacionales y auto-reportados (n = 19 en el núcleo integrado, 24 en música + IA). Los resultados son **asociaciones exploratorias**: ninguna supera la corrección por comparaciones múltiples y no implican causalidad. Ver `docs/tecnico.pdf` y `docs/negocio.pdf`, que se generan localmente y no se suben a Git.

## Estructura

```
├── data/                 # no se versiona (contiene números de cuenta)
│   ├── raw/              # 3 cuestionarios aceptados + clave del seudónimo
│   ├── processed/        # datos limpios, integrados y perfiles (seudonimizados)
│   └── excluded/         # 3 cuestionarios rechazados en el Momento A
├── notebooks/
│   ├── 00_analisis_documentos.ipynb # Momento A: de los 6 documentos a la pregunta
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
│   └── analisis_documentos.py, anexos.py, exportar_docs.py
├── app/app.py            # tablero Streamlit + Plotly (KPI, perfiles y clasificaciones: artistas, plataformas, uso de IA)
├── docs/                 # se genera localmente; en Git solo se versionan las figuras
│   ├── tecnico.{md,docx,pdf}       # método y resultados
│   ├── negocio.{md,docx,pdf}       # Momento A, problemática, KPI y recomendaciones
│   ├── figuras/                    # figuras del documento técnico (sí se versionan)
│   └── *.csv                       # matriz, diccionario, variables y pruebas
├── requirements.txt
└── README.md
```

## Requisitos

| Herramienta | Para qué | Obligatoria |
|-------------|----------|-------------|
| **Python 3.14** | Ejecutar los cuadernos y el tablero. Las versiones de `requirements.txt` se probaron con Python 3.14.2; con versiones anteriores algunas podrían no instalarse | Sí |
| **Git** | Descargar (clonar) el repositorio | Sí |
| **Los 6 cuestionarios originales** | No están en el repositorio porque contienen números de cuenta. Se piden a los autores | Sí |
| **Un navegador Edge, Chrome o Chromium**, o **LaTeX** (`xelatex`) | Generar los PDF de la documentación. Los `.docx` se generan sin nada adicional | Solo para los PDF |

Los comandos de esta guía se ejecutan en una terminal: **PowerShell** en Windows, **Terminal** en macOS y la terminal de tu distribución en Linux.

## Instalación paso a paso

### Paso 1. Instalar Python 3.14 y Git

**Windows**

1. Instala Python 3.14 desde [python.org/downloads](https://www.python.org/downloads/). En el instalador marca **"Add python.exe to PATH"**. También puedes usar winget:

   ```powershell
   winget install Python.Python.3.14
   ```

2. Instala Git desde [git-scm.com](https://git-scm.com/download/win), o con winget:

   ```powershell
   winget install Git.Git
   ```

3. Cierra y vuelve a abrir PowerShell. Comprueba la instalación:

   ```powershell
   py -3.14 --version
   ```

   ```powershell
   git --version
   ```

**macOS**

1. Instala [Homebrew](https://brew.sh) si no lo tienes, y después Python y Git:

   ```bash
   brew install python@3.14 git
   ```

   También puedes usar el instalador de [python.org/downloads](https://www.python.org/downloads/).
2. Comprueba la instalación:

   ```bash
   python3.14 --version
   ```

**Linux (Ubuntu / Debian)**

1. Instala Git y las herramientas de entornos virtuales:

   ```bash
   sudo apt update && sudo apt install -y git python3-venv
   ```

2. Comprueba qué versión de Python trae tu distribución:

   ```bash
   python3 --version
   ```

   Si no es 3.14, instálala con [uv](https://docs.astral.sh/uv/), que funciona en cualquier distribución:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   ```bash
   uv python install 3.14
   ```

   En Fedora, usa `sudo dnf install git python3` en lugar de `apt`.

### Paso 2. Descargar el repositorio

Igual en los tres sistemas. Reemplaza `<URL-del-repositorio>` por la dirección del repositorio en GitHub (botón **Code**):

```bash
git clone <URL-del-repositorio> Datos-Formularios
```

```bash
cd Datos-Formularios
```

### Paso 3. Crear y activar el entorno virtual

El entorno virtual (`.venv`) guarda las librerías del proyecto sin mezclarlas con las de tu sistema. **Hay que activarlo cada vez que abras una terminal nueva** para trabajar en el proyecto.

| Sistema | Crear el entorno (una sola vez) | Activarlo (cada vez) |
|---------|----------------------------------|----------------------|
| Windows (PowerShell) | `py -3.14 -m venv .venv` | `.venv\Scripts\Activate.ps1` |
| Windows (CMD) | `py -3.14 -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS | `python3.14 -m venv .venv` | `source .venv/bin/activate` |
| Linux | `python3.14 -m venv .venv` (con uv: `uv venv --python 3.14 .venv`) | `source .venv/bin/activate` |

Cuando el entorno está activo, la terminal muestra `(.venv)` al inicio de la línea.

> **Windows:** si PowerShell responde que "la ejecución de scripts está deshabilitada", permítela solo para esa ventana y vuelve a activar el entorno:
>
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```

### Paso 4. Instalar las librerías

Con el entorno activo, el comando es igual en los tres sistemas:

```bash
python -m pip install --upgrade pip
```

```bash
python -m pip install -r requirements.txt
```

Tarda unos minutos la primera vez. Para comprobar que quedó bien:

```bash
python -c "import pandas, sklearn, streamlit, nltk; print('Instalación correcta')"
```

### Paso 5. Colocar los datos

Los cuestionarios no se descargan con el repositorio. Copia los archivos originales con sus **nombres exactos** (la lista completa está en [`data/README.md`](data/README.md)):

- `data/raw/`: los 3 cuestionarios que usa el estudio (música, bienestar e IA).
- `data/excluded/`: los 3 cuestionarios descartados (Test, Pelis y series, Relación amor–carrera). Solo se necesitan para el cuaderno `00_analisis_documentos`.

La primera vez que se ejecuta la limpieza se crea la clave del seudónimo en `data/raw/.clave_seudonimo`. Si quieres obtener **exactamente** los mismos identificadores que otra persona, copia también su clave antes de ejecutar los cuadernos. Nunca la subas a Git.

### Paso 6 (opcional). Herramienta para los PDF

Solo hace falta si vas a regenerar la documentación en PDF:

- **Windows:** no hay que instalar nada; se usa Microsoft Edge, que ya viene con el sistema.
- **macOS:** instala Google Chrome o Microsoft Edge (por ejemplo, `brew install --cask google-chrome`), o LaTeX con [MacTeX](https://www.tug.org/mactex/).
- **Linux:** instala Chromium (`sudo apt install -y chromium`, o `chromium-browser` en algunas versiones de Ubuntu) o LaTeX (`sudo apt install -y texlive-xetex`).

El script usa `xelatex` si lo encuentra; si no, imprime el documento con el primer navegador que encuentre.

## Ejecución

Todos los comandos se ejecutan desde la carpeta del proyecto y **con el entorno virtual activo**.

### 1. Ejecutar los cuadernos (en orden)

El cuaderno 01 genera los datos limpios que usan el 02 y el 03, así que el orden importa.

**macOS y Linux:**

```bash
cd notebooks && jupyter-execute --inplace 00_analisis_documentos.ipynb 00_perfil_aceptados.ipynb 01_limpieza.ipynb 02_eda.ipynb 03_modelado.ipynb && cd ..
```

**Windows (PowerShell).** Primero activa el modo UTF-8 de Python en esa ventana. Sin él, `jupyter-execute` lee los acentos del código con la codificación de Windows y falla:

```powershell
$env:PYTHONUTF8 = "1"
```

```powershell
cd notebooks; jupyter-execute --inplace 00_analisis_documentos.ipynb 00_perfil_aceptados.ipynb 01_limpieza.ipynb 02_eda.ipynb 03_modelado.ipynb; cd ..
```

En CMD, el equivalente es `set PYTHONUTF8=1`.

También se pueden abrir y ejecutar uno por uno en VS Code o en Jupyter, eligiendo el kernel del entorno `.venv`.

**Qué deberías obtener:**

- `data/processed/` con 6 archivos `.csv`: `doc1_musica_clean`, `doc2_bienestar_clean`, `doc3_ia_clean`, `integrado_123`, `integrado_13` y `perfiles`.
- Las figuras en `docs/figuras/`.
- Los cuadernos con sus resultados y sin errores.

### 2. Abrir el tablero

```bash
streamlit run app/app.py
```

Se abre en el navegador, en `http://localhost:8501`. Para detenerlo, presiona `Ctrl + C` en la terminal. Si el puerto está ocupado, usa otro:

```bash
streamlit run app/app.py --server.port 8502
```

### 3. Regenerar la documentación (Word y PDF)

```bash
python src/anexos.py
```

```bash
python src/exportar_docs.py docs/tecnico.md docs/negocio.md
```

Los documentos quedan en `docs/` y **no se suben a Git**; solo se versionan las figuras.

### Problemas frecuentes

| Problema | Causa | Solución |
|----------|-------|----------|
| `jupyter-execute`, `streamlit` o `python` "no se reconoce" | El entorno virtual no está activo | Actívalo (Paso 3) |
| En Windows, error de codificación o acentos raros al ejecutar los cuadernos | Falta el modo UTF-8 | Ejecuta `$env:PYTHONUTF8 = "1"` en esa ventana |
| `FileNotFoundError` en el cuaderno 00 o 01 | Faltan cuestionarios o tienen otro nombre | Revisa los nombres en `data/README.md` |
| El tablero dice que no encontró los datos | No se ejecutaron los cuadernos 01 a 03 | Ejecútalos en orden (Ejecución, punto 1) |
| `permission denied` al regenerar un `.docx` | El archivo está abierto en Word | Ciérralo y vuelve a intentarlo |
| "Para el PDF se necesita xelatex o un navegador…" | No hay navegador Chromium ni LaTeX | Instala uno (Paso 6); el `.docx` sí se generó |
| Error al instalar una librería | Versión de Python distinta de 3.14 | Crea el entorno con Python 3.14 |

## Publicar el tablero (Streamlit Community Cloud)

El repositorio **no contiene datos**. Para que el tablero funcione en la nube, se le entrega un conjunto mínimo como *secreto* de Streamlit, que vive en la configuración de la app y no en GitHub. Ese conjunto tiene:

- solo las 49 columnas que usa el tablero;
- un número consecutivo en orden aleatorio en lugar del seudónimo;
- ninguna respuesta abierta, salvo los nombres de artistas normalizados.

1. Genera el secreto en tu equipo (con el entorno virtual activo), después de ejecutar los cuadernos 01 a 03:

   ```bash
   python src/preparar_despliegue.py
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

## Privacidad

- Los números de cuenta se sustituyen por un seudónimo HMAC-SHA256 con clave secreta, que no se versiona.
- La carpeta `data/` está excluida de Git.
- Los cuadernos y el tablero muestran solo información agregada y ocultan cualquier selección con menos de 3 estudiantes.

## Curso y autores

- Curso: Sistemas Inteligentes — FES Acatlán, UNAM.
- Autores: 
   -    Franco Mitzi Natalie Gabrielle
   -    García Nazario Carlos Yahir
   -    Hernández Sandoval Kevin Odin
   -    Montoya Santiago Francisco

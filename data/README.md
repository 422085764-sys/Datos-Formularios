# Datos

Los datos **sí se suben** a este repositorio: los cuestionarios originales, los excluidos en el Momento A y los conjuntos procesados. Contienen números de cuenta y correos institucionales de los participantes; los documentos y el tablero solo presentan resultados agregados.

## Archivos originales

Los cuestionarios originales (exportados de Google Forms) están en el repositorio con estos nombres:

| Carpeta | Archivo | Uso |
|---------|---------|-----|
| `raw/` | `La música y su influencia en el estado de ánimo (respuestas).xlsx` | Documento 1 (principal) |
| `raw/` | `Cuestionario_ Entorno Universitario y Bienestar.csv` | Documento 2 (bienestar) |
| `raw/` | `Desempeño académico por el uso de IA.csv` | Documento 3 (uso de IA) |
| `excluded/` | `Test (Respuestas).xlsx` | Solo para reproducir el Momento A |
| `excluded/` | `Pelis y series (Respuestas).xlsx` | Solo para reproducir el Momento A |
| `excluded/` | `Relación Amor - Carrera (Respuestas).xlsx` | Solo para reproducir el Momento A |

`src/diccionario.py` documenta, columna por columna, la estructura que debe tener cada archivo. La función de carga verifica que el número de columnas coincida.

## Archivos generados

- `processed/`: conjuntos limpios (`doc*_clean.csv`), integrados (`integrado_*.csv`) y perfiles (`perfiles.csv`). Los generan los cuadernos 01 a 03 y también se versionan. La columna `id` es el número de cuenta.

## Despliegue del tablero

Como `processed/` está en el repositorio, el tablero publicado en Streamlit Community Cloud lee esos archivos directamente. De forma opcional, `python src/preparar_despliegue.py` genera `.streamlit/secrets.toml` (excluido de Git) con un conjunto mínimo de 24 filas y 49 columnas. Ese conjunto no tiene números de cuenta ni respuestas abiertas, salvo los nombres de artistas, y su contenido se pega en la configuración de *Secrets* de la app. Ver la sección "Publicar el tablero" del README.


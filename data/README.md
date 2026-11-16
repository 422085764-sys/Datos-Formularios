# Datos

Los datos **no se publican** en este repositorio: las respuestas originales contienen números de cuenta y correos institucionales de los participantes. Solo se versiona la estructura de carpetas.

## Archivos esperados

Para reproducir el proyecto, coloca los cuestionarios originales (exportados de Google Forms) con estos nombres exactos:

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

- `raw/.clave_seudonimo`: clave secreta del seudónimo HMAC. Se crea la primera vez que se ejecuta `notebooks/01_limpieza.ipynb`. Para obtener los mismos identificadores en otra máquina, copia esta clave. **Nunca la publiques.**
- `processed/`: conjuntos limpios (`doc*_clean.csv`), integrados (`integrado_*.csv`) y perfiles (`perfiles.csv`). Los generan los cuadernos 01 a 03. No contienen números de cuenta, pero sí respuestas abiertas, por lo que tampoco se publican.

## Acceso a los datos

Los datos se recolectaron con fines académicos en un grupo de 7.º semestre de MAC, FES Acatlán, UNAM. Para solicitarlos, contacta a los autores del proyecto.

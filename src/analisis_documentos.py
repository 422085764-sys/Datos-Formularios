"""Análisis de los 6 documentos disponibles: de qué tratan, quién los respondió,
qué temas comparten y qué señales muestran. Sirve para justificar el tema y la pregunta del
proyecto y, después, para elegir qué documentos se usan.

Lo usa notebooks/00_analisis_documentos.ipynb. También se puede ejecutar como script:
    python src/analisis_documentos.py
No imprime números de cuenta ni correos (anonimización).
"""
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
# Aceptados en data/raw, rechazados en data/excluded (Fase 1); antes, en la raíz
CARPETAS = [RAIZ / "data" / "raw", RAIZ / "data" / "excluded", RAIZ]

# Documento -> (archivo, columna llave o None si la llave se deriva del correo)
DOCS = {
    1: ("La música y su influencia en el estado de ánimo (respuestas).xlsx", "Número de cuenta"),
    2: ("Cuestionario_ Entorno Universitario y Bienestar.csv", "Ingresa tu número de cuenta"),
    3: ("Desempeño académico por el uso de IA.csv", "Número de cuenta "),
    4: ("Test (Respuestas).xlsx", "Ingresa tu número de cuenta (solo números) "),
    5: ("Pelis y series (Respuestas).xlsx", "1. Número de cuenta"),
    6: ("Relación Amor - Carrera (Respuestas).xlsx", None),  # solo correo
}

NOMBRES = {1: "Música y estado de ánimo", 2: "Entorno universitario y bienestar", 3: "Uso de IA en lo académico",
           4: "Test (personalidad)", 5: "Pelis y series", 6: "Relación amor–carrera"}

# Temas que se buscan en los ENUNCIADOS de las preguntas (no en las respuestas)
TEMAS = {
    "Música": r"musica|cancion|artista",
    "Ánimo y emociones": r"animo|emocion|triste|decaido|desmotiv|feliz|paciencia|irritacion",
    "Estrés y carga": r"estres|carga mental|preocupado",
    "Sueño y descanso": r"sueno|descanso",
    "Concentración y desempeño": r"concentr|tareas|calificacion|academic",
    "Inteligencia artificial": r"\bia\b|inteligencia artificial",
    "Contexto (carrera, semestre, traslado)": r"carrera|semestre|traslad|transporte|vives|edad",
    "Cine y series": r"pelicula|serie|actor|actriz",
    "Pareja": r"pareja|enamorad|cita ideal|carino|amor\b|red flags|no negociables",
    "Personalidad y ocio": r"pasatiempo|deporte|platillo|tiempo libre|decision|en equipo|tus planes|fin de semana",
}


def normalizar(texto) -> str:
    """Minúsculas y sin acentos, para comparar texto sin importar cómo se escribió."""
    t = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def leer(archivo: str) -> pd.DataFrame:
    ruta = next(c / archivo for c in CARPETAS if (c / archivo).exists())
    return pd.read_csv(ruta) if ruta.suffix == ".csv" else pd.read_excel(ruta)


def llave(df: pd.DataFrame, col: str | None) -> pd.Series:
    """Devuelve el número de cuenta; si no existe, lo extrae del prefijo del correo."""
    if col is None:
        return df["Dirección de correo electrónico"].str.extract(r"^(\d+)@")[0].astype("Int64")
    return df[col].astype("Int64")


def columna(df: pd.DataFrame, palabras: str) -> pd.Series:
    """Respuestas (normalizadas) de la única columna cuyo encabezado contiene `palabras`."""
    encontradas = [c for c in df.columns if palabras in normalizar(c)]
    assert len(encontradas) == 1, f"'{palabras}' coincide con {len(encontradas)} columnas"
    return df[encontradas[0]].map(normalizar)


def mapa_de_temas(docs: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """Número de preguntas de cada documento que tocan cada tema (filas: temas, columnas: documentos)."""
    filas = {}
    for tema, patron in TEMAS.items():
        filas[tema] = {n: sum(bool(re.search(patron, normalizar(c))) for c in d.columns[2:]) for n, d in docs.items()}
    tabla = pd.DataFrame(filas).T
    tabla.columns = [f"Doc {n}" for n in tabla.columns]
    return tabla


def perfil(n: int) -> tuple[pd.DataFrame, set]:
    archivo, col = DOCS[n]
    df = leer(archivo)
    k = llave(df, col)
    print(f"\n=== Doc {n}: {archivo} ===")
    print(f"shape={df.shape} | llave únicos={k.nunique()} | llave duplicados={k.duplicated().sum()}")
    return df, set(k.dropna().astype(int))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # consola de Windows
    datos, llaves = {}, {}
    for n in DOCS:
        datos[n], llaves[n] = perfil(n)
    print("\n=== Preguntas por tema ===")
    print(mapa_de_temas(datos).to_string())
    inter = pd.DataFrame([[len(llaves[a] & llaves[b]) for b in DOCS] for a in DOCS],
                         index=[f"Doc{n}" for n in DOCS], columns=[f"Doc{n}" for n in DOCS])
    print("\n=== Intersección de números de cuenta ===")
    print(inter.to_string())

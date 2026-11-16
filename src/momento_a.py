"""Momento A — Perfilado de los 6 documentos y matriz de relación.

Ejecutar desde la raíz del proyecto:
    python src/momento_a.py
No imprime números de cuenta ni correos (anonimización).
"""
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw" if (RAIZ / "data" / "raw").exists() else RAIZ

# Documento -> (archivo, columna llave o None si la llave se deriva del correo)
DOCS = {
    1: ("La música y su influencia en el estado de ánimo (respuestas).xlsx", "Número de cuenta"),
    2: ("Cuestionario_ Entorno Universitario y Bienestar.csv", "Ingresa tu número de cuenta"),
    3: ("Desempeño académico por el uso de IA.csv", "Número de cuenta "),
    4: ("Test (Respuestas).xlsx", "Ingresa tu número de cuenta (solo números) "),
    5: ("Pelis y series (Respuestas).xlsx", "1. Número de cuenta"),
    6: ("Relación Amor - Carrera (Respuestas).xlsx", None),  # solo correo
}


def leer(archivo: str) -> pd.DataFrame:
    ruta = RAW / archivo
    return pd.read_csv(ruta) if ruta.suffix == ".csv" else pd.read_excel(ruta)


def llave(df: pd.DataFrame, col: str | None) -> pd.Series:
    """Devuelve el número de cuenta; si no existe, lo extrae del prefijo del correo."""
    if col is None:
        return df["Dirección de correo electrónico"].str.extract(r"^(\d+)@")[0].astype("Int64")
    return df[col].astype("Int64")


def perfil(n: int) -> tuple[pd.DataFrame, set]:
    archivo, col = DOCS[n]
    df = leer(archivo)
    k = llave(df, col)
    print(f"\n=== Doc {n}: {archivo} ===")
    print(f"shape={df.shape} | llave únicos={k.nunique()} | llave duplicados={k.duplicated().sum()}")
    tabla = pd.DataFrame({
        "tipo": df.dtypes.astype(str),
        "nulos": df.isna().sum(),
        "únicos": df.nunique(),
    })
    tabla.index = [c[:70] for c in tabla.index]
    print(tabla.to_string())
    return df, set(k.dropna().astype(int))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # consola de Windows
    llaves = {n: perfil(n)[1] for n in DOCS}
    inter = pd.DataFrame(
        [[len(llaves[a] & llaves[b]) for b in DOCS] for a in DOCS],
        index=[f"Doc{n}" for n in DOCS], columns=[f"Doc{n}" for n in DOCS],
    )
    print("\n=== Intersección de números de cuenta ===")
    print(inter.to_string())
    print("Doc1 ∩ Doc2 ∩ Doc3 =", len(llaves[1] & llaves[2] & llaves[3]))

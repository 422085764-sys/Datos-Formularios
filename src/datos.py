"""Rutas del proyecto, lectura de los documentos aceptados y perfilado.

Funciones reutilizadas por los notebooks (00_perfil_aceptados, 01_limpieza, ...).
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from diccionario import DICCIONARIO

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
PROCESSED = RAIZ / "data" / "processed"
EXCLUDED = RAIZ / "data" / "excluded"
DOCS_DIR = RAIZ / "docs"

# Documentos aceptados en el Momento A (id -> metadatos)
ACEPTADOS = {
    1: {"nombre": "Música y estado de ánimo", "rol": "Principal", "prefijo": "m_",
        "archivo": "La música y su influencia en el estado de ánimo (respuestas).xlsx"},
    2: {"nombre": "Entorno universitario y bienestar", "rol": "Complementario fuerte", "prefijo": "b_",
        "archivo": "Cuestionario_ Entorno Universitario y Bienestar.csv"},
    3: {"nombre": "Desempeño académico por el uso de IA", "rol": "Complementario medio", "prefijo": "ia_",
        "archivo": "Desempeño académico por el uso de IA.csv"},
}


def leer_crudo(doc: int) -> pd.DataFrame:
    """Lee el archivo original sin modificaciones."""
    ruta = RAW / ACEPTADOS[doc]["archivo"]
    return pd.read_csv(ruta) if ruta.suffix == ".csv" else pd.read_excel(ruta)


def cargar(doc: int) -> pd.DataFrame:
    """Lee el documento y renombra sus columnas a nombres cortos según el diccionario.

    El renombrado es posicional y valida que el número de columnas coincida, para que
    un cambio en el formulario no produzca una asignación silenciosa incorrecta.
    """
    df = leer_crudo(doc)
    dic = DICCIONARIO[DICCIONARIO["doc"] == doc]
    if len(dic) != df.shape[1]:
        raise ValueError(f"Doc {doc}: {df.shape[1]} columnas vs {len(dic)} en el diccionario")
    df.columns = dic["variable"].tolist()
    df["cuenta"] = df["cuenta"].astype("Int64")
    return df


def parsear_marca_temporal(s: pd.Series) -> pd.Series:
    """Convierte marcas de Google Forms a datetime.

    Los .xlsx ya traen datetime; los .csv traen texto como
    '2026/11/01 12:33:29 a.m. GMT-6'.
    """
    if pd.api.types.is_datetime64_any_dtype(s):
        return s
    t = (s.astype(str)
         .str.replace(r"\s*GMT[+-]\d+", "", regex=True)
         .str.replace(r"a\.\s*m\.", "AM", regex=True)
         .str.replace(r"p\.\s*m\.", "PM", regex=True))
    return pd.to_datetime(t, format="%Y/%m/%d %I:%M:%S %p", errors="coerce")


def _palabras(s: pd.Series) -> float:
    txt = s.dropna().astype(str)
    return round(txt.map(lambda x: len(re.findall(r"\w+", x))).mean(), 1) if len(txt) else 0.0


def perfil_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """Tipo, nulos, cardinalidad y longitud media (en palabras) de cada variable."""
    return pd.DataFrame({
        "tipo_pandas": df.dtypes.astype(str),
        "nulos": df.isna().sum(),
        "pct_nulos": (df.isna().mean() * 100).round(1),
        "unicos": df.nunique(),
        "pct_unicos": (df.nunique() / len(df) * 100).round(1),
        "palabras_prom": [(_palabras(df[c]) if c != "marca_temporal" and df[c].dtype != "Int64" else None)
                          for c in df.columns],
    })


def perfil_documento(doc: int, df: pd.DataFrame) -> dict:
    """Resumen estructural de un documento (sin exponer llaves)."""
    fechas = parsear_marca_temporal(df["marca_temporal"])
    texto = [c for c in df.columns if pd.api.types.is_string_dtype(df[c])]
    return {
        "doc": doc,
        "documento": ACEPTADOS[doc]["nombre"],
        "rol": ACEPTADOS[doc]["rol"],
        "registros": len(df),
        "variables": df.shape[1],
        "vars_texto": len(texto),
        "celdas_nulas": int(df.isna().sum().sum()),
        "filas_duplicadas": int(df.drop(columns="marca_temporal").duplicated().sum()),
        "cuentas_duplicadas": int(df["cuenta"].duplicated().sum()),
        "cuentas_no_9_digitos": int((df["cuenta"].astype(str).str.len() != 9).sum()),
        "fecha_min": fechas.min().date(),
        "fecha_max": fechas.max().date(),
    }

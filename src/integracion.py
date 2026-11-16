"""Integración de los documentos limpios (Fase 4)."""
from __future__ import annotations

import pandas as pd

from datos import PROCESSED

ARCHIVOS = {1: "doc1_musica_clean.csv", 2: "doc2_bienestar_clean.csv", 3: "doc3_ia_clean.csv"}


def cargar_limpios() -> dict[int, pd.DataFrame]:
    """Lee los conjuntos _clean y prefija las columnas comunes para evitar colisiones."""
    dfs = {}
    for d, archivo in ARCHIVOS.items():
        df = pd.read_csv(PROCESSED / archivo)
        df = df.rename(columns={"marca_temporal": f"marca_temporal_d{d}"})
        if d == 3 and "sospecha_copia" in df.columns:  # misma bandera que en el doc 1
            df = df.rename(columns={"sospecha_copia": "sospecha_copia_d3"})
        dfs[d] = df
    return dfs


def integrar(dfs: dict[int, pd.DataFrame], docs: tuple[int, ...]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Unión interna por seudónimo y reporte de registros conservados y perdidos por documento."""
    base = dfs[docs[0]]
    for d in docs[1:]:
        base = base.merge(dfs[d], on="id", how="inner", validate="one_to_one")
    reporte = pd.DataFrame({
        "registros": {f"Doc {d}": len(dfs[d]) for d in docs},
        "conservados": {f"Doc {d}": int(dfs[d]["id"].isin(base["id"]).sum()) for d in docs},
    })
    reporte["perdidos"] = reporte["registros"] - reporte["conservados"]
    reporte["pct_conservado"] = (reporte["conservados"] / reporte["registros"] * 100).round(1)
    return base, reporte

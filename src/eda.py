"""Pruebas estadísticas para el EDA (Fase 4).

Todas las funciones devuelven diccionarios homogéneos (prueba, n, estadístico, p, efecto)
para poder reunirlas en una sola tabla y corregir por comparaciones múltiples.
Con muestras de ~19 casos se privilegian pruebas no paramétricas y exactas.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def spearman(df: pd.DataFrame, x: str, y: str, hipotesis: str = "") -> dict:
    d = df[[x, y]].dropna().astype(float)
    rho, p = stats.spearmanr(d[x], d[y]) if len(d) > 2 else (np.nan, np.nan)
    return {"hipótesis": hipotesis, "prueba": "Spearman", "x": x, "y": y, "n": len(d),
            "estadístico": rho, "p": p, "efecto": rho, "medida_efecto": "rho"}


def mann_whitney(df: pd.DataFrame, grupo: str, y: str, hipotesis: str = "") -> dict:
    """Compara y entre los dos niveles de `grupo`. Efecto: correlación biserial de rangos."""
    d = df[[grupo, y]].dropna()
    niveles = sorted(d[grupo].unique())
    if len(niveles) != 2:
        return {"hipótesis": hipotesis, "prueba": "Mann-Whitney", "x": grupo, "y": y, "n": len(d),
                "estadístico": np.nan, "p": np.nan, "efecto": np.nan, "medida_efecto": "r_rb"}
    a = d.loc[d[grupo] == niveles[0], y].astype(float)
    b = d.loc[d[grupo] == niveles[1], y].astype(float)
    u, p = stats.mannwhitneyu(b, a, alternative="two-sided", method="auto")
    r_rb = 2 * u / (len(a) * len(b)) - 1  # > 0: el grupo de nivel mayor tiende a valores mayores
    return {"hipótesis": hipotesis, "prueba": "Mann-Whitney", "x": grupo, "y": y, "n": len(d),
            "detalle": f"n={len(a)}/{len(b)}; mediana {a.median():.2f} vs {b.median():.2f}",
            "estadístico": u, "p": p, "efecto": r_rb, "medida_efecto": "r_rb"}


def fisher_2x2(df: pd.DataFrame, x: str, y: str, hipotesis: str = "") -> dict:
    """Prueba exacta de Fisher para dos variables binarias. Efecto: razón de momios (con +0.5)."""
    d = df[[x, y]].dropna().astype(int)
    tabla = pd.crosstab(d[x], d[y]).reindex(index=[0, 1], columns=[0, 1], fill_value=0)
    _, p = stats.fisher_exact(tabla.values)
    t = tabla.values + 0.5  # corrección de Haldane-Anscombe para celdas en cero
    or_ = (t[1, 1] * t[0, 0]) / (t[1, 0] * t[0, 1])
    return {"hipótesis": hipotesis, "prueba": "Fisher exacta", "x": x, "y": y, "n": len(d),
            "detalle": f"tabla {tabla.values.tolist()}",
            "estadístico": np.nan, "p": p, "efecto": or_, "medida_efecto": "OR"}


def kruskal(df: pd.DataFrame, grupo: str, y: str, hipotesis: str = "", min_n: int = 3) -> dict:
    """Kruskal-Wallis entre grupos con al menos `min_n` casos. Efecto: épsilon cuadrado."""
    d = df[[grupo, y]].dropna()
    conteo = d[grupo].value_counts()
    d = d[d[grupo].isin(conteo[conteo >= min_n].index)]
    grupos = [g[y].astype(float).values for _, g in d.groupby(grupo)]
    if len(grupos) < 2:
        return {"hipótesis": hipotesis, "prueba": "Kruskal-Wallis", "x": grupo, "y": y, "n": len(d),
                "estadístico": np.nan, "p": np.nan, "efecto": np.nan, "medida_efecto": "ε²"}
    h, p = stats.kruskal(*grupos)
    eps2 = h / ((len(d) ** 2 - 1) / (len(d) + 1))
    return {"hipótesis": hipotesis, "prueba": "Kruskal-Wallis", "x": grupo, "y": y, "n": len(d),
            "detalle": f"{len(grupos)} grupos con n≥{min_n}",
            "estadístico": h, "p": p, "efecto": eps2, "medida_efecto": "ε²"}


def chi2_independencia(df: pd.DataFrame, x: str, y: str, hipotesis: str = "") -> dict:
    """Ji-cuadrada de independencia. Efecto: V de Cramér. Reporta el % de celdas esperadas < 5."""
    d = df[[x, y]].dropna()
    tabla = pd.crosstab(d[x], d[y])
    chi2, p, _, esperadas = stats.chi2_contingency(tabla, correction=False)
    k = min(tabla.shape) - 1
    v = np.sqrt(chi2 / (len(d) * k)) if k > 0 else np.nan
    return {"hipótesis": hipotesis, "prueba": "Ji-cuadrada", "x": x, "y": y, "n": len(d),
            "detalle": f"{(esperadas < 5).mean() * 100:.0f}% celdas esperadas < 5",
            "estadístico": chi2, "p": p, "efecto": v, "medida_efecto": "V de Cramér"}


def tabla_resultados(filas: list[dict]) -> pd.DataFrame:
    """Reúne los resultados y agrega q de Benjamini-Hochberg sobre las pruebas con p válido."""
    t = pd.DataFrame(filas)
    if "detalle" not in t:
        t["detalle"] = ""
    validos = t["p"].notna()
    t["q_BH"] = np.nan
    if validos.any():
        t.loc[validos, "q_BH"] = stats.false_discovery_control(t.loc[validos, "p"].values, method="bh")
    cols = ["hipótesis", "prueba", "x", "y", "n", "detalle", "estadístico", "p", "q_BH", "efecto", "medida_efecto"]
    return t[cols].round({"estadístico": 3, "p": 4, "q_BH": 4, "efecto": 3})


def matriz_spearman(df: pd.DataFrame, variables: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Matriz de rho de Spearman (por pares completos) y matriz de p."""
    v = df[variables].astype(float)
    rho = pd.DataFrame(np.nan, index=variables, columns=variables)
    pv = rho.copy()
    for i, a in enumerate(variables):
        for b in variables[i:]:
            d = v[[a, b]].dropna()
            r, p = stats.spearmanr(d[a], d[b]) if a != b else (1.0, 0.0)
            rho.loc[a, b] = rho.loc[b, a] = r
            pv.loc[a, b] = pv.loc[b, a] = p
    return rho, pv

"""Gráficas estáticas (matplotlib) con una paleta validada para daltonismo.

Paleta de referencia (modo claro):
- Categórica, en orden fijo: azul, naranja, aqua (los 3 primeros espacios validan todos
  los pares para CVD; con más series se agrupa en "otros").
- Secuencial/ordinal: rampa azul (pasos 250 a 650).
- Divergente: azul <-> rojo con punto medio gris neutro.
- Texto con tintas neutras, nunca con el color de la serie; cuadrícula y ejes recesivos.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator

SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
TENUE = "#898781"
CUADRICULA = "#e1e0d9"
EJE = "#c3c2b7"
CATEGORICA = ["#2a78d6", "#eb6834", "#1baf7a"]
ORDINAL_AZUL = ["#86b6ef", "#3987e5", "#256abf", "#104281"]
DIVERGENTE = LinearSegmentedColormap.from_list(
    "azul_rojo", ["#1c5cab", "#86b6ef", "#f0efec", "#ef9a99", "#c22f2f"])

plt.rcParams.update({
    "figure.facecolor": SUPERFICIE, "axes.facecolor": SUPERFICIE, "savefig.facecolor": SUPERFICIE,
    "font.family": "DejaVu Sans", "font.size": 9.5, "text.color": TINTA,
    "axes.labelcolor": TINTA_2, "axes.edgecolor": EJE, "axes.linewidth": 0.8,
    "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.titlecolor": TINTA, "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": TENUE, "ytick.color": TENUE, "xtick.labelcolor": TINTA_2, "ytick.labelcolor": TINTA_2,
    "axes.grid": True, "grid.color": CUADRICULA, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "legend.frameon": False, "figure.dpi": 110,
})


def guardar(fig, ruta: Path) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=160, bbox_inches="tight")
    return ruta


def barras_h(conteos: pd.Series, titulo: str, xlabel: str, color: str = CATEGORICA[0],
             total: int | None = None):
    """Barras horizontales de una sola serie, ordenadas, con etiqueta 'n (%)' en el extremo."""
    conteos = conteos.sort_values()
    fig, ax = plt.subplots(figsize=(6.4, 0.38 * len(conteos) + 1.0))
    ax.barh(conteos.index, conteos.values, color=color, height=0.55)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel(xlabel)
    ax.set_title(titulo)
    tope = conteos.max()
    for i, v in enumerate(conteos.values):
        etiqueta = f"{v:g}" + (f" ({v / total:.0%})" if total else "")
        ax.text(v + tope * 0.015, i, etiqueta, va="center", fontsize=8.5, color=TINTA_2)
    ax.set_xlim(0, tope * 1.22)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    return fig, ax


def puntos_por_grupo(df: pd.DataFrame, grupo: str, y: str, orden: list, etiquetas: list[str],
                     titulo: str, ylabel: str, semilla: int = 42):
    """Diagrama de puntos con dispersión horizontal y mediana por grupo (útil con n pequeño)."""
    rng = np.random.default_rng(semilla)
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    for i, (nivel, etiqueta) in enumerate(zip(orden, etiquetas)):
        vals = df.loc[df[grupo] == nivel, y].dropna().astype(float)
        x = i + rng.uniform(-0.2, 0.2, len(vals))
        ax.scatter(x, vals, s=46, color=CATEGORICA[i % 3], edgecolor=SUPERFICIE, linewidth=1.5, zorder=3)
        if len(vals):
            ax.hlines(vals.median(), i - 0.28, i + 0.28, color=TINTA, linewidth=2, zorder=4)
            ax.text(i + 0.31, vals.median(), f"mediana {vals.median():.2g}", va="center",
                    fontsize=8, color=TINTA_2)
        etiquetas[i] = f"{etiqueta}\n(n = {len(vals)})"
    ax.set_xticks(range(len(orden)), etiquetas)
    ax.set_xlim(-0.5, len(orden) - 0.1)
    ax.grid(axis="x", visible=False)
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    return fig, ax


def heatmap_spearman(rho: pd.DataFrame, pv: pd.DataFrame, etiquetas: dict[str, str], titulo: str):
    """Matriz triangular de Spearman en escala divergente; * marca p < 0.05 sin corregir."""
    # Triángulo inferior sin diagonal: se omiten la primera fila y la última columna (vacías)
    rho, pv = rho.iloc[1:, :-1], pv.iloc[1:, :-1]
    n = len(rho)
    mascara = np.triu(np.ones((n, n), dtype=bool), k=1)
    datos = np.ma.array(rho.values, mask=mascara)
    fig, ax = plt.subplots(figsize=(7.6, 6.4))
    im = ax.imshow(datos, cmap=DIVERGENTE, vmin=-1, vmax=1)
    ax.set_xticks(range(n), [etiquetas.get(c, c) for c in rho.columns], rotation=55, ha="right")
    ax.set_yticks(range(n), [etiquetas.get(c, c) for c in rho.index])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    for i in range(n):
        for j in range(i + 1):
            r, p = rho.iat[i, j], pv.iat[i, j]
            if pd.notna(r):
                ax.text(j, i, f"{r:.2f}{'*' if p < 0.05 else ''}", ha="center", va="center", fontsize=7,
                        color="#ffffff" if abs(r) > 0.55 else TINTA)
    cb = fig.colorbar(im, ax=ax, shrink=0.7)
    cb.set_label("ρ de Spearman")
    cb.outline.set_visible(False)
    ax.set_title(titulo)
    return fig, ax


def linea_metrica(x, y, titulo: str, xlabel: str, ylabel: str, destacar=None, referencia=None):
    """Una métrica por k (una sola escala); marca opcional del k elegido y línea de referencia."""
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    ax.plot(x, y, color=CATEGORICA[0], linewidth=2, marker="o", markersize=7,
            markeredgecolor=SUPERFICIE, markeredgewidth=1.5, zorder=3)
    if referencia is not None:
        ax.axhline(referencia, color=TENUE, linewidth=1, linestyle="--")
        ax.text(x[0], referencia, f"referencia {referencia}", ha="left", va="bottom", fontsize=8, color=TENUE)
    if destacar is not None:
        i = list(x).index(destacar)
        ax.scatter([x[i]], [y[i]], s=140, facecolor="none", edgecolor=TINTA, linewidth=1.5, zorder=4)
        ax.annotate(f"k = {destacar}", (x[i], y[i]), xytext=(12, -14), textcoords="offset points",
                    fontsize=8.5, color=TINTA_2)
    ax.set_xticks(list(x))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    return fig, ax


def heatmap_perfiles(medias_z: pd.DataFrame, etiquetas: dict[str, str], titulo: str, anotaciones=None):
    """Medias estandarizadas por perfil (filas = variables, columnas = perfiles), escala divergente."""
    fig, ax = plt.subplots(figsize=(6.2, 0.42 * len(medias_z) + 1.4))
    lim = max(1.0, float(np.nanmax(np.abs(medias_z.values))))
    im = ax.imshow(medias_z.values, cmap=DIVERGENTE, vmin=-lim, vmax=lim, aspect="auto")
    ax.set_yticks(range(len(medias_z)), [etiquetas.get(i, i) for i in medias_z.index])
    ax.set_xticks(range(medias_z.shape[1]), medias_z.columns)
    ax.xaxis.tick_top()
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    textos = anotaciones if anotaciones is not None else medias_z.round(2).astype(str)
    for i in range(medias_z.shape[0]):
        for j in range(medias_z.shape[1]):
            v = medias_z.iat[i, j]
            ax.text(j, i, textos.iat[i, j], ha="center", va="center", fontsize=8,
                    color="#ffffff" if abs(v) > 0.65 * lim else TINTA)
    cb = fig.colorbar(im, ax=ax, shrink=0.8)
    cb.set_label("Media estandarizada (z)")
    cb.outline.set_visible(False)
    ax.set_title(titulo, pad=28)
    return fig, ax


def dispersion_por_grupo(df: pd.DataFrame, x: str, y: str, grupo: str, niveles: list, etiquetas: list[str],
                         titulo: str, xlabel: str, ylabel: str):
    """Dispersión con hasta 3 grupos y recta de tendencia (mínimos cuadrados) por grupo."""
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    for i, (nivel, etiqueta) in enumerate(zip(niveles, etiquetas)):
        d = df.loc[df[grupo] == nivel, [x, y]].dropna().astype(float)
        ax.scatter(d[x], d[y], s=48, color=CATEGORICA[i], edgecolor=SUPERFICIE, linewidth=1.5, zorder=3,
                   label=f"{etiqueta} (n = {len(d)})")
        if len(d) >= 3 and d[x].nunique() > 1:
            b, a = np.polyfit(d[x], d[y], 1)
            xs = np.linspace(d[x].min(), d[x].max(), 20)
            ax.plot(xs, a + b * xs, color=CATEGORICA[i], linewidth=2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    return fig, ax

"""Análisis descriptivo de texto libre con NLTK (Fase 4, complemento).

Se usan solo componentes de NLTK que no requieren descargar corpus (tokenizador por
expresión regular, FreqDist y bigramas), con una lista propia de palabras vacías en español.
"""
from __future__ import annotations

import re
from collections import Counter

import pandas as pd
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.util import bigrams

from limpieza import normalizar

PALABRAS_VACIAS = set("""
a al algo algun alguna algunas alguno algunos ante antes aun aunque bien cada casi como con contra cual
cuando de del desde donde dos e el ella ellas ellos en entre era es esa esas ese eso esos esta estas este
esto estos fue ha hace hacer hacia han hasta hay he la las le les lo los mas me mi mis mucho muy
nada ni no nos o otra otras otro otros para pero poco por porque pues que se sea ser si sin sobre solo
son su sus tambien tan tanto te tener tengo ti tiene todo todos tu un una uno unos usar uso y ya yo
puede pueden puedo hago veces vez asi mismo cosas cosa ademas siempre ia
""".split())

_TOKENIZADOR = RegexpTokenizer(r"[a-zñ]{3,}")


def tokens(texto) -> list[str]:
    t = normalizar(texto)
    return [w for w in _TOKENIZADOR.tokenize(t or "") if w not in PALABRAS_VACIAS]


def frecuencias(serie: pd.Series, n: int = 10, min_freq: int = 2) -> pd.DataFrame:
    """Palabras y bigramas más frecuentes de una pregunta abierta (frecuencia >= min_freq)."""
    toks = [tokens(x) for x in serie.dropna()]
    palabras = FreqDist(w for t in toks for w in t)
    pares = FreqDist(" ".join(b) for t in toks for b in bigrams(t))
    # documentos que mencionan cada palabra (más robusto que la frecuencia bruta con n pequeño)
    docs = Counter(w for t in toks for w in set(t))
    top = [(w, f, docs[w]) for w, f in palabras.most_common(n) if f >= min_freq]
    top_b = [(b, f) for b, f in pares.most_common(n) if f >= min_freq]
    filas = max(len(top), len(top_b))
    return pd.DataFrame({
        "palabra": [x[0] for x in top] + [""] * (filas - len(top)),
        "frecuencia": [x[1] for x in top] + [None] * (filas - len(top)),
        "respuestas": [x[2] for x in top] + [None] * (filas - len(top)),
        "bigrama": [x[0] for x in top_b] + [""] * (filas - len(top_b)),
        "frecuencia_bigrama": [x[1] for x in top_b] + [None] * (filas - len(top_b)),
    })


def artistas(serie: pd.Series, min_menciones: int = 2) -> pd.Series:
    """Cuenta artistas mencionados (lista libre separada por comas, saltos de línea, 'y' o números)."""
    conteo = Counter()
    for x in serie.dropna():
        t = normalizar(x) or ""
        t = re.sub(r"del resto.*$|no conozco.*$", "", t)
        partes = re.split(r",|;|\n|\s+y\s+|\d+\.\s*|\s{2,}", t)
        vistos = set()
        for p in partes:
            p = re.sub(r"[^a-z0-9ñ&' ]", "", p).strip()
            if 2 <= len(p) <= 40 and p not in vistos:
                vistos.add(p)
                conteo[p] += 1
    s = pd.Series(conteo, dtype=int).sort_values(ascending=False)
    return s[s >= min_menciones]

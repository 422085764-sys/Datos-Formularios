"""Funciones de limpieza y codificación (Fase 3).

Principios:
- Las reglas son explícitas (expresiones regulares en orden de prioridad: gana la primera
  que coincide) para que cualquier persona pueda auditar cómo se codificó cada respuesta.
- Si ninguna regla aplica, el resultado es NaN (faltante). Nunca se imputa un valor.
- Toda la comparación se hace sobre texto normalizado (minúsculas, sin acentos, NFKD).
"""
from __future__ import annotations

import hashlib
import hmac
import re
import secrets
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------------------
# Normalización de texto
# --------------------------------------------------------------------------------------

def normalizar(texto) -> str | None:
    """Minúsculas, sin acentos (NFKD), sin saltos de línea ni espacios repetidos."""
    if texto is None or (isinstance(texto, float) and np.isnan(texto)) or pd.isna(texto):
        return None
    t = unicodedata.normalize("NFKD", str(texto))
    t = "".join(ch for ch in t if not unicodedata.combining(ch)).lower()
    t = re.sub(r"\s+", " ", t).strip()
    return t or None


def codificar(texto, reglas: list[tuple[str, object]]):
    """Aplica reglas (regex, valor) en orden; devuelve el valor de la primera coincidencia.

    `valor` puede ser una función que recibe el objeto Match (para reglas numéricas).
    """
    t = normalizar(texto)
    if t is None:
        return np.nan
    for patron, valor in reglas:
        m = re.search(patron, t)
        if m:
            return valor(m) if callable(valor) else valor
    return np.nan


def banderas(texto, grupos: dict[str, str]) -> dict[str, float]:
    """Devuelve 1/0 por grupo según si el patrón aparece en el texto (NaN si no hay texto)."""
    t = normalizar(texto)
    return {g: (np.nan if t is None else float(bool(re.search(p, t)))) for g, p in grupos.items()}


# --------------------------------------------------------------------------------------
# Números escritos y duraciones
# --------------------------------------------------------------------------------------

_NUMEROS = {
    "media": "0.5", "una": "1", "uno": "1", "un": "1", "dos": "2", "tres": "3", "cuatro": "4",
    "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9", "diez": "10",
    "veintiuno": "21", "veintidos": "22", "veintitres": "23", "veinticuatro": "24",
    "veinticinco": "25", "veintiseis": "26",
}


def palabras_a_numeros(t: str) -> str:
    return re.sub(r"\b(" + "|".join(sorted(_NUMEROS, key=len, reverse=True)) + r")\b",
                  lambda m: _NUMEROS[m.group(1)], t)


def a_horas(texto) -> float:
    """Convierte una duración escrita a horas.

    Reglas (en orden): sin escucha -> 0; 'menos de 1' -> 0.5; minutos explícitos -> /60;
    'h y media' -> h + 0.5; 'h horas y m minutos' -> h + m/60; rangos 'a-b', 'a o b',
    'entre a y b', 'a a b' -> punto medio; 'x o más' -> x (cota inferior); en otro caso,
    el primer número.
    """
    t = normalizar(texto)
    if t is None:
        return np.nan
    if re.search(r"no escucho|^0$", t):
        return 0.0
    t = palabras_a_numeros(t)
    if re.search(r"menos de 1", t):
        return 0.5
    t = re.sub(r"(\d)\s*(hrs?|h)\b", r"\1 horas", t)
    m = re.search(r"(\d+(?:\.\d+)?)\s*horas? y (\d+)\s*min", t)
    if m:
        return float(m.group(1)) + float(m.group(2)) / 60
    m = re.search(r"(\d+)\s*horas? y 0\.5", t) or re.search(r"(\d+)\s*horas? y media", t)
    if m:
        return float(m.group(1)) + 0.5
    if re.search(r"^1?\s*hora y (0\.5|media)", t) or re.search(r"\bhora y (0\.5|media)", t):
        return 1.5
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|o|a|y)\s*(\d+(?:\.\d+)?)", t)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        return (a + b) / 2
    m = re.search(r"(\d+(?:\.\d+)?)\s*(m\b|min)", t)
    if m:
        return float(m.group(1)) / 60
    m = re.search(r"(\d+(?:\.\d+)?)", t)
    if m:
        return float(m.group(1))
    if re.search(r"\bhora\b", t):
        return 1.0
    return np.nan


def a_minutos(texto) -> float:
    h = a_horas(texto)
    return h * 60 if not np.isnan(h) else np.nan


def a_entero(texto) -> float:
    t = normalizar(texto)
    if t is None:
        return np.nan
    m = re.search(r"\d+", palabras_a_numeros(t))
    return float(m.group()) if m else np.nan


_ORDINALES = {"primer": 1, "segund": 2, "tercer": 3, "cuart": 4, "quint": 5, "sext": 6,
              "septim": 7, "setim": 7, "octav": 8}


def a_semestre(texto, semestre_actual: int = 7) -> float:
    """Semestre a partir de número u ordinal escrito; 'hace k semestres' -> actual - k."""
    t = normalizar(texto)
    if t is None:
        return np.nan
    m = re.search(r"hace (\d+)", t)
    if m:
        return float(semestre_actual - int(m.group(1)))
    m = re.search(r"\d+", t)
    if m:
        return float(m.group())
    for raiz, n in _ORDINALES.items():
        if raiz in t:
            return float(n)
    return np.nan


def escala_10(m, niveles: int) -> int:
    """Convierte una calificación x/10 a una escala 0..niveles-1 (redondeo)."""
    x = float(m.group(1))
    return int(round(min(x, 10) / 10 * (niveles - 1)))


# --------------------------------------------------------------------------------------
# Calidad: atípicos, copias y seudónimos
# --------------------------------------------------------------------------------------

def atipicos_iqr(s: pd.Series, k: float = 1.5) -> pd.Series:
    """Marca valores fuera de [Q1 - k·IQR, Q3 + k·IQR]. No modifica los valores."""
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return ((s < q1 - k * iqr) | (s > q3 + k * iqr)).astype("Int64").where(s.notna())


def respuestas_copiadas(df: pd.DataFrame, columnas: list[str], min_palabras: int = 5) -> pd.Series:
    """Cuenta, por fila, las respuestas abiertas idénticas a la de otro estudiante.

    Solo considera respuestas de al menos `min_palabras` palabras, para no contar
    coincidencias naturales en respuestas cortas ("El ritmo", "Muy fácilmente").
    """
    n = pd.Series(0, index=df.index)
    for c in columnas:
        s = df[c].map(normalizar)
        largas = s[s.fillna("").str.split().str.len() >= min_palabras]
        n.loc[largas[largas.duplicated(keep=False)].index] += 1
    return n


def clave_seudonimo(ruta: Path) -> bytes:
    """Lee (o crea una sola vez) la clave secreta para seudonimizar. Vive en data/ (fuera de Git)."""
    if not ruta.exists():
        ruta.write_text(secrets.token_hex(32), encoding="utf-8")
    return bytes.fromhex(ruta.read_text(encoding="utf-8").strip())


def seudonimo(cuenta, clave: bytes) -> str | None:
    """HMAC-SHA256 del número de cuenta, truncado a 12 caracteres hexadecimales.

    Es determinista (la misma cuenta produce el mismo id en los tres documentos, lo que
    permite la integración) e irreversible sin la clave.
    """
    if pd.isna(cuenta):
        return None
    return hmac.new(clave, str(int(cuenta)).encode(), hashlib.sha256).hexdigest()[:12]

"""Datos y cálculo de indicadores para el tablero (Fase 6).

Separado de app/app.py para poder probar los KPI sin interfaz. Las definiciones siguen
docs/negocio.md §9.4: cada indicador reporta su n, los porcentajes van con el conteo
absoluto y no se muestran categorías con menos de MIN_N estudiantes.
"""
from __future__ import annotations

import pandas as pd

from datos import PROCESSED

MIN_N = 3  # umbral de protección contra la reidentificación y de estabilidad mínima

GENEROS = {"rock_metal": "Rock / metal", "pop": "Pop", "electronica": "Electrónica", "urbano": "Urbano",
           "regional": "Regional mexicano", "variado": "Variado", "no_escucha": "No escucha"}
MODALIDAD = {"guia": "Guía para aprender", "ambas": "Guía y atajo / atajo", "atajo": "Guía y atajo / atajo"}
NIVELES_IEP = ["bajo", "medio", "alto"]
NIVELES_HORAS = ["baja", "media", "alta"]
MOMENTOS = {"mom_traslado": "Traslado", "mom_estudio": "Estudio / tarea", "mom_ejercicio": "Ejercicio",
            "mom_descanso": "Descanso", "mom_hogar": "Labores del hogar", "mom_trabajo": "Trabajo",
            "mom_todo_el_dia": "Todo el día"}


def cargar_base() -> pd.DataFrame:
    """Una fila por estudiante con Doc 1 + Doc 3 (n = 24), bienestar del Doc 2 y perfil, si existen.

    Se parte de música + IA para que los KPI 1 y 2 usen a todos los que respondieron el Doc 1;
    las variables del Doc 2 quedan vacías para quien no lo respondió.
    """
    base = pd.read_csv(PROCESSED / "integrado_13.csv")
    bienestar = pd.read_csv(PROCESSED / "doc2_bienestar_clean.csv")
    cols_b = ["id", "b_semestre_cod", "iep", "iep_nivel", "b_sueno_calidad_cod", "b_concentracion_dif_cod",
              "b_traslado_min_cod", "b_desanimo_cod", "b_irritabilidad_cod"]
    base = base.merge(bienestar[cols_b], on="id", how="left", validate="one_to_one")
    perfiles = pd.read_csv(PROCESSED / "perfiles.csv")
    base = base.merge(perfiles, on="id", how="left", validate="one_to_one")
    base["genero"] = base["m_genero_grupo"].map(GENEROS)
    base["modalidad_ia"] = base["ia_guia_vs_atajo_cod"].map(MODALIDAD)
    base["en_nucleo"] = base["iep"].notna() | base["b_semestre_cod"].notna()
    return base


def filtrar(base: pd.DataFrame, generos=None, semestres=None, horas=None, estres=None, modalidades=None):
    """Aplica los filtros. Los filtros del Doc 2 (semestre, estrés) excluyen a quien no lo respondió."""
    d = base
    if generos:
        d = d[d["genero"].isin(generos)]
    if semestres:
        d = d[d["b_semestre_cod"].isin(semestres)]
    if horas is not None:
        d = d[d["m_horas"].between(horas[0], horas[1])]
    if estres:
        d = d[d["iep_nivel"].isin(estres)]
    if modalidades:
        d = d[d["modalidad_ia"].isin(modalidades)]
    return d


def pct(k: int, n: int) -> str:
    return f"{k / n:.0%} ({k} de {n})" if n else "sin datos"


# ------------------------------------------------------------------------------------------
# KPI
# ------------------------------------------------------------------------------------------

def kpi1_mejora(d: pd.DataFrame) -> dict:
    """% que reporta mejora de ánimo con música (sobre respuestas codificables)."""
    y = d["mejora_animo"].dropna()
    return {"valor": y.mean() if len(y) else None, "k": int(y.sum()), "n": len(y), "texto": pct(int(y.sum()), len(y))}


def kpi2_horas(d: pd.DataFrame, por: str = "perfil") -> pd.DataFrame:
    """Horas de escucha por perfil (K-Means) o por nivel de horas; oculta grupos con n < MIN_N."""
    col = "perfil" if por == "perfil" else "m_horas_nivel"
    t = d.dropna(subset=[col]).groupby(col)["m_horas"].agg(n="count", media="mean", mediana="median")
    if col == "m_horas_nivel":
        t = t.reindex([x for x in NIVELES_HORAS if x in t.index])
    return t[t["n"] >= MIN_N].round(2)


def kpi3_generos(d: pd.DataFrame) -> pd.DataFrame:
    """Por género principal con n >= MIN_N: % de mejora de ánimo y IEP medio (cada uno con su n)."""
    filas = []
    for g, sub in d.dropna(subset=["genero"]).groupby("genero"):
        y = sub["mejora_animo"].dropna()
        iep = sub["iep"].dropna()
        if len(sub) < MIN_N:
            continue
        filas.append({"genero": g, "n": len(sub), "n_mejora": len(y),
                      "pct_mejora": y.mean() if len(y) >= MIN_N else None,
                      "n_iep": len(iep), "iep_medio": iep.mean() if len(iep) >= MIN_N else None})
    t = pd.DataFrame(filas)
    return t.sort_values("pct_mejora", ascending=False).reset_index(drop=True) if len(t) else t


def kpi4_estres_por_perfil(d: pd.DataFrame) -> pd.DataFrame:
    """IEP medio y distribución de niveles de IEP por perfil de hábitos (n >= MIN_N)."""
    sub = d.dropna(subset=["perfil", "iep_nivel"])
    if sub.empty:
        return pd.DataFrame()
    t = pd.crosstab(sub["perfil"], sub["iep_nivel"]).reindex(columns=NIVELES_IEP, fill_value=0)
    t["n"] = t.sum(axis=1)
    t["iep_medio"] = sub.groupby("perfil")["iep"].mean()
    return t[t["n"] >= MIN_N].round(2)


def kpi5_ia_por_bienestar(d: pd.DataFrame) -> pd.DataFrame:
    """Horas de IA y % de uso como guía por nivel de IEP (n >= MIN_N)."""
    sub = d.dropna(subset=["iep_nivel"])
    if sub.empty:
        return pd.DataFrame()
    t = sub.groupby("iep_nivel").agg(
        n=("id", "size"), horas_ia_media=("ia_horas", "mean"), horas_ia_mediana=("ia_horas", "median"),
        pct_guia=("modalidad_ia", lambda s: (s == MODALIDAD["guia"]).mean()))
    t = t.reindex([x for x in NIVELES_IEP if x in t.index])
    return t[t["n"] >= MIN_N].round(2)


def momentos(d: pd.DataFrame) -> pd.Series:
    return d[list(MOMENTOS)].sum().rename(index=MOMENTOS).sort_values()


# ------------------------------------------------------------------------------------------
# Clasificaciones complementarias (preguntas de opción libre codificadas en la Fase 3/4)
# ------------------------------------------------------------------------------------------

MIN_MENCIONES = 2  # un artista o término se muestra si lo mencionan al menos 2 estudiantes

PLATAFORMAS = {"plat_youtube": "YouTube / YT Music", "plat_spotify": "Spotify", "plat_apple": "Apple Music",
               "plat_otra": "Otras"}
CARACTERISTICAS = {"car_ritmo": "Ritmo", "car_letra": "Letra", "car_volumen": "Volumen",
                   "car_instrumental": "Instrumentación"}
EMOCION = {"emo_pop": "Pop", "emo_rock_metal": "Rock / metal", "emo_urbano": "Urbano",
           "emo_baladas": "Baladas / desamor", "emo_regional": "Regional mexicano",
           "emo_electronica": "Electrónica", "emo_clasica": "Clásica / soundtracks"}
FASES_IA = {"fase_investigacion": "Investigación / dudas", "fase_correccion": "Corrección",
            "fase_redaccion": "Redacción", "fase_estructuracion": "Estructuración", "fase_repaso": "Repaso"}
MOTIVOS_IA = {"tiempo": "Ahorrar tiempo / carga", "comprension": "Comprender temas", "ambos": "Ambos",
              "otro": "Otro"}


def conteo_banderas(d: pd.DataFrame, columnas: dict[str, str]) -> pd.Series:
    """Estudiantes que mencionan cada opción de una pregunta multirrespuesta (n por opción)."""
    cols = [c for c in columnas if c in d.columns]
    return d[cols].sum().rename(index=columnas).astype(int).sort_values()


def top_artistas(d: pd.DataFrame, minimo: int = MIN_MENCIONES) -> pd.Series:
    """Artistas mencionados por al menos `minimo` estudiantes de la selección."""
    from texto import artistas  # importación diferida: NLTK solo se carga si se usa la vista
    s = artistas(d["m_artistas"], min_menciones=minimo)
    s.index = [a.title() for a in s.index]
    return s.sort_values()


def motivos_ia(d: pd.DataFrame) -> pd.Series:
    return d["ia_motivo_cod"].map(MOTIVOS_IA).value_counts().sort_values()


"""Reglas de codificación por documento (Fase 3).

Cada diccionario REGLAS_* contiene listas (regex sobre texto normalizado, valor), evaluadas
en orden. El orden importa: las expresiones más específicas (negaciones, matices) van
antes que las generales. Las funciones `limpiar_docN` devuelven el DataFrame limpio con:
  - id (número de cuenta), llave para unir los documentos;
  - columnas originales de texto (para el análisis descriptivo de texto);
  - columnas codificadas (sufijos _cod, _h, _min, banderas con prefijo);
  - banderas de calidad (atípicos, respuestas copiadas).
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

from limpieza import (a_entero, a_horas, a_minutos, a_semestre, atipicos_iqr, banderas,
                      codificar, escala_10, normalizar, respuestas_copiadas)

# ======================================================================================
# Documento 1 — Música y estado de ánimo
# ======================================================================================

GENEROS = {  # grupo -> patrón (para el género principal se toma el que aparece primero)
    "pop": r"\bpop|k-pop",
    "rock_metal": r"rock|metal|\bcore\b",
    "electronica": r"electronica|house",
    "urbano": r"r&b|hip ?-?hop|\brap\b|reg+u?eton|regueton|trap|urbana|pluggnb",
    "regional": r"corrido|nortenyo|norteno|banda|regional|cumbia|salsa",
    "baladas": r"balada|jose jose|luis miguel|desamor",
    "clasica": r"clasica|soundtrack",
}

REGLAS_D1 = {
    "mejora_animo": [  # 1 = describe mejora/activación; 0 = sin cambio; resto -> NaN
        (r"^mejorable$|^(muy )?bueno$|centrarme", np.nan),
        (r"igual|neutral|permanece", 0),
        (r"mejor|sube|despues|paso de|energ|anim|feliz|contento|buen humor|ayuda", 1),
    ],
    "m_energia_cod": [  # 0 no influye, 1 poco/moderado, 2 mucho
        (r"no influye|\bnada\b", 0),
        (r"no mucho|un poco|medianamente|\bpoco\b", 1),
        (r"mucho|bastante|gran|100|todo el dia", 2),
        (r"influye|incluye|ayuda|dan mas|exalt|sube", 1),
    ],
    "m_concentracion_cod": [  # -1 distrae, 0 depende/neutral, 1 ayuda
        (r"no distraerme|no me distraigo", 1),
        (r"contraproducente", -1),
        (r"depende|a menos que|a veces|regular|no influye", 0),
        (r"no me puedo concentr|distrae|distraigo", -1),
        (r"concentr|enfoc|enfoque|ayuda|positiv", 1),
    ],
    "m_sueno_cod": [  # -1 perjudica, 0 no afecta / no la usa, 1 ayuda
        (r"despierta|duerma menos|desconcentra", -1),
        (r"no afecta|no hay influencia|no creo que influya|no influye|irrelevante|no la ocupo"
         r"|no escucho|depende|regular|^poca", 0),
        (r"relaj|ayuda|buena", 1),
    ],
    "m_con_vs_sin_cod": [  # -1 mejor en silencio, 0 depende/igual, 1 mejor con música
        (r"depende|en cambio|casi nada|igual", 0),
        (r"en silencio me cuesta|sin musica se siente|en silencio se nota|en silencio el ambiente"
         r"|me desconcentro", 1),
        (r"me distraigo|distraer|en silencio me concentro|sin musica lo hago|con sonido me cuesta"
         r"|no deja concentrar", -1),
        (r"motiva|ameno|vivo|concentro mas|energ", 1),
    ],
    "m_maneja_emociones_cod": [(r"^(si|claro)\b", 1), (r"^no\b", 0)],
    "m_importancia_cod": [  # 0 baja, 1 media, 2 alta
        (r"del 1 al 10 un (\d+)|(\d+)\s*/\s*10",
         lambda m: int(np.digitize(float(m.group(1) or m.group(2)), [5, 8]))),
        (r"no es importante|nada importante", 0),
        (r"no indispensable|medianamente", 1),
        (r"importante|necesari|fundamental|muy util|muy grande|bastante|indispensable", 2),
    ],
}

MOMENTOS = {
    "mom_estudio": r"tarea|estudi|concentra|biblioteca|clases",
    "mom_traslado": r"camino|transporte|trasporte|camion|traslad|ir y regresar|calle|viaj|manej|regreso",
    "mom_ejercicio": r"ejercicio|gym|gimnasio|deport|fisic",
    "mom_descanso": r"descans|relaj|dormir|distraer",
    "mom_hogar": r"quehacer|limpi|traste|me bano|actividades en casa",
    "mom_trabajo": r"trabaj",
    "mom_todo_el_dia": r"todo momento|todo el dia|cualquier hora",
}

PLATAFORMAS = {
    "plat_spotify": r"spotify",
    "plat_youtube": r"youtube|\byt\b",
    "plat_apple": r"apple",
    "plat_otra": r"trebel|powerramp|streaming",
}

CARACTERISTICAS = {
    "car_ritmo": r"ritmo|rimo|notas alegres",
    "car_letra": r"letra|hable de algo",
    "car_volumen": r"volumen",
    "car_instrumental": r"solos|guitarra|piano",
}


def genero_principal(texto) -> str | float:
    t = normalizar(texto)
    if t is None:
        return np.nan
    if "no escucho" in t:
        return "no_escucha"
    if "variado" in t:
        return "variado"
    posiciones = {}
    for g, p in GENEROS.items():
        m = re.search(p, t)
        if m:
            posiciones[g] = m.start()
    return min(posiciones, key=posiciones.get) if posiciones else "otro"


def corregir_cuenta_invalida(cuentas: pd.Series, referencia: set) -> tuple[pd.Series, int]:
    """Corrige cuentas de longitud distinta de 9 si, al borrar un dígito, coinciden con
    exactamente una cuenta de `referencia` (cuentas de otro documento sin pareja).
    Si no hay coincidencia única, la cuenta se conserva tal cual (no se inventa)."""
    corregidas, n = cuentas.copy(), 0
    for idx, c in cuentas.items():
        s = str(c)
        if pd.isna(c) or len(s) == 9:
            continue
        candidatas = {int(s[:k] + s[k + 1:]) for k in range(len(s))} & referencia
        if len(candidatas) == 1:
            corregidas.loc[idx] = candidatas.pop()
            n += 1
    return corregidas, n


def limpiar_doc1(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["id"] = out["cuenta"].astype("Int64")
    out["m_horas"] = out["m_horas_dia"].map(a_horas)
    out["m_horas_nivel"] = pd.cut(out["m_horas"], [-0.01, 1.99, 4, np.inf],
                                  labels=["baja", "media", "alta"]).astype("string")
    out["m_genero_grupo"] = out["m_genero_frecuente"].map(genero_principal)
    for var, origen in [("mejora_animo", "m_animo_antes_despues"), ("m_energia_cod", "m_energia"),
                        ("m_concentracion_cod", "m_concentracion"), ("m_sueno_cod", "m_sueno"),
                        ("m_con_vs_sin_cod", "m_con_vs_sin"),
                        ("m_maneja_emociones_cod", "m_maneja_emociones"),
                        ("m_importancia_cod", "m_importancia")]:
        out[var] = out[origen].map(lambda x, r=REGLAS_D1[var]: codificar(x, r)).astype("Float64")
    # Banderas multirrespuesta
    for col, grupos in [("m_momentos", MOMENTOS), ("m_plataforma", PLATAFORMAS),
                        ("m_caracteristicas", CARACTERISTICAS)]:
        b = out[col].map(lambda x, g=grupos: banderas(x, g)).apply(pd.Series)
        out[b.columns] = b
    emo = out["m_generos_emocion"].map(
        lambda x: banderas(x, {f"emo_{g}": p for g, p in GENEROS.items()})).apply(pd.Series)
    out[emo.columns] = emo
    # Quien no escucha música no tiene momentos ni plataformas: 0, no faltante
    no_escucha = out["m_horas"].eq(0)
    out.loc[no_escucha, list(MOMENTOS) + list(PLATAFORMAS)] = 0.0
    sin_dato = out["m_caracteristicas"].map(normalizar).fillna("").str.contains("no sabri")
    out.loc[sin_dato, list(CARACTERISTICAS)] = np.nan
    # Calidad
    out["m_horas_atipico"] = atipicos_iqr(out["m_horas"])
    abiertas = [c for c in df.columns if c.startswith("m_")]
    out["copias_d1"] = respuestas_copiadas(out, abiertas)
    return out.drop(columns="cuenta")


# ======================================================================================
# Documento 2 — Entorno universitario y bienestar
# ======================================================================================

REGLAS_D2 = {
    "b_desanimo_cod": [  # 0 nunca .. 4 muy frecuentemente
        (r"muy pocas|rara vez|casi nunca|no es frecuente|1 vez al mes", 1),
        (r"muy frecuente|casi siempre|todos los dias|\bmuch[oa]\b", 4),
        (r"\d+ (o \d+ )?veces a la semana", 3),
        (r"\d+ (o \d+ )?veces al mes", 2),
        (r"frecuente|bastante", 3),
        (r"algunas ocasiones|a veces|un poco", 2),
        (r"\bnunca\b", 0),
    ],
    "b_irritabilidad_cod": [  # 0 nunca .. 4 muy fácilmente
        (r"no pierdo|poca facilidad|\bpocas?\b|\bpoco\b|rara vez|casi nunca|dificilmente"
         r"|buena tolerancia", 1),
        (r"muy facil|muy rapido|facilmente", 4),
        (r"veces a la semana", 3),
        (r"a veces|solo cuando", 2),
        (r"\bnunca\b", 0),
    ],
    "b_sueno_calidad_cod": [  # 0 mala .. 3 buena
        (r"un poco mal|no es tan buen|no muy buen|corto|irregular", 1),
        (r"un poco buen|regular", 2),
        (r"muy pesad|\bmal", 0),
        (r"buen", 3),
    ],
    "b_concentracion_dif_cod": [  # 0 ninguna .. 3 mucha
        (r"no tengo problemas|nada dificil|no se me dificulta", 0),
        (r"no mucho|no muy|no ha cambiado|un poco|\bpoco\b|algo|regular|me cuesta|en ocasiones", 1),
        (r"bastante", 2),
        (r"muy dificil|demasiado|extremadamente|mucho", 3),
    ],
    "b_traslado_impacto_cod": [  # 0 ninguno .. 3 alto
        (r"(\d+)\s*/\s*10", lambda m: escala_10(m, 4)),
        (r"ninguno|\bnada\b", 0),
        (r"no mucho|no tiene mucho|muy poco|\bpoco\b", 1),
        (r"intermedio|bastante|agobi", 2),
        (r"mucho|muy cansad|alto|\bmil\b|odio", 3),
    ],
    "b_apoyo_social_cod": [  # 0 bajo .. 3 alto
        (r"(\d+)\s*/\s*10", lambda m: escala_10(m, 4)),
        (r"^un (\d+)", lambda m: escala_10(m, 4)),
        (r"^(\d+)$", lambda m: escala_10(m, 4)),
        (r"muy buen|excelente|gran apoyo|plena|muy alto|mucha ayuda", 3),
        (r"medio", 1),
        (r"buen|bien", 2),
    ],
    "b_ambiente_hogar_cod": [  # 0 conflictivo, 1 normal, 2 tranquilo
        (r"insegur|conflict|tens", 0),
        (r"normal|neutral|diferencias", 1),
        (r"tranquil|buen|amable|agradable|sano|ameno|armon", 2),
    ],
    "b_espacio_estudio_cod": [  # 0 poco, 1 medio, 2 mucho
        (r"\bpero\b|aunque|media|regular|necesari|suficiente", 1),
        (r"poca|solo cuando", 0),
        (r"mucha|bastante|buen|tranquil", 2),
    ],
    "b_interes_cod": [  # 0 bajo, 1 medio, 2 alto
        (r"del 1 al 10 un (\d+)|(\d+)\s*/\s*10",
         lambda m: int(np.digitize(float(m.group(1) or m.group(2)), [5, 8]))),
        (r"aburrid", 0),
        (r"sin embargo|\bpero\b|medio|bajo un poco", 1),
        (r"excelent|mucho|muy|buen|alto", 2),
    ],
    "b_alimentacion_cod": [  # 1 = reporta cambio
        # La negación solo cuenta si abre la respuesta: "he disminuido mis porciones y mi
        # apetito no ha cambiado" sí reporta un cambio.
        (r"^(no ha cambiado|no han cambiado|ningun cambio|lo normal)", 0),
        (r"hambre|descuid|cambio|reduc|salt|disminu|dejado|desbalance|menos|desayun|desyun", 1),
    ],
    "b_convivencia_cod": [
        (r"familia", "familia"), (r"\bsolo\b", "solo"), (r"companer", "companeros"),
    ],
    "b_carrera_cod": [(r"\bmac\b|matematicas apl", "MAC")],  # incluye la errata "aplciadas"
}


def nivel_iep(x: float):
    if pd.isna(x):
        return pd.NA
    return "bajo" if x < 1.5 else ("medio" if x <= 2.5 else "alto")


def limpiar_doc2(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["id"] = out["cuenta"].astype("Int64")
    out["b_semestre_cod"] = out["b_semestre"].map(a_semestre)
    out["b_edad_cod"] = out["b_edad"].map(a_entero)
    out["b_traslado_min_cod"] = out["b_traslado_min"].map(a_minutos)
    for var, reglas in REGLAS_D2.items():
        origen = var.removesuffix("_cod")
        serie = out[origen].map(lambda x, r=reglas: codificar(x, r))
        out[var] = serie if var in ("b_convivencia_cod", "b_carrera_cod") else serie.astype("Float64")
    # Índice de estrés percibido (indicador indirecto, ver docs/negocio.md §9.4)
    out["iep"] = out[["b_desanimo_cod", "b_irritabilidad_cod"]].mean(axis=1, skipna=False)
    out["iep_nivel"] = out["iep"].map(nivel_iep).astype("string")
    for c in ["b_edad_cod", "b_traslado_min_cod"]:
        out[c.replace("_cod", "_atipico")] = atipicos_iqr(out[c])
    abiertas = [c for c in df.columns if c.startswith("b_")]
    out["copias_d2"] = respuestas_copiadas(out, abiertas)
    return out.drop(columns="cuenta")


# ======================================================================================
# Documento 3 — Desempeño académico por el uso de IA
# ======================================================================================

HERRAMIENTAS = {
    "ia_chatgpt": r"chat ?gpt|chargpt", "ia_gemini": r"gemini", "ia_claude": r"claude",
    "ia_deepseek": r"deeps", "ia_copilot": r"copilot", "ia_notebooklm": r"notebook",
    "ia_qwen": r"qwen",
}

FASES = {
    "fase_investigacion": r"investig|consulta|dudas|comprender|explica",
    "fase_estructuracion": r"estructur|creacion de proyectos",
    "fase_redaccion": r"redac",
    "fase_correccion": r"correc|errores|revisar",
    "fase_repaso": r"repas",
}

REGLAS_D3 = {
    "ia_estres_cod": [  # -1 aumenta, 0 sin efecto, 1 disminuye
        (r"aumenta", -1),
        (r"no cambia|no ha influido|no influye|es lo mismo", 0),
        (r"menos|baj|disminu|ayud|liber|quitad|aliv|control|colapsado|pesada", 1),
    ],
    "ia_independencia_cod": [  # -1 debilita, 0 depende/ambas, 1 fortalece
        (r"no lo debilita", 1),
        (r"fortalec.*debilit|debilit.*fortalec|punto medio|50/50|dependiendo|solo si|solo cuando"
         r"|debilita si", 0),
        (r"debilit|disminuido|perjudic|dependiente|dependo|floj", -1),
        (r"fortalec", 1),
    ],
    "ia_impacto_tiempo_cod": [  # -1 más tiempo, 0 igual/mixto, 1 menos tiempo
        (r"extenso|casi nada|igual|no ha cambiado", 0),
        (r"reduc|disminu|ahorr|menos tiempo|rapido|optimiz|positiv|para bien|mas facil"
         r"|distribuido|mas tiempo", 1),
    ],
    "ia_calificaciones_cod": [  # -1 empeoran, 0 igual, 1 mejoran
        (r"no sabria", np.nan),
        (r"dependen|igual|ninguna|no mucha|no ha habido|no he notado|casi nada", 0),
        (r"estrict|empeor", -1),
        (r"mejor|aument|favorable|suben|siben", 1),
    ],
    "ia_pensamiento_critico_cod": [  # -1 afecta, 0 poco/mixto, 1 mejora
        (r"positiva y negativa|no obstante|hay temas donde", 0),
        (r"no me afecta|no siento|no mucho|afectan poco|no me afectan|casi no|^no\.?$", 0),
        (r"benefici|me ayudan", 1),
        (r"afect|quitan|esfuerzo|cuadrada|razonar|perdido|aprenda a cambio", -1),
    ],
    "ia_reemplazo_laboral_cod": [
        (r"^no se\b", np.nan),
        (r"no completamente|depende|pero no todas", "parcial"),
        (r"^si\b", "si"), (r"^no\b", "no"),
    ],
    "ia_guia_vs_atajo_cod": [
        (r"principalmente como una guia", "guia"),
        (r"ambas|ambos|las dos|depende", "ambas"),
        (r"atajo", "atajo"),
        (r"guia|aprender", "guia"),
    ],
    "ia_otros_usos_cod": [(r"^no\b", 0), (r"\w", 1)],
}

_MOTIVO_TIEMPO = r"tiempo|rapid|carga|muchas actividades|cansa|flojera|comodidad"
_MOTIVO_COMPRENSION = (r"comprend|entend|aprend|duda|dificult|desconozco|conceptos|corrobor"
                       r"|corregir|redaccion|problema|resumen")


def motivo_ia(texto):
    t = normalizar(texto)
    if t is None:
        return np.nan
    tiempo, comp = bool(re.search(_MOTIVO_TIEMPO, t)), bool(re.search(_MOTIVO_COMPRENSION, t))
    return "ambos" if tiempo and comp else "tiempo" if tiempo else "comprension" if comp else "otro"


def limpiar_doc3(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["id"] = out["cuenta"].astype("Int64")
    out["ia_horas"] = out["ia_horas_dia"].map(a_horas)
    out["ia_semestre_inicio_cod"] = out["ia_semestre_inicio"].map(a_semestre)
    for var, reglas in REGLAS_D3.items():
        origen = var.removesuffix("_cod")
        serie = out[origen].map(lambda x, r=reglas: codificar(x, r))
        numerica = var not in ("ia_reemplazo_laboral_cod", "ia_guia_vs_atajo_cod")
        out[var] = serie.astype("Float64") if numerica else serie
    out["ia_motivo_cod"] = out["ia_motivo"].map(motivo_ia)
    for col, grupos in [("ia_herramientas", HERRAMIENTAS), ("ia_fase_uso", FASES)]:
        b = out[col].map(lambda x, g=grupos: banderas(x, g)).apply(pd.Series)
        out[b.columns] = b
    out["ia_n_herramientas"] = out[list(HERRAMIENTAS)].sum(axis=1)
    out["ia_horas_atipico"] = atipicos_iqr(out["ia_horas"])
    abiertas = [c for c in df.columns if c.startswith("ia_")]
    out["copias_d3"] = respuestas_copiadas(out, abiertas)
    return out.drop(columns="cuenta")

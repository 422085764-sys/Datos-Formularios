"""Tablero analítico: música, estado de ánimo, estrés y uso de IA en estudiantes de MAC.

Ejecutar desde la raíz del proyecto:
    streamlit run app/app.py

Datos: usa data/processed/ (generado por los cuadernos 01 a 03) o, si no existe, el secreto
[datos] tablero_csv de Streamlit (ver src/preparar_despliegue.py y la sección de despliegue del README).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
import tablero as tb  # noqa: E402

# Paleta validada (orden fijo; el color sigue a la entidad, nunca a su rango)
AZUL, NARANJA, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
ORDINAL = {"bajo": "#86b6ef", "medio": "#3987e5", "alto": "#104281"}
GRIS = "#898781"
PERFIL_COLOR = {"P1 · Escucha intensiva": AZUL, "P2 · Estrés alto": NARANJA,
                "P3 · IA como guía, estrés bajo": AQUA}

st.set_page_config(page_title="Música, ánimo e IA · MAC", page_icon="🎧", layout="wide")


# ------------------------------------------------------------------------------------------
# Utilidades de gráficas (Plotly)
# ------------------------------------------------------------------------------------------

def estilo(fig: go.Figure, titulo: str, alto: int = 340, xaxis: str = "", yaxis: str = "") -> go.Figure:
    fig.update_layout(title=dict(text=titulo, x=0, xanchor="left", font=dict(size=15)), height=alto,
                      margin=dict(l=10, r=10, t=50, b=10), bargap=0.35, showlegend=False,
                      hoverlabel=dict(font_size=12), xaxis_title=xaxis, yaxis_title=yaxis)
    fig.update_xaxes(showgrid=True, gridwidth=0.5, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def barras_h(etiquetas, valores, titulo, xaxis, textos, hover, color=AZUL, alto=None):
    fig = go.Figure(go.Bar(y=list(etiquetas), x=list(valores), orientation="h", marker_color=color,
                           text=list(textos), textposition="outside", cliponaxis=False,
                           hovertext=list(hover), hoverinfo="text"))
    fig = estilo(fig, titulo, alto or 70 + 42 * len(valores), xaxis)
    tope = max([float(v) for v in valores] + [0])
    fig.update_xaxes(range=[0, tope * 1.3 if tope else 1])  # espacio para la etiqueta "valor (n)"
    return fig


def tabla_accesible(df: pd.DataFrame, etiqueta: str = "Ver datos de la gráfica"):
    with st.expander(etiqueta):
        st.dataframe(df, width="stretch")


def grafica_conteo(conteos: pd.Series, titulo: str, xaxis: str, total: int, nota: str = "",
                   minimo: int = tb.MIN_MENCIONES, color: str = AZUL):
    """Barras de una clasificación (menciones por opción); omite opciones con menos de `minimo`."""
    conteos = conteos[conteos >= minimo].sort_values()
    if conteos.empty:
        st.info(f"{titulo}: ninguna opción alcanza {minimo} menciones con la selección actual.")
        return
    st.plotly_chart(barras_h(conteos.index, conteos.values, titulo, xaxis,
                             [f"{int(v)} ({v / total:.0%})" for v in conteos.values],
                             [f"{i}: {int(v)} de {total} estudiantes" for i, v in conteos.items()], color=color),
                    width="stretch")
    if nota:
        st.caption(nota)
    tabla_accesible(conteos.rename("estudiantes").to_frame())


def aviso_n(n: int, minimo: int = tb.MIN_N) -> bool:
    """minimo = MIN_N: estudiantes en la selección; minimo = 1: grupos que ya cumplen el umbral."""
    if n < minimo:
        if minimo == 1:
            st.info(f"Ningún grupo de esta vista tiene al menos {tb.MIN_N} estudiantes con la selección actual. "
                    "Se oculta para proteger el anonimato y evitar cifras inestables.")
        else:
            st.info(f"Esta vista necesita al menos {minimo} estudiantes con datos (hay {n}). "
                    "Se oculta para proteger el anonimato y evitar cifras inestables.")
        return False
    return True


# ------------------------------------------------------------------------------------------
# Datos
# ------------------------------------------------------------------------------------------

@st.cache_data
def datos_locales() -> pd.DataFrame:
    return tb.cargar_base()


@st.cache_data
def datos_de_secreto(texto_csv: str) -> pd.DataFrame:
    return tb.base_desde_csv(texto_csv)


def secreto_csv() -> str | None:
    """CSV mínimo guardado como secreto ([datos] tablero_csv); None si no está configurado."""
    try:
        return st.secrets["datos"]["tablero_csv"]
    except (KeyError, FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return None


# 1) Datos locales (data/processed/, generados por los cuadernos); 2) secreto de Streamlit
#    (despliegue en Community Cloud, donde los datos no están en el repositorio).
#    TABLERO_FUENTE=secretos fuerza la segunda opción (se usa en las pruebas).
base = None
if os.environ.get("TABLERO_FUENTE") != "secretos":
    try:
        base = datos_locales()
    except FileNotFoundError:
        base = None
if base is None and (csv := secreto_csv()):
    base = datos_de_secreto(csv)
if base is None:
    st.error("No se encontraron datos. **En local:** ejecuta los cuadernos `01_limpieza`, `02_eda` y "
             "`03_modelado` (ver README). **En Streamlit Community Cloud:** pega el contenido generado por "
             "`python src/preparar_despliegue.py` en *Settings → Secrets* de la app.")
    st.stop()

st.title("Música, estado de ánimo, estrés e IA")
st.caption("Estudiantes de 7.º semestre de Matemáticas Aplicadas y Computación, FES Acatlán · "
           "Datos auto-reportados y observacionales: las relaciones mostradas son asociaciones, no causas.")

# ------------------------------------------------------------------------------------------
# Filtros (una fila sobre las vistas)
# ------------------------------------------------------------------------------------------

f1, f2, f3, f4, f5 = st.columns([1.3, 0.8, 1.3, 1.1, 1.3])
generos = f1.multiselect("Género musical", sorted(base["genero"].dropna().unique()), placeholder="Todos")
semestres_disp = sorted(base["b_semestre_cod"].dropna().astype(int).unique())
semestres = f2.multiselect("Semestre", semestres_disp, placeholder="Todos",
                           help="Hoy solo hay estudiantes de 7.º semestre; el filtro queda listo para más datos.")
hmax = float(base["m_horas"].max())
horas = f3.slider("Horas de música al día", 0.0, hmax, (0.0, hmax), step=0.5)
estres = f4.multiselect("Nivel de estrés (IEP)", tb.NIVELES_IEP, placeholder="Todos",
                        help="Índice de estrés percibido: promedio de desánimo e irritabilidad (0-4). "
                             "Indicador indirecto, no clínico.")
modalidades = f5.multiselect("Uso de IA", sorted(set(tb.MODALIDAD.values())), placeholder="Todos")

horas_filtro = None if horas == (0.0, hmax) else horas
d = tb.filtrar(base, generos, [float(s) for s in semestres], horas_filtro, estres, modalidades)
filtros_doc2 = bool(semestres or estres)
st.markdown(f"**Estudiantes en la selección: {len(d)}** de {len(base)}"
            + (" · los filtros de semestre y estrés solo incluyen a quienes respondieron el cuestionario de bienestar"
               if filtros_doc2 else ""))

if not aviso_n(len(d)):
    st.stop()

tabs = st.tabs(["Resumen", "Hábitos musicales", "Música y bienestar", "Uso de IA", "Perfiles",
                "Notas metodológicas"])

# ------------------------------------------------------------------------------------------
# Resumen
# ------------------------------------------------------------------------------------------
with tabs[0]:
    k1 = tb.kpi1_mejora(d)
    k2 = d["m_horas"].dropna()
    k3 = tb.kpi3_generos(d)
    k4 = tb.kpi4_estres_por_perfil(d)
    k5 = tb.kpi5_ia_por_bienestar(d)
    c = st.columns(5)
    c[0].metric("Mejora de ánimo con música", f"{k1['valor']:.0%}" if k1["n"] else "—",
                help="KPI 1. Estudiantes que describen una mejora o activación al escuchar su música favorita.")
    c[0].caption(f"{k1['k']} de {k1['n']} con respuesta codificable")
    c[1].metric("Horas de música al día (mediana)", f"{k2.median():.1f} h" if len(k2) else "—",
                help="KPI 2. Ver el desglose por perfil en la pestaña Perfiles.")
    c[1].caption(f"n = {len(k2)} · media {k2.mean():.1f} h")
    if len(k3) and k3["pct_mejora"].notna().any():
        top = k3.dropna(subset=["pct_mejora"]).iloc[0]
        c[2].metric("Género con más mejora reportada", top["genero"], help="KPI 3. Solo géneros con al menos 3 estudiantes.")
        c[2].caption(f"{top['pct_mejora']:.0%} de mejora · n = {int(top['n_mejora'])}")
    else:
        c[2].metric("Género con más mejora reportada", "—")
        c[2].caption("Ningún género llega a 3 estudiantes")
    if len(k4):
        alto = k4["iep_medio"].idxmax()
        c[3].metric("Perfil con más estrés (IEP)", alto.split(" · ")[0], help="KPI 4. IEP medio por perfil de hábitos.")
        c[3].caption(f"IEP medio {k4.loc[alto, 'iep_medio']:.2f} de 4 · n = {int(k4.loc[alto, 'n'])}")
    else:
        c[3].metric("Perfil con más estrés (IEP)", "—")
        c[3].caption("Sin perfiles con al menos 3 estudiantes")
    if len(k5):
        guia = k5["pct_guia"]
        c[4].metric("Usan la IA como guía", f"{(d['modalidad_ia'] == tb.MODALIDAD['guia']).mean():.0%}",
                    help="KPI 5. Proporción en la selección; abajo, por nivel de estrés.")
        c[4].caption(" · ".join(f"{i}: {v:.0%}" for i, v in guia.items()))
    else:
        c[4].metric("Usan la IA como guía", f"{(d['modalidad_ia'] == tb.MODALIDAD['guia']).mean():.0%}")
        c[4].caption("Sin niveles de estrés con al menos 3 estudiantes")

    # Clasificaciones destacadas de la selección (cada una con su conteo)
    def destacado(serie: pd.Series, etiqueta: str) -> str:
        serie = serie[serie >= tb.MIN_MENCIONES]
        if serie.empty:
            return f"**{etiqueta}:** sin opción con {tb.MIN_MENCIONES}+ menciones"
        return f"**{etiqueta}:** {serie.idxmax()} ({int(serie.max())} de {len(d)})"

    st.markdown(" · ".join([
        destacado(tb.top_artistas(d), "Artista más mencionado"),
        destacado(tb.conteo_banderas(d, tb.PLATAFORMAS), "Plataforma principal"),
        destacado(tb.conteo_banderas(d, tb.CARACTERISTICAS), "Lo que más influye de una canción"),
        destacado(tb.conteo_banderas(d, tb.FASES_IA), "Uso principal de la IA"),
    ]))

    st.divider()
    st.subheader("Lo que muestran los datos")
    st.markdown(
        "- **La música se percibe como beneficiosa** (85 % reporta mejora), sobre todo en los traslados, "
        "y el beneficio crece con las horas de escucha.\n"
        "- **Ese beneficio no se refleja en el bienestar general**: desánimo, irritabilidad y sueño no varían "
        "con los hábitos musicales. El efecto parece situacional.\n"
        "- **Usar la IA como guía para aprender** se asocia con menos estrés percibido; las horas de uso, no.\n"
        "- **Los traslados más largos** se asocian con peor calidad de sueño.\n\n"
        "Son señales exploratorias con muestras pequeñas (n = 17 a 24); ninguna se confirma tras corregir por "
        "comparaciones múltiples. Ver *Notas metodológicas*.")

# ------------------------------------------------------------------------------------------
# Hábitos musicales
# ------------------------------------------------------------------------------------------
with tabs[1]:
    a, b = st.columns(2)
    with a:
        gen = d["genero"].value_counts().sort_values()
        gen = gen[gen >= tb.MIN_N] if len(gen) else gen
        otros = d["genero"].value_counts()
        otros = int(otros[otros < tb.MIN_N].sum())
        if otros:
            gen = pd.concat([pd.Series({"Otros (< 3 c/u)": otros}), gen])
        if aviso_n(int(gen.sum()) if len(gen) else 0):
            n = int(gen.sum())
            st.plotly_chart(barras_h(gen.index, gen.values, "Género musical principal", "Estudiantes",
                                     [f"{v} ({v / n:.0%})" for v in gen.values],
                                     [f"{i}: {v} de {n}" for i, v in gen.items()]), width="stretch")
            tabla_accesible(gen.rename("estudiantes").to_frame())
    with b:
        mom = tb.momentos(d)
        n = len(d)
        st.plotly_chart(barras_h(mom.index, mom.values, "Momentos en que escuchan música",
                                 "Estudiantes que lo mencionan", [f"{int(v)} ({v / n:.0%})" for v in mom.values],
                                 [f"{i}: {int(v)} de {n}" for i, v in mom.items()]), width="stretch")
        tabla_accesible(mom.rename("menciones").to_frame())
    h = d["m_horas"].dropna()
    fig = go.Figure(go.Histogram(x=h, xbins=dict(start=0, end=16, size=1), marker_color=AZUL,
                                 hovertemplate="%{x} h: %{y} estudiantes<extra></extra>"))
    fig.add_vline(x=h.median(), line_color="#0b0b0b", line_width=2,
                  annotation_text=f"mediana {h.median():.1f} h", annotation_position="top right",
                  annotation=dict(bgcolor="rgba(252,252,251,0.9)", font=dict(color="#0b0b0b")))
    st.plotly_chart(estilo(fig, f"Horas diarias de música (n = {len(h)})", 300, "Horas por día", "Estudiantes"),
                    width="stretch")

    st.subheader("Preferencias musicales")
    st.caption(f"Clasificaciones de respuestas abiertas. Se muestran las opciones mencionadas por al menos "
               f"{tb.MIN_MENCIONES} estudiantes de la selección; un estudiante puede mencionar varias.")
    a, b = st.columns(2)
    with a:
        grafica_conteo(tb.top_artistas(d), "Artistas más mencionados", "Estudiantes que lo mencionan", len(d),
                       "Lista libre de 5 artistas favoritos, separada y normalizada con NLTK. La diversidad es "
                       "alta: pocos artistas se repiten.")
    with b:
        grafica_conteo(tb.conteo_banderas(d, tb.PLATAFORMAS), "Plataformas de escucha", "Estudiantes", len(d))
    a, b = st.columns(2)
    with a:
        grafica_conteo(tb.conteo_banderas(d, tb.CARACTERISTICAS), "Qué de una canción influye en sus emociones",
                       "Estudiantes", len(d))
    with b:
        grafica_conteo(tb.conteo_banderas(d, tb.EMOCION), "Géneros que asocian con emociones",
                       "Estudiantes que lo mencionan", len(d),
                       "Pregunta: «¿Qué géneros te hacen sentir feliz, tranquilo, triste o motivado?»")

# ------------------------------------------------------------------------------------------
# Música y bienestar
# ------------------------------------------------------------------------------------------
with tabs[2]:
    a, b = st.columns(2)
    with a:
        k3 = tb.kpi3_generos(d).dropna(subset=["pct_mejora"])
        if aviso_n(len(k3), 1):
            k3 = k3.sort_values("pct_mejora")
            st.plotly_chart(barras_h(k3["genero"], k3["pct_mejora"] * 100, "Mejora de ánimo por género",
                                     "% que reporta mejora",
                                     [f"{p:.0%} (n = {n})" for p, n in zip(k3["pct_mejora"], k3["n_mejora"])],
                                     [f"{g}: {p:.0%} de {n} · IEP medio {i:.2f} (n = {ni})" if pd.notna(i)
                                      else f"{g}: {p:.0%} de {n}"
                                      for g, p, n, i, ni in zip(k3["genero"], k3["pct_mejora"], k3["n_mejora"],
                                                                k3["iep_medio"], k3["n_iep"])]),
                            width="stretch")
            st.caption("Solo géneros con al menos 3 estudiantes. Las diferencias no son estadísticamente significativas.")
            tabla_accesible(k3)
    with b:
        k4 = tb.kpi4_estres_por_perfil(d)
        if aviso_n(len(k4), 1):
            fig = go.Figure()
            for nivel in tb.NIVELES_IEP:
                fig.add_bar(y=k4.index, x=k4[nivel], name=f"Estrés {nivel}", orientation="h",
                            marker=dict(color=ORDINAL[nivel], line=dict(color="#fcfcfb", width=2)),
                            hovertemplate=f"%{{y}} · estrés {nivel}: %{{x}} estudiantes<extra></extra>")
            fig = estilo(fig, "Nivel de estrés (IEP) por perfil de hábitos", 70 + 60 * len(k4), "Estudiantes")
            fig.update_layout(barmode="stack", showlegend=True,
                              legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0, title=None,
                                          traceorder="normal"))
            st.plotly_chart(fig, width="stretch")
            tabla_accesible(k4)
    sub = d.dropna(subset=["mejora_animo", "m_horas"])
    if aviso_n(len(sub)):
        fig = go.Figure()
        for valor, nombre, color in [(0.0, "Sin cambio", NARANJA), (1.0, "Mejora", AZUL)]:
            v = sub.loc[sub["mejora_animo"] == valor, "m_horas"]
            if len(v) >= tb.MIN_N:
                fig.add_box(x=v, name=f"{nombre} (n = {len(v)})", marker_color=color, boxpoints="all",
                            jitter=0.3, pointpos=0, line_width=2, hoverinfo="x")
        st.plotly_chart(estilo(fig, "Horas de música según el efecto en el ánimo", 260, "Horas por día"),
                        width="stretch")
        st.caption("Quienes reportan mejora escuchan más horas (señal exploratoria; uno de los casos sin cambio no "
                   "escucha música).")

# ------------------------------------------------------------------------------------------
# Uso de IA
# ------------------------------------------------------------------------------------------
with tabs[3]:
    a, b = st.columns(2)
    k5 = tb.kpi5_ia_por_bienestar(d)
    with a:
        if aviso_n(len(k5), 1):
            st.plotly_chart(barras_h([f"Estrés {i}" for i in k5.index][::-1], (k5["pct_guia"] * 100)[::-1],
                                     "Usan la IA como guía, por nivel de estrés", "% del nivel",
                                     [f"{p:.0%} (n = {n})" for p, n in zip(k5["pct_guia"], k5["n"])][::-1],
                                     [f"Estrés {i}: {p:.0%} de {n}" for i, p, n in
                                      zip(k5.index, k5["pct_guia"], k5["n"])][::-1], color=AQUA),
                            width="stretch")
            tabla_accesible(k5)
    with b:
        if aviso_n(len(k5), 1):
            st.plotly_chart(barras_h([f"Estrés {i}" for i in k5.index][::-1], k5["horas_ia_mediana"][::-1],
                                     "Horas de IA al día (mediana), por nivel de estrés", "Horas",
                                     [f"{h:.2g} h (n = {n})" for h, n in zip(k5["horas_ia_mediana"], k5["n"])][::-1],
                                     [f"Estrés {i}: mediana {h:.2g} h, media {m:.2g} h" for i, h, m in
                                      zip(k5.index, k5["horas_ia_mediana"], k5["horas_ia_media"])][::-1]),
                            width="stretch")
    herr = {"ia_gemini": "Gemini", "ia_chatgpt": "ChatGPT", "ia_claude": "Claude", "ia_deepseek": "DeepSeek",
            "ia_notebooklm": "NotebookLM", "ia_copilot": "Copilot", "ia_qwen": "Qwen"}
    st.subheader("Cómo y para qué usan la IA")
    grafica_conteo(d[list(herr)].sum().rename(index=herr).astype(int), "Herramientas de IA más usadas",
                   "Estudiantes", len(d))
    a, b = st.columns(2)
    with a:
        grafica_conteo(tb.conteo_banderas(d, tb.FASES_IA), "Fase del estudio en que más la usan", "Estudiantes",
                       len(d), color=AQUA)
    with b:
        grafica_conteo(tb.motivos_ia(d), "Motivo principal para recurrir a la IA", "Estudiantes", len(d),
                       "«Ambos» = menciona comprender y ahorrar tiempo.", color=AQUA)
    st.caption("Lo que distingue a los grupos con menos estrés es **cómo** usan la IA (como guía para aprender), "
               "no cuántas horas la usan.")

# ------------------------------------------------------------------------------------------
# Perfiles
# ------------------------------------------------------------------------------------------
with tabs[4]:
    sub = d.dropna(subset=["perfil"])
    st.markdown("Perfiles obtenidos por **K-Means** (k = 3) con horas de música, beneficios percibidos de la música, "
                "IEP, horas de IA y uso de la IA como guía. Silueta = 0.28: la estructura es débil, así que los "
                "perfiles son una **guía descriptiva**, no una clasificación definitiva.")
    if aviso_n(len(sub)):
        a, b = st.columns([1.3, 1])
        with a:
            fig = go.Figure()
            for perfil, color in PERFIL_COLOR.items():
                p = sub[sub["perfil"] == perfil]
                if len(p):
                    fig.add_scatter(x=p["CP1"], y=p["CP2"], mode="markers", name=f"{perfil} (n = {len(p)})",
                                    marker=dict(size=13, color=color, line=dict(color="#fcfcfb", width=2)),
                                    hovertemplate=f"{perfil}<extra></extra>")
            fig = estilo(fig, "Perfiles en el plano de componentes principales", 380,
                         "CP1: uso de IA como guía (+) frente a estrés y horas de música (−)",
                         "CP2: escucha y energía (+)")
            fig.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="top", y=-0.2, x=0))
            fig.update_yaxes(showgrid=True)
            st.plotly_chart(fig, width="stretch")
        with b:
            st.markdown("**P1 · Escucha intensiva.** Más horas de música; siente que la música le ayuda a "
                        "concentrarse; estrés medio; traslados más largos.\n\n"
                        "**P2 · Estrés alto.** Estrés alto; menos horas de música; la música lo distrae al "
                        "estudiar; solo la mitad reporta mejora de ánimo.\n\n"
                        "**P3 · IA como guía, estrés bajo.** Usa la IA para aprender, con poco tiempo de IA y "
                        "de música; el estrés más bajo.")
        k2p = tb.kpi2_horas(d, "perfil")
        if len(k2p):
            st.plotly_chart(barras_h(k2p.index[::-1], k2p["mediana"][::-1], "Horas de música por perfil (mediana)",
                                     "Horas por día", [f"{m:.2g} h (n = {n})" for m, n in zip(k2p["mediana"], k2p["n"])][::-1],
                                     [f"{i}: mediana {m:.2g} h, media {me:.2g} h" for i, m, me in
                                      zip(k2p.index, k2p["mediana"], k2p["media"])][::-1]),
                            width="stretch")
            tabla_accesible(k2p, "Ver horas por perfil")

# ------------------------------------------------------------------------------------------
# Notas metodológicas
# ------------------------------------------------------------------------------------------
with tabs[5]:
    st.markdown(f"""
**Fuentes.** Tres cuestionarios (música y ánimo, n = 24; bienestar, n = 19; uso de IA, n = 24) unidos por un
seudónimo irreversible. Los indicadores de bienestar solo existen para los 19 que respondieron los tres.

**Codificación.** Las respuestas abiertas se convirtieron en escalas con reglas explícitas y revisadas una por una;
lo que no se pudo codificar sin suponer queda como faltante. Nunca se imputa.

**Índice de estrés percibido (IEP).** Promedio de desánimo e irritabilidad (0-4): bajo < 1.5, medio 1.5-2.5,
alto > 2.5. Es un indicador **indirecto**, no un instrumento clínico validado.

**Protección de datos.** No se muestran respuestas individuales ni identificadores. Si una selección tiene menos de
{tb.MIN_N} estudiantes, la vista se oculta; las categorías con menos de {tb.MIN_N} se agrupan u omiten.

**Alcance.** Datos auto-reportados y transversales de un solo grupo de 7.º semestre: las relaciones son
**asociaciones**, no causas, y no se generalizan a otros semestres o carreras. Con n ≈ 19 solo se detectan
efectos grandes; ninguna asociación se confirma tras la corrección de Benjamini-Hochberg.

**Más detalle.** `docs/tecnico.pdf` (método y resultados) y `docs/negocio.pdf` (problemática y KPI).
""")

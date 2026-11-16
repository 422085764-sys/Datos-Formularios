"""Modelado no supervisado (Fase 5): preparación, K-Means, DBSCAN, PCA y estabilidad."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (adjusted_rand_score, calinski_harabasz_score, davies_bouldin_score,
                             silhouette_samples, silhouette_score)
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

SEMILLA = 42


def preparar_matriz(df: pd.DataFrame, variables: list[str], log: tuple[str, ...] = ()):
    """Casos completos (sin imputación), log1p en variables sesgadas y estandarización z."""
    datos = df.dropna(subset=variables).copy()
    X = datos[variables].astype(float).copy()
    for c in log:
        X[c] = np.log1p(X[c])
    escalador = StandardScaler().fit(X)
    return datos, escalador.transform(X), escalador


def evaluar_kmeans(Z: np.ndarray, ks=range(2, 7)) -> pd.DataFrame:
    """Métricas internas por k y concordancia con el agrupamiento jerárquico de Ward."""
    filas = []
    for k in ks:
        km = KMeans(k, n_init=50, random_state=SEMILLA).fit(Z)
        ward = AgglomerativeClustering(k, linkage="ward").fit(Z)
        filas.append({
            "k": k, "inercia": km.inertia_, "silueta": silhouette_score(Z, km.labels_),
            "davies_bouldin": davies_bouldin_score(Z, km.labels_),
            "calinski_harabasz": calinski_harabasz_score(Z, km.labels_),
            "tamaños": sorted(np.bincount(km.labels_).tolist(), reverse=True),
            "siluetas_negativas": int((silhouette_samples(Z, km.labels_) < 0).sum()),
            "ARI_vs_Ward": adjusted_rand_score(km.labels_, ward.labels_),
        })
    return pd.DataFrame(filas).set_index("k")


def estabilidad_bootstrap(Z: np.ndarray, k: int, B: int = 200) -> np.ndarray:
    """ARI entre la solución completa y soluciones reentrenadas en remuestras bootstrap.

    Cada remuestra se agrupa de nuevo y se compara, sobre los casos únicos que contiene,
    con las etiquetas de la solución completa. ARI cercano a 1 indica perfiles estables.
    """
    base = KMeans(k, n_init=50, random_state=SEMILLA).fit(Z).labels_
    rng = np.random.default_rng(SEMILLA)
    aris = []
    for b in range(B):
        idx = rng.choice(len(Z), len(Z), replace=True)
        unicos = np.unique(idx)
        modelo = KMeans(k, n_init=10, random_state=b).fit(Z[idx])
        aris.append(adjusted_rand_score(base[unicos], modelo.predict(Z[unicos])))
    return np.array(aris)


def distancias_k(Z: np.ndarray, k: int) -> np.ndarray:
    """Distancia al k-ésimo vecino ordenada (gráfica de codo para elegir eps en DBSCAN)."""
    return np.sort(NearestNeighbors(n_neighbors=k + 1).fit(Z).kneighbors(Z)[0][:, -1])


def explorar_dbscan(Z: np.ndarray, eps_valores, min_samples: int, referencia: np.ndarray) -> pd.DataFrame:
    filas = []
    for eps in eps_valores:
        lab = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(Z)
        grupos = sorted(set(lab) - {-1})
        validos = lab != -1
        sil = (silhouette_score(Z[validos], lab[validos])
               if len(grupos) >= 2 and validos.sum() > len(grupos) else np.nan)
        filas.append({"eps": eps, "grupos": len(grupos), "ruido": int((lab == -1).sum()),
                      "tamaños": [int((lab == g).sum()) for g in grupos], "silueta_sin_ruido": sil,
                      "ARI_vs_KMeans": adjusted_rand_score(referencia, lab)})
    return pd.DataFrame(filas).set_index("eps")


def pca_2d(Z: np.ndarray, variables: list[str]):
    pca = PCA(n_components=2, random_state=SEMILLA).fit(Z)
    cargas = pd.DataFrame(pca.components_.T, index=variables, columns=["CP1", "CP2"])
    return pca.transform(Z), pca.explained_variance_ratio_, cargas

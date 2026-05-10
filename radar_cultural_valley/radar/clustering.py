from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def cluster_opportunities(scored: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    if scored.empty or len(scored) < n_clusters:
        result = scored.copy()
        result["cluster"] = "dados_insuficientes"
        return result

    features = [
        "popularidade_norm",
        "engajamento_norm",
        "sinal_tendencia_norm",
        "volume_social_norm",
        "novidade_norm",
        "aderencia_estrategica_norm",
    ]
    X = scored[features].fillna(0)
    X_scaled = StandardScaler().fit_transform(X)
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")

    result = scored.copy()
    result["cluster_id"] = model.fit_predict(X_scaled)
    labels = {
        0: "Apostas emergentes",
        1: "Conteúdos de escala",
        2: "Nichos estratégicos",
    }
    result["cluster"] = result["cluster_id"].map(labels).fillna("Cluster cultural")
    return result

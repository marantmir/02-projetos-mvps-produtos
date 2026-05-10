from __future__ import annotations

import numpy as np
import pandas as pd
from .config import ScoreWeights


def _norm(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").fillna(0)
    min_v, max_v = values.min(), values.max()
    if max_v == min_v:
        return pd.Series(np.zeros(len(values)), index=series.index)
    return (values - min_v) / (max_v - min_v)


def build_unified_candidates(sources: dict[str, pd.DataFrame]) -> pd.DataFrame:
    spotify = sources.get("spotify", pd.DataFrame()).copy()
    youtube = sources.get("youtube", pd.DataFrame()).copy()
    trends = sources.get("trends", pd.DataFrame()).copy()
    x = sources.get("x", pd.DataFrame()).copy()

    rows = []

    if not spotify.empty:
        for _, row in spotify.iterrows():
            rows.append({
                "conteudo": row.get("nome"),
                "origem": "Spotify",
                "categoria": row.get("genero", "música"),
                "popularidade": row.get("popularidade", 0),
                "engajamento": row.get("popularidade", 0),
                "sinal_tendencia": 0,
                "volume_social": 0,
                "novidade": 0.55,
                "aderencia_estrategica": 0.70,
            })

    if not youtube.empty:
        max_views = max(float(youtube["visualizacoes"].max()), 1.0) if "visualizacoes" in youtube.columns else 1.0
        for _, row in youtube.iterrows():
            views = row.get("visualizacoes", 0)
            likes = row.get("likes", 0)
            rows.append({
                "conteudo": row.get("titulo"),
                "origem": "YouTube",
                "categoria": row.get("tema", "vídeo"),
                "popularidade": views / max_views * 100,
                "engajamento": likes,
                "sinal_tendencia": 0,
                "volume_social": 0,
                "novidade": 0.50,
                "aderencia_estrategica": 0.75,
            })

    if not trends.empty:
        for _, row in trends.iterrows():
            rows.append({
                "conteudo": row.get("termo"),
                "origem": "Google Trends",
                "categoria": "busca",
                "popularidade": row.get("interesse", 0),
                "engajamento": 0,
                "sinal_tendencia": row.get("crescimento_pct", 0),
                "volume_social": 0,
                "novidade": 0.80,
                "aderencia_estrategica": 0.80,
            })

    if not x.empty:
        for _, row in x.iterrows():
            rows.append({
                "conteudo": row.get("assunto"),
                "origem": "X",
                "categoria": "conversa social",
                "popularidade": 0,
                "engajamento": row.get("volume", 0) * row.get("sentimento", 0.5),
                "sinal_tendencia": 0,
                "volume_social": row.get("volume", 0),
                "novidade": 0.65,
                "aderencia_estrategica": 0.72,
            })

    candidates = pd.DataFrame(rows).dropna(subset=["conteudo"])
    if candidates.empty:
        return candidates

    # Agrupa sinais iguais vindos de múltiplas fontes.
    grouped = candidates.groupby("conteudo", as_index=False).agg({
        "origem": lambda s: ", ".join(sorted(set(s))),
        "categoria": lambda s: ", ".join(sorted(set(map(str, s))))[:120],
        "popularidade": "max",
        "engajamento": "max",
        "sinal_tendencia": "max",
        "volume_social": "max",
        "novidade": "mean",
        "aderencia_estrategica": "mean",
    })
    return grouped


def score_candidates(candidates: pd.DataFrame, weights: ScoreWeights | None = None) -> pd.DataFrame:
    if candidates.empty:
        return candidates

    weights = weights or ScoreWeights()
    df = candidates.copy()

    for col in ["popularidade", "engajamento", "sinal_tendencia", "volume_social"]:
        df[f"{col}_norm"] = _norm(df[col])

    # novidade e aderência já estão em escala 0-1 por desenho.
    df["novidade_norm"] = pd.to_numeric(df["novidade"], errors="coerce").fillna(0).clip(0, 1)
    df["aderencia_estrategica_norm"] = pd.to_numeric(df["aderencia_estrategica"], errors="coerce").fillna(0).clip(0, 1)

    df["score_oportunidade"] = (
        df["popularidade_norm"] * weights.popularity
        + df["engajamento_norm"] * weights.engagement
        + df["sinal_tendencia_norm"] * weights.trend_signal
        + df["volume_social_norm"] * weights.social_volume
        + df["novidade_norm"] * weights.novelty
        + df["aderencia_estrategica_norm"] * weights.strategic_fit
    ) * 100

    df["prioridade"] = pd.cut(
        df["score_oportunidade"],
        bins=[-1, 45, 65, 80, 101],
        labels=["Monitorar", "Testar", "Priorizar", "Apostar forte"],
    )

    return df.sort_values("score_oportunidade", ascending=False).reset_index(drop=True)

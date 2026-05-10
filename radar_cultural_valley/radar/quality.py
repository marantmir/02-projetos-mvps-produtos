from __future__ import annotations

import pandas as pd


def validate_dataframe(df: pd.DataFrame, required_columns: list[str], source_name: str) -> dict:
    missing = [col for col in required_columns if col not in df.columns]
    return {
        "fonte": source_name,
        "linhas": int(len(df)) if isinstance(df, pd.DataFrame) else 0,
        "colunas": list(df.columns) if isinstance(df, pd.DataFrame) else [],
        "colunas_ausentes": missing,
        "valido": isinstance(df, pd.DataFrame) and not df.empty and not missing,
    }


def build_quality_report(sources: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rules = {
        "spotify": ["nome", "artista", "popularidade"],
        "youtube": ["titulo", "canal", "visualizacoes"],
        "trends": ["termo"],
        "x": ["assunto", "volume", "created_at"],
    }
    report = [validate_dataframe(sources.get(src, pd.DataFrame()), cols, src) for src, cols in rules.items()]
    return pd.DataFrame(report)

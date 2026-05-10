from __future__ import annotations

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


def build_topic_baskets(sources: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Cria cestas simples por fonte para encontrar coocorrência de sinais culturais."""
    baskets = []

    if not sources.get("trends", pd.DataFrame()).empty:
        baskets.append(set(sources["trends"].get("termo", pd.Series(dtype=str)).astype(str).str.lower()))
    if not sources.get("x", pd.DataFrame()).empty:
        baskets.append(set(sources["x"].get("assunto", pd.Series(dtype=str)).astype(str).str.lower()))
    if not sources.get("youtube", pd.DataFrame()).empty:
        baskets.append(set(sources["youtube"].get("tema", pd.Series(dtype=str)).astype(str).str.lower()))
    if not sources.get("spotify", pd.DataFrame()).empty:
        baskets.append(set(sources["spotify"].get("genero", pd.Series(dtype=str)).astype(str).str.lower()))

    topics = sorted(set().union(*baskets)) if baskets else []
    if not topics:
        return pd.DataFrame()

    rows = []
    for basket in baskets:
        rows.append({topic: topic in basket for topic in topics})
    return pd.DataFrame(rows)


def discover_associations(sources: dict[str, pd.DataFrame], min_support: float = 0.25, min_confidence: float = 0.5) -> pd.DataFrame:
    encoded = build_topic_baskets(sources)
    if encoded.empty or encoded.shape[0] < 2:
        return pd.DataFrame(columns=["antecedents", "consequents", "support", "confidence", "lift"])

    frequent = apriori(encoded, min_support=min_support, use_colnames=True)
    if frequent.empty:
        return pd.DataFrame(columns=["antecedents", "consequents", "support", "confidence", "lift"])

    rules = association_rules(frequent, metric="confidence", min_threshold=min_confidence)
    if rules.empty:
        return rules

    rules = rules[["antecedents", "consequents", "support", "confidence", "lift"]].copy()
    rules["antecedents"] = rules["antecedents"].apply(lambda x: ", ".join(sorted(x)))
    rules["consequents"] = rules["consequents"].apply(lambda x: ", ".join(sorted(x)))
    return rules.sort_values(["lift", "confidence"], ascending=False).reset_index(drop=True)

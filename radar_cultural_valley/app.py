from __future__ import annotations

import streamlit as st
import pandas as pd

from radar.config import ProductConfig, ScoreWeights
from radar.demo_data import load_demo_sources
from radar.quality import build_quality_report
from radar.scoring import build_unified_candidates, score_candidates
from radar.clustering import cluster_opportunities
from radar.apriori_engine import discover_associations
from radar.content_ai import generate_content_brief, build_ai_prompt
from radar.visuals import render_kpis, render_opportunity_chart, render_source_mix, render_scatter

config = ProductConfig()

st.set_page_config(page_title=config.app_name, page_icon="🧠", layout="wide")

st.title("🧠 Radar Cultural AI")
st.caption(config.app_subtitle)

st.sidebar.header("Configuração estratégica")
country = st.sidebar.selectbox("Mercado", ["Brasil", "Global", "América Latina"], index=0)
objective = st.sidebar.selectbox(
    "Objetivo de conteúdo",
    ["Alcance", "Engajamento", "Autoridade", "Conversão", "Lançamento de produto"],
)
min_score = st.sidebar.slider("Score mínimo", 0, 100, 45)
brand_context = st.sidebar.text_area("Contexto da marca/produtor", placeholder="Ex.: produtor musical independente, canal de tecnologia, marca de moda...")

sources = load_demo_sources()
quality_report = build_quality_report(sources)
candidates = build_unified_candidates(sources)
scored = score_candidates(candidates, ScoreWeights())
scored = cluster_opportunities(scored)
filtered = scored[scored["score_oportunidade"] >= min_score].copy()

executivo, oportunidades, associacoes, ia_criativa, qualidade = st.tabs([
    "Visão executiva",
    "Radar de oportunidades",
    "Associações culturais",
    "IA criativa",
    "Governança dos dados",
])

with executivo:
    st.subheader(f"Pulso cultural — {country} | Objetivo: {objective}")
    render_kpis(filtered)
    left, right = st.columns([2, 1])
    with left:
        render_opportunity_chart(filtered)
    with right:
        render_source_mix(filtered)

with oportunidades:
    st.subheader("Ranking explicável de oportunidades")
    render_scatter(filtered)
    st.dataframe(
        filtered[[
            "conteudo", "prioridade", "score_oportunidade", "origem", "categoria", "cluster",
            "popularidade", "engajamento", "sinal_tendencia", "volume_social"
        ]],
        use_container_width=True,
        hide_index=True,
    )

with associacoes:
    st.subheader("Temas que aparecem juntos")
    rules = discover_associations(sources)
    if rules.empty:
        st.info("Ainda não há volume suficiente para regras fortes. Aumente dados ou reduza suporte/confiança.")
    else:
        st.dataframe(rules, use_container_width=True, hide_index=True)

with ia_criativa:
    st.subheader("Brief automático para produção de conteúdo")
    if filtered.empty:
        st.warning("Nenhuma oportunidade acima do score mínimo.")
    else:
        selected = st.selectbox("Escolha uma oportunidade", filtered["conteudo"].tolist())
        row = filtered[filtered["conteudo"] == selected].iloc[0]
        brief = generate_content_brief(row)
        st.json(brief)
        st.markdown("### Prompt premium para IA generativa")
        st.code(build_ai_prompt(row, brand_context), language="text")

with qualidade:
    st.subheader("Data quality e observabilidade")
    st.dataframe(quality_report, use_container_width=True, hide_index=True)
    st.markdown(
        """
        **Recomendação de produção:** criar logs estruturados, trilha de auditoria, versionamento de features,
        monitoramento de APIs, controle de custo e validação automática por fonte antes de alimentar o score.
        """
    )

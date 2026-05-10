from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render_kpis(scored: pd.DataFrame) -> None:
    if scored.empty:
        st.info("Sem oportunidades calculadas ainda.")
        return
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Oportunidades", len(scored))
    col2.metric("Score máximo", f"{scored['score_oportunidade'].max():.1f}")
    col3.metric("Apostas fortes", int((scored["prioridade"] == "Apostar forte").sum()))
    col4.metric("Fontes integradas", scored["origem"].str.split(", ").explode().nunique())


def render_opportunity_chart(scored: pd.DataFrame) -> None:
    if scored.empty:
        return
    top = scored.head(12).sort_values("score_oportunidade")
    fig = px.bar(
        top,
        x="score_oportunidade",
        y="conteudo",
        orientation="h",
        color="prioridade",
        hover_data=["origem", "categoria"],
        title="Top oportunidades culturais por score proprietário",
    )
    st.plotly_chart(fig, use_container_width=True)


def render_source_mix(scored: pd.DataFrame) -> None:
    if scored.empty:
        return
    exploded = scored.assign(origem=scored["origem"].str.split(", ")).explode("origem")
    fig = px.pie(exploded, names="origem", title="Participação das fontes nos sinais detectados")
    st.plotly_chart(fig, use_container_width=True)


def render_scatter(scored: pd.DataFrame) -> None:
    if scored.empty:
        return
    fig = px.scatter(
        scored,
        x="sinal_tendencia_norm",
        y="engajamento_norm",
        size="score_oportunidade",
        color="prioridade",
        hover_name="conteudo",
        title="Matriz: tendência x engajamento",
    )
    st.plotly_chart(fig, use_container_width=True)

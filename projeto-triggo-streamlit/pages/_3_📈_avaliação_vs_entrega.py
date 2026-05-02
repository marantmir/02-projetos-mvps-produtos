import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def get_review_data():
    from utils.load_data import load_data_from_sql
    df = load_data_from_sql()
    review_data = df[['review_score', 'delivery_days']].dropna()
    return review_data

def main():
    st.header("📉 Avaliação vs Tempo de Entrega")
    data = get_review_data()

    st.markdown("### Relação entre nota do cliente e tempo de entrega:")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(data=data, x='delivery_days', y='review_score', alpha=0.5, ax=ax)
    ax.set_xlabel("Tempo de Entrega (dias)")
    ax.set_ylabel("Nota do Cliente")
    st.pyplot(fig)

main()

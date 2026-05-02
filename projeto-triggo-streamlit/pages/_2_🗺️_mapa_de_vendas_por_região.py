import streamlit as st
import pandas as pd
from utils.load_data import load_data_from_sql

@st.cache_data
def get_sales_by_state():
    df = load_data_from_sql()
    if 'customer_state' not in df.columns or 'price' not in df.columns:
        raise KeyError("Colunas necessárias não encontradas no DataFrame")
    sales_by_state = df.groupby('customer_state')['price'].sum().reset_index()
    return sales_by_state

def main():
    st.header("🗺️ Mapa de Vendas por Estado")

    try:
        sales_by_state = get_sales_by_state()
        fig = st.map(sales_by_state,
                     latitude='customer_state',
                     longitude='customer_state',
                     size='price',
                     zoom=3)
        st.write(fig)
    except KeyError as e:
        st.error(f"Erro ao carregar dados: {e}")
    except Exception as e:
        st.warning("Dados insuficientes ou formato incorreto para visualização.")

main()

import streamlit as st
import pandas as pd
from utils.load_data import load_data_from_sql, download_and_cache_data
from utils.db_utils import init_db

init_db()

st.set_page_config(page_title="Dashboard E-commerce", layout="wide")

st.title("🛒 Dashboard de Análise de Vendas - Olist")
st.markdown("Projeto desenvolvido como parte do teste técnico da Triggo.ai.")

# Navegação
st.sidebar.title("📌 Navegação")
pages = {
    "1. Vendas por Mês e Categoria": "_1_📊_Vendas_por_Mês_e_Categoria",
    "2. Mapa de Vendas por Região": "_2_🗺️_Mapa_de_Vendas_por_Região",
    "3. Avaliação vs Tempo de Entrega": "_3_📈_Avaliação_vs_Entrega",
    "4. Análise de Vendedores": "_4_🧑‍💼_Análise_de_Vendedores"
}

selection = st.sidebar.radio("Ir para:", list(pages.keys()))

# Caminho absoluto para evitar erro de diretório
current_dir = os.path.dirname(__file__)
page_file = f"{pages[selection]}.py"
page_path = os.path.join(current_dir, 'pages', page_file)

if os.path.exists(page_path):
    with open(page_path, 'r', encoding='utf-8') as f:
        code = compile(f.read(), page_file, 'exec')
        exec(code)
else:
    st.error(f"❌ Arquivo não encontrado: {page_path}")
    st.stop()

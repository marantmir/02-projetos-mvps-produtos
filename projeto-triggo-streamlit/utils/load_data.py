import pandas as pd
import kagglehub
import sqlite3
import os

def get_db_connection():
    return sqlite3.connect('olist.db')

def create_tables(df_orders):
    conn = get_db_connection()
    df_orders.to_sql('orders', conn, if_exists='replace', index=False)
    conn.close()

def load_data_from_sql():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    conn.close()
    return df

def download_and_cache_data():
    path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
    print(f"Dataset baixado em: {path}")

    # Carregar arquivos CSV do dataset
    df_orders = pd.read_csv(os.path.join(path, "olist_orders_dataset.csv"))
    df_customers = pd.read_csv(os.path.join(path, "olist_customers_dataset.csv"))
    df_items = pd.read_csv(os.path.join(path, "olist_order_items_dataset.csv"))

    # Converter datas
    df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])
    df_orders['order_delivered_customer_date'] = pd.to_datetime(df_orders['order_delivered_carrier_date'], errors='coerce')
    df_orders['order_estimated_delivery_date'] = pd.to_datetime(df_orders['order_estimated_delivery_date'])

    # Tratar valores nulos
    df_orders = df_orders.dropna(subset=['order_delivered_customer_date'])

    # Junções básicas
    df_full = pd.merge(df_orders, df_customers, on='customer_id', how='inner')
    df_full = pd.merge(df_full, df_items, on='order_id', how='inner')

    # Calcular tempo de entrega
    df_full['delivery_days'] = (df_full['order_delivered_customer_date'] - df_full['order_purchase_timestamp']).dt.days
    df_full['delayed'] = (df_full['order_delivered_customer_date'] > df_full['order_estimated_delivery_date']).astype(int)

    # Salvar no SQLite
    create_tables(df_orders)

    return df_full

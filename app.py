import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "total_order_value": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "total_order_value": "revenue"
    }, inplace=True)
    
    return daily_orders_df
  def create_sum_order_items_df(df):
    order_by_product_category = df.groupby(by="product_category_name_english").agg(num_of_order=('order_id', 'count')).reset_index()
    top_10_categories = order_by_product_category.sort_values(by=['num_of_order'], ascending=False)
    return top_10_categories
  def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_unique_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bystate_df
  def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": "max", #mengambil tanggal order terakhir
        "order_id": "nunique",
        "total_price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_purchase_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_purchase_timestamp"] = rfm_df["max_order_purchase_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_purchase_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_purchase_timestamp", axis=1, inplace=True)
    return rfm_df
all_df = pd.read_csv("all_data_ecommerce.csv")
all_df.info()
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
st.write()
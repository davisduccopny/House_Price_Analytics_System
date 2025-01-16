import streamlit as st
import pandas as pd
import os
import numpy as np
import PROJECTS.config as module_config
import altair as alt
import plotly.express as px
import json


def query_to_dataframe(query, conn):
    cursor = conn.cursor(dictionary=True)  
    cursor.execute(query)
    data = cursor.fetchall()  
    cursor.close()
    return pd.DataFrame(data)

@st.cache_data
def load_data():
    conn = module_config.connect_to_mysql()
    try:
        region_info = query_to_dataframe(f"SELECT tinh_thanh_pho,ma_tp,quan_huyen,ma_qh,phuong_xa,ma_px FROM region_info;", conn)
        house_price = query_to_dataframe(f"SELECT dia_chi, dien_tich,gia,longitude,latitude FROM thong_tin_bat_dong_san;",conn)
        return region_info,house_price
    finally:
        conn.close()
@st.cache_data
def load_data_from_csv():
    data = pd.read_csv("data/data_prosesing.csv")
    data = pd.DataFrame(data)
    return data

@st.cache_data
def load_region_data_json():
    with open("src/location/output.geojson", "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
    return geojson_data

@st.cache_resource
def load_model(model_path):
    import joblib
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None
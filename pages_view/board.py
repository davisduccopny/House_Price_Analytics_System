import streamlit as st
import pandas as pd
import json
from openpyxl.styles import Font, Border, Side, PatternFill, Alignment
from openpyxl import Workbook
import openpyxl
import time
import datetime
import plotly.express as px
import PROJECTS.config as module_config


# PART SET CONFIG
with open('src/style/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True) 
with open('src/style/style_board.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
if "login_request" not in st.session_state:
    st.session_state.login_request = None
if "register_request" not in st.session_state:
    st.session_state.register_request = None
# PART LOAD DATA
@st.cache_data
def load_data_from_csv():
    data = pd.read_csv("data/data_prosesing.csv")
    data = pd.DataFrame(data)
    return data
@st.cache_data
def load_region_data_json():
    with open("src/location/diaphantinh.geojson", "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
    return geojson_data
# PART BOARD PREDICT
class BOARD_PREDICT():
    def __init__(self):
        self.province_data = module_config.show_province()
        self.province_data_arr = {row["ma_tp"]: row["tinh_thanh_pho"] for _, row in self.province_data.iterrows()}
        self.selected_provine_key =list(self.province_data_arr.keys())
    
    def filter_data(self,data,selected_provine,max_price,min_price):
        selected_provine = float(selected_provine) if selected_provine != "Tất cả" else selected_provine
        if selected_provine != "Tất cả":
            data_selected = data[(data["Ma_TP"] == selected_provine) &
                        (data["Price"] >= min_price) &
                        (data["Price"] <= max_price)]
        else:
            data_selected = data[(data["Price"] >= min_price) &
                        (data["Price"] <= max_price)]
        return data_selected
    def map_vietnam_chart_price(self,data, geojson_data):
        data = data.rename(columns={"Province": "ten_tinh"})
        if len(data["ten_tinh"].unique()) > 1:
            data = data.groupby("ten_tinh").agg({"Price": "mean"}).reset_index()
            all_provinces = [feature["properties"]["ten_tinh"] for feature in geojson_data["features"]]
            data = data.set_index("ten_tinh").reindex(all_provinces).reset_index()
            data["Price"] = data["Price"].fillna(0)
        else:
            data = data.groupby("ten_tinh").agg({"Price": "mean"}).reset_index()
        
        fig = px.choropleth(
            data_frame=data,
            geojson=geojson_data,
            locations="ten_tinh",  
            featureidkey="properties.ten_tinh",  
            color="Price", 
            labels={"Price": "Average"},
            projection="mercator"
        )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            geo=dict(
            projection_scale=50
            )
        )
        st.plotly_chart(fig,use_container_width=True,theme="streamlit",key="map_vietnam_chart_price")
    def Pie_chart_by_params(self,data, params):
        data["Count"] = data.groupby(params)[params].transform('count')
        data["Percentage"] = (data["Count"] / data["Count"].sum()) * 100
        data = data[[params, "Percentage"]]
        pie_fig = px.pie(
            data, 
            names= params,
            values="Percentage", 
            labels=params,
            hole=0.3,
        )
        pie_fig.update_traces(
                        hoverlabel=dict(
                        bgcolor="lightblue",  # Màu nền khi hover
                        font_size=14,         # Kích thước chữ
                        font_color="black"    # Màu chữ
                    )
        )
        
        pie_fig.update_layout(
            title={
            'text': f"Biểu đồ phân bố {params}",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
            legend={
            "y": -0.005, 
            "x": 0.5,
            "xanchor": "center",
            "orientation": "h"
            },
            margin=dict(l=0, r=0, t=50, b=0),
            height=300
        )

        st.plotly_chart(pie_fig, use_container_width=True, theme="streamlit", key="pie_fig_params")
    
    def box_plot_by_params(self, data, params):
        box_fig = px.box(
            data,
            x=params,
            y="Price",
            points="all",
            labels={params: params, "Price": "Price"},
            title=f"Mối quan hệ {params} với Giá"
        )
        box_fig.update_traces(
                        hoverlabel=dict(
                        bgcolor="lightblue",  # Màu nền khi hover
                        font_size=14,         # Kích thước chữ
                        font_color="black"    # Màu chữ
                    )
        )
        box_fig.update_traces(
            marker=dict(size=5, opacity=0.7)
        )
        box_fig.update_layout(
            title={
                'text': f"Mối quan hệ {params} với Giá",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            margin=dict(l=0, r=0, t=50, b=0),
            height=300
        )
        st.plotly_chart(box_fig, use_container_width=True, theme="streamlit", key="box_fig_params")
    
    def house_board_predict(self):
        if "display_name_house" not in st.session_state:
            st.session_state.display_name_house = None
        ctn_house_header = st.container(key="ctn_house_header")
        data_show = load_data_from_csv()
        with ctn_house_header:
            cols_house_header = st.columns([1,1,1])
            cols_house_header[0].write(" ")
            cols_house_header[0].info("HOUSE PRICE PREDICTION" if st.session_state.display_name_house is None else st.session_state.display_name_house,icon=":material/grid_view:")
            
            selected_provine = cols_house_header[1].selectbox("Chọn tỉnh thành",options=["Tất cả"] + list(self.selected_provine_key),
                                                              format_func=lambda x: "Tất cả" if x == "Tất cả" else self.province_data_arr.get(x, ""),
                                                              key="selected_provine")
            
            price_range = cols_house_header[2].slider(
                "Chọn khoảng giá (tỷ đồng):",
                min_value=data_show["Price"].min(),
                max_value=data_show["Price"].max(),
                value=(6.0, 10.0),  
                step=0.5
            )
        data_selected = self.filter_data(data_show,selected_provine,price_range[1],price_range[0])
        with st.spinner("Đang tải giao diện..."):
            ctn_main_board_house = st.container(key="ctn_main_board_house")
            with ctn_main_board_house:
                cols_main_board_house = st.columns([1.4,4.5,2.1])
                with cols_main_board_house[0]:
                    ctn_metric_board_01 = st.container(key="ctn_metric_board_01")
                    ctn_metric_board_02 = st.container(key="ctn_metric_board_02")
                    ctn_metric_board_03 = st.container(key="ctn_metric_board_03")

                    if data_selected is not None:
                        ctn_metric_board_01.metric("Số đang bán",len(data_selected))
                        avg_price = round(data_selected["Price"].mean(), 2)
                        ctn_metric_board_02.metric(label="Giá trung bình", value=f"{avg_price} tỷ")
                        avg_area = round(data_selected["Area"].mean(), 2)
                        ctn_metric_board_03.metric(label="S trung bình (m²)", value=f"{avg_area} m²")
                    else:
                        ctn_metric_board_01.metric("Số đang bán",0)
                        ctn_metric_board_02.metric(label="Giá trung bình", value=f"0 tỷ")
                        ctn_metric_board_03.metric(label="S trung bình (m²)", value=f"0 m²")
                    ctn_metric_board_01.caption("Số lượng")
                    ctn_metric_board_02.caption("Giá trung bình")
                    ctn_metric_board_03.caption("Diện tích trung bình")
                with cols_main_board_house[1]:
                    geojson_data = load_region_data_json()
                    self.map_vietnam_chart_price(data_selected, geojson_data)
                    
                with cols_main_board_house[2]:
                    if data_selected is not None:
                        data_show_df_mean = data_selected.groupby("Province").agg({"Price": "mean"}).reset_index()
                        st.data_editor(data_show_df_mean,
                                    column_config={
                                        "Province": "Tỉnh thành",
                                        "Price":  st.column_config.ProgressColumn(
                                            "Giá trung bình (tỷ đồng)",
                                                min_value=data_show["Price"].min(),
                                                max_value=data_show["Price"].max(),
                                                format="%.2f"
                                                
                                        )
                                    },hide_index=True,disabled=True,height=400,use_container_width=True)
                    else:
                        st.write("Không có dữ liệu")
            ctn_secondary_board_house = st.container(key="ctn_secondary_board_house")
            with ctn_secondary_board_house:
                cols_secondary_board_house = st.columns([0.4,1,1])
                with cols_secondary_board_house[0]:
                    radio_selected_params = st.radio("Chọn thông số", ['Floors', 'Bedrooms', 'Bathrooms'],key="radio_selected_params")
                with cols_secondary_board_house[1]:
                    self.Pie_chart_by_params(data_selected, radio_selected_params) 
                with cols_secondary_board_house[2]:
                    self.box_plot_by_params(data_selected, radio_selected_params)

            
class MAIN_BOARD():
    def __init__(self):
        pass
    def run_board(self):
        module_config.create_db_pool()
        BOARD_PREDICT().house_board_predict()
        module_config.add_sidebar_footer()
if (st.session_state.login_request == False and st.session_state.register_request == False) or (st.session_state.login_request is None and st.session_state.register_request is None):
    MAIN_BOARD().run_board()
    

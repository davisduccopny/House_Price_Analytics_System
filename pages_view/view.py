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
from streamlit_option_menu import option_menu
import folium
from streamlit_folium import st_folium
from streamlit.components.v1 import html
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
import PROJECTS.module_predict as module_predict


# PART STYLE
with open('src/style/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True) 
with open('src/style/style_view.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True) 

# PART LOGIN
if "login_request" not in st.session_state:
    st.session_state.login_request = None
if "register_request" not in st.session_state:
    st.session_state.register_request = None
    
@st.cache_data()
def create_map(df,predict_price):
    if len(df["dia_chi"].unique()) > 1:
        map_center = [14.0583, 108.2772] 
        m = folium.Map(location=map_center, zoom_start=6,png_enabled=True,height="100vh")
    else:
        map_center = [df['latitude'].mean(), df['longitude'].mean()]
        m = folium.Map(location=map_center, zoom_start=12,png_enabled=True,height="100vh")
    
    marker_cluster = MarkerCluster().add_to(m)
    
    for index, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Giá: {row['gia']}<br>Thành phố: {row['dia_chi']}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(marker_cluster)
    if predict_price is not None:
        st.success(f"##### Giá nhà dự đoán: {round(predict_price,4)} tỷ VND")
    
    return m._repr_html_()
# PART VIEW
class VIEW_CLASS():
    def __init__(self):
        self.region_info,self.house_data = module_predict.load_data()
        
        self.province_data_arr = {row["ma_tp"]: row["tinh_thanh_pho"] for _, row in self.region_info[["ma_tp","tinh_thanh_pho"]].drop_duplicates().iterrows()}
        self.selected_provine_key =list(self.province_data_arr.keys())
        self.model_prediction = module_predict.load_model("notebooks/random_forest_model.pkl")
        st.session_state.house_data = self.house_data
    
    def predict_house_price(self,area, frontage, access_road, 
                            floors, bedrooms, bathrooms, 
                            Ma_TP, Ma_QH, Ma_PX):
        input_data = pd.DataFrame({
            'Area': [area],
            'Frontage': [frontage],
            'Access Road': [access_road],
            'Floors': [floors],
            'Bedrooms': [bedrooms],
            'Bathrooms': [bathrooms],
            'Ma_TP': [Ma_TP],
            'Ma_QH': [Ma_QH],
            'Ma_PX': [Ma_PX]
        })
        
        try:
            predicted_price = self.model_prediction.predict(input_data)[0]
            return predicted_price
        except NameError:
            return "Mô hình dự đoán chưa được khởi tạo."
    def ui_predict(self):
        ctn_hearder_predict_house = st.container(key="ctn_hearder_predict_house")
        with ctn_hearder_predict_house:
            cols_header = st.columns([1, 1, 1, 1,0.5])
            city_selected = cols_header[0].selectbox(" ",options=["Lựa chọn tỉnh"] + list(self.selected_provine_key),
                                                              format_func=lambda x: "Lựa chọn tỉnh" if x == "Lựa chọn tỉnh" else self.province_data_arr.get(x, ""),
                                                              key="selected_provine",index=50)
            
            if city_selected != "Lựa chọn tỉnh":
                district_data = self.region_info[self.region_info["ma_tp"] == city_selected][["ma_qh","quan_huyen"]].drop_duplicates()
            else:
                district_data = None
            district_selected = cols_header[1].selectbox(" ",options=["Lựa chọn huyện"] + (list(district_data["ma_qh"]) if district_data is not None else []),
                                                                format_func=lambda x: "Lựa chọn huyện" if x == "Lựa chọn huyện" else (district_data[district_data["ma_qh"] == x]["quan_huyen"].values[0] if district_data is not None else ""),
                                                                key="selected_district")
            if district_selected != "Lựa chọn huyện":
                ward_data = self.region_info[self.region_info["ma_qh"] == district_selected][["ma_px","phuong_xa"]].drop_duplicates()
            else:
                ward_data = None
            ward_selected = cols_header[2].selectbox(" ",options=["Lựa chọn phường"] + (list(ward_data["ma_px"]) if ward_data is not None else []),
                                                                format_func=lambda x: "Lựa chọn phường" if x == "Lựa chọn phường" else (ward_data[ward_data["ma_px"] == x]["phuong_xa"].values[0] if ward_data is not None else ""),
                                                                key="selected_ward")
            with cols_header[3].popover("Bổ sung",icon=":material/filter_list:",use_container_width=True):
                cols_expand_info = st.columns(2)
                area_input = cols_expand_info[0].number_input("Diện tích (m2)",min_value=0.0,value=50.0,step=0.1,key="area_input")
                fronstage_input = cols_expand_info[0].number_input("Mặt tiền (m)",min_value=0.0,value=5.0,step=0.1,key="fronstage_input")
                access_road_input = cols_expand_info[0].number_input("Đường vào (m)",min_value=0.0,value=5.0,step=0.1,key="access_road_input")
                floor_input = cols_expand_info[1].number_input("Số tầng",min_value=0.0,value=5.0,step=1.0,key="floor_input")
                bedroom_input = cols_expand_info[1].number_input("Số phòng ngủ",min_value=0.0,value=2.0,step=1.0,key="bedroom_input")
                badroom_input = cols_expand_info[1].number_input("Số phòng vệ sinh",min_value=0.0,value=2.0,step=1.0,key="badroom_input")
            predicted_price = None
            if cols_header[4].button("Dự đoán",key="btn_predict",use_container_width=True,type="primary"):
                with st.spinner("Đang dự đoán..."):
                    if (city_selected == "Lựa chọn tỉnh" or district_selected == "Lựa chọn huyện" or ward_selected == "Lựa chọn phường"):
                        st.toast("##### Vui lòng chọn đầy đủ thông tin về vị trí nhà cần dự đoán!",icon="🚫")
                    else:
                        predicted_price = self.predict_house_price(area_input, fronstage_input, access_road_input, floor_input, bedroom_input, badroom_input, city_selected, district_selected, ward_selected)
                        house_data = self.house_data.copy()
                        city_name = self.province_data_arr.get(city_selected, "")
                        house_data = house_data[house_data["dia_chi"] == city_name]
                        if house_data is not None:
                            st.session_state.house_data = house_data
            
            html(create_map(st.session_state.house_data,predicted_price))
                

    
class MAIN_CLASS():
    def __init__(self):
        pass
    def sidebar(self):
        with st.sidebar:
            selected = option_menu(
                menu_title= None,  # required
                options=["Dự đoán","Thống kê chi tiết"],
                icons=["clipboard-data-fill","clipboard2-pulse-fill"],  
                menu_icon= None,  
                default_index=0,  
                orientation="vertical",  
                key="menu_sidebar_delete",
                styles={
                "container": {
                    "padding": "0px 5px", 
                    "max-width": "100%",
                    "margin": "0px auto",  
                    "border": "None",
                    "border-radius": "20px",
                },
                "icon": {
                    "font-size": "0.8rem",
                    "font-weight": "bold",
                },
                "nav-link": {
                    "font-size": "0.8rem", 
                    "text-align": "left",  
                    "--hover-color": "#54a7ef",
                    "font-weight": "bold",
                },
                "nav-link-selected": {
                    "border-radius": "15px",
                    "font-size": "0.8rem",
                    "font-family": "Tahoma, Geneva, sans-serif",
                    
                    
                }
            }
                )
        return selected
    def run_view(self):
        selected = self.sidebar()
        if selected == "Dự đoán":
            VIEW_CLASS().ui_predict()
        else:
            st.title("Thống kê chi tiết")
            st.markdown("### Thống kê chi tiết")
if (st.session_state.login_request == False and st.session_state.register_request == False) or (st.session_state.login_request is None and st.session_state.register_request is None):
    MAIN_CLASS().run_view()
    module_config.add_sidebar_footer()
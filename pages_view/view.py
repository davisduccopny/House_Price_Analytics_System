import streamlit as st
import pandas as pd
import json
import time
import datetime
import plotly.express as px
import PROJECTS.config as module_config
from streamlit_option_menu import option_menu
import folium
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
    
@st.cache_data
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
                
    def ui_info_detail(self):
        
        ctn_hearder_info_detail = st.container(key="ctn_hearder_info_detail")
        with ctn_hearder_info_detail:
            cols_header = st.columns([0.5,0.5, 1])
            cols_header[0].markdown("""
                                    <h5 style="text-align:center;padding-top:10px">📊Thống kê chi tiết💰</h5>
                                    """,unsafe_allow_html=True)
            city_selected = cols_header[1].selectbox(" ",options=list(self.selected_provine_key),
                                                              format_func=lambda x: "Lựa chọn tỉnh" if x == "Lựa chọn tỉnh" else self.province_data_arr.get(x, ""),
                                                              key="selected_provine_detail",index=49)

            district_data = self.region_info[self.region_info["ma_tp"] == city_selected][["ma_qh","quan_huyen"]].drop_duplicates()
            district_selected = cols_header[2].multiselect("Chọn huyện: ",options=["Lựa chọn huyện"] + (list(district_data["ma_qh"]) if district_data is not None else []),
                                                                format_func=lambda x: "Lựa chọn huyện" if x == "Lựa chọn huyện" else (district_data[district_data["ma_qh"] == x]["quan_huyen"].values[0] if district_data is not None else ""),
                                                                key="selected_district_detail",default=["767","764","765"] if city_selected == "79" else [])
        with st.spinner("Đang tải dữ liệu..."):
            self.house_data_csv = module_predict.load_data_from_csv()
            district_selected = [(float(i)) for i in district_selected]
            house_data = self.house_data_csv.copy()
            house_data = house_data[house_data["Ma_QH"].isin(district_selected)]
            ctn_main_info_detail = st.container(key="ctn_main_info_detail")
            with ctn_main_info_detail:
                cols_main = st.columns([1,1])
                cols_main[0].plotly_chart(self.bar_chart_compare_price(house_data),use_container_width=True,key="bar_chart_price")
                cols_main[1].plotly_chart(self.bar_chart_compare_area(house_data),use_container_width=True,key="bar_chart_area")
            ctn_secondary_info_detail = st.container(key="ctn_secondary_info_detail")
            with ctn_secondary_info_detail:
                cols_secondary = st.columns([1,1])
                cols_secondary[0].plotly_chart(self.bar_chart_compare_bedrooms_and_bathrooms(house_data),use_container_width=True,key="scatter_chart_bedrooms_bathroom")
                cols_secondary[1].plotly_chart(self.bar_chart_compare_fronstage_and_accessRoad(house_data),use_container_width=True,key="scatter_chart_fronstage_accessRoad")
            ctn_third_info_detail = st.container(key="ctn_third_info_detail")
            with ctn_third_info_detail:
                ctn_child_third = st.container(key="ctn_child_third")
                with ctn_child_third:
                    cols_ctn_child_third = st.columns([0.4,1])
                    cols_ctn_child_third[0].markdown("""
                                                    <h5 style="text-align:center;">🗺️Bản đồ nhiệt so sánh💰</h5>
                                                    """,unsafe_allow_html=True)
                    radio_data_type = cols_ctn_child_third[1].radio("Chọn loại dữ liệu: ",["Giá nhà","Diện tích","Số phòng ngủ","Số phòng vệ sinh","Mặt tiền" ,"Đường vào"],horizontal=True,key="selectbox_data_type")
                city_selected = self.province_data_arr.get(city_selected, "")
                ctn_child_third_02 = st.container(key="ctn_child_third_02")
                with ctn_child_third_02:
                    html(self.map_chart_show_params(house_data,city_selected,district_selected,radio_data_type,district_data))
                        
                    
    def bar_chart_compare_price(self,df):
        df = df.groupby('District')['Price'].mean().reset_index()
        fig = px.bar(df, x='District', y='Price', color='District', title='Biểu đồ so sánh giá nhà',labels={'District':'Quận huyện','Price':'Giá nhà (tỷ VND)'})
        fig.update_layout(
            xaxis_title="Quận huyện",
            yaxis_title="Giá nhà (tỷ VND)",
            legend_title="Quận huyện",
            font=dict(
            size=12,
            color="RebeccaPurple"
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            height=250,
            title={
            'text': "Biểu đồ so sánh giá nhà",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            }
        )
        return fig
    def bar_chart_compare_area(self,df):
        df = df.groupby('District')['Area'].mean().reset_index()
        fig = px.bar(df, x='District', y='Area', color='District', title='Biểu đồ so sánh diện tích nhà theo Quận huyện',labels={'District':'Quận huyện','Area':'Diện tích nhà (m2)'})
        fig.update_layout(
            xaxis_title="Quận huyện",
            yaxis_title="Diện tích nhà (m2)",
            legend_title="Quận huyện",
            font=dict(
            size=12,
            color="RebeccaPurple"
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            height=250,
            title={
            'text': "Biểu đồ so sánh diện tích nhà",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            }
        )
        return fig
    def bar_chart_compare_bedrooms_and_bathrooms(self, df):
        df = df.groupby(['District']).agg({'Bedrooms': 'mean', 'Bathrooms': 'mean'}).reset_index()
        fig = px.bar(df, x='District', y=['Bedrooms', 'Bathrooms'], barmode='group',
                     title='Biểu đồ so sánh trung bình số phòng ngủ và số phòng vệ sinh',
                     labels={'value': 'Số lượng trung bình', 'variable': 'Loại phòng'})
        fig.update_layout(
            xaxis_title="Quận huyện",
            yaxis_title="Số lượng trung bình",
            legend_title="Loại phòng",
            font=dict(
                size=12,
                color="RebeccaPurple"
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            height=250,
            title={
                'text': "Biểu đồ so sánh trung bình số phòng ngủ và số phòng vệ sinh",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        return fig
    def bar_chart_compare_fronstage_and_accessRoad(self, df):
        df = df.groupby(['District']).agg({'Frontage': 'mean', 'Access Road': 'mean'}).reset_index()
        fig = px.bar(df, x='District', y=['Frontage', 'Access Road'], barmode='group',
                     title='Biểu đồ so sánh trung bình mặt tiền và đường vào',
                     labels={'value': 'Số lượng trung bình', 'variable': 'Loại phòng'})
        fig.update_layout(
            xaxis_title="Quận huyện",
            yaxis_title="Số lượng trung bình",
            legend_title="Loại phòng",
            font=dict(
                size=12,
                color="RebeccaPurple"
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            height=250,
            title={
                'text': "Biểu đồ so sánh trung bình mặt tiền và đường vào",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        return fig
    
    def map_chart_show_params(self, df, city_selected, selected_districts, radio_data_type, district_data):
        from unidecode import unidecode
        df["District"] = df['District'].apply(unidecode)
        district_data["ma_qh"] = district_data["ma_qh"].astype(int)
        try:

            selected_districts = [int(district) for district in selected_districts]
            mapping = dict(zip(district_data['ma_qh'].astype(str), district_data['quan_huyen']))
            selected_districts_names = [mapping[str(district)] for district in selected_districts if str(district) in mapping]
            selected_districts_names = [unidecode(mapping[str(district)]) for district in selected_districts if str(district) in mapping]
            
            
            if not selected_districts_names:
                st.error("Không có quận/huyện nào hợp lệ được chọn!")
                return None

            geojson_data = module_predict.load_region_data_json()

            data_column_map = {
                "Giá nhà": "Price",
                "Diện tích": "Area",
                "Số phòng ngủ": "Bedrooms",
                "Số phòng vệ sinh": "Bathrooms",
                "Mặt tiền": "Frontage",
                "Đường vào": "Access Road"
            }
            data_column = data_column_map.get(radio_data_type)
            if not data_column:
                st.error(f"Loại dữ liệu '{radio_data_type}' không hợp lệ!")
                return None

            district_lat_lon = {}
            for feature in geojson_data['features']:
                province_name = feature['properties']['Ten_Tinh']  
                district_name = feature['properties']['Ten_Huyen']  
                
                if province_name == city_selected and district_name in selected_districts_names:
                    coords = feature['geometry']['coordinates'][0]
                    lat = sum([coord[1] for coord in coords]) / len(coords)
                    lon = sum([coord[0] for coord in coords]) / len(coords)
                    district_lat_lon[district_name] = [lat, lon]

            if not district_lat_lon:
                st.error(f"Không tìm thấy dữ liệu quận/huyện cho tỉnh {city_selected}.")
                return None
            
            if district_lat_lon:
                first_district_coords = list(district_lat_lon.values())[0]
                m = folium.Map(location=first_district_coords, zoom_start=12)
            else:
                m = folium.Map(location=[21.0285, 105.8542], zoom_start=12)


            for district_name, coords in district_lat_lon.items():
                if district_name in df['District'].values:
                    value = df[df['District'] == district_name][data_column].values[0]
                    folium.CircleMarker(
                        location=coords,
                        radius=5,
                        color='blue',
                        fill=True,
                        fill_color='blue',
                        fill_opacity=0.7,
                        popup=f"{district_name}: {value}"
                    ).add_to(m)
                else:
                    st.warning(f"Dữ liệu cho huyện '{district_name}' không có trong DataFrame!")

            if not df.empty:
                heat_data = [
                    [coords[0], coords[1], df[df['District'] == district_name][data_column].values[0]]
                    for district_name, coords in district_lat_lon.items()
                    if district_name in df['District'].values
                ]
                HeatMap(heat_data).add_to(m)

            if df.empty:
                for feature in geojson_data['features']:
                    if feature['properties']['Ten_Tinh'] == city_selected:
                        folium.GeoJson(feature).add_to(m)

            return m._repr_html_()
        except Exception as e:
            st.error(f"Lỗi khi tạo bản đồ: {e}")
            return None

    
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
            VIEW_CLASS().ui_info_detail()
if (st.session_state.login_request == False and st.session_state.register_request == False) or (st.session_state.login_request is None and st.session_state.register_request is None):
    MAIN_CLASS().run_view()
    module_config.add_sidebar_footer()
    
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import time
import PROJECTS.config as module_config
import PROJECTS.module_expand as module_expand
import PROJECTS.module_users as module_users
import numpy as np
import plotly.graph_objects as go
from PROJECTS.module_expand import load_page_data_references

if "login_request" not in st.session_state:
    st.session_state.login_request = None
if "register_request" not in st.session_state:
    st.session_state.register_request = None
    
with open('src/style/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style/style_expand.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
class EXPAND_CLASS():
    def __init__(self):
        pass
    def ui_info(self, text,loai_data):
        container_title_manage_expand = st.container(key="container_title_manage_expand")
        with container_title_manage_expand:
            col_title_dmanage_expand = st.columns([5,2])
            col_title_dmanage_expand[0].markdown(f"""<h3 style='text-align: left; padding:0; margin-bottom:5px;'>{text}</h3>
                                            <p style='text-align: left; padding:0'>Biết nhiều hơn về bất động sản! <span style="color:#c4c411; font-weight:bolder;"> {loai_data} </span></p>""", unsafe_allow_html=True)
            with col_title_dmanage_expand[1]:
                with st.form(key="search_form", enter_to_submit=True,border=False):
                    cols_search = st.columns([6,1])
                    search_term = cols_search[0].text_input(label=" ",placeholder="Tìm kiếm thông tin", key="search_term",type="default")
                    if cols_search[1].form_submit_button("🔍",use_container_width=True):
                        if search_term:
                            return search_term
                        else:
                            st.toast(f"##### Vui lòng nhập thông tin!", icon="⚠️")
                            return None
    def calculate_loan(self,principal, rate, years):
        monthly_rate = rate / 12 / 100
        months = years * 12
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        
        payments = []
        remaining_balance = principal
        total_interest = 0

        for month in range(1, months + 1):
            interest_payment = remaining_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            total_interest += interest_payment
            payments.append((month, principal_payment, interest_payment, remaining_balance))

        return monthly_payment, payments, total_interest
    def loan_ui(self):
        ctn_loan_ui = st.container(key="container_loan_ui")
        with ctn_loan_ui:
            st.markdown("""
                        <h3 style='text-align: center; padding:0; margin-bottom:10px;'>CÔNG CỤ TÍNH KHOẢN VAY</h3>
                        """,unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                loan_amount = st.number_input("💵 Số tiền vay (triệu VND)", min_value=100, max_value=10000, value=2000, step=50,key="loan_amount_key_id")
            with col2:
                loan_term = st.number_input("📅 Thời gian vay (năm)", min_value=1, max_value=30, value=15, step=1,key="loan_term_number_input")
            interest_rate = st.slider("📊 Lãi suất hàng năm (%)", min_value=1.0, max_value=15.0, value=7.5, step=0.1,key="interest_rate_number_input")

            if st.button("Tính toán khoản vay",icon=":material/calculate:",key="button_calculate_loan"):
                monthly_payment, payments, total_interest = self.calculate_loan(loan_amount * 1_000_000, interest_rate, loan_term)

                st.subheader("📌 Kết quả:",divider="blue")
                st.write(f"💰 **Số tiền phải trả hàng tháng:** {monthly_payment:,.0f} VND")
                st.write(f"📉 **Tổng tiền lãi phải trả:** {total_interest:,.0f} VND")
                st.write(f"💵 **Tổng tiền phải trả sau {loan_term} năm:** {(monthly_payment * loan_term * 12):,.0f} VND")

                months = [p[0] for p in payments]
                principal_payments = [p[1] for p in payments]
                interest_payments = [p[2] for p in payments]
                remaining_balances = [p[3] for p in payments]

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=months, y=principal_payments, mode="lines", name="Trả gốc", fill="tozeroy"))
                fig.add_trace(go.Scatter(x=months, y=interest_payments, mode="lines", name="Trả lãi", fill="tozeroy"))
                fig.update_layout(title="Biểu đồ thanh toán khoản vay theo tháng", xaxis_title="Tháng", yaxis_title="Số tiền (VND)", legend_title="Loại khoản thanh toán")

                st.plotly_chart(fig, use_container_width=True,key="plotly_chart_loan")
   

    def reference_ui(self):
        if "references" not in st.session_state or len(st.session_state.references) == 0:
            st.session_state.references = load_page_data_references(0, 9)
            st.session_state.reference_offset = 9

        st.markdown("""
            <style>
                .grid-container {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    background-color: #f9f9f9;
                    padding: 20px;
                    border-radius: 10px;
                }
                .grid-item {
                    display: flex;
                    align-items: center;
                    background: white;
                    padding: 10px;
                    margin-bottom: 10px;
                    border-radius: 10px;
                    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
                }
                .grid-item img {
                    width: 80px;
                    height: 80px;
                    margin-right: 10px;
                    border-radius: 5px;
                }
                .grid-item a {
                    text-decoration: none;
                    color: #007BFF;
                    font-size: 16px;
                    font-weight: bold;
                }
            </style>
            <div class="grid-container">
        """, unsafe_allow_html=True)

        for item in st.session_state.references:
            st.markdown(f"""    
                <div class="grid-item">
                    <img src='{item["link_image"]}' alt='Thumbnail'>
                    <a href='{item["link_page"]}' target='_blank'>{item["title"]}</a>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        
        if len(load_page_data_references(st.session_state.reference_offset, 1)) > 0:
            if st.button("Xem thêm"):
                new_references = load_page_data_references(st.session_state.reference_offset, limit=9)
                st.session_state.references.extend(new_references)  # Giữ bài cũ + thêm bài mới
                st.session_state.reference_offset += 9 

    def guide_ui(self):
        ctn_guide_ui = st.container()
        with ctn_guide_ui:
            st.markdown("""
                    <style>
                    .guide-container {
                        background-color: #f9f9f9;
                        padding: 25px;
                        border-radius: 12px;
                        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                    }
                    .guide-title {
                        text-align: center;
                        font-size: 24px;
                        font-weight: bold;
                        color: #2c3e50;
                        margin-bottom: 15px;
                    }
                    .guide-section {
                        margin-top: 15px;
                        padding: 15px;
                        border-left: 5px solid #3498db;
                        background-color: #ecf0f1;
                        border-radius: 8px;
                    }
                    .guide-section h4 {
                        color: #2980b9;
                        margin-bottom: 8px;
                    }
                    .guide-section p {
                        color: #2c3e50;
                        font-size: 16px;
                    }
                    .guide-list {
                        padding-left: 20px;
                    }
                    </style>
            
                    <div class='guide-container'>
                    <h3 class='guide-title'>HƯỚNG DẪN SỬ DỤNG</h3>

                    <div class='guide-section'>
                        <h4>1. Dự đoán giá bất động sản</h4>
                        <p>Chọn khu vực bạn quan tâm và nhập các thông tin cần thiết để dự đoán giá bất động sản.</p>
                    </div>
                    
                    <div class='guide-section'>
                        <h4>2. Phân tích dữ liệu bất động sản</h4>
                        <p>Sử dụng công cụ phân tích để xem xu hướng và thông tin chi tiết về thị trường.</p>
                    </div>
                    
                    <div class='guide-section'>
                        <h4>3. So sánh dữ liệu giữa các khu vực</h4>
                        <p>Chọn các khu vực để so sánh sự khác biệt về giá cả, xu hướng và các yếu tố khác.</p>
                    </div>
                    
                    <div class='guide-section'>
                        <h4>4. Gửi email báo cáo bất động sản</h4>
                        <p>Nhập email của bạn để nhận báo cáo chi tiết về thị trường.</p>
                    </div>
                    
                    <div class='guide-section'>
                        <h4>5. Công cụ tính khoản vay</h4>
                        <p>Nhập số tiền vay, thời gian vay, lãi suất để tính toán khoản vay.</p>
                        <p><b>Ví dụ:</b> Nếu vay 2 tỷ VND trong 15 năm với lãi suất 7.5%/năm, số tiền trả hàng tháng sẽ là <b>18,537,000 VND</b>.</p>
                    </div>
                    
                    <div class='guide-section'>
                        <h4>6. Tham khảo & Hướng dẫn</h4>
                        <p>Cung cấp các bài viết về mua bán, đầu tư bất động sản, cùng hướng dẫn chi tiết về ứng dụng.</p>
                    </div>
                    
                    <div class='guide-section'>
                        <h4>7. Liên hệ</h4>
                        <p>Mọi thắc mắc xin gửi email đến <b>support@example.com</b>.</p>
                    </div>
                    
                    <div class='guide-section'>
                        <h4>8. Các bước sử dụng</h4>
                        <ol class='guide-list'>
                            <li>Chọn công cụ tính khoản vay.</li>
                            <li>Nhập thông tin số tiền vay, thời gian vay, lãi suất.</li>
                            <li>Nhấn "Tính toán" để xem kết quả.</li>
                            <li>Đọc các bài viết tham khảo.</li>
                            <li>Xem hướng dẫn chi tiết tại mục "Hướng dẫn".</li>
                        </ol>
                    </div>
                    
                    <div class='guide-section'>
                        <h4>9. Lưu ý</h4>
                        <p>Thông tin chỉ mang tính chất tham khảo. Hãy liên hệ chuyên gia tài chính để được tư vấn cụ thể.</p>
                    </div>
                    </div>
            
            """, unsafe_allow_html=True)

        
class MAIN_RUN():
    def __init__(self):
        self.expand_class = EXPAND_CLASS()
    def sidebar_ui(self):
        container_sidebar_user = st.sidebar.container(key="container_sidebar_expand")
        container_sidebar_user.markdown("<h3 style='text-align: center; padding:0; margin-bottom:5px;'>MỞ RỘNG</h3>", unsafe_allow_html=True)
        # container_sidebar_user.divider()
        with container_sidebar_user:
            selected = option_menu(
                menu_title= None,  # required
                options=["Công cụ tính khoản vay","Tham khảo","Hướng dẫn"],  # required
                icons=["cash-coin","book","question-circle"],  # optional
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
    def run_expand(self):
        option = self.sidebar_ui()
        if option == "Công cụ tính khoản vay":
            self.expand_class.loan_ui()
        elif option == "Tham khảo":
            self.expand_class.ui_info("THAM KHẢO","Team Real Estate")
            self.expand_class.reference_ui()
        elif option == "Hướng dẫn":
            self.expand_class.guide_ui()
main_run_app = MAIN_RUN()
main_run_app.run_expand()
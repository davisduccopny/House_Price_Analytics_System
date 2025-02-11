import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import time
import PROJECTS.config as module_config
import PROJECTS.module_expand as module_expand
import PROJECTS.module_users as module_users
import numpy as np
import plotly.graph_objects as go

with open('src/style/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style/style_expand.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
class EXPAND_CLASS():
    def __init__(self):
        pass
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
            st.title("Tham khảo")
        elif option == "Hướng dẫn":
            st.title("Hướng dẫn")
main_run_app = MAIN_RUN()
main_run_app.run_expand()
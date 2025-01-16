import bcrypt
import streamlit as st
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import PROJECTS.config as config_project
import time
import json
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

# LOAD LOTTIE JSON
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


### PATH THAO TAC VOI DATABASE
def check_user_access(username, input_password, conn, cursor):
    '''Ham kiem tra xem nguoi dung co quyen truy cap hay khong'''
    
    cursor.execute("SELECT password, role,display_name FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    # Nếu tìm thấy user trong cơ sở dữ liệu
    if user:
        stored_password = user[0]  # Lấy mật khẩu đã mã hóa từ CSDL
        stored_role = user[1]
        display_name = user[2]

        # Kiểm tra mật khẩu nhập vào có khớp với mật khẩu đã mã hóa không
        if bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8')):
            return stored_role,display_name  # Mật khẩu đúng
        else:
            return None,None
    else:
        return None,None
def select_info_user(username,cursor):
    cursor.execute("SELECT username,password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    return user
def update_user_by_users(username_state, username,display_name, password, conn, cursor):
    '''Ham cap nhat thong tin nguoi dung boi chinh nguoi dung'''
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute(
        "UPDATE users SET username = %s,display_name = %s, password = %s WHERE username = %s",
        (username,display_name, hashed_password, username_state)
    )
    conn.commit()

    if cursor.rowcount == 0:
        return False  
    return True
def update_user_by_admin(username_state, username,display_name, password, conn, cursor):
    '''Ham cap nhat thong tin nguoi dung boi admin'''
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute(
        "UPDATE users SET username = %s,display_name = %s, password = %s WHERE username = %s",
        (username,display_name, hashed_password, username_state)
    )
    conn.commit()

    if cursor.rowcount == 0:
        return False  
    return True

### PATH THIET KE VA XU LY LOGIN
def login(type_process):
    cols_login_parent = st.columns([1,1])
    container_login = cols_login_parent[0].container(key="container_login")
    with container_login:
        st.markdown("""
                    <h5 style='text-align: center; padding:0;'>IM SCIENCE</h5>
                    <h2 style='text-align: center;'>HOUSE PRICE PREDICTION</h2>""", unsafe_allow_html=True)
        config_project.social_media_show()
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False
        st.session_state.role_access_admin = False
        st.session_state.username_house = None
    background_image_login = config_project.get_relative_file_path("../src/image/background-login-2.jpg")
    icon_login_path = config_project.get_relative_file_path("../src/image/icon-logo.png")
    st.markdown(f"""
            <style>
                [data-testid="stMainBlockContainer"]{{
                width: 100%;
                padding: 3rem 8rem 10rem !important;
                min-width: auto;
                max-width: initial;

                }}
                [data-testid="stSidebar"] {{
                    display: none;
                }}
                .st-key-container_login {{
                    width: 100%;
                    box-shadow: -10px 5px 10px rgba(255, 255, 255, 0.1), 
                    10px 5px 10px rgba(255, 255, 255, 0.1), 
                    0px 10px 10px rgba(255, 255, 255, 0.1);
                    padding: 25px;
                    border-radius: 15px;
                    background: rgba(255, 255, 255, 0.8);
                }}
                .house-price-icon {{
                    display: inline-block;
                    width: 1.65rem;
                    height: 1.65rem;
                    background-image: url('data:image/png;base64,{icon_login_path}');
                    background-size: contain;
                    background-repeat: no-repeat;
                }}
                [data-testid="stHeader"] {{
                    background: rgba(0,0,0,0);
                }}
                [data-testid="stAppViewContainer"] > .stMain {{
                    background-image: url("data:image/jpg;base64,{background_image_login}");
                    background-size: cover;
                    background-position: center center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
            </style>
            """, unsafe_allow_html=True)

    
    if not st.session_state.is_logged_in:
        config_project.create_db_pool()
        if type_process == 'login':
            with container_login.form(key="login_form",enter_to_submit=True, border=False):
                title_placeholder = st.empty()
                title_placeholder.subheader("Đăng nhập")
                username_placeholder = st.empty()
                password_placeholder = st.empty()
                success_placeholder = st.empty()
                username = username_placeholder.text_input("Tên người dùng", placeholder="Enter user name", key="username_login")
                password = password_placeholder.text_input("Mật khẩu", type="password", placeholder="Enter password", key="password_login")
                
                if st.form_submit_button("🔓Đăng nhập",type="primary", help="Nhấn vào để đăng nhập!"):
                    with st.spinner('🔒 Đang kiểm tra thông tin đăng nhập...'): 
                        if (username is not None and password is not None) and (username != '' and password != ''):
                            conn = config_project.connect_to_mysql()
                            cursor = conn.cursor()
                            user_role_house,display_name_house = check_user_access(username,password,conn,cursor)
                            if user_role_house and (user_role_house is not None):
                                st.session_state.is_logged_in = True
                                st.session_state.role_access_admin = user_role_house
                                st.session_state.username_house = username
                                st.session_state.display_name_house = display_name_house
                                del st.session_state.login_request
                                success_placeholder.success("✅ Đăng nhập thành công!")
                                time.sleep(2)  
                                title_placeholder.empty()
                                username_placeholder.empty()
                                password_placeholder.empty()
                                success_placeholder.empty()
                                st.rerun()
                            else:
                                st.error("❌ Tên đăng nhập hoặc mật khẩu không đúng!")
                        else:
                            st.warning("❌ Vui lòng nhập tên đăng nhập và mật khẩu!")
        elif type_process == 'register':
            with container_login.form(key="register_form",enter_to_submit=True, border=False):
                title_placeholder = st.empty()
                title_placeholder.subheader("Đăng ký")
                username_placeholder = st.empty()
                password_placeholder = st.empty()
                display_name_placeholder = st.empty()
                success_placeholder = st.empty()
                username = username_placeholder.text_input("Tên người dùng", placeholder="Enter user name", key="username_register")
                password = password_placeholder.text_input("Mật khẩu", type="password", placeholder="Enter password", key="password_register")
                display_name = display_name_placeholder.text_input("Tên hiển thị", placeholder="Enter display name", key="display_name_register")
               
                cols_register_type_process = st.columns([3,1])
                with cols_register_type_process[0]:
                    if cols_register_type_process[0].form_submit_button("🔓Đăng ký",type="primary", help="Nhấn vào để đăng ký!"):
                        with st.spinner('🔒 Đang kiểm tra thông tin đăng ký...'): 
                            if (username is not None and password is not None) and (username != '' and password != ''):
                                conn = config_project.connect_to_mysql()
                                cursor = conn.cursor()
                                user = select_info_user(username,cursor)
                                if user is None:
                                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                                    cursor.execute(
                                        "INSERT INTO users (username, password, role,display_name) VALUES (%s, %s, %s, %s)",
                                        (username, hashed_password, 'user',display_name)
                                    )
                                    conn.commit()
                                    st.success("✅ Đăng ký thành công!")
                                    time.sleep(2)  
                                    st.session_state.is_logged_in = True
                                    st.session_state.role_access_admin = 'user'
                                    st.session_state.username_house = username
                                    st.session_state.display_name_house = display_name
                                    del st.session_state.register_request
                                    title_placeholder.empty()
                                    username_placeholder.empty()
                                    password_placeholder.empty()
                                    display_name_placeholder.empty()
                                    success_placeholder.empty()
                                    st.rerun()
                                else:
                                    st.error("❌ Tên đăng nhập đã tồn tại!")

    # with cols_login_parent[1]:
    #     st_lottie(load_lottiefile("src/lottie/Animation -login.json"),key="lottie_login") 
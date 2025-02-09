import streamlit as st 
import time
from PROJECTS.module_login import login



st.set_page_config(layout="wide", page_icon='src/image/icon-logo.png', initial_sidebar_state='auto')
st.logo("src/image/logo_2-Photoroom.png",icon_image="src/image/icon-logo.png")
from st_pages import add_page_title, get_nav_from_toml, hide_pages
nav = get_nav_from_toml(".streamlit/pages.toml")
pg = st.navigation(nav)
pg.run()

if st.session_state.login_request:
    if "is_logged_in" not in st.session_state or not st.session_state.is_logged_in:
        login("login")
    else:
        st.toast("##### Bạn đã đăng nhập!",icon="🔒")
if st.session_state.register_request:
    if "is_logged_in" not in st.session_state or not st.session_state.is_logged_in:
        login("register")
    else:
        st.toast("##### Bạn đã đăng nhập!",icon="🔒")


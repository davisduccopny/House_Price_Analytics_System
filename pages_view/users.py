import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import time
import PROJECTS.config as module_config
import PROJECTS.module_expand as module_expand
import PROJECTS.module_users as module_users
from PROJECTS.module_login import login

if not st.session_state.get("is_logged_in", False):
    st.session_state.login_request = True
if "login_request" not in st.session_state:
    st.session_state.login_request = None
if "register_request" not in st.session_state:
    st.session_state.register_request = None
    
with open('src/style/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style/style_users.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


class OTHER_USER():
    def __init__(self):
        pass
    def check_password(self, password):
        if len(password) < 6:
            return False
        has_digit = any(char.isdigit() for char in password)
        has_alpha = any(char.isalpha() for char in password)
        return has_digit and has_alpha
class FRONTEND_UI_DESIGN():
    def __init__(self):
        pass

    def ui_info(self, text,loai_data):
        container_title_manage_expand = st.container(key="container_title_manage_expand")
        with container_title_manage_expand:
            col_title_dmanage_expand = st.columns([5,2])
            col_title_dmanage_expand[0].markdown(f"""<h3 style='text-align: left; padding:0; margin-bottom:5px;'>{text}</h3>
                                            <p style='text-align: left; padding:0'>Cài đặt người dùng <span style="color:#c4c411; font-weight:bolder;"> {loai_data} </span></p>""", unsafe_allow_html=True)
            with col_title_dmanage_expand[1]:
                with st.form(key="search_form", enter_to_submit=True,border=False):
                    cols_search = st.columns([6,1])
                    search_term = cols_search[0].text_input(label=" ",placeholder="Tìm kiếm thông tin", key="search_term",type="default")
                    if cols_search[1].form_submit_button("🔍"):
                        if search_term:
                            return search_term
                        else:
                            st.toast(f"##### Vui lòng nhập thông tin!", icon="⚠️")
                            return None
    def sidebar_ui(self):
        container_sidebar_user = st.sidebar.container(key="container_sidebar_user")
        container_sidebar_user.markdown("<h3 style='text-align: center; padding:0; margin-bottom:5px;'>👨‍💼 NGƯỜI DÙNG</h3>", unsafe_allow_html=True)
        # container_sidebar_user.divider()
        with container_sidebar_user:
            selected = option_menu(
                menu_title= None,  # required
                options=["Mật khẩu","Hiển thị", "Khác"],
                icons=[],  
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

    def change_password_user(self):
        container_change_pass = st.container(key="container_change_pass")
        with container_change_pass:
            cols_permission_pass = st.columns([3,1])
            permission_pass_toggle = cols_permission_pass[0].toggle(
                "Cho phép sửa mật khẩu", key="permission_pass_toggle", value=False
            )
            cols_permission_pass[1].write(f"##### 👋 {MAIN_USER().load_data_for_user()[1]}")
            if permission_pass_toggle:
                disable = False
            else:
                disable = True
            container_form_change_pass = st.container(key="container_form_change_pass")
            with container_form_change_pass:
                with st.form(key="change_pass_form", enter_to_submit=True, border=False, clear_on_submit=True):
                    cols_change_pass = st.columns([6,1])
                    old_pass = cols_change_pass[0].text_input(label="🔑Mật khẩu cũ",placeholder="Nhập mật khẩu cũ", key="old_pass",type="password", disabled=disable)
                    new_pass = cols_change_pass[0].text_input(label="🔑Mật khẩu mới",placeholder="Nhập mật khẩu mới", key="new_pass",type="password", disabled=disable)
                    confirm_pass = cols_change_pass[0].text_input(label="🔑Xác nhận mật khẩu mới",placeholder="Nhập lại mật khẩu mới", key="confirm_pass",type="password", disabled=disable)
                    if st.form_submit_button("Save", icon=":material/save:", type="primary", help="Nhấn vào để lưu thay đổi!", disabled=disable):
                        with st.spinner("🔐 Đang thực hiện thao tác..."):
                            if old_pass and new_pass and confirm_pass:
                                if not OTHER_USER().check_password(new_pass):
                                    st.toast(f"##### Mật khẩu phải có ít nhất 6 ký tự, bao gồm cả chữ và số!", icon="⚠️")
                                    time.sleep(2)
                                    return None
                                else:
                                    if new_pass != confirm_pass:
                                        st.toast(f"##### Mật khẩu mới không khớp!", icon="⚠️")
                                        time.sleep(1)
        
                                    else:
                                        if module_users.change_password(st.session_state.username_house, old_pass, new_pass):
                                            st.toast("##### Đổi mật khẩu thành công!", icon="✅")
                                            time.sleep(1)
                                            st.rerun()
                                        else:
                                            st.toast("##### Mật khẩu cũ không đúng!", icon="❌")
                                            time.sleep(1)
                            else:
                                st.toast(f"##### Vui lòng nhập thông tin!", icon="⚠️")
                                time.sleep(1)

    def display_user_change(self):
        container_change_display = st.container(key="container_change_display")
        with container_change_display:
            cols_permission_display = st.columns([3,1])
            permission_display_toggle = cols_permission_display[0].toggle(
                "Cho phép sửa thông tin", key="permission_display_toggle", value=False
            )
            cols_permission_display[1].write(f"##### 👋 {MAIN_USER().load_data_for_user()[0]}")
            if permission_display_toggle:
                disable = False
            else:
                disable = True
            container_form_change_display = st.container(key="container_form_change_display")
            with container_form_change_display:
                with st.form(key="change_display_form", enter_to_submit=True, border=False, clear_on_submit=False):
                    cols_change_display = st.columns([6,1])
                    display_name = cols_change_display[0].text_input(label="Tên hiển thị", value=MAIN_USER().load_data_for_user()[0],placeholder="Nhập tên hiển thị", key="display_name_user", disabled=disable)
                    if st.form_submit_button("Save", icon=":material/save:", type="primary", help="Nhấn vào để lưu thay đổi!", disabled=disable):
                        with st.spinner("🔐 Đang thực hiện thao tác..."):
                            if display_name:
                                if module_users.change_profile(st.session_state.username_house, display_name):
                                    st.toast("##### Đổi thông tin thành công!", icon="✅")
                                    st.session_state.display_name_house = display_name
                                    time.sleep(1)
                                    module_users.load_data_for_user.clear()
                                    st.rerun()
                                else:
                                    st.toast("##### Mã nhân viên đã tồn tại!", icon="❌")
                                    time.sleep(1)
                            else:
                                st.toast(f"##### Vui lòng nhập thông tin!", icon="⚠️")
                                time.sleep(1)
    def account_delete(self, search_term=None):
        st.info("##### ⚠️ Lưu ý: Hành động này không thể hoàn tác!")
        container_delete_account = st.container(key="container_delete_account")
        with container_delete_account:
            tabs_account_info_action =  st.tabs(["⏲️ Hành động người dùng","🗑️ Xóa tài khoản"])
            with tabs_account_info_action[1]:
                cols_delete_account = st.columns([0.5,2,3])
                with cols_delete_account[1]:
                    st.write("#### ⚠️ Xóa tài khoản 🤔🤔🤔")
                    key_delete_button_delete = st.button("Xóa tài khoản", icon=":material/delete:", key="delete_button_delete", use_container_width=True, help="Nhấn vào để xóa tài khoản của bạn!")
                    if key_delete_button_delete:
                        st.session_state.dialog_open = True
                            
                    if st.session_state.get("dialog_open", False):
                        module_config.show_confirmation_dialog("xóa tài khoản")
                    if "confirmation" in st.session_state:
                        if st.session_state.confirmation == "Yes":
                            with st.spinner("🔐 Đang thực hiện thao tác..."):
                                st.session_state.confirmation = None
                                if module_users.delete_user(st.session_state.username_house):
                                    st.session_state.is_logged_in = False
                                    st.session_state.role_access_admin = False
                                    st.switch_page("main.py")
                                else:
                                    st.toast("##### Xóa tài khoản không thành công!", icon="❌")
                
class MAIN_USER():
    def __init__(self):
        self.frontend = FRONTEND_UI_DESIGN()
    def user(self):
        
        selected = self.frontend.sidebar_ui()
        if selected == "Mật khẩu":
            self.frontend.ui_info("👨‍💼 MẬT KHẨU","thay đổi mật khẩu")
            self.frontend.change_password_user()
        elif selected == "Hiển thị":
            self.frontend.ui_info("👨‍💼 HIỂN THỊ","thay đổi hiển thị")
            self.frontend.display_user_change()
        elif selected == "Khác":
            search_tearm = self.frontend.ui_info("👨‍💼 KHÁC","- hành động - xóa")
            self.frontend.account_delete(search_tearm)
    def load_data_for_user(self):
        diplay_name = data_user[data_user["username"] == st.session_state.username_house]["display_name"].values[0]
        role = data_user[data_user["username"] == st.session_state.username_house]["role"].values[0]
        return diplay_name,role
    
if (st.session_state.login_request == False and st.session_state.register_request == False) or (st.session_state.login_request is None and st.session_state.register_request is None): 
    data_user = module_users.load_data_for_user(st.session_state.username_house)
        
    main_user = MAIN_USER()
    main_user.user()
    module_config.add_sidebar_footer()
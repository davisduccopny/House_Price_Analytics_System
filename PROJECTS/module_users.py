import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import pooling, Error
from mysql.connector import OperationalError, InternalError
import PROJECTS.config as module_config
import bcrypt

@st.cache_data
def load_data_for_user(username):
    conn = module_config.connect_to_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, display_name,region_use,send_mail FROM users WHERE username = %s;", (username,))
        users = cursor.fetchall()
        users = pd.DataFrame(users, columns=["id", "username", "role", "display_name","region_use","send_mail"])
        if users.empty:
            return False
        return users
    finally:
        conn.close()
def change_password(username, old_pass, new_pass):
    conn = module_config.connect_to_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s;", (username,))
        result = cursor.fetchone()
        if result is None:
            return False
        
        stored_password = result[0]
        if not bcrypt.checkpw(old_pass.encode('utf-8'), stored_password.encode('utf-8')):
            return False
        
        hashed_new_pass = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("UPDATE users SET password = %s WHERE username = %s;", (hashed_new_pass, username))
        conn.commit()
        return True
    except (OperationalError, InternalError, Error) as e:
        st.error(f"Error: {e}")
        return False
    finally:
        conn.close()
def change_profile(username, display_name,region_use,send_mail_status):
    conn = module_config.connect_to_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET display_name = %s,region_use = %s,send_mail = %s WHERE username = %s;", (display_name,region_use,send_mail_status, username))
        conn.commit()
        return True
    except (OperationalError, InternalError, Error) as e:
        st.error(f"Error: {e}")
        return False
    finally:
        conn.close()
def delete_user(username):
    conn = module_config.connect_to_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s;", (username,))
        conn.commit()
        return True
    except (OperationalError, InternalError, Error) as e:
        st.error(f"Error: {e}")
        return False
    finally:
        conn.close()
        

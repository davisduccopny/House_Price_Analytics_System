import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import pooling, Error
from mysql.connector import OperationalError, InternalError
import PROJECTS.config as module_config

@st.cache_data
def load_page_data_references(offset,limit=9):
    module_config.create_db_pool()
    conn = module_config.connect_to_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, link_page, link_image FROM references_page LIMIT %s OFFSET %s", (limit, offset))
    data = cursor.fetchall()
    conn.close()
    return data


import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "data/nifty100.db"

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

@st.cache_data
def load_table(table_name):
    conn = get_connection()
    return pd.read_sql(f"SELECT * FROM {table_name}", conn)
import streamlit as st
import sqlite3
import pandas as pd
import requests
import json

st.title("MIC API Test")

DATABASE = "api_test.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            model_name TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            success INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def load():
    conn = sqlite3.connect(DATABASE)
    data = pd.read_sql_query("SELECT name, model_name, 1 as Success FROM data", conn)
    data = data.set_index("name")
    conn.close()
    return data

def add_data(name, model_name, endpoint, request):
    conn = sqlite3.connect(DATABASE)

    response = requests.post(endpoint, json=request)
    data = pd.read_sql_query("SELECT name FROM data", conn)
    if data["name"].values and name in data["name"].values[0]:
        st.error("Name already exists", icon="🚨")
        return True
    print(response.status_code)
    if response.status_code == 200:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO data (name, model_name, endpoint, success)
            VALUES (?, ?, ?, ?)
        ''', (name, model_name, endpoint, 1))
        conn.commit()
        conn.close()
        return True
    else:
        return False

if __name__ == "__main__":
    init_db()

    col1, col2 = st.columns(2)

    with col1:
        with st.form("API Tester"):
            name = st.text_input("Name")
            model_name = st.text_input("Model Name")
            endpoint = st.text_input("Endpoint URL")
            request = st.text_area("JSON Request")
            submit = st.form_submit_button("Submit")
            
            if submit:
                try:
                    request_data = json.loads(request)
                    print(request_data)
                    if add_data(name, model_name, endpoint, request_data):
                        st.success("Success!", icon="✅")
                    else:
                        st.error("Failed to get OK response from endpoint", icon="🚨")
                except json.JSONDecodeError:
                    st.error("Invalid JSON format", icon="🚨")

    with col2:
        st.dataframe(
            load(),
            column_config={
                "name": "Name",
                "model_name": "Model Name",
                "Success": st.column_config.NumberColumn(
                    format="✅",
                ),
            },
            use_container_width=True,
        )
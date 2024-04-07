import streamlit as st
import requests
import pandas as pd

st.title("MIC API Test")


DATA_GET_URL = "http://127.0.0.1:8080/get"
DATA_ADD_URL = "http://127.0.0.1:8080/add"


def load():
    r = requests.post(DATA_GET_URL)
    data = pd.read_json(r.text)
    data = data.drop(columns=["id", "endpoint"])
    titles = ["name", "model_name"]
    data = data.reindex(columns=titles)
    data["Success"] = 1
    data = data.set_index("name")
    return data


if __name__ == "__main__":

    col1, col2 = st.columns(2)

    with col1:
        with st.form("API Tester"):
            name = st.text_input("Name")
            model_name = st.text_input("Model Name")
            endpoint = st.text_input("Endpoint URL")
            request = st.text_area("JSON Request")
            submit = st.form_submit_button("Submit")

            if submit:
                response = requests.post(
                    DATA_ADD_URL,
                    json={
                        "name": name,
                        "model_name": model_name,
                        "endpoint": endpoint,
                        "request": request,
                    },
                )

                if response.json()["success"] == 1:
                    st.success("This is a success message!", icon="✅")
                else:
                    st.error("This is an error", icon="🚨")
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

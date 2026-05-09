import streamlit as st
from google.oauth2.service_account import Credentials

try:

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=scope
    )

    st.success("Credentials berhasil dibaca!")

except Exception as e:

    st.error(e)

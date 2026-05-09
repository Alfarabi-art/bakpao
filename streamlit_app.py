import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

try:

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    st.success("Secrets berhasil dibaca")

    client = gspread.authorize(creds)

    st.success("Google Auth berhasil")

except Exception as e:

    st.error(e)

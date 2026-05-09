import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

st.success("Google Auth berhasil")

try:

    spreadsheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/157PtqTU5MmkF5Zf1KiPPsIBwvomXOoyVieifrYaz6M4/edit#gid=0"
    )

    st.success("Spreadsheet berhasil dibuka")

    worksheet = spreadsheet.worksheet("Data")

    st.success("Worksheet Data berhasil dibuka")

except Exception as e:

    st.error(e)

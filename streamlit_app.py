import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import gspread
from google.oauth2.service_account import Credentials

# =========================================
# CONFIG
# =========================================
st.set_page_config(
    page_title="Distributor Bakpao",
    page_icon="🥟",
    layout="wide"
)

# =========================================
# GOOGLE SHEETS CONNECT
# =========================================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

spreadsheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/157PtqTU5MmkF5Zf1KiPPsIBwvomXOoyVieifrYaz6M4/edit#gid=0"
)

sheet = spreadsheet.worksheet("Data")

# =========================================
# VIDEO BACKGROUND
# =========================================
VIDEO_URL = "https://raw.githubusercontent.com/Alfarabi-art/bakpao/main/bg.mp4"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: transparent;
    }}

    video {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        object-fit: cover;
        z-index: -100;
    }}

    .main {{
        background: rgba(0,0,0,0.45);
        border-radius: 20px;
        padding: 20px;
    }}

    h1,h2,h3,h4,p,label,div {{
        color: white !important;
    }}

    .stButton>button {{
        width: 100%;
        border-radius: 12px;
        background-color: orange;
        color: white;
        border: none;
        font-weight: bold;
    }}

    .stDownloadButton>button {{
        width: 100%;
        border-radius: 12px;
        background-color: green;
        color: white;
        border: none;
        font-weight: bold;
    }}

    .css-1d391kg {{
        background-color: rgba(0,0,0,0);
    }}

    .block-container {{
        padding-top: 2rem;
    }}

    </style>

    <video autoplay muted loop>
        <source src="{VIDEO_URL}" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)

# =========================================
# DATA PRODUK
# =========================================
produk_data = {
    "Bakpao Coklat": {
        "harga": 5000,
        "gambar": "https://images.unsplash.com/photo-1504674900247-0877df9cc836"
    },
    "Bakpao Ayam": {
        "harga": 7000,
        "gambar": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
    },
    "Bakpao Keju": {
        "harga": 8000,
        "gambar": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601"
    },
    "Bakpao Kacang Hijau": {
        "harga": 6000,
        "gambar": "https://images.unsplash.com/photo-1490645935967-10de6ba17061"
    }
}

# =========================================
# TITLE
# =========================================
st.title("🥟 Distributor Bakpao")

# =========================================
# INPUT NAMA
# =========================================
nama = st.text_input("Nama Pembeli")

# =========================================
# PILIH PRODUK
# =========================================
st.subheader("🛒 Pilih Produk")

cart = []
total_qty = 0
total_omzet = 0

for produk, info in produk_data.items():

    col1, col2 = st.columns([2, 1])

    with col1:
        st.image(info["gambar"], use_container_width=True)

    with col2:
        st.markdown(f"## {produk}")
        st.markdown(f"### Rp {info['harga']:,}")

        qty = st.number_input(
            f"Qty {produk}",
            min_value=0,
            step=1,
            key=produk
        )

        if qty > 0:
            subtotal = qty * info["harga"]

            cart.append(
                f"{produk} ({qty} pcs)"
            )

            total_qty += qty
            total_omzet += subtotal

            st.success(f"Subtotal: Rp {subtotal:,}")

# =========================================
# TOTAL
# =========================================
st.markdown("---")

st.subheader("💰 Ringkasan")

st.write(f"Total Qty : {total_qty}")
st.write(f"Total Omzet : Rp {total_omzet:,}")

status = st.selectbox(
    "Status Pembayaran",
    ["Belum Bayar", "Sudah Bayar"]
)

# =========================================
# SIMPAN
# =========================================
if st.button("💾 Simpan Data"):

    if nama == "":
        st.warning("Masukkan nama pembeli")
    elif total_qty == 0:
        st.warning("Pilih produk dulu")
    else:

        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        produk_text = ", ".join(cart)

        sheet.append_row([
            waktu,
            nama,
            produk_text,
            total_qty,
            total_omzet,
            status
        ])

        st.success("Data berhasil disimpan!")

# =========================================
# AMBIL DATA DARI GOOGLE SHEETS
# =========================================
data = sheet.get_all_records()

df = pd.DataFrame(data)

# =========================================
# RIWAYAT
# =========================================
st.markdown("---")

st.subheader("📋 Riwayat Distribusi")

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True
    )

    # DOWNLOAD CSV
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "⬇ Download CSV",
        csv,
        "distributor_bakpao.csv",
        "text/csv"
    )

    # =========================================
    # UPDATE STATUS
    # =========================================
    st.markdown("---")
    st.subheader("💳 Update Status Pembayaran")

    pilihan = st.selectbox(
        "Pilih Data",
        df.index
    )

    current_status = df.loc[pilihan, "Status"]

    st.write(f"Status sekarang: {current_status}")

    new_status = st.selectbox(
        "Ubah Status",
        ["Belum Bayar", "Sudah Bayar"]
    )

    if st.button("✅ Update Status"):

        row_number = pilihan + 2

        sheet.update_cell(
            row_number,
            6,
            new_status
        )

        st.success("Status berhasil diupdate!")
        st.rerun()

else:
    st.info("Belum ada data")

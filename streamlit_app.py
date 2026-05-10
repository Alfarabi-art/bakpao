import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import gspread
from google.oauth2.service_account import Credentials

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Bakpao Ceu Mumun",
    page_icon="🥟",
    layout="wide"
)

# =====================================================
# VIDEO BACKGROUND
# =====================================================

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
        z-index: -2;
    }}

    .overlay {{
        position: fixed;
        top:0;
        left:0;
        width:100%;
        height:100%;
        background: rgba(0,0,0,0.55);
        z-index:-1;
    }}

    .block-container {{
        padding-top: 2rem;
    }}

    /* INPUT */
    .stTextInput input {{
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        border-radius: 15px;
    }}

    .stSelectbox div[data-baseweb="select"] {{
        background: rgba(255,255,255,0.15);
        border-radius: 15px;
    }}

    /* BUTTON */
    .stButton>button {{
        width: 100%;
        border-radius: 15px;
        border: none;
        background: rgba(255,255,255,0.15);
        color: white;
        backdrop-filter: blur(10px);
        padding: 12px;
        font-weight: bold;
    }}

    .stDownloadButton>button {{
        width: 100%;
        border-radius: 15px;
        border: none;
        background: rgba(255,255,255,0.15);
        color: white;
        backdrop-filter: blur(10px);
        padding: 12px;
        font-weight: bold;
    }}

    /* METRIC CARD */
    .glass {{
        background: rgba(255,255,255,0.12);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        color: white;
    }}

    /* TABLE */
    table {{
        text-align: center !important;
    }}

    th {{
        text-align: center !important;
    }}

    td {{
        text-align: center !important;
    }}

    </style>

    <video autoplay muted loop>
        <source src="{VIDEO_URL}" type="video/mp4">
    </video>

    <div class="overlay"></div>

    """,
    unsafe_allow_html=True
)

# =====================================================
# GOOGLE SHEETS
# =====================================================

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

# =====================================================
# AMBIL DATA
# =====================================================

data = sheet.get_all_records()

df = pd.DataFrame(data)

if df.empty:
    df = pd.DataFrame(columns=[
        "Tanggal",
        "Nama",
        "Produk",
        "Total Qty",
        "Total Omzet",
        "Status"
    ])

# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <h1 style='color:white; font-size:60px;'>
    🥟 Bakpao Ceu Mumun
    </h1>

    <h3 style='color:white;'>
    Sistem Distribusi & Pendapatan UMKM
    </h3>
    """,
    unsafe_allow_html=True
)

# =====================================================
# HITUNG DASHBOARD
# =====================================================

total_omzet = df["Total Omzet"].sum() if not df.empty else 0
total_qty = df["Total Qty"].sum() if not df.empty else 0
total_transaksi = len(df)

belum_bayar = 0

if not df.empty:
    belum_bayar = df[df["Status"] == "Belum Bayar"]["Total Omzet"].sum()

# =====================================================
# DASHBOARD GLASSMORPHISM
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="glass">
        <h4>💰 Total Omzet</h4>
        <h1>Rp {total_omzet:,}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="glass">
        <h4>📦 Produk Keluar</h4>
        <h1>{total_qty} pcs</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="glass">
        <h4>🧾 Total Transaksi</h4>
        <h1>{total_transaksi}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="glass">
        <h4>💳 Belum Dibayar</h4>
        <h1>Rp {belum_bayar:,}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")
st.write("")

# =====================================================
# INPUT DATA
# =====================================================

st.markdown(
    """
    <h1 style='color:white;'>
    📋 Input Data Pembeli
    </h1>
    """,
    unsafe_allow_html=True
)

nama = st.text_input("Nama Pembeli")

produk_list = {
    "Bakpao Coklat": 5000,
    "Bakpao Ayam": 6000,
    "Bakpao Keju": 7000,
    "Bakpao Kacang Hijau": 5000
}

selected_produk = []

total_qty_input = 0
total_harga = 0

st.write("### Pilih Produk")

for produk, harga in produk_list.items():

    qty = st.number_input(
        f"{produk} - Rp {harga}",
        min_value=0,
        step=1,
        key=produk
    )

    if qty > 0:
        selected_produk.append(f"{produk} ({qty} pcs)")
        total_qty_input += qty
        total_harga += qty * harga

status = st.selectbox(
    "Status Pembayaran",
    ["Belum Bayar", "Sudah Bayar"]
)

# =====================================================
# SIMPAN DATA
# =====================================================

if st.button("💾 Simpan Data"):

    if nama == "":
        st.warning("Nama wajib diisi")

    elif total_qty_input == 0:
        st.warning("Pilih minimal 1 produk")

    else:

        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        produk_text = ", ".join(selected_produk)

        new_data = [
            waktu,
            nama,
            produk_text,
            total_qty_input,
            total_harga,
            status
        ]

        sheet.append_row(new_data)

        st.success("Data berhasil disimpan")

        st.rerun()

# =====================================================
# RIWAYAT
# =====================================================

st.write("")
st.write("")

st.markdown(
    """
    <h1 style='color:white;'>
    📊 Riwayat Distribusi
    </h1>
    """,
    unsafe_allow_html=True
)

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Belum ada data")

# =====================================================
# UBAH STATUS
# =====================================================

st.write("")
st.markdown(
    """
    <h2 style='color:white;'>
    💳 Update Status Pembayaran
    </h2>
    """,
    unsafe_allow_html=True
)

if not df.empty:

    pilihan = []

    for i, row in df.iterrows():
        pilihan.append(
            f"{i+2} - {row['Nama']} - {row['Status']}"
        )

    selected = st.selectbox(
        "Pilih Data",
        pilihan
    )

    status_baru = st.selectbox(
        "Ubah Status",
        ["Sudah Bayar", "Belum Bayar"]
    )

    if st.button("✅ Update Status"):

        row_index = pilihan.index(selected) + 2

        sheet.update_cell(row_index, 6, status_baru)

        st.success("Status berhasil diupdate")

        st.rerun()

# =====================================================
# DOWNLOAD CSV
# =====================================================

csv = df.to_csv(index=False).encode('utf-8')

st.write("")

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name='distributor_bakpao.csv',
    mime='text/csv',
    use_container_width=True
)

# =====================================================
# RESET DATA
# =====================================================

st.write("")
st.markdown(
    """
    <h2 style='color:white;'>
    🗑 Reset Semua Data
    </h2>
    """,
    unsafe_allow_html=True
)

if st.button("Hapus Semua Data", use_container_width=True):

    sheet.resize(rows=1)

    st.success("Semua data berhasil dihapus")

    st.rerun()

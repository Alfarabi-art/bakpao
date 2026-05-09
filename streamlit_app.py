import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# =========================================
# PAGE CONFIG
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
        background: rgba(0,0,0,0);
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    h1, h2, h3, h4, h5, h6, p, label {{
        color: white !important;
    }}

    .glass {{
        background: rgba(255,255,255,0.12);
        border-radius: 25px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 20px;
    }}

    .produk-card {{
        background: rgba(255,255,255,0.12);
        padding: 15px;
        border-radius: 25px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 20px;
    }}

    .stButton>button {{
        width: 100%;
        border-radius: 15px;
        border: none;
        background: linear-gradient(45deg,#ff9800,#ff5722);
        color: white;
        font-weight: bold;
        height: 3em;
    }}

    .stDownloadButton>button {{
        width: 100%;
        border-radius: 15px;
        border: none;
        background: linear-gradient(45deg,#4caf50,#2e7d32);
        color: white;
        font-weight: bold;
        height: 3em;
    }}

    div[data-baseweb="select"] > div {{
        background-color: rgba(255,255,255,0.15);
        color: white;
        border-radius: 15px;
    }}

    input {{
        background-color: rgba(255,255,255,0.15) !important;
        color: white !important;
        border-radius: 15px !important;
    }}

    @media (max-width: 768px) {{

        .block-container {{
            padding: 1rem;
        }}

        h1 {{
            font-size: 30px !important;
        }}

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
st.markdown("""
<div class="glass">
<h1>🥟 Distributor Bakpao</h1>
<p>Aplikasi Distributor Modern</p>
</div>
""", unsafe_allow_html=True)

# =========================================
# NAMA
# =========================================
nama = st.text_input("👤 Nama Pembeli")

# =========================================
# PRODUK
# =========================================
st.markdown("""
<div class="glass">
<h2>🛒 Pilih Produk</h2>
</div>
""", unsafe_allow_html=True)

cart = []
total_qty = 0
total_omzet = 0

for produk, info in produk_data.items():

    st.markdown('<div class="produk-card">', unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.image(
            info["gambar"],
            use_container_width=True
        )

    with col2:

        st.markdown(f"### {produk}")
        st.markdown(f"## Rp {info['harga']:,}")

        qty = st.number_input(
            f"Qty {produk}",
            min_value=0,
            step=1,
            key=produk
        )

        subtotal = qty * info["harga"]

        if qty > 0:

            cart.append(
                f"{produk} ({qty} pcs)"
            )

            total_qty += qty
            total_omzet += subtotal

            st.success(f"Subtotal Rp {subtotal:,}")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# TOTAL
# =========================================
st.markdown("""
<div class="glass">
<h2>💰 Ringkasan</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Qty", total_qty)

with col2:
    st.metric("Total Omzet", f"Rp {total_omzet:,}")

status = st.selectbox(
    "💳 Status Pembayaran",
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

        st.success("✅ Data berhasil disimpan!")

# =========================================
# RIWAYAT
# =========================================
st.markdown("""
<div class="glass">
<h2>📋 Riwayat Distribusi</h2>
</div>
""", unsafe_allow_html=True)

data = sheet.get_all_records()

df = pd.DataFrame(data)

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        file_name="distributor_bakpao.csv",
        mime="text/csv"
    )

    # =========================================
    # UPDATE STATUS
    # =========================================
    st.markdown("""
    <div class="glass">
    <h2>💳 Update Status Pembayaran</h2>
    </div>
    """, unsafe_allow_html=True)

    pilihan = st.selectbox(
        "Pilih Data",
        df.index
    )

    st.write(
        "Status Sekarang:",
        df.loc[pilihan, "Status"]
    )

    new_status = st.selectbox(
        "Ubah Menjadi",
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

import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from reportlab.lib.pagesizes import letter
from io import BytesIO

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Bakpao Ceu Mumun",
    page_icon="🥟",
    layout="wide"
)

# =====================================================
# GOOGLE SHEETS CONNECT
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
# VIDEO BACKGROUND
# =====================================================

VIDEO_URL = "https://raw.githubusercontent.com/Alfarabi-art/bakpao/main/bg.mp4"

# =====================================================
# CSS
# =====================================================

st.markdown(f"""
<style>

[data-testid="stHeader"] {{
    background: transparent;
}}

.stApp {{
    background: transparent;
}}

video {{
    position: fixed;
    top: 0;
    left: 0;
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
    background: rgba(0,0,0,0.65);
    z-index:-1;
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
}}

h1,h2,h3,h4,h5,h6,p,label,span {{
    color:white !important;
}}

.product-box {{
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}}

.metric-card {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 25px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: 0.3s;
}}

.metric-card:hover {{
    transform: translateY(-5px);
    background: rgba(255,255,255,0.12);
}}

.metric-title {{
    font-size: 18px;
    color: white;
    margin-bottom: 10px;
    font-weight: 500;
}}

.metric-value {{
    font-size: 42px;
    font-weight: bold;
    color: white;
}}

.stButton button {{
    width:100%;
    background:#ff4b4b;
    color:white;
    border:none;
    border-radius:15px;
    padding:14px;
    font-size:17px;
    font-weight:bold;
}}

.stButton button:hover {{
    background:#ff2e2e;
}}

[data-testid="stDownloadButton"] button {{
    width:100%;
    background:#00c853 !important;
    color:white !important;
    border:none !important;
    border-radius:15px !important;
    padding:14px !important;
    font-size:17px !important;
    font-weight:bold !important;
}}

[data-testid="stDownloadButton"] button:hover {{
    background:#00b248 !important;
}}

section[data-testid="stSidebar"] {{
    background: rgba(0,0,0,0.4);
    backdrop-filter: blur(10px);
}}

@media(max-width:768px) {{

    .block-container {{
        padding-left: 15px;
        padding-right: 15px;
    }}

    h1 {{
        font-size: 34px !important;
    }}

    .metric-value {{
        font-size: 28px;
    }}

}}

</style>

<video autoplay muted loop playsinline>
    <source src="{VIDEO_URL}" type="video/mp4">
</video>

<div class="overlay"></div>

""", unsafe_allow_html=True)

# =====================================================
# DATA PRODUK
# =====================================================

produk_data = {

    "Bakpao Coklat": {
        "harga": 5000,
        "gambar": "images/cokelat.jpg"
    },

    "Bakpao Ayam": {
        "harga": 7000,
        "gambar": "images/ayam.jpg"
    },

    "Bakpao Kacang": {
        "harga": 5000,
        "gambar": "images/kacang.jpg"
    },

    "Bakpao Kentang": {
        "harga": 5000,
        "gambar": "images/kentang.jpg"
    },

    "Bakpao Unti Kelapa": {
        "harga": 5000,
        "gambar": "images/kelapa.jpg"
    }

}

# =====================================================
# AMBIL DATA SPREADSHEET
# =====================================================

data_sheet = sheet.get_all_records()

if len(data_sheet) > 0:
    df_sheet = pd.DataFrame(data_sheet)
else:
    df_sheet = pd.DataFrame(columns=[
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

st.title("🥟 Bakpao Ceu Mumun")
st.subheader("Sistem Distribusi & Pendapatan UMKM")

# =====================================================
# DASHBOARD
# =====================================================

total_omzet = df_sheet["Total Omzet"].sum() if not df_sheet.empty else 0

total_produk = df_sheet["Total Qty"].sum() if not df_sheet.empty else 0

total_transaksi = len(df_sheet)

belum_bayar = df_sheet[
    df_sheet["Status"] == "Belum Bayar"
]["Total Omzet"].sum() if not df_sheet.empty else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">💰 Total Omzet</div>
        <div class="metric-value">Rp {total_omzet:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📦 Produk Keluar</div>
        <div class="metric-value">{total_produk} pcs</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🧾 Total Transaksi</div>
        <div class="metric-value">{total_transaksi}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">💳 Belum Dibayar</div>
        <div class="metric-value">Rp {belum_bayar:,}</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# INPUT
# =====================================================

st.write("")
st.markdown("## 📋 Input Data Pembeli")

nama = st.text_input("Nama Pembeli")

status = st.selectbox(
    "Status Pembayaran",
    ["Belum Bayar", "Sudah Bayar"]
)

# =====================================================
# PRODUK
# =====================================================

st.write("")
st.markdown("## 🛒 Pilih Produk")

produk_terpilih = []

for nama_produk, data in produk_data.items():

    st.markdown(
        '<div class="product-box">',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2,1])

    with col1:

        st.image(
            data["gambar"],
            use_container_width=True
        )

    with col2:

        st.markdown(f"""
        <h3>{nama_produk}</h3>
        <h2 style="color:#ffcc66;">
            Rp {data['harga']:,}
        </h2>
        """, unsafe_allow_html=True)

        qty = st.number_input(
            f"Qty {nama_produk}",
            min_value=0,
            step=1,
            key=nama_produk
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    if qty > 0:

        total_jual = qty * data["harga"]

        produk_terpilih.append({

            "Produk": nama_produk,
            "Qty": qty,
            "Total Jual": total_jual

        })

# =====================================================
# TOTAL
# =====================================================

grand_qty = sum(
    x["Qty"]
    for x in produk_terpilih
)

grand_jual = sum(
    x["Total Jual"]
    for x in produk_terpilih
)

# =====================================================
# RINGKASAN
# =====================================================

st.write("")
st.markdown("## 🧾 Ringkasan")

col1, col2 = st.columns(2)

with col1:
    st.success(
        f"Total Produk: {grand_qty} pcs"
    )

with col2:
    st.info(
        f"Total Omzet: Rp {grand_jual:,}"
    )

# =====================================================
# SIMPAN
# =====================================================

if st.button("💾 Simpan Data Pembeli"):

    if nama == "":
        st.warning("Masukkan nama pembeli")

    elif len(produk_terpilih) == 0:
        st.warning("Pilih minimal 1 produk")

    else:

        daftar_produk = []

        for item in produk_terpilih:

            daftar_produk.append(
                f"{item['Produk']} ({item['Qty']} pcs)"
            )

        gabungan_produk = "\n".join(
            daftar_produk
        )

        waktu = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        # SIMPAN KE GOOGLE SHEETS
        sheet.append_row([
            waktu,
            nama,
            gabungan_produk,
            grand_qty,
            grand_jual,
            status
        ])

        # FORMAT SHEET
        last_row = len(sheet.get_all_values())

        sheet.format(
            f"A{last_row}:F{last_row}",
            {
                "wrapStrategy": "WRAP",
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE"
            }
        )

        st.success(
            "Distribusi berhasil disimpan"
        )

        st.rerun()

# =====================================================
# RIWAYAT
# =====================================================

st.write("")
st.markdown("## 📊 Riwayat Penjualan")

if df_sheet.empty:

    st.info("Belum ada data distribusi")

else:

    st.dataframe(
        df_sheet,
        use_container_width=True,
        height=400
    )

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    st.write("")
    st.markdown("## ✅ Update Status Pembayaran")

    for i, row in df_sheet.iterrows():

        col1, col2, col3, col4 = st.columns([3,3,2,2])

        with col1:
            st.write(f"👤 {row['Nama']}")

        with col2:
            st.write(f"💰 Rp {row['Total Omzet']:,}")

        with col3:
            st.write(row["Status"])

        with col4:

            if row["Status"] == "Belum Bayar":

                if st.button(
                    f"Tandai Lunas #{i}",
                    key=f"lunas_{i}"
                ):

                    sheet.update_cell(
                        i + 2,
                        6,
                        "Sudah Bayar"
                    )

                    st.success("Status berhasil diubah")
                    st.rerun()

            else:

                st.success("Lunas")

    # =====================================================
    # DOWNLOAD CSV
    # =====================================================

    csv = df_sheet.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="laporan_penjualan.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # =====================================================
    # RESET DATA
    # =====================================================

    st.write("")
    st.markdown("## 🗑 Reset Semua Data")

    if st.button(
        "Hapus Semua Data",
        use_container_width=True
    ):

        # SISAKAN HEADER SAJA
        headers = [
            "Tanggal",
            "Nama",
            "Produk",
            "Total Qty",
            "Total Omzet",
            "Status"
        ]

        # HAPUS SEMUA DATA
        sheet.clear()

        # KEMBALIKAN HEADER
        sheet.append_row(headers)

        st.success("Semua data berhasil dihapus")

        st.rerun()

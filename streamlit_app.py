import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Distributor Bakpau",
    page_icon="🥟",
    layout="wide"
)

# =====================================================
# GOOGLE SHEETS
# =====================================================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open("Distributor Bakpau").worksheet("Data")

# =====================================================
# VIDEO BACKGROUND
# =====================================================

VIDEO_URL = "https://raw.githubusercontent.com/Alfarabi-art/bakpau/main/bg.mp4"

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

.invoice-box {{
    background: white;
    padding: 30px;
    border-radius: 20px;
    color: black !important;
}}

.invoice-box h1,
.invoice-box h2,
.invoice-box h3,
.invoice-box p {{
    color: black !important;
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

@media(max-width:768px) {{

    .block-container {{
        padding-left: 15px;
        padding-right: 15px;
    }}

    h1 {{
        font-size: 34px !important;
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

    "Bakpau Coklat": {
        "harga": 5000,
        "gambar": "https://images.unsplash.com/photo-1512058564366-18510be2db19?q=80&w=1200"
    },

    "Bakpau Ayam": {
        "harga": 7000,
        "gambar": "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?q=80&w=1200"
    },

    "Bakpau Kacang Hijau": {
        "harga": 6000,
        "gambar": "https://images.unsplash.com/photo-1526318896980-cf78c088247c?q=80&w=1200"
    },

    "Bakpau Keju": {
        "harga": 8000,
        "gambar": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?q=80&w=1200"
    }

}

# =====================================================
# AMBIL DATA SHEET
# =====================================================

records = sheet.get_all_records()

df = pd.DataFrame(records)

# =====================================================
# HEADER
# =====================================================

st.title("🥟 Distributor Bakpau")
st.subheader("Sistem Distribusi & Pendapatan UMKM")

# =====================================================
# DASHBOARD
# =====================================================

if not df.empty:

    total_omzet = df["Total Omzet"].sum()
    total_produk = df["Total Qty"].sum()
    total_transaksi = len(df)

else:

    total_omzet = 0
    total_produk = 0
    total_transaksi = 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Total Omzet",
        f"Rp {total_omzet:,}"
    )

with col2:
    st.metric(
        "📦 Produk Keluar",
        f"{total_produk} pcs"
    )

with col3:
    st.metric(
        "🧾 Total Transaksi",
        total_transaksi
    )

# =====================================================
# INPUT
# =====================================================

st.write("")
st.markdown("## 📋 Input Distribusi")

nama = st.text_input(
    "Nama Reseller"
)

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
            "Total": total_jual

        })

# =====================================================
# TOTAL
# =====================================================

grand_qty = sum(
    x["Qty"]
    for x in produk_terpilih
)

grand_total = sum(
    x["Total"]
    for x in produk_terpilih
)

st.write("")

col1, col2 = st.columns(2)

with col1:
    st.success(
        f"📦 Total Produk: {grand_qty} pcs"
    )

with col2:
    st.info(
        f"💰 Total Omzet: Rp {grand_total:,}"
    )

# =====================================================
# SIMPAN
# =====================================================

if st.button("💾 Simpan Distribusi"):

    if nama == "":
        st.warning("Masukkan nama reseller")

    elif len(produk_terpilih) == 0:
        st.warning("Pilih minimal 1 produk")

    else:

        daftar_produk = []

        for item in produk_terpilih:

            daftar_produk.append(
                f"{item['Produk']} ({item['Qty']} pcs)"
            )

        gabungan_produk = ", ".join(
            daftar_produk
        )

        tanggal = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        sheet.append_row([

            tanggal,
            nama,
            gabungan_produk,
            grand_qty,
            grand_total,
            status

        ])

        st.success(
            "Data berhasil disimpan ke Google Spreadsheet"
        )

        st.rerun()

# =====================================================
# RIWAYAT
# =====================================================

st.write("")
st.markdown("## 📊 Riwayat Distribusi")

if df.empty:

    st.info("Belum ada data distribusi")

else:

    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )

    # =================================================
    # UPDATE STATUS
    # =================================================

    st.write("")
    st.markdown("## ✅ Update Status Pembayaran")

    for i in range(len(df)):

        col1, col2, col3, col4 = st.columns([3,3,2,2])

        with col1:
            st.write(f"👤 {df.iloc[i]['Nama']}")

        with col2:
            st.write(f"💰 Rp {df.iloc[i]['Total Omzet']:,}")

        with col3:
            st.write(df.iloc[i]["Status"])

        with col4:

            if df.iloc[i]["Status"] == "Belum Bayar":

                if st.button(
                    f"Tandai Lunas #{i}",
                    key=f"lunas_{i}"
                ):

                    row_number = i + 2

                    sheet.update_cell(
                        row_number,
                        6,
                        "Sudah Bayar"
                    )

                    st.rerun()

            else:

                st.success("Lunas")

    # =================================================
    # DOWNLOAD CSV
    # =================================================

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="laporan_distributor.csv",
        mime="text/csv",
        use_container_width=True
    )

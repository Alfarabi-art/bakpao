import streamlit as st
import pandas as pd
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
# VIDEO BACKGROUND
# =====================================================

VIDEO_URL = "https://raw.githubusercontent.com/Alfarabi-art/bakpao/main/bg.mp4"

# =====================================================
# CSS
# =====================================================

st.markdown(f"""
<style>

/* HEADER */
[data-testid="stHeader"] {{
    background: transparent;
}}

/* APP */
.stApp {{
    background: transparent;
}}

/* VIDEO */
video {{
    position: fixed;
    top: 0;
    left: 0;
    min-width: 100%;
    min-height: 100%;
    object-fit: cover;
    z-index: -2;
}}

/* OVERLAY */
.overlay {{
    position: fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background: rgba(0,0,0,0.65);
    z-index:-1;
}}

/* CONTAINER */
.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
}}

/* TEXT */
h1,h2,h3,h4,h5,h6,p,label,span {{
    color:white !important;
}}

/* PRODUCT CARD */
.product-box {{
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}}

/* INVOICE */
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

/* BUTTON */
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

/* DOWNLOAD BUTTON */
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

/* MOBILE */
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
        "gambar": "images/cokelat.jpg"
    },

    "Bakpau Ayam": {
        "harga": 7000,
        "gambar": "images/ayam.jpg"
    },

    "Bakpau Keju": {
        "harga": 5000,
        "gambar": "images/keju.jpg"
    },

    "Bakpau Kacang": {
        "harga": 5000,
        "gambar": "images/kacang.jpg"
    },

    "Bakpau Kentang": {
        "harga": 5000,
        "gambar": "images/kentang.jpg"
    }

}

# =====================================================
# SESSION
# =====================================================

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "invoice_terakhir" not in st.session_state:
    st.session_state.invoice_terakhir = None

# =====================================================
# HEADER
# =====================================================

st.title("🥟 Distributor Bakpau")
st.subheader("Sistem Distribusi & Pendapatan UMKM")

# =====================================================
# DASHBOARD
# =====================================================

total_omzet = sum(
    x["Total Omzet"]
    for x in st.session_state.riwayat
)

total_produk = sum(
    x["Total Qty"]
    for x in st.session_state.riwayat
)

total_transaksi = len(
    st.session_state.riwayat
)

belum_bayar = sum(
    x["Total Omzet"]
    for x in st.session_state.riwayat
    if x["Status"] == "Belum Bayar"
)

col1, col2, col3, col4 = st.columns(4)

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

with col4:
    st.metric(
        "💳 Belum Dibayar",
        f"Rp {belum_bayar:,}"
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
# BUTTON SIMPAN
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

        invoice_data = {

            "Tanggal":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),

            "Nama": nama,

            "Produk": gabungan_produk,

            "Total Qty": grand_qty,

            "Total Omzet": grand_jual,

            "Status": status
        }

        st.session_state.invoice_terakhir = invoice_data

        st.session_state.riwayat.append(
            invoice_data
        )

        st.success(
            "Distribusi berhasil disimpan"
        )

        st.rerun()

# =====================================================
# INVOICE
# =====================================================

if st.session_state.invoice_terakhir is not None:

    invoice = st.session_state.invoice_terakhir

    st.write("")
    st.markdown("## 🧾 Invoice")

    st.markdown(f"""
    <div class="invoice-box">

    <h2>🥟 Distributor Bakpau</h2>

    <hr>

    <p><b>Tanggal:</b> {invoice['Tanggal']}</p>

    <p><b>Nama:</b> {invoice['Nama']}</p>

    <p><b>Status:</b> {invoice['Status']}</p>

    <hr>

    <p><b>Produk:</b><br>
    {invoice['Produk']}
    </p>

    <hr>

    <h3>
    Total Produk: {invoice['Total Qty']} pcs
    </h3>

    <h1 style="color:#ff4b4b !important;">
    Rp {invoice['Total Omzet']:,}
    </h1>

    </div>
    """, unsafe_allow_html=True)

# =====================================================
# RIWAYAT
# =====================================================

st.write("")
st.markdown("## 📊 Riwayat Distribusi")

if len(st.session_state.riwayat) == 0:

    st.info("Belum ada data distribusi")

else:

    df = pd.DataFrame(
        st.session_state.riwayat
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )

    st.write("")
    st.markdown("## ✅ Update Status Pembayaran")

    for i, item in enumerate(st.session_state.riwayat):

        col1, col2, col3, col4 = st.columns([3,3,2,2])

        with col1:
            st.write(f"👤 {item['Nama']}")

        with col2:
            st.write(f"💰 Rp {item['Total Omzet']:,}")

        with col3:
            st.write(item["Status"])

        with col4:

            if item["Status"] == "Belum Bayar":

                if st.button(
                    f"Tandai Lunas #{i}",
                    key=f"lunas_{i}"
                ):

                    st.session_state.riwayat[i]["Status"] = "Sudah Bayar"

                    st.rerun()

            else:

                st.success("Lunas")

    # DOWNLOAD CSV

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

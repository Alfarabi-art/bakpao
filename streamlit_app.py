import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import urllib.parse

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Bakpao Ceu Mumun",
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

    h1,h2,h3,h4,h5,h6,p,label,span {{
        color:white !important;
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

    /* GLASS CARD */
    .metric-card {{
        background: rgba(255,255,255,0.12);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }}

    .metric-title {{
        font-size: 18px;
        margin-bottom: 10px;
    }}

    .metric-value {{
        font-size: 32px;
        font-weight: bold;
    }}

    /* PRODUCT */
    .product-box {{
        background: rgba(255,255,255,0.08);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 25px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
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
# PRODUK
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

    "Bakpao Kentang": {
        "harga": 6000,
        "gambar": "images/kentang.jpg"
    },

    "Bakpao Kacang": {
        "harga": 5000,
        "gambar": "images/kacang.jpg"
    },

    "Bakpao Unti Kelapa": {
        "harga": 5000,
        "gambar": "images/kelapa.jpg"
    }

}

# =====================================================
# AMBIL DATA SHEET
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
# LAPORAN OMZET
# =====================================================

st.write("")
st.markdown("## 📈 Laporan Omzet")

if not df_sheet.empty:

    df_sheet["Tanggal Convert"] = pd.to_datetime(
        df_sheet["Tanggal"],
        format="%d-%m-%Y %H:%M:%S",
        errors="coerce"
    )

    today = datetime.now().date()

    omzet_harian = df_sheet[
        df_sheet["Tanggal Convert"].dt.date == today
    ]["Total Omzet"].sum()

    now = datetime.now()

    omzet_bulanan = df_sheet[
        (df_sheet["Tanggal Convert"].dt.month == now.month) &
        (df_sheet["Tanggal Convert"].dt.year == now.year)
    ]["Total Omzet"].sum()

    omzet_tahunan = df_sheet[
        df_sheet["Tanggal Convert"].dt.year == now.year
    ]["Total Omzet"].sum()

else:

    omzet_harian = 0
    omzet_bulanan = 0
    omzet_tahunan = 0

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📅 Omzet Harian</div>
        <div class="metric-value">Rp {omzet_harian:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🗓️ Omzet Bulanan</div>
        <div class="metric-value">Rp {omzet_bulanan:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📆 Omzet Tahunan</div>
        <div class="metric-value">Rp {omzet_tahunan:,}</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# PDF FUNCTION
# =====================================================

def generate_pdf(
    nama,
    produk,
    total_qty,
    total_harga,
    status,
    tanggal
):

    buffer = BytesIO()

    p = canvas.Canvas(
        buffer,
        pagesize=letter
    )

    p.setFont("Helvetica-Bold", 20)

    p.drawString(
        200,
        750,
        "INVOICE BAKPAO"
    )

    p.setFont("Helvetica", 12)

    p.drawString(50, 700, f"Tanggal : {tanggal}")
    p.drawString(50, 680, f"Nama : {nama}")

    p.drawString(50, 650, "Produk :")

    y = 630

    for item in produk.split("\n"):

        p.drawString(70, y, f"- {item}")

        y -= 20

    p.drawString(
        50,
        y - 20,
        f"Total Qty : {total_qty}"
    )

    p.drawString(
        50,
        y - 40,
        f"Total Bayar : Rp {total_harga:,}"
    )

    p.drawString(
        50,
        y - 60,
        f"Status : {status}"
    )

    p.save()

    buffer.seek(0)

    return buffer

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
        <h2>Rp {data['harga']:,}</h2>
        """, unsafe_allow_html=True)

        qty = st.number_input(
            f"Qty {nama_produk}",
            min_value=0,
            step=1,
            key=nama_produk
        )

    st.markdown('</div>', unsafe_allow_html=True)

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

        # SIMPAN GOOGLE SHEETS
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

        # PDF
        pdf_file = generate_pdf(
            nama,
            gabungan_produk,
            grand_qty,
            grand_jual,
            status,
            waktu
        )

        st.download_button(
            label="📄 Download Invoice PDF",
            data=pdf_file,
            file_name=f"invoice_{nama}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        # WHATSAPP
        pesan = f'''
Halo {nama}

Berikut invoice pembelian Anda.

🧾 Produk:
{gabungan_produk}

📦 Total Qty: {grand_qty}
💰 Total Bayar: Rp {grand_jual:,}
💳 Status: {status}

Terima kasih 🙏
'''

        wa_link = (
            "https://wa.me/?text=" +
            urllib.parse.quote(pesan)
        )

        st.link_button(
            "📲 Kirim ke WhatsApp",
            wa_link,
            use_container_width=True
        )

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

if not df_sheet.empty:

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

    headers = [
        "Tanggal",
        "Nama",
        "Produk",
        "Total Qty",
        "Total Omzet",
        "Status"
    ]

    sheet.clear()

    sheet.append_row(headers)

    st.success("Semua data berhasil dihapus")

    st.rerun()

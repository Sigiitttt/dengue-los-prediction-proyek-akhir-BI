import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="MediPredict · Estimasi LOS DBD",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state ─────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Estimasi LOS"

st.markdown("""
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
p, span, label, h1, h2, h3, h4, div, li, button {
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(140deg, #0A7EA4 0%, #0A7EA4 40%, #047857 100%) !important;
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent !important; display: none !important; }
.main .block-container   { padding: 2rem 2.5rem !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.08) !important;
    border-right: 1px solid rgba(255,255,255,0.12) !important;
}
[data-testid="stSidebar"] > div { padding: 1.5rem 1.2rem !important; }

p, span, label, div { color: rgba(255,255,255,0.85) !important; }

/* logo */
.logo-wrap { display:flex;align-items:center;gap:10px;margin-bottom:28px; }
.logo-icon { width:38px;height:38px;border-radius:10px;background:#F97316;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0; }
.logo-name { font-size:15px !important;font-weight:700 !important;color:#fff !important;letter-spacing:-0.3px; }
.logo-sub  { font-size:11px !important;color:rgba(255,255,255,0.45) !important;margin-top:1px; }
.nav-label { font-size:10px !important;font-weight:700 !important;letter-spacing:.10em !important;text-transform:uppercase !important;color:rgba(255,255,255,0.30) !important;margin-bottom:6px; }
.stat-block{ padding-top:24px;display:flex;flex-direction:column;gap:8px; }
.stat-card-s{ background:rgba(255,255,255,0.09);border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:12px 14px; }
.stat-lbl  { font-size:10px !important;color:rgba(255,255,255,0.40) !important;margin-bottom:4px; }
.stat-num  { font-size:22px !important;font-weight:700 !important;color:#fff !important;letter-spacing:-0.5px; }
.stat-unit { font-size:11px !important;color:rgba(255,255,255,0.40) !important;margin-left:3px;font-weight:400 !important; }

/* nav buttons */
[data-testid="stSidebar"] [data-testid="baseButton-secondary"] {
    background: transparent !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 9px 12px !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    color: rgba(255,255,255,0.55) !important;
    width: 100% !important;
    text-align: left !important;
    margin-bottom: 2px !important;
    box-shadow: none !important;
    transition: background .15s !important;
    justify-content: flex-start !important;
}
[data-testid="stSidebar"] [data-testid="baseButton-secondary"]:hover {
    background: rgba(255,255,255,0.07) !important;
    color: #fff !important;
}
[data-testid="stSidebar"] [data-testid="baseButton-secondary"] p {
    color: inherit !important;
    font-weight: inherit !important;
}

/* nav button aktif — pakai key class via st.markdown trick, kita handle via CSS :focus */
.nav-active [data-testid="baseButton-secondary"] {
    background: rgba(255,255,255,0.14) !important;
    color: #fff !important;
    font-weight: 500 !important;
}

/* page header */
.page-breadcrumb { font-size:11px !important;color:rgba(255,255,255,0.35) !important;margin-bottom:6px;letter-spacing:.03em; }
.page-title      { font-size:26px !important;font-weight:700 !important;color:#fff !important;letter-spacing:-0.6px;line-height:1.2; }
.page-sub        { font-size:13px !important;color:rgba(255,255,255,0.45) !important;margin-top:5px;line-height:1.5;margin-bottom:28px; }

/* glass card */
.glass {
    background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.16);
    border-radius:18px;padding:20px 24px 6px;margin-bottom:4px;
}
.card-ttl {
    font-size:10.5px !important;font-weight:700 !important;letter-spacing:.09em !important;
    text-transform:uppercase !important;color:rgba(255,255,255,0.40) !important;
    display:flex;align-items:center;gap:8px;margin-bottom:14px;
}
.cdot         { width:6px;height:6px;border-radius:50%;display:inline-block;flex-shrink:0; }
.cdot-orange  { background:#F97316; }
.cdot-teal    { background:#34D399; }

/* form */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    font-size:11px !important;font-weight:500 !important;
    color:rgba(255,255,255,0.50) !important;margin-bottom:4px !important;
}
[data-baseweb="select"] > div,
[data-baseweb="base-input"] {
    background:rgba(255,255,255,0.08) !important;
    border:1px solid rgba(255,255,255,0.15) !important;
    border-radius:10px !important;color:#fff !important;
}
[data-baseweb="select"] > div:focus-within,
[data-baseweb="base-input"]:focus-within {
    border-color:rgba(255,255,255,0.45) !important;background:rgba(255,255,255,0.14) !important;box-shadow:none !important;
}
[data-baseweb="select"] *     { color:#fff !important; }
[data-baseweb="popover"]      { background:#0d7090 !important;border:1px solid rgba(255,255,255,0.15) !important;border-radius:12px !important; }
[data-baseweb="menu"]         { background:#0d7090 !important; }
[data-baseweb="option"]:hover { background:rgba(255,255,255,0.12) !important; }
input[type="number"]          { color:#fff !important;background:transparent !important; }
[data-testid="stNumberInput"] button {
    background:rgba(255,255,255,0.08) !important;border:1px solid rgba(255,255,255,0.15) !important;
    border-radius:8px !important;color:rgba(255,255,255,0.6) !important;
}
[data-testid="stNumberInput"] button:hover { background:rgba(255,255,255,0.18) !important;color:#fff !important; }

.footer-note { font-size:12px !important;color:rgba(255,255,255,0.32) !important;line-height:1.55 !important;margin-bottom:12px; }

/* CTA button (di konten utama) */
[data-testid="stMain"] [data-testid="baseButton-secondary"] {
    background:#F97316 !important;border:none !important;
    border-radius:12px !important;padding:0.65rem 2rem !important;
    font-size:0.9rem !important;font-weight:700 !important;
    box-shadow:0 4px 18px rgba(249,115,22,0.35) !important;
    transition:opacity .2s,transform .15s !important;
}
[data-testid="stMain"] [data-testid="baseButton-secondary"]:hover { opacity:.88 !important;transform:translateY(-1px) !important; }
[data-testid="stMain"] [data-testid="baseButton-secondary"] p     { color:#fff !important;font-weight:700 !important; }

/* result */
.result-box {
    background:rgba(249,115,22,0.12);border:1px solid rgba(249,115,22,0.28);
    border-radius:18px;padding:22px 26px;margin-top:16px;
    display:flex;align-items:center;gap:24px;
}
.result-num   { font-size:52px !important;font-weight:800 !important;color:#FED7AA !important;letter-spacing:-2px;line-height:1; }
.result-unit  { font-size:14px !important;color:rgba(255,255,255,0.40) !important;margin-top:2px; }
.result-vdiv  { width:1px;background:rgba(255,255,255,0.12);align-self:stretch;flex-shrink:0; }
.result-risk  { font-size:16px !important;font-weight:700 !important;margin-bottom:6px; }
.result-note-t{ font-size:12px !important;color:rgba(255,255,255,0.38) !important;line-height:1.55 !important; }
.risk-low { color:#34D399 !important; }
.risk-med { color:#FCD34D !important; }
.risk-hi  { color:#FCA5A5 !important; }

/* placeholder pages */
.placeholder {
    background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);
    border-radius:18px;padding:48px 32px;text-align:center;margin-top:8px;
}
.placeholder-icon { font-size:40px;margin-bottom:14px; }
.placeholder-title{ font-size:18px !important;font-weight:700 !important;color:#fff !important;margin-bottom:8px; }
.placeholder-sub  { font-size:13px !important;color:rgba(255,255,255,0.40) !important;line-height:1.6 !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
      <div class="logo-icon">🏥</div>
      <div>
        <div class="logo-name">MediPredict</div>
        <div class="logo-sub">Clinical Decision Support</div>
      </div>
    </div>
    <div class="nav-label">Menu</div>
    """, unsafe_allow_html=True)

    pages = {
        "Estimasi LOS":      "🩺",
        "Riwayat Prediksi":  "📋",
        "Statistik Model":   "📊",
        "Panduan Penggunaan":"📖",
    }

    for label, icon in pages.items():
        is_active = st.session_state.page == label
        # Warna teks berubah berdasarkan state aktif
        btn_style = (
            "background:rgba(255,255,255,0.14);color:#fff;font-weight:600;"
            if is_active else
            "background:transparent;color:rgba(255,255,255,0.55);"
        )
        st.markdown(f"""
        <style>
        div[data-testid="stButton"]:has(button[kind="secondary"][aria-label="{label}"])
            button {{
            {btn_style}
            border-radius:10px !important;padding:9px 12px !important;
            width:100% !important;text-align:left !important;
            border:none !important;box-shadow:none !important;
            font-size:13px !important;margin-bottom:2px !important;
        }}
        </style>
        """, unsafe_allow_html=True)

        if st.button(f"{icon}  {label}", key=label, args=None,
                     help=None, use_container_width=True):
            st.session_state.page = label
            st.rerun()

    st.markdown("""
    <div class="stat-block">
      <div class="stat-card-s">
        <div class="stat-lbl">Akurasi Model</div>
        <div class="stat-num">87.4<span class="stat-unit">%</span></div>
      </div>
      <div class="stat-card-s">
        <div class="stat-lbl">Margin Error (MAD)</div>
        <div class="stat-num">±1.5<span class="stat-unit">hari</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# ROUTER HALAMAN
# ═══════════════════════════════════════════════════════
page = st.session_state.page

# ── PAGE: Estimasi LOS ────────────────────────────────
if page == "Estimasi LOS":
    st.markdown("""
    <div class="page-breadcrumb">Dashboard · Prediksi LOS</div>
    <div class="page-title">Estimasi Rawat Inap DBD</div>
    <div class="page-sub">Masukkan data klinis pasien untuk mendapatkan prediksi durasi perawatan.</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass"><div class="card-ttl"><span class="cdot cdot-orange"></span>Profil Pasien</div></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        input_jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    with c2:
        input_umur = st.number_input("Umur (Tahun)", min_value=1, max_value=100, value=25)
    with c3:
        input_demam = st.selectbox("Diagnosis",
            ["DD (Dengue Fever)", "DBD (Hemorrhagic)", "DSS (Shock Syndrome)"])

    st.markdown('<div class="glass"><div class="card-ttl"><span class="cdot cdot-teal"></span>Hasil Laboratorium</div></div>', unsafe_allow_html=True)
    l1, l2, l3 = st.columns(3)
    with l1:
        input_hb = st.number_input("Hemoglobin (g/dL)", min_value=1.0, max_value=25.0, value=12.0, step=0.1)
    with l2:
        input_hct = st.number_input("Hematokrit (%)", min_value=10.0, max_value=65.0, value=40.0, step=0.1)
    with l3:
        input_trombo = st.number_input("Trombosit (/µL)", min_value=1000, max_value=500000, value=100000, step=1000)

    st.markdown('<div class="footer-note" style="margin-top:16px;">Hasil prediksi bersifat estimasi ± 1.5 hari. Gunakan sebagai referensi sekunder, bukan diagnosis klinis final.</div>', unsafe_allow_html=True)

    proses = st.button("Proses Analisis →")

    val_jk    = 0 if input_jk == "Laki-laki" else 1
    val_demam = 0 if input_demam.startswith("DD") else (1 if input_demam.startswith("DBD") else 2)

    if proses:
        try:
            model  = joblib.load("model_regresi_dbd.pkl")
            scaler = joblib.load("scaler_dbd.pkl")
            fitur  = pd.DataFrame(
                [[val_jk, input_umur, val_demam, input_hb, input_hct, input_trombo]],
                columns=["jenis_kelamin","umur","jenis_demam","hemoglobin","hct","trombosit"]
            )
            hari = max(1, round(model.predict(scaler.transform(fitur))[0], 1))
            if hari <= 5:   rc, rl = "risk-low", "Risiko Rendah"
            elif hari <= 8: rc, rl = "risk-med", "Risiko Sedang"
            else:           rc, rl = "risk-hi",  "Risiko Tinggi"

            st.markdown(f"""
            <div class="result-box">
              <div><div class="result-num">{hari}</div><div class="result-unit">hari</div></div>
              <div class="result-vdiv"></div>
              <div>
                <div class="result-risk {rc}">{rl}</div>
                <div class="result-note-t">Diprediksi oleh Stacking Regression Model<br>
                berdasarkan parameter klinis yang dimasukkan. Margin error ± 1.5 hari.</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        except FileNotFoundError:
            st.error("File model tidak ditemukan. Pastikan model_regresi_dbd.pkl dan scaler_dbd.pkl ada di direktori yang sama.")


# ── PAGE: Riwayat Prediksi ────────────────────────────
elif page == "Riwayat Prediksi":
    st.markdown('<div class="page-title">Riwayat Prediksi</div><div class="page-sub">Daftar prediksi yang telah dilakukan sebelumnya.</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="placeholder">
      <div class="placeholder-icon">📋</div>
      <div class="placeholder-title">Belum ada riwayat</div>
      <div class="placeholder-sub">Riwayat prediksi akan muncul di sini setelah kamu melakukan analisis pertama.</div>
    </div>
    """, unsafe_allow_html=True)


# ── PAGE: Statistik Model ─────────────────────────────
elif page == "Statistik Model":
    st.markdown('<div class="page-title">Statistik Model</div><div class="page-sub">Performa dan metrik evaluasi model Stacking Regression.</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("Akurasi", "87.4", "%"),
        ("MAE", "1.32", "hari"),
        ("RMSE", "1.87", "hari"),
        ("R² Score", "0.81", ""),
    ]
    for col, (label, val, unit) in zip([m1,m2,m3,m4], metrics):
        with col:
            st.markdown(f"""
            <div class="stat-card-s" style="padding:18px 20px;">
              <div class="stat-lbl">{label}</div>
              <div class="stat-num">{val}<span class="stat-unit">{unit}</span></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="placeholder" style="margin-top:16px;">
      <div class="placeholder-icon">📊</div>
      <div class="placeholder-title">Visualisasi segera hadir</div>
      <div class="placeholder-sub">Grafik feature importance dan learning curve akan ditampilkan di sini.</div>
    </div>
    """, unsafe_allow_html=True)


# ── PAGE: Panduan Penggunaan ──────────────────────────
elif page == "Panduan Penggunaan":
    st.markdown('<div class="page-title">Panduan Penggunaan</div><div class="page-sub">Cara menggunakan aplikasi MediPredict dengan benar.</div>', unsafe_allow_html=True)

    steps = [
        ("1", "Isi Profil Pasien", "Masukkan jenis kelamin, umur, dan diagnosis pasien DBD pada bagian Profil Pasien."),
        ("2", "Input Hasil Lab",   "Masukkan nilai hemoglobin, hematokrit, dan trombosit dari hasil laboratorium terkini."),
        ("3", "Proses Analisis",   "Klik tombol Proses Analisis. Model akan memproses data dan menghasilkan estimasi lama rawat inap."),
        ("4", "Interpretasi",      "Hasil menampilkan estimasi hari rawat dan kategori risiko: Rendah (≤5 hari), Sedang (6–8 hari), Tinggi (>8 hari)."),
    ]
    for num, title, desc in steps:
        st.markdown(f"""
        <div class="glass" style="display:flex;align-items:flex-start;gap:16px;padding:18px 22px;margin-bottom:10px;">
          <div style="width:32px;height:32px;border-radius:50%;background:#F97316;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:#fff;flex-shrink:0;">{num}</div>
          <div>
            <div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:4px;">{title}</div>
            <div style="font-size:13px;color:rgba(255,255,255,0.50);line-height:1.55;">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

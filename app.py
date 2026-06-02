import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="MediPredict · Estimasi LOS DBD",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "page" not in st.session_state:
    st.session_state.page = "Estimasi LOS"

st.markdown("""
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
p, span, label, h1, h2, h3, h4, div, li, button {
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif !important;
}

/* ── Background ── */
[data-testid="stAppViewContainer"] { background: #F0F4FF !important; }
[data-testid="stHeader"]           { display: none !important; }
.main .block-container             { padding: 2rem 2.5rem !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #E4E9F2 !important;
}
[data-testid="stSidebar"] > div { padding: 1.8rem 1.4rem !important; }

/* reset warna teks global */
p, span, label, div { color: #1A1A2E !important; }

/* ── Brand ── */
.brand-row  { display:flex;align-items:center;gap:9px;margin-bottom:3px; }
.brand-dot  { width:10px;height:10px;border-radius:50%;background:#F97316;display:inline-block; }
.brand-name { font-size:16px !important;font-weight:700 !important;color:#1A1A2E !important;letter-spacing:-0.4px; }
.brand-tag  { font-size:11px !important;color:#A0AABF !important;padding-left:19px; }

/* ── Nav label ── */
.nav-label  {
    font-size:10px !important;font-weight:700 !important;letter-spacing:.12em !important;
    text-transform:uppercase !important;color:#C0C8D8 !important;
    margin-bottom:6px; margin-top:24px;
}

/* ── Nav buttons di sidebar ── */
[data-testid="stSidebar"] [data-testid="baseButton-secondary"] {
    background: transparent !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 9px 11px !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    color: #7A8499 !important;
    width: 100% !important;
    text-align: left !important;
    margin-bottom: 2px !important;
    box-shadow: none !important;
    justify-content: flex-start !important;
    transition: background .15s, color .15s !important;
}
[data-testid="stSidebar"] [data-testid="baseButton-secondary"]:hover {
    background: #F5F7FF !important;
    color: #3B5BDB !important;
}
[data-testid="stSidebar"] [data-testid="baseButton-secondary"] p {
    color: inherit !important;
    font-weight: inherit !important;
}

/* ── Mini stat di sidebar ── */
.mini-stat {
    background:#F8FAFF;border:1px solid #E4E9F2;
    border-radius:12px;padding:12px 14px;margin-bottom:8px;
}
.mini-stat-label { font-size:10px !important;color:#A0AABF !important;margin-bottom:3px; }
.mini-stat-val   { font-size:21px !important;font-weight:700 !important;color:#1A1A2E !important;letter-spacing:-0.5px; }
.mini-stat-unit  { font-size:11px !important;color:#A0AABF !important;margin-left:2px;font-weight:400 !important; }

/* ── Page header ── */
.crumb    { font-size:11px !important;color:#A0AABF !important;margin-bottom:5px;letter-spacing:.02em; }
.page-h   { font-size:24px !important;font-weight:700 !important;color:#1A1A2E !important;letter-spacing:-0.6px;line-height:1.2; }
.page-sub { font-size:13px !important;color:#7A8499 !important;margin-top:4px;line-height:1.5;margin-bottom:24px; }

.topbadge {
    display:inline-flex;align-items:center;gap:7px;
    background:#fff;border:1px solid #E4E9F2;border-radius:20px;
    padding:6px 13px;font-size:11px;color:#7A8499;font-weight:500;
    float:right; margin-top:4px;
}
.live-dot {
    width:6px;height:6px;border-radius:50%;background:#10B981;
    display:inline-block;animation:pulse 2s infinite;
}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}

/* ── White card ── */
.wcard {
    background:#fff;border:1px solid #E4E9F2;
    border-radius:16px;padding:20px 22px 8px;margin-bottom:14px;
}
.card-hdr {
    display:flex;align-items:center;gap:8px;margin-bottom:16px;
}
.cdot          { width:7px;height:7px;border-radius:50%;display:inline-block;flex-shrink:0; }
.cdot-orange   { background:#F97316; }
.cdot-green    { background:#10B981; }
.card-ttl {
    font-size:10px !important;font-weight:700 !important;letter-spacing:.10em !important;
    text-transform:uppercase !important;color:#A0AABF !important;
}

/* ── Form elements ── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    font-size:11px !important;font-weight:500 !important;
    color:#7A8499 !important;margin-bottom:4px !important;
}
[data-baseweb="select"] > div,
[data-baseweb="base-input"] {
    background:#F8FAFF !important;
    border:1px solid #E4E9F2 !important;
    border-radius:9px !important;
    color:#1A1A2E !important;
    transition:border-color .15s,background .15s !important;
}
[data-baseweb="select"] > div:focus-within,
[data-baseweb="base-input"]:focus-within {
    border-color:#3B5BDB !important;background:#fff !important;box-shadow:none !important;
}
[data-baseweb="select"] * { color:#1A1A2E !important; }
[data-baseweb="popover"]  { background:#fff !important;border:1px solid #E4E9F2 !important;border-radius:12px !important; }
[data-baseweb="menu"]     { background:#fff !important; }
[data-baseweb="option"]:hover { background:#F0F4FF !important; }
input[type="number"]      { color:#1A1A2E !important; }

[data-testid="stNumberInput"] button {
    background:#F0F4FF !important;border:1px solid #E4E9F2 !important;
    border-radius:8px !important;color:#7A8499 !important;
}
[data-testid="stNumberInput"] button:hover {
    background:#EEF2FF !important;color:#3B5BDB !important;border-color:#C5D0FF !important;
}

/* ── Action note ── */
.action-note {
    font-size:12px !important;color:#A0AABF !important;
    line-height:1.55 !important;margin-bottom:12px;
}

/* ── CTA button di konten utama ── */
[data-testid="stMain"] [data-testid="baseButton-secondary"] {
    background: #F97316 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(249,115,22,0.28) !important;
    transition: opacity .2s, transform .15s !important;
}
[data-testid="stMain"] [data-testid="baseButton-secondary"]:hover {
    opacity: .88 !important; transform: translateY(-1px) !important;
}
[data-testid="stMain"] [data-testid="baseButton-secondary"] p {
    color: #fff !important; font-weight: 700 !important;
}

/* ── Result ── */
.result-box {
    background:#FFF7ED;border:1px solid #FED7AA;
    border-radius:16px;padding:20px 24px;margin-top:4px;
    display:flex;align-items:center;gap:22px;
}
.r-num  { font-size:50px !important;font-weight:800 !important;color:#EA580C !important;letter-spacing:-2px;line-height:1; }
.r-unit { font-size:13px !important;color:#A0AABF !important;margin-top:1px; }
.r-div  { width:1px;background:#FED7AA;align-self:stretch;flex-shrink:0; }
.r-risk { font-size:15px !important;font-weight:700 !important;margin-bottom:5px; }
.r-note { font-size:12px !important;color:#A0AABF !important;line-height:1.55 !important; }
.low    { color:#10B981 !important; }
.med    { color:#F59E0B !important; }
.hi     { color:#EF4444 !important; }

/* placeholder pages */
.placeholder {
    background:#fff;border:1px solid #E4E9F2;
    border-radius:16px;padding:48px 32px;text-align:center;margin-top:8px;
}
.ph-icon  { font-size:36px;margin-bottom:12px; }
.ph-title { font-size:18px !important;font-weight:700 !important;color:#1A1A2E !important;margin-bottom:8px; }
.ph-sub   { font-size:13px !important;color:#A0AABF !important;line-height:1.6 !important; }

.metric-row { display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px; }
.metric-card {
    background:#fff;border:1px solid #E4E9F2;border-radius:14px;padding:16px 18px;
}
.metric-label { font-size:10px !important;color:#A0AABF !important;margin-bottom:6px;letter-spacing:.03em; }
.metric-val   { font-size:24px !important;font-weight:700 !important;color:#1A1A2E !important;letter-spacing:-0.5px; }
.metric-unit  { font-size:12px !important;color:#A0AABF !important;margin-left:2px;font-weight:400 !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:28px">
      <div class="brand-row"><div class="brand-dot"></div><div class="brand-name">MediPredict</div></div>
      <div class="brand-tag">Clinical Decision Support</div>
    </div>
    <div class="nav-label">Menu Utama</div>
    """, unsafe_allow_html=True)

    pages = {
        "Estimasi LOS":     "🩺",
        "Riwayat":          "📋",
        "Statistik Model":  "📊",
        "Panduan":          "📖",
    }
    for label, icon in pages.items():
        is_active = st.session_state.page == label
        style = (
            "background:#EEF2FF !important;color:#3B5BDB !important;font-weight:600 !important;"
            if is_active else ""
        )
        st.markdown(f"""
        <style>
        div[data-testid="stButton"]:has(button[aria-label="{label}"]) button {{
            {style}
        }}
        </style>
        """, unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=label, use_container_width=True):
            st.session_state.page = label
            st.rerun()

    st.markdown("""
    <div style="margin-top:28px">
      <div class="mini-stat">
        <div class="mini-stat-label">Akurasi Model</div>
        <div class="mini-stat-val">87.4<span class="mini-stat-unit">%</span></div>
      </div>
      <div class="mini-stat">
        <div class="mini-stat-label">Margin Error (MAD)</div>
        <div class="mini-stat-val">±1.5<span class="mini-stat-unit">hari</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════
page = st.session_state.page


# ── Estimasi LOS ─────────────────────────────────────
if page == "Estimasi LOS":
    st.markdown("""
    <div class="crumb">Dashboard · Prediksi LOS</div>
    <div class="page-h">Estimasi Rawat Inap DBD
      <span class="topbadge"><span class="live-dot"></span>&nbsp;Stacking Regression</span>
    </div>
    <div class="page-sub">Input data klinis — model prediksi durasi perawatan otomatis.</div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.6], gap="medium")

    with col_left:
        st.markdown('<div class="wcard"><div class="card-hdr"><div class="cdot cdot-orange"></div><div class="card-ttl">Profil Pasien</div></div></div>', unsafe_allow_html=True)
        input_jk    = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        input_umur  = st.number_input("Umur (Tahun)", min_value=1, max_value=100, value=25)
        input_demam = st.selectbox("Diagnosis", [
            "DD — Dengue Fever",
            "DBD — Hemorrhagic",
            "DSS — Shock Syndrome"
        ])

    with col_right:
        st.markdown('<div class="wcard"><div class="card-hdr"><div class="cdot cdot-green"></div><div class="card-ttl">Hasil Laboratorium</div></div></div>', unsafe_allow_html=True)
        l1, l2, l3 = st.columns(3)
        with l1:
            input_hb = st.number_input("Hemoglobin (g/dL)", min_value=1.0, max_value=25.0, value=12.0, step=0.1)
        with l2:
            input_hct = st.number_input("Hematokrit (%)", min_value=10.0, max_value=65.0, value=40.0, step=0.1)
        with l3:
            input_trombo = st.number_input("Trombosit (/µL)", min_value=1000, max_value=500000, value=100000, step=1000)

        st.markdown('<div class="action-note" style="margin-top:12px">Estimasi ± 1.5 hari. Gunakan sebagai referensi sekunder, bukan diagnosis klinis final.</div>', unsafe_allow_html=True)
        proses = st.button("Analisis →")

    val_jk    = 0 if input_jk == "Laki-laki" else 1
    val_demam = 0 if "DD" in input_demam else (1 if "DBD" in input_demam else 2)

    if proses:
        try:
            model  = joblib.load("model_regresi_dbd.pkl")
            scaler = joblib.load("scaler_dbd.pkl")
            fitur  = pd.DataFrame(
                [[val_jk, input_umur, val_demam, input_hb, input_hct, input_trombo]],
                columns=["jenis_kelamin","umur","jenis_demam","hemoglobin","hct","trombosit"]
            )
            hari = max(1, round(model.predict(scaler.transform(fitur))[0], 1))
            if hari <= 5:   rc, rl = "low", "Risiko Rendah"
            elif hari <= 8: rc, rl = "med", "Risiko Sedang"
            else:           rc, rl = "hi",  "Risiko Tinggi"

            st.markdown(f"""
            <div class="result-box">
              <div><div class="r-num">{hari}</div><div class="r-unit">hari</div></div>
              <div class="r-div"></div>
              <div>
                <div class="r-risk {rc}">{rl}</div>
                <div class="r-note">Diprediksi Stacking Regression · berdasarkan parameter klinis · margin ± 1.5 hari</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        except FileNotFoundError:
            st.error("File model tidak ditemukan. Pastikan model_regresi_dbd.pkl dan scaler_dbd.pkl ada di direktori yang sama.")


# ── Riwayat ──────────────────────────────────────────
elif page == "Riwayat":
    st.markdown('<div class="page-h">Riwayat Prediksi</div><div class="page-sub">Daftar prediksi yang telah dilakukan.</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="placeholder">
      <div class="ph-icon">📋</div>
      <div class="ph-title">Belum ada riwayat</div>
      <div class="ph-sub">Riwayat prediksi akan muncul di sini setelah kamu melakukan analisis pertama.</div>
    </div>
    """, unsafe_allow_html=True)


# ── Statistik Model ───────────────────────────────────
elif page == "Statistik Model":
    st.markdown('<div class="page-h">Statistik Model</div><div class="page-sub">Performa dan metrik evaluasi Stacking Regression.</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="metric-row">
      <div class="metric-card"><div class="metric-label">Akurasi</div><div class="metric-val">87.4<span class="metric-unit">%</span></div></div>
      <div class="metric-card"><div class="metric-label">MAE</div><div class="metric-val">1.32<span class="metric-unit">hari</span></div></div>
      <div class="metric-card"><div class="metric-label">RMSE</div><div class="metric-val">1.87<span class="metric-unit">hari</span></div></div>
      <div class="metric-card"><div class="metric-label">R² Score</div><div class="metric-val">0.81</div></div>
    </div>
    <div class="placeholder">
      <div class="ph-icon">📊</div>
      <div class="ph-title">Visualisasi segera hadir</div>
      <div class="ph-sub">Grafik feature importance dan learning curve akan ditampilkan di sini.</div>
    </div>
    """, unsafe_allow_html=True)


# ── Panduan ───────────────────────────────────────────
elif page == "Panduan":
    st.markdown('<div class="page-h">Panduan Penggunaan</div><div class="page-sub">Cara menggunakan MediPredict dengan benar.</div>', unsafe_allow_html=True)
    steps = [
        ("1", "Isi Profil Pasien", "Masukkan jenis kelamin, umur, dan diagnosis pasien pada kolom kiri."),
        ("2", "Input Hasil Lab",   "Masukkan nilai hemoglobin, hematokrit, dan trombosit terkini."),
        ("3", "Klik Analisis",     "Tekan tombol Analisis — model memproses data dan menghasilkan estimasi hari rawat."),
        ("4", "Baca Hasilnya",     "Lihat estimasi hari dan kategori risiko: Rendah ≤5 hari, Sedang 6–8 hari, Tinggi >8 hari."),
    ]
    for num, title, desc in steps:
        st.markdown(f"""
        <div class="wcard" style="display:flex;align-items:flex-start;gap:14px;padding:18px 22px;margin-bottom:10px">
          <div style="width:30px;height:30px;border-radius:50%;background:#F97316;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:#fff;flex-shrink:0">{num}</div>
          <div>
            <div style="font-size:14px;font-weight:600;color:#1A1A2E;margin-bottom:4px">{title}</div>
            <div style="font-size:13px;color:#7A8499;line-height:1.55">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

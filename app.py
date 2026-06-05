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
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Syne:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Global font override ── */
html, body, p, span, label, h1, h2, h3, h4, div, li, button, input, select, textarea {
    font-family: 'Syne', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ── Background & layout ── */
[data-testid="stAppViewContainer"] { background: #0D0F14 !important; }
[data-testid="stHeader"]           { display: none !important; }
.main .block-container             { padding: 2.2rem 2.8rem !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #13161D !important;
    border-right: 1px solid #252A38 !important;
}
[data-testid="stSidebar"] > div { padding: 1.8rem 1.4rem !important; }

/* reset text colors */
p, span, label, div { color: #F0F2F8 !important; }

/* ── Brand ── */
.brand-row  { display:flex; align-items:center; gap:10px; margin-bottom:4px; }
.brand-icon {
    width:34px; height:34px; background:#F97316; border-radius:9px;
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
}
.brand-icon-inner { font-size:16px; line-height:1; }
.brand-name { font-size:15px !important; font-weight:800 !important; color:#F0F2F8 !important; letter-spacing:-0.3px; }
.brand-sub  { font-size:9px !important; color:#3D4557 !important; letter-spacing:.12em; text-transform:uppercase; margin-bottom:28px; padding-left:44px; }

/* ── Nav section label ── */
.nav-label {
    font-size:9px !important; font-weight:700 !important; letter-spacing:.14em !important;
    text-transform:uppercase !important; color:#3D4557 !important;
    margin-bottom:8px; margin-top:24px;
}

/* ── Nav radio ── */
[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    display: none !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
    gap: 2px !important;
    display: flex !important;
    flex-direction: column !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    padding: 9px 12px !important;
    cursor: pointer !important;
    transition: background .15s, color .15s !important;
    align-items: center !important;
    gap: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:hover {
    background: #191D27 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] span:last-child {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #7A8499 !important;
    padding-left: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
    background: rgba(249,115,22,.12) !important;
    border: 1px solid rgba(249,115,22,.2) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span:last-child {
    color: #F97316 !important;
    font-weight: 700 !important;
}
/* sembunyikan radio circle asli */
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
    display: none !important;
}

/* ── Sidebar stats ── */
.mini-stat {
    background: #191D27;
    border: 1px solid #252A38;
    border-radius: 13px;
    padding: 14px 16px;
    margin-bottom: 8px;
}
.mini-stat-label { font-size:9px !important; color:#7A8499 !important; letter-spacing:.08em; text-transform:uppercase; margin-bottom:6px; }
.mini-stat-val   { font-size:22px !important; font-weight:800 !important; color:#F0F2F8 !important; letter-spacing:-0.8px; line-height:1; }
.mini-stat-unit  { font-size:11px !important; color:#7A8499 !important; margin-left:2px; font-weight:400 !important; }
.mini-stat-bar   { height:3px; background:#252A38; border-radius:2px; margin-top:10px; overflow:hidden; }
.mini-stat-fill  { height:100%; width:87.4%; border-radius:2px; background:#F97316; }

/* ── Page header ── */
.crumb    { font-size:11px !important; color:#3D4557 !important; margin-bottom:6px; letter-spacing:.04em; }
.page-h   { font-size:26px !important; font-weight:800 !important; color:#F0F2F8 !important; letter-spacing:-0.8px; line-height:1.1; }
.page-h em { font-family:'Instrument Serif', Georgia, serif !important; font-style:italic; color:#F97316 !important; }
.page-sub { font-size:13px !important; color:#7A8499 !important; margin-top:6px; line-height:1.55; margin-bottom:28px; }

.topbadge {
    display:inline-flex; align-items:center; gap:7px;
    background:#13161D; border:1px solid #252A38; border-radius:20px;
    padding:7px 14px; font-size:11px; color:#7A8499; font-weight:500;
    float:right; margin-top:6px;
}
.live-dot {
    width:7px; height:7px; border-radius:50%; background:#10B981;
    display:inline-block; animation:pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; box-shadow:0 0 0 0 rgba(16,185,129,.4); }
    50%      { opacity:.7; box-shadow:0 0 0 5px rgba(16,185,129,0); }
}

/* ── White card → Dark card ── */
.wcard {
    background: #13161D;
    border: 1px solid #252A38;
    border-radius: 18px;
    padding: 22px 24px 10px;
    margin-bottom: 16px;
}
.card-hdr {
    display:flex; align-items:center; gap:9px;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 1px solid #252A38;
}
.cdot        { width:8px; height:8px; border-radius:50%; display:inline-block; flex-shrink:0; }
.cdot-orange { background:#F97316; }
.cdot-green  { background:#10B981; }
.card-ttl {
    font-size:9px !important; font-weight:700 !important; letter-spacing:.14em !important;
    text-transform:uppercase !important; color:#7A8499 !important;
}

/* ── Form elements ── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    font-size:10px !important; font-weight:600 !important;
    letter-spacing:.08em !important; text-transform:uppercase !important;
    color:#7A8499 !important; margin-bottom:6px !important;
}
[data-baseweb="select"] > div,
[data-baseweb="base-input"] {
    background: #191D27 !important;
    border: 1px solid #252A38 !important;
    border-radius: 10px !important;
    color: #F0F2F8 !important;
    transition: border-color .2s, background .2s !important;
}
[data-baseweb="select"] > div:focus-within,
[data-baseweb="base-input"]:focus-within {
    border-color: #F97316 !important;
    background: #0D0F14 !important;
    box-shadow: none !important;
}
[data-baseweb="select"] *       { color: #F0F2F8 !important; }
[data-baseweb="popover"]        { background:#13161D !important; border:1px solid #252A38 !important; border-radius:12px !important; }
[data-baseweb="menu"]           { background:#13161D !important; }
[data-baseweb="option"]:hover   { background:#191D27 !important; }
input[type="number"]            { color:#F0F2F8 !important; }

[data-testid="stNumberInput"] button {
    background: #191D27 !important;
    border: 1px solid #252A38 !important;
    border-radius: 8px !important;
    color: #7A8499 !important;
}
[data-testid="stNumberInput"] button:hover {
    background: #252A38 !important;
    color: #F97316 !important;
    border-color: #3D4557 !important;
}

/* ── Hint box ── */
.action-note {
    font-size:11px !important; color:#7A8499 !important;
    line-height:1.6 !important; margin-bottom:14px;
    padding:12px 14px; background:#191D27;
    border-radius:10px; border-left:2px solid #7C3A0A;
}

/* ── Analyse button ── */
[data-testid="stMain"] [data-testid="baseButton-secondary"] {
    background: #F97316 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: .02em !important;
    box-shadow: 0 8px 24px rgba(249,115,22,.3) !important;
    transition: opacity .2s, transform .15s !important;
}
[data-testid="stMain"] [data-testid="baseButton-secondary"]:hover {
    opacity: .88 !important;
    transform: translateY(-1px) !important;
}
[data-testid="stMain"] [data-testid="baseButton-secondary"] p {
    color: #fff !important;
    font-weight: 700 !important;
}

/* ── Result box ── */
.result-box {
    background: linear-gradient(135deg, #1A0E05 0%, #110D05 100%);
    border: 1px solid #7C3A0A;
    border-radius: 18px;
    padding: 24px 28px;
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 24px;
    position: relative;
    overflow: hidden;
}
.result-box::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 160px; height: 160px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(249,115,22,.12), transparent 70%);
    pointer-events: none;
}
.r-num  {
    font-size: 62px !important; font-weight: 800 !important;
    color: #F97316 !important; letter-spacing: -3px; line-height: 1;
    font-family: 'DM Mono', monospace !important;
}
.r-unit { font-size: 13px !important; color: #7A8499 !important; margin-top: 2px; }
.r-div  { width: 1px; background: #7C3A0A; align-self: stretch; flex-shrink: 0; }
.r-risk { font-size: 15px !important; font-weight: 700 !important; margin-bottom: 6px; letter-spacing:-.2px; }
.r-note { font-size: 12px !important; color: #7A8499 !important; line-height: 1.65 !important; }
.low    { color: #10B981 !important; }
.med    { color: #F59E0B !important; }
.hi     { color: #EF4444 !important; }

.risk-pill {
    display: inline-flex; align-items: center; gap: 6px;
    border-radius: 20px; padding: 4px 12px;
    font-size: 11px; font-weight: 700;
    margin-bottom: 8px; letter-spacing: .04em;
}
.pill-low { background: rgba(16,185,129,.12); color:#10B981 !important; border:1px solid rgba(16,185,129,.2); }
.pill-med { background: rgba(245,158,11,.12); color:#F59E0B !important; border:1px solid rgba(245,158,11,.2); }
.pill-hi  { background: rgba(239,68,68,.12);  color:#EF4444 !important; border:1px solid rgba(239,68,68,.2); }

/* ── Placeholder pages ── */
.placeholder {
    background: #13161D;
    border: 1px solid #252A38;
    border-radius: 18px;
    padding: 64px 32px;
    text-align: center;
    margin-top: 8px;
}
.ph-icon  { font-size: 36px; margin-bottom: 14px; opacity:.5; }
.ph-title { font-size: 20px !important; font-weight: 700 !important; color: #F0F2F8 !important; margin-bottom: 8px; letter-spacing:-.3px; }
.ph-sub   { font-size: 13px !important; color: #7A8499 !important; line-height: 1.65 !important; }

/* ── Statistik metric row ── */
.metric-row { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:16px; }
.metric-card {
    background: #13161D;
    border: 1px solid #252A38;
    border-radius: 14px;
    padding: 18px 20px;
}
.metric-label { font-size:9px !important; color:#7A8499 !important; letter-spacing:.1em; text-transform:uppercase; margin-bottom:8px; }
.metric-val   { font-size:26px !important; font-weight:800 !important; color:#F0F2F8 !important; letter-spacing:-0.8px; line-height:1; }
.metric-unit  { font-size:12px !important; color:#7A8499 !important; margin-left:2px; font-weight:400 !important; }

/* ── Guide steps ── */
.guide-step {
    background: #13161D;
    border: 1px solid #252A38;
    border-radius: 14px;
    padding: 18px 20px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 10px;
    transition: border-color .2s;
}
.guide-step:hover { border-color: #3D4557; }
.step-num {
    width: 34px; height: 34px; border-radius: 10px;
    background: #F97316;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 800; color: #fff; flex-shrink: 0;
}
.step-title { font-size:14px !important; font-weight:700 !important; color:#F0F2F8 !important; margin-bottom:4px; letter-spacing:-.2px; }
.step-desc  { font-size:13px !important; color:#7A8499 !important; line-height:1.6 !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:28px">
      <div class="brand-row">
        <div class="brand-icon"><div class="brand-icon-inner">♡</div></div>
        <div class="brand-name">MediPredict</div>
      </div>
      <div class="brand-sub">Clinical Decision Support</div>
    </div>
    <div class="nav-label">Menu Utama</div>
    """, unsafe_allow_html=True)

    pages = {
        "Estimasi LOS":    "🩺",
        "Riwayat":         "📋",
        "Statistik Model": "📊",
        "Panduan":         "📖",
    }
    for label, icon in pages.items():
        is_active = st.session_state.page == label
        active_style = (
            "background:rgba(249,115,22,.12) !important;"
            "color:#F97316 !important;"
            "font-weight:700 !important;"
            "border:1px solid rgba(249,115,22,.2) !important;"
            if is_active else ""
        )
        st.markdown(f"""
        <style>
        div[data-testid="stButton"]:has(button[aria-label="{label}"]) button {{
            {active_style}
        }}
        </style>
        """, unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=label, use_container_width=True):
            st.session_state.page = label
            st.rerun()

    st.markdown("""
    <div style="margin-top:28px; border-top:1px solid #252A38; padding-top:20px;">
      <div class="mini-stat">
        <div class="mini-stat-label">Akurasi Model</div>
        <div class="mini-stat-val">87.4<span class="mini-stat-unit">%</span></div>
        <div class="mini-stat-bar"><div class="mini-stat-fill"></div></div>
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


# ── Estimasi LOS ──────────────────────────────────────
if page == "Estimasi LOS":
    st.markdown("""
    <div class="crumb">Dashboard · Prediksi LOS</div>
    <div class="page-h">Estimasi Rawat Inap <em>DBD</em>
      <span class="topbadge"><span class="live-dot"></span>&nbsp;Stacking Regression</span>
    </div>
    <div class="page-sub">Input data klinis — model prediksi durasi perawatan otomatis.</div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.6], gap="medium")

    with col_left:
        st.markdown("""
        <div class="wcard">
          <div class="card-hdr">
            <div class="cdot cdot-orange"></div>
            <div class="card-ttl">Profil Pasien</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        input_jk    = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        input_umur  = st.number_input("Umur (Tahun)", min_value=1, max_value=100, value=25)
        input_demam = st.selectbox("Diagnosis", [
            "DD — Dengue Fever",
            "DBD — Hemorrhagic",
            "DSS — Shock Syndrome",
        ])

    with col_right:
        st.markdown("""
        <div class="wcard">
          <div class="card-hdr">
            <div class="cdot cdot-green"></div>
            <div class="card-ttl">Hasil Laboratorium</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        l1, l2, l3 = st.columns(3)
        with l1:
            input_hb = st.number_input("Hemoglobin (g/dL)", min_value=1.0, max_value=25.0, value=12.0, step=0.1)
        with l2:
            input_hct = st.number_input("Hematokrit (%)", min_value=10.0, max_value=65.0, value=40.0, step=0.1)
        with l3:
            input_trombo = st.number_input("Trombosit (/µL)", min_value=1000, max_value=500000, value=100000, step=1000)

        st.markdown("""
        <div class="action-note">
          Estimasi ± 1.5 hari. Gunakan sebagai referensi sekunder, bukan diagnosis klinis final.
        </div>
        """, unsafe_allow_html=True)
        proses = st.button("Analisis →")

    val_jk    = 0 if input_jk == "Laki-laki" else 1
    val_demam = 0 if "DD" in input_demam else (1 if "DBD" in input_demam else 2)

    if proses:
        try:
            model  = joblib.load("model_regresi_dbd.pkl")
            scaler = joblib.load("scaler_dbd.pkl")
            fitur  = pd.DataFrame(
                [[val_jk, input_umur, val_demam, input_hb, input_hct, input_trombo]],
                columns=["jenis_kelamin", "umur", "jenis_demam", "hemoglobin", "hct", "trombosit"]
            )
            hari = max(1, round(model.predict(scaler.transform(fitur))[0], 1))

            if hari <= 5:
                rc, rl, pill_class, pill_desc = (
                    "low", "Risiko Rendah", "pill-low",
                    "Rawat inap singkat diprediksi. Pantau trombosit harian dan pastikan hidrasi cukup."
                )
            elif hari <= 8:
                rc, rl, pill_class, pill_desc = (
                    "med", "Risiko Sedang", "pill-med",
                    "Monitoring intensif diperlukan. Pantau tanda perdarahan dan perubahan hematokrit."
                )
            else:
                rc, rl, pill_class, pill_desc = (
                    "hi", "Risiko Tinggi", "pill-hi",
                    "Perlu perhatian klinis ekstra. Pertimbangkan pemantauan ICU dan konsultasi spesialis."
                )

            st.markdown(f"""
            <div class="result-box">
              <div>
                <div class="r-num">{hari}</div>
                <div class="r-unit">hari rawat inap</div>
              </div>
              <div class="r-div"></div>
              <div>
                <div class="risk-pill {pill_class}">● {rl}</div>
                <div class="r-note">
                  Diprediksi Stacking Regression · margin ± 1.5 hari<br>
                  {pill_desc}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        except FileNotFoundError:
            st.error("⚠️  File model tidak ditemukan. Pastikan model_regresi_dbd.pkl dan scaler_dbd.pkl ada di direktori yang sama.")


# ── Riwayat ───────────────────────────────────────────
elif page == "Riwayat":
    st.markdown("""
    <div class="crumb">Dashboard · Riwayat</div>
    <div class="page-h">Riwayat <em>Prediksi</em></div>
    <div class="page-sub">Daftar prediksi yang telah dilakukan.</div>
    <div class="placeholder">
      <div class="ph-icon">📋</div>
      <div class="ph-title">Belum ada riwayat</div>
      <div class="ph-sub">Riwayat prediksi akan muncul di sini setelah analisis pertama dilakukan.</div>
    </div>
    """, unsafe_allow_html=True)


# ── Statistik Model ───────────────────────────────────
elif page == "Statistik Model":
    st.markdown("""
    <div class="crumb">Dashboard · Statistik</div>
    <div class="page-h">Statistik <em>Model</em></div>
    <div class="page-sub">Performa dan metrik evaluasi Stacking Regression.</div>
    <div class="metric-row">
      <div class="metric-card">
        <div class="metric-label">Akurasi</div>
        <div class="metric-val">87.4<span class="metric-unit">%</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-label">MAE</div>
        <div class="metric-val">1.32<span class="metric-unit">hari</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-label">RMSE</div>
        <div class="metric-val">1.87<span class="metric-unit">hari</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-label">R² Score</div>
        <div class="metric-val">0.81</div>
      </div>
    </div>
    <div class="placeholder">
      <div class="ph-icon">📊</div>
      <div class="ph-title">Visualisasi segera hadir</div>
      <div class="ph-sub">Grafik feature importance dan learning curve akan ditampilkan di sini.</div>
    </div>
    """, unsafe_allow_html=True)


# ── Panduan ───────────────────────────────────────────
elif page == "Panduan":
    st.markdown("""
    <div class="crumb">Dashboard · Panduan</div>
    <div class="page-h">Panduan <em>Penggunaan</em></div>
    <div class="page-sub">Cara menggunakan MediPredict dengan benar.</div>
    """, unsafe_allow_html=True)

    steps = [
        ("1", "Isi Profil Pasien",
         "Masukkan jenis kelamin, umur, dan diagnosis pasien pada kolom kiri."),
        ("2", "Input Hasil Lab",
         "Masukkan nilai hemoglobin, hematokrit, dan trombosit terkini."),
        ("3", "Klik Analisis",
         "Tekan tombol Analisis — model memproses data dan menghasilkan estimasi hari rawat."),
        ("4", "Baca Hasilnya",
         "Lihat estimasi hari dan kategori risiko: Rendah ≤5 hari, Sedang 6–8 hari, Tinggi >8 hari."),
    ]
    for num, title, desc in steps:
        st.markdown(f"""
        <div class="guide-step">
          <div class="step-num">{num}</div>
          <div>
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

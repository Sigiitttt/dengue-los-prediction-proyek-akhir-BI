import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="MediPredict · Estimasi LOS DBD",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
[data-testid="stHeader"]              { background: transparent !important; display: none !important; }
.main .block-container                { padding: 2rem 2.5rem !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.08) !important;
    border-right: 1px solid rgba(255,255,255,0.12) !important;
}
[data-testid="stSidebar"] > div { padding: 2rem 1.5rem !important; }

p, span, label, div { color: rgba(255,255,255,0.85) !important; }

/* sidebar custom */
.logo-wrap  { display:flex;align-items:center;gap:10px;margin-bottom:32px; }
.logo-icon  { width:38px;height:38px;border-radius:10px;background:#F97316;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0; }
.logo-name  { font-size:15px !important;font-weight:700 !important;color:#fff !important;letter-spacing:-0.3px; }
.logo-sub   { font-size:11px !important;color:rgba(255,255,255,0.45) !important;margin-top:1px; }
.nav-label  { font-size:10px !important;font-weight:700 !important;letter-spacing:.10em !important;text-transform:uppercase !important;color:rgba(255,255,255,0.30) !important;margin-bottom:8px;margin-top:24px; }
.nav-item   { display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:10px;font-size:13px !important;color:rgba(255,255,255,0.55) !important;margin-bottom:3px; }
.nav-item.active { background:rgba(255,255,255,0.14);color:#fff !important;font-weight:500 !important; }
.nav-dot    { width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,0.25);display:inline-block;flex-shrink:0; }
.nav-dot.orange { background:#F97316; }
.stat-block { padding-top:32px;display:flex;flex-direction:column;gap:8px; }
.stat-card-s{ background:rgba(255,255,255,0.09);border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:12px 14px; }
.stat-lbl   { font-size:10px !important;color:rgba(255,255,255,0.40) !important;margin-bottom:4px;letter-spacing:.03em; }
.stat-num   { font-size:22px !important;font-weight:700 !important;color:#fff !important;letter-spacing:-0.5px; }
.stat-unit  { font-size:11px !important;color:rgba(255,255,255,0.40) !important;margin-left:3px;font-weight:400 !important; }

/* ── Page header ── */
.page-breadcrumb { font-size:11px !important;color:rgba(255,255,255,0.35) !important;margin-bottom:6px;letter-spacing:.03em; }
.page-title      { font-size:26px !important;font-weight:700 !important;color:#fff !important;letter-spacing:-0.6px;line-height:1.2; }
.page-sub        { font-size:13px !important;color:rgba(255,255,255,0.45) !important;margin-top:5px;line-height:1.5;margin-bottom:28px; }

/* ── Glass card ── */
.glass {
    background:rgba(255,255,255,0.10);
    border:1px solid rgba(255,255,255,0.16);
    border-radius:18px;padding:20px 24px 6px;margin-bottom:4px;
}
.card-ttl {
    font-size:10.5px !important;font-weight:700 !important;
    letter-spacing:.09em !important;text-transform:uppercase !important;
    color:rgba(255,255,255,0.40) !important;
    display:flex;align-items:center;gap:8px;margin-bottom:14px;
}
.cdot         { width:6px;height:6px;border-radius:50%;display:inline-block;flex-shrink:0; }
.cdot-orange  { background:#F97316; }
.cdot-teal    { background:#34D399; }

/* ── Form elements ── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    font-size:11px !important;font-weight:500 !important;
    color:rgba(255,255,255,0.50) !important;margin-bottom:4px !important;letter-spacing:.02em !important;
}
[data-baseweb="select"] > div,
[data-baseweb="base-input"] {
    background:rgba(255,255,255,0.08) !important;
    border:1px solid rgba(255,255,255,0.15) !important;
    border-radius:10px !important;color:#fff !important;
    transition:border-color .18s,background .18s !important;
}
[data-baseweb="select"] > div:focus-within,
[data-baseweb="base-input"]:focus-within {
    border-color:rgba(255,255,255,0.45) !important;
    background:rgba(255,255,255,0.14) !important;box-shadow:none !important;
}
[data-baseweb="select"] *      { color:#fff !important; }
[data-baseweb="popover"]       { background:#0d7090 !important;border:1px solid rgba(255,255,255,0.15) !important;border-radius:12px !important; }
[data-baseweb="menu"]          { background:#0d7090 !important; }
[data-baseweb="option"]:hover  { background:rgba(255,255,255,0.12) !important; }
input[type="number"]           { color:#fff !important;background:transparent !important; }

[data-testid="stNumberInput"] button {
    background:rgba(255,255,255,0.08) !important;
    border:1px solid rgba(255,255,255,0.15) !important;
    border-radius:8px !important;color:rgba(255,255,255,0.6) !important;
}
[data-testid="stNumberInput"] button:hover {
    background:rgba(255,255,255,0.18) !important;color:#fff !important;
}

/* ── Footer note ── */
.footer-note {
    font-size:12px !important;color:rgba(255,255,255,0.32) !important;
    line-height:1.55 !important;margin-bottom:12px;
}

/* ── CTA button ── */
[data-testid="baseButton-secondary"] {
    background:#F97316 !important;border:none !important;
    border-radius:12px !important;padding:0.65rem 2rem !important;
    font-size:0.9rem !important;font-weight:700 !important;
    letter-spacing:-0.01em !important;white-space:nowrap !important;
    box-shadow:0 4px 18px rgba(249,115,22,0.35) !important;
    transition:opacity .2s,transform .15s !important;
}
[data-testid="baseButton-secondary"]:hover { opacity:.88 !important;transform:translateY(-1px) !important; }
[data-testid="baseButton-secondary"] p     { color:#fff !important;font-weight:700 !important; }

/* ── Result ── */
.result-box {
    background:rgba(249,115,22,0.12);
    border:1px solid rgba(249,115,22,0.28);
    border-radius:18px;padding:22px 26px;margin-top:16px;
    display:flex;align-items:center;gap:24px;
}
.result-num   { font-size:52px !important;font-weight:800 !important;color:#FED7AA !important;letter-spacing:-2px;line-height:1; }
.result-unit  { font-size:14px !important;color:rgba(255,255,255,0.40) !important;margin-top:2px; }
.result-vdiv  { width:1px;background:rgba(255,255,255,0.12);align-self:stretch;flex-shrink:0; }
.result-risk  { font-size:16px !important;font-weight:700 !important;margin-bottom:6px; }
.result-note-t{ font-size:12px !important;color:rgba(255,255,255,0.38) !important;line-height:1.55 !important; }
.risk-low     { color:#34D399 !important; }
.risk-med     { color:#FCD34D !important; }
.risk-hi      { color:#FCA5A5 !important; }

[data-testid="stAlert"] {
    background:rgba(220,50,50,0.15) !important;
    border:1px solid rgba(220,50,50,0.30) !important;
    border-radius:12px !important;margin-top:16px !important;
}
[data-testid="stAlert"] p { color:#FCA5A5 !important; }
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
    <div class="nav-item active"><span class="nav-dot orange"></span>Estimasi LOS</div>
    <div class="nav-item"><span class="nav-dot"></span>Riwayat Prediksi</div>
    <div class="nav-item"><span class="nav-dot"></span>Statistik Model</div>
    <div class="nav-item"><span class="nav-dot"></span>Panduan Penggunaan</div>

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
# KONTEN UTAMA
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="page-breadcrumb">Dashboard · Prediksi LOS</div>
<div class="page-title">Estimasi Rawat Inap DBD</div>
<div class="page-sub">Masukkan data klinis pasien untuk mendapatkan prediksi durasi perawatan secara otomatis.</div>
""", unsafe_allow_html=True)

# ── Card Profil Pasien ────────────────────────────────
st.markdown('<div class="glass"><div class="card-ttl"><span class="cdot cdot-orange"></span>Profil Pasien</div></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    input_jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
with c2:
    input_umur = st.number_input("Umur (Tahun)", min_value=1, max_value=100, value=25)
with c3:
    input_demam = st.selectbox(
        "Diagnosis",
        ["DD (Dengue Fever)", "DBD (Hemorrhagic)", "DSS (Shock Syndrome)"]
    )

# ── Card Hasil Lab ────────────────────────────────────
st.markdown('<div class="glass"><div class="card-ttl"><span class="cdot cdot-teal"></span>Hasil Laboratorium</div></div>', unsafe_allow_html=True)
l1, l2, l3 = st.columns(3)
with l1:
    input_hb = st.number_input("Hemoglobin (g/dL)", min_value=1.0, max_value=25.0, value=12.0, step=0.1)
with l2:
    input_hct = st.number_input("Hematokrit (%)", min_value=10.0, max_value=65.0, value=40.0, step=0.1)
with l3:
    input_trombo = st.number_input("Trombosit (/µL)", min_value=1000, max_value=500000, value=100000, step=1000)

# ── Footer note + tombol ──────────────────────────────
st.markdown("""
<div class="footer-note" style="margin-top:16px;">
  Hasil prediksi bersifat estimasi dengan margin ± 1.5 hari.
  Gunakan sebagai referensi sekunder, bukan diagnosis klinis final.
</div>
""", unsafe_allow_html=True)

proses = st.button("Proses Analisis →")


# ═══════════════════════════════════════════════════════
# LOGIKA PREDIKSI
# ═══════════════════════════════════════════════════════
val_jk    = 0 if input_jk == "Laki-laki" else 1
val_demam = 0 if input_demam.startswith("DD") else (1 if input_demam.startswith("DBD") else 2)

if proses:
    try:
        model  = joblib.load("model_regresi_dbd.pkl")
        scaler = joblib.load("scaler_dbd.pkl")

        fitur_input = pd.DataFrame(
            [[val_jk, input_umur, val_demam, input_hb, input_hct, input_trombo]],
            columns=["jenis_kelamin", "umur", "jenis_demam", "hemoglobin", "hct", "trombosit"]
        )
        prediksi_hari = max(1, round(model.predict(scaler.transform(fitur_input))[0], 1))

        if prediksi_hari <= 5:
            risk_label, risk_class = "Risiko Rendah", "risk-low"
        elif prediksi_hari <= 8:
            risk_label, risk_class = "Risiko Sedang",  "risk-med"
        else:
            risk_label, risk_class = "Risiko Tinggi",  "risk-hi"

        st.markdown(f"""
        <div class="result-box">
          <div>
            <div class="result-num">{prediksi_hari}</div>
            <div class="result-unit">hari</div>
          </div>
          <div class="result-vdiv"></div>
          <div>
            <div class="result-risk {risk_class}">{risk_label}</div>
            <div class="result-note-t">
              Diprediksi oleh Stacking Regression Model<br>
              berdasarkan parameter klinis yang dimasukkan.<br>
              Margin error ± 1.5 hari.
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("File model tidak ditemukan. Pastikan model_regresi_dbd.pkl "
                 "dan scaler_dbd.pkl ada di direktori yang sama dengan app.py.")

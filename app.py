import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Prediksi LOS DBD",
    layout="centered",
    initial_sidebar_state="collapsed"
)

custom_css = """
<style>
/* ── Background & container ─────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stBlockContainer"] {
    max-width: 720px !important;
    padding-top: 4rem !important;
    padding-bottom: 4rem !important;
}

/* ── Global font ─────────────────────────────────────────── */
p, span, label, h1, h2, h3, div, li {
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif !important;
}

/* ── Header ──────────────────────────────────────────────── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.10);
    border: 0.5px solid rgba(255,255,255,0.20);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    color: rgba(255,255,255,0.70);
    letter-spacing: 0.5px;
    margin-bottom: 14px;
}
.dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #34d399;
    display: inline-block;
    animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.35} }

.main-title {
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.04em !important;
    text-align: center !important;
    color: #FFFFFF !important;
    margin-bottom: 0.5rem !important;
    line-height: 1.1 !important;
}
.sub-title {
    font-size: 1rem !important;
    font-weight: 300 !important;
    color: rgba(255,255,255,0.45) !important;
    text-align: center !important;
    margin-bottom: 3rem !important;
    line-height: 1.6 !important;
}

/* ── Glass card wrapper ──────────────────────────────────── */
.glass-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 0.5px solid rgba(255,255,255,0.15);
    border-radius: 24px;
    padding: 2rem 2.2rem 2.4rem;
    box-shadow: 0 32px 64px rgba(0,0,0,0.35),
                inset 0 1px 0 rgba(255,255,255,0.10);
    margin-bottom: 0;
}

/* ── Section title ───────────────────────────────────────── */
.section-title {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.10em !important;
    text-transform: uppercase !important;
    color: rgba(255,255,255,0.35) !important;
    padding-bottom: 10px !important;
    border-bottom: 0.5px solid rgba(255,255,255,0.10) !important;
    margin-bottom: 1.2rem !important;
}

/* ── Form labels ─────────────────────────────────────────── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.55) !important;
    margin-bottom: 4px !important;
    letter-spacing: 0.01em !important;
}

/* ── Select & number input ───────────────────────────────── */
[data-baseweb="select"] > div,
[data-baseweb="base-input"] {
    background-color: rgba(255,255,255,0.07) !important;
    border: 0.5px solid rgba(255,255,255,0.18) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    transition: border-color 0.2s, background 0.2s !important;
}
[data-baseweb="select"] > div:hover,
[data-baseweb="base-input"]:hover {
    border-color: rgba(255,255,255,0.35) !important;
    background-color: rgba(255,255,255,0.11) !important;
}
[data-baseweb="select"] * { color: #FFFFFF !important; }
input[type="number"] {
    color: #FFFFFF !important;
    background: transparent !important;
}
[data-baseweb="popover"] { background: #2c2845 !important; }
[data-baseweb="menu"] { background: #2c2845 !important; }
[data-baseweb="option"] { background: #2c2845 !important; color: #fff !important; }
[data-baseweb="option"]:hover { background: rgba(255,255,255,0.10) !important; }

/* Stepper buttons ( +/- ) */
[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.09) !important;
    border: 0.5px solid rgba(255,255,255,0.18) !important;
    color: rgba(255,255,255,0.70) !important;
    border-radius: 8px !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(255,255,255,0.18) !important;
    color: #fff !important;
}

/* ── Divider ─────────────────────────────────────────────── */
.divider {
    height: 0.5px;
    background: rgba(255,255,255,0.09);
    margin: 1.8rem 0;
}

/* ── CTA button ──────────────────────────────────────────── */
[data-testid="baseButton-secondary"] {
    background: rgba(255,255,255,0.95) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.4rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: none !important;
}
[data-testid="baseButton-secondary"]:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
[data-testid="baseButton-secondary"] p {
    color: #1a1a2e !important;
    font-weight: 600 !important;
}

/* ── Result box ──────────────────────────────────────────── */
.result-box {
    background: rgba(52, 211, 153, 0.10);
    border: 0.5px solid rgba(52, 211, 153, 0.35);
    border-radius: 18px;
    padding: 2.2rem 2rem;
    text-align: center;
    margin-top: 1.8rem;
}
.result-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: rgba(52,211,153,0.70) !important;
    margin-bottom: 10px;
}
.result-value {
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    color: #34d399 !important;
    line-height: 1;
}
.result-note {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.38) !important;
    margin-top: 0.9rem;
    line-height: 1.55;
}

/* Error box */
[data-testid="stAlert"] {
    background: rgba(220,53,69,0.15) !important;
    border: 0.5px solid rgba(220,53,69,0.35) !important;
    border-radius: 12px !important;
    color: #ff8a94 !important;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-bottom:8px;">
  <span class="badge"><span class="dot"></span>&nbsp;Stacking Regression Model</span>
</div>
<div class="main-title">Estimasi Rawat Inap</div>
<div class="sub-title">
  Prediksi durasi perawatan klinis pasien demam berdarah<br>
  menggunakan arsitektur Stacking Regression.
</div>
""", unsafe_allow_html=True)

# ── Glass card open ───────────────────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-title">Profil Pasien</div>', unsafe_allow_html=True)
    input_jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    input_umur = st.number_input("Umur (Tahun)", min_value=1, max_value=100, value=25)
    input_demam = st.selectbox(
        "Diagnosis",
        ["DD (Dengue Fever)", "DBD (Hemorrhagic)", "DSS (Shock Syndrome)"]
    )

with col2:
    st.markdown('<div class="section-title">Hasil Laboratorium</div>', unsafe_allow_html=True)
    input_hb    = st.number_input("Hemoglobin (g/dL)", min_value=1.0,   max_value=25.0,  value=12.0,  step=0.1)
    input_hct   = st.number_input("Hematokrit (%)",    min_value=10.0,  max_value=65.0,  value=40.0,  step=0.1)
    input_trombo = st.number_input("Trombosit (/µL)",  min_value=1000,  max_value=500000, value=100000, step=1000)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Tombol ────────────────────────────────────────────────────────────────────
proses = st.button("Proses Analisis")

st.markdown('</div>', unsafe_allow_html=True)  # tutup glass-card

# ── Logic prediksi ────────────────────────────────────────────────────────────
val_jk = 0 if input_jk == "Laki-laki" else 1
val_demam = 0 if input_demam.startswith("DD") else (1 if input_demam.startswith("DBD") else 2)

if proses:
    try:
        model  = joblib.load('model_regresi_dbd.pkl')
        scaler = joblib.load('scaler_dbd.pkl')

        fitur_input = pd.DataFrame(
            [[val_jk, input_umur, val_demam, input_hb, input_hct, input_trombo]],
            columns=['jenis_kelamin', 'umur', 'jenis_demam', 'hemoglobin', 'hct', 'trombosit']
        )
        fitur_scaled = scaler.transform(fitur_input)
        prediksi_hari = max(1, round(model.predict(fitur_scaled)[0], 1))

        st.markdown(f"""
        <div class="result-box">
          <div class="result-label">Estimasi Lama Rawat Inap</div>
          <div class="result-value">{prediksi_hari} hari</div>
          <div class="result-note">
            Hasil diprediksi dengan margin of error (MAD) ± 1.5 hari.<br>
            Gunakan sebagai referensi sekunder, bukan diagnosis klinis.
          </div>
        </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("⚠️  File model atau scaler tidak ditemukan. Pastikan "
                 "'model_regresi_dbd.pkl' dan 'scaler_dbd.pkl' ada di direktori yang sama.")

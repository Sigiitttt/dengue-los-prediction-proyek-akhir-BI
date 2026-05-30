import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Estimasi Rawat Inap DBD",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #FDF6F0 !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stBlockContainer"] {
    max-width: 740px !important;
    padding-top: 3rem !important;
    padding-bottom: 4rem !important;
}
p, span, label, h1, h2, h3, h4, div, li {
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif !important;
}

/* ── Hero ── */
.chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: #FDE8F0; border: 1px solid #F4B8D0;
    border-radius: 20px; padding: 4px 13px;
    font-size: 11px; font-weight: 600;
    color: #C2547A; letter-spacing: 0.05em;
    margin-bottom: 14px;
}
.dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #E87FAB; display: inline-block;
    animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.hero-title {
    font-size: 2.4rem !important; font-weight: 700 !important;
    color: #2D2326 !important; letter-spacing: -0.04em !important;
    line-height: 1.15 !important; margin-bottom: 0.5rem !important;
}
.hero-title span { color: #D4698A !important; }
.hero-sub {
    font-size: 0.95rem !important; color: #9C8589 !important;
    line-height: 1.6 !important; margin-bottom: 2.5rem !important;
}

/* ── Panel cards ── */
.panel {
    border-radius: 20px; padding: 22px 22px 10px;
    margin-bottom: 0;
}
.panel-pink { background: #FEF0F5; border: 1px solid #F4C8D8; }
.panel-mint { background: #F0FAF5; border: 1px solid #C0E8D4; }

.panel-header {
    display: flex; align-items: center; gap: 9px; margin-bottom: 18px;
}
.panel-icon {
    width: 30px; height: 30px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px;
}
.icon-pink { background: #FAD6E4; }
.icon-mint { background: #C8EDD8; }
.panel-label {
    font-size: 10.5px !important; font-weight: 700 !important;
    letter-spacing: 0.10em !important; text-transform: uppercase !important;
}
.label-pink { color: #C2547A !important; }
.label-mint { color: #3A9668 !important; }

/* ── Streamlit form overrides ── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: #8A7070 !important;
    margin-bottom: 3px !important;
}
[data-baseweb="select"] > div,
[data-baseweb="base-input"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E8D8DE !important;
    border-radius: 10px !important;
    color: #2D2326 !important;
    transition: border-color .18s !important;
}
[data-baseweb="select"] > div:focus-within,
[data-baseweb="base-input"]:focus-within {
    border-color: #D4698A !important;
    box-shadow: none !important;
}
[data-baseweb="select"] * { color: #2D2326 !important; }
[data-baseweb="popover"], [data-baseweb="menu"] { background: #fff !important; }
[data-baseweb="option"]:hover { background: #FDE8F0 !important; }

[data-testid="stNumberInput"] button {
    background: #FDF0F4 !important;
    border: 1px solid #E8D8DE !important;
    border-radius: 8px !important;
    color: #C2547A !important;
}
[data-testid="stNumberInput"] button:hover {
    background: #F4C8D8 !important;
    color: #A0355A !important;
}

/* ── Bottom action bar ── */
.action-bar {
    background: #FFFFFF;
    border: 1px solid #F0E4E8;
    border-radius: 20px;
    padding: 18px 22px;
    display: flex; align-items: center; justify-content: space-between;
    gap: 16px; margin-top: 16px;
}
.action-note {
    font-size: 12px !important; color: #B09898 !important;
    line-height: 1.55 !important; max-width: 280px !important;
}

[data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, #E87FAB, #C8547A) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.8rem !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    transition: opacity .2s, transform .15s !important;
    box-shadow: 0 4px 16px rgba(200,84,122,0.25) !important;
}
[data-testid="baseButton-secondary"]:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
[data-testid="baseButton-secondary"] p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* ── Result ── */
.result-box {
    background: #FEF8E0;
    border: 1px solid #F0D870;
    border-radius: 20px;
    padding: 28px 24px;
    text-align: center;
    margin-top: 16px;
}
.result-tag {
    font-size: 10.5px !important; font-weight: 700 !important;
    letter-spacing: 0.10em !important; text-transform: uppercase !important;
    color: #B09020 !important; margin-bottom: 10px !important;
}
.result-num {
    font-size: 3rem !important; font-weight: 700 !important;
    color: #8A6C00 !important; letter-spacing: -0.05em !important;
    line-height: 1 !important;
}
.result-note {
    font-size: 0.85rem !important; color: #B09898 !important;
    margin-top: 10px !important; line-height: 1.55 !important;
}
.risk-low { color: #3A9668 !important; font-weight: 600 !important; }
.risk-med { color: #C28020 !important; font-weight: 600 !important; }
.risk-hi  { color: #C25050 !important; font-weight: 600 !important; }

.error-box {
    background: #FEF0F0; border: 1px solid #F4C0C0;
    border-radius: 14px; padding: 16px 20px; margin-top: 16px;
    font-size: 13px; color: #A03030;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:28px">
  <div class="chip"><span class="dot"></span>&nbsp;Stacking Regression · DBD</div>
  <div class="hero-title">Estimasi <span>Rawat Inap</span><br>Pasien DBD</div>
  <div class="hero-sub">Masukkan data klinis untuk mendapatkan prediksi<br>durasi perawatan secara otomatis.</div>
</div>
""", unsafe_allow_html=True)

# ── Form ──────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("""
    <div class="panel panel-pink">
      <div class="panel-header">
        <div class="panel-icon icon-pink">🧑</div>
        <span class="panel-label label-pink">Profil Pasien</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    input_jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    input_umur = st.number_input("Umur (Tahun)", min_value=1, max_value=100, value=25)
    input_demam = st.selectbox(
        "Diagnosis",
        ["DD (Dengue Fever)", "DBD (Hemorrhagic)", "DSS (Shock Syndrome)"]
    )

with col2:
    st.markdown("""
    <div class="panel panel-mint">
      <div class="panel-header">
        <div class="panel-icon icon-mint">🧪</div>
        <span class="panel-label label-mint">Hasil Laboratorium</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    input_hb     = st.number_input("Hemoglobin (g/dL)", min_value=1.0,  max_value=25.0,   value=12.0,   step=0.1)
    input_hct    = st.number_input("Hematokrit (%)",    min_value=10.0, max_value=65.0,   value=40.0,   step=0.1)
    input_trombo = st.number_input("Trombosit (/µL)",   min_value=1000, max_value=500000, value=100000, step=1000)

# ── Action bar ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="action-bar">
  <div class="action-note">Hasil bersifat estimasi dengan margin ± 1.5 hari.<br>Gunakan sebagai referensi sekunder, bukan diagnosis klinis.</div>
</div>
""", unsafe_allow_html=True)

proses = st.button("Proses Analisis →")

# ── Logic ─────────────────────────────────────────────────────────────────────
val_jk    = 0 if input_jk == "Laki-laki" else 1
val_demam = (0 if input_demam.startswith("DD")
             else 1 if input_demam.startswith("DBD")
             else 2)

if proses:
    try:
        model  = joblib.load("model_regresi_dbd.pkl")
        scaler = joblib.load("scaler_dbd.pkl")

        fitur_input = pd.DataFrame(
            [[val_jk, input_umur, val_demam, input_hb, input_hct, input_trombo]],
            columns=["jenis_kelamin", "umur", "jenis_demam", "hemoglobin", "hct", "trombosit"]
        )
        fitur_scaled  = scaler.transform(fitur_input)
        prediksi_hari = max(1, round(model.predict(fitur_scaled)[0], 1))

        if prediksi_hari <= 5:
            risk_label = "Risiko Rendah"
            risk_class = "risk-low"
        elif prediksi_hari <= 8:
            risk_label = "Risiko Sedang"
            risk_class = "risk-med"
        else:
            risk_label = "Risiko Tinggi"
            risk_class = "risk-hi"

        st.markdown(f"""
        <div class="result-box">
          <div class="result-tag">Estimasi Lama Rawat Inap</div>
          <div class="result-num">{prediksi_hari} hari</div>
          <div class="result-note">
            <span class="{risk_class}">{risk_label}</span>
            &nbsp;·&nbsp;Berdasarkan parameter klinis yang dimasukkan
          </div>
        </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.markdown("""
        <div class="error-box">
          ⚠️ File model tidak ditemukan. Pastikan <code>model_regresi_dbd.pkl</code>
          dan <code>scaler_dbd.pkl</code> ada di direktori yang sama dengan app.py.
        </div>
        """, unsafe_allow_html=True)

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
[data-testid="stAppViewContainer"] {
    background-color: #F5F5F7 !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stBlockContainer"] {
    max-width: 760px !important;
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
}

p, span, label, h1, h2, h3, h4, div, li {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    color: #1D1D1F !important;
}

.main-title {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    text-align: center;
    margin-bottom: 0.5rem;
}

.sub-title {
    font-size: 1.05rem;
    font-weight: 400;
    color: #86868B !important;
    text-align: center;
    margin-bottom: 3.5rem;
    line-height: 1.5;
}

.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1.2rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #D2D2D7;
}

[data-baseweb="select"] > div,
[data-baseweb="base-input"],
input[type="number"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D2D2D7 !important;
    border-radius: 8px !important;
    padding: 3px 8px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
}

[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="baseButton-secondary"] {
    background-color: #1D1D1F !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    border: none !important;
    width: 100% !important;
    margin-top: 1.5rem !important;
    transition: opacity 0.2s ease !important;
}

[data-testid="baseButton-secondary"]:hover {
    opacity: 0.8 !important;
}

[data-testid="baseButton-secondary"] p {
    color: #FFFFFF !important;
}

.result-box {
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    margin-top: 2.5rem;
    border: 1px solid #E5E5EA;
    box-shadow: 0 10px 30px rgba(0,0,0,0.04);
}

.result-text {
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}

.result-note {
    font-size: 0.95rem;
    color: #86868B !important;
    margin-top: 1rem;
    line-height: 1.5;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

header_html = (
    '<div class="main-title">Estimasi Rawat Inap</div>'
    '<div class="sub-title">Prediksi durasi perawatan klinis pasien demam '
    'berdarah menggunakan arsitektur Stacking Regression.</div>'
)
st.markdown(header_html, unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-title">Profil Pasien</div>', unsafe_allow_html=True)
    
    input_jk = st.selectbox(
        "Jenis Kelamin", 
        ["Laki-laki", "Perempuan"]
    )
    
    input_umur = st.number_input(
        "Umur (Tahun)", 
        min_value=1, max_value=100, value=25
    )
    
    input_demam = st.selectbox(
        "Diagnosis", 
        ["DD (Dengue Fever)", "DBD (Hemorrhagic)", "DSS (Shock Syndrome)"]
    )

with col2:
    st.markdown('<div class="section-title">Laboratorium</div>', unsafe_allow_html=True)
    
    input_hb = st.number_input(
        "Hemoglobin (g/dL)", 
        min_value=1.0, max_value=25.0, value=12.0, step=0.1
    )
    
    input_hct = st.number_input(
        "Hematokrit (%)", 
        min_value=10.0, max_value=65.0, value=40.0, step=0.1
    )
    
    input_trombo = st.number_input(
        "Trombosit (/µL)", 
        min_value=1000, max_value=500000, value=100000, step=1000
    )

val_jk = 0 if input_jk == "Laki-laki" else 1

if input_demam.startswith("DD"):
    val_demam = 0
elif input_demam.startswith("DBD"):
    val_demam = 1
else:
    val_demam = 2

if st.button("Proses Analisis"):
    try:
        model = joblib.load('model_regresi_dbd.pkl')
        scaler = joblib.load('scaler_dbd.pkl')
        
        fitur_input = pd.DataFrame(
            [[val_jk, input_umur, val_demam, input_hb, input_hct, input_trombo]], 
            columns=['jenis_kelamin', 'umur', 'jenis_demam', 'hemoglobin', 'hct', 'trombosit']
        )
        
        fitur_scaled = scaler.transform(fitur_input)
        
        prediksi = model.predict(fitur_scaled)[0]
        prediksi_hari = max(1, round(prediksi, 1))
        
        result_html = (
            '<div class="result-box">'
            f'<div class="result-text">Estimasi: {prediksi_hari} Hari</div>'
            '<div class="result-note">Hasil diprediksi dengan margin of error '
            '(MAD) ± 1.5 hari. Gunakan sebagai referensi sekunder.</div>'
            '</div>'
        )
        st.markdown(result_html, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error("Sistem tidak menemukan file model atau scaler.")

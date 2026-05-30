import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Prediksi LOS DBD",
    layout="centered"
)

custom_css = """
<style>
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #1d1d1f;
    background-color: #ffffff;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.main-title {
    font-size: 2.5rem;
    font-weight: 600;
    letter-spacing: -0.015em;
    text-align: center;
    margin-bottom: 0.5rem;
    margin-top: 1rem;
}

.sub-title {
    font-size: 1.1rem;
    font-weight: 400;
    color: #86868b;
    text-align: center;
    margin-bottom: 3.5rem;
    line-height: 1.5;
}

.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1d1d1f;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid #d2d2d7;
    padding-bottom: 0.5rem;
}

div[data-baseweb="select"] > div, input[type="number"] {
    border-radius: 12px !important;
    background-color: #fbfbfd !important;
    border: 1px solid #d2d2d7 !important;
    padding: 2px;
}

.stButton > button {
    background-color: #0071e3;
    color: white;
    border-radius: 980px;
    padding: 14px 24px;
    font-weight: 500;
    font-size: 17px;
    border: none;
    width: 100%;
    transition: background-color 0.3s ease;
    margin-top: 1rem;
}

.stButton > button:hover {
    background-color: #0077ed;
}

.result-box {
    background-color: #fbfbfd;
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    margin-top: 2.5rem;
    border: 1px solid #d2d2d7;
}

.result-text {
    font-size: 2.2rem;
    font-weight: 600;
    color: #1d1d1f;
    letter-spacing: -0.01em;
}

.result-note {
    font-size: 0.95rem;
    color: #86868b;
    margin-top: 0.8rem;
    line-height: 1.4;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

header_html = """
<div class="main-title">Estimasi Rawat Inap</div>
<div class="sub-title">Prediksi durasi perawatan klinis pasien demam berdarah menggunakan 
arsitektur Stacking Regression.</div>
"""
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
    st.markdown('<div class="section-title">Hasil Laboratorium</div>', unsafe_allow_html=True)
    
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
        
        result_html = f"""
        <div class="result-box">
            <div class="result-text">Estimasi: {prediksi_hari} Hari</div>
            <div class="result-note">Hasil diprediksi dengan margin of error (MAD) ± 1.5 hari. 
            Gunakan sebagai referensi sekunder.</div>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error("Sistem tidak dapat menemukan file model atau scaler.")

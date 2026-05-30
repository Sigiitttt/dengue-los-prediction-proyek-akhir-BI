import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Prediksi LOS DBD", 
    layout="centered"
)

st.markdown("""
<style>
.main-title {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
}
.sub-title {
    font-family: 'Georgia', serif;
    font-size: 1.1rem;
    color: #4a4a4a;
    margin-bottom: 2.5rem;
    line-height: 1.6;
}
.result-box {
    background-color: #f8f9fa;
    border-left: 4px solid #2c3e50;
    padding: 1.5rem;
    margin-top: 2rem;
}
.result-text {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 1.4rem;
    font-weight: bold;
    color: #2c3e50;
}
.result-note {
    font-family: 'Georgia', serif;
    font-size: 0.95rem;
    color: #6c757d;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Estimasi Lama Rawat Inap Pasien DBD</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sistem prediksi klinis berbasis Stacking Ensemble Regression untuk memperkirakan durasi perawatan pasien berdasarkan indikator vital dan hasil laboratorium awal.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Profil Pasien**")
    input_jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    input_umur = st.number_input("Umur (Tahun)", min_value=1, max_value=100, value=25)
    input_demam = st.selectbox("Diagnosis Demam", ["DD (Dengue Fever)", "DBD (Dengue Hemorrhagic Fever)", "DSS (Dengue Shock Syndrome)"])

with col2:
    st.markdown("**Indikator Laboratorium**")
    input_hb = st.number_input("Hemoglobin (g/dL)", min_value=1.0, max_value=25.0, value=12.0, step=0.1)
    input_hct = st.number_input("Hematokrit (%)", min_value=10.0, max_value=65.0, value=40.0, step=0.1)
    input_trombo = st.number_input("Trombosit (/µL)", min_value=1000, max_value=500000, value=100000, step=1000)

val_jk = 0 if input_jk == "Laki-laki" else 1

if input_demam.startswith("DD"):
    val_demam = 0
elif input_demam.startswith("DBD"):
    val_demam = 1
else:
    val_demam = 2

if st.button("Proses Prediksi"):
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
        
        st.markdown(f'<div class="result-box"><div class="result-text">Estimasi Waktu Perawatan: {prediksi_hari} Hari</div><div class="result-note">Catatan: Hasil prediksi ini memiliki margin error (MAD) sekitar 1.5 hari dan ditujukan sebagai alat bantu pengambilan keputusan sekunder bagi tenaga medis.</div></div>', unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error("File model atau scaler tidak ditemukan di dalam folder.")

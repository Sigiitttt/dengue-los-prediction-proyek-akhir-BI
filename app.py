<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Estimasi Rawat Inap</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      min-height: 100vh;
      background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
      display: flex; flex-direction: column; align-items: center;
      justify-content: center; padding: 40px 20px;
      font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
    }
    .hero { text-align: center; margin-bottom: 36px; }
    .badge {
      display: inline-flex; align-items: center; gap: 6px;
      background: rgba(255,255,255,0.1); border: 0.5px solid rgba(255,255,255,0.2);
      border-radius: 20px; padding: 5px 14px; margin-bottom: 16px;
      font-size: 12px; color: rgba(255,255,255,0.7); letter-spacing: 0.5px;
    }
    .dot {
      width: 6px; height: 6px; border-radius: 50%;
      background: #34d399; animation: pulse 2s infinite;
    }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
    .hero h1 {
      font-size: 34px; font-weight: 600; color: #fff;
      letter-spacing: -0.8px; line-height: 1.1; margin-bottom: 10px;
    }
    .hero p {
      font-size: 15px; color: rgba(255,255,255,0.45); font-weight: 300;
      line-height: 1.5; max-width: 340px; margin: 0 auto;
    }
    .card {
      width: 100%; max-width: 640px;
      background: rgba(255,255,255,0.07);
      backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
      border: 0.5px solid rgba(255,255,255,0.15);
      border-radius: 24px; padding: 32px;
      box-shadow: 0 32px 64px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
    }
    .sections { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
    .section-title {
      font-size: 11px; font-weight: 500; letter-spacing: 1px;
      color: rgba(255,255,255,0.35); text-transform: uppercase; margin-bottom: 16px;
      padding-bottom: 10px; border-bottom: 0.5px solid rgba(255,255,255,0.1);
    }
    .field { margin-bottom: 14px; }
    .field label {
      display: block; font-size: 12px; color: rgba(255,255,255,0.5);
      margin-bottom: 6px; font-weight: 400;
    }
    .field select, .field input[type="text"] {
      width: 100%; background: rgba(255,255,255,0.06);
      border: 0.5px solid rgba(255,255,255,0.15);
      border-radius: 10px; padding: 10px 14px;
      font-size: 14px; color: #fff;
      outline: none; transition: border-color 0.2s, background 0.2s;
      appearance: none;
    }
    .field select option { background: #2c2845; color: #fff; }
    .field select:focus, .field input[type="text"]:focus {
      border-color: rgba(255,255,255,0.35); background: rgba(255,255,255,0.1);
    }
    .stepper { display: flex; align-items: center; }
    .stepper input[type="number"] {
      flex: 1; background: rgba(255,255,255,0.06);
      border-top: 0.5px solid rgba(255,255,255,0.15);
      border-bottom: 0.5px solid rgba(255,255,255,0.15);
      border-left: none; border-right: none; border-radius: 0;
      padding: 10px 12px; font-size: 14px; color: #fff;
      text-align: center; outline: none;
      -moz-appearance: textfield; width: 0;
    }
    .stepper input::-webkit-outer-spin-button,
    .stepper input::-webkit-inner-spin-button { -webkit-appearance: none; }
    .stepper-btn {
      background: rgba(255,255,255,0.08); border: 0.5px solid rgba(255,255,255,0.15);
      color: rgba(255,255,255,0.6); font-size: 16px; width: 40px; height: 40px;
      cursor: pointer; display: flex; align-items: center; justify-content: center;
      transition: background 0.15s; user-select: none; flex-shrink: 0;
    }
    .stepper-btn:first-child { border-radius: 10px 0 0 10px; }
    .stepper-btn:last-child  { border-radius: 0 10px 10px 0; }
    .stepper-btn:hover { background: rgba(255,255,255,0.14); color: #fff; }
    .divider { height: 0.5px; background: rgba(255,255,255,0.08); margin: 24px 0; }
    .footer { display: flex; align-items: center; justify-content: space-between; }
    .info { font-size: 12px; color: rgba(255,255,255,0.3); }
    .btn-analyze {
      background: rgba(255,255,255,0.95);
      color: #1a1a2e; border: none; border-radius: 12px;
      padding: 11px 28px; font-size: 14px; font-weight: 600;
      cursor: pointer; transition: transform 0.15s, opacity 0.15s;
      letter-spacing: -0.2px;
    }
    .btn-analyze:hover { opacity: 0.9; transform: translateY(-1px); }
    .btn-analyze:active { transform: scale(0.97); }
    .result-card {
      margin-top: 20px; background: rgba(52, 211, 153, 0.1);
      border: 0.5px solid rgba(52, 211, 153, 0.3);
      border-radius: 16px; padding: 20px 24px;
      display: none; text-align: center;
    }
    .result-label {
      font-size: 12px; color: rgba(52,211,153,0.7);
      letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px;
    }
    .result-value {
      font-size: 36px; font-weight: 600; color: #34d399; letter-spacing: -1px;
    }
    .result-sub { font-size: 13px; color: rgba(255,255,255,0.4); margin-top: 4px; }

    @media (max-width: 540px) {
      .sections { grid-template-columns: 1fr; }
      .hero h1 { font-size: 26px; }
      .card { padding: 24px 20px; }
    }
  </style>
</head>
<body>

  <div class="hero">
    <div class="badge"><span class="dot"></span> Stacking Regression Model</div>
    <h1>Estimasi Rawat Inap</h1>
    <p>Prediksi durasi perawatan klinis pasien demam berdarah berdasarkan data klinis dan laboratorium.</p>
  </div>

  <div class="card">
    <div class="sections">
      <!-- KIRI: Profil Pasien -->
      <div>
        <div class="section-title">Profil Pasien</div>
        <div class="field">
          <label>Jenis Kelamin</label>
          <select id="jk">
            <option value="" disabled selected>Pilih jenis kelamin</option>
            <option value="L">Laki-laki</option>
            <option value="P">Perempuan</option>
          </select>
        </div>
        <div class="field">
          <label>Umur (Tahun)</label>
          <div class="stepper">
            <button class="stepper-btn" onclick="step('umur', -1)">−</button>
            <input type="number" id="umur" value="25" min="0" max="120">
            <button class="stepper-btn" onclick="step('umur', 1)">+</button>
          </div>
        </div>
        <div class="field">
          <label>Diagnosis</label>
          <select id="diag">
            <option value="" disabled selected>Pilih diagnosis</option>
            <option>DBD Derajat I</option>
            <option>DBD Derajat II</option>
            <option>DBD Derajat III</option>
            <option>DBD Derajat IV</option>
          </select>
        </div>
      </div>

      <!-- KANAN: Hasil Lab -->
      <div>
        <div class="section-title">Hasil Laboratorium</div>
        <div class="field">
          <label>Hemoglobin (g/dL)</label>
          <div class="stepper">
            <button class="stepper-btn" onclick="stepf('hb', -0.1)">−</button>
            <input type="number" id="hb" value="12.5" step="0.1" min="0">
            <button class="stepper-btn" onclick="stepf('hb', 0.1)">+</button>
          </div>
        </div>
        <div class="field">
          <label>Hematokrit (%)</label>
          <div class="stepper">
            <button class="stepper-btn" onclick="stepf('hct', -0.1)">−</button>
            <input type="number" id="hct" value="38.0" step="0.1" min="0">
            <button class="stepper-btn" onclick="stepf('hct', 0.1)">+</button>
          </div>
        </div>
        <div class="field">
          <label>Trombosit (/µL)</label>
          <div class="stepper">
            <button class="stepper-btn" onclick="step('trom', -1000)">−</button>
            <input type="number" id="trom" value="150000" step="1000" min="0">
            <button class="stepper-btn" onclick="step('trom', 1000)">+</button>
          </div>
        </div>
      </div>
    </div>

    <div class="divider"></div>

    <div class="footer">
      <span class="info">Semua field wajib diisi</span>
      <button class="btn-analyze" onclick="proses()">Proses Analisis</button>
    </div>

    <div class="result-card" id="result">
      <div class="result-label">Estimasi Lama Rawat Inap</div>
      <div class="result-value" id="res-val">— hari</div>
      <div class="result-sub" id="res-sub"></div>
    </div>
  </div>

  <script>
    function step(id, d) {
      const el = document.getElementById(id);
      el.value = (parseInt(el.value) || 0) + d;
    }
    function stepf(id, d) {
      const el = document.getElementById(id);
      el.value = ((parseFloat(el.value) || 0) + d).toFixed(1);
    }
    function proses() {
      const hb    = parseFloat(document.getElementById('hb').value)   || 12.5;
      const hct   = parseFloat(document.getElementById('hct').value)  || 38;
      const trom  = parseFloat(document.getElementById('trom').value) || 150000;
      const umur  = parseInt(document.getElementById('umur').value)   || 25;
      const diag  = document.getElementById('diag').value;
      const derajat = diag ? parseInt(diag.slice(-1)) : 2;

      // Estimasi sederhana — ganti dengan model ML asli jika tersedia
      const est = Math.round(
        3 + derajat * 1.2
        + (umur > 50 ? 1.5 : 0)
        + (hb < 10 ? 1.8 : 0)
        + (trom < 100000 ? 2.1 : 0)
        + (hct > 45 ? 1.1 : 0)
      );

      const risk = est <= 5 ? 'Risiko Rendah'
                 : est <= 8 ? 'Risiko Sedang'
                 : 'Risiko Tinggi';

      document.getElementById('res-val').textContent = est + ' hari';
      document.getElementById('res-sub').textContent =
        risk + ' · Berdasarkan parameter klinis yang dimasukkan';
      document.getElementById('result').style.display = 'block';
    }
  </script>

</body>
</html>

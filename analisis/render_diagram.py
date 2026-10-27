import subprocess
from pathlib import Path

html_content = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #0b0f19;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #e2e8f0;
    width: 1600px;
    height: 1050px;
    padding: 40px;
    overflow: hidden;
  }

  /* Header */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #1e293b;
    padding-bottom: 20px;
    margin-bottom: 30px;
  }
  .title-box h1 {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 0.5px;
    color: #f8fafc;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .badge-case {
    background: #e11d48;
    color: #fff;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 700;
    text-transform: uppercase;
  }
  .subtitle {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 6px;
  }
  .unit-tag {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 13px;
    color: #38bdf8;
    font-weight: 600;
  }

  /* Grid Layout */
  .main-grid {
    display: grid;
    grid-template-columns: 360px 400px 400px 320px;
    gap: 24px;
    height: 720px;
  }

  .col {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  /* Cards */
  .card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 18px;
    position: relative;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding-bottom: 10px;
    margin-bottom: 12px;
    border-bottom: 1px solid #1f2937;
  }

  /* Border Themes */
  .theme-victim { border-left: 4px solid #ef4444; }
  .theme-victim .card-header { color: #f87171; }

  .theme-malware { border-left: 4px solid #f59e0b; }
  .theme-malware .card-header { color: #fbbf24; }

  .theme-hardware { border-left: 4px solid #06b6d4; }
  .theme-hardware .card-header { color: #22d3ee; }

  .theme-money { border-left: 4px solid #a855f7; }
  .theme-money .card-header { color: #c084fc; }

  .theme-action { border-left: 4px solid #10b981; }
  .theme-action .card-header { color: #34d399; }

  /* Card Content Styles */
  .highlight-title {
    font-size: 17px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 4px;
  }
  .meta-row {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    padding: 5px 0;
    border-bottom: 1px dashed #1e293b;
  }
  .meta-label { color: #64748b; }
  .meta-val { font-weight: 600; color: #cbd5e1; }
  .meta-val.danger { color: #f87171; font-weight: 700; }
  .meta-val.success { color: #34d399; font-weight: 700; }
  .meta-val.code { font-family: monospace; color: #38bdf8; background: #0f172a; padding: 2px 6px; border-radius: 4px; }

  /* Flow arrows indicator */
  .flow-indicator {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  .flow-indicator span {
    background: #1e293b;
    color: #94a3b8;
    padding: 2px 8px;
    border-radius: 10px;
  }

  /* Target Kunci Box */
  .gold-box {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.1));
    border: 1px solid #059669;
    border-radius: 8px;
    padding: 12px;
    margin-top: 10px;
  }
  .gold-box h4 {
    font-size: 12px;
    color: #34d399;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 6px;
  }

  /* List steps */
  .step-item {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
  }
  .step-num {
    width: 24px;
    height: 24px;
    background: #0284c7;
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    flex-shrink: 0;
  }
  .step-num.green { background: #059669; }
  .step-num.amber { background: #d97706; }
  .step-num.rose { background: #e11d48; }
  .step-text h5 { font-size: 13px; color: #f1f5f9; font-weight: 700; }
  .step-text p { font-size: 11px; color: #94a3b8; margin-top: 2px; }

  /* Footer / Key takeaway */
  .footer-bar {
    position: absolute;
    bottom: 25px;
    left: 40px;
    right: 40px;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 13px;
  }
</style>
</head>
<body>

  <!-- HEADER -->
  <div class="header">
    <div class="title-box">
      <h1>
        <span class="badge-case">ANALISIS KASUS</span>
        SINDIKAT PASSOBIS ENREKANG - MALWARE APK IKD
      </h1>
      <div class="subtitle">Rekonstruksi Keterkaitan Vektor Serangan, Hardware IMEI, Pool Kartu SIM & Aliran Dana Perbankan</div>
    </div>
    <div class="unit-tag">
      SUBDIT II FISMONDEV DITRESKRIMSUS POLDA SULSEL
    </div>
  </div>

  <!-- MAIN 4-COLUMN WORKFLOW -->
  <div class="main-grid">

    <!-- KOLOM 1: KORBAN & MODUS -->
    <div class="col">
      <div class="card theme-victim">
        <div class="card-header">
          <span>1. Profil Korban</span>
          <span style="color:#ef4444;">Target</span>
        </div>
        <div class="highlight-title">Bachri Sudda</div>
        <div style="font-size:12px; color:#94a3b8; margin-bottom:10px;">Penerima telp: Habibi (Anak Korban)</div>
        
        <div class="meta-row">
          <span class="meta-label">Rekening</span>
          <span class="meta-val code">BRI 008201000759568</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Total Kerugian</span>
          <span class="meta-val danger">Rp 249.900.000</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Sisa Saldo</span>
          <span class="meta-val">Rp 103.851</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Status App</span>
          <span class="meta-val" style="font-size:11px;">Belum pernah aktivasi BRImo</span>
        </div>
      </div>

      <div class="card theme-malware">
        <div class="card-header">
          <span>2. Vektor Serangan</span>
          <span style="color:#fbbf24;">Rekayasa Sosial</span>
        </div>
        <div class="highlight-title" style="font-size:15px; color:#fbbf24;">Sosialisasi Palsu IKD</div>
        <p style="font-size:12px; color:#cbd5e1; margin-top:4px; line-height:1.4;">
          Pelaku mengaku pegawai Dukcapil/Kecamatan dengan dalih aktivasi KTP Digital gagal.
        </p>

        <div style="margin-top:12px; background:#1e1b4b; border:1px solid #4338ca; padding:10px; border-radius:6px;">
          <div style="font-size:11px; font-weight:700; color:#a5b4fc; text-transform:uppercase;">Payload Trojan:</div>
          <div style="font-size:11px; color:#e0e7ff; margin-top:4px;">
            • Intersepsi SMS OTP & Notifikasi<br>
            • Curi data KTP & Ibu Kandung<br>
            • Registrasi liar & Takeover akun BRImo
          </div>
        </div>
      </div>
    </div>

    <!-- KOLOM 2: HARDWARE & EKSEKUSI -->
    <div class="col">
      <div class="card theme-hardware">
        <div class="card-header">
          <span>3. Perangkat Utama Eksekutor</span>
          <span style="color:#22d3ee;">Unit A</span>
        </div>
        <div class="highlight-title">Redmi A7 Pro</div>
        <div style="font-size:11px; color:#64748b; margin-bottom:8px;">Model: 25128RN17Y | TAC: 86077808</div>

        <div class="meta-row">
          <span class="meta-label">IMEI 1 / 2</span>
          <span class="meta-val code">860778085873297 / 290</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Nomor Hubungi Korban</span>
          <span class="meta-val danger" style="font-size:13px;">0852-8613-5512</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Nomor Pasangan</span>
          <span class="meta-val">0821-4637-098</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Cross SIM Card</span>
          <span class="meta-val" style="color:#fbbf24;">0852-1803-2439 (Dari Unit B)</span>
        </div>
      </div>

      <div class="card theme-hardware">
        <div class="card-header">
          <span>4. Perangkat Pendukung / Pool</span>
          <span style="color:#38bdf8;">Unit B</span>
        </div>
        <div class="highlight-title">Redmi A7 Pro (Kembar)</div>
        <div style="font-size:11px; color:#64748b; margin-bottom:8px;">Model: 25128RN17Y | TAC: 86077808</div>

        <div class="meta-row">
          <span class="meta-label">IMEI 1 / 2</span>
          <span class="meta-val code">860778087058137 / 130</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Nomor Aktif Terakhir</span>
          <span class="meta-val">0852-1803-2439</span>
        </div>

        <div class="gold-box">
          <h4>Kunci Identitas Non-Burner</h4>
          <div style="font-size:14px; font-weight:800; color:#34d399;">0851-7898-5913 (by.U)</div>
          <div style="font-size:11px; color:#a7f3d0; margin-top:2px;">
            Aktivasi digital mandiri via aplikasi. Wajib NIK & KK Asli pemilik.
          </div>
        </div>
      </div>
    </div>

    <!-- KOLOM 3: BUKTI SINDIKAT & ALIRAN DANA -->
    <div class="col">
      <div class="card theme-money">
        <div class="card-header">
          <span>5. Bukti Fisik Satu Sindikat</span>
          <span style="color:#c084fc;">SIM Pool</span>
        </div>
        <div style="font-size:13px; font-weight:700; color:#f8fafc; margin-bottom:6px;">Nomor Berurutan Segel Boks:</div>
        
        <div style="background:#0f172a; padding:10px; border-radius:6px; font-family:monospace; font-size:11px; line-height:1.6; color:#93c5fd;">
          • Seri 7227: 0813-7227-819 / 820 / 830<br>
          • Seri 7228: 0813-7228-089 (Unit B)<br>
          • Seri 7228: 0813-7228-090 (Unit A)<br>
          • Seri 8613: 0852-8613-1272 / 1646 / 1956
        </div>
        <p style="font-size:11px; color:#a855f7; margin-top:6px; font-weight:600;">
          Kesimpulan: Pengadaan kartu perdana borongan dalam 1 boks di konter yang sama.
        </p>
      </div>

      <div class="card theme-money">
        <div class="card-header">
          <span>6. Aliran Dana (Follow The Money)</span>
          <span style="color:#ec4899;">Rek Penampung</span>
        </div>

        <div style="margin-bottom:10px;">
          <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:700;">
            <span style="color:#f472b6;">Layer 1: Bank MNC</span>
            <span style="color:#f87171;">Rp 100.000.000</span>
          </div>
          <div style="font-size:11px; color:#cbd5e1; margin-top:2px;">
            a.n. <strong style="color:#fff;">Septian Egi Saputra</strong>
          </div>
        </div>

        <div>
          <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:700;">
            <span style="color:#f472b6;">Layer 2: Bank BCA (2x Tf)</span>
            <span style="color:#f87171;">Rp 149.900.000</span>
          </div>
          <div style="font-size:11px; color:#cbd5e1; margin-top:2px;">
            a.n. <strong style="color:#fff;">Yandi Rizki Maulana</strong>
          </div>
        </div>
      </div>
    </div>

    <!-- KOLOM 4: LANGKAH TAKTIS PENYIDIKAN -->
    <div class="col">
      <div class="card theme-action" style="height:100%;">
        <div class="card-header">
          <span>7. Action Plan Lidik / Sidik</span>
          <span style="color:#34d399;">Prioritas</span>
        </div>

        <div class="step-item">
          <div class="step-num">1</div>
          <div class="step-text">
            <h5>Lacak Outlet ID</h5>
            <p>Minta Telkomsel periksa kode ID konter penjual nomor boks segel seri 7227 / 7228.</p>
          </div>
        </div>

        <div class="step-item">
          <div class="step-num green">2</div>
          <div class="step-text">
            <h5>KYC Telkomsel by.U</h5>
            <p>Tarik data NIK/KK pendaftaran nomor <strong>0851-7898-5913</strong> untuk identitas nyata pelaku.</p>
          </div>
        </div>

        <div class="step-item">
          <div class="step-num amber">3</div>
          <div class="step-text">
            <h5>Dump BTS / Cell ID</h5>
            <p>Geolokasi koordinat last-seen BTS Unit A & B saat jam eksekusi di Enrekang / Sidrap.</p>
          </div>
        </div>

        <div class="step-item">
          <div class="step-num rose">4</div>
          <div class="step-text">
            <h5>Blokir & CCTV ATM</h5>
            <p>Freeze rekening MNC & BCA via IASC OJK + tarik rekaman CCTV ATM penarikan tunai.</p>
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- FOOTER BAR -->
  <div class="footer-bar">
    <div>
      <span style="color:#64748b;">Target Sasaran:</span>
      <span style="color:#f1f5f9; font-weight:700; margin-left:8px;">Sindikat Passobis / Malware Modus IKD Wilayah Enrekang - Sidrap</span>
    </div>
    <div style="color:#94a3b8; font-size:12px;">
      Dokumen Resmi Subdit II Fismondev Ditreskrimsus Polda Sulsel
    </div>
  </div>

</body>
</html>
"""

html_path = Path("/home/ubuntu/penyidikan/analisis/diagram_passobis_enrekang_clear.html")
png_path = Path("/home/ubuntu/penyidikan/analisis/diagram_passobis_enrekang_clear.png")

html_path.write_text(html_content, encoding="utf-8")

# Render via Google Chrome headless
cmd = [
    "/usr/bin/google-chrome",
    "--headless",
    "--disable-gpu",
    "--window-size=1600,1050",
    f"--screenshot={png_path}",
    str(html_path)
]
subprocess.run(cmd, check=True)
print(f"Generated: {png_path}")

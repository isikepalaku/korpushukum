import subprocess
from pathlib import Path

html_content = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Papan Keterkaitan Investigasi Sindikat Passobis Toraja-Enrekang-Makassar</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #070b14;
    background-image: 
      radial-gradient(rgba(37, 99, 235, 0.18) 1.2px, transparent 1.2px),
      linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    background-size: 36px 36px, 120px 120px, 120px 120px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #e2e8f0;
    width: 2300px;
    height: 1400px;
    position: relative;
    overflow: hidden;
  }

  /* Header Bar */
  .header-bar {
    position: absolute;
    top: 25px;
    left: 45px;
    right: 45px;
    height: 85px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(15, 23, 42, 0.92);
    backdrop-filter: blur(10px);
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 0 32px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.6);
    z-index: 100;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 18px;
  }
  .badge-case {
    background: #dc2626;
    color: #fff;
    font-size: 11.5px;
    font-weight: 800;
    letter-spacing: 1.2px;
    padding: 7px 14px;
    border-radius: 8px;
    text-transform: uppercase;
  }
  .header-title h1 {
    font-size: 23px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: 0.5px;
  }
  .header-title p {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 3px;
  }
  .header-right {
    text-align: right;
    max-width: 480px;
  }
  .header-right .unit {
    font-size: 13.5px;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: 0.5px;
  }
  .header-right .sub {
    font-size: 11.5px;
    color: #cbd5e1;
    margin-top: 3px;
    line-height: 1.3;
  }
  .badge-correction {
    background: rgba(239, 68, 68, 0.15);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.35);
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 700;
    display: inline-block;
  }

  /* Legend Bar */
  .legend-bar {
    position: absolute;
    bottom: 25px;
    left: 45px;
    right: 45px;
    height: 60px;
    background: rgba(15, 23, 42, 0.94);
    border: 1px solid #1e293b;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding: 0 25px;
    z-index: 100;
    font-size: 12.5px;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .legend-line {
    width: 32px;
    height: 4px;
    border-radius: 2px;
  }

  /* Node Cards Base */
  .node-card {
    position: absolute;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 15px 18px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.65);
    z-index: 20;
  }
  .node-card .card-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
    padding-bottom: 9px;
    border-bottom: 1px solid rgba(51, 65, 85, 0.6);
  }
  .icon-box {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .icon-box svg {
    width: 22px;
    height: 22px;
  }
  .card-type {
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }
  .card-name {
    font-size: 15.5px;
    font-weight: 800;
    color: #f8fafc;
    line-height: 1.2;
    margin-top: 2px;
  }
  .prop-list {
    font-size: 12.5px;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  .prop-row {
    display: flex;
    justify-content: space-between;
    gap: 14px;
    border-bottom: 1px dashed rgba(51, 65, 85, 0.35);
    padding-bottom: 4px;
  }
  .prop-label {
    color: #94a3b8;
    font-weight: 500;
  }
  .prop-val {
    color: #f1f5f9;
    font-weight: 600;
    text-align: right;
  }
  .mono {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 12px;
  }

  /* Node Themes */
  .theme-victim {
    border-color: #ef4444;
    border-left: 6px solid #ef4444;
  }
  .theme-victim .icon-box { background: rgba(239, 68, 68, 0.16); color: #f87171; border: 1px solid #ef4444; }
  .theme-victim .card-type { color: #f87171; }

  .theme-sim {
    border-color: #06b6d4;
    border-left: 6px solid #06b6d4;
  }
  .theme-sim .icon-box { background: rgba(6, 182, 212, 0.16); color: #22d3ee; border: 1px solid #06b6d4; }
  .theme-sim .card-type { color: #22d3ee; }

  .theme-device {
    border-color: #3b82f6;
    border-left: 6px solid #3b82f6;
  }
  .theme-device .icon-box { background: rgba(59, 130, 246, 0.16); color: #60a5fa; border: 1px solid #3b82f6; }
  .theme-device .card-type { color: #60a5fa; }

  .theme-suspect {
    border-color: #f59e0b;
    border-left: 6px solid #f59e0b;
  }
  .theme-suspect .icon-box { background: rgba(245, 158, 11, 0.16); color: #fbbf24; border: 1px solid #f59e0b; }
  .theme-suspect .card-type { color: #fbbf24; }

  .theme-mule {
    border-color: #a855f7;
    border-left: 6px solid #a855f7;
  }
  .theme-mule .icon-box { background: rgba(168, 85, 247, 0.16); color: #c084fc; border: 1px solid #a855f7; }
  .theme-mule .card-type { color: #c084fc; }

  .theme-bank {
    border-color: #10b981;
    border-left: 6px solid #10b981;
  }
  .theme-bank .icon-box { background: rgba(16, 185, 129, 0.16); color: #34d399; border: 1px solid #10b981; }
  .theme-bank .card-type { color: #34d399; }

  /* SVG Links Canvas */
  #network-svg {
    position: absolute;
    top: 0;
    left: 0;
    width: 2300px;
    height: 1400px;
    z-index: 10;
    pointer-events: none;
  }
  .link-path {
    fill: none;
    stroke-linecap: round;
  }
  .link-label-bg {
    fill: #090e1a;
    stroke-width: 1.5;
    rx: 6;
    ry: 6;
  }
  .link-label-text {
    font-size: 11.5px;
    font-weight: 800;
    letter-spacing: 0.4px;
    text-anchor: middle;
    dominant-baseline: middle;
  }

  /* Section Title Overlay */
  .column-label {
    position: absolute;
    font-size: 12.5px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #64748b;
    z-index: 5;
  }
</style>
</head>
<body>

  <!-- HEADER -->
  <div class="header-bar">
    <div class="header-left">
      <span class="badge-case">ANALISIS HUBUNGAN</span>
      <div class="header-title">
        <h1>LINK ANALYSIS BOARD: SINDIKAT PASSOBIS TORAJA - ENREKANG - MAKASSAR</h1>
        <p>Visualisasi Pemetaan Korban, Saluran Komunikasi (SIM), Perangkat IMEI, Eksekutor Lapangan & Rekening Penampung</p>
      </div>
    </div>
    <div class="header-right">
      <div class="unit">SUBDIT II FISMONDEV DITRESKRIMSUS POLDA SULSEL</div>
      <div class="sub">
        <span class="badge-correction">RALAT STATUS</span> <strong>Ibu dr. Revas & Ayah dr. Riad</strong> = Korban Materiil | <strong>Revas & Riad</strong> = Narahubung Koordinasi
      </div>
    </div>
  </div>

  <!-- COLUMN LABELS -->
  <div class="column-label" style="top: 130px; left: 60px;">[ 1 ] KORBAN & NARAHUBUNG</div>
  <div class="column-label" style="top: 130px; left: 470px;">[ 2 ] SALURAN TELEKOMUNIKASI (SIM)</div>
  <div class="column-label" style="top: 130px; left: 910px;">[ 3 ] PERANGKAT FISIK (IMEI)</div>
  <div class="column-label" style="top: 130px; left: 1370px;">[ 4 ] EKSEKUTOR LAPANGAN</div>
  <div class="column-label" style="top: 130px; left: 1840px;">[ 5 ] REKENING PENAMPUNG & MULES</div>

  <!-- SVG NETWORK OVERLAY -->
  <svg id="network-svg">
    <defs>
      <!-- Arrow Markers -->
      <marker id="arrow-red" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M 0 1 L 9 5 L 0 9 z" fill="#ef4444" />
      </marker>
      <marker id="arrow-gold" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M 0 1 L 9 5 L 0 9 z" fill="#f59e0b" />
      </marker>
      <marker id="arrow-cyan" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M 0 1 L 9 5 L 0 9 z" fill="#06b6d4" />
      </marker>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M 0 1 L 9 5 L 0 9 z" fill="#3b82f6" />
      </marker>
      <marker id="arrow-purple" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M 0 1 L 9 5 L 0 9 z" fill="#a855f7" />
      </marker>
      <marker id="arrow-emerald" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M 0 1 L 9 5 L 0 9 z" fill="#10b981" />
      </marker>
    </defs>

    <!-- ============================================== -->
    <!-- 1. KORBAN KE SIM PENELPON (Kontak Penipuan)    -->
    <!-- ============================================== -->
    <!-- Ibu Revas -> SIM 0858-2851-2082 -->
    <path d="M 380 270 C 415 270, 430 280, 470 280" class="link-path" stroke="#ef4444" stroke-width="2.8" stroke-dasharray="6,4" marker-end="url(#arrow-red)" />
    
    <!-- Ayah Riad -> SIM 0858-2851-2082 -->
    <path d="M 380 840 C 430 840, 420 330, 470 330" class="link-path" stroke="#ef4444" stroke-width="2.8" stroke-dasharray="6,4" marker-end="url(#arrow-red)" />

    <!-- ============================================== -->
    <!-- 2. KORBAN KE REKENING (Aliran Transfer Dana)   -->
    <!-- ============================================== -->
    <!-- Ibu Revas -> Bank Mandiri (melengkung tinggi di atas koridor header) -->
    <path d="M 380 230 C 430 160, 800 150, 1300 150 C 1600 150, 1750 170, 1840 250" class="link-path" stroke="#f59e0b" stroke-width="3.2" marker-end="url(#arrow-gold)" />
    
    <!-- Ayah Riad -> Bank BNI Taplus (melengkung bawah di atas koridor legend) -->
    <path d="M 380 900 C 450 950, 800 1250, 1300 1250 C 1650 1250, 1780 1150, 1840 850" class="link-path" stroke="#f59e0b" stroke-width="3.2" marker-end="url(#arrow-gold)" />

    <!-- ============================================== -->
    <!-- 3. SIM CARD KE IMEI (Hardware Binding)         -->
    <!-- Entry points tersebar di tepi kiri iPhone XR  -->
    <!-- ============================================== -->
    <!-- SIM 1 (0858) -> iPhone XR top -->
    <path d="M 780 290 C 830 290, 860 550, 910 550" class="link-path" stroke="#06b6d4" stroke-width="2.5" marker-end="url(#arrow-cyan)" />
    
    <!-- SIM 2 (0857) -> iPhone XR mid-top -->
    <path d="M 780 490 C 830 490, 860 590, 910 590" class="link-path" stroke="#06b6d4" stroke-width="2" marker-end="url(#arrow-cyan)" />

    <!-- SIM 3 (0851 by.U) -> iPhone XR mid-bottom -->
    <path d="M 780 690 C 830 690, 860 630, 910 630" class="link-path" stroke="#06b6d4" stroke-width="3" marker-end="url(#arrow-cyan)" />

    <!-- SIM 4 (0812 Suami) -> iPhone XR bottom -->
    <path d="M 780 890 C 830 890, 860 670, 910 670" class="link-path" stroke="#06b6d4" stroke-width="2.5" marker-end="url(#arrow-cyan)" />

    <!-- ============================================== -->
    <!-- 4. PENGUASAAN PERANGKAT (iPhone XR -> Pelaku)  -->
    <!-- ============================================== -->
    <!-- iPhone XR -> Pregita Angel -->
    <path d="M 1240 570 C 1290 570, 1320 420, 1370 420" class="link-path" stroke="#f59e0b" stroke-width="3" marker-end="url(#arrow-gold)" />

    <!-- iPhone XR -> Suami Pregita -->
    <path d="M 1240 670 C 1290 670, 1320 830, 1370 830" class="link-path" stroke="#3b82f6" stroke-width="2.8" marker-end="url(#arrow-blue)" />

    <!-- ============================================== -->
    <!-- 5. KONEKSI KELUARGA / JARINGAN                 -->
    <!-- ============================================== -->
    <!-- Suami <-> Pregita Angel (Pasutri) Vertikal Bersih -->
    <path d="M 1530 630 L 1530 740" class="link-path" stroke="#a855f7" stroke-width="3" stroke-dasharray="6,4" />

    <!-- Pregita Angel -> Nenek Phora Bibiana (Nenek - Cucu) -->
    <path d="M 1700 400 C 1750 400, 1780 440, 1840 470" class="link-path" stroke="#a855f7" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-purple)" />

    <!-- ============================================== -->
    <!-- 6. KEPEMILIKAN REKENING BANK                   -->
    <!-- ============================================== -->
    <!-- Bank Mandiri -> Phora Bibiana Vertikal -->
    <path d="M 2005 385 L 2005 440" class="link-path" stroke="#10b981" stroke-width="3.2" marker-end="url(#arrow-emerald)" />

    <!-- Bank BNI -> Muh Nursyahadat Vertikal -->
    <path d="M 2005 955 L 2005 1010" class="link-path" stroke="#10b981" stroke-width="3.2" marker-end="url(#arrow-emerald)" />

    <!-- ============================================== -->
    <!-- FLOATING BADGES & LABELS                       -->
    <!-- ============================================== -->
    <!-- Label: Dihubungi WA (Di celah tengah antara Kolom 1 & 2) -->
    <g transform="translate(425, 255)">
      <rect x="-42" y="-10" width="84" height="20" class="link-label-bg" stroke="#ef4444"/>
      <text x="0" y="0" class="link-label-text" fill="#f87171">Dihubungi WA</text>
    </g>

    <!-- Label: Dihubungi Voice (Di celah tengah antara Kolom 1 & 2) -->
    <g transform="translate(425, 430)">
      <rect x="-48" y="-10" width="96" height="20" class="link-label-bg" stroke="#ef4444"/>
      <text x="0" y="0" class="link-label-text" fill="#f87171">Dihubungi Voice</text>
    </g>

    <!-- Label: Transfer Rp 3.2 Juta -->
    <g transform="translate(1120, 140)">
      <rect x="-85" y="-12" width="170" height="24" class="link-label-bg" stroke="#f59e0b"/>
      <text x="0" y="0" class="link-label-text" fill="#fbbf24">Transfer Rp 3.200.000,-</text>
    </g>

    <!-- Label: Transfer Rp 250 Ribu -->
    <g transform="translate(1120, 1260)">
      <rect x="-75" y="-12" width="150" height="24" class="link-label-bg" stroke="#f59e0b"/>
      <text x="0" y="0" class="link-label-text" fill="#fbbf24">Transfer Rp 250.000,-</text>
    </g>

    <!-- Label: Hubungan Pasutri (Offset di samping kanan garis) -->
    <g transform="translate(1625, 685)">
      <rect x="-65" y="-10" width="130" height="20" class="link-label-bg" stroke="#a855f7"/>
      <text x="0" y="0" class="link-label-text" fill="#c084fc">Pasangan Suami-Istri</text>
    </g>

    <!-- Label: Hubungan Nenek-Cucu -->
    <g transform="translate(1775, 415)">
      <rect x="-65" y="-10" width="130" height="20" class="link-label-bg" stroke="#a855f7"/>
      <text x="0" y="0" class="link-label-text" fill="#c084fc">Nenek - Cucu (Satu RT)</text>
    </g>
  </svg>

  <!-- ============================================== -->
  <!-- NODES / ENTITY CARDS                           -->
  <!-- ============================================== -->

  <!-- [KOLOM 1: KORBAN] -->
  
  <!-- KORBAN 1: Ibu dr Revas (Female) -->
  <div class="node-card theme-victim" style="top: 175px; left: 60px; width: 320px;">
    <div class="card-head">
      <div class="icon-box">
        <!-- Female User SVG Icon -->
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="7" r="4"/>
          <path d="M5.5 21v-2a6.5 6.5 0 0 1 13 0v2"/>
          <path d="M8 8a4 4 0 0 0 8 0" stroke-width="1.5"/>
        </svg>
      </div>
      <div>
        <div class="card-type">KORBAN MATERIIL 1 (FEMALE)</div>
        <div class="card-name">IBU dr. REVAS</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">Narahubung</span>
        <span class="prop-val" style="color:#f87171;">Sdr. Revas (Anak Korban)</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Waktu Kejadian</span>
        <span class="prop-val">15 September 2026</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Modus Kejahatan</span>
        <span class="prop-val">Catut Nama Anak ("hp jil temanku")</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Total Kerugian</span>
        <span class="prop-val mono" style="color:#ef4444; font-weight:800; font-size:13px;">Rp 3.200.000,-</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Tujuan Transfer</span>
        <span class="prop-val" style="color:#fbbf24;">Bank Mandiri (Phora Bibiana)</span>
      </div>
    </div>
  </div>

  <!-- KORBAN 2: Ayah dr Riad (Male) -->
  <div class="node-card theme-victim" style="top: 750px; left: 60px; width: 320px;">
    <div class="card-head">
      <div class="icon-box">
        <!-- Male User SVG Icon -->
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="7" r="4"/>
          <path d="M5 21v-2a7 7 0 0 1 14 0v2"/>
        </svg>
      </div>
      <div>
        <div class="card-type">KORBAN MATERIIL 2 (MALE)</div>
        <div class="card-name">AYAH dr. RIAD</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">Narahubung</span>
        <span class="prop-val" style="color:#f87171;">Sdr. Riad (Anak Korban)</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Waktu Kejadian</span>
        <span class="prop-val">05 Oktober 2026 (17:11 WIB)</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Modus Kejahatan</span>
        <span class="prop-val">Catut Keluarga Mendesak</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Kartu Pengirim</span>
        <span class="prop-val mono">60130xxxxxx83624</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Total Kerugian</span>
        <span class="prop-val mono" style="color:#ef4444; font-weight:800; font-size:13px;">Rp 250.000,-</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Tujuan Transfer</span>
        <span class="prop-val" style="color:#fbbf24;">BNI Taplus (M. Nursyahadat)</span>
      </div>
    </div>
  </div>


  <!-- [KOLOM 2: SALURAN SIM CARD] -->

  <!-- SIM 1: 0858-2851-2082 -->
  <div class="node-card theme-sim" style="top: 230px; left: 470px; width: 310px;">
    <div class="card-head">
      <div class="icon-box">
        <!-- SIM Card SVG Icon -->
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 2h9l5 5v15H6z"/>
          <rect x="9" y="10" width="6" height="8" rx="1"/>
          <line x1="9" y1="14" x2="15" y2="14"/>
        </svg>
      </div>
      <div>
        <div class="card-type">SIM OPERASIONAL UTAMA</div>
        <div class="card-name mono" style="color:#22d3ee;">0858-2851-2082</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">Operator</span>
        <span class="prop-val">Indosat Ooredoo</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Peran Kontak</span>
        <span class="prop-val" style="color:#f87171; font-weight:700;">Menghubungi Kedua Korban</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Binding IMEI</span>
        <span class="prop-val mono">353068103923504 (iPhone XR)</span>
      </div>
    </div>
  </div>

  <!-- SIM 2: 0857-9611-4333 -->
  <div class="node-card theme-sim" style="top: 430px; left: 470px; width: 310px;">
    <div class="card-head">
      <div class="icon-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 2h9l5 5v15H6z"/>
          <rect x="9" y="10" width="6" height="8" rx="1"/>
        </svg>
      </div>
      <div>
        <div class="card-type">SIM OPERASIONAL PENDUKUNG</div>
        <div class="card-name mono">0857-9611-4333</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">Operator</span>
        <span class="prop-val">Indosat Ooredoo</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Peran</span>
        <span class="prop-val">Chat & Koordinasi Palsu</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Binding IMEI</span>
        <span class="prop-val mono">353068103923504 (iPhone XR)</span>
      </div>
    </div>
  </div>

  <!-- SIM 3: 0851-4390-3425 -->
  <div class="node-card theme-sim" style="top: 630px; left: 470px; width: 310px;">
    <div class="card-head">
      <div class="icon-box" style="background:rgba(16, 185, 129, 0.16); border-color:#10b981; color:#34d399;">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 2h9l5 5v15H6z"/>
          <circle cx="12" cy="14" r="2"/>
        </svg>
      </div>
      <div>
        <div class="card-type" style="color:#34d399;">SIM AKTIF REAL-TIME</div>
        <div class="card-name mono" style="color:#34d399;">0851-4390-3425</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">Operator</span>
        <span class="prop-val">by.U (Telkomsel)</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Status Sinyal</span>
        <span class="prop-val" style="color:#34d399; font-weight:700;">Aktif Memancar (Curio)</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Pemakai Utama</span>
        <span class="prop-val">Pregita Angel (Enjel)</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Binding IMEI</span>
        <span class="prop-val mono">353068103923504 (iPhone XR)</span>
      </div>
    </div>
  </div>

  <!-- SIM 4: 0812-4348-4035 -->
  <div class="node-card theme-sim" style="top: 830px; left: 470px; width: 310px;">
    <div class="card-head">
      <div class="icon-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 2h9l5 5v15H6z"/>
          <path d="M10 12h4v5h-4z"/>
        </svg>
      </div>
      <div>
        <div class="card-type">SIM SUAMI PELAKU</div>
        <div class="card-name mono">0812-4348-4035</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">Operator</span>
        <span class="prop-val">Telkomsel</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Pengguna</span>
        <span class="prop-val">Suami Pregita Angel</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Binding IMEI</span>
        <span class="prop-val mono">353068103923504 (iPhone XR)</span>
      </div>
    </div>
  </div>


  <!-- [KOLOM 3: PERANGKAT FISIK IMEI] -->
  
  <!-- Apple iPhone XR -->
  <div class="node-card theme-device" style="top: 500px; left: 910px; width: 330px;">
    <div class="card-head">
      <div class="icon-box">
        <!-- Smartphone SVG Icon -->
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="5" y="2" width="14" height="20" rx="3"/>
          <line x1="12" y1="18" x2="12.01" y2="18" stroke-width="3"/>
        </svg>
      </div>
      <div>
        <div class="card-type">PERANGKAT HARDWARE TUNGGAL</div>
        <div class="card-name" style="color:#60a5fa;">APPLE iPHONE XR</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">Model Fisik</span>
        <span class="prop-val">A1984 (Single Nano-SIM)</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Nomor IMEI</span>
        <span class="prop-val mono" style="color:#38bdf8; font-weight:800; font-size:13px;">353068103923504</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">TAC Number</span>
        <span class="prop-val mono">35306810</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Pola Penggunaan</span>
        <span class="prop-val" style="color:#fbbf24; font-weight:700;">Shared Device (Pasutri)</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Lokasi BTS Aktif</span>
        <span class="prop-val">Desa Pebaloran, Kec. Curio</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Wilayah Hukum</span>
        <span class="prop-val">Enrekang (Perbatasan Tator)</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Koordinat CGI</span>
        <span class="prop-val mono" style="color:#34d399; font-weight:700;">-3.292840, 119.866410</span>
      </div>
    </div>
  </div>


  <!-- [KOLOM 4: EKSEKUTOR LAPANGAN] -->

  <!-- EKSEKUTOR 1: Pregita Angel (Female) -->
  <div class="node-card theme-suspect" style="top: 260px; left: 1370px; width: 330px;">
    <div class="card-head">
      <div class="icon-box">
        <!-- Female Suspect SVG Icon -->
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="7" r="4"/>
          <path d="M5.5 21v-2a6.5 6.5 0 0 1 13 0v2"/>
          <path d="M9 10h6"/>
        </svg>
      </div>
      <div>
        <div class="card-type">EKSEKUTOR LAPANGAN (FEMALE)</div>
        <div class="card-name" style="color:#fbbf24;">PREGITA ANGEL (ENJEL)</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">NIK</span>
        <span class="prop-val mono">7371035911060002</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">TTL / Usia</span>
        <span class="prop-val">Tator, 19-11-2006 (19 Thn)</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Alamat KTP</span>
        <span class="prop-val" style="font-size:11px;">Jl. Jalahong Dg Mattutu 57/59, Bara-Baraya, Makassar</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Posisi Nyata</span>
        <span class="prop-val" style="color:#fbbf24; font-weight:700;">Desa Pebaloran, Curio, Enrekang</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Getcontact Tags</span>
        <span class="prop-val" style="color:#f87171;">"Pregita Angel", "Mafia Gadai", "Penipu"</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Peran</span>
        <span class="prop-val">Eksekutor Penelpon & Pemegang HP</span>
      </div>
    </div>
  </div>

  <!-- EKSEKUTOR 2: Suami Pregita Angel (Male) -->
  <div class="node-card theme-suspect" style="top: 740px; left: 1370px; width: 330px;">
    <div class="card-head">
      <div class="icon-box">
        <!-- Male Suspect SVG Icon -->
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="7" r="4"/>
          <path d="M5 21v-2a7 7 0 0 1 14 0v2"/>
        </svg>
      </div>
      <div>
        <div class="card-type">CO-EKSEKUTOR / SUAMI (MALE)</div>
        <div class="card-name" style="color:#f8fafc;">SUAMI PREGITA ANGEL</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">Nomor Kontak</span>
        <span class="prop-val mono" style="color:#38bdf8;">0812-4348-4035</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Hubungan</span>
        <span class="prop-val" style="color:#c084fc; font-weight:700;">Suami Sah / Pasangan Hidup</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Domisili Lapangan</span>
        <span class="prop-val">Curio, Kab. Enrekang</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Peran</span>
        <span class="prop-val">Pendamping Operasional & Shared Phone</span>
      </div>
    </div>
  </div>


  <!-- [KOLOM 5: REKENING BANK & MULES] -->

  <!-- REKENING 1: Bank Mandiri (Bank Icon) -->
  <div class="node-card theme-bank" style="top: 210px; left: 1840px; width: 330px;">
    <div class="card-head">
      <div class="icon-box">
        <!-- Bank Building SVG Icon -->
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 21h18M3 10h18M5 10v11M9 10v11M15 10v11M19 10v11M12 2L2 7h20L12 2z"/>
        </svg>
      </div>
      <div>
        <div class="card-type">REKENING PENAMPUNG 1</div>
        <div class="card-name" style="color:#34d399;">BANK MANDIRI</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">No. Rekening</span>
        <span class="prop-val mono" style="color:#34d399; font-weight:800; font-size:13px;">1520036531610</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Atas Nama</span>
        <span class="prop-val">Phora Bibiana</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Dana Masuk</span>
        <span class="prop-val mono" style="color:#ef4444; font-weight:800;">Rp 3.200.000,-</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Asal Pengirim</span>
        <span class="prop-val" style="color:#f87171;">Ibu dr. Revas</span>
      </div>
    </div>
  </div>

  <!-- MULE 1: Phora Bibiana (Female) -->
  <div class="node-card theme-mule" style="top: 440px; left: 1840px; width: 330px;">
    <div class="card-head">
      <div class="icon-box">
        <!-- Elderly Female SVG Icon -->
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="7" r="4"/>
          <path d="M5.5 21v-2a6.5 6.5 0 0 1 13 0v2"/>
          <path d="M7 11c1-2 3-2 5-2s4 0 5 2" stroke-width="1.5"/>
        </svg>
      </div>
      <div>
        <div class="card-type">PEMILIK REKENING (FEMALE)</div>
        <div class="card-name" style="color:#c084fc;">PHORA BIBIANA (58 THN)</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">Hubungan</span>
        <span class="prop-val" style="color:#c084fc; font-weight:700;">Nenek Kandung Pregita Angel</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Pekerjaan</span>
        <span class="prop-val">Ibu Rumah Tangga (IRT)</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Alamat KTP</span>
        <span class="prop-val" style="font-size:11px;">Jl. Jalahong Dg Matutu No. 87 RT 002/RW 001, Bara-Baraya</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Lokasi Rumah</span>
        <span class="prop-val" style="color:#fbbf24;">Satu RT / Bersebelahan dg Pregita</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Peran</span>
        <span class="prop-val">Penyedia Buku Tabungan/ATM Penampung</span>
      </div>
    </div>
  </div>

  <!-- REKENING 2: Bank BNI Taplus (Bank Icon) -->
  <div class="node-card theme-bank" style="top: 780px; left: 1840px; width: 330px;">
    <div class="card-head">
      <div class="icon-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 21h18M3 10h18M5 10v11M9 10v11M15 10v11M19 10v11M12 2L2 7h20L12 2z"/>
        </svg>
      </div>
      <div>
        <div class="card-type">REKENING PENAMPUNG 2</div>
        <div class="card-name" style="color:#34d399;">BANK BNI TAPLUS</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">Jenis Tabungan</span>
        <span class="prop-val">BNI Taplus Perorangan</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Atas Nama</span>
        <span class="prop-val">M. Nursyahadat Firmansyah</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Dana Masuk</span>
        <span class="prop-val mono" style="color:#ef4444; font-weight:800;">Rp 250.000,-</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Asal Pengirim</span>
        <span class="prop-val" style="color:#f87171;">Ayah dr. Riad</span>
      </div>
    </div>
  </div>

  <!-- MULE 2: Muh Nursyahadat (Male) -->
  <div class="node-card theme-mule" style="top: 1010px; left: 1840px; width: 330px;">
    <div class="card-head">
      <div class="icon-box">
        <!-- Male Mule SVG Icon -->
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="7" r="4"/>
          <path d="M5 21v-2a7 7 0 0 1 14 0v2"/>
        </svg>
      </div>
      <div>
        <div class="card-type">PEMILIK REKENING (MALE)</div>
        <div class="card-name" style="color:#c084fc;">MUH NURSYAHADAT F. (31 THN)</div>
      </div>
    </div>
    <div class="prop-list">
      <div class="prop-row">
        <span class="prop-label">Domisili</span>
        <span class="prop-val" style="font-size:11px;">Jl. Baji Gio No. 33 B / Bonto Duri VII, Tamalate, Makassar</span>
      </div>
      <div class="prop-row">
        <span class="prop-label">Peran</span>
        <span class="prop-val">Rekening Penampung (Mule Account) BNI</span>
      </div>
    </div>
  </div>


  <!-- BOTTOM LEGEND BAR -->
  <div class="legend-bar">
    <div class="legend-item">
      <div class="legend-line" style="background:#ef4444; border-top: 2px dashed #fff;"></div>
      <span>Kontak Penipuan (Voice / Chat WhatsApp)</span>
    </div>
    <div class="legend-item">
      <div class="legend-line" style="background:#f59e0b;"></div>
      <span>Aliran Dana Kejahatan (Transfer Korban ke Bank)</span>
    </div>
    <div class="legend-item">
      <div class="legend-line" style="background:#06b6d4;"></div>
      <span>Binding Perangkat (SIM Card terpasang pada IMEI iPhone XR)</span>
    </div>
    <div class="legend-item">
      <div class="legend-line" style="background:#3b82f6;"></div>
      <span>Penguasaan Fisik HP di Pebaloran, Curio</span>
    </div>
    <div class="legend-item">
      <div class="legend-line" style="background:#a855f7; border-top: 2px dashed #fff;"></div>
      <span>Hubungan Kekerabatan (Pasutri & Nenek-Cucu Bara-Baraya)</span>
    </div>
    <div class="legend-item">
      <div class="legend-line" style="background:#10b981;"></div>
      <span>Penguasaan Rekening Bank Penampung</span>
    </div>
  </div>

</body>
</html>
"""

html_path = Path("/home/ubuntu/penyidikan/analisis/board_keterkaitan_sindikat_passobis.html")
png_path = Path("/home/ubuntu/penyidikan/analisis/board_keterkaitan_sindikat_passobis.png")

html_path.write_text(html_content, encoding="utf-8")

cmd = [
    "/usr/bin/google-chrome",
    "--headless",
    "--disable-gpu",
    "--window-size=2300,1400",
    f"--screenshot={png_path}",
    str(html_path)
]
subprocess.run(cmd, check=True)
print(f"File updated: {png_path} ({png_path.stat().st_size} bytes)")

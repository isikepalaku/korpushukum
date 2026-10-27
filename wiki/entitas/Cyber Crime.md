---
title: "Cyber Crime"
aliases: ["Tindak Pidana Siber", "Kejahatan Siber", "Cyber Offence", "Kejahatan Komputer"]
tags: [entitas, cyber-crime, siber, ite, illegal-access, hacking, fraud, digital-forensics]
type: entitas
source: "UU 11/2008 jo UU 19/2016 jo UU 1/2024 (ITE), UU 1/2023 (KUHP), UU 1/2026, UU 27/2022 (PDP), Budapest Convention on Cybercrime"
last_updated: 2026-09-23
related: ["UU ITE", "Alat Bukti Elektronik", "Pelindungan Data Pribadi (PDP)", "TPPU", "Pinjol & ITSK", "Perbankan"]
---

# Cyber Crime (Tindak Pidana Siber)

## Ringkasan
Tindak pidana di bidang teknologi informasi, transaksi elektronik, dan sistem komputer. Dalam ranah penyidikan Polri (khususnya Subdit Siber & Subdit Fismondev), kejahatan siber terbagi menjadi dua klasifikasi utama:
1. **Cyber-Dependent Crimes:** Kejahatan yang hanya dapat dilakukan menggunakan komputer/jaringan komputer (misal: *illegal access, DDoS, ransomware, malware injection, data alteration*).
2. **Cyber-Enabled Crimes:** Kejahatan tradisional yang dieskalasi skala dan kecepatannya melalui sistem elektronik (misal: *online fraud/phishing, BEC - Business Email Compromise, illegal online gambling, crypto money laundering, digital extortion*).

---

## Tipologi Kejahatan Siber & Pasal Terkait

| Kategori Kejahatan | Modus Operandi Utama | Dasar Hukum Utama (UU ITE jo UU 1/2026) | Hubungan Delik Lain |
|---|---|---|---|
| **Unauthorized Access (Hacking / Cracking)** | Brute force, credential stuffing, exploiting zero-day, password spraying, remote access trojan (RAT) | **Pasal 30 ayat (1), (2), (3) jo. Pasal 46** UU ITE | [[Pelindungan Data Pribadi (PDP)]] Ps. 65 jo. 67, KUHP Ps. 492 |
| **Data Interference (Pencurian & Perusakan Data)** | Data theft, database exfiltration, wiping data, skimming, scraping ilegal | **Pasal 32 ayat (1), (2), (3) jo. Pasal 48** UU ITE | UU PDP Ps. 65–68, Rahasia Bank |
| **System Interference (Gangguan Sistem)** | DDoS attack, defacing website lembaga/perbankan, ransomware locking | **Pasal 33 jo. Pasal 49** UU ITE | KUHP Ps. 406/521 (Pengrusakan) |
| **Penyalahgunaan Perangkat / Fasilitasi** | Jual-beli tools exploit, panel phishlet, botnet rental, credential logs | **Pasal 34 jo. Pasal 50** UU ITE | Penyertaan KUHP Ps. 55/56 |
| **Computer-Related Forgery (Pemalsuan Data)** | Fake login page, pembuatan dokumen digital palsu, pemalsuan identitas KTP/slip gaji digital | **Pasal 35 jo. Pasal 51** UU ITE | KUHP Ps. 391–392 (Pemalsuan Surat) |
| **Cyber Fraud / Penipuan Transaksi Elektronik** | Phishing perbankan/m-banking, invoice spoofing, SIM swap fraud, APK kurir/undangan fiktif | **Pasal 28 ayat (1) jo. Pasal 45A ayat (1)** UU ITE | KUHP Ps. 492 (Penipuan), [[Perbankan]] |
| **Judi Online (Online Gambling)** | Website slot/gacor, link deposit QRIS/kripto/VA, sindikat live kasino luar negeri | **Pasal 27 ayat (2) jo. Pasal 45 ayat (3)** UU ITE | KUHP Ps. 426, [[TPPU]] UU 8/2010 |
| **Pemerasan & Pengancaman Siber** | Doxing, sextortion, ransomware payment demand, debt collector teror pinjol | **Pasal 27B jo. Pasal 45 ayat (8)/(10)** UU ITE *(UU 1/2024)* | KUHP Ps. 482/483, [[Pinjol & ITSK]] |
| **Illegal Interception (Sniffing / Penyadapan)** | Man-in-the-middle (MitM), fake BTS/IMSI catcher, packet sniffing | **Pasal 31 jo. Pasal 47** UU ITE | Telekomunikasi UU 36/1999 |

---

## Titik Temu Siber & Fismondev (Financial Cyber Crime)

Kejahatan modern umumnya merupakan hibrida antara **siber (vektor intrusi)** dan **finansial (monetisasi hasil kejahatan)**:

1. **Social Engineering & Phishing APK:**
   - Pelaku mengirimkan file APK perusak (misal Trojan SMS grabber/accessibility service).
   - Kode OTP/SMS perbankan dicuri melalui *illegal access* (Ps. 30 jo. 32 UU ITE).
   - Saldo rekening korban dikuras via Internet Banking / QRIS / Top-up e-wallet (Ps. 35/36 UU ITE jo. KUHP 492).
   - Dana diputar melalui jaringan rekening *nominee* / rekening penampung (*mule accounts*) → ditarik tunai atau dikonversi ke USDT kripto ([[TPPU]] UU 8/2010).

2. **SIM Swap Fraud:**
   - Pelaku membuat KTP palsu (Ps. 35 UU ITE / KUHP 391).
   - Mengambil alih nomor ponsel korban di gerai operator.
   - Mereset password akun m-banking dan memindahkan dana.

3. **Kredit Fiktif & Penggunaan Identitas Tanpa Izin:**
   - Data e-KTP dan foto selfie hasil kebocoran data (*data breach*) dimanfaatkan untuk mendaftar pinjol atau fasilitas kredit bank secara daring.
   - Konstruksi: UU PDP Pasal 65–68 + UU ITE Pasal 35 + KUHP Pasal 492.

---

## Langkah & Checklist Penyidikan Kasus Siber (SOP Lapangan)

1. **Digital Evidence Acquisition & Chain of Custody:**
   - Amankan perangkat digital (smartphone, laptop, server, router).
   - Buat *forensic image* bit-by-bit (E01/DD/RAW) dan hitung nilai hash (MD5, SHA-256) sebelum analisis untuk menjaga integritas bukti ([[Alat Bukti Elektronik]]).
2. **Network & System Log Analysis:**
   - Analisis Web Server Access Logs, Firewall Logs, DNS Query Logs, dan Mail Header.
   - Sinkronisasi waktu (*Time Zone & NTP synchronization*) untuk menyusun *timeline of events* (tempus delicti).
3. **OSINT & Telecom Attribution:**
   - Pelacakan IP Public & ASN, Whois lookup, DNS history.
   - Koordinasi permintaan CDR (Call Detail Record), IMEI/IMSI history, LAC-Cell ID BTS ke operator seluler.
4. **Follow The Money & Asset Tracing:**
   - Permintaan data mutasi rekening bank (surat izin pembukaan [[Rahasia Bank]] atau koordinasi penyidik siber/fismondev).
   - Pelacakan alur e-wallet dan transaksi on-chain cryptocurrency (blockchain explorer / transaction tracing tools).
   - Pemblokiran segera terhadap rekening penampung dan akun pedagang fisik aset kripto.

---

## Terkait
- [[UU ITE]] · [[Alat Bukti Elektronik]] · [[Pelindungan Data Pribadi (PDP)]] · [[TPPU]] · [[Pinjol & ITSK]] · [[Perbankan]] · [[UU 1-2026]]

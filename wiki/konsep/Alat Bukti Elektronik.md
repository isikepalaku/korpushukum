---
title: "Alat Bukti Elektronik"
aliases: ["Bukti Digital", "Digital Evidence", "Electronic Evidence", "Bukti Elektronik"]
tags: [konsep, bukti-elektronik, hukum-acara, kuhap, digital-forensics, chain-of-custody]
type: konsep
source:
  - "[[UU Nomor 11 Tahun 2008 tentang Informasi dan Transaksi Elektronik]]"
  - "[[UU Nomor 1 Tahun 2024 Perubahan Kedua UU ITE]]"
  - "[[KUHAP - UU 20 Tahun 2025]]"
  - "Putusan MK Nomor 20/PUU-XIV/2016 (Keabsahan Rekaman Elektronik)"
  - "Perkap No. 10 Tahun 2009 & Standar ISO/IEC 27037"
last_updated: 2026-09-23
related: ["UU ITE", "Cyber Crime", "KUHAP", "Pelindungan Data Pribadi (PDP)"]
---

# Alat Bukti Elektronik & Digital Forensics

## Dasar Hukum Keabsahan
1. **Pasal 5 ayat (1) & (2) UU ITE:**
   - Informasi Elektronik dan/atau Dokumen Elektronik dan/atau hasil cetaknya merupakan alat bukti hukum yang sah.
   - Merupakan **perluasan** dari alat bukti yang sah sesuai dengan Hukum Acara yang berlaku di Indonesia (KUHAP).
2. **Pasal 6 UU ITE (Syarat Keabsahan):**
   - Informasi/Dokumen Elektronik dianggap sah sepanjang dapat diakses, ditampilkan, **dijamin keutuhannya**, dan dapat dipertanggungjawabkan sehingga menerangkan suatu keadaan.
3. **Pasal 44 UU ITE:**
   - Alat bukti penyidikan mencakup alat bukti menurut KUHAP ditambah Informasi Elektronik dan Dokumen Elektronik.
4. **Putusan Mahkamah Konstitusi No. 20/PUU-XIV/2016:**
   - Dokumen/rekaman elektronik sebagai alat bukti **hanya sah** apabila diperoleh secara sah oleh aparat penegak hukum yang berwenang atas perintah hukum (*lawful interception/acquisition*). Perekaman diam-diam oleh perorangan tanpa izin tidak dapat serta merta dijadikan bukti primer tanpa uji forensik dan korelasi bukti lain.

---

## Prinsip Penanganan Bukti Digital (ISO/IEC 27037)

Dalam pembuktian di pengadilan, nilai kekuatan pembuktian bukti elektronik sangat bergantung pada integritas **Chain of Custody (Rantai Pengawasan Bukti)**:

```
[ IDENTIFIKASI ] ──> [ AKUISISI / CLONING ] ──> [ PRESERVASI ] ──> [ ANALISIS ] ──> [ PRESENTASI / BAP ]
```

1. **Identification (Identifikasi):**
   - Menentukan perangkat/media penyimpanan sumber bukti (smartphone, server, hard disk, router, cloud account, log provider).
2. **Acquisition (Akuisisi & Kloning Forensik):**
   - Menggunakan metode *Write Blocker* hardware/software agar data asli tidak terubah 1 bit pun.
   - Membuat salinan bit-by-bit (*forensic duplicate / raw image .dd/.e01*).
3. **Preservation & Verification (Preservasi & Uji Hash):**
   - Menghitung nilai hash matematis (MD5, SHA-1, SHA-256) pada file master dan salinan kerja (*working image*).
   - Nilai hash master = nilai hash salinan kerja (bukti tidak mengalami alterasi).
4. **Analysis (Analisis Ahli Digital Forensik):**
   - Analisis artefak sistem, log aktivitas, database aplikasi (SQLite/WAL), memori RAM (*live memory dump*), dan metadata (EXIF, timestamp MAC - Modified, Accessed, Created).
5. **Presentation & Documentation (Laporan Hasil Analisis / BAP Ahli):**
   - Disusun dalam Berita Acara Pemeriksaan Laboratoris Digital Forensik yang memuat kronologi penanganan, metodologi, software valid (FTK, EnCase, Autopsy, AXIOM, Cellebrite), dan kesimpulan fakta digital.

---

## Kategori Artefak Digital Utama dalam Penyidikan

| Kategori Artefak | Sumber Data | Relevansi Pembuktian Perkara |
|---|---|---|
| **CDR & BTS Log** | Operator Telekomunikasi | Posisi geografis perangkat, durasi komunikasi, pola hubungan antar-tersangka. |
| **Server & Access Logs** | Web Server, Proxy, Cloud Firewall | IP Address sumber penyerang (*attacker IP*), timestamp akses, URI request, User-Agent string. |
| **Database & Transaction Logs** | Core Banking, Gateway Pembayaran, DBMS | Mutasi saldo, waktu settlement, akun penampung, identitas rekening transfer. |
| **Mobile Artifacts** | SQLite DB (WhatsApp, Telegram, SMS) | Riwayat chat, pengiriman file APK berbahaya, pertukaran nomor rekening/crypto wallet. |
| **File Metadata & Hash** | File System (NTFS, EXT4, APFS) | Waktu modifikasi, author dokumen palsu, kecocokan hash file malware/ransomware. |

---

## Poin Kritis Uji di Pengadilan (Tangkisan Pembelaan & Solusi Penyidik)
- **Tangkisan: "Data mudah dimanipulasi / direkayasa":**
  - *Counter:* Buktikan dengan kesesuaian nilai hash SHA-256 sejak saat penyitaan sampai persidangan; sertakan BAP Penyitaan Digital yang mencantumkan hash asli.
- **Tangkisan: "IP Address dinamis bukan pelaku sesungguhnya":**
  - *Counter:* Lakukan korelasi triangulasi (Log IP + CDR ISP + Penguasaan fisik perangkat + Bukti transfer dana + Akun media sosial/email login bersamaan).
- **Tangkisan: "Screenshot chat tanpa file asli":**
  - *Counter:* Screenshot berdiri sendiri bernilai bukti petunjuk lemah; wajib didukung ekstraksi database chat fisik (*raw physical dump*) dari perangkat ponsel atau keterangan saksi ahli.

---

## Terkait
- [[UU ITE]] · [[Cyber Crime]] · [[Pelindungan Data Pribadi (PDP)]] · [[KUHAP]]

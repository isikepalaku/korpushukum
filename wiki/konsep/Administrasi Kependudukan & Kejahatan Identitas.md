---
title: "Administrasi Kependudukan & Kejahatan Identitas"
aliases: [Adminduk, SIAK, IKD, Kejahatan Identitas, Pemalsuan NIK]
tags: [adminduk, kependudukan, pemalsuan-identitas, siak, ikd, uu-adminduk, penyidikan]
type: konsep
source:
  - "[[Undang-Undang Nomor 23 Tahun 2006 tentang Administrasi Kependudukan]]"
  - "[[Undang-Undang Nomor 24 Tahun 2013 tentang Perubahan atas UU 23-2006 tentang Administrasi Kependudukan]]"
  - "[[Peraturan Pemerintah Nomor 40 Tahun 2019 tentang Pelaksanaan UU Administrasi Kependudukan]]"
  - "[[Peraturan Presiden Nomor 96 Tahun 2018 tentang Persyaratan dan Tata Cara Pendaftaran Penduduk dan Pencatatan Sipil]]"
  - "[[Permendagri Nomor 108 Tahun 2019 tentang Peraturan Pelaksanaan Perpres 96-2018 (Pendaftaran Penduduk dan Pencatatan Sipil)]]"
  - "[[Permendagri Nomor 95 Tahun 2019 tentang Sistem Informasi Administrasi Kependudukan]]"
  - "[[Permendagri Nomor 72 Tahun 2022 tentang Standar Blangko KTP-el dan Penyelenggaraan Identitas Kependudukan Digital]]"
last_updated: 2026-10-01
related: ["[[KUHP]]", "[[KUHAP]]", "[[UU 1-2026]]", "[[UU ITE]]", "[[Pelindungan Data Pribadi (PDP)]]", "[[Perbankan]]", "[[Cyber Crime]]", "[[TPPU]]"]
---

# Administrasi Kependudukan & Kejahatan Identitas

## 1. Status Korpus & Payung Hukum

Bidang Administrasi Kependudukan (Adminduk) merupakan pilar pembuktian identitas hukum subjek hukum perorangan dalam penanganan tindak pidana perbankan, kejahatan siber (*identity theft*, *social engineering* IKD), dan tindak pidana pencucian uang (TPPU). 

Hierarki regulasi kanonik yang berlaku:
1. **Undang-Undang Pokok:** [[Undang-Undang Nomor 23 Tahun 2006 tentang Administrasi Kependudukan]] sebagaimana telah diubah dengan [[Undang-Undang Nomor 24 Tahun 2013 tentang Perubahan atas UU 23-2006 tentang Administrasi Kependudukan]].
2. **Peraturan Pelaksanaan Pemerintah:** [[Peraturan Pemerintah Nomor 40 Tahun 2019 tentang Pelaksanaan UU Administrasi Kependudukan]].
3. **Tata Cara Pendaftaran & Pencatatan:** [[Peraturan Presiden Nomor 96 Tahun 2018 tentang Persyaratan dan Tata Cara Pendaftaran Penduduk dan Pencatatan Sipil]].
4. **Petunjuk Teknis Pendaftaran Penduduk:** [[Permendagri Nomor 108 Tahun 2019 tentang Peraturan Pelaksanaan Perpres 96-2018 (Pendaftaran Penduduk dan Pencatatan Sipil)]].
5. **Arsitektur Sistem & Basis Data:** [[Permendagri Nomor 95 Tahun 2019 tentang Sistem Informasi Administrasi Kependudukan]] (SIAK).
6. **Identitas Digital & KTP-el:** [[Permendagri Nomor 72 Tahun 2022 tentang Standar Blangko KTP-el dan Penyelenggaraan Identitas Kependudukan Digital]] (IKD).

---

## 2. Konstruksi Pidana Sektoral (*Lex Specialis*) & Penyesuaian UU 1/2026

Berdasarkan asas *lex specialis derogat legi generali*, manipulasi data kependudukan dan penerbitan dokumen tanpa hak diproses menggunakan ketentuan pidana dalam Bab XI UU Adminduk (Pasal 93 – Pasal 97), yang disinkronkan dengan aturan transisi **[[UU 1-2026]] (Penyesuaian Pidana jo. KUHP Nasional)**:

* **Manipulasi Data oleh Pejabat / Petugas (Pasal 94 UU 24/2013):**
  * *Unsur:* Pejabat dan/atau petugas pada penyelenggara dan instansi pelaksana yang memerintahkan dan/atau memfasilitasi dan/atau melakukan manipulasi data kependudukan dan/atau elemen data penduduk.
  * *Penerapan:* Penjara maks 6 tahun atau denda Kategori V (Rp 500 juta) sesuai konversi UU 1/2026.
* **Penerbitan Dokumen Tanpa Prosedur (Pasal 95B UU 24/2013):**
  * *Unsur:* Pejabat dan/atau petugas yang membantu menerbitkan Dokumen Kependudukan tanpa hak atau tanpa melalui prosedur yang ditentukan.
  * *Penerapan:* Penjara maks 6 tahun atau denda Kategori V.
* **Akses Ilegal ke Database Kependudukan (Pasal 95A UU 24/2013):**
  * *Unsur:* Setiap orang yang tanpa hak mengakses database kependudukan.
  * *Penerapan:* Penjara maks 2 tahun atau denda Kategori III (Rp 50 juta).
* **Pemalsuan Surat & Dokumen Kependudukan (Pasal 93 UU 23/2006):**
  * *Unsur:* Setiap orang yang sengaja memalsukan surat dan/atau dokumen kependudukan.
  * *Penerapan:* Penjara maks 6 tahun atau denda Kategori V.
* **Kepemilikan Identitas Ganda (Pasal 96 UU 24/2013):**
  * *Unsur:* Setiap orang atau badan hukum yang tanpa hak mencetak, menerbitkan, dan/atau mendistribusikan blangko dokumen kependudukan atau memiliki NIK/KTP ganda secara melawan hukum.
  * *Penerapan:* Penjara maks 10 tahun atau denda Kategori VI (Rp 2 miliar).

---

## 3. Titik Rawan Modus Kejahatan dalam Penyidikan

### A. Modus Rekayasa SKPWNI Lintas Wilayah (Kasus BWS)
* **Pola:** Menghindari sistem verifikasi tatap muka yang ketat di domisili tujuan (misal Makassar) dengan cara melempar permohonan ke Disdukcapil kabupaten lain (misal Poso) via perantara/oknum.
* **Celah:** Penerbitan Surat Keterangan Pindah WNI (SKPWNI) secara *remote* dalam format PDF tanpa verifikasi fisik berkas pemohon dan tanpa kehadiran pemohon.
* **Hukum Pelaksanaan:** Melanggar ketentuan Pasal 25 s.d. Pasal 32 [[Peraturan Presiden Nomor 96 Tahun 2018 tentang Persyaratan dan Tata Cara Pendaftaran Penduduk dan Pencatatan Sipil]] dan Pasal 28 s.d. Pasal 40 [[Permendagri Nomor 108 Tahun 2019 tentang Peraturan Pelaksanaan Perpres 96-2018 (Pendaftaran Penduduk dan Pencatatan Sipil)]].
* **Konstruksi Penyertaan:** Oknum Disdukcapil yang memproses dijerat Pasal 94/95B UU Adminduk jo. Pasal 55/56 KUHP jo. Pasal 35 UU ITE.

### B. Modus NIK Manipulatif / Duplikat (*Mule Account*)
* Penciptaan NIK baru dengan mengubah sebagian elemen data (nama orang tua, tanggal lahir) ke dalam sistem SIAK guna membuka rekening tabungan penampung (*mule account*) perbankan atau fasilitas kredit fiktif.
* Status pada sistem SIAK: `DUPLICATE_RECORD` atau NIK aspal yang dapat dilacak melalui riwayat log pendaftaran data keluarga.

### C. Modus Social Engineering Berkedok Sosialisasi IKD (Kasus APK Trojan Bachri Sudda)
* Penyerang mengaku petugas Disdukcapil/Kecamatan yang menawarkan aktivasi Identitas Kependudukan Digital (IKD) via tautan unduhan APK palsu.
* Melanggar ketentuan penyelenggaraan IKD resmi sebagaimana diatur dalam [[Permendagri Nomor 72 Tahun 2022 tentang Standar Blangko KTP-el dan Penyelenggaraan Identitas Kependudukan Digital]], di mana registrasi IKD sah **wajib** melalui verifikasi biometrik tatap muka di kantor Disdukcapil atau aplikasi resmi Kemendagri di Google Play Store.

---

## 4. Pedoman Pembuktian Forensik Adminduk

Dalam menelusuri oknum dan membuktikan tindak pidana terkait data kependudukan:
1. **Audit Trail SIAK:**
   * Minta log audit ke Ditjen Dukcapil Kemendagri / Administrator Database (ADB) SIAK setempat berdasarkan [[Permendagri Nomor 95 Tahun 2019 tentang Sistem Informasi Administrasi Kependudukan]].
   * Komponen bukti: User ID penginput, User ID pejabat verifikator, IP Address, MAC Address workstation, dan timestamp transaksi.
2. **Validasi TTE / Sertifikat Digital BSrE:**
   * Uji keabsahan QR code Tanda Tangan Elektronik pada dokumen PDF (SKPWNI/KK) ke Balai Sertifikasi Elektronik (BSrE) BSSN.
3. **Sinkronisasi Follow the Money:**
   * Menggabungkan riwayat chat permintaan pembuatan dokumen dengan mutasi aliran dana suap/jasa transfer bank/e-wallet ke oknum ASN atau perantara.

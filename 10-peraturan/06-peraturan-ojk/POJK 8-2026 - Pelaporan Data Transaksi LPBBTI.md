---
id: POJK 8/2026
jenis: POJK
lembaga: Otoritas Jasa Keuangan
nomor: 8
tahun: 2026
judul: Pelaporan dan Permintaan Data Transaksi Pendanaan oleh Penyelenggara Layanan
  Pendanaan Bersama Berbasis Teknologi Informasi
judul_singkat: Pelaporan Data Transaksi LPBBTI
status: berlaku
mencabut_sebagian:
- POJK 40/2024
bidang:
- keuangan
tags:
- jenis/pojk
- bidang/keuangan
- status/berlaku
struktur_teks: datar
penjelasan: tidak
anchor_pasal: false
kelengkapan: lengkap
verifikasi: sebagian
last_updated: '2026-11-01'
---

# POJK Nomor 8 Tahun 2026 tentang Pelaporan dan Permintaan Data Transaksi Pendanaan oleh Penyelenggara LPBBTI

> **Status:** Berlaku (Ditetapkan: 12 Juni 2026 | Diundangkan: 06 Juli 2026)  
> **Sumber Resmi:** [OJK JDIH / Regulasi](https://ojk.go.id/id/regulasi/Pages/POJK-8-Tahun-2026-Pelaporan-dan-Permintaan-Data-Transaksi-Pendanaan-oleh-Penyelenggara-LPBBTI.aspx)  
> **Ketentuan Terkait:** Mencabut Pasal 187 [[POJK No. 40 Tahun 2024 tentang Layanan Pendanaan Bersama Berbasis Teknologi Informasi]]  
> **Relevansi Lidik/Sidik:** Akses data transaksi riil (borrower/lender), deteksi over-indebtedness (gali lubang tutup lubang pinjol), serta pemenuhan bukti elektronik transaksi pendanaan.

---

## 1. Latar Belakang & Urgensi
1. Kebutuhan standardisasi dan integrasi data transaksi pendanaan secara real-time / berkala guna memitigasi risiko kredit macet (TWP90) dan pendanaan berlebihan (over-indebtedness).
2. Penyempurnaan infrastruktur Pusat Data Fintech Lending (**Pusdafil**) dan Fintech Data Center (**FDC**) untuk menyaring calon penerima dana (borrower).
3. Penguatan pengawasan OJK terhadap penyelenggara LPBBTI (Pinjaman Daring / Pindar).

---

## 2. Pokok-Pokok Pengaturan

### A. Kewajiban Integrasi Sistem dan Pelaporan
* Penyelenggara LPBBTI wajib mengintegrasikan sistem elektroniknya dengan **Pusdafil** milik OJK.
* Pelaporan mencakup data identitas debitur/kreditur, profil risiko, plafon pinjaman, outstanding, status kolektibilitas/kelancaran pembayaran, dan histori restrukturisasi.
* Pelaporan wajib disampaikan secara akurat, lengkap, dan tepat waktu sesuai protokol data OJK.

### B. Mekanisme Permintaan Informasi (FDC/Pusdafil)
* Penyelenggara wajib melakukan pengecekan rekam jejak kredit calon penerima dana ke Pusdafil/FDC sebelum menyetujui pendanaan baru.
* Penyelenggara dilarang menyalurkan pendanaan kepada penerima dana yang telah melebihi batas batas maksimum penerimaan pendanaan lintas platform (maksimal 3 platform sesuai [[SEOJK No. 19-SEOJK.06-2023 tentang Penyelenggaraan Layanan Pendanaan Bersama Berbasis Teknologi Informasi]]).

### C. Keamanan Data Pribadi dan Rahasia Transaksi
* Penyelenggara wajib menerapkan standar keamanan siber ISO 27001 dan mematuhi UU Pelindungan Data Pribadi (UU 27/2022).
* Akses data Pusdafil hanya diperkenankan untuk mitigasi risiko pendanaan, dilarang disalahgunakan untuk tujuan komersial di luar persetujuan debitur.

---

## 3. Titik Kritis Penyelidikan Fismondev / Tipid Siber

> [!caution] Titik Kritis Pembuktian (Ps. 184 KUHAP)
> 1. **Pengecekan Izin & Integrasi Pusdafil:** Pinjol ilegal tidak pernah dan tidak memiliki akses ke Pusdafil OJK. Ketiadaan data entitas di Pusdafil menjadi indikator awal pinjol tanpa izin.
> 2. **Audit Forensik Transaksi:** Dalam penyidikan tindak pidana fraud/fiktif borrower di platform fintech, mintakan penetapan pengadilan / izin OJK untuk membuka logs transaksi di Pusdafil.
> 3. **Bukti Elektronik Transaksi:** Rekam jejak transmisi data dari server penyelenggara ke Pusdafil menjadi alat bukti surat / petunjuk yang sah sesuai Pasal 5 UU ITE.

> [!danger] Rekonstruksi Hukum & Sanksi
> * Pelanggaran kewajiban pelaporan dikenakan sanksi administratif bertingkat (peringatan tertulis, denda, pembatasan kegiatan usaha, hingga pencabutan izin usaha).
> * Modus manipulasi data laporan (misal menyembunyikan NPL/TWP90 palsu) dapat dijerat Pasal 301 [[UU 4 Tahun 2023 P2SK]] (penyampaian laporan palsu kepada OJK).
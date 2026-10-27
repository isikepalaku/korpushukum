<!-- llm-wiki-log-header-start -->
# Wiki Operation Log

Every ingest, lint run, and maintenance operation is recorded here automatically. For a better experience, use the **Operation History** panel:
- Cmd+P → "View operation history"
- Or open from Settings → Auto Maintenance → Operation History

---
> Catatan kronologis append-only dari aktivitas wiki (ingest, query, lint). Format tiap entry: `## [YYYY-MM-DD] <aksi> | <judul>`.

## [2026-08-30] init | Inisialisasi LLM Wiki
- Implementasi pola LLM Wiki (karpathy) di vault hukum.
- Dibuat: `AGENTS.md` (schema), `wiki/index.md` (katalog), `wiki/log.md` (ini), `wiki/entitas/Koperasi.md` (contoh entitas).
- Mapping 3 lapisan: raw = `Hukum Pidana/` & `Hukum Keuangan/`; wiki = `wiki/`; schema = `AGENTS.md`.

## [2026-08-30] seed | Seeding lengkap lapisan wiki
- **Entitas (11)**: Koperasi, Fidusia, Pinjol & ITSK, Money Changer, Investasi Bodong, TPPU, Perbankan, Pasar Modal, Asuransi, Pembiayaan, LKM.
- **Konsep (7)**: KUHP, KUHAP, UU 1-2026, Lex Specialis, Open Loop Closed Loop, Bank Gelap, Kewenangan Penyidikan SJK.
- Update `wiki/index.md` (katalog) + `INDEX.md` (seksi Wiki).
- Semua ancaman pidana ditulis versi **pasca UU 1/2026**.

## [2026-08-30] ingest | Kasus: KSPPS Bakti Huria Syariah
- Buat `wiki/kasus/KSPPS Bakti Huria Syariah.md` — lidik OSINT lengkap (profil, sinyal legitimasi, gap izin, laporan kredibilitas rendah, dimensi m-payment/BI, checklist verifikasi, konstruksi hukum tentatif).
- Buat `wiki/_templates/kasus.md` — template halaman kasus untuk ingest konsisten.
- Setup alat: Dataview block di `wiki/index.md`; catatan qmd readiness di `AGENTS.md`.
- Update `wiki/index.md` + `INDEX.md`.

## [2026-08-30] koreksi | Pergadaian (Ps. 273 KUHP & Ps. 237/305 P2SK)
- **KOREKSI**: gadai tanpa izin BUKAN hanya administratif. Ditemukan **Ps. 273 KUHP** (Tindak Pidana Perizinan — Gadai Tanpa Izin, penjara maks 1 thn / denda kat. III) dan **Ps. 237 jo 305 P2SK** (larangan umum + pidana kegiatan keuangan tanpa izin, penjara maks 10 thn).
- Update `Hukum Keuangan/Peta Pidana Sektor Jasa Keuangan - Referensi Lidik.md` (seksi Pergadaian).
- Buat `wiki/entitas/Pergadaian.md`. Update `wiki/index.md` + `INDEX.md`.

## [2026-09-01] ingest | Rahasia Bank (materi diseminasi OJK 2026)
- Commit `raw/rahasia-bank/` — `Format-Standar.docx` (template surat permintaan izin pembukaan rahasia bank) + `Komik-Rahasia-Bank-OJK-2026.pdf` (unduhan sesi 30 Agu dari materi S-196/KO.16/2026, link bit.ly/RahasiaBankOJK).
- Buat `wiki/konsep/Rahasia Bank.md` — prosedur permintaan izin ke Ketua Dewan Komisioner OJK, struktur format standar 5 bagian (kop, dasar/rujukan: LP+Sprindik+Penetapan Tersangka, kronologi, keterangan+alasan+hubungan perkara, daftar pihak), dasar hukum POJK 44/2024 & UU 4/2026.
- Update `wiki/entitas/Perbankan.md` (alias Rahasia Bank dilepas, related + catatan lidik), `wiki/index.md`, `INDEX.md`.

## [2026-09-02] ingest | Raw data Direktori Putusan MA (query "gadai")
- Tambah `analisis/direktori-putusan/cari-gadai1.json` (36.466 putusan, agregasi 2019-2026) & `cari-kasasi-gadai.json` (2.276 putusan kasasi) — hasil query API apigateway.mahkamahagung.go.id via `dirput-api.sh`, artefak lidik gadai ilegal (dukungan `wiki/entitas/Pergadaian.md`).

## [2026-09-02] ingest | Studi dana moneter & BPR
- Buat `wiki/entitas/BPR.md` — studi kerangka hukum dana moneter terkait BPR: definisi & posisi moneter (tidak ikut lalu lintas giral), regulasi kunci (POJK 7/2024, POJK 1/2024, UU LPS), izin OJK (Ps. 16 jo. P2SK), kegiatan vs larangan (Ps. 13-14 pasca-P2SK: transfer dana & penukaran valas baru, giro tetap dilarang), penjaminan LPS (Rp 2 M, PP 66/2008), konstruksi pidana (Ps. 46/49/50A; BPRS Ps. 59-66; KUHP 486/492; TPPU), indikasi lidik BPR bermasalah.
- Update `wiki/index.md` + `wiki/log.md`.

## [2026-09-02] ingest | Analisis LK BPRS Dana Moneter vs POJK
- OCR 2 PDF scan: Laporan Posisi Keuangan Publikasi **PT BPRS Dana Moneter** (31 Mar 2026 & 30 Jun 2026) — tesseract ind+eng (render 300dpi) + verifikasi vision.
- Buat `wiki/kasus/BPRS Dana Moneter.md`: posisi keuangan, rasio (KPMM 27,97 / NPF gross 3,09 / BOPO 86,6 / FDR 117,82), perbandingan POJK (modal min zona 2 = Rp35 M vs 7,6 M; **BMPK pihak terkait 10% modal vs 103,9–148,7%**; audit KAP kosong; publikasi POJK 23/2024), red flag lidik (qardh +167%, pendapatan murabahah turun, CKPN turun, hapus buku 7,87 M).
- Update `wiki/index.md` + `wiki/log.md`.

## [2026-09-02] ingest | Paket Operasi Enrekang 2026 (Satgas PASTI, kunjungan 8 Sep)
- Persiapan kunjungan Satgas internal Polda (tergabung Satgas PASTI) ke Kab. Enrekang utk sosialisasi dan pemeriksaan kelengkapan koperasi.
- Buat folder `analisis/enrekang-2026/`: 01-REGULASI-KOPERASI.md (inventaris regulasi, rezim Kemenkop vs OJK), 02-MATRIKS-CELAH-PIDANA.xlsx (12 modus: bank gelap Ps. 46 UU Perbankan, open-loop Ps. 44B jo POJK 47/2024, KUHP 391-392/492, gadai Ps. 273 / Ps. 237 jo 305, Ps. 299/304 P2SK, TPPU), 03-CHECKLIST-KELENGKAPAN-KOPERASI.docx (7 bagian isian lapangan), 04-MATERI-SOSIALISASI-SATGAS-PASTI.pptx (14 slide), 05-AGENDA-KUNJUNGAN.md (alur SOP + uji pembeli), 06-HASIL-RISET-WEB.md (KDMP/KKMP 129 SK, KOSIPA Sulselbar, data Satgas PASTI).
- Verifikasi pasal ke file vault: Ps. 44B UU 25/1992 = Pasal 202 UU P2SK (open-loop -> OJK); Ps. 46 UU Perbankan pasca UU 1/2026 = maks 15 thn / denda kat. VII; KUHP 2023 Ps. 391-392 pemalsuan surat, Ps. 486 penggelapan, Ps. 492 penipuan.
- Buat `wiki/kasus/Operasi-Enrekang-2026.md`; update `wiki/index.md` + `wiki/log.md`.

## [2026-09-02] lidik-ulang | Kasus KSPPS Bakti Huria Syariah (snapshot ODS resmi Sep 2026)
- Update `wiki/kasus/KSPPS Bakti Huria Syariah.md`: verifikasi data ODS resmi (badan hukum `14/BH/DK.UKM.20.3/XII/2003`, AHU perubahan AD terbit 17 Feb 2020, pelaporan 10 Jun 2025 = RAT TB2024), koreksi typo profil lama (`DH` → `DK`).
- Temuan: sertifikat NIK **expired 23 Des 2025** (grade C2), register ODS basi (RAT TB2025 26 Mar 2026 & klaim media anggota ±25rb belum masuk vs ODS 13.131), kesehatan belum dinilai, klaim akses **SLIK** (Kredit Multiprima), produk historis "simpanan calon anggota" (riset Unibos 2018 / UIN Alauddin).
- Kerangka: kriteria open-loop **lengkap** POJK 47/2024 Ps. 2(2) huruf a/b/c ditulis ke halaman kasus & konsep `Open Loop Closed Loop`.
- Status: presumsi sah bertahan (terdaftar, RAT rutin, apresiasi Dinas Koperasi Sulsel); gap kritis = Izin Usaha SP + uji open-loop lapangan. Kekuatan konstruksi bank gelap ±25–30% (jujur, naik tipis dari 20–25% bila uji lapangan membuktikan simpanan/pinjaman non-anggota).

## [2026-09-02] ingest | Artikel EMIK 2022 (Pareto/BHS) — data self-disclosed
- Arsip `analisis/bakti-huria-2026/01-ARTIKEL-EMIK-2022-Pareto-BHS.pdf` + `00-INTISARI-EMIK-2022.md` — artikel Amri & Nurjaya, EMIK 5(2) 2022, hal 222–240.
- Data kunci: 25 cabang Sulsel; anggota/mitra 8.119 (2022); aset Rp108 M; DPK Rp28,61 M (2016)→Rp74,85 M (2021); skoring via **Pefindo IDScore**; AO bina 300 anggota; VA Bank Permata; core banking PT Mikro Data; e-RAT sejak 2019; sejarah nama Churia→Huria→KSPPS BHS.
- ⚠️ Penulis-1 (Andi Amri, FEB Univ. Muslim Maros) berpotensi = Ketua BHS → artikel = riset orang dalam, bukan validasi independen (meredam sinyal "objek riset akademik").
- Koreksi lead: klaim "SLIK" (Kredit Multiprima 2026) kemungkinan = pemasaran atas pengecekan via biro kredit (Pefindo IDScore), bukan SLIK OJK langsung → verifikasi ke OJK.
- Update `wiki/kasus/KSPPS Bakti Huria Syariah.md` (sumber + seksi data self-disclosed).

## [2026-09-03] init-kasus | Kredit Plus — Mario Loberto
- Buat `wiki/kasus/Kredit Plus - Mario Loberto.md` sebagai halaman awal perkara.
- Status: menunggu dokumen dan hasil lidik; fakta, peran, alat bukti, kerugian, serta konstruksi pasal belum diverifikasi.
- Siapkan checklist dokumen, agenda verifikasi, matriks unsur/alat bukti, dan follow the money untuk pembaruan bertahap.
- Update `wiki/index.md`.

## [2026-09-03] lidik | Trace telekomunikasi Kredit Plus — Mario Loberto
- Update halaman kasus dengan hasil awal *IMEI history*: satu perangkat dilaporkan berkorelasi dengan 8 MSISDN dari Telkomsel dan Hutchinson/3; nomor awal dan nomor terbaru dimasking.
- Catat lokasi sel wilayah Wajo; label sistem Marannu/Pitumpanua berbeda dengan *reverse geocoding* OSM yang mengembalikan Wajo/La'loa.
- Tandai anomali format: IMEI lokasi 14 digit cocok dengan 14 digit pertama IMEI history; `LAC 351105` tidak sesuai rentang LAC GSM 16-bit dan perlu klarifikasi sebagai TAC/ID internal.
- Dugaan pencabutan SIM untuk mengelabui pelacakan dipertahankan sebagai hipotesis, bukan fakta; perlu korelasi waktu, data resmi operator, dan bukti penguasaan perangkat.
- Identifikator telekomunikasi dan koordinat presisi tidak disimpan dalam wiki yang tersinkron GitHub.

## [2026-09-04] query-save | Penggunaan Identitas dalam Pengajuan Kartu Kredit
- Menyimpan analisis awal konstruksi UU PDP Pasal 65–70, penipuan, pemalsuan surat, UU ITE untuk pengajuan digital, penyertaan, TPPU, tanggung jawab PUJK, tempus delicti, dan prioritas pembuktian.
- Menambahkan sumber lengkap UU Nomor 1 Tahun 2024 Perubahan Kedua UU ITE dari JDIH BPK ke `Hukum Pidana/Regulasi PDP/`.

## [2026-09-04] maintenance | Auto-ingest sumber resmi pemerintah
- Menetapkan aturan tetap: setiap sumber resmi pemerintah/lembaga negara yang ditemukan atau dipakai untuk jawaban penyidikan/hukum harus dicek terhadap vault dan otomatis ditambahkan bila belum tersedia.
- Sumber wajib berasal dari situs resmi, disimpan lengkap pada RAW SOURCES, diverifikasi statusnya, dideduplikasi, disintesis ke wiki, lalu disinkronkan melalui Git.
- Verifikasi sumber dalam pembahasan terakhir: UU 25/1992, Permenkop UKM 8/2023, dan POJK 47/2024 sudah tersedia dalam vault; tidak dibuat duplikat.

## [2026-09-04] ingest | Koperasi Unit Desa (KUD)
- Menambahkan sumber resmi `Inpres No. 4 Tahun 1984` dan `Inpres No. 18 Tahun 1998` dari JDIH BPK.
- Status diverifikasi: Inpres 4/1984 tidak berlaku karena dicabut oleh Inpres 18/1998.
- Membuat `wiki/konsep/Koperasi Unit Desa (KUD).md`: KUD adalah identitas/basis ekonomi pedesaan, bukan bentuk atau jenis badan hukum khusus dalam rezim UU 25/1992; izin mengikuti kegiatan usaha nyata.
- Memperbarui `wiki/index.md`, `INDEX.md`, dan halaman [[Koperasi]].

## [2026-09-04] ingest | Pelindungan Data Pribadi (PDP)
- Audit awal menemukan vault belum memiliki UU PDP atau halaman wiki khusus; hanya rujukan insidental dalam regulasi OJK/P2SK.
- Menambahkan sebelas sumber lengkap: UU 27/2022; PP 33/2026; PP 71/2019; Permenkominfo 20/2016; PP 80/2019; PP 17/2025; Permenkomdigi 9/2026; Kepmenkomdigi 140/2026, 142/2026, dan 219/2026; serta Putusan MK 151/PUU-XXII/2024.
- PP 33/2026 dicatat dengan status temporal: diundangkan 16 Juli 2026, baru mulai berlaku 16 Januari 2027; naskah mirror diverifikasi silang karena URL JDIH resmi belum tersedia saat ingest.
- Membuat `wiki/konsep/Pelindungan Data Pribadi (PDP).md`: peta hak/kewajiban, delik Pasal 65–68, korporasi dan pemulihan aset Pasal 69–70, fokus pembuktian, status aturan pelaksana, serta kesenjangan KB.
- Putusan MK 151/2024 dicatat sebagai norma berlaku: kata “dan” Pasal 53 ayat (1) huruf b dimaknai “dan/atau”.
- Memperbarui `wiki/index.md` dan `INDEX.md`.
## [2026-09-13] tools | Cell ID mapper & TikTok OSINT watch collector
- Menambahkan `tools/cellid-map/` — pemetaan Cell ID/LAC ke area perangkat: lookup, render peta sektor statis (HTML), automasi tautan sector image, dan semantik lookup dibakukan sebagai *estimasi area perangkat* (bukan lokasi presisi). Commit `45a5201`, `9014bac`, `b3243ca`, `02269c0`.
- Menambahkan `tools/tiktok-watch/` — kolektor pemantauan OSINT TikTok. Commit `4c1a93d`.
- Catatan: artefak regenerable (`jadx/`, `blutter-out/`, `apk/`) sudah tercakup `.gitignore`; tidak ada dump decompile yang masuk repo.
- Update `wiki/log.md`.

## [2026-09-14] konten | Brief berita BBM Makassar (produk kerja, bukan fakta vault)
- `berita-bbm-makassar/` — brief/draft/final berbasis atribusi + `source-ledger.md` dan `retrieval.json`: antrean BBM SPBU Makassar 10–13 Sep 2026, seluruh klaim dilekatkan pada sumber (ANTARA, DetikSulsel) dan pernyataan korporasi Pertamina.
- Ditegaskan sebagai produk kerja jurnalistik: keterangan Pertamina tidak dinaikkan menjadi fakta vault tanpa data operasional primer (volume stok, realisasi penyaluran, durasi antrean).
- Tidak dibuat halaman `wiki/` dari materi ini.

## [2026-09-14] maintenance | Audit kebersihan wiki & perbaikan struktur
- **Urutan log dinormalkan** — entry `[2026-09-04] query-save` yang terselip di atas entry Agustus dipindah ke posisi kronologis; konvensi ditetapkan: kronologis menaik, entry baru ditambahkan di AKHIR.
- **Plugin Dataview dipasang** di `.obsidian/plugins/dataview/` (v0.5.68) dan didaftarkan pada `.obsidian/community-plugins.json`, sehingga blok Dataview di `wiki/index.md` aktif setelah mesin Windows melakukan pull.
- **`wiki/index.md`** — frontmatter dilengkapi (`source`, `last_updated`, `related`); kolom "Terakhir" disinkronkan ulang dari frontmatter tiap halaman (Koperasi, Perbankan, KSPPS Bakti Huria Syariah).
- **Wikilink diperbaiki** — rujukan `Inpres No. 4 Tahun 1984` dan `Inpres No. 18 Tahun 1998` kini memakai ekstensi `.pdf` agar resolve ke berkas di `Hukum Keuangan/Regulasi Kemenkop/` (sebelumnya tautan tidak terselesaikan tanpa ekstensi).
- **Scaffolding dibersihkan** — catatan otomatis plugin berbahasa Inggris `wiki/Welcome to Karpathy LLM Wiki.md` dan `Welcome.md` bawaan Obsidian dihapus; isi panduan plugin dipindahkan ke `Panduan Plugin Karpathy LLM Wiki.md` (root, di luar lapisan wiki).
- **`AGENTS.md`** — menambahkan seksi **"Kebersihan berkala (audit)"** (urutan log, sinkron `index.md`, wikilink non-markdown wajib ekstensi, orphan, kelengkapan frontmatter, artefak berat, scaffolding) dan mendokumentasikan plugin `karpathywiki` serta status pemasangan Dataview. Penyisipan ini sempat tertahan gerbang pengaman karena `AGENTS.md` diklasifikasi sebagai berkas instruksi agen; diterapkan setelah Komandan menyetujui secara eksplisit. Pelajaran: perubahan `AGENTS.md` selalu butuh persetujuan pengguna lebih dahulu, jangan diakali lewat jalur lain.
- Hasil audit lain: 0 orphan page; tidak ada berkas `.pyc` atau dump decompile yang ter-track git.

## [2026-09-14] koreksi | "Pergadaian" adalah istilah perundang-undangan, bukan salah tulis
- Usulan normalisasi ejaan `Pergadaian` → `Pegadaian` (diajukan agen saat audit kebersihan hari ini) **DIBATALKAN** setelah verifikasi sumber primer di vault. Tidak ada berkas yang di-rename.
- Bukti: **POJK No. 39 Tahun 2024 berjudul "tentang Pergadaian"**; **UU 21/2011 Ps. 1 angka 10** — "Lembaga Jasa Keuangan Lainnya adalah **pergadaian**, …"; **POJK 47/2024 Ps. 1 angka 13** — "**Perusahaan Pergadaian** adalah badan hukum yang …". Kata "Pegadaian" pada sumber primer muncul hanya sebagai **"PT Pegadaian"** (BUMN), bukan sebagai nama rezim usaha.
- Tindakan: `wiki/entitas/Pergadaian.md` diberi seksi **"Catatan istilah"** (alasan ejaan dipertahankan + rujukan pasal) dan seksi **"Dasar hukum"** (POJK 39/2024, POJK 29/2025, UU 21/2011, POJK 47/2024); alias `Pegadaian` tetap terdaftar sehingga `[[Pegadaian]]` tetap resolve. `wiki/index.md` diberi catatan singkat yang sama.
- Pelajaran: sebelum menormalkan istilah hukum, uji dulu terhadap nama resmi peraturan di lapisan sumber — istilah yang tampak seperti salah tulis bisa justru istilah baku perundang-undangan.

## [2026-09-15] ingest | Regulasi pembiayaan BUS/UUS dan verifikasi identitas/agunan
- Tambah sumber resmi: POJK 42/POJK.03/2017 beserta lampiran, POJK 65/POJK.03/2016, SEOJK 8/SEOJK.03/2015, POJK 19/POJK.03/2018, POJK 1/POJK.07/2013, UU 4/1996 tentang Hak Tanggungan, UU 24/2013 Administrasi Kependudukan, dan UU 1/1946.
- Buat [[Pembiayaan Bank Syariah - Kehati-hatian dan Kualitas Aset]]: peta norma menurut tempus, batas inferensi kolektibilitas 5, serta bukti pembeda pembiayaan yang disengketakan.
- POJK 19/2018 ditandai berlaku 20 September 2018 sehingga tidak dipakai sebagai dasar proses pembiayaan Maret 2018; POJK 1/2013 ditandai berlaku pada 2018 dan dicabut pada 2022.
- Update `INDEX.md`, `wiki/index.md`, dan [[Perbankan]].

## [2026-09-15] ingest | SLIK dan analisis awal kredit atas nama Ria
- Tambah sumber resmi [[POJK No. 18-POJK.03-2017 tentang Pelaporan dan Permintaan Informasi Debitur melalui SLIK.pdf]] dari OJK; PDF 48 halaman tervalidasi.
- Buat [[Kredit atas Nama Ria - Dugaan Penyalahgunaan Identitas]]: fakta awal versus hal yang belum terverifikasi, empat hipotesis, bukti pembeda, jalur pemulihan administrasi SLIK, dan rencana penyelidikan empat tahap.
- Tegaskan: SLIK dikelola OJK tetapi Informasi Debitur bersumber dari Laporan Debitur Pelapor; kolektibilitas 5 tidak membuktikan pelapor mengajukan akad atau menikmati pencairan.
- Update `INDEX.md` dan `wiki/index.md`.

## [2026-09-15] analisis-dokumen | BA interogasi staf collection BSI Makassar 2
- Menelaah BA interogasi saksi staf *Area Collection & Recovery* BSI tertanggal 2026-09-14; dokumen mentah tidak disalin ke vault karena memuat data pribadi.
- Update [[Kredit atas Nama Ria - Dugaan Penyalahgunaan Identitas]]: BA mengonfirmasi catatan sistem/dokumen BSI tentang fasilitas mikro, kol 5, dan klaim proses 2018, tetapi saksi tidak memiliki pengetahuan langsung atas pengajuan, akad, survei, maupun pencairan.
- Catat kontradiksi tempus April 2021 versus Maret 2018, ketidakpastian penyimpanan agunan, ketiadaan Hak Tanggungan, dan kekosongan bukti aliran dana sebagai prioritas lidik.

## [2026-09-15] pengembangan-lidik | Target personel proses pembiayaan Ria
- Update [[Kredit atas Nama Ria - Dugaan Penyalahgunaan Identitas]] dengan urutan target berbasis fungsi: *Sales Officer*, kepala cabang/pemutus, pelaksana survei, analis/administrasi, operasional pencairan, legal/agunan, dan penyimpan berkas.
- Tegaskan Erick Makmur dan Achmad Ramadana Syafmir adalah nama dari BA yang perlu dicari serta diverifikasi jabatan/perannya; bukan penetapan tersangka.
- Tambah daftar data terukur yang diminta dari BSI/HRIS untuk melacak eks-pegawai dan akun kerja secara sah.

## [2026-09-23] ingest | Kasus: Bank Woori Saudara - Kredit Fiktif KUPEG TNI
- Menerima berkas arsip 8 Berita Acara Interogasi (BAI): BA Pelapor (Muhammad Wildan - Pinca BWS Makassar), BAI Muhammad Yunus (terlapor/eks RO), BAI Henny Adam alias Hendro (perekrut sipil), BAI Febe Marla Ginting (eks agen BWS/istri Hendro), BAI Hamdanil (debitur boneka non-TNI), BAI Rahmat (driver ojol penyedia rekening penampung cicilan), BAI Yos Makatengkeng (calo adminduk Dukcapil), BAI Rio Milanda (Kabag Ops BWS).
- Mengisolasi dokumen ke `raw/bank-woori-saudara/` dan membuat register perkara serta matriks analisis ketat fakta vs inferensi vs unknown di `analisis/bank-woori-saudara-2026/README.md`.
- Membuat halaman wiki `wiki/kasus/Bank Woori Saudara - Kredit Fiktif KUPEG TNI.md`: rekonstruksi modus pencairan Rp 7,189 Miliar, 30 debitur non-TNI berdandan militer, TTD di Hotel Arthama Makassar, dan rekayasa pembayaran cicilan via M-Banking Mandiri driver ojol oleh terlapor M. Yunus.
- Update `wiki/index.md` dan `wiki/log.md`.

## [2026-09-23] ingest-finansial | Mutasi Rekening BNI Terlapor M. Yunus (2022-2025)
- Mengarsip mutasi rekening BNI Taplus `1373172229` a.n. MUH YUNUS (22.883 transaksi, periode 11 Apr 2022 s.d. 31 Des 2025) ke `raw/bank-woori-saudara/mutasi_bni_yunus/`.
- Temuan korelasi mutlak (*follow the money*): Inflow setor tunai BNI Yunus sebesar Rp 6.876.370.000,- (korelasi identik kerugian BWS Rp 7,189 M).
- Temuan transfer keluar (*layering/cover-up*): M. Yunus mentransfer 126 kali total Rp 476.320.000,- ke rekening Bank Mandiri `1520016332484` milik saksi RAHMAT (driver ojol) untuk membayarkan angsuran gali lubang tutup lubang 11 debitur fiktif BWS.
- Temuan indikasi TPPU aset: Pembelian Ruko Blok H No. 17c (Rp 1,999 Miliar) dan sewa properti (Rp 3,058 Miliar).
- Update register perkara dan halaman kasus wiki.

## [2026-09-23] update-hukum | Re-parsing 4 UU Utama via Docling GPU
- Mengganti teks lapisan sumber 4 undang-undang pilar dengan hasil ekstraksi Docling 2.130.0 (CUDA accelerated):
  1. `Hukum Pidana/UU 1 Tahun 2026 Penyesuaian Pidana.md` (tabel konversi denda pengganti pidana penjara kini utuh sebagai tabel Markdown terstruktur).
  2. `Hukum Pidana/KUHP - UU 1 Tahun 2023.md` (hierarki bab, bagian, paragraf, pasal, dan penjelasan umum/pasal rapi).
  3. `Hukum Keuangan/UU Nomor 4 Tahun 2023 P2SK.md` (struktur bab dan pasal anchor 237 jo 305 terstruktur jelas).
  4. `Hukum Keuangan/UU Nomor 4 Tahun 2026 Perubahan UU P2SK.md` (kewenangan penyidikan SJK Pasal 278A-278O dan Bab Keadilan Restoratif terkonversi presisi).
- Menjaga metadata YAML frontmatter Obsidian dan menormalkan OCR glitch pada nomor pasal utama.
- Git commit & push ke GitHub private `isikepalaku/vault-hukum`.

## [2026-09-23] ingest-hukum | Putusan MK Fidusia & Update Doktrin Eksekusi
- Mengunduh dan mengonversi berkas resmi salinan putusan Mahkamah Konstitusi:
  1. `Hukum Keuangan/Regulasi Fidusia/Putusan MK No. 18-PUU-XVII-2019 Eksekusi Jaminan Fidusia.md` (putusan monumental pembatalan eksekusi sepihak leasing tanpa kesepakatan wanprestasi sukarela).
  2. `Hukum Keuangan/Regulasi Fidusia/Putusan MK No. 2-PUU-XIX-2021 Penegasan Eksekusi Fidusia.md` (penegasan kembali bahwa wanprestasi tidak dapat ditentukan sepihak).
- Memperbarui halaman wiki `wiki/entitas/Fidusia.md`:
  - Menambahkan doktrin eksekusi pasca Putusan MK 18/2019 dan 2/2021 (gugurnya parate eksekusi sepihak, kewajiban fiat eksekusi PN).
  - Menetapkan batas tegas garis merah pidana *debt collector* / mata elang (Pasal 368 KUHP pemerasan, Pasal 365 KUHP pencurian dgn kekerasan, Pasal 306 UU P2SK intimidasi penagihan).
  - Melengkapi SOP pembuktian Pasal 36 UU 42/1999 bagi penyidik (pengalihan objek tanpa izin).
- Update `wiki/index.md`.

## [2026-09-23] maintenance | Pembersihan Berkas Ekspor Artikel dari Vault
- Menghapus folder kerja `berita-bbm-makassar/` dan berkas tercecer `sintesis-ai-pangkas-klik-organik-pergeseran-peran-website.md` dari tracking git vault.
- Seluruh berkas dipindahkan ke lokasi eksternal `E:\project\artikel\` agar vault Obsidian murni hanya berisi KB hukum & kasus penyidikan.

## [2026-09-23] refactor-kategori | Elevasi Hukum Siber Menjadi Pilar Utama Top-Level
- Mereorganisasi struktur kategori vault agar selaras dengan pemisahan subdit operasional di Ditreskrimsus (Subdit II Fismondev, Subdit V Siber, dan Kodifikasi Pidana Umum).
- Membentuk folder tingkat atas baru: `Hukum Siber/` sejajar dengan `Hukum Keuangan/` dan `Hukum Pidana/`.
- Memindahkan regulasi terkait siber dan data digital ke bawah `Hukum Siber/`:
  - `Hukum Siber/Regulasi ITE & Cyber Crime/` (UU 11/2008, UU 19/2016, UU 1/2024, SKB 2021).
  - `Hukum Siber/Regulasi PDP & Sistem Elektronik/` (UU 27/2022 PDP, PP 33/2026, PP 71/2019, PP 80/2019, PP 17/2025, Permenkominfo/Permenkomdigi, Putusan MK 151/2024).
- `Hukum Pidana/` kini murni menampung kodifikasi pidana materiil & formil umum (KUHP UU 1/2023, KUHAP UU 20/2025, UU 1/2026 Penyesuaian Pidana, Putusan MK KUHP, Regulasi Historis).
- Memperbarui `AGENTS.md` (skema pilar sumber RAW), `INDEX.md` (navigasi MOC 3 pilar), dan `wiki/index.md`.
- Git commit & push ke GitHub private `isikepalaku/vault-hukum`.

## [2026-09-23] ingest-regulasi | Peraturan Turunan & Pelaksana Cyber ITE
- Menambahkan 6 instrumen regulasi turunan dan operasional ke `Hukum Siber/Regulasi ITE & Cyber Crime/`:
  1. `Permenkominfo Nomor 5 Tahun 2020 tentang Penyelenggara Sistem Elektronik Lingkup Privat` (kewajiban PSE privat memberikan data lalu lintas/pengguna dan akses penegakan hukum ke Polri, takedown konten 4 jam/24 jam).
  2. `Permenkominfo Nomor 10 Tahun 2021 tentang Perubahan atas Permenkominfo 5-2020 tentang PSE Lingkup Privat` (pendaftaran OSS & penataan mekanisme perlindungan data).
  3. `Surat Edaran Kapolri Nomor SE-2-II-2021 tentang Penegakan Hukum UU ITE` (pedoman penanganan perkara ITE oleh penyelidik/penyidik Polri, mediasi wajib pelapor langsung, batasan restorative justice).
  4. `Perpres Nomor 82 Tahun 2022 tentang Pelindungan Infrastruktur Informasi Vital` (sektor keuangan, energi, TIK, transportasi, kesehatan; CSIRT & wajib lapor breach 1x24 jam).
  5. `Permenkominfo Nomor 19 Tahun 2014 tentang Penanganan Situs Internet Bermuatan Negatif` (sistem Trust Positif, domain/IP blacklist, mekanisme pemblokiran ISP).
  6. `Instruksi Menteri Kominfo Nomor 1 Tahun 2023 tentang Pemberantasan Perjudian Online` (crawling AI, sapu bersih judol/slot, takedown massal, koordinasi pemblokiran rekening bank & pelimpahan Bareskrim).
- Memperbarui `INDEX.md` dan halaman wiki konsep `[[UU ITE]]`.
- Git commit & push ke GitHub private `isikepalaku/vault-hukum`.

## [2026-09-23] create-kategori | Kategori Baru Subdit Tipidter & Cipta Kerja
- Membentuk pilar kategori baru di Obsidian Vault: `Hukum Tipidter/` yang sejajar dengan `Hukum Keuangan/`, `Hukum Siber/`, dan `Hukum Pidana/` merefleksikan yurisdiksi Subdit IV Ditreskrimsus.
- Memindahkan dan mengorganisasi 15 berkas hasil konversi Docling CUDA dari `E:\UU\ciptakerja\` ke dalam:
  1. `Hukum Tipidter/Regulasi Cipta Kerja & Sektoral/`:
     - `UU Nomor 6 Tahun 2023 tentang Cipta Kerja.md` (Omnibus Utama, 1.127 hal)
     - `UU Nomor 2 Tahun 2025 tentang Perubahan Keempat UU Minerba.md` (PETI Ps. 158/161)
     - `UU Nomor 66 Tahun 2024 tentang Perubahan Ketiga UU Pelayaran.md` (Kemaritiman & SPB)
     - `UU Nomor 18 Tahun 2025 tentang Perubahan Ketiga UU Kepariwisataan.md` (Perizinan Pariwisata)
     - `UU Nomor 65 Tahun 2024 tentang Perubahan Ketiga UU Paten.md` (Kekayaan Intelektual)
     - `UU Nomor 63 Tahun 2024 tentang Perubahan Ketiga UU Keimigrasian.md` (Pengawasan TKA & Keimigrasian)
     - `UU Nomor 3 Tahun 2024 tentang Perubahan Kedua UU Desa.md` (Tata Kelola Aset & Wilayah Desa)
     - `UU Nomor 1 Tahun 2025 tentang Perubahan Ketiga UU BUMN.md` & `UU Nomor 16 Tahun 2025 tentang Perubahan Keempat UU BUMN.md`
     - `UU Nomor 14 Tahun 2025 tentang Perubahan Ketiga UU Haji dan Umrah.md` (Perizinan PPIU/PIHK)
     - `UU Nomor 5 Tahun 2026 tentang Perubahan Ketiga UU Kepolisian.md` (Kewenangan Penyidikan Polri)
     - `UU Nomor 1 Tahun 2026 tentang Penyesuaian Pidana.md` (Harmonisasi Pidana Sektoral)
  2. `Hukum Tipidter/Putusan MK/`:
     - `Putusan MK 168-PUU-XXI-2023 Uji Materi UU Cipta Kerja (Ketenagakerjaan).md` (Koreksi Fundamental Ketenagakerjaan: Outsourcing, PKWT maks 5 thn, Upah Minimum, Pesangon)
     - `Putusan MK 273-PUU-XXIII-2025 Uji Materi UU Cipta Kerja (Tarif Telekomunikasi).md`
     - `Putusan MK 39-PUU-XXI-2023 Formil UU Cipta Kerja.md`
- Membuat halaman wiki LLM Wiki baru:
  1. `wiki/entitas/Tipidter.md` — Yurisdiksi Subdit IV Tipidter Ditreskrimsus, delik inti PETI Minerba, PPLH (pencemaran/limbah B3), perambahan hutan/illegal logging, BBM bersubsidi, ketenagakerjaan pasca Putusan MK 168/2023, doktrin ultimum vs premium remedium, serta SOP dan checklist lidik/sidik lapangan.
  2. `wiki/konsep/Perizinan Berusaha & Cipta Kerja.md` — Kerangka Perizinan Berusaha Berbasis Risiko (OSS-RBA: Rendah, Menengah Rendah, Menengah Tinggi, Tinggi), 3 persyaratan dasar (KKPR, AMDAL/UKL-UPL, PBG/SLF), batas demarkasi sanksi administratif vs delik pidana langsung, serta penyesuaian sanksi UU 1/2026.
- Memperbarui `INDEX.md` (menambahkan seksi navigasi lengkap Tipidter), `AGENTS.md` (menambahkan pilar ke-4 raw sources), dan `wiki/index.md` (katalog entitas dan konsep).
- Git commit & push ke GitHub private `isikepalaku/vault-hukum`.

## [2026-09-23] ingest-regulasi | UU Kesehatan & UU Minyak dan Gas Bumi (Tipidter)
- Menambahkan 2 regulasi krusial Tipidter ke `Hukum Tipidter/Regulasi Cipta Kerja & Sektoral/` via Docling CUDA:
  1. `UU Nomor 17 Tahun 2023 tentang Kesehatan.md` (Omnibus Law Kesehatan, 300 hal, 371 KB):
     - Delik peredaran sediaan farmasi/alkes tak berstandar (Pasal 435, maks 12 thn / Denda Kat. VII).
     - Sediaan farmasi/alkes tanpa izin edar & kosmetik ilegal bermerkuri (Pasal 436, maks 5 thn / Denda Kat. V).
     - Penyelenggaraan fasyankes ilegal (Pasal 439).
     - Praktik kedokteran ilegal tanpa STR/SIP / dokter gadungan (Pasal 441).
     - Aborsi ilegal (Pasal 427 & 428).
  2. `UU Nomor 22 Tahun 2001 tentang Minyak dan Gas Bumi.md` (53 hal, 75 KB):
     - Usaha niaga/pengolahan/pengangkutan migas tanpa izin berusaha (Pasal 53).
     - Pemalsuan/pengoplosan BBM (Pasal 54).
     - Penyalahgunaan pengangkutan/niaga BBM bersubsidi (Solar/Pertalite) & LPG 3 kg (Pasal 55 jo UU Cipta Kerja).
- Memperbarui halaman wiki `wiki/entitas/Tipidter.md` dengan matriks unsur delik, modus operandi lapangan (helikopter tank, pengerukan gudang timbun, suntik LPG), dan checklist SOP lidik/sidik farmasi & migas.
- Memperbarui `INDEX.md` dan melakukan sinkronisasi Git commit & push ke GitHub private `isikepalaku/vault-hukum`.

## [2026-09-24] create-kategori | Kategori Mindik & Skill Mindik SOP Perkaba
- Membuat folder baru `Mindik/` di Obsidian Vault (`E:\Agent\UU\Mindik\`):
  1. `Mindik/Contoh Format Dokumen/`:
     - `CONTOH BAP SAKSI.docx` (Naskah asli Word standar SOP Perkaba)
     - `CONTOH BAP SAKSI.jsonl` (Skema semantik 13 blok struktural data per baris lengkap dengan style rules)
     - `CONTOH BAP SAKSI.md` (Hasil parsing Docling murni ke Markdown)
     - `CONTOH BAP SAKSI_docling.json` (AST JSON pohon sintaks dokumen Docling)
     - `TEMPLATE_BAP_SAKSI_STANDAR_POLRI.md` (Template prompt BAP Saksi berbasis variabel untuk LLM)
  2. `Mindik/Petunjuk Teknis/`:
     - `Petunjuk Teknis Pembuatan BAP Saksi.md` (Juknis komprehensif tipografi Arial Narrow 12pt justify, line fillers `-----`, anatomi 13 blok, dan formula tanya jawab ADI DEMEN BABI).
- Membuat halaman wiki `wiki/entitas/Mindik Polri.md` (Katalog tipologi dokumen formil Mindik, prinsip pemisahan format statis vs materi dinamis, SOP Perkaba).
- Membuat skill baru `mindik` (penyidikan) di Hermes Agent untuk memandu AI menyusun dan memvalidasi dokumen BAP sesuai standar baku.
- Memperbarui `INDEX.md`, `AGENTS.md`, dan `wiki/index.md`.
- Sinkronisasi Git commit & push ke GitHub private `isikepalaku/vault-hukum`.

## [2026-10-01] ingest | Korpus Administrasi Kependudukan (Adminduk, SIAK, IKD)
- Menambahkan 7 regulasi kanonik Administrasi Kependudukan ke `Hukum Pidana/Regulasi Administrasi Kependudukan/`:
  1. `Undang-Undang Nomor 23 Tahun 2006 tentang Administrasi Kependudukan.md` (UU Dasar Adminduk).
  2. `Undang-Undang Nomor 24 Tahun 2013 tentang Perubahan atas UU 23-2006 tentang Administrasi Kependudukan.md` (KTP-el seumur hidup, delik manipulasi petugas Ps. 94/95B, akses database tanpa hak Ps. 95A).
  3. `Peraturan Pemerintah Nomor 40 Tahun 2019 tentang Pelaksanaan UU Administrasi Kependudukan.md` (Penyelenggaraan pendaftaran penduduk dan tata kelola data nasional).
  4. `Peraturan Presiden Nomor 96 Tahun 2018 tentang Persyaratan dan Tata Cara Pendaftaran Penduduk dan Pencatatan Sipil.md` (Tata cara penerbitan KK, KTP-el, dan SKPWNI).
  5. `Permendagri Nomor 108 Tahun 2019 tentang Peraturan Pelaksanaan Perpres 96-2018 (Pendaftaran Penduduk dan Pencatatan Sipil).md` (Juklak operasional pindah datang dan penerbitan dokumen).
  6. `Permendagri Nomor 95 Tahun 2019 tentang Sistem Informasi Administrasi Kependudukan.md` (Arsitektur SIAK, hak akses, audit trail pendaftaran data).
  7. `Permendagri Nomor 72 Tahun 2022 tentang Standar Blangko KTP-el dan Penyelenggaraan Identitas Kependudukan Digital.md` (Standar KTP-el dan tata cara penyelenggaraan resmi IKD).
- Membuat konsep wiki: `wiki/konsep/Administrasi Kependudukan & Kejahatan Identitas.md` (pemetaan pasal pidana sektoral, penyesuaian ancaman pidana UU 1/2026, tipologi kejahatan bypass SKPWNI fiktif, NIK ganda/manipulatif, social engineering APK IKD palsu, dan pedoman audit trail SIAK / TTE BSrE).
- Memperbarui katalog `INDEX.md` dan `wiki/index.md`.
- Sinkronisasi Git commit & push ke GitHub private `isikepalaku/vault-hukum`.

## [2026-10-01] intake | Berkas Perkara PT KB Finansia Multi Finance (Kredit Plus) Cab. Sudiang — Tsk Mario Loberto
- Menerima dan mengisolasi 18 berkas perkara primer (format DOCX/PDF) dari arsip `SUB2.zip` ke `raw/kredit-plus-sudiang/`.
- Membuka workspace analisis aktif di `analisis/kredit-plus-sudiang-2026/README.md` lengkap dengan Register Penerimaan Dokumen (18 BAP & Resume perkara) serta Matriks Pemisahan Fakta Hukum.
- Memperbarui halaman perkara `wiki/kasus/Kredit Plus - Mario Loberto.md` dari tahap lidik ke penyidikan (Resume selesai):
  - Tersangka: Mario Loberto Paulus Tampubolon bin Yohanis Tampubolon, S.TP. (Branch Manager PT KB Finansia Cab. Sudiang).
  - Dasar hukum: LPB/779/VIII/2023/SPKT/POLDA SULSEL, persangkaan Pasal 35 UU No. 42 Tahun 1999 tentang Jaminan Fidusia.
  - Modus operandi: Merekayasa pembelian dump truck bekas (milik Hamka Gaffar) menjadi pembiayaan Sale and Leaseback an. anak nasabah (Mulyadi Amri) demi menghindari batas usia debitur riil (Amri Haji Sia >60 thn), serta menggelapkan dana angsuran Rp 33.350.000,-.
  - Skala fraud internal: 18 debitur dengan 49 fasilitas pembiayaan bermasalah berdasarkan Laporan Hasil Investigasi Fraud KP Jakarta Ref. 001/LHI/III/2023.
- Menautkan perkara ke daftar kasus pada `INDEX.md` dan `wiki/index.md`.
- Ingest Surat Pemberitahuan Hasil Penyidikan Lengkap (**P-21**) dari Kejaksaan Negeri Makassar No. `B-7820/P.4.10/Eku.1/09/2026` tertanggal 29 September 2026 (ditandatangani Kajari Makassar Andi Panca Sakti, S.H., M.H.):
  - Persangkaan P-21: Pasal 35 UU No. 42/1999 tentang Jaminan Fidusia jo. Lampiran II UU No. 1 Tahun 2026 tentang Penyesuaian Pidana.
  - Penetapan jadwal Tahap II (Penyerahan Tersangka & Barang Bukti): Selasa, 13 Oktober 2026 pukul 11.00 WITA di Ruang Tahap II & Gudang Barang Bukti Kejari Makassar.

## [2026-10-07] sync | Sinkronisasi Git + ingest berkas kasus baru (BFI Finance Hino & BSI/Ria)
- `git pull --rebase origin main` → **Already up to date** (tidak ada commit baru dari mesin lain; tanpa konflik).
- Ingest berkas kerja lokal yang belum tersinkron (hasil operasi 7 Okt 2026), semuanya commit + push:
  - `analisis/bfi-finance-hino-2026/ANALISIS_AWAL_LP_1193_X_2026.md` dan `raw/bfi-finance-hino-2026/LP_HAL_1.jpg`, `LP_HAL_2.jpg` — berkas perkara **baru**: dugaan pengalihan objek jaminan fidusia 1 unit Truk Hino Dutro-136 HDX an. Terlapor Hamka Rahman (Maros); LP/B/1193/X/2026/SPKT/Polda Sulsel tgl 5 Okt 2026; kerugian dilaporkan Rp 431.000.000,-; kompensasi pengalihan Rp 22.000.000,-.
  - `raw/bank-syariah-indonesia/SURAT_PERMOHONAN_SAKSI_DOKUMEN_KP_BSI.md` dan `SURAT_UNDANGAN_KLARIFIKASI_2_ERICK_MAKMUR.md` — dua draf surat keluar tahap lidik kasus Ria (permohonan saksi & dokumen ke Kantor Pusat BSI; undangan klarifikasi ke-2 eks Sales Officer Erick Makmur).
- Halaman wiki baru: `wiki/kasus/BFI Finance - Pengalihan Objek Fidusia Hino (Hamka Rahman).md` — konstruksi tentatif **Pasal 36 jo. Pasal 23 ayat (2) UU No. 42/1999** (lex specialis; pidana maks 2 thn / denda maks Rp 50 jt, disesuaikan pasca UU 1/2026), temuan kontradiksi *tempus delicti* (13 Apr vs 13 Nov 2025), checklist pulbaket (Surat Kuasa Direksi, akad, AJF, sertifikat fidusia Kemenkumham, riwayat angsuran/SP), dan risiko pembuktian.
- Update `wiki/kasus/Kredit atas Nama Ria - Dugaan Penyalahgunaan Identitas.md`: seksi **"Perkembangan penyelidikan (Oktober 2026)"** — status lidik aktif (LI/653/VIII/RES.2.2./2026), dua draf surat keluar, dasar hukum **Pasal 63 UU 21/2008 dan/atau Pasal 263 KUHP**, catatan bahwa nomor/jadwal surat masih blanko (draf, belum formil).
- Update katalog `wiki/index.md` (baris kasus baru BFI Finance + penyegaran baris Ria; `last_updated` → 2026-10-07) dan `INDEX.md` (daftar kasus wiki).
- Sinkronisasi git: `git add -A` → commit → `git pull --rebase` → push ke GitHub private `isikepalaku/vault-hukum`.


## [2026-10-12] sync | Sinkronisasi Git + ingest papan analisis Sindikat Passobis
- `git pull --rebase origin main` → **Already up to date** (tidak ada commit baru dari mesin lain; tanpa konflik).
- Ingest artefak analisis lokal yang belum tersinkron (hasil kerja 12 Okt 2026, tidak termasuk berkas sumber hukum baru):
  - `analisis/board_keterkaitan_sindikat_passobis.html` (papan `link analysis`), `analisis/board_keterkaitan_sindikat_passobis.excalidraw` (sumber editable), `analisis/board_keterkaitan_sindikat_passobis.png` (render), dan generator `analisis/generate_board.py`.
- Halaman wiki baru: `wiki/kasus/Sindikat Passobis - Penipuan Telepon Bertarget Toraja-Enrekang-Makassar.md` — pemetaan korban (2 kejadian, Rp 3,45 jt; ralat status: korban materiil = orang tua, Revas & Riad = narahubung), 4 SIM Indosat/by.U/Telkomsel dibinding satu IMEI iPhone XR `353068103923504` (shared device pasutri, lokasi Curio–Enrekang), eksekutor lapangan + 2 rekening penampung (Mandiri & BNI Taplus) di Bara-Baraya/Tamalate Makassar; konstruksi tentatif **Pasal 492 KUHP Nasional** (4 thn / kat. V) jo. **Pasal 20 & 21 KUHP Nasional**, alternatif Pasal 28(1) jo. 45A UU ITE, TPPU **Pasal 5 UU 8/2010** untuk pemilik rekening penampung (kap 15 thn via UU 1/2026) dan Pasal 591 KUHP Nasional (penadahan); checklist pulbaket (verifikasi formil LP/LI, data pelanggan operator, uji binding IMEI, izin rahasia bank POJK 44/2024, follow the money, data kependudukan) + catatan kelemahan (tanpa dokumen formil, tag Getcontact bukan alat bukti).
- Identifikator sensitif (NIK, nomor SIM/rekening penuh) sengaja tidak ditulis di halaman wiki — mengikuti konvensi privasi; data penuh ada di artefak `analisis/board_*`.
- Update katalog `wiki/index.md` (baris kasus baru; `last_updated` → 2026-10-12) dan `INDEX.md` (daftar kasus wiki).
- Sinkronisasi git: `git add -A` → commit → `git pull --rebase` → push ke GitHub private `isikepalaku/vault-hukum`.

## [2026-10-13] sync | Sinkronisasi Git + ingest telaahan yuridis Tahap II Kredit Plus (Mario Loberto)
- `git pull --rebase origin main` → **Already up to date** (tidak ada commit baru dari mesin lain; tanpa konflik).
- Ingest artefak kerja lokal yang belum tersinkron (hasil operasi 12–13 Okt 2026, tidak termasuk berkas sumber hukum baru): `analisis/kredit-plus-sudiang-2026/TELAAHAN_TAHAP_2_FIDUSIA.md` (+ `.html`/`.pdf`) dan `analisis/kredit-plus-sudiang-2026/TELAAHAN_TAHAP_2_MARIO_LOBERTO.html` (+ `.pdf`).
- Update halaman perkara `wiki/kasus/Kredit Plus - Mario Loberto.md`: seksi baru **"Telaahan Yuridis Tahap II (12–13 Oktober 2026)"** —
  - Pendampingan Penasihat Hukum **tidak wajib** pada Tahap II Pasal 35 UU 42/1999: ancaman maksimal 5 tahun berada di bawah ambang *mandatory legal counsel* Pasal 56 ayat (1) KUHAP (pidana mati / ≥15 tahun / di atas 5 tahun bagi yang tidak mampu); kedudukan PH = hak tersangka (Pasal 54 KUHAP), tahap II tetap sah dengan Surat Pernyataan Menolak Didampingi PH.
  - Pendampingan keluarga tidak disyaratkan KUHAP, tetapi taktis sebagai penjamin bila JPU mempertimbangkan penahanan.
  - Penahanan pasca Tahap II = **wewenang mutlak JPU**: syarat objektif Pasal 21 ayat (4) huruf a KUHAP terpenuhi (ancaman 5 tahun atau lebih), sehingga JPU dapat menerbitkan Form T-4 tanpa memandang status tidak-ditahan di Kepolisian.
  - Checklist taktis: klausul "dapat didampingi PH dan/atau keluarga" pada surat panggilan; Surat Keterangan Sehat + bebas narkoba (Biddokkes) sebelum berangkat; kesiapan keluarga (KTP + surat permohonan penangguhan penahanan).
  - Penyesuaian UU 1/2026: pidana minimum khusus dihapus, denda dikonversi ke Kategori IV Pasal 79 KUHP (maks Rp 200 jt), kap penjara tetap 5 tahun.
- **Catatan defisit berkas**: telaahan `TELAAHAN_TAHAP_2_MARIO_LOBERTO` hanya ada dalam format render (`.html`/`.pdf`); berkas sumber `.md` (editable) tidak ditemukan di vault → perlu dibuat/di-restore agar revisi telaahan tidak bergantung pada render ulang.
- Update katalog `wiki/index.md` (penyegaran baris kasus Kredit Plus; `last_updated` → 2026-10-13). `INDEX.md` tidak berubah (daftar kasus sudah memuat tautan).
- Sinkronisasi git: `git add -A` → commit → `git pull --rebase` → push ke GitHub private `isikepalaku/vault-hukum`.

## [2026-10-16] sync | Sinkronisasi Git + ingest analisis statis APK Anggotaku (REA)
- `git pull --rebase origin main` → **Already up to date** (tidak ada commit baru dari mesin lain; tanpa konflik; divergensi `origin/main...HEAD` = 0/0). Tidak ada berkas baru/berubah di `Hukum Keuangan/`, `Hukum Pidana/`, maupun `wiki/` dari remote.
- Ingest artefak analisis lokal yang belum tersinkron (hasil kerja 16 Okt 2026, tidak termasuk berkas sumber hukum baru):
  - `analisis/bakti-huria-2026/02-PETA-WORKFLOW-DAN-IDENTITAS-ANGGOTAKU.md` — peta workflow & identitas aplikasi ANGGOTAKU (`com.baktihuria.mobilebmt.anggotaku`, v9.1.2) hasil REA 6.4.0 (jadx-headless 0.7.1 + Apktool 2.7.0), metode **statis — APK tidak pernah dieksekusi**; SHA-256 berkas identik dengan triase 22 Sep 2026.
  - `analisis/bakti-huria-2026/rea/` — register evidence REA (`01-package.yaml`, `02-allclasses.yaml`, `02-classes-own.txt`, `10-class-01…09-*.yaml`, `20-xref-*.yaml`, `evidence-index.json`, `evidence-index-xref.json`, `run_map.sh`), seluruhnya `confidence: observed` / `coverage: complete`, dengan `evidence_id` per operasi.
  - `analisis/bakti-huria-2026/LAPORAN-PIMPINAN-ANGGOTAKU.pdf` + `presentasi-anggotaku.html` — produk laporan pimpinan & materi paparan.
- Update halaman perkara `wiki/kasus/KSPPS Bakti Huria Syariah.md`: seksi baru **"Analisis statis APK Anggotaku — REA 6.4.0 (16 Okt 2026)"** —
  - Rantai workflow terkonfirmasi silang via `trace_android_references`: `SplashActivity` → `ControllerActivity` → `PreRegistrasiActivity` → `Registrasi2Activity` → `IsiFormulirActivity` → `IsiFormulirBerkasActivity` → `AktivasiActivity` → `BaruPin` → dashboard.
  - Akun terikat pada **perangkat + SIM** (`imsi` = turunan `android_id` + ID langganan SIM, plus fingerprint `Build.*`/`rooted`); relevan untuk mendeteksi agen/pihak ketiga yang mengoperasikan akun orang lain.
  - Teks resmi `strings.xml` menegaskan gerbang keanggotaan (nomor registrasi dari CS, formulir diisi di kantor layanan) → memperkuat argumen *closed-loop* pada lapisan aplikasi, **bukan pembuktian** status anggota di basis data.
  - **Koreksi triage otomatis 22 Sep** ("CRITICAL / MALICIOUS skor 130"): tidak berdasar — tidak ada izin SMS/aksesibilitas/notification-listener/overlay, tidak ada `SmsManager`. Fokus perkara tetap regulasi & operasional, bukan malware.
  - Batas analisis: seluruh base URL/kredensial/path API berada di `libnative-lib.so` via JNI dan berkas ini base APK App Bundle **tanpa entri `lib/…`** → endpoint server tidak terbukti; perlu `.xapk`/`.apks` lengkap.
  - ⚠️ **Berkas ditandatangani ulang pihak ketiga** (hash AGP stamp ≠ hash sertifikat aktif) → tidak dapat dipastikan bit-identik dengan distribusi Play Store; cacat potensial chain of custody bila dijadikan lampiran BAP.
  - Vendor core banking teridentifikasi: **PT USID / PT UGT System Integrator**, infrastruktur Firebase `usid-mobile-3` — kandidat permintaan keterangan.
  - Checklist lidik butir 5 ditandai **sebagian terjawab**; `status` kekuatan perkara tidak berubah (uji lapangan open-loop tetap penentu).
- Update katalog `wiki/index.md` (penyegaran baris kasus KSPPS Bakti Huria Syariah + `last_updated` → 2026-10-16). `INDEX.md` tidak berubah (daftar kasus sudah memuat tautan).
- Sinkronisasi git: `git add -A` → commit → `git pull --rebase` → push ke GitHub private `isikepalaku/vault-hukum`.


## [2026-10-16] analisis | Draft paparan PPTX Workshop Tertutup OVO & OVO Finansial (Ditreskrimsus Polda Sulsel)
- Konteks: undangan narasumber dari PT Visionet Internasional (OVO) & PT Indonusa Bara Sejahtera (OVO Finansial), Surat No. 338/PA-VI/C/IX/2026 (Jakarta, 29 Sep 2026). Acara: Kamis, 22 Okt 2026, 13.00-16.35 WITA, Hotel Hyatt Place Makassar. Sesi Ditreskrimsus 14.25-15.10 (45 menit).
- Produk: `analisis/workshop-ovo-2026/Draf_Paparan_Kejahatan_Keuangan_Berbasis_AI_Ditreskrimsus_Polda_Sulsel.pptx` — **29 slide**, 16:9, tema biru-navy/merah, font Tahoma, lengkap dengan **catatan pembicara** pada setiap slide. Skrip pembangun dapat direproduksi: `analisis/workshop-ovo-2026/build_deck.py`.
- Struktur: (I) dinamika makro TKM & pergeseran kanal QRIS; (II) studi kasus botnet Makassar (2.000+ akun bot, 180 situs) + anatomi structuring/smurfing; (III) vektor eksploitasi AI (e-KYC injection attack, deepfake, identitas sintetik, akun dorman, merchant fiktif/agregator); (IV) kerangka hukum; (V) tantangan yuridis & dampak bansos 1,49 juta KPM; (VI) empat rekomendasi + peta jalan 90 hari.
- **Dasar hukum yang diverifikasi ke teks UU di vault** (bukan asumsi):
  - KUHP (UU 1/2023, berlaku 2 Jan 2026) — Ps. 332 (akses ilegal; menggantikan UU ITE Ps. 30 jo. 46), Ps. 258 (penyadapan; menggantikan UU ITE Ps. 31 jo. 47), Ps. 426 (perjudian; maks 9 thn / denda kat. VI), Ps. 492 (penipuan; maks 4 thn / kat. V), Ps. 486 (penggelapan; maks 4 thn / kat. IV), Ps. 607 (TPPU; maks 15 thn & denda kat. VII), Ps. 607(1)c (maks 5 thn), Ps. 608 (pengecualian pihak pelapor APU-PPT).
  - Pengalihan pengacuan UU ITE ke KUHP tercantum dalam lampiran KUHP (Ps. 622) — huruf r & ayat (10): 27(1)&45(1) -> Ps. 407; 27(3)&45(3) -> Ps. 441; 28(2)&45A(2) -> Ps. 243; 30&46 -> Ps. 332; 31&47 -> Ps. 258 ayat (2). TPPU UU 8/2010 Ps. 2(1), 3, 4, 5 -> KUHP Ps. 607-608.
  - KUHAP (UU 20/2025, berlaku 2 Jan 2026) **Ps. 140** — pemblokiran oleh Penyidik/PU/Hakim wajib izin ketua PN (ayat 2); jangka 1 tahun + perpanjangan 2x6 bulan (ayat 6); **keadaan mendesak dapat blokir tanpa izin ketua PN** (ayat 7), meliputi potensi pengalihan harta, TP terkait ITE, dan permufakatan terorganisasi (ayat 8), persetujuan diminta maks 2x24 jam (ayat 9), penetapan/penolakan (ayat 10-12), pembukaan blokir maks 3 hari kerja (ayat 13); Ps. 136 penyadapan.
  - UU ITE jo. UU 1/2024 — Ps. 27 ayat (2) judi online dengan ancaman **Ps. 45 ayat (3): maks 10 thn dan/atau Rp10 miliar**; Ps. 28(1) jo. 45A(1) maks 6 thn/Rp1 miliar; **Ps. 43 ayat (5) huruf l**: perintah pemutusan akses sementara atas akun medsos, rekening bank, uang elektronik, dan aset digital; Ps. 42 & 44 (penyidikan & alat bukti elektronik).
  - UU 27/2022 (PDP) Ps. 67 dan 68; UU 8/2010 Ps. 71 & 74 (tetap berlaku untuk prosedur TPPU); P2SK Ps. 306; POJK 8/2023, POJK 24/2025, POJK 40/2024, POJK 22/2023; PBI 22/23/2020 & PBI 23/6/PBI/2021 (PJP & QRIS).
- Temuan hukum utama untuk narasi: hambatan pemblokiran cepat **bukan pada norma** — KUHAP Ps. 140 ayat (7)-(9) sudah membuka jalur blokir mendesak tanpa izin pengadilan; yang belum ada adalah prosedur teknis, kanal komunikasi 24/7, dan format parameter digital yang eksekutabel oleh PJP.
- RAW SOURCES di-ingest: `raw/workshop-ovo-2026/Surat Undangan Workshop Tertutup OVO 338-PA-VI-C-IX-2026.pdf` dan `raw/workshop-ovo-2026/Riset Penegakan Hukum Kejahatan Keuangan Berbasis AI.pdf`.
- Verifikasi mutu: outline 29 slide terbaca ulang (`pptx_read`), tabel 7 halaman, catatan pembicara ada di seluruh slide; pemeriksaan kepadatan teks otomatis hanya menyisakan 1 peringatan minor (tinggi baris tabel halaman 18 tumbuh ~0,02 inci). Render PNG tidak dapat dilakukan: LibreOffice/poppler tidak terpasang di mesin ini.
- Sinkronisasi git: `git add -A` -> commit -> `git pull --rebase` -> push ke GitHub private `isikepalaku/vault-hukum`.

## [2026-10-16] analisis | Versi RINGKAS paparan OVO (13 slide) — revisi atas keluhan kepadatan slide
- Produk: `analisis/workshop-ovo-2026/Ringkas_Paparan_Kejahatan_Keuangan_Berbasis_AI_Ditreskrimsus_Polda_Sulsel.pptx` (13 slide, 16:9) + skrip `build_deck_ringkas.py`. Versi lengkap 29 slide tetap tersimpan sebagai cadangan/lampiran.
- Perubahan desain: slide hanya memuat kata kunci (maks 6 poin, font 20-24 pt pada poin utama); seluruh uraian, angka rinci, dan pengacuan pasal dipindah ke catatan pembicara (298-607 karakter per slide). Ditambah slide lampiran daftar dasar hukum untuk tanya jawab (tidak dipaparkan).
- Komposisi: (1) cover; (2) tiga temuan utama; (3) empat angka kunci; (4) anatomi serangan bot-to-cash; (5) empat vektor AI (kartu); (6) dasar hukum pidana (KUHP Ps. 332, 258, 426, 492, 607; UU ITE Ps. 27(2); UU PDP Ps. 67-68); (7) dasar hukum acara (KUHAP Ps. 140 utuh, UU ITE Ps. 43(5)l, UU TPPU Ps. 71 & 74); (8) mengapa pemblokiran terlambat; (9) dampak bansos 1,49 juta KPM; (10) rekomendasi 1-3; (11) gugus tugas + peta jalan 90 hari; (12) penutup; (13) lampiran dasar hukum.
- Verifikasi: outline 13 slide terbaca, catatan pembicara lengkap pada semua slide, pemeriksaan kepadatan teks otomatis tanpa temuan overflow (0 flag). Render PNG tetap tidak tersedia (LibreOffice/poppler tidak terpasang).
- Sinkronisasi git: `git add -A` -> commit -> `git pull --rebase` -> push.

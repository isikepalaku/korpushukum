# Kasus: Bank Woori Saudara (BWS) — Kredit Fiktif KUPEG TNI

- **Status Tahapan:** **PENYIDIKAN** (Ditingkatkan dari Penyelidikan per Oktober 2026)
- **Tanggal Register Awal:** 2026-09-23
- **Unit Penanganan:** Subdit II Fismondev Ditreskrimsus Polda Sulsel
- **Penyidik / Penyidik Pembantu:** AKP Indra, S.H. (NRP 74060594), Briptu Ahmad Fadlan Makbul (NRP 01030181), Briptu Afrizal Usman, S.H. (NRP 98040317)
- **Laporan Polisi / Pengaduan:** Laporan Pengaduan tanggal 21 November 2025
- **Dugaan Tindak Pidana:** Tindak Pidana Perbankan (UU No. 10/1998 jo UU No. 4/2023 tentang P2SK) dan/atau Pemalsuan Surat (Pasal 263/264 KUHP jo UU 1/2026) dan/atau Penggelapan/Penipuan jo TPPU (UU No. 8/2010).
- **Nilai Kerugian Sementara:** **Rp 7.189.000.000,- (Tujuh Koma Satu Delapan Sembilan Miliar Rupiah)**

---

## 1. Register Penerimaan Dokumen (Raw Intake)
| No | Tanggal Masuk | Nama Berkas / Dokumen | Jenis Bukti | Pihak Terperiksa / Saksi | Ringkasan Pokok Pemeriksaan | Status / Lokasi |
|---|---|---|---|---|---|---|
| 1 | 2026-09-23 | `BA pelapor.txt` | Dokumen Primer (BAI) | MUHAMMAD WILDAN (Pimpinan Cabang BWS Makassar) | Laporan awal dugaan kredit fiktif KUPEG TNI sebanyak 30 debitur dengan kerugian Rp 7,189 Miliar, terlapor M. Yunus (RO). Audit internal BWS dipimpin Yusuf Indra Jaya. | Terverifikasi (`raw/bank-woori-saudara/bap_extracted/`) |
| 2 | 2026-09-23 | `BAI MUHAMMAD YUNUS FIX.txt` | Dokumen Primer (BAI) | MUHAMMAD YUNUS (Terlapor / eks RO BWS Makassar) | Keterangan RO pemroses kredit KUPEG TNI. Mengakui proses 24-30 berkas tanpa verifikasi keabsahan KTA/ASABRI/juru bayar TNI. Mengaku lalai dan menyalahkan Febe/Hendro. Posisi saat diperiksa: tahanan Rutan Kelas 1 Makassar. | Terverifikasi (`raw/bank-woori-saudara/bap_extracted/`) |
| 3 | 2026-09-23 | `BAI HENNY ADAM alias HENDRO alias PACE.txt` | Dokumen Primer (BAI) | HENNY ADAM alias HENDRO (Saksi / Perekrut Boneka) | Merekrut Hamdanil & Roni Johan atas arahan M. Yunus; mengkondisikan potong rambut cepak ala militer; memfasilitasi TTD berkas di Hotel Arthama Makassar; menerima pencairan cash dari teller lalu setor kembali ke M. Yunus via Anta (alm). | Terverifikasi (`raw/bank-woori-saudara/bap_extracted/`) |
| 4 | 2026-09-23 | `BAI FEBE MARLA GINTING.txt` | Dokumen Primer (BAI) | FEBE MARLA GINTING (Saksi / eks Agen BWS, Istri Hendro) | Mengakui menerima data 16 calon debitur dari M. Yunus untuk diuruskan KK/NIK ke Dukcapil via Yos; menerima fee Rp 500.000/data. Mengonfirmasi keterlibatan M. Yunus. | Terverifikasi (`raw/bank-woori-saudara/bap_extracted/`) |
| 5 | 2026-09-23 | `BAI HAMDANIL.txt` | Dokumen Primer (BAI) | HAMDANIL alias DANIL (Saksi / Debitur Boneka) | Mahasiswa UMI (bukan anggota TNI). Diajak Ardito ke Hotel Arthama, disuruh potong cepak, tanda tangan berkas kosong/kredit plafon Rp 301,4 Juta (RB KUPEG Kompi Kavaleri XIV). Diarahkan Yunus ambil uang di teller BWS lalu diserahkan ke komplotan. | Terverifikasi (`raw/bank-woori-saudara/bap_extracted/`) |
| 6 | 2026-09-23 | `BAI RAHMAT.txt` | Dokumen Primer (BAI) | RAHMAT Bin ABDUL SAMAD (Saksi / Driver Ojol) | Rekening & M-Banking Mandiri miliknya (No. Rek 1520016332484) dipinjam/dikuasai penuh oleh M. Yunus untuk lalu lintas uang dan pembayaran cicilan kredit fiktif 11 debitur agar kredit tampak lancar. | Terverifikasi (`raw/bank-woori-saudara/bap_extracted/`) |
| 7 | 2026-09-23 | `BAI YOS.txt` | Dokumen Primer (BAI) | YOS MAKATENGKENG (Saksi / eks Jukir Dukcapil) | Perantara pengurusan KK/SKPWNI bodong di Dukcapil Makassar; menerima data dari Febe, diteruskan ke Muh Husni (Dukcapil); menerima bayaran fee transfer BRI. | Terverifikasi (`raw/bank-woori-saudara/bap_extracted/`) |
| 8 | 2026-09-23 | `BAI RIO MILANDA.txt` | Dokumen Primer (BAI) | RIO MILANDA (Saksi / Kabag Operasional BWS Makassar) | Menjelaskan SOP verifikasi back office/operasional, verifikasi sistem SLIK/e-KTP reader, dan proses pencairan kredit pegawai. | Terverifikasi (`raw/bank-woori-saudara/bap_extracted/`) |
| 9 | 2026-09-23 | `00_IKHTISAR_REKENING_YUNUS.md` & `MUTASI_YUNUS_LENGKAP_2022_2025.md` (dan file per tahun 2022-2025) | Dokumen Primer Finansial (Mutasi Rekening BNI) | Rekening BNI No. `1373172229` a.n. MUH YUNUS (dicetak sendiri oleh Yunus per 08/09/2026) | Mutasi 22.883 transaksi (Apr 2022 - Des 2025). Total perputaran debet/kredit Rp 22,29 Miliar. Inflow setor tunai masif Rp 6,87 Miliar (korelasi identik dgn kerugian BWS Rp 7,189 M). Outflow terkonfirmasi: transfer ke Rek Mandiri saksi Rahmat 126x total Rp 476,32 Juta untuk cicilan gali lubang tutup lubang, pembelian ruko Rp 1,99 M, dan sewa ruko/rumah Rp 3,05 M. | Terverifikasi (`raw/bank-woori-saudara/mutasi_bni_yunus/`) |

---

## 2. Struktur Pihak & Jaringan Pelaku
```
                 [ PT Bank Woori Saudara (BWS) Cabang Makassar ]
                                        |
                 +----------------------+----------------------+
                 |                                             |
       MUHAMMAD WILDAN (Pinca/Pelapor)            RIO MILANDA (Kabag Ops/Verifikator)
                 |
        MUHAMMAD YUNUS (Terlapor Utama / Relationship Officer)
                 |
        +--------+------------------------------------+--------------------------+
        |                                             |                          |
 [Jaringan Lapangan]                           [Penyamaran Arus Uang]      [Jaringan Dokumen Dukcapil]
  HENNY ADAM @ HENDRO (Perekrut)               RAHMAT (Driver Ojol)        FEBE MARLA GINTING (eks Agen BWS)
    +-- ARDITO (Keponakan Hendro)              Rek Mandiri 1520016332484              |
    +-- SUGIYANTO (Rekan Hendro)               (M-Banking dikuasai Yunus   YOS MAKATENGKENG (eks Jukir)
    +-- ANTA (Almarhum / Kurir Uang)            utk bayar cicilan gali               |
        |                                       lubang tutup lubang)       MUH HUSNI (Oknum Dukcapil Mks)
  DEBITUR BONEKA (Sipil disulap TNI):                                      (Cetak KK/SKPWNI rekayasa)
  1. HAMDANIL (Mahasiswa UMI - Rp 301,4 Juta)
  2. RONI JOHAN (Warga sipil)
  3. 28 Nama Debitur lainnya (Total Plafon Rp 7,189 M)
```

---

## 3. Matriks Fakta Hukum (Pemisahan Ketat)

### A. FAKTA HUKUM (Didukung Dokumen Primer BAI)
1. **Plafond & Kerugian:** Terdapat 30 debitur fasilitas KUPEG TNI (Kredit Umum Pegawai) fiktif di BWS Cabang Makassar kurun waktu 2023–2025 dengan total kerugian bank Rp 7.189.000.000,-.
2. **Debitur Fiktif / Non-TNI:** Saksi Hamdanil adalah mahasiswa aktif semester 8 UMI Makassar dan bukan prajurit TNI, tetapi diproses dan dicairkan kreditnya dengan berkas dinas militer palsu (KTA, SK Pengangkatan, Slip Gaji Kompi Kavaleri XIV) senilai Rp 301.494.774,-.
3. **Penyulapan Identitas:** Hendro dan Ardito mengkondisikan calon debitur untuk potong rambut model cepak tentara, memakai kemeja berkerah dan sepatu lari ala militer untuk mengelabui teller/petugas bank.
4. **Tempat TTD Tidak Wajar:** Proses penandatanganan berkas pengajuan kredit dilakukan di luar kantor bank, yaitu di kamar Hotel Arthama Makassar.
5. **Keterlibatan Terlapor (M. Yunus):** M. Yunus sebagai RO menerima berkas tanpa melakukan konfirmasi/verifikasi ke juru bayar kesatuan TNI terkait dan tidak melakukan kunjungan lapangan (OTS). M. Yunus menginstruksikan debitur saat di teller untuk mengiyakan semua pertanyaan teller agar uang tunai segera cair.
6. **Aliran Uang Tunai:** Uang tunai pencairan ratusan juta dibawa kembali ke Hotel Arthama. Debitur boneka (Hamdanil) hanya dijanjikan fee kecil, Hendro mendapat jatah, dan sisa uang terbanyak diserahkan kepada Anta (alm) untuk diantarkan kembali ke M. Yunus di sekitar kantor BWS.
7. **Manipulasi Angsuran (Cover Up):** M. Yunus menguasai akun M-Banking Mandiri milik saksi Rahmat (driver ojol) untuk membayarkan angsuran pinjaman atas sedikitnya 11 debitur fiktif (antara lain: Kristian Salomo, Marcelo Nataniel, Ahmad Wahyudi, Ade Romanda, Adiatma Zulfikar, Haikal Kamil, Didin) guna menunda kredit macet terdeteksi sistem bank.
8. **Pemalsuan Adminduk:** Febe Marla Ginting menyerahkan data 16 nama kepada calo Yos Makatengkeng untuk diterbitkan KK baru di Disdukcapil Kota Makassar via Muh Husni dengan imbalan uang Rp 500.000 per data.
9. **Korelasi Finansial Masif (Rekening BNI Yunus `1373172229`):**
   - Mutasi BNI Yunus 2022–2025 mencatat total perputaran **Rp 22,29 Miliar**.
   - **Inflow Setor Tunai CRM (Kluster 1):** Tercatat 658 kali setor tunai pecahan <10 Jt senilai **Rp 6.876.370.000,-** (indikasi kuat penampungan uang tunai teller pencairan kredit KUPEG TNI fiktif via Hotel Arthama, wajib diuji tempus).
   - **Inflow Intersepsi Pembayaran KPR Perumahan/Ruko (Kluster 2):** Ditemukan **78 transaksi masuk senilai total Rp 5.057.000.000,-** dari Rekening `1988033092` (Rp 3,058 M), Rekening `1854510423` (Rp 1,999 M), dan setoran Ibu NINA ANGGRAENI (Rp 1,83 M) dengan keterangan: DP, angsuran/cicilan, dan pelunasan unit di berbagai perumahan (Citra Garden, Patra Residen, Tallasa City, Tanjung Alya, Sukma Gowa, Minasa Upa, dll.). Ini membuktikan Yunus menyelewengkan uang angsuran/DP debitur KPR BWS langsung ke rekening BNI pribadinya!
   - **Outflow Gali Lubang Tutup Lubang (Cover-Up):** Terbukti M. Yunus mentransfer dana dari BNI miliknya ke rekening Bank Mandiri No. `1520016332484` a.n. RAHMAT (driver ojol) sebanyak **126 transaksi senilai Rp 476.320.000,-** untuk dioperasikan membayar cicilan 11 debitur fiktif BWS.
   - **Outflow Penarikan Tunai & Belanja Pribadi:** Tarik tunai teller/ATM Rp 1,183 Miliar dan belanja kartu debit POS Rp 1,145 Miliar (Total Rp 2,328 Miliar).

### B. INFERENSI / DUGAAN
1. M. Yunus adalah otak perencana (intellectual dader) sindikat pembobolan BWS dengan dua kluster kejahatan: (1) kredit KUPEG TNI fiktif, dan (2) penggelapan dana angsuran/pelunasan debitur KPR BWS.
2. Terdapat sindikat pembuat fisik dokumen militer palsu (stempel, blanko SK Pangdam/Kasad, blanko KTA, dan slip gaji dinas militer) yang digunakan berulang pada ke-30 debitur.
3. Rekening Mandiri atas nama Rahmat digunakan sebagai rekening penampung transit (smurfing/layering) sebelum dialihkan untuk cicilan dan keperluan pribadi terlapor.
4. Yunus memanfaatkan jabatannya selaku RO kredit perumahan untuk mengarahkan pengembang (developer) dan debitur KPR menyetorkan pembayaran ke rekening BNI pribadinya, bukan rekening escrow/virtual account resmi BWS.

### C. UNKNOWN (Perlu Diuji / Ditelusuri)
1. **Identitas Pemilik Rekening `1988033092` dan `1854510423`:** Siapa pemilik kedua rekening pengirim miliaran rupiah tersebut (apakah kantor pemasaran developer, notaris rekanan, atau perantara)?
2. **Peran Saksi NINA ANGGRAENI:** Siapa Ibu Nina Anggraeni yang rutin menyetor tunai/transfer DP dan pelunasan rumah puluhan unit ke rekening Yunus?
3. **Audit Kredit KPR BWS:** Berapa total debitur KPR di BWS yang merasa sudah membayar angsuran/pelunasan ke Yunus tetapi status kreditnya di pembukuan BWS macet/menunggak?
4. **Identitas Pembuat Fisik Dokumen Militer:** Siapa yang mencetak dan mengisi blanko KTA TNI, SK Pengangkatan, dan Slip Gaji palsu yang dibawa ke Hotel Arthama?
5. **Peran Oknum Dukcapil (MUH HUSNI):** Apakah Muh Husni menerbitkan dokumen sah tapi palsu (aspal) dari dalam sistem SIAK Dukcapil, atau hanya mencetak blangko palsu?
6. **Peran Pejabat Pengambil Keputusan Kredit:** Siapa pejabat BWS yang memberikan persetujuan akhir (*approval/DCRM*) atas pencairan kredit 30 berkas ini? Apakah murni tertipu atau ada unsur pembiaran/kickback?

### D. KONTRADIKSI & ALIBI
- **Bantahan M. Yunus vs Keterangan Hendro & Febe:** M. Yunus mengklaim dirinya lalai dan mengira debitur adalah prajurit TNI asli yang berkasnya dibawa sendiri oleh nasabah. Namun keterangan Hendro, Febe, dan Hamdanil secara mutlak membuktikan bahwa M. Yunus sendiri yang menginap di Hotel Arthama, membawa dokumen, mengatur instruksi pencairan teller, dan menerima uang hasil pencairan tunai.
- **Bantahan M. Yunus vs Keterangan Saksi Rahmat:** M. Yunus menyatakan angsuran dibayar dari sisa pencairan debitur, namun bukti mutasi rekening Mandiri saksi Rahmat membuktikan M. Yunus sendiri yang mengoperasikan M-Banking milik driver ojol untuk menyetor angsuran fiktif tersebut.

### E. KELEMAHAN PEMBUKTIAN & RISIKO HUKUM
1. **Saksi Kunci Meninggal Dunia:** Sdr. ANTA yang mengantar fisik uang tunai dari Hotel Arthama ke M. Yunus telah meninggal dunia (*almarhum*), sehingga rantai serah terima uang tunai fisik memerlukan bukti petunjuk lain (CCTV hotel/kantor, bukti chat WA Hendro-Yunus, atau mutasi rekening pendukung).
2. **Ketiadaan Bukti Setor Tunai Langsung ke Rekening Yunus:** Pelaku utama sengaja menggunakan penarikan tunai (*cash*) di counter teller untuk memutus jejak audit perbankan (*paper trail*).

---

## 4. Rekomendasi Langkah Penyelidikan Lanjutan
1. **Pemeriksaan Tambahan / Konfrontasi:**
   - Sita bukti chat WhatsApp antara M. Yunus, Hendro, Febe, dan Ardito.
   - Periksa Sdr. ARDITO (keponakan Hendro) dan Sdr. SUGIYANTO.
   - Panggil dan periksa Sdr. MUH HUSNI (oknum Disdukcapil Kota Makassar).
2. **Forensik Dokumen & Digital:**
   - Sita berkas asli kredit ke-30 debitur di BWS Makassar.
   - Lakukan uji laboratorium forensik (Labfor) atas tanda tangan, stempel kesatuan militer, dan keaslian material KTA/SK TNI.
   - Ekstraksi digital forensik handphone saksi Rahmat (jejak login M-Banking Mandiri oleh device M. Yunus) dan HP para saksi.
3. **Penyitaan Rekening Koran & Follow the Money:**
   - Minta print out rekening koran lengkap Bank Mandiri saksi Rahmat (rekening penampung cicilan).
   - Telusuri rekening operasional dan rekening pribadi/keluarga M. Yunus untuk penerapan Pasal TPPU (UU No. 8/2010).
4. **Koordinasi POM TNI / Kesatuan Militer:**
   - Terbitkan surat permintaan keterangan resmi ke Pomdam XIV/Hasanuddin atau kesatuan Kompi Kavaleri XIV / Kodam XIV Hasanuddin untuk memastikan status keanggotaan 30 debitur tersebut fiktif (bukan prajurit aktif).

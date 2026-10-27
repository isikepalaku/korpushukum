---
title: "Kasus: Sindikat Passobis — Penipuan Telepon Bertarget (Toraja–Enrekang–Makassar)"
aliases: [Sindikat Passobis, Passobis, Vishing Toraja-Enrekang-Makassar, Papan Keterkaitan Passobis]
tags: [kasus, penipuan, vishing, mule-account, tppu, enrekang, tator, makassar, lidik]
type: kasus
source: "Artefak internal: `analisis/board_keterkaitan_sindikat_passobis.html` · `.excalidraw` · `.png` (generator `analisis/generate_board.py`), 12 Okt 2026"
last_updated: 2026-10-12
related: ["Cyber Crime", "TPPU", "KUHP", "UU 1-2026", "Perbankan", "Alat Bukti Elektronik"]
status: "Analisis hubungan (link analysis) — bahan lidik; belum ada LP/berkas formil di vault"
---

# Kasus: Sindikat Passobis — Penipuan Telepon Bertarget (Toraja–Enrekang–Makassar)

> Status: **papan analisis hubungan**, bukan dokumen formil. Belum ada LP, Surat Perintah Lidik, atau berkas perkara di vault ini; seluruh isi halaman diturunkan dari artefak analisis internal dan **belum diuji di persidangan**.
>
> **Catatan privasi**: mengikuti konvensi halaman kasus lain di vault ini, identifikator sensitif (NIK, nomor SIM, nomor rekening, koordinat presisi rumah) tidak ditulis lengkap di wiki — rujuk artefak `analisis/board_keterkaitan_sindikat_passobis.*` untuk data penuh.

## Ringkasan

Papan analisis keterkaitan (*link analysis board*) yang memetakan satu jaringan dugaan penipuan berbasis **telepon (vishing) + WhatsApp** dengan pola *impersonation* keluarga. Korban menyasar **lingkungan keluarga dokter** (Toraja–Enrekang) dengan narahubung anak korban, sementara eksekutor lapangan berbasis di **Desa Pebaloran, Kec. Curio, Kab. Enrekang** (wilayah perbatasan Tana Toraja) memakai **satu perangkat iPhone XR bersama** (suami–istri, 4 SIM) dan dua **rekening penampung (mule account)** yang dikuasai kerabat para pelaku di **Makassar (Bara-Baraya)**.

Nilai kerugian terpantau masih kecil (Rp 3,45 juta total dari 2 korban) — indikatif baru sebagian kejadian terlaporkan, bukan batas atas kerugian jaringan.

## Korban & kerugian (terpantau)

| Korban | Narahubung | Waktu | Modus | Kerugian | Rekening tujuan |
|---|---|---|---|---|---|
| Ibu dr. Revas (perempuan) | Sdr. Revas (anak) | 15 Sep 2026 | Catut nama anak ("hp jil temanku") | Rp 3.200.000,- | Bank Mandiri — a.n. P.B. (58 thn) |
| Ayah dr. Riad (laki-laki) | Sdr. Riad (anak) | 5 Okt 2026, 17.11 WIB | Catut keluarga mendesak | Rp 250.000,- | BNI Taplus — a.n. M.N.F. (31 thn) |

> Pada papan terdapat catatan **RALAT STATUS**: korban materiil adalah orang tua (Ibu dr. Revas & Ayah dr. Riad); Revas & Riad berperan sebagai **narahubung koordinasi**, bukan korban.

## Saluran telekomunikasi (SIM)

| SIM | Operator | Peran pada konstruksi | Status |
|---|---|---|---|
| 0858-2851-2082 | Indosat Ooredoo | Kontak yang menghubungi **kedua korban** | *SIM operasional utama* |
| 0857-9611-4333 | Indosat Ooredoo | Chat & koordinasi internal (indikasi rekayasa percakapan) | *SIM pendukung* |
| 0851-4390-3425 | by.U (Telkomsel) | Aktif memancar real-time di area Curio | **Titik tangkap (tangkan)** |
| 0812-4348-4035 | Telkomsel | Dipakai pihak yang diduga **suami eksekutor** | *SIM pendamping* |

Keempat SIM dibinding pada **satu IMEI yang sama** → indikasi *shared device* satu rumah tangga pelaku (lihat di bawah).

## Perangkat fisik

| Item | Nilai |
|---|---|
| Model | Apple iPhone XR (`A1984`, single nano-SIM) |
| IMEI | `353068103923504` (TAC `35306810`) |
| Pola penggunaan | *Shared device* — suami & istri |
| Lokasi BTS aktif | Desa Pebaloran, Kec. Curio, Kab. Enrekang (perbatasan Tator) |
| Koordinat CGI | sekitar `-3.2928, 119.8664` (presisi penuh di artefak papan) |

## Eksekutor lapangan & pihak yang menguasai rekening

| Peran | Ringkas |
|---|---|
| Eksekutor (penelpon/pemegang HP) | **Pregita Angel** ("Enjel") — NIK `737103591106****`, lahir Tator 19-11-2006 (19 thn), alamat KTP Bara-Baraya, Makassar; posisi nyata Curio, Enrekang. Tag *Getcontact* publik antara lain "Mafia Gadai" & "Penipu" (indikatif, bukan alat bukti) |
| Co-eksekutor / suami | Suami Pregita Angel — domisili lapangan Curio; pemegang SIM 0812-4348-4035 |
| Pemilik rekening penampung 1 | **P.B.** (58 thn, IRT) — Mandiri `15200365316**`; **nenek kandung** Pregita, satu RT/bersebelahan di Bara-Baraya |
| Pemilik rekening penampung 2 | **M.N.F.** (31 thn) — BNI Taplus; domisili Tamalate/Bonto Duri, Makassar |

Aliran dana kejahatan: **korban → transfer → rekening penampung (Bank) → perangkat/eksekutor di Curio** (hubungan kekerabatan pasutri & nenek–cucu adalah simpul penghubung Makassar ↔ Enrekang).

## Konstruksi hukum (tentatif)

| Temuan (jika terbukti) | Pasal (pasca UU 1/2026) | Catatan |
|---|---|---|
| Menggerakkan korban menyerahkan uang dengan nama/kedudukan palsu & rangkaian kata bohong ("catut nama anak/keluarga") | **Pasal 492 KUHP Nasional** (penipuan) | Penjara maks **4 tahun** atau denda **kategori V** (Rp 500 juta) — alternatif, bukan kumulatif |
| Bila perbuatan dilakukan secara bersama-sama / dengan bantuan sarana | **Pasal 20 KUHP Nasional** (pelaku/penyertaan) & **Pasal 21 KUHP Nasional** (pembantuan) | Uji peran masing-masing: penelpon, pendamping, penyedia SIM, penyedia HP |
| Perbuatan lewat sistem elektronik dengan tipu daya terhadap konsumen/pengguna jasa | **Pasal 28 ayat (1) jo. Pasal 45A UU ITE** (UU 11/2008 jo. UU 19/2016 jo. UU 1/2024) | Delik alternatif — uji apakah terjadi "transaksi elektronik"; jangan dipaksakan bila murni telepon |
| Pemilik rekening penampung yang mengetahui/menguasai hasil kejahatan | **Pasal 5 UU 8/2010** (TPPU — menerima/menguasai harta hasil kejahatan; maks 5 thn); Pasal 3/4 bila ikut menempatkan/mentransfer (maks 20 thn, **dibatasi kap 15 thn oleh UU 1/2026**; TPPU tetap dikecualikan dari penghapusan minimum khusus) | Fokus pembuktian pada **pengetahuan** (unsur subjektif) pemilik rekening |
| Menerima/menyimpan barang (perangkat) hasil kejahatan dengan mengetahuinya | **Pasal 591 KUHP Nasional** (penadahan; maks 4 thn / kat. V) | Subsidair |

> Konstruksi di atas **tentatif dan belum didukung dokumen formil**. KUHP Nasional = lex generalis; TPPU/UU ITE berkedudukan sebagai lex specialis pada unsur masing-masing.

## Titik verifikasi (checklist pulbaket)

1. **Cek formil**: apakah peristilahan ini sudah ada LP/LI? Bila belum, kejadian korban perlu dilaporkan agar ada dasar formil (tidak bisa menindak hanya atas dasar papan analisis).
2. **Korban**: minta keterangan & bukti transfer kedua korban (bukti transfer, screenshot chat, rekaman panggilan, log panggilan masuk).
3. **SIM & IMEI**: konfirmasi data pelanggan 3 SIM Indosat/by.U/Telkomsel (permintaan resmi ke operator) dan uji *binding* IMEI `353068103923504` — uji apakah benar satu perangkat dipakai bergantian atau perangkat hasil kloning/repack.
4. **Titik tangkap lokasi**: verifikasi BTS/CGI Curio terhadap waktu kejadian (bukan hanya posisi "aktif sinyal"); bandingkan dengan lokasi KTP (Bara-Baraya) → uji kandidat *alibi*.
5. **Rekening penampung**: ajukan permintaan izin pembukaan rahasia bank (POJK 44/2024) untuk rekening Mandiri & BNI Taplus; minta mutasi + profil nasabah + rekaman CCTV penarikan.
6. **Follow the money**: lacak lintas rekening (kemungkinan penarikan tunai/transfer lanjutan), petakan kesamaan penarik/ATM.
7. **Kekerabatan**: verifikasi KK/akta + catatan kependudukan untuk memastikan relasi nenek–cucu & pasutri (Bara-Baraya ↔ Curio).
8. **Potensi korban lain**: pola ini serupa dengan tari singkong/catut keluarga — cek LP lain dengan SIM/IMEI yang sama (indikatif sindikat, bukan pelaku tunggal).

## Kelemahan & hal belum diketahui

- **Tidak adanya dokumen formil** (LP/LI) di vault → konstruksi hukum belum punya pijakan prosedural.
- **Peran M.N.F. (rekening kedua)** belum jelas: penerima manfaat, perantara, atau korban penyalahgunaan identitas juga (uji indikasi pembelian rekening).
- **Status kekerabatan & peran suami** baru dari narasi papan; belum dari dokumen kependudukan/KK.
- **Tag Getcontact** ("Penipu", "Mafia Gadai") bersifat *crowdsourced* → tidak boleh dipakai sebagai alat bukti, hanya petunjuk lidik.
- **Angka kerugian** Rp 3,45 juta dari 2 kejadian hanya menunjukkan yang terpantau; kemungkinan besar ada kejadian lain yang belum dilaporkan.
- **Locus delicti**: panggilan dari Curio, transfer diterima di Makassar, korban di Toraja/Enrekang → uji kompetensi wilayah (mana yang menguasai penyidikan).

## Status & tindak lanjut

Papan analisis hubungan sudah disusun dan disimpan ke vault (`analisis/board_keterkaitan_sindikat_passobis.*`, dapat diregenerasi via `generate_board.py`). Langkah berikutnya: konfirmasi formil (LP/LI), permintaan data operator & perbankan, lalu uji titik tangkap lokasi perangkat pada rentang waktu kejadian.

## Terkait

- [[Cyber Crime]] · [[TPPU]] · [[KUHP]] · [[UU 1-2026]] · [[Perbankan]] · [[Alat Bukti Elektronik]]
- Sumber: `analisis/board_keterkaitan_sindikat_passobis.html` · `.excalidraw` · `.png`; generator: `analisis/generate_board.py`
- Monitor pendukung: `tools/tiktok-watch/watchlist.txt` (kata kunci `passobis`)

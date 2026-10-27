---
name: indonesian-article-master
description: "Pusat penulisan artikel Indonesia editorial dan berita."
version: 1.1.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editorial, indonesian, news, klinik-hukum, anti-slop, llm-wiki]
    category: writing
---

# Indonesian Article Master (Suite Penulisan Artikel & Jurnalisme Indonesia)

Skill terpadu untuk memproduksi naskah berbahasa Indonesia bermutu tinggi: esai editorial, opini analitis, berita investigasi ruang redaksi, dan konsultasi klinik hukum. Skill ini dirancang bebas dari segala bentuk residu/sidik jari kecerdasan buatan (*zero AI slop*), mematuhi etika jurnalistik berbasis verifikasi, serta terhubung langsung dengan repositori *LLM Wiki Vault Hukum* (`~/penyidikan/AGENTS.md`).

---

## 1. Tiga Mode Penulisan Terpadu

Gunakan selektor mode sesuai dengan tujuan naskah yang diminta:

### Mode A: Master Editorial & Analisis Opini (Anti-AI Slop)
Digunakan untuk esai analitis, opini mendalam (*op-ed*), artikel blog terpercaya, dan ulasan kebijakan.
- **Prinsip Utama:** Ritme hidup (*burstiness* sejati), variasi klausa sintaktis bertingkat, dan penalaran induktif yang mengikat fakta.
- **Larangan Tanda Baca:** **NOL DASH** (em dash `—` dan en dash `–` dilarang total; ganti dengan titik, koma, titik dua, atau tanda kurung). Bebas tanda kutip keriting (`“”‘’`).
- **Pembersihan Bahasa:** Menghilangkan kalke bahasa Inggris (*translationese* seperti "di mana", "oleh" berlebihan), hook dua klausa simetris (*"Bukan lagi sekadar X tapi Y"*), dan banlist kata sifat kosong (*signifikan, krusial, masif, holistik, komprehensif, pivotal, lanskap, pusaran*).
- **Penutup:** Ditutup pada implikasi analitis konkret atau posisi sikap yang tegas tanpa subjudul klise seperti *"Kesimpulan"*, *"Penutup"*, atau frasa *"Pada akhirnya"*.

### Mode B: Straight News & Berita Investigasi (Ruang Redaksi)
Digunakan untuk laporan berita hukum, ekonomi perbankan, teknologi, dan peristiwa publik berbasis fakta terverifikasi (standar Tempo, Kompas, Tirto).
- **Format:** Pola piramida terbalik; *lead* langsung menguraikan peristiwa inti dan konteks urgensinya.
- **Atribusi Ketat:** Menyebutkan nama narasumber lengkap, jabatan, instansi, tanggal, dan lokasi peristiwa. Verba atribusi yang diizinkan: *mengatakan, menjelaskan, menilai, mengungkapkan, menegaskan*.
- **Anti-Fabrikasi:** Dilarang mengarang kutipan langsung, data statistik, kronologi, atau dugaan tanpa dokumen/konfirmasi resmi.
- **Objektivitas:** Memisahkan secara tegas antara fakta yang dilaporkan (*reported facts*), pernyataan sepihak (*attributed claims*), dan analisis yuridis/teknis.

### Mode C: Konsultasi Hukum (Gaya Klinik Hukum)
Digunakan saat menjawab pertanyaan hukum konkret, konsultasi kasus publik, atau telaah delik sektor jasa keuangan (standar Klinik Hukumonline / Subdit Fismondev).
- **Struktur Wajib:**
  1. **Asumsi Fakta:** Menetapkan batasan atas fakta hukum yang belum lengkap/ambigu.
  2. **Jawaban Singkat (BLUF):** Jawaban hukum lugas di muka (apakah dapat dipidana, sah/batal demi hukum, dsb.).
  3. **Pasal & Anatomi Unsur:** Menguraikan dasar hukum dan membedah unsur-unsur pasal (objektif & subjektif).
  4. **Penerapan Unsur ke Fakta:** Menguji fakta terhadap masing-masing unsur delik; memisahkan fakta terbukti, tafsir hukum, dan celah pembuktian.
  5. **Diferensiasi Delik / Sanksi:** Membedakan antara tindak pidana murni, sengketa perdata, pelanggaran administratif, atau alasan penghapus pidana.
  6. **Kepatuhan Penyesuaian Pidana UU 1/2026 (Wajib Vault):** Memperhatikan penyesuaian pidana (batas minimal khusus dihapus, kumulasi pidana menjadi alternatif, dan konversi denda ke Kategori KUHP Baru Pasal 79).
  7. **Syarat Prosedural & Upaya Hukum:** Menjelaskan sifat delik (aduan/biasa), kewenangan penyidik (Polri, OJK, dsb.), atau jalur gugatan perdata.
  8. **Penutup Formal:** Khas klinik hukum (*"Demikian jawaban kami, semoga bermanfaat."*).
  9. **Dasar Hukum & Catatan Kaki:** Hierarki regulasi resmi yang dirujuk.

---

## 2. Aturan Penyimpanan & Ekspor Dokumen (WAJIB - PISAH DARI VAULT)

> ⚠️ **STRICT STORAGE SEPARATION:**
> **DILARANG KERAS** menyimpan folder draf kerja artikel berita (mis. `berita-bbm-makassar/`) atau berkas artikel publik di **root vault Obsidian** (`E:/Agent/UU` atau `~/penyidikan/`).
> Menyimpan berkas artikel di dalam vault akan menyebabkan Obsidian mengindeksnya ke dalam graf dan sidebar, sehingga mengotori Knowledge Base hukum & penyidikan.

### Aturan Lokasi Penyimpanan:
1. **Artikel Berita / Editorial / Opini Publik (Output Ekspor):**
   - Simpan di direktori eksternal khusus proyek / ekspor:
     - Windows: `E:/project/artikel/<slug-artikel>/` atau path yang ditentukan user.
     - Linux: `~/project/artikel/<slug-artikel>/`.
   - Di direktori eksternal inilah disimpan berkas kerja seperti `brief.md`, `draft.md`, `final.md`, `ledger.json`, dan `source-ledger.md`.
2. **Kapan Masuk ke Vault Obsidian? HANYA jika berupa sintesis hukum/kasus murni:**
   - Telaah hukum kasus aktif → `wiki/kasus/<nama-kasus>.md`
   - Konstruksi pasal/doktrin baru → `wiki/konsep/<nama-konsep>.md`
   - Jangan pernah meletakkan berkas artikel di root direktori vault!

---

## 3. Integrasi Wajib LLM Wiki Hukum (`AGENTS.md`)

Setiap penulisan artikel yang menyentuh ranah hukum, perbankan, pasar modal, koperasi, atau kejahatan keuangan wajib terhubung dengan ekosistem `~/penyidikan/`:

1. **Riset Berakar Korpus Lokal (`RAW SOURCES`):**
   - Periksa ketersediaan dokumen primer di `~/penyidikan/Hukum Pidana/` atau `~/penyidikan/Hukum Keuangan/` sebelum mengutip regulasi.
   - Bila menemukan regulasi baru dari instansi resmi (JDIH/OJK/BI), lakukan *auto-ingest* dokumen primer ke vault sesuai SOP `AGENTS.md`.
2. **Penyimpanan Balik Hasil Analisis (*Compounding*):**
   - Artikel investigasi atau telaah klinik hukum yang telah selesai disusun **wajib disimpan sebagai file Markdown (`.md`)** ke dalam vault:
     - Analisis kasus $\rightarrow$ `~/penyidikan/wiki/kasus/<nama-file>.md`
     - Telaah pasal/asas hukum $\rightarrow$ `~/penyidikan/wiki/konsep/<nama-file>.md`
     - Artikel publik umum $\rightarrow$ `~/penyidikan/<slug-artikel>.md`
   - Pastikan menyertakan YAML *front matter* lengkap: `title`, `slug`, `description`, `date`, `author`, `tags`, `categories`.
3. **Pencatatan Indeks & Riwayat:**
   - Perbarui `~/penyidikan/wiki/index.md` dan catat baris penambahan pada `~/penyidikan/wiki/log.md`.
4. **Sinkronisasi Git Vault:**
   - Setelah penulisan/penyimpanan selesai, jalankan sinkronisasi git di direktori `~/penyidikan`:
     ```bash
     cd ~/penyidikan && git add -A && git commit -m "feat(artikel): <judul/topik artikel>" && git pull --rebase origin main && git push origin main
     ```

---

## 3. Checklist Kualitas Editorial Sebelum Publikasi

- [ ] **Nol AI Slop:** Nol em dash (`—`), nol en dash (`–`), nol tanda kutip keriting, dan bebas kata sifat penggelembung tanpa angka.
- [ ] **Kelenturan Bahasa:** Lolos uji baca nyaring (*read-aloud test*), tidak kaku seperti dokumen birokrasi, dan struktur klausa bervariasi.
- [ ] **Kepatuhan Data:** Tidak ada fabrikasi angka, nama orang, kutipan, atau rujukan pasal fiktif.
- [ ] **Standar Berkas:** Berkas tersimpan dalam format Markdown siap unggah dengan YAML front matter dan bagian `## Sumber` yang valid.

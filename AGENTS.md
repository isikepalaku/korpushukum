---
title: "AGENTS.md — Schema LLM Wiki Vault Hukum"
aliases: [Schema, LLM Wiki]
tags: [schema, llm-wiki, konfigurasi]
type: schema
---

# Schema — LLM Wiki Vault Hukum (E:/Agent/UU)

Pola diadaptasi dari [LLM Wiki — karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) untuk second brain hukum **Penyidik Fismondev** (tindak pidana sektor jasa keuangan). Ini file konfigurasi yang membuat LLM menjadi **pemelihara wiki yang disiplin**, bukan sekadar chatbot.

> **Strategi memori (keputusan user, diperbarui 27 Sep 2026):** vault ini = **memori utama pengetahuan hukum/kasus**; **OpenViking lokal** (`127.0.0.1:1933`, provider memori Hermes) = **lapisan recall rinci** untuk profil, tim, toolset, SOP, dan kasus aktif; built-in memori (MEMORY.md/USER.md) = **aturan & preferensi selalu-aktif**; `session_search` = recall percakapan masa lalu. OpenViking berjalan **terisolasi** (database di `~/.openviking/`, akses via HTTP) — **tidak menyentuh file markdown vault**, jadi tidak ada risiko korupsi vault.
>
> *Catatan lama:* keputusan awal vault adalah "TANPA memory provider eksternal". Keputusan itu **digantikan** oleh pemasangan OpenViking di atas; alasan pergantian = recall semantik lintas sesi tanpa membebani batas karakter memori built-in.

## Tiga lapisan

1. **RAW SOURCES (immutable)** — sumber kurasi, dibaca tapi TIDAK diubah:
   - `Hukum Keuangan/` (Subdit Fismondev: UU P2SK + UU sektoral, POJK, Permenkop, putusan MK)
   - `Hukum Siber/` (Subdit Siber: UU ITE, UU PDP, PP PSTE, regulasi digital & siber)
   - `Hukum Tipidter/` (Subdit Tipidter: UU Cipta Kerja & UU sektoral SDA, Minerba, Lingkungan Hidup, Ketenagakerjaan, Pelayaran, putusan MK)
   - `Hukum Pidana/` (Hukum Pidana Umum & Acara: KUHP, KUHAP, UU Penyesuaian, putusan MK)
   - `Mindik/` (Administrasi Penyidikan Polri: SOP Perkaba, Template BAP Saksi/Tersangka, Juknis Tipografi & Skema JSONL)
   - Ini sumber kebenaran. LLM hanya membaca darinya.

2. **WIKI (dimiliki LLM)** — folder `wiki/`, di-create/di-maintain penuh oleh LLM:
   - `wiki/entitas/` — satu file per subjek kasus (Koperasi, Fidusia, Pinjol, Money Changer, Investasi Bodong, TPPU…)
   - `wiki/konsep/` — satu file per pasal/azas (bank gelap, open-loop/closed-loop, lex specialis, UU 1/2026…)
   - `wiki/kasus/` — analisis/sintesis dari query (jawaban bagus disimpan balik, jangan hilang di chat)
   - `wiki/index.md` — katalog konten (kategori, link, ringkasan, metadata)
   - `wiki/log.md` — catatan kronologis append-only

3. **SCHEMA** — file ini (`AGENTS.md`).

## Konvensi halaman wiki

- **Frontmatter YAML** setiap halaman: `title`, `aliases`, `tags`, `type`, `source`, `last_updated`, `related`.
- **Cross-reference** pakai `[[wikilink]]` (resolve by filename).
- **Tandai konflik:** jika sumber baru bertentangan dengan klaim lama, tulis `> ⛔ KONFLIK: <klaim lama> vs <klaim baru>`. Jangan diamkan.
- **Konsep yang disebut tapi belum punya halaman** → buat halaman baru.
- **Orphan page** (tanpa inbound link) → tautkan dari halaman relevan atau index.

## Aturan konten (domain penyidik) — WAJIB

- **HANYA** masukkan yang relevan ranah **penyidikan** (izin/legalitas, kewenangan, pidana, follow the money). **JANGAN** tata kelola/GCG (ranah pengawasan administratif OJK, bukan konstruksi pidana).
- **Verifikasi dulu, jangan vonis.** Terdaftar/berizin = presumsi sah.
- Setiap menyebut **ancaman hukuman** → wajib ikutkan **UU 1/2026 (Penyesuaian Pidana)**: min khusus dihapus, penjara+denda kumulatif→alternatif, denda→kategori (KUHP Ps. 79), kap penjara 15 thn.
- Konstruksi pidana → **asas lex specialis** (pilih pasal sektoral paling spesifik).
- Draft pertanyaan BAP → pakai skill **`teknik-interogasi`** (ADI DEMEN BABI), acuan KUHAP 166–180.
- Referensi riset hukum → skill **`indonesian-legal-research`** (sumber kanonik, parsing, status peraturan).

## Operasi

**AUTO-INGEST SUMBER RESMI** (aturan tetap pengguna):
- Setiap sumber baru resmi pemerintah/lembaga negara yang ditemukan atau dipakai dalam jawaban penyidikan/hukum wajib dicek terlebih dahulu terhadap isi vault.
- Jika belum ada, unduh teks/dokumen lengkap dari situs resmi (JDIH/instansi penerbit), simpan ke folder RAW SOURCES yang sesuai, lalu ingest ke wiki. Jangan hanya menyimpan URL, cuplikan mesin pencari, atau ringkasan.
- Verifikasi keaslian, nomor, tahun, judul, instansi penerbit, status berlaku/perubahan/pencabutan, dan URL asal. Sumber nonresmi hanya boleh menjadi jalur penemuan, bukan sumber kanonik bila dokumen resmi tersedia.
- Deduplikasi berdasarkan identitas peraturan/dokumen dan isi; jangan membuat salinan kedua dengan nama berbeda.
- Penambahan file baru diperbolehkan pada RAW SOURCES; sifat *immutable* berarti file sumber yang sudah disimpan tidak ditulis ulang atau diedit isi substantifnya.
- Setelah ingest: perbarui halaman wiki terkait, `wiki/index.md`, `wiki/log.md`, `INDEX.md` bila diperlukan, lalu commit dan push.

**INGEST** (tambah sumber baru):
1. Cek apakah sumber sudah ada di vault; jika ada, gunakan file yang ada dan jangan duplikasi.
2. Baca sumber → diskusi poin penting dengan user.
3. Tulis/update halaman wiki (entitas/konsep/kasus).
4. Update `wiki/index.md`.
5. Append `wiki/log.md`: `## [YYYY-MM-DD] ingest | Judul`. 

**QUERY** (tanya ke wiki):
1. Baca `wiki/index.md` dulu → temukan halaman relevan.
2. Baca halaman → sintesis dengan citation ke sumber.
3. Jawaban/analisis berharga → **simpan balik sebagai halaman wiki baru** (compounding).

**LINT** (health-check berkala):
- Kontradiksi antar halaman, klaim basi yang disupersede, orphan pages, konsep tanpa halaman, cross-reference hilang, data gap yang bisa diisi web search. Sarankan topik/sumber baru.

## Sinkronisasi lintas mesin (git — WAJIB setelah tiap operasi)

Vault ini adalah **git repo**, remote `origin` → **GitHub private** `isikepalaku/vault-hukum` (pengganti Obsidian Sync berbayar).

### Path vault per mesin
- **Komputer utama (Windows):** `E:/Agent/UU` (dengan Obsidian)
- **Agent server (Linux):** `~/penyidikan/` (TANPA Obsidian — file markdown dibaca/ditulis langsung)

### Sinkronisasi dari agent server (Linux) — WAJIB setelah tiap operasi

Setiap operasi yang mengubah isi vault (INGEST, QUERY save-back, LINT, update halaman) WAJIB diakhiri:

```bash
cd ~/penyidikan
git add -A
git commit -m "<tipe>: <ringkasan>"
git pull --rebase origin main   # ← tarik dulu perubahan dari komputer lain
git push origin main
```

**Sebelum memulai kerja di server** (jika komputer lain sudah push):
```bash
cd ~/penyidikan && git pull --rebase origin main
```

### Sinkronisasi dari komputer Windows (dengan Obsidian)
```bash
git -C "E:/Agent/UU" add -A
git -C "E:/Agent/UU" commit -m "<tipe>: <ringkasan>"
git -C "E:/Agent/UU" pull --rebase
git -C "E:/Agent/UU" push
```

Aturan: satu mesin "writer utama" per halaman; jangan edit halaman yang sama bersamaan di dua mesin (git merge konflik = tanda proses, resolve manual). `.obsidian/workspace.json` dan `.obsidian/graph.json` di-gitignore (UI state per mesin — layout/tab/tampilan graph tidak ikut sync, memang seharusnya begitu).

**Otomatisasi di komputer Windows — plugin Obsidian Git** (v2.42.0, terpasang di `.obsidian/plugins/obsidian-git/`, ikut ter-commit sehingga mesin lain yang pull langsung aktif; core plugin **Sync berbayar dinonaktifkan**):
- auto commit tiap **5 menit** bila ada perubahan → pesan `auto: vault backup <tanggal>`;
- auto push tiap commit, `pullBeforePush: true`, `syncMethod: merge`;
- auto pull tiap **15 menit** + saat Obsidian dibuka (`autoPullOnBoot`);
- `limitToVault: true` — operasi git plugin tidak merambat ke repo induk.
- Autentikasi push memakai helper **repo-local** `gh auth git-credential` (`git config --local credential.helper`), jadi **tidak ada PAT** di `data.json`. Mesin baru: `gh auth login` sekali.
- Commit agent di akhir operasi (INGEST/LINT) **tetap wajib** — pesan bermakna `tipe: ringkasan`; commit otomatis plugin hanya jaring pengaman.
- Jangan menjalankan perintah git CLI pada file yang sedang diproses plugin (lock `.git/index.lock`); tunggu operasi plugin selesai.

**Line-ending:** `core.autocrlf=false` di-set **repo-local** (`.gitattributes` sudah memaksa `eol=lf`). Dengan autocrlf global `true`, entri index menyimpan ukuran CRLF sehingga file bisa tampak `modified` padahal isi identik. Gejala `M` tanpa isi diff → `git add <file>` untuk me-refresh stat index (bukan perubahan konten).

### Konflik git (jika terjadi)
1. `git status` → lihat file konflik (ditandai `UU` / `both modified`)
2. Buka file → cari marker `<<<<<<<`, `=======`, `>>>>>>>`
3. Gabungkan manual (pilih versi yang benar)
4. `git add <file>` → `git commit` → `git push`

## File khusus

- `wiki/index.md` — katalog semua halaman (link + ringkasan + metadata), update tiap ingest.
- `wiki/log.md` — kronologis append-only. Tiap entry diawali `## [YYYY-MM-DD] ingest | ...` agar grep-able (`grep "^## \[" log.md | tail -5`).

## Kebersihan berkala (audit)

Audit wajib saat lint mingguan atau bila diminta:

- **Urutan `wiki/log.md`** — kronologis menaik; entry baru ditambahkan di AKHIR berkas. Auto-maintenance plugin Obsidian cenderung menyisipkan entry tepat setelah header → pindahkan ke posisi kronologis bila terjadi.
- **Kolom "Terakhir" di `wiki/index.md`** — disinkronkan dari `last_updated` frontmatter tiap halaman, bukan dari tanggal gubahan berkas.
- **Wikilink ke berkas non-markdown** (PDF sumber) — wajib memakai ekstensi, mis. `[[Inpres No. 4 Tahun 1984 tentang Pembinaan dan Pengembangan KUD.pdf]]`, karena tanpa ekstensi tautan tidak terselesaikan.
- **Orphan page** — setiap halaman `entitas/`, `konsep/`, `kasus/` harus punya inbound link.
- **Frontmatter lengkap** — `title`, `aliases`, `tags`, `type`, `source`, `last_updated`, `related` pada setiap halaman wiki.
- **Artefak berat tidak masuk repo** — `analisis/**/jadx/`, `blutter-*/`, `apk/`, `*.pyc` sudah tercakup `.gitignore`; verifikasi dengan `git ls-files` bila ragu.
- **Scaffolding bukan konten wiki** — catatan bawaan plugin/Obsidian dan dokumentasi alat tidak disimpan di `wiki/`, tetapi di root vault.

## Alat (setup & kapan dipakai)

- **Obsidian Git (plugin `obsidian-git`, v2.42.0)** — pengganti Obsidian Sync: auto commit/push tiap 5 menit + auto pull tiap 15 menit (rincian di bagian Sinkronisasi). Butuh `gh auth login` di tiap mesin; plugin memanggil git sistem.
- **Dataview (Obsidian plugin)** — tabel dinamis dari frontmatter. **Sudah terpasang di vault** (`.obsidian/plugins/dataview/`, v0.5.68) dan terdaftar di `.obsidian/community-plugins.json`, sehingga aktif otomatis setelah mesin lain melakukan pull. Blok Dataview ada di `wiki/index.md`. WAJIB frontmatter YAML konsisten di tiap halaman wiki.
- **Karpathy LLM Wiki (Obsidian plugin, `karpathywiki`)** — ingest/query/lint berbasis LLM di dalam Obsidian. Hanya dijalankan di komputer utama; **tidak** di server. Dokumentasi kerja: `Panduan Plugin Karpathy LLM Wiki.md`. Auto-maintenance-nya bisa menyisipkan `index.md`/`log.md` di luar urutan → periksa diff sebelum commit.
- **qmd** (github.com/tobi/qmd) — search engine lokal markdown (BM25/vector + MCP server). **Gunakan bila wiki tumbuh besar (≳100 halaman/sumber)** atau saat `index.md` tidak lagi cukup. Instal: `cargo install qmd` (butuh Rust) atau pakai rilis biner; index folder vault lalu query via CLI/MCP. Untuk skala kecil–sedang, `index.md` sudah cukup.
- **Marp** — slide deck markdown (plugin Obsidian) untuk presentasi dari konten wiki.
- Vault = git repo markdown → version history gratis.

## Tools & Skills Agen (`tools/`)

Folder `tools/` berisi skill siap pakai untuk agen AI (Hermes/LLM lain) — disinkronkan via git agar kemampuan agen ikut berpindah antar mesin:

- `tools/pencarian-putusan-ma/` — skill pencarian putusan Mahkamah Agung via API mobile (apigateway.mahkamahagung.go.id): endpoint, auth (apikey + UA Dart), skenario terverifikasi, script `dirput-api.sh`. Berisi API key — repo ini PRIVATE, jangan publikasikan.
- `tools/scrapling/` — skill scraping web cerdas dan anti-bot (Cloudflare/WAF bypass via Camoufox, dynamic rendering, adaptive selectors) untuk ekstraksi web kasus penipuan, form phishing, direktori putusan, dan dokumen regulasi resmi.
- `tools/agent-reach/` — router akses baca/cari lintas platform publik (YouTube, RSS, V2EX, Bilibili, GitHub, Jina Reader) sebagai pelengkap Scrapling untuk jejaring sosial dan transkrip video.
- `tools/kutipan-hadis/` — skill pencarian, verifikasi, dan kutipan hadis Rasulullah SAW via Hadith API (fawazahmed0/hadith-api): matan Arab berharakat lengkap, terjemahan resmi Indonesia, status derajat hadis (Al-Albani dkk.), dan CLI `hadith`.
- `tools/auto-visualizer/` — skill otomatisasi peringkasan statistik data tabular (CSV, Excel) dan pembuatan grafik visual (distribusi histogram, frekuensi bar chart, korelasi heatmap, tren waktu) berbasis pandas, matplotlib, dan seaborn di venv `~/venvs/docs/`.
- `tools/openviking-backup/` — backup & restore storage OpenViking lokal (`~/.openviking/data`): `backup.py` (snapshot filesystem + SQLite backup API + redaksi API key + sha256 + prune), `run-backup.sh` (wrapper cron pola watchdog: diam kalau sukses, berisik kalau gagal, heartbeat Minggu), dan `SKILL.md`. Dipakai oleh cron Hermes `Backup Harian OpenViking` (harian 02:00 WITA, `no_agent`).

**Instalasi ke agen lokal (server Linux):**
```bash
cp -r ~/penyidikan/tools/pencarian-putusan-ma ~/.hermes/skills/penyidikan/
```
Untuk agen lain: gunakan `TEMPLATE-AGEN-EKSTERNAL.md` (ada di `analisis/direktori-putusan/`) sebagai media transfer.

Setiap penambahan/update skill di `tools/` → WAJIB git sync (aturan sinkronisasi di atas).

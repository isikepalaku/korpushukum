---
id: PERMENDAGRI_72_2022_Pasal_27
uu_induk: Standar Blangko KTP-el dan Penyelenggaraan Identitas Kependudukan Digital
kode_uu: PERMENDAGRI_72_2022
pasal: '27'
status: BERLAKU_AKTIF
substantive_explanation: false
tags:
- hukum/pidana
- uu/permendagri_72_2022
---

# Pasal 27 — Standar Blangko KTP-el dan Penyelenggaraan Identitas Kependudukan Digital

## Batang Tubuh

Peraturan Menteri ini mulai berlaku pada tanggal diundangkan.

Agar 
setiap 
orang 
mengetahuinya, 
memerintahkan 
pengundangan Peraturan Menteri ini dengan penempatannya 
dalam Berita Negara Republik Indonesia. 
 
 
Ditetapkan di Jakarta 
pada tanggal 1 April 2022 
 
MENTERI DALAM NEGERI 
REPUBLIK INDONESIA, 
ttd 
MUHAMMAD TITO KARNAVIAN 
 
Diundangkan di Jakarta 
pada tanggal 13 April 2022 
 
DIREKTUR JENDERAL 
PERATURAN PERUNDANG-UNDANGAN 
KEMENTERIAN HUKUM DAN HAK ASASI MANUSIA 
REPUBLIK INDONESIA, 
 ttd 
BENNY RIYANTO 
 
 
BERITA NEGARA REPUBLIK INDONESIA TAHUN 2022 NOMOR 397 
Salinan sesuai dengan aslinya 
Kepala Biro Hukum, 
 
 ttd 
 
R. Gani Muhamad, SH, MAP 
Pembina Utama Muda (IV/c) 
NIP. 19690818 199603 1001

LAMPIRAN 
PERATURAN MENTERI DALAM NEGERI 
REPUBLIK INDONESIA 
NOMOR 72 TAHUN 2022 
TENTANG STANDAR DAN SPESIFIKASI 
PERANGKAT 
KERAS, 
PERANGKAT 
LUNAK, DAN BLANGKO KARTU TANDA 
PENDUDUK 
ELEKTRONIK 
SERTA 
PENYELENGGARAAN 
IDENTITAS 
KEPENDUDUKAN DIGITAL 
 
 
URAIAN STANDAR DAN SPESIFIKASI PERANGKAT KERAS, PERANGKAT 
LUNAK, DAN BLANGKO KARTU TANDA PENDUDUK ELEKTRONIK 
SERTA PENYELENGGARAAN IDENTITAS KEPENDUDUKAN DIGITAL 
 
I. STANDAR DAN SPESIFIKASI PERANGKAT KERAS DAN PERANGKAT LUNAK 
A. Standar dan Spesifikasi Perangkat Keras 
1. Cip 
a. Struktur data dalam cip mencakup data KTP-el serta data 
dan/atau aplikasi multiguna meliputi: 
1) Struktur data KTP-el 
a) Biodata Penduduk wajib KTP-el dengan ukuran rekaman 
paling rendah 0,5 kilobyte; 
b) Tanda tangan Penduduk wajib KTP-el dengan format 
digital yang dikompresi dengan ukuran rekaman paling 
rendah 0,5 kilobyte; 
c) Pasfoto dengan format digital yang dikompresi dengan 
ukuran rekaman paling rendah 3 kilobyte; dan 
d) Kode keamanan dengan rincian: 
(1) Minutiae per sidik jari dengan ukuran paling rendah 
0,4 kilobyte dan dapat diverifikasi 1:1 dengan referensi 
format INCITS 378 MIN:A atau SNI ISO/IEC 19794-
2:2011; 
(2) Format minutiae sidik jari berdasarkan standar ANSI, 
INCITS atau proprietary yang sudah diuji dalam hal 
interoperabilitas oleh NIST; dan

(3) Tanda 
tangan 
elektronik 
(digital 
signature) 
berdasarkan standar elliptic curve digital signature 
algorithm paling rendah 256 bit atau RSA 2048 bit dan 
hash algorithm SHA-256. 
2) Struktur data multiguna 
Struktur data dan/atau aplikasi tambahan dan mekanisme 
pengamanannya 
untuk 
kebutuhan 
multiguna 
harus 
mendapatkan persetujuan Ditjen. 
b. Memori terdiri dari beberapa hal sebagai berikut: 
1) Ukuran memori penyimpanan paling rendah 32 kilobyte untuk 
menyimpan biodata, tanda tangan, pasfoto dan minutiae sidik 
jari telunjuk tangan kanan dan sidik jari telunjuk tangan kiri 
Penduduk yang bersangkutan serta tambahan data dan/atau 
aplikasi untuk kebutuhan multiguna; 
2) Daya tahan penulisan memori (write endurance) paling rendah 
100.000 kali; 
3) Daya tahan penyimpanan data (data retention) paling singkat 
10 tahun; dan 
4) Pengaturan 
penyimpanan 
data 
(data 
organization) 
menggunakan flexible file system. 
c. Frekuensi radio (radio frequency) terdiri dari beberapa hal sebagai 
berikut: 
1) Berdasarkan standar SNI ISO/IEC 14443-1:2013, SNI 
ISO/IEC 14443-2:2013, SNI ISO/IEC 14443-3:2015, SNI 
ISO/IEC 14443-4:2015, SNI ISO/IEC 14443-1:2018, SNI 
ISO/IEC 14443-4:2018, SNI ISO/IEC 14443-3:2018; dan 
2) Jarak pengoperasian pembacaan dan penulisan (operating 
distance) paling jauh 100 mm. 
d. Keamanan terdiri dari beberapa hal sebagai berikut: 
1) Pembangkit bilangan acak (random number generator) yang 
sesuai standar AIS-31 (P2)/FIPS 140-2 atau pengujian yang 
direkomendasikan oleh Kementerian melalui Ditjen; 
2) Mendukung autentikasi dua arah antara 
smart card 
reader/writer dan cip; 
3) Access conditions diterapkan per file; 
4) Algoritma enskripsi bersifat simetris (symmetric) berdasarkan 
algoritma: minimum 3DES dengan panjang kunci 168 bit,

advanced encryption standard (AES) atau lebih tinggi 
dan/atau algoritma lainnya sesuai kebutuhan; 
5) Memenuhi syarat ketunggalan transaksi (anti tear), supported 
by cip; 
6) Memiliki perangkat keras crypto co-processor; 
7) KTP-el 
didukung 
dengan 
pengamanan 
melalui 
sistem 
manajemen kunci (key management system); dan 
8) Keamanan (security) data dan/atau aplikasi tambahan untuk 
kebutuhan 
multiguna 
disesuaikan 
dengan 
kebutuhan 
pemanfaatan dan persyaratan keamanan penggunaan data 
(baca dan tulis). 
e. Lain-lain meliputi hal sebagai berikut: 
1) Cip adalah smart card nirsentuh yang berbasis CPU 
(microcontroller chip) dan menggunakan sistem operasi 
(operating system) terbuka; 
2) Electro static discharge paling rendah ESD 2 kV; 
3) Cip pada blangko kartu bekerja dengan baik pada suhu 
(temperature) dari -25ºC sampai dengan 70ºC; dan 
4) Memerlukan pasokan daya (voltage) dari 2,7 volt sampai 
dengan 3,6 volt. 
2. Perangkat pembaca dan penulis (card encoder) KTP-el pada blangko 
kartu terdiri dari beberapa hal sebagai berikut: 
a. Smart card encoder 
1) Standar: SNI ISO/IEC 14443-1:2013, SNI ISO/IEC 14443-
2:2013, SNI ISO/IEC 14443-3:2015, SNI ISO/IEC 14443-
4:2015, SNI ISO/IEC 14443-1:2018, SNI ISO/IEC 14443-
4:2018, SNI ISO/IEC 14443-3:2018. 
2) Frekuensi: 13,56 MHz ± 7 KHz. 
3) Baudrate [kbit/s]: 106, 212, 424, 848 kbps. 
4) Kuat medan operasi: dari 1,5 A/m (rms) sampai dengan 7,5 
A/m (rms). 
5) Jarak transaksi: maksimum 10 cm. 
6) Slot Secure Access Module (SAM): mendukung paling sedikit 1 
slot SAM (SAM ditanam di dalam smart card encoder). 
7) Keamanan: Memiliki mekanisme perlindungan keamanan 
terhadap SAM. 
8) Interface: USB

9) Autentikasi: mendukung autentikasi dua arah antara smart 
card encoder dan cip 
10) Protokol: T=0, T=1, dan T=CL. 
11) Komunikasi dengan Komputer (Host Protocol): personal 
computer/smart card (PC/SC) pada windows atau linux. 
12) Fitur/Fungsi: 
a) menuliskan data ke dalam cip KTP-el. 
b) melakukan verifikasi keabsahan cip KTP-el. 
c) membaca data KTP-el (rekaman biodata, pas photo, tanda 
tangan dan sidik jari) dari cip KTP-el. 
d) melakukan verifikasi keabsahan data KTP-el. 
e) menampilkan data KTP-el (rekaman biodata, pas photo, 
tanda tangan). 
f) 
melakukan aktivasi cip KTP-el. 
g) menyimpan riwayat transaksi. 
h) mampu mengirimkan hasil pembacaan data KTP-el 
(rekaman biodata, pas photo, tanda tangan) ke perangkat 
komputasi eksternal. 
i) 
indikator berhasil atau tidaknya sebuah transaksi (visual 
berupa layar LCD atau setara, atau audio berupa buzzer 
atau setara). 
13) Perangkat pembaca dan penulis (card encoder) KTP-el 
terhadap data dan/atau aplikasi tambahan untuk kebutuhan 
multiguna disesuaikan dengan kebutuhan pemanfaatan dan 
persyaratan keamanan pengunaan data (baca dan tulis). 
14) Lain-lain : software development kit. 
b. SAM pada smart card encoder 
1) Cip: smart card kontak (contact smart card) berbasis 
microprocessor. 
2) Standar: SNI ISO/IEC 7816-1:2013, SNI ISO/IEC 7816-
2:2013, SNI ISO/IEC 7816-3:2015, SNI ISO/IEC 7816-4:2015 
(protokol T=1). 
3) Instruction Set: SNI ISO/IEC 7816-1:2013, SNI ISO/IEC 7816-
2:2013, SNI ISO/IEC 7816-3:2015, SNI ISO/IEC 7816-4:2015. 
4) Kapasitas EEPROM: minimal 32 KB. 
5) Daya tahan penyimpanan data: paling singkat 10 tahun.

6) Crypto co-processor: memiliki 
crypto co-processor 
yang 
mendukung algoritma penyandian minimal pada 3-Key Triple-
DES (3KTDEA) dengan panjang kunci paling rendah 168-bit, 
algoritma hash SHA256 serta mendukung digital signature 
dengan menggunakan ECDSA 256-bit dengan point curve 
secp256r1 dan/atau algoritma lainnya sesuai kebutuhan. 
7) Pembangkit bilangan acak: standar FIPS 140-2 atau AIS-31 
(P2). 
8) Sertifikasi keamanan: memiliki sertifikasi keamanan dengan 
tingkat jaminan keamanan paling rendah common criteria 
EAL5+ atau FIPS 140-2 (atau standar FIPS yang lebih terbaru) 
paling rendah tingkat 4. 
9) Mutual authentication : mendukung proses autentikasi dua 
arah antara smart card dan encoder dengan mekanisme 
umpan-balik (mutual authentication). 
10) Anti cloning : memiliki proteksi terhadap penggandaan secara 
ilegal. 
11) Mode: dengan fungsi baca tulis. 
12) Kartu SAM dalam operasionalnya dapat digantikan dengan 
kode kunci. Kode kunci adalah metode yang digunakan selain 
menggunakan kartu SAM secara fisik. Penggunaan kode kunci 
setelah dilakukan Proof of Concept (PoC) dan memenuhi 
standar keamanan informasi. 
3. Perangkat server yang meliputi: 
a. Platform perangkat server berbentuk rak mounted atau blade; 
b. Kinerja (performance) perangkat server bersifat upgradeable dan 
scalable; 
c. Sistem operasi (operating system) berbasis linux/windows; 
d. Basis data berbasis standar RDBMS (Relational Database 
Management System), seperti MySQL, Oracle, MS SQL server atau 
setara; 
e. Perangkat lunak (software) untuk penunggalan data Automated 
Biometric Identification System (ABIS) tersedia di pusat; 
f. 
Sistem ABIS tidak boleh mengikat pada perangkat dan harus bisa 
menyesuaikan dengan perkembangan teknologi perangkat; dan 
g. Sistem ABIS dapat mengolah gambar (image) sidik jari, iris, pas 
foto dalam bentuk minutiae.

4. Perangkat klien yang meliputi: 
a. Platform perangkat keras berbasis PC dan berbasis laptop untuk 
pelayanan mobile; 
b. Sistem operasi (operating system) berbasis windows atau yang 
setara; 
c. Basis data berbasis standard RDBMS, seperti MySQL, Oracle, MS 
SQL Server atau setara untuk pelayanan mobile; 
d. Perangkat lunak (software) klien dapat mendukung verifikasi 
secara realtime; 
e. Perangkat lunak (perekaman dan pencetakan) terintegrasi dengan 
SIAK yang sudah berjalan; dan 
f. 
Selain perangkat keras dan perangkat lunak di atas pada klien 
dilengkapi dengan perangkat smart card encoder beserta SAM 
atau kode kunci, perangkat pemindai sidik jari, perangkat 
pemindai iris, perangkat pemindai tanda tangan, perangkat 
kamera dan perangkat pencetak KTP-el. 
5. Pemindai sidik jari (fingerprint scanner) yang meliputi: 
a. Pemindai hidup (live scanner) berbasis optik, pemindai sepuluh 
jari (ten finger scanner); 
b. Pemindai dengan kemampuan resolusi (scanner resolution) paling 
rendah 356 x 292 pixels 500 dpi; 
c. Driver berbasis linux/windows atau yang setara; 
d. Ukuran pelat minimal 3,2 inch x 3,0 inch; 
e. Area pelat aktif minimal 3,2 inch x 3,0 inch; 
f. 
Format pengambilan single rolled/flat finger, four finger slaps, two 
thumbs; 
g. Kecepatan tangkap empat jari dan dua ibu jari minimal 3 frames 
per second; 
h. Gambar pixel empat jari kanan dan kiri serta dua ibu jari minimal 
1600 x 1500 Pixels; 
i. 
Distortion ± 1%; 
j. 
Tingkat abu-abu minimal 256; 
k. Antarmuka (interface) USB minimal 2.0; 
l. 
Sertifikasi FBI Appendix F, CE, FCC, KCC, BIS, RoHS, IP54, SNI IEC 
60950-1:2016, BSI-TR-03104, WHQL. 
6. Pemindai iris (iris scanner) yang meliputi: 
a. Dapat digenggam atau dipegang (hand-held)/diletakkan;

b. Resolusi spatial minimal 60% @4.0 Lp/mm; 
c. Resolusi pixel minimal 16 pixel/mm; 
d. Kedalaman pixel minimal 8 bits/pixel; 
e. Jarak pengambilan minimal 20 mm; 
f. 
Pengambilan gambar secara otomatis dilengkapi dengan ukuran 
kualitas gambar yang sudah menyatu dengan perangkat; 
g. Gambar kedua iris dapat ditangkap (captured) secara bersamaan 
(simultaneously); 
h. Panjang gelombang pencitraan antara 700 – 900 nm; 
i. 
Sensor signal to noise (S/N) ratio minimal 36 dB; dan 
j. 
Antarmuka (interface) minimal USB 2.0. 
7. Perangkat pemindai tanda tangan yang meliputi: 
a. Sensor type active electromagnetic; 
b. Pen type active energized; 
c. Lebar layar minimal 4.3 inches; 
d. Resolution minimal 400 true points per inch; 
e. Data conversion rate minimal 300 points per second; 
f. 
Antarmuka (interface)USB minimal 2.0; dan 
g. Supported OS windows/linux. 
8. Perangkat kamera yang meliputi: 
a. Model type APS-C digital SLR; 
b. Sensor high quality CCD or CMOS; 
c. Image resolution minimal 12 Mega Pixel; 
d. Image size large, medium, small; 
e. Image format JPEG; 
f. 
Power source li-ion battery; 
g. Auto focus model al focus,one shot,al servo; 
h. LCD minimal 2.7 inch; 
i. 
PC Connectivity minimal USB 2.0; 
j. 
Lensa minimal 18 mm; 
k. Tinggi tripod minimal 48 cm; dan 
l. 
Tripod bahan metal, aluminium, atau sejenisnya. 
9. Perangkat perekaman dapat dimungkinkan untuk diintegrasikan 
menjadi satu alat dengan mengikuti minimal spesifikasi yang sudah 
ditentukan di atas (misal: iris scanner dan kamera menjadi satu alat, 
signature pad dan finger print menjadi satu alat, dan lainnya).

10. Perangkat alat cetak KTP-el meliputi: 
a. Metode pencetakan menggunakan High Definition Printing (HDP), 
thermal transfer (re-transfer printing); 
b. Resolusi pencetakan minimal 300 dot per inch (dpi); 
c. Jumlah warna pencetakan sampai dengan 16.7 juta/256 corak 
per pixel; 
d. Koneksi menggunakan USB minimal 2.0; 
e. Printing speed (with transfer) maksimal 32 sec/card (tanpa 
encode); 
f. 
Kapasitas ribbon YMCK minimal 500 prints; 
g. Kapasitas HDP film minimal 500 prints; 
h. Ukuran kartu: CR-80; 
i. 
Ketebalan kartu: 30-50 mil; 
j. 
Jenis kartu: ABS, laminated PVC, PET, PET-G, proximity, smart and 
mag stripe cards (PVC, ABS, PET, PET-G, POLYCARBONATE (PC)); 
k. Print area: mencakup seluruh area kartu CR-80; 
l. 
Daya tampung hopper: 
a) Input minimal 100; 
b) Tray minimal 100; dan 
c) User antarmuka (interface): tersedia secara grafis 
d) Dapat ditambahkan modul smart card contactless encoder; 
e) Drivers mendukung operating system: windows dan/atau 
linux; dan 
f) 
Tegangan listrik: 100-240 VAC 
 
B. Standar dan spesifikasi Perangkat Lunak 
1. Automated Biometric Identification System (ABIS), terdiri atas: 
a. Sidik jari tak tergantung putaran (rotation independent) dan dapat 
diputar hingga 360 derajat; 
b. Pemadanan (matching) mendukung 1:N pemadanan (matching) 
untuk identifikasi dan 1:1 pemadanan (matching) untuk verifikasi 
yang terintegrasi; 
c. Jenis pencarian (type of searches) meliputi sepuluh sidik jari 
(tenprint), sidik jari laten-sepuluh sidik jari (latentprint-tenprint), 
dan tambahan fungsi pencarian berdasarkan empat empat dua 
sidik jari atau satu sidik jari dan mata serta foto;

d. Hasil pemadanan (matching results) ditampilkan dalam bentuk 
daftar ketukan (hit list) dengan layar terbelah (split screen) dan 
ambang batas yang dapat disesuaikan (adjustable threshold); 
e. Sistem 
yang 
dikembangkan 
juga 
memiliki 
kemampuan 
identifikasi atau autentikasi 1:1 baik melalui jari, iris maupun 
foto; 
f. 
Kapasitas penyimpanan (storage capacity) bersifat tak terbatas 
(unlimited), dapat ditingkatkan (upgradeable) dan kinerja dapat 
berskala (scalable performance); 
2. Pasfoto terintegrasi secara penuh (fully integrated) atau mudah untuk 
antarmuka (interface) dengan basis data yang sudah ada dan 
memenuhi jpeg color image compression; 
3. Biodata terintegrasi secara penuh (fully integrated) atau mudah untuk 
antarmuka (interface) dengan basis data yang sudah ada; 
4. Hasil pemadanan sidik jari (matching results finger) pernah masuk 
dalam sepuluh besar dari National Institute of Standards and 
Technology Internal Report (NISTIR), Amerika Serikat mulai tahun 
2003 sampai dengan sekarang; 
5. Kinerja pemadanan (matching performance) memiliki kecepatan paling 
rendah 100.000 pemadanan ABIS per detik per prosesor (core), dapat 
berskala sesuai dengan jumlah prosesor (scalable to number of 
processors), dan memiliki kemampuan pencarian data tak terbatas 
(unlimited number of data searchability); 
6. Middleware yang digunakan mengacu pada standar terbuka; 
7. Aplikasi untuk perekaman KTP-el (B-Enroller) memiliki fungsi sebagai 
berikut: 
a. Citra sidik jari (fingerprint images) memiliki sifat: 
1) Minimum 500 dpi, 256 gray level; 
2) ANSI/NIST compliant; dan 
3) WSQ compression: 1:10 for ten prints, 1:15 for latent prints. 
b. Image sidik jari (fingerprint image) mengikuti standar ANSI/NIST 
ITL-1-2000 atau SNI ISO/IEC 19794-5:2011, SNI ISO/IEC 19794-
5:2011, SNI ISO/IEC 19794-13:2018; 
c. Finger print scanner, iris scanner, signature pad, perangkat 
kamera dapat saling terintegrasi di aplikasi perekaman;

d. Terintegrasi dengan data kependudukan, tanda tangan, pas foto 
dan minutiae sidik jari telunjuk kanan dan kiri sebagai primary 
atau jari lainnya sebagai primary dalam hal exception; 
e. Apabila sidik jari tangan tidak bisa direkam, dilakukan 
perekaman foto dengan kedua tangan Penduduk yang tidak dapat 
direkam dan kemudian dilakukan perekaman iris dan foto yang 
bersangkutan ke dalam basis data kependudukan untuk 
dilakukan penunggalan. Apabila iris tidak bisa dilakukan 
perekaman, dilakukan pengecualian terhadap iris yang kemudian 
dilakukan perekaman sebagaimana biasanya; 
f. 
Apabila kedua tangan Penduduk dan iris tidak bisa dilakukan 
perekaman maka dilakukan pengecualian dan dilanjutkan 
perekaman dan penunggalan dengan menggunakan wajah; 
g. Data hasil perekaman biometrik Penduduk dapat dikirimkan ke 
data center pusat dengan menggunakan web service agar dapat 
dilakukan proses penunggalan. 
8. Aplikasi untuk pencetakan KTP-el (B-Card management) yang 
meliputi memiliki fungsi sebagai berikut: 
a. Finger print scanner, iris scanner, signature pad, perangkat kamera 
dapat saling terintegrasi di aplikasi pencetakan; 
b. Terintegrasi dengan data kependudukan, tanda tangan, pas foto 
dan minutiae sidik jari telunjuk kanan dan kiri sebagai primary 
atau jari lainnya sebagai primary dalam hal exception yang 
disimpan pada cip blangko KTP-el dengan menggunakan smart 
card encoder; 
c. Mendukung 1:N pemadanan (matching) dengan menggunakan 
sidik jari secara live capture dan atau iris mata secara live capture 
dan atau pasfoto secara live capture; 
d. Melakukan proses penggantian paspoto dan atau tanda tangan 
perekaman sebelumnya dengan adanya proses verifikasi terlebih 
dahulu. 
 
II. STANDAR DAN SPESIFIKASI BLANGKO KARTU TANDA PENDUDUK 
ELEKTRONIK 
A. Material terbuat dari bahan PET/PETF/PETG/PC = PET (polyethylene 
terephthalate), PETF (polyethylene terephthalate film), PETG (polyethylene 
terephthalate glycol) atau PC (polycarbonate);

B. Teknologi printing background blangko KTP-el menggunakan offset 
printing; 
C. Teknologi 
printing 
personalisasi 
menggunakan 
dye 
sublimation 
(retransfer) atau setara; 
D. Printing 
warna 
dipergunakan 
untuk 
mencetak 
latar 
belakang 
(background) blangko dan pasfoto; 
E. Karakteristik fisik, mempunyai ukuran 85,60 x 53,98 mm, warna biru 
gradasi untuk blangko KTP-el untuk warga negara Indonesia, warna 
oranye gradasi untuk blangko KTP-el untuk warga negara asing, 
ketebalan dari 0,76 mm sampai dengan 1 mm kedap air (waterproof) 
sesuai SNI ISO/IEC 7810:2015; 
F. Susunan lapisan (layer) terdiri atas: 
1. Tampak Depan 
a. Lapisan pelindung transparan; 
b. Uraian desain tampak depan terdiri atas: 
1) Area judul pada bagian atas terdapat tulisan “KARTU TANDA 
PENDUDUK REPUBLIK INDONESIA”; 
2) Area logo atau gambar: 
a) Pada gambar depan sebelah kiri atas terdapat gambar 
Lambang Negara Kesatuan Republik Indonesia “Burung 
Garuda Pancasila”; dan 
b) Terdapat peta Kepulauan Indonesia. 
3) Area penempatan cip berada pada sebelah kiri di dalam 
blangko KTP-el; dan 
4) Keamanan pencetakan (security printing) harus mencakup 
minimal 2 (dua) level fitur keamanan atau setara dengan 
hologram dan microtext. 
c. Lapisan pelindung bagian depan; 
d. Inlay pad, sebagai lapisan pelindung cip bagian depan; 
e. Inlay core, lapisan yang berisi cip dan antenna; 
f. 
Inlay pad, sebagai lapisan pelindung cip bagian belakang; dan 
g. Lapisan pelindung bagian belakang. 
2. Tampak belakang 
a. Keamanan pencetakan (security printing) atau setara dengan 
gambar peta kepulauan Indonesia di dalam bola dunia; 
b. Lapisan personalisasi yang terlaminasi atau terlapisi oleh overlay; 
dan

c. Teknologi ultraviolet invisible full colour spectrum design. 
G. Desain blangko KTP-el untuk warga negara Indonesia: 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
H. Desain blangko KTP-el untuk warga negara asing: 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
6 
7 
1 
3 
2 
4 
5 
1 
5 
4 
3 
2 
7 
6

Keterangan: 
1. Tulisan Kartu Tanda Penduduk; 
2. Lambang burung garuda pancasila; 
3. Peta kepulauan Indonesia; 
4. Area penempatan cip; 
5. Fitur keamanan hologram dan microtext; 
6. Peta kepulauan Indonesia; dan 
7. Fitur keamanan teknologi ultraviolet invisible full colour spectrum 
design. 
 
III. STANDAR PROTOKOL IDENTITAS KEPENDUDUKAN DIGITAL 
A. Standar protokol yang dipergunakan untuk membuat Identitas 
Kependudukan Digital dan protokol komunikasi pertukaran data 
Identitas Kependudukan Digital berdasarkan standar terbuka seperti 
OIDC (openid connect) + OAuth2.0, SAML (Security Assertion Markup 
Language), hyperledger atau setara. 
B. Aplikasi yang dipasangkan mendukung terhadap perangkat mobile yang 
tersedia saat ini. 
C. Aplikasi tidak terkendala terhadap upgrade operating system pada alat 
mobile. 
 
MENTERI DALAM NEGERI 
REPUBLIK INDONESIA, 
ttd 
MUHAMMAD TITO KARNAVIAN 
 
Salinan sesuai dengan aslinya 
Kepala Biro Hukum, 
 
 
 ttd 
 
R. Gani Muhamad, SH, MAP 
Pembina Utama Muda (IV/c) 
NIP. 19690818 199603 1001

## Penjelasan Resmi

Cukup jelas.

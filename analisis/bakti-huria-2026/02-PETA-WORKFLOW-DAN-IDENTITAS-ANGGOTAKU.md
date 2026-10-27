# PETA WORKFLOW & IDENTITAS — APLIKASI ANGGOTAKU (MobileBMT)

**Unit:** Subdit II Fismondev Ditreskrimsus Polda Sulsel
**Tanggal analisis:** 16 Oktober 2026 (WITA)
**Metode:** REA (Reverse Engineer Anything) 6.4.0 — provider `jadx-headless-mcp` 0.7.1 + `rea-artifact-graph` + Apktool 2.7.0
**Klasifikasi berkas:** bukti digital — analisis statis, APK **tidak pernah dieksekusi**

---

## 1. IDENTITAS & INTEGRITAS BERKAS (Chain of Custody)

| Parameter | Nilai |
|---|---|
| Nama berkas bukti | `doc_82d8408fc891_ANGGOTAKU.apk` |
| Lokasi | `/home/ubuntu/.hermes/cache/documents/doc_82d8408fc891_ANGGOTAKU.apk` |
| Ukuran | 9.320.153 byte |
| MD5 | `0e66680dfa6db2d19c7d62ae67eaf259` |
| SHA-1 | `cd4d684e2b9ff09c71c0d5e2cb8124e48f61e734` |
| **SHA-256** | `c2dbe3b58ebae731f25117104b3b256f1085545b681f300dcc6811f9d98cc931` |
| Format | APK (base APK bundle AAB) |
| Package | `com.baktihuria.mobilebmt.anggotaku` |
| Versi | 9.1.2 (versionCode 912) |
| minSdk / targetSdk | 23 / 37 |
| Komponen | 99 activity, 8 service, 6 receiver, 4 provider |
| Kelas DEX | 4.765 (inventaris REA `coverage: complete`) |

**Catatan kesamaan berkas:** SHA-256 identik dengan berkas yang dianalisis 22 September 2026 (`~/laporan_anggotaku.md`, `~/triage_anggotaku.json`, `~/anggotaku_decompiled/`). Temuan triage lama tetap berlaku untuk berkas ini.

---

## 2. REGISTER EVIDENCE REA

Semua artefak mentah tersimpan di `~/penyidikan/analisis/bakti-huria-2026/rea/`.

| Berkas evidence | Operasi | Evidence ID |
|---|---|---|
| `01-package.yaml` | `inspect_android_package` | `ev_6f1426c80df026373f1b91f347642157528fcf4480f1b6a74233116bfd3f69fc` |
| `02-allclasses.yaml` | `search_android_classes` (inventaris penuh) | `ev_6a077118b63b3b700d076b572ad61066756730d7ea358436d517dd94228350b2` |
| `10-class-01-…SplashActivity.yaml` | `inspect_android_class` | `ev_6d1f773429c7e0bc6687d0eaa8d934179454ae460c17b90003587210c71681d8` |
| `10-class-02-…ControllerActivity.yaml` | `inspect_android_class` | `ev_796a4c7d8370da1013f510645713d7bca42b75cec3f3bcdc53fb60b842204e98` |
| `10-class-03-…utils.MyVariable.yaml` | `inspect_android_class` | `ev_14bb7009e0c4bfb3c6625f4edaaad287188d82e03b2c4b05ea9c923f5d39c236` |
| `10-class-04-…PreRegistrasiActivity.yaml` | `inspect_android_class` | `ev_19fdb78470e6c3bb0d14286ec429cbbcbfd9a1961b93980c2b6ce19030870c41` |
| `10-class-05-…IsiFormulirActivity.yaml` | `inspect_android_class` | `ev_c2c66a8e7783201d56b2cdef4704ead5a8aedcb1637fc184d5156df88409a4ee` |
| `10-class-06-…AktivasiActivity.yaml` | `inspect_android_class` | `ev_4315f20b75e22389bd40bcd804cc1b03fd60605d4f1881b8078f7d4ae91aa47d` |
| `10-class-07-…LupaPin.yaml` | `inspect_android_class` | `ev_796109af615d9436b1619b74bf01a944cdcc206568b65d90a0548e800789ccc7` |
| `10-class-08-…ForwardSMS.yaml` | `inspect_android_class` | `ev_53a0a3f203c6e4650e1fbc80e7b7214f885ca8b6afeb4953c135295b4c0702bd` |
| `10-class-09-…MyFirebaseMessagingService.yaml` | `inspect_android_class` | `ev_62a2d5882de744b7698b11418b5fed84f86c58915257ae328d6d6a81efd1f31b` |
| `20-xref-…AktivasiActivity.yaml` | `trace_android_references` | `ev_5685180bf34c0a0628b586cb522f2acce0ab3c70e070f45192a17bafb8d04c7b` |
| `20-xref-…MyVariable.yaml` | `trace_android_references` (41 referensi) | `ev_490f4e0678a1a85b9a6a3c1a0e9197d28192fa24cdf7c0ecf5a289451685564f` |
| `20-xref-…SplashActivity.yaml` | `trace_android_references` (7 referensi) | `ev_f2806b49a188f0b97e29667bc506013161774b936d0991f2908629f612ac5f10` |

Evidence pendahuluan sesi 07:25–07:28 (16 Okt 2026), tersimpan di `~/.hermes/cache/terminal-output/`:
`ev_cac4460…9cdbf` (`inspect_artifact` / rea-artifact-graph, seluruh entri `hash_status: verified`), `ev_8c42730…69d75` (`inspect_android_package` JADX — LOADED, 4765 kelas), `ev_b8002fa…4f2af` (`search_android_classes` kueri "Aktivasi"), `ev_6b3d3a8…c1f49` (`decode_android_resources` Apktool).

Sifat bukti: `confidence: observed`, `authority: shipped-artifact`, seluruh artefak ber-`coverage: complete`.

---

## 3. PETA WORKFLOW APLIKASI

### 3.1 Rantai masuk (gate identitas perangkat)

```
SplashActivity
  ├─ permintaan izin: READ_PHONE_STATE, CAMERA, READ_CONTACTS
  │   (+ WRITE_EXTERNAL_STORAGE untuk API < 33)
  └─ cek kodebmt ∈ {0045, 0078, 0123}      → build white-label multi-BMT
        ↓
ControllerActivity  (GERBANG UTAMA)
  ├─ ambil IMSI/token SIM      : d.r(this)      → "TIDAK ADA KARTU" bila SIM tidak siap
  ├─ token saat ini            : d.n(strImsi)
  ├─ prefs "config" → METAREG  : token terdaftar (terenkripsi)
  ├─ prefs "config" → 3D0k     : kredensial akun
  └─ keputusan:
       METAREG/3D0k kosong ATAU token ≠ METAREG  → PreRegistrasiActivity
       token cocok                               → InfoActivity
                                                   (atau NotificationActivity bila is_notif=true)
```

**Konsekuensi hukum/teknis:** aplikasi mengikat akun ke kombinasi **perangkat + SIM**. Nomor SIM berbeda atau `android_id` berbeda → dipaksa registrasi ulang. Ini kontrol anti-sharing akun.

### 3.2 Rantai registrasi → aktivasi

```
PreRegistrasiActivity  (syarat & ketentuan; butuh "nomor registrasi" dari CS kantor layanan)
        ↓  btn_setuju (x3.y0)
Registrasi2Activity
        ↓  (x3.e1 / x3.f1)
IsiFormulirActivity    — formulir anggota:
        ed_nik_cek, ed_form_nama, ed_form_ktp, ed_form_tempatlahir, ed_form_tgllahir,
        ed_form_ibu (nama ibu kandung), ed_form_telp, ed_form_email, ed_form_alamat,
        ed_form_ahliwaris, ed_form_wali, ed_form_referral, ed_captcha, sp_cabang
        (varian form per kode BMT: _602 / _606 / _607 → nomor VA, bank, kode institusi, jenis trx)
        ↓  (x3.c0 / x3.u)
IsiFormulirBerkasActivity   — unggah berkas identitas
        ├─ CameraActivity / Camera2Activity   (foto KTP)
        ├─ GooglyEyesActivity                 (liveness/selfie)
        └─ SyaratKetentuanActivity            (startActivityForResult, request 600)
        ↓
Registrasi2Activity  →  AktivasiActivity   (dikonfirmasi REA xref: Registrasi2Activity mereferensikan AktivasiActivity)
        ↓
AktivasiActivity   — POST ke endpoint `urlAktivasi2`
        payload: kodeaktivasi, nokartu, imsi, kodebmt
        + fingerprint perangkat (lihat §4.3)
        ↓  (e3.e)
BaruPin            — PIN standar (hanya untuk cek saldo & mutasi terakhir)
        ↓  (x3.g)
NewMainActivity    — dashboard
```

Teks resmi aplikasi (`res/values/strings.xml`) mengonfirmasi kontrol berjenjang:
- `text_pre_2_2`: anggota mengisi formulir registrasi **di kantor layanan** dengan menyerahkan salinan identitas.
- `text_pre_2_4`: registrasi dengan **nomor registrasi dari customer service** kantor layanan.
- `text_pre_2_5`–`text_pre_2_7`: PIN standar diperoleh **setelah aktivasi berhasil**; transaksi finansial baru bisa setelah PIN diubah.

### 3.3 Rantai transaksi (pasca-login)

```
NewMainActivity (dashboard)
  ├─ PIN transaksi        : PinInputActivity, PinInputPPOBActivity
  ├─ Ganti PIN / Lupa PIN : dashboard.akun.GantiPin, registrasi.LupaPin
  ├─ Logout / aktivasi ulang : registrasi.LogoutActivity
  ├─ Layanan (service)
  │    ├─ MyFirebaseMessagingService (FCM push) → NotificationActivity → NewMainActivity
  │    ├─ notifications.tosqlite.SQLService (arsip notifikasi ke SQLite)
  │    ├─ NotificationWakeBroadcastReceiver, FirebaseDataReceiver
  │    └─ Provider: FirebaseInitProvider, FileProvider, PicassoProvider
  ├─ Transfer    : AntarRekening, AntarBank, Emaal, ScannerEmaalActivity, DaftarRekening/Bank/Emaal
  ├─ Pembelian   : Pulsa, PLN, EToll, Uang (DaftarPulsa/PLNPembelian/DaftarEToll/DaftarUang)
  ├─ Pembayaran  : BPJS, PDAM, PLN, Telkom, Multifinance
  ├─ Donasi/ZS   : Donasi, DonasiEvent; LAZ (urlLAZ), LKAF (urlLKAF), Infaq (urlInfaq)
  ├─ E-Warkat    : LihatEWarkatActivity, StrukEWarkatActivity (MDA)
  ├─ Informasi   : InfoMutasi, InfoPoinKu, InfoSimpanan, InfoPembiayaan, ProdukActivity,
  │                PromoActivity, KantorLayanan, InfoBiaya, KalkulatorZakat, PrivacyActivity
  ├─ Scan/QR     : ScanActivity, QRProfileActivity, ZoomQRActivity, ZoomBarcodeActivity
  └─ Akun        : AkunDetailActivity, AboutTentang, ContactUsActivity, Inbox, InboxList,
                   CaraVAActivity, ForwardSMS, PrivacyActivity
```

### 3.4 Konfirmasi silang via `trace_android_references` (REA)

| Kelas sasaran | Referensi masuk (containing class) | Makna |
|---|---|---|
| `AktivasiActivity` | `Registrasi2Activity`, `e3.e`, `x3.a`, `x3.b`, `x3.c`, `b3.i0` | mengunci urutan **Registrasi2 → Aktivasi**; `e3.e` pemanggil jaringan, `x3.a/b/c` penanganannya, `b3.i0` pengatur waktu/countdown aktivasi |
| `SplashActivity` | `MyFirebaseMessagingService`, `f4.d`, `z2.q`, `z2.r`, `b3.g`, `m3.g`, `sa.d` | splash dapat dipicu ulang dari notifikasi FCM; `z2.q`/`z2.r` merutekan splash → `ControllerActivity` |
| `utils.MyVariable` | 41 kelas, termasuk `SplashActivity`, `ControllerActivity`, `InfoActivity`, `AkunDetailActivity`, `CaraVAActivity`, `ProdukActivity`, serta seluruh paket transaksi `b3.*` | menegaskan `MyVariable` sebagai pemegang identitas server (base URL, kredensial, URI) — seluruhnya dari JNI |

---

## 4. PETA IDENTITAS

### 4.1 Identitas aplikasi & kanal

| Elemen | Nilai |
|---|---|
| Nama aplikasi | **ANGGOTAKU** (MobileBMT) |
| Package | `com.baktihuria.mobilebmt.anggotaku` |
| `app_id` internal | `com.baktihuria.mobilebmt.anggotaku-PRO` |
| `channel_id` | `anggotaku-01-PRO` |
| `kodebmt` | `0123` |
| `application` / nama URL | `mobilebmtanggotaku` |
| Basis data notifikasi | `mobilebmtanggotakunotifications` |
| Path core banking | `/M-BMT` |
| Ikon play | `https://play.google.com/store/apps/details?id=com.baktihuria.mobilebmt.anggotaku` |

### 4.2 Identitas penyelenggara & pihak ketiga

| Elemen | Nilai | Sumber |
|---|---|---|
| Lembaga penyelenggara | **KSPPS Bakti Huria Syariah** (`nama_instansi`) | `strings.xml` |
| Naskah pre-registrasi | "Registrasi ANGGOTAKU untuk Anggota KSPPS Bakti Huria Syariah" | `strings.xml` |
| Call center | 08123000861 (`call_center`, `jam_layanan`) | `strings.xml` |
| Situs/legal | `baktihuria.co.id/privacy-policy` | `strings.xml` |
| Layanan pelanggan daring | `https://t.me/CSANGGOTAKU` | `strings.xml` |
| Vendor core banking | **PT USID** — kredit aplikasi "©2016 PT. UGT System Integrator", `www.usid.co.id` | `strings.xml` |
| Infrastruktur awan vendor | Firebase project `usid-mobile-3`; RTDB `https://usid-mobile-3.firebaseio.com`; bucket `usid-mobile-3.appspot.com`; sender `1024224325332`; `google_app_id 1:1024224325332:android:c77b7070ac4acaf75ad541` | `strings.xml` |

### 4.3 Identitas perangkat & binding akun

Dikirim sebagai parameter pada proses aktivasi (`f4.d.d(Context)` + `imsi`):

| Kunci | Isi |
|---|---|
| `manufacture`, `brand`, `model`, `hardware`, `device`, `product` | `android.os.Build.*` |
| `androidversion`, `os` | versi SDK & `Build.VERSION.INCREMENTAL` |
| `rooted` | hasil uji root pada perangkat (true/false) |
| `appid`, `vername`, `vercode`, `buildtype` | `com.baktihuria.mobilebmt.anggotaku`, `9.1.2`, `912` |
| `imsi` | token turunan: `android_id` + ID langganan SIM (`Settings.Secure android_id` + `SubscriptionManager.getActiveSubscriptionInfoList`) |
| `kodeaktivasi`, `nokartu`, `kodebmt` | diterbitkan kantor layanan saat registrasi |

Penyimpanan lokal: SharedPreferences `config` (kunci `METAREG`, `3D0k`) dan `usid_firebase` (`fbaseToken`, `statusnotification`). Nilai `METAREG` dienkripsi `PBEWithMD5AndDES` (PBE parameter `{-34,51,16,18,-34,51,16,18}`, iterasi 20), frasa sandi diambil dari method native **`MyVariable.appsCode()`**.

### 4.4 Lapisan yang tidak dapat dibaca dari berkas ini

Seluruh nilai berikut berasal dari pustaka native **`libnative-lib.so`** melalui JNI (`MyVariable`), dan **`lib/` tidak ada** di berkas ini:

`URL_BASE_ENC`, `URL_BASE_PPOB_ENC`, `URL_BASE_CONTENT_ENC`, `URL_VA_ENC`,
`URI_LOGIN`, `URI_RELOGIN`, `URI_CEKNIK`, `URI_INSERTREG`, `URI_PUTREG`, `URI_LOGOUT_PIN`,
`URI_LIHAT_EWARKAT_JNI`, `URI_STRUK_EWARKAT_JNI`, `ENCRYPTION_CODE_JNI`,
`username()`, `pass()`, `appsCode()`, `appsCode4()`, `AktivasiDemoLast()`, `RekDemoLast()`, `TelpDemoLast()`.

Dasar: `System.loadLibrary("native-lib")` pada `utils/MyVariable.java`; berkas APK tidak memuat entri `lib/…`, sesuai metadata `com.android.vending.splits.required` (base APK dari Android App Bundle). Akibatnya **base URL, kredensial, dan seluruh path API tidak dapat dibuktikan dari berkas ini**; perlu `split_config.arm64_v8a.apk` atau paket `.xapk`/`.apks` lengkap.

Nilai endpoint non-native tetap terekam terenkripsi di `res/values/strings.xml` (mis. `urlLogin`, `urlAktivasi2`, `urlRegistrasi2`, `urlGetVA`, `urlPayBank`, `urlCekSaldo`, `urlGetTokenId`, `server_key`), didekripsi saat runtime via `f4.d.k()` dengan sandi yang sama dari JNI.

---

## 5. VERIFIKASI TANDA TANGAN

- Skema: v1 ✓, v2 ✓, v3 ✓, v4 ✗ — status VALID.
- Signer: `CN=Android, OU=Android, O=Google Inc., L=Mountain View, ST=California, C=US`
  SHA-256 cert `b7df5b316c759019034d2541a311542d4d0354b39388c62b61e6aaf8bbce9477`
- Hash AGP stamp `3257d599a49d2c961a471ca9843f59d341a405884583fc087df4237b733bbd6d` ≠ hash sertifikat aktif
  → **berkas ditandatangani ulang pihak ketiga (re-signed / debug keystore)**
- Implikasi: tidak dapat dipastikan bahwa berkas ini bit-identik dengan distribusi resmi Play Store. Untuk kepentingan pembuktian, hash Play Store perlu diambil dari perangkat korban/saksi atau dari akun pengembang.

---

## 6. PENILAIAN INDIKATOR ANCAMAN (koreksi triage otomatis)

| Temuan triage 22 Sep | Hasil verifikasi statis di DEX |
|---|---|
| Label "CRITICAL / MALICIOUS (skor 130)" | **Tidak berdasar.** Tidak ada `RECEIVE_SMS`, `READ_SMS`, `SEND_SMS`, `BIND_ACCESSIBILITY_SERVICE`, `BIND_NOTIFICATION_LISTENER_SERVICE`, maupun `SYSTEM_ALERT_WINDOW` |
| `READ_CONTACTS` = spyware | Dipakai `dashboard.akun.ForwardSMS` untuk memilih kontak dan meneruskan pesan (bagikan bukti transaksi). Tidak ada pengiriman dump kontak ke server |
| `READ_PHONE_STATE` | Untuk uji kesiapan SIM (`getSimState`) dan turunan token perangkat+SIM pada proses aktivasi |
| `CAMERA` | Foto KTP dan selfie liveness (`GooglyEyesActivity`) pada `IsiFormulirBerkasActivity` |
| `CALL_PHONE` | Panggilan ke call center 08123000861 |
| Tidak ada `SmsManager` pada kode sendiri | Terkonfirmasi — aplikasi tidak mengirim SMS secara senyap |

Kesimpulan sementara: karakter berkas adalah **aplikasi operasional keuangan/koperasi (mobile BMT)**, bukan trojan pencuri OTP. Fokus pembuktian bergeser ke aspek regulasi dan operasional (keabsahan keanggotaan, penghimpunan dana, kepatuhan perizinan) — bukan ke ranah malware.

---

## 7. TINDAK LANJUT YANG DISARANKAN

1. **Ambil paket APK lengkap (XAPK/`.apks`)** untuk memperoleh `libnative-lib.so`, lalu baca `URL_BASE_ENC` dan kredensial via REA (`inspect_native_*`, `search_strings`). Tanpa ini endpoint server tidak terbukti.
2. **Uji kesesuaian berkas dengan distribusi resmi** — bandingkan SHA-256 dengan APK pada perangkat anggota koperasi atau akun pengembang di Play Store.
3. **Permintaan keterangan PT USID / PT UGT System Integrator** sebagai vendor core banking `usid-mobile-3` (log akses, konfigurasi `kodebmt 0123`, basis data anggota).
4. **Uji registrasi aktif** hanya dengan izin resmi: catat `kodeaktivasi`/`nokartu` yang diterbitkan CS dan bandingkan dengan basis data anggota (uji pembeli ganda / anggota fiktif).
5. **Intersepsi lalu lintas** memerlukan perangkat uji: CA store Dart tidak dipakai (aplikasi bukan Flutter, jadi mitmproxy/PCAPdroid dapat dipakai), tetapi koneksi ke Firebase RTDB `usid-mobile-3` tetap dapat diverifikasi.
6. Simpan register evidence (§2) sebagai lampiran BAP; kutip `evidence_id` saat merujuk hasil REA.

---

## 8. LAMPIRAN — ARTEFAK MENTAH

Direktori: `~/penyidikan/analisis/bakti-huria-2026/rea/`
`01-package.yaml`, `02-allclasses.yaml`, `02-classes-own.txt`, `10-class-01…09-*.yaml`, `20-xref-*.yaml`, `evidence-index.json`, `run_map.sh`
Hasil dekompilasi penuh (jadx, 22 Sep 2026): `~/anggotaku_decompiled/`
Laporan triage lama: `~/laporan_anggotaku.md`, `~/triage_anggotaku.json`

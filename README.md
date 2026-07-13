# Sistem Cerdas Prediksi & Rekomendasi Risiko Diabetes

Tugas UAS Data Mining — Sistem cerdas berbasis Machine Learning (Random Forest)
untuk memprediksi status diabetes pasien (Normal / Prediabetes / Diabetes)
dan memberikan rekomendasi kesehatan personal, berjalan di localhost.

## 1. Dataset

- Sumber: Mendeley Data — *Dataset of Diabetes*
- 1000 baris data pasien, 14 kolom: `ID, No_Pation, Gender, AGE, Urea, Cr,
  HbA1c, Chol, TG, HDL, LDL, VLDL, BMI, CLASS`
- Target (`CLASS`): `N` = Normal, `P` = Prediabetes, `Y` = Diabetes
- File dataset ada di `data/diabetes.csv`

## 2. Model

- Algoritma: **Random Forest** (`sklearn.ensemble.RandomForestClassifier`, n_estimators=150)
- Preprocessing: encoding gender (M=1/F=0), `StandardScaler` untuk fitur numerik,
  `LabelEncoder` untuk target
- Akurasi pada data uji (20%): **99.5%**
- Model, scaler, dan label encoder disimpan di folder `model/` (`.pkl`, via `joblib`)

Untuk melatih ulang model (opsional, model hasil training sudah disertakan):
```bash
python train_model.py
```

## 3. Arsitektur Sistem

Aplikasi dibangun **full Python (Flask)** — dipilih karena ini opsi paling
mudah untuk dijalankan di localhost (tidak perlu setup XAMPP/Apache/PHP
terpisah, cukup satu perintah `python app.py` dan langsung bisa diakses
di browser).

```
diabetes-recsys/
├── app.py                 # Aplikasi Flask utama (routing, load model, prediksi)
├── train_model.py         # Script training model Random Forest
├── recommendation.py      # Modul rule-based rekomendasi kesehatan
├── database.py            # Modul database SQLite (simpan & ambil riwayat)
├── requirements.txt
├── data/
│   ├── diabetes.csv       # Dataset Mendeley
│   └── history.db         # Database riwayat prediksi (dibuat otomatis)
├── model/
│   ├── random_forest_model.pkl
│   ├── scaler.pkl
│   └── label_encoder.pkl
├── templates/
│   ├── index.html         # Form input data pasien
│   ├── result.html        # Halaman hasil prediksi + rekomendasi
│   └── history.html       # Halaman riwayat prediksi
└── static/
    └── style.css
```

Alur sistem:
1. User mengisi form data klinis pasien di halaman utama (`/`)
2. Flask menerima input di route `/predict`, melakukan scaling, lalu
   memprediksi kelas menggunakan model Random Forest
3. Modul `recommendation.py` menghasilkan rekomendasi personal berdasarkan
   kelas prediksi + nilai klinis individu (HbA1c, BMI, Chol, TG, HDL, LDL, usia)
4. Setiap hasil prediksi otomatis disimpan ke **database SQLite**
   (`data/history.db`) lewat modul `database.py`
5. Hasil (kelas, probabilitas tiap kelas, rekomendasi) ditampilkan di halaman hasil
6. Riwayat seluruh prediksi bisa dilihat di halaman `/history`, lengkap
   dengan opsi hapus riwayat

**Kenapa SQLite (bukan MySQL/XAMPP)?** SQLite sudah built-in di Python
(modul `sqlite3`), datanya tersimpan dalam satu file lokal tanpa perlu
instalasi/setup server database terpisah — paling praktis untuk aplikasi
skala tugas seperti ini, sambil tetap memenuhi requirement "ada database".

## 4. Cara Menjalankan di Localhost

**Prasyarat:** Python 3.9+ sudah terinstal.

```bash
# 1. Masuk ke folder project
cd diabetes-recsys

# 2. (Opsional tapi disarankan) buat virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
python app.py
```

Lalu buka browser ke: **http://127.0.0.1:5000**

> Model sudah pre-trained (ada di folder `model/`), jadi tidak perlu jalankan
> `train_model.py` lagi kecuali ingin melatih ulang.

### Jika wajib pakai XAMPP

XAMPP dirancang untuk PHP, bukan Python, jadi cara paling umum dipakai
mahasiswa adalah: jalankan Flask seperti di atas (tetap "localhost"), lalu
kalau dosen mensyaratkan tampilan di folder `htdocs` XAMPP, buat file PHP
sederhana di `htdocs` yang me-redirect/embed (iframe) ke `http://127.0.0.1:5000`.
Beri tahu saya kalau opsi ini yang diperlukan, saya bisa siapkan filenya.

## 5. Submit ke GitHub & Invite Kolaborator

Karena saya tidak punya akses ke akun GitHub kamu, langkah ini perlu
dilakukan manual dari sisi kamu:

```bash
cd diabetes-recsys
git init
git add .
git commit -m "Sistem cerdas prediksi & rekomendasi risiko diabetes (Random Forest)"
git branch -M main
git remote add origin <URL_REPO_GITHUB_KAMU>
git push -u origin main
```

Untuk invite "Pak Ilham" sebagai kolaborator:
1. Buka repo di GitHub → tab **Settings**
2. Klik **Collaborators** (di sidebar kiri)
3. Klik **Add people**, masukkan username/email GitHub Pak Ilham
4. Kirim undangan

## 6. Catatan

Sistem ini adalah proyek akademik untuk mata kuliah Data Mining dan **bukan**
alat diagnosis medis resmi. Ambang batas pada modul rekomendasi mengacu pada
rentang umum, bukan pengganti konsultasi dengan tenaga medis profesional.

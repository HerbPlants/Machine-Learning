# 🌿 HerbPlants – Machine Learning Project

Proyek ini merupakan bagian dari **Capstone Project** yang terdiri dari dua komponen utama:

1. **Scraping dan ETL** – Mengumpulkan data deskriptif tanaman herbal dari website.
2. **Build Model** – Membangun model klasifikasi gambar tanaman herbal berbasis Machine Learning menggunakan arsitektur MobileNetV2.
3. **Machine Learning Deployment** - Mengimplementasikan model ke dalam aplikasi web berbasis Flask. Aplikasi ini menyediakan API untuk menerima input gambar dan mengembalikan hasil klasifikasi, serta dapat dijalankan secara lokal atau menggunakan Docker agar siap di-deploy ke berbagai environment seperti server atau cloud (AWS).
   
---

## 🗂 Struktur Direktori

```
Machine-Learning-main/
├── build_model/
│   ├── indexplant/
│   │   └── class_indices.json 
│   ├── models/
│   │   ├── h5_model/              # model.h5 untuk backend (Flask)
│   │   └── tfjs_model/            # model TensorFlow.js (frontend)
│   │       ├── model.json
│   │       └── group1-shard*.bin
│   ├── notebook/
│   │   ├── HerbPlants_CC25_CF155.ipynb
│   │   └── herbplants_cc25_cf155.py
│   ├── README.md 
│   └── requirements.txt 
├── dataset/
│   └── Dataset HerbPlants.txt 
├── scraping/
│   ├── extract.py, transform.py, load.py, main.py 
│   ├── hasil_scraping.xlsx, link_sisa_5.xlsx
│   ├── requirements.txt 
│   └── README_ETL.md 
├── machine learning deploy/
│   ├── app.py
│   ├── model.h5
│   ├── class_indices.json
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── result-scrapping.json
│   └── .dockerignore
└── README.md  
```

---

## 1️⃣ Scraping & ETL

📁 `scraping/`

Berisi skrip Python untuk mengumpulkan dan membersihkan data deskriptif mengenai tanaman herbal lokal Indonesia.

* `extract.py` – Mengambil data dari situs sumber (via `requests` & `BeautifulSoup`).
* `transform.py` – Membersihkan dan menyusun ulang data mentah.
* `load.py` – Menyimpan hasil ke file Excel.
* `main.py` – Pipeline ETL terintegrasi.
* `hasil_scraping.xlsx` – Output akhir data deskriptif.
* `README_ETL.md` – Dokumentasi scraping.

> **Dependencies**: `requests`, `pandas`, `openpyxl`, `BeautifulSoup4`

---

## 2️⃣ Build Model (Training & Konversi)

📁 `build_model/`

Berisi proses pelatihan model klasifikasi gambar tanaman herbal menggunakan transfer learning (MobileNetV2).

* `HerbPlants_CC25_CF155.ipynb` – Notebook pelatihan dan konversi model.
* `model.h5` – Model hasil training (Keras).
* `model.json`, `.bin` – Model versi TensorFlow\.js.
* `class_indices.json` – Mapping label kelas.
* `requirements.txt` – Dependensi ML.
* `README.md` – Dokumentasi pelatihan.

> **Dependencies**: `tensorflow`, `keras`, `matplotlib`, `tensorflowjs`

---
Tentu! Ini versi **Deployment**-nya yang sudah disusun dengan format dan gaya yang konsisten dengan bagian Build Model yang kamu kasih:

---

## 🚀 Deployment

📁 `machine learning deploy/`

Berisi berkas-berkas deployment aplikasi klasifikasi gambar berbasis Flask yang memuat model, API prediksi, serta konfigurasi Docker.

* `app.py` – Script utama aplikasi Flask untuk menerima input gambar dan menghasilkan prediksi tanaman.
* `model.h5` – Model klasifikasi tanaman herbal dalam format Keras (hasil training).
* `class_indices.json` – Mapping indeks ke nama kelas tanaman untuk kebutuhan interpretasi output.
* `result-scrapping.json` – Data deskriptif hasil scraping yang dapat digunakan untuk mendukung tampilan atau penjelasan hasil prediksi.
* `requirements.txt` – Daftar dependensi Python untuk menjalankan server Flask dan memuat model.
* `Dockerfile` – Instruksi pembuatan image Docker untuk menjalankan aplikasi dalam container.
* `.dockerignore` – Daftar file/folder yang dikecualikan saat proses build image Docker.

> **Dependencies**: `Flask`, `TensorFlow`, `Pillow`, `NumPy`, `Gunicorn`

## 📦 Dataset

📁 `dataset/`
Berisi dataset deskriptif tanaman herbal yang digunakan untuk training & klasifikasi.

* `Dataset HerbPlants.txt` – Berisi link github dataset tanaman yang digunakan untuk training model.File dilampirkan dalam format `.txt` karena size nya melebihi batas kapasitas.

---








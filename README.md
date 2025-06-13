# 🌿 HerbPlants – Machine Learning 

Proyek ini merupakan bagian dari Capstone Project yang terdiri dari dua komponen utama:

1. **Scraping dan ETL** – Mengumpulkan data deskriptif tanaman herbal dari website.
2. **Build Model** – Membangun model klasifikasi gambar tanaman herbal berbasis machine learning menggunakan MobileNetV2.

---

## 🗂 Struktur Proyek

```
Machine-Learning-main/
├── build_model/
│   ├── indexplant/
│   │   └── class_indices.json 
│   ├── models/
│   │   ├── h5_model/ ➝ model.h5
│   │   └── tfjs_model/ ➝ model.json, group1-shard1of3.bin, ...
│   ├── notebook/ ➝ HerbPlants_CC25_CF155.ipynb, .py file
│   ├── README.md 
│   └── requirements.txt 
├── dataset/
│   └── Dataset HerbPlants.txt 
├── scraping/
│   ├── README_ETL.md 
│   ├── extract.py, transform.py, load.py, main.py 
│   ├── hasil_scraping.xlsx, link sisa 5.xlsx
│   └── requirements.txt 
└── README.md  
```

---

## 1️⃣ Scraping & ETL

📁 `scraping/`

Berisi serangkaian script Python untuk mengumpulkan dan membersihkan data tekstual mengenai tanaman herbal lokal Indonesia.

- `extract.py` – Mengambil data dari situs sumber menggunakan requests dan BeautifulSoup.
- `transform.py` – Membersihkan dan menyusun ulang data.
- `load.py` – Menyimpan hasil akhir ke dalam Excel.
- `main.py` – Pipeline ETL utama.
- `hasil_scraping.xlsx` – Output akhir deskriptif tanaman herbal.
- `README_ETL.md` – Dokumentasi khusus bagian scraping.

> Tools: `requests`, `pandas`, `openpyxl`, `BeautifulSoup4`

---

## 2️⃣ Build Model (Training & Konversi)

📁 `build_model/`

Membangun model klasifikasi gambar tanaman herbal berdasarkan dataset internal menggunakan transfer learning (MobileNetV2).

- `HerbPlants_CC25_CF155.ipynb` – Notebook pelatihan model CNN dan konversi ke TensorFlow.js
- `model.h5` – Model Keras hasil training
- `model.json` + `.bin` files – Hasil konversi untuk TensorFlow.js (frontend-ready)
- `class_indices.json` – Mapping label untuk frontend
- `requirements.txt` – Dependensi ML
- `README.md` – Dokumentasi khusus bagian ini

> Tools: `tensorflow`, `keras`, `matplotlib`, `tensorflowjs`


---

## 📦 Dataset

📁 `dataset/`  
Berisi dataset yang digunakan untuk melakukan training model.

---




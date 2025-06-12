# HerbPlants Machine Learning Repository - Build Model

Repositori ini berisi dataset, skrip, dan model deep learning yang dikembangkan untuk proyek **HerbPlants**, yaitu sistem klasifikasi tanaman herbal. Proyek ini menerapkan teknik computer vision dan deep learning untuk mengklasifikasikan berbagai tanaman herbal Indonesia menggunakan data citra.

Proyek **HerbPlants** bertujuan untuk mendukung edukasi, penelitian, dan pemanfaatan tanaman herbal dengan menyediakan alat yang andal untuk mengidentifikasi tanaman herbal melalui klasifikasi berbasis gambar.

## **Gambaran Umum**

Model ini mampu mengenali 100 spesies tanaman obat Indonesia berdasarkan gambar yang diunggah oleh pengguna. Model dibangun menggunakan MobileNetV2 sebagai feature extractor yang telah di-*fine-tune* dan dilatih menggunakan *Indonesia Medical Plant Dataset*. Dataset ini telah divalidasi oleh ahli taksonomi tumbuhan untuk menjamin keaslian dan kualitas data.

Tujuan utama proyek ini adalah menjadikan identifikasi tanaman herbal lebih mudah diakses dan berskala, terutama bagi peneliti, mahasiswa, dan masyarakat umum yang tertarik pada kekayaan biodiversitas Indonesia.

## **Perangkat dan Kerangka Kerja**

Proyek **HerbPlants** memanfaatkan berbagai perangkat, pustaka, dan kerangka kerja untuk mendukung pengembangan, pelatihan, dan penerapan model klasifikasi tanaman obat. Teknologi-teknologi berikut digunakan dalam proyek ini:

- *Programming Language* : Python

- *Deep Learning Frameworks* : TensorFlow dan Keras

- *Pre-trained Model* : MobileNetV2

- *Libraries* : NumPy, Pandas, Matplotlib, Scikit-learn, dan PIL

- *Data Augmentation* : ImageDataGenerator

- *Development Platforms* : Google Colab dan Google Drive

- *Model Optimization* : Keras Callbacks (ModelCheckpoint, EarlyStopping, dan ReduceLROnPlateau)

- *Model Optimization* : TensorFlow\.js

## **Dataset**

Dataset yang digunakan dalam proyek ini adalah [**Indonesia Medical Plant Dataset**](https://drive.google.com/file/d/1pybPSWmiql6XEhSgdwQsTG_409iQbOw9/view), yaitu kumpulan gambar tanaman obat Indonesia yang telah dikurasi. Dataset ini terdiri dari **100 kelas** yang merepresentasikan spesies tanaman obat Indonesia yang berbeda, dengan total **10.000 gambar** yang digunakan dalam proyek ini. Setiap gambar telah diberi label sesuai spesies tanaman dan melalui proses seleksi untuk menjamin konsistensi serta relevansi dalam tugas klasifikasi.

## **Pra-pemrosesan**

Tahap pra-pemrosesan dalam proyek **HerbPlants** memastikan bahwa data gambar masukan telah dipersiapkan dengan baik untuk melatih model klasifikasi yang andal. Berikut adalah langkah-langkah utama yang diterapkan:

1. **Ubah Ukuran Gambar**  
   Semua gambar masukan diubah ukurannya menjadi dimensi seragam `224x224` piksel untuk menstandarkan bentuk input bagi model deep learning dan mengoptimalkan kinerja pelatihan.

2. **Pembagian Data**  
   Dataset dikocok secara acak dan dibagi menjadi tiga subset dengan rasio sebagai berikut.

   - **Data Latih (80%)** : 8.000 gambar
   - **Data Validasi (10%)** : 1.000 gambar
   - **Data Uji (10%)** : 1.000 gambar

   Pembagian ini memastikan jumlah data yang cukup untuk proses pembelajaran model, sekaligus mempertahankan proporsi yang seimbang untuk evaluasi kinerja.

3. **Normalisasi**  
   Semua nilai piksel dinormalisasi ke dalam rentang \[0, 1] dengan cara membagi nilai piksel dengan 255 menggunakan `ImageDataGenerator`.

4. **Konfigurasi Data Generator**  
   `ImageDataGenerator` dikonfigurasi untuk membaca gambar langsung dari dataframe beserta label yang sesuai, lalu mengubahnya menjadi batch berukuran 32 untuk pelatihan yang efisien.

5. **Augmentasi Data**  
   Untuk meningkatkan kemampuan generalisasi model dan mengurangi overfitting, teknik augmentasi dasar seperti zoom acak dan flipping acak (horizontal dan vertikal) diterapkan selama pelatihan.

## **Arsitektur Model**

Model yang digunakan dalam proyek ini merupakan *Convolutional Neural Network (CNN)* berbasis *transfer learning* dengan arsitektur **MobileNetV2**, sebuah model ringan dan efisien yang telah dilatih sebelumnya (*pre-trained*) pada dataset ImageNet. Pendekatan ini memungkinkan model untuk memanfaatkan fitur-fitur yang telah dipelajari dari dataset berskala besar dan mengadaptasinya untuk tugas klasifikasi tanaman obat Indonesia.

### **Rincian Arsitektur**

1. **Lapisan Input**  
   Menerima gambar RGB berukuran `(224 × 224 × 3)`.

2. **Lapisan Pra-pemrosesan**  
   Pipeline augmentasi data yang menggunakan `RandomZoom(0.1)` dan `RandomFlip('horizontal_and_vertical')`.

3. **MobileNetV2**  
   Model menggunakan `MobileNetV2`, CNN ringan yang telah dilatih pada ImageNet, sebagai *feature extractor*. Model ini membantu mengenali pola visual seperti tepi dan tekstur pada gambar tanaman obat.

   * Lapisan klasifikasi atas dihapus.
   * *Global Average Pooling* digunakan untuk merangkum fitur menjadi vektor 1 dimensi.
   * Hanya lapisan akhir (mulai dari `block_16_expand`) yang dapat dilatih, sedangkan lapisan sebelumnya dibekukan untuk mempertahankan pengetahuan awal yang telah dipelajari.

4. **Klasifikasi**

   * `Dense(256)` dengan aktivasi ReLU untuk mempelajari pola baru yang spesifik pada tanaman obat.
   * `Dropout(0.3)` untuk mencegah *overfitting*.
   * `Dense(100)` dengan aktivasi Softmax, untuk mengklasifikasikan gambar ke salah satu dari 100 kategori tanaman.

### **Ringkasan Model**

| Komponen               | Deskripsi                                     |
| ---------------------- | --------------------------------------------- |
| Model Dasar            | MobileNetV2 (pre-trained, sebagian dibekukan) |
| Lapisan Tambahan       | Dense(256) + Dropout(0.3) + Dense(100)        |
| Fungsi Aktivasi        | ReLU (lapisan tersembunyi), Softmax (output)  |
| Total Parameter        | **2.257.984**                                 |
| Parameter yang Dilatih | **886.080**                                   |
| Parameter Beku         | **1.371.904**                                 |

Arsitektur ini dioptimalkan untuk efisiensi dan akurasi, dengan menggabungkan fitur-fitur dalam dari model pra-latih dengan lapisan pembelajaran spesifik. Model ini sangat cocok untuk diterapkan pada platform web dan mobile karena bobot model yang ringan.

## **Proses Pelatihan**

Model dikompilasi menggunakan **Adam optimizer** dengan *learning rate* sebesar 0.0001, yang sesuai untuk melakukan *fine-tuning* pada model yang telah dilatih sebelumnya. Fungsi loss yang digunakan adalah **categorical crossentropy**, yang tepat untuk tugas klasifikasi multi-kelas dengan 100 kategori tanaman. **Akurasi** digunakan sebagai metrik evaluasi.

Untuk memastikan performa terbaik, *callback* berikut diterapkan:

* **ModelCheckpoint** : Menyimpan model terbaik berdasarkan *validation loss*.

* **EarlyStopping** : Menghentikan pelatihan jika *validation accuracy* tidak meningkat selama 5 epoch berturut-turut dan mengembalikan bobot terbaik.

* **ReduceLROnPlateau**: Menurunkan *learning rate* jika *validation loss* tidak menunjukkan penurunan (mengalami stagnasi).

Konfigurasi ini membantu mencegah *overfitting* dan mempercepat proses konvergensi selama pelatihan.

## **Evaluasi dan Hasil**

Untuk mengevaluasi perilaku pembelajaran dan performa akhir model, akurasi pelatihan dan validasi dipantau sepanjang setiap *epoch*, diikuti dengan evaluasi pada *test set* terpisah.

![alt text](image-1.png)

Akurasi pelatihan menunjukkan peningkatan yang stabil dan hampir mencapai 100% pada *epoch* terakhir. Sementara itu, akurasi validasi meningkat signifikan pada tahap awal pelatihan dan secara bertahap stabil di sekitar 88%, yang mengindikasikan proses pembelajaran yang efektif dan generalisasi yang baik. Perbedaan kecil antara kedua kurva menunjukkan adanya *overfitting* ringan, yang telah diminimalkan melalui penggunaan *dropout* dan *early stopping*.

Setelah pelatihan selesai, model dievaluasi menggunakan *test set* yang tidak digunakan selama proses pelatihan maupun validasi. Hasil akhir evaluasi sebagai berikut:

* **Akurasi Uji (Test Accuracy)** : 87,00%

* **Loss Uji (Test Loss)** : 0,5424

Hasil ini menunjukkan bahwa model memiliki kinerja yang andal dalam mengklasifikasikan 100 kategori tanaman obat Indonesia, dengan tingkat akurasi tinggi dan kemampuan generalisasi yang stabil.

## **Ekspor dan Deployment**

Setelah proses pelatihan selesai, model diekspor dan dikonversi untuk memungkinkan *deployment* di berbagai platform, baik web maupun mobile. Adapun tahapan yang dilakukan adalah sebagai berikut:

* **Format Model**:

  * **Format H5**
    Model disimpan dalam format `.h5` menggunakan Keras, sehingga mudah dimuat kembali, dibagikan, dan digunakan ulang di masa mendatang.

  * **Format TensorFlow\.js**  
    Model `.h5` kemudian dikonversi ke format **TensorFlow\.js** agar dapat digunakan langsung di browser web dan aplikasi berbasis JavaScript.

* **Konversi Model**  
  Proses konversi dilakukan menggunakan perintah `tensorflowjs_converter`, yang mengubah model Keras menjadi format yang kompatibel dengan TensorFlow\.js.

* **Deployment**  
  Model yang telah dikonversi ke TensorFlow\.js disiapkan untuk **deployment berbasis web**, memungkinkan prediksi secara real-time langsung di browser tanpa memerlukan pemrosesan dari sisi server (*serverless*).

* **File Model**:

  * **[model.h5]**: Model terlatih dalam format Keras `.h5`.

  * **[Model TensorFlow.js]**: Model yang telah dikonversi untuk digunakan dalam lingkungan TensorFlow\.js.

Proses ekspor dan konversi ini memastikan bahwa model klasifikasi tanaman obat dapat diakses secara lintas platform dengan performa optimal dan kemudahan penggunaan, khususnya bagi pengguna yang mengakses melalui browser atau aplikasi web mobile.

## **Struktur Direktori**

```
build_model/
├── indexplant/
│   └── class_indices.json     # Pemetaan indeks ke nama kelas
├── models/
│   ├── h5_model                    # Folder model hasil pelatihan
│   └── tfjs_model
├── notebook/
│   ├── HerbPlants_CC25_CF155.ipynb  # Notebook Jupyter utama
│   └── herbplants_cc25_cf155.py     # Versi script Python dari notebook
├── requirements.txt          # Daftar dependensi Python
```

Struktur direktori ini dirancang agar modular dan mudah digunakan, baik untuk keperluan pelatihan ulang, evaluasi, maupun deployment model klasifikasi tanaman obat.

### **Catatan Penggunaan**

Untuk menjalankan proyek ini secara lokal, pastikan kamu telah menginstal semua dependensi yang tercantum dalam file `requirements.txt`. Berikut langkah-langkah umum penggunaannya:

1. **Instalasi Dependensi**  
   Gunakan perintah berikut di terminal:

   ```bash
   pip install -r requirements.txt
   ```

2. **Menjalankan Notebook**  
   Buka file Jupyter Notebook `HerbPlants_CC25_CF155.ipynb` yang ada di folder `notebook` untuk menjalankan proses pelatihan model atau mempelajari alur kerja proyek ini.

3. **Menjalankan via Script Python**  
   Alternatifnya, kamu juga dapat menjalankan skrip Python `herbplants_cc25_cf155.py` untuk melakukan pelatihan model melalui CLI.

4. **File Indeks Kelas**  
   File `class_indices.json` yang terdapat di folder `indexplant` menyimpan informasi pemetaan antara label kelas dan indeks numeriknya. File ini penting dalam proses inferensi (*inference*).

5. **Model Terlatih**  
   Folder `models/sv` menyimpan hasil model terlatih yang bisa digunakan untuk prediksi lebih lanjut atau proses deployment.

# HerbPlants ETL Pipeline

Repositori ini berisi skrip dan alur pemrosesan yang dikembangkan untuk modul **HerbPlants ETL**, yaitu sistem Extract–Transform–Load (ETL) yang berfungsi untuk memberikan informasi dari tanaman herbal hasil klasifikasi. Komponen ETL ini menjalankan proses otomatis mulai dari pengambilan data melalui *web scraping*, pembersihan data, hingga ekspor data terstruktur. Tujuannya adalah untuk mengumpulkan informasi penting mengenai botani, seperti distribusi, nama lokal, kondisi ekologi, serta pemanfaatannya secara tradisional dari berbagai tanaman herbal Indonesia.

Proses ETL ini mendukung model klasifikasi deep learning dengan menyediakan informasi kontekstual sehingga sistem **HerbPlants** menjadi lebih informatif, praktis, dan mudah digunakan oleh peneliti, mahasiswa, maupun masyarakat umum yang tertarik pada keanekaragaman hayati tanaman herbal di Indonesia.

## **Gambaran Umum**

*ETL Pipeline* ini dirancang untuk mendukung sistem klasifikasi tanaman herbal dengan cara mengambil, memodifikasi, dan menyimpan informasi tanaman herbal secara terstruktur dari sumber yang terpercaya. Setelah suatu tanaman herbal berhasil diidentifikasi melalui model klasifikasi, proses ETL ini akan secara otomatis memperkaya hasil prediksi dengan informasi botani, seperti nama lokal, persebaran geografis, kebutuhan ekologis, dan kegunaan dalam pengobatan tradisional.

Informasi tersebut diambil secara langsung dari **Website Konservasi Socfindo** yang diubah ke dalam bentuk data tabular terstruktur, lalu dimuat ke dalam file Excel yang telah diformat. Hal ini mempermudah proses peninjauan, verifikasi, serta integrasi data ke dalam aplikasi lanjutan maupun antarmuka pengguna.

Pendekatan ini menjembatani kesenjangan antara pengenalan berbasis citra dengan pemahaman kontekstual mengenai tanaman herbal sehingga memberikan nilai tambah bagi peneliti, pendidik, pengembang, maupun pemerhati keanekaragaman hayati.

## **Perangkat yang Digunakan**

*ETL Pipeline* dalam proyek **HerbPlants** dirancang untuk mengumpulkan serta menyusun informasi tanaman herbal dari sumber daring. Proses ETL ini melengkapi model klasifikasi dengan memberikan deskripsi mendetail dari setiap tanaman yang berhasil diidentifikasi. Adapun perangkat dan pustaka yang digunakan dalam pengembangan sistem ini adalah sebagai berikut:

* *Programming Language* : Python
* *Data Processing* : pandas dan openpyxl
* *Web Scraping* : requests dan BeautifulSoup
* *Custom Extraction* : extract_plant_data

## **Sumber Data**

Sumber informasi utama yang digunakan dalam proyek ini adalah [**Website Konservasi Socfindo**](https://www.socfindoconservation.co.id/plant/), yaitu sebuah basis pengetahuan digital yang mendokumentasikan keanekaragaman hayati tanaman, khususnya tanaman herbal dan konservasi di Indonesia. Platform ini menyediakan profil tanaman secara terstruktur dan mendetail, termasuk informasi penting yang bersifat etnobotanis.

Setiap profil tanaman di dalam situs tersebut terdiri dari beberapa bagian standar, antara lain:

- **Penyebaran Tanaman** (Distribusi Geografis)
- **Nama Lokal** (Nama-nama yang digunakan di berbagai daerah)
- **Agroekologi** (Kondisi ekologis dan lingkungan tumbuh)
- **Khasiat** (Manfaat dalam pengobatan tradisional)

Bagian-bagian ini secara khusus menjadi target dalam proses *web scraping* yang dilakukan pada tahap **Extract** dan **Transform** dalam *ETL pipeline* ini. Struktur halaman yang konsisten dan terstandarisasi memungkinkan ekstraksi data dilakukan secara sistematis. Informasi yang berhasil dikumpulkan kemudian dicocokkan dengan nama tanaman hasil prediksi dari model klasifikasi sehingga sistem dapat menampilkan informasi tanaman herbal secara dinamis kepada pengguna akhir.

## **Extract: Pengambilan Informasi melalui Web Scraping**

Tahap ini berfokus pada pengambilan informasi terkait tanaman herbal Indonesia dari sumber daring yang terstruktur. Setelah nama tanaman berhasil diidentifikasi oleh model klasifikasi, proses *extract* ini akan mengambil informasi detail seperti nama lokal, manfaat, distribusi geografis, serta konteks agroekologi dari tanaman tersebut.

### **Gambaran Skrip**

Skrip `extract.py` berfungsi untuk mengumpulkan informasi tanaman herbal dari sumber daring melalui proses *web scraping*. Tahapan ini menjadi krusial setelah model klasifikasi citra mengidentifikasi spesies tanaman, sehingga aplikasi dapat menampilkan pengetahuan tanaman herbal yang sesuai kepada pengguna.

Terdapat tiga fungsi utama dalam skrip ini:

1. **extract_links(file_path)**  
   Fungsi ini digunakan untuk memuat file Excel yang umumnya berisi daftar tautan (URL) halaman profil tanaman. File akan dibaca ke dalam format DataFrame menggunakan pustaka Pandas, sehingga memudahkan akses ke seluruh tautan tanaman.

```python
def extract_links(file_path):
    df = pd.read_excel(file_path)
    return df
```

2. **clean_text(text)**  
   Konten web seringkali mengandung karakter khusus atau simbol yang tidak sesuai untuk diekspor ke Excel atau dimasukkan ke dalam basis data. Fungsi ini akan menghapus semua karakter yang tidak dapat dicetak (*non-printable*) agar teks menjadi bersih dan siap diproses lebih lanjut.

```python
def clean_text(text):
    return ''.join(c for c in text if c.isprintable())
```

3. **extract_plant_data(link)**  
   Merupakan fungsi utama yang menjalankan proses *web scraping*. Fungsi ini menggunakan pustaka `requests` dan `BeautifulSoup` untuk mengekstraksi bagian-bagian tertentu dari halaman web, dengan mencari elemen `<h2>` dan mengambil isi dari elemen-elemen setelahnya. Bagian-bagian yang menjadi target pengambilan data meliputi:

    - **Penyebaran Tanaman** (Distribusi Geografis)
    - **Nama Lokal** (Nama-nama daerah)
    - **Agroekologi** (Kondisi ekologi tanaman)
    - **Khasiat** (Manfaat pengobatan tradisional)

```python
def extract_plant_data(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        h2_elements = soup.find_all('h2')
        data = {
            'Penyebaran Tanaman': '',
            'Nama Lokal': '',
            'Agroekologi': '',
            'Khasiat': ''
        }

        for h2 in h2_elements:
            title = h2.get_text(strip=True)
            content = ''
            for sibling in h2.find_next_siblings():
                if sibling.name == 'h2':
                    break
                content += sibling.get_text(strip=True) + ' '
            content = clean_text(content.strip())

            if title in data:
                data[title] = content

        return data
    except Exception as e:
        print(f"Error processing {link}: {e}")
        return None
```

## **Transform: Menyusun dan Memperkaya Data Tanaman**

Tahap ini berfokus pada penataan ulang data mentah hasil ekstraksi menjadi format yang bersih dan seragam. Setelah melakukan *scraping* informasi tanaman dari situs web, proses *transform* memastikan bahwa detail tanaman diselaraskan secara tepat dengan nama dan sumbernya, serta menangani kemungkinan kesalahan atau kekurangan data secara sistematis.

### **Gambaran Skrip**

Skrip `transform.py` bertugas untuk memproses daftar tanaman herbal beserta tautan informasinya. Skrip ini memanggil fungsi ekstraksi untuk setiap tanaman, lalu menggabungkan hasilnya dengan nama umum dan nama Latin tanaman dalam format yang terstruktur.

1. **transform_data(df)**  
   Fungsi ini melakukan iterasi untuk setiap baris dalam DataFrame input berupa file Excel kemudian mengekstrak informasi detail dari setiap tanaman dan membentuk daftar baru yang berisi data informasi seputar tanaman.

```python
def transform_data(df):
    records = []
    for index, row in df.iterrows():
        nama_tanaman = row.get('Nama Tanaman', '')
        nama_latin = row.get('Nama Latin', '')
        link = row.get('Link', '')

        if pd.isna(link) or not link.strip():
            print(f"{nama_tanaman or '[Tanpa Nama]'}... dilewati (tidak ada link)")
            records.append({
                'Nama Tanaman': nama_tanaman,
                'Nama Latin': nama_latin,
                'Link': '',
                'Penyebaran Tanaman': '',
                'Nama Lokal': '',
                'Agroekologi': '',
                'Khasiat': ''
            })
            continue

        print(f"Memproses: {nama_tanaman}...")
        extracted = extract_plant_data(link)
        if extracted:
            extracted['Nama Tanaman'] = nama_tanaman
            extracted['Nama Latin'] = nama_latin
            extracted['Link'] = link
            records.append(extracted)
            print(f"{nama_tanaman}... done")
        else:
            print(f"{nama_tanaman}... gagal")
            records.append({
                'Nama Tanaman': nama_tanaman,
                'Nama Latin': nama_latin,
                'Link': link,
                'Penyebaran Tanaman': '',
                'Nama Lokal': '',
                'Agroekologi': '',
                'Khasiat': ''
            })
    return pd.DataFrame(records)
```

### **Logika Transformasi**

- Untuk setiap baris dalam input, fungsi akan memeriksa apakah terdapat tautan yang valid.
- Jika tautan tidak tersedia atau kosong, nama tanaman akan tetap dimasukkan namun detail lainnya dikosongkan.
- Jika tautan valid, data akan diambil dan diekstraksi menggunakan `extract_plant_data()`.
- Jika proses *scraping* gagal (misalnya karena *timeout* atau perubahan struktur halaman), fungsi tetap melanjutkan dan mencatat data kosong dengan informasi minimal.
- Hasil akhirnya adalah dataset yang terstruktur dengan baik dan telah diperkaya, siap untuk dimuat ke dalam file Excel atau basis data.

## **Load: Menyimpan Data ke File Excel**

Tahap ini bertanggung jawab untuk menyimpan data terstruktur akhir yang mencakup nama-nama tanaman dari input serta informasi hasil *scraping* ke dalam file Excel. Tujuan dari tahap ini adalah menghasilkan *output* yang mudah dibaca dan dapat digunakan kembali dalam sistem antarmuka visual.

### **Gambaran Skrip**

Fungsi `load_to_excel` menangani proses ekspor data tanaman yang telah ditransformasi ke dalam file Excel menggunakan `pandas` dan `openpyxl`. Proses ini memisahkan kolom-kolom input dan kolom hasil *scraping* (data terstruktur) kemudian menggabungkannya secara rapi dalam Excel. Skrip ini terdiri dari tiga langkah utama:

1. **Memisahkan Kolom**
   Skrip memisahkan kolom-kolom menjadi dua bagian:

   - **Input** : Nama Tanaman, Nama Latin, Link
   - **Output** : Penyebaran Tanaman, Nama Lokal, Agroekologi, Khasiat

```python
cols_input = ['Nama Tanaman', 'Nama Latin', 'Link']
cols_output = ['Penyebaran Tanaman', 'Nama Lokal', 'Agroekologi', 'Khasiat']

df_input = df[cols_input]
df_output = df[cols_output]
```

2. **Menyimpan Kolom Input ke File Excel**  
   Pertama-tama, skrip memeriksa apakah file Excel sebelumnya sudah ada. Apabila ditemukan file tersebut maka akan dihapus terlebih dahulu untuk menghindari masalah perizinan. Setelah itu, kolom input ditulis ke file Excel baru.

```python
df_input.to_excel(output_path, index=False)
```

3. **Menambahkan Kolom Output Hasil Scraping**  
   Setelah data input ditulis, skrip menggunakan `openpyxl` untuk membuka kembali file tersebut dan menambahkan kolom hasil *scraping* dimulai dari kolom D (kolom ke-4) sehingga data input dan hasil berada berdampingan.

```python
for row_idx, row in enumerate(dataframe_to_rows(df_output, index=False, header=True), start=1):
    for col_idx, value in enumerate(row, start=4):
        ws.cell(row=row_idx, column=col_idx, value=value)

wb.save(output_path)
```

### **Penanganan Error**

Jika file Excel sedang dibuka saat skrip dijalankan, maka akan muncul `PermissionError`. Dalam kasus ini, skrip akan mencetak pesan untuk mengingatkan pengguna agar menutup file terlebih dahulu.

```python
except PermissionError:
    print(f"Gagal menyimpan {output_path}: file sedang terbuka.")
```

## **Main: Menjalankan Proses ETL**

Tahap ini berperan sebagai pengendali utama yang menjalankan seluruh proses ETL (*Extract, Transform, Load*) secara berurutan. Skrip ini mengelola alur mulai dari membaca input berupa tautan, melakukan *scraping* dan transformasi data, hingga menyimpan hasil akhirnya ke dalam file Excel. Dengan adanya skrip ini, proses ekstraksi informasi tanaman obat dapat dilakukan secara otomatis dan berulang dengan mudah.

### **Gambaran Skrip**

File `main.py` mengoordinasikan jalannya pipeline ETL dengan memanggil tiga komponen utama yaitu `extract_links`, `transform_data`, dan `load_to_excel`. Masing-masing fungsi memiliki peran spesifik untuk memastikan informasi tanaman herbal dikumpulkan dan disimpan dengan rapi. Berikut tiga langkah utama dalam skrip ini:

1. **Membaca Tautan Tanaman dari Excel**  
   Skrip dimulai dengan membaca file Excel yang berisi daftar tautan profil tanaman obat.

```python
input_file = "link sisa 5.xlsx"
link_df = extract_links(input_file)
```

2. **Melakukan Scraping dan Transformasi Data**  
   Setiap tautan tanaman akan diproses untuk mengambil data terstruktur seperti penyebaran tanaman, nama lokal, agroekologi, dan khasiat. Hasilnya kemudian dibersihkan dan disusun dalam format yang seragam.

```python
transformed_df = transform_data(link_df)
```

3. **Mengekspor Data Akhir ke File Excel**  
   Hasil akhir disimpan ke dalam file Excel yang mencakup baik data input maupun hasil transformasi dengan menggunakan fungsi `load_to_excel`.

```python
output_file = "hasil_scraping.xlsx"
load_to_excel(transformed_df, output_file)
print("Saved to local Excel file:", output_file)
```

### **Catatan Penggunaan**

Untuk menjalankan seluruh pipeline, cukup eksekusi skrip ini dari command line atau lingkungan Python Anda:

```bash
python main.py
```

Pastikan bahwa :

- File input (misalnya `link sisa 5.xlsx`) tersedia di direktori kerja.
- File output tidak sedang terbuka di program lain (seperti Excel) agar tidak terjadi kesalahan penulisan.

Skrip ini memastikan bahwa proses ETL berlangsung secara efisien, modular, dan siap diintegrasikan dengan aplikasi atau antarmuka lanjutan.
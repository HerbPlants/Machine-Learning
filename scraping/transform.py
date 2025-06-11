from extract import extract_plant_data
import pandas as pd

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
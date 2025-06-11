import pandas as pd
import requests
from bs4 import BeautifulSoup

def extract_links(file_path):
    df = pd.read_excel(file_path)
    return df

def clean_text(text):
    # Remove illegal characters for Excel
    return ''.join(c for c in text if c.isprintable())

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
from flask import Flask, request, Response
from flask_cors import CORS
from tensorflow.keras.models import load_model
from PIL import Image, UnidentifiedImageError
import numpy as np
import json

app = Flask(__name__)
CORS(app)
model = load_model('model.h5')

# Load class indices
with open('class_indices.json', 'r', encoding='utf-8') as f:
    label_data = json.load(f)

# Load scraping detail data
with open('result-scrapping.json', 'r', encoding='utf-8') as f:
    herb_details = json.load(f)

@app.route('/predict', methods=['GET'])
def get_predict_info():
    info = {
        "success": True,
        "code": 200,
        "message": "Informasi endpoint prediksi gambar tanaman",
        "data": {
            "method": "POST",
            "endpoint": "/predict",
            "description": "Mengirim file gambar tumbuhan dan mendapatkan hasil prediksi nama tumbuhan serta detailnya.",
            "content_type": "multipart/form-data",
            "request_field": {
                "file": "File gambar tumbuhan (.jpg, .jpeg, .png)"
            },
            "response_format": {
                "success": True,
                "code": 200,
                "message": "Tumbuhan berhasil di prediksi",
                "data": {
                    "hasil_predict": {
                        "class_index": 3,
                        "confidence": 0.9876,
                        "name": "Kunyit (Curcuma longa)"
                    },
                    "detail": {
                        "name": "Kunyit",
                        "nameLatin": "Curcuma longa",
                        "description": "...",
                        "...": "..."
                    }
                }
            },
            "note": "Jika confidence < 0.70 maka akan dianggap tumbuhan tidak valid"
        }
    }
    return Response(json.dumps(info, ensure_ascii=False, indent=2), mimetype='application/json'), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return Response(json.dumps({
                "success": False,
                "code": 400,
                "message": "File foto harus ada",
                "data": {}
            }, ensure_ascii=False), mimetype='application/json'), 400

        file = request.files['file']

        # Cek apakah file benar-benar gambar
        try:
            img = Image.open(file).convert('RGB')
        except UnidentifiedImageError:
            return Response(json.dumps({
                "success": False,
                "code": 400,
                "message": "File yang dikirim bukan gambar yang valid",
                "data": {}
            }, ensure_ascii=False), mimetype='application/json'), 400

        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)[0]
        top_class = int(np.argmax(prediction))
        confidence = float(np.max(prediction))

        if confidence < 0.70:
            return Response(json.dumps({
                "success": False,
                "code": 404,
                "message": "Tumbuhan tidak valid",
                "data": {}
            }, ensure_ascii=False), mimetype='application/json'), 404

        # Dapatkan nama class lengkap
        try:
            class_full = next(name for name, idx in label_data.items() if idx == top_class)
        except StopIteration:
            class_full = "Unknown"

        # Ambil nama latin dari string class_full
        if '(' in class_full and ')' in class_full:
            name_latin = class_full.split(' (')[0]
        else:
            name_latin = class_full

        # Ambil detail berdasarkan nameLatin
        detail_data = next((item for item in herb_details if item.get("nameLatin") == name_latin), {})

        return Response(json.dumps({
            "success": True,
            "code": 200,
            "message": "Tumbuhan berhasil di prediksi",
            "data": {
                "hasil_predict": {
                    "class_index": top_class,
                    "confidence": round(confidence, 4),
                    "name": class_full
                },
                "detail": detail_data
            }
        }, ensure_ascii=False), mimetype='application/json'), 200

    except Exception as e:
        return Response(json.dumps({
            "success": False,
            "code": 500,
            "message": f"Terjadi kesalahan pada server: {str(e)}",
            "data": {}
        }, ensure_ascii=False), mimetype='application/json'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

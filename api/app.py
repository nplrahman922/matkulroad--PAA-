from flask import Flask, jsonify, request
from flask_cors import CORS
from tpsort import build_roadmap

app = Flask(__name__)
CORS(app) # Mengizinkan frontend Vue mengakses backend ini

# Simulasi data mata kuliah (bisa diganti dengan data dari Supabase/Database)
DB_DATA = [
    {"id": "MK1", "label": "Pemrograman Dasar", "sks": 3, "prerequisites": []},
    {"id": "MK2", "label": "Matematika Diskrit", "sks": 3, "prerequisites": []},
    {"id": "MK3", "label": "Struktur Data", "sks": 3, "prerequisites": ["MK1", "MK2"]},
    {"id": "MK4", "label": "Algoritma PAA", "sks": 3, "prerequisites": ["MK3"]},
]

@app.route('/api/roadmap', methods=['GET'])
def get_roadmap():
    # Kamu bisa menambahkan logika filter berdasarkan request.args.get('target')
    data = build_roadmap(DB_DATA)
    return jsonify(data)

if __name__ == '__main__':
    # Flask biasanya berjalan di port 5000
    app.run(debug=True, port=5000)
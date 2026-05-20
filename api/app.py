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
    {"id": "MK5", "label": "Basis Data", "sks": 3, "prerequisites": ["MK1"]},
    {"id": "MK6", "label": "Sistem Operasi", "sks": 3, "prerequisites": ["MK3"]},
    {"id": "MK7", "label": "Jaringan Komputer", "sks": 3, "prerequisites": ["MK6"]},
    {"id": "MK8", "label": "Pemrograman Berorientasi Objek", "sks": 3, "prerequisites": ["MK1"]},
    {"id": "MK9", "label": "Rekayasa Perangkat Lunak", "sks": 3, "prerequisites": ["MK8"]},
    {"id": "MK10", "label": "Kecerdasan Buatan", "sks": 3, "prerequisites": ["MK3", "MK2"]},
    {"id": "MK11", "label": "Pembelajaran Mesin", "sks": 3, "prerequisites": ["MK10"]},
    {"id": "MK12", "label": "Grafika Komputer", "sks": 3, "prerequisites": ["MK3"]},
    {"id": "MK13", "label": "Pemrograman Web", "sks": 3, "prerequisites": ["MK5"]},
    {"id": "MK14", "label": "Keamanan Informasi", "sks": 3, "prerequisites": ["MK7"]},
    {"id": "MK15", "label": "Skripsi", "sks": 4, "prerequisites": ["MK9", "MK4"]},
    {"id": "MK16", "label": "Pemrograman Mobile", "sks": 3, "prerequisites": ["MK8"]},
    {"id": "MK17", "label": "Interaksi Manusia dan Komputer", "sks": 3, "prerequisites": []},
    {"id": "MK18", "label": "Cloud Computing", "sks": 3, "prerequisites": ["MK7", "MK5"]},
]

@app.route('/api/roadmap', methods=['GET'])
def get_roadmap():
    target = request.args.get('target', '').strip()
    if not target:
        data = build_roadmap(DB_DATA)
        return jsonify(data)
    
    # 1. Cari mata kuliah yang cocok dengan search term (case-insensitive)
    target_lower = target.lower()
    matched_ids = []
    for course in DB_DATA:
        if target_lower in course['id'].lower() or target_lower in course['label'].lower():
            matched_ids.append(course['id'])
            
    if not matched_ids:
        # Jika tidak ada yang cocok, kembalikan graph kosong
        return jsonify({"nodes": [], "edges": []})
        
    # 2. Ambil semua leluhur (prerequisites) secara rekursif (hanya hulu/upstream)
    id_to_course = {c['id']: c for c in DB_DATA}
    
    def get_ancestors(course_id, visited):
        if course_id in visited:
            return
        visited.add(course_id)
        course = id_to_course.get(course_id)
        if course:
            for pre in course.get('prerequisites', []):
                get_ancestors(pre, visited)
                
    final_set = set()
    for m_id in matched_ids:
        ancestors_visited = set()
        get_ancestors(m_id, ancestors_visited)
        final_set.update(ancestors_visited)
        
    # Filter DB_DATA hanya untuk courses yang ada di final_set
    filtered_data = [c for c in DB_DATA if c['id'] in final_set]
    
    data = build_roadmap(filtered_data)
    return jsonify(data)

if __name__ == '__main__':
    # Flask biasanya berjalan di port 5000
    app.run(debug=True, port=5000)
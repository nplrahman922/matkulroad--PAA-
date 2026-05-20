# 🎓 MatkulRoad - Visualisasi Roadmap Mata Kuliah

[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4fc08d?style=for-the-badge&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.0-38bdf8?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Algorithm](https://img.shields.io/badge/Algorithm-Topological_Sort-blueviolet?style=for-the-badge)](https://en.wikipedia.org/wiki/Topological_sorting)

**MatkulRoad** adalah sebuah aplikasi web interaktif yang dirancang untuk memvisualisasikan peta jalan (roadmap) prasyarat mata kuliah program studi Teknik Informatika / Ilmu Komputer. Aplikasi ini dibuat untuk memenuhi tugas mata kuliah **Perancangan dan Analisis Algoritma (PAA)** dengan memanfaatkan **Algoritma Topological Sort** untuk menentukan urutan semester secara otomatis dan logis.

---

## ✨ Fitur Utama

- 🔍 **Pencarian Terarah & Presisi**: Masukkan nama atau kode mata kuliah untuk melacak jalur prasyarat secara eksklusif dari semester paling awal (*upstream ancestors*).
- 🧭 **Visualisasi Graf Interaktif**: Menggunakan **Vue Flow** untuk rendering node mata kuliah yang responsif, lengkap dengan garis penghubung yang beranimasi (*smoothstep*).
- 🗂️ **Penghitungan Layout Otomatis**: Memanfaatkan **Dagre** untuk menghitung posisi koordinat X dan Y setiap node agar graf tersusun rapi tanpa tumpang tindih.
- 🎒 **Informasi Lengkap Node**: Setiap mata kuliah menampilkan kode unik, nama mata kuliah, jumlah SKS, serta estimasi level semester.
- 📱 **Desain UI Premium & Modern**: Layout minimalis menggunakan Tailwind CSS, dilengkapi efek glowing ring saat node dicocokkan, serta animasi transisi yang mulus.
- ⚡ **Auto-Reset**: Tampilan graf akan otomatis kembali bersih saat input pencarian dikosongkan.

---

## 🏗️ Arsitektur & Teknologi

### Frontend
- **Framework**: Vue 3 (Script Setup & TypeScript)
- **Bundler**: Vite
- **Grafik/Node**: `@vue-flow/core`
- **Layouting Engine**: `dagre`
- **Styling**: Tailwind CSS (v4)

### Backend
- **Framework**: Flask (Python 3)
- **Cross-Origin**: `flask-cors`
- **Penyimpanan Data**: Simulasi Database Statis (18 Mata Kuliah CS)

---

## ⚙️ Implementasi Algoritma: Topological Sort

Aplikasi ini menggunakan **Kahn's Algorithm** untuk melakukan pengurutan topologi (*Topological Sort*) pada graf berarah tanpa siklus (*Directed Acyclic Graph* / DAG) dari mata kuliah.

### Cara Kerja Algoritma:
1. **Derajat Masuk (In-Degree)**: Menghitung berapa banyak prasyarat yang harus diselesaikan untuk mengambil suatu mata kuliah.
2. **Kahn's Queue**: Mata kuliah yang tidak memiliki prasyarat (In-Degree = 0) dimasukkan ke dalam antrean (*queue*) untuk ditempatkan pada semester awal.
3. **Reduksi Derajat**: Setiap kali sebuah mata kuliah diproses keluar dari antrean, derajat masuk mata kuliah tetangganya (yang membutuhkannya sebagai prasyarat) akan dikurangi. Jika derajat masuk tetangganya menjadi 0, mata kuliah tersebut masuk ke antrean berikutnya (semester selanjutnya).

### Skema Penyaringan Jalur:
Saat pengguna melakukan pencarian target mata kuliah (misalnya **MK4 - Algoritma PAA**), backend secara rekursif akan mengumpulkan semua leluhurnya (*ancestors*):
$$\text{MK1 (Pemrograman Dasar) \& MK2 (Matematika Diskrit)} \rightarrow \text{MK3 (Struktur Data)} \rightarrow \text{MK4 (Algoritma PAA)}$$
Hanya mata kuliah dalam rantai ini yang diproses oleh algoritma pengurutan topologi, sehingga graf yang ditampilkan fokus pada syarat menempuh mata kuliah tersebut tanpa menampilkan mata kuliah lain yang tidak relevan.

---

## 🚀 Panduan Memulai (Instalasi & Menjalankan)

### 1. Klon Repositori
```bash
git clone https://github.com/USERNAME/matkulroad--PAA-.git
cd matkulroad--PAA-
```

### 2. Jalankan Backend (Flask API)
Masuk ke direktori `api` dan siapkan Python virtual environment:
```bash
cd api

# Buat virtual environment (jika belum ada)
python -m venv .venv

# Aktifkan virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux/MacOS/WSL:
source .venv/bin/activate

# Pasang dependensi
pip install flask flask-cors

# Jalankan server Flask (berjalan di http://localhost:5000)
python app.py
```

### 3. Jalankan Frontend (Vue 3 + Vite)
Buka terminal baru di direktori utama `matkulroad--PAA-`:
```bash
cd frontend/matkulroad-view

# Pasang dependensi node
npm install

# Jalankan dev server (berjalan di http://localhost:5173)
npm run dev
```

---

## 📊 Struktur Data Mata Kuliah

Simulasi database mata kuliah disimpan dalam format JSON di `app.py`. Contoh bentuk datanya:

```json
{
  "id": "MK3",
  "label": "Struktur Data",
  "sks": 3,
  "prerequisites": ["MK1", "MK2"]
}
```

---

## 🤝 Kontribusi

Kontribusi sangat terbuka! Silakan lakukan *Fork* repositori ini, buat *branch* baru, lakukan perubahan, lalu ajukan *Pull Request*.

*Dibuat untuk tugas mata kuliah Perancangan dan Analisis Algoritma (PAA).*

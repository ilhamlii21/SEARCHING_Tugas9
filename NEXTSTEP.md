# Rencana Kerja & Checklist (NEXTSTEP.md)

**Mata Kuliah:** Kecerdasan Buatan RPL (Semester Genap 2025/2026)  
**Tugas:** Case Based - Searching (Genetic Algorithm)  
**Anggota Kelompok:** Lian & Ilham  
**Tenggat Waktu (Deadline LMS):** **Senin, 16 November 2026, pukul 23:59 WIB**  

---

## 📌 Ringkasan Status Pengerjaan

| No | Komponen Deliverable | Penanggung Jawab (PIC) | Status | Keterangan & Ketergantungan |
|---|---|---|---|---|
| 1 | **Source Code Program (`ga_varian.py`)** | **Lian** | ✅ **DONE** | Telah diuji dan berjalan normal tanpa library pihak ketiga. |
| 2 | **Laporan Tahapan Algoritma (.PDF)** | **Lian** | ⏳ **SOON** | Sedang disusun (mengacu pada kode & template PDF tugas). |
| 3 | **Slide Presentasi (.PPTX / .PDF)** | **Ilham** | ⏳ **SOON** | Menunggu outline & screenshot running dari Laporan Lian. |
| 4 | **Perekaman Video Presentasi** | **Ilham** *(didukung Lian)* | ⏳ **SOON** | Menunggu PPT selesai dan materi laporan difinalkan. |
| 5 | **Pengemasan & Submit LMS CeLOE (.ZIP)** | **Lian & Ilham** | ⏳ **SOON** | Dilakukan serentak sebelum deadline 16 Nov 2026 23:59. |

---

## 📋 Checklist Rinci Tahapan Kerja

### 1. Source Code Program (`ga_varian.py`) — [PIC: Lian]
> **Status:** ✅ **DONE** (Bobot Penilaian: 30%)
- [x] Implementasi inisialisasi populasi real-coded (`[g1, g2]`) dengan ukuran populasi 74.
- [x] Implementasi fungsi decoding linear dari domain $[0, 1]$ ke $[-10, 10]$.
- [x] Implementasi fungsi objektif matematis $f(x_1, x_2)$.
- [x] Implementasi fungsi fitness dengan transformasi maksimasi & kompresi logaritmik $\ln(1 + g - g_{\min})$ untuk mengatasi asimtot tangen.
- [x] Implementasi pemilihan orang tua dengan *Roulette Wheel Selection*.
- [x] Implementasi *Whole Arithmetic Crossover* ($P_c = 0.75$).
- [x] Implementasi *Gaussian Mutation* ($P_m = 0.15, \sigma = 0.05$).
- [x] Implementasi *Generational Replacement* dengan Elitisme 5% (4 individu terbaik).
- [x] Implementasi kriteria penghentian (Target $f \le -10^6$, Max Generasi = 250, Stagnan = 40 generasi).
- [x] Memastikan tidak ada penggunaan library GA pihak ketiga (hanya menggunakan bawaan `math` dan `random`).
- [x] Validasi eksekusi program tanpa error dan verifikasi format output terminal.

---

### 2. Dokumen Laporan Tugas (.PDF) — [PIC: Lian]
> **Status:** ⏳ **SOON** (Bobot Penilaian: 40%)  
> *Target Penyelesaian: Minggu, 15 November 2026, 18:00 WIB*

- [ ] **Persiapan & Cover:**
  - [ ] Judul: Laporan Case Based - Searching Kecerdasan Buatan.
  - [ ] Informasi kelompok: Kelas, Nomor Kelompok, Nama Lengkap & NIM (Lian & Ilham).
- [ ] **Bab 1: Deskripsi Masalah & Persoalan:**
  - [ ] Menuliskan kembali fungsi matematis $f(x_1, x_2)$ dan batas domain $[-10 \le x_1, x_2 \le 10]$.
  - [ ] Analisis karakteristik fungsi (adanya fungsi tangen yang memiliki titik diskontinuitas/asimtot).
  - [ ] Tujuan optimasi (minimasi fungsi).
- [ ] **Bab 2: Desain & Analisis Algoritma Genetika:**
  - [ ] **2.1 Ukuran Populasi & Kromosom:** Penjelasan alasan ukuran populasi 74, representasi gen real `[g1, g2]`, dan rumus dekode.
  - [ ] **2.2 Perhitungan Fitness:** Penjelasan konversi minimasi ke maksimasi dan formula kompresi logaritmik $\ln(1 + g - g_{\min})$ agar seleksi stabil saat mendekati asimtot.
  - [ ] **2.3 Pemilihan Orang Tua:** Mekanisme kerja *Roulette Wheel Selection*.
  - [ ] **2.4 Operasi Genetik:** Formula dan parameter *Arithmetic Crossover* ($P_c = 0.75$) dan *Gaussian Mutation* ($P_m = 0.15$).
  - [ ] **2.5 Pergantian Generasi:** Skema pergantian generasi dan elitisme 4 individu terbaik.
  - [ ] **2.6 Kriteria Penghentian:** Kriteria target nilai, batas 250 generasi, dan batas stagnansi 40 generasi.
- [ ] **Bab 3: Hasil Eksperimen & Analisis:**
  - [ ] Melampirkan **Screenshot hasil running program** langsung dari terminal.
  - [ ] Menampilkan nilai kromosom terbaik, nilai $x_1$ dan $x_2$ hasil dekode, serta nilai minimum $f(x_1, x_2)$ yang diperoleh.
  - [ ] Pembahasan singkat mengenai konvergensi generasi ke generasi.
- [ ] **Bab 4: Pembagian Peran Anggota Kelompok:**
  - [ ] Menjelaskan kontribusi Lian (pengembangan source code & penyusunan laporan tertulis).
  - [ ] Menjelaskan kontribusi Ilham (desain slide presentasi & perekaman/editing video presentasi).
- [ ] **Finalisasi Laporan:**
  - [ ] Proofreading dan cek kesesuaian antara penjelasan laporan dengan kode program.
  - [ ] Export dokumen ke format **PDF** (`Laporan_Case_Based_Searching.pdf`).

---

### 3. Slide Presentasi PPT untuk Bahan Video — [PIC: Ilham]
> **Status:** ⏳ **SOON** (Menunggu Laporan & Screenshot dari Lian)  
> *Target Penyelesaian: Minggu, 15 November 2026, 22:00 WIB*

- [ ] **Penyusunan Struktur Slide (Maksimal 5-6 Slide, fokus durasi < 5 menit):**
  - [ ] **Slide 1 (Judul):** Judul tugas, mata kuliah, kelas, nama & NIM Lian & Ilham.
  - [ ] **Slide 2 (Pemahaman Masalah):** Definisi fungsi objektif matematis, domain $[-10, 10]$, dan tantangan optimasi (asimtot $\tan$).
  - [ ] **Slide 3 (Arsitektur Desain GA):** Ringkasan tabel/poin GA (Real-coded, Fitness logaritma, Roulette Wheel, Arithmetic Crossover, Gaussian Mutation, Elitisme).
  - [ ] **Slide 4 (Hasil Running & Output):** Screenshot eksekusi program, nilai $x_1, x_2$ terbaik, nilai minimum fungsi, dan grafik/catatan generasi berhenti.
  - [ ] **Slide 5 (Analisis & Kesimpulan):** Efektivitas metode yang dirancang dan insight performa GA.
- [ ] **Review Slide Bersama Lian:** Memastikan data pada slide identik dengan apa yang tertulis di laporan dan kode.

---

### 4. Perekaman Video Presentasi — [PIC: Ilham & Lian]
> **Status:** ⏳ **SOON** (Menunggu PPT dan Laporan siap)  
> *Target Penyelesaian: Senin, 16 November 2026, 15:00 WIB*

- [ ] **Ketentuan Video (Mengacu aturan presentasi):**
  - [ ] Durasi pemaparan materi inti maksimal **5 menit**.
  - [ ] Fokus isi: (1) Pemahaman masalah, (2) Hal-hal yang dirancang kelompok, (3) Hasil/output program & pendapat tim terhadapnya.
- [ ] **Teknis Perekaman:**
  - [ ] Menggunakan platform perekam (Zoom, OBS Studio, Google Meet, atau Canva Presentation).
  - [ ] Pastikan suara jelas dan slide terbaca dengan baik.
  - [ ] Demonstrasikan sedikit cuplikan running kode program `ga_varian.py` di terminal.
- [ ] **Penyimpanan Video:**
  - [ ] Unggah video ke Google Drive / YouTube (Unlisted) dan pastikan permission link diset ke *"Anyone with the link can view"*.
  - [ ] Sisipkan link video ke dalam slide dan dokumen laporan (untuk antisipasi ukuran file jika zip terbatas).

---

### 5. Packaging Akhir & Pengumpulan LMS CeLOE — [PIC: Lian & Ilham]
> **Status:** ⏳ **SOON**  
> *Target Pengumpulan: Senin, 16 November 2026, sebelum pukul 20:00 WIB (Batas akhir: 23:59 WIB)*

- [ ] Kumpulkan seluruh file final ke dalam satu folder:
  1. `ga_varian.py` (Source Code Python)
  2. `Laporan_Case_Based_Searching.pdf` (Laporan Lengkap PDF)
  3. `Slide_Presentasi.pptx` / `Slide_Presentasi.pdf`
- [ ] Kompres folder menjadi format **`.ZIP`**.
- [ ] **Format Penamaan File ZIP Wajib:**
  - Rumus: `KELAS_KELOMPOK_NIM.zip`
  - Contoh: `SE4801_03_1311281234.zip`
- [ ] **Upload ke CeLOE:**
  - [ ] Lian mengunggah file zip dengan penamaan NIM Lian.
  - [ ] Ilham mengunggah file zip dengan penamaan NIM Ilham.
- [ ] Lakukan verifikasi di LMS bahwa status pengumpulan sudah *Submitted for grading*.

# PANDUAN KONTEN SLIDE PRESENTASI (PPT.md)

**Mata Kuliah:** Kecerdasan Buatan RPL (Semester Genap 2025/2026)  
**Tugas:** Case Based - Searching (Genetic Algorithm)  
**Varian:** Varian 3 (Real-Coded GA + Logarithmic Fitness)  
**Anggota Kelompok:**  
1. **Lian** (NIM: [Isi NIM Lian]) — *Developer & Author Laporan*  
2. **Ilham** (NIM: [Isi NIM Ilham]) — *Presenter & Visual Designer*  

> **Petunjuk untuk Ilham:**  
> File ini dirancang untuk 10 slide presentasi. Setiap slide dilengkapi dengan **Poin Isi Slide** (yang ditampilkan di PowerPoint) dan **Script / Talking Points** (narasi yang dibaca saat *take video* presentasi, total estimasi durasi: 4–5 menit).

---

## SLIDE 1: Pembuka & Identitas Kelompok

### Konten Visual Slide:
- **Judul Utama:** Optimasi Fungsi Non-Linear Kompleks Menggunakan Algoritma Genetika
- **Sub-judul:** Case Based - Searching | Kecerdasan Buatan RPL (Genap 2025/2026)
- **Desain Khusus:** Varian 3 (Real-Coded GA with Logarithmic Fitness Compression)
- **Identitas Anggota Kelompok:**
  - **Lian** — NIM: [Isi NIM Lian]
  - **Ilham** — NIM: [Isi NIM Ilham]
- **Institusi:** S1 Rekayasa Perangkat Lunak, Telkom University

### Narasi Presenter (Talking Points):
> "Halo semuanya dan selamat datang pada presentasi tugas Case Based Searching mata kuliah Kecerdasan Buatan. Saya Ilham bersama rekan saya Lian dari kelompok [Nomor Kelompok]. Pada kesempatan ini, kami mempresentasikan perancangan dan implementasi Algoritma Genetika yang kami bangun murni dari nol untuk menyelesaikan permasalahan minimasi fungsi matematis non-linear kompleks."

---

## SLIDE 2: Definisi Masalah & Fungsi Objektif

### Konten Visual Slide:
- **Tujuan Kasus:** Mencari nilai $x_1$ dan $x_2$ yang menghasilkan nilai **minimum global**.
- **Fungsi Matematis:**
  $$f(x_1, x_2) = -\left(\sin(x_1)\cos(x_2)\tan(x_1 + x_2) + \frac{1}{2}\exp(1 - \sqrt{x_2^2})\right)$$
- **Batasan Ruang Pencarian (Domain):**
  $$-10 \le x_1 \le 10 \quad \text{dan} \quad -10 \le x_2 \le 10$$
- **Tantangan Utama:**
  - Fungsi trigonometri $\tan(x_1 + x_2)$ memiliki asimtot tegak pada titik $\frac{\pi}{2} + k\pi$.
  - Menimbulkan jurang nilai ekstrem menuju $-\infty$, rentan menyebabkan ketidakstabilan numerik (*arithmetic overflow*).

### Narasi Presenter (Talking Points):
> "Permasalahan yang kami selesaikan adalah mencari nilai x1 dan x2 pada interval minus 10 hingga positif 10 yang meminimalkan fungsi f(x1, x2). Tantangan utama fungsi ini terletak pada komponen tangen (x1 + x2) yang memiliki asimtot tegak. Ketika input mendekati asimtot, nilai fungsi dapat turun drastis menuju minus tak hingga. Hal ini menuntut desain algoritma genetika yang kokoh agar tidak bias atau rusak secara numerik."

---

## SLIDE 3: Arsitektur Umum Algoritma Genetika (Varian 3)

### Konten Visual Slide:
- **Diagram Alur GA:**
  `Inisialisasi Populasi` $\to$ `Dekode Kromosom` $\to$ `Evaluasi Fitness` $\to$ `Seleksi Roulette Wheel` $\to$ `Arithmetic Crossover` $\to$ `Gaussian Mutation` $\to$ `Pergantian Generasi (Elitisme)` $\to$ `Pengecekan Terminasi`
- **Aturan Implementasi:**
  - Murni *From Scratch* (Hanya modul bawaan Python `math` dan `random`).
  - Tanpa library GA eksternal (bebas dari DEAP, PyGAD, dll.).
- **Spesifikasi Varian 3:**
  - Populasi: 74 individu.
  - Representasi: Vektor Real-Coded $[0, 1]$.
  - Elitisme: 5% (4 individu terbaik).

### Narasi Presenter (Talking Points):
> "Berdasarkan pedoman tugas, kami mengimplementasikan seluruh komponen GA secara mandiri tanpa menggunakan library tambahan. Alur yang kami bangun menerapkan Varian 3, dimulai dari inisialisasi 74 individu berkode riil, dekode pemetaan linear, perhitungan fitness terkompresi logaritmik, seleksi roulette wheel, operasi pindah silang aritmatika, mutasi gaussian, dan elitisme untuk menjaga individu terbaik."

---

## SLIDE 4: Representasi Kromosom & Metode Dekode

### Konten Visual Slide:
- **Rancangan Kromosom:**
  - Model: *Real-Coded Chromosome* $[g_1, g_2]$.
  - Panjang: 2 Gen (1 gen untuk $x_1$, 1 gen untuk $x_2$).
  - Ruang Genetik: Tiap alel $g_i \in [0.0, 1.0]$ (bilangan desimal presisi tinggi).
- **Formula Dekode (Linear Mapping):**
  $$x_1 = -10.0 + g_1 \times (10.0 - (-10.0))$$
  $$x_2 = -10.0 + g_2 \times (10.0 - (-10.0))$$
- **Keunggulan:**
  - Kontinu tanpa diskritisasi (tidak kehilangan resolusi dibanding representasi biner).
  - Ringkas dan efisien secara komputasi memori.

### Narasi Presenter (Talking Points):
> "Kromosom dirancang menggunakan representasi Real-Coded dengan 2 gen bernilai desimal antara 0 dan 1. Untuk mengevaluasi ke dalam fungsi objektif, gen tersebut didekode secara linear ke domain minus 10 hingga 10. Pendekatan real-coded ini sangat ideal untuk masalah optimasi kontinu karena menghindari masalah resolusi diskrit yang biasa terjadi pada representasi biner."

---

## SLIDE 5: Evaluasi Fitness & Strategi Kompresi Logaritmik

### Konten Visual Slide:
- **Transformasi Minimasi ke Maksimasi:**
  $$g(x_1, x_2) = -f(x_1, x_2)$$
- **Masalah Dominasi Ekstrem:**
  - Nilai $g$ di dekat asimtot bisa mencapai ribuan hingga jutaan.
  - Individu ekstrem akan memonopoli roda roulette (99%+ proporsi), merusak diversitas populasi (*premature convergence*).
- **Formula Solusi (Compressed Fitness):**
  $$\text{Fitness}_i = \ln(1 + g_i - g_{\min}) + 10^{-9}$$
- **Hasil:**
  - Nilai fitness selalu positif ($\ge 0$).
  - Mempertahankan urutan keunggulan (*rank-preserving*).
  - Skala roulette wheel tetap proporsional dan sehat.

### Narasi Presenter (Talking Points):
> "Karena tujuan kita adalah minimasi, nilai f dikalikan minus satu agar menjadi masalah maksimasi. Namun, karena adanya asimtot tangen, nilai g bisa melonjak sangat besar dan memonopoli seleksi. Solusi inovatif yang kelompok kami terapkan adalah pergeseran baseline dan kompresi logaritmik: ln(1 + g - g_min). Melalui kompresi ini, individu terbaik tetap memiliki peluang tertinggi, namun individu lain tetap berkesempatan berevolusi."

---

## SLIDE 6: Mekanisme Seleksi Orang Tua (Roulette Wheel)

### Konten Visual Slide:
- **Metode Seleksi:** *Roulette Wheel Selection* (Seleksi Roda Roulette Proposional).
- **Formula Probabilitas:**
  $$P_k = \frac{\text{Fitness}_k}{\sum_{j=1}^{N} \text{Fitness}_j}$$
- **Mekanisme Eksekusi:**
  1. Hitung total fitness populasi.
  2. Bangkitkan angka acak $r \in [0, \text{Total Fitness}]$.
  3. Lakukan akumulasi kumulatif hingga melewati $r$.
- **Karakteristik:**
  - Eksploitasi terkontrol (individu fit lebih sering terpilih).
  - Mempertahankan variasi genetik generasi berikutnya.

### Narasi Presenter (Talking Points):
> "Untuk memilih orang tua yang akan bereproduksi, kami menggunakan metode Roulette Wheel Selection. Peluang terpilihnya suatu kromosom berbanding lurus dengan nilai fitness terkompresinya. Dengan memanfaatkan kumulatif fitness dan sampling acak, algoritma kami menyeimbangkan aspek eksploitasi solusi terbaik dengan eksplorasi gen-gen baru."

---

## SLIDE 7: Operasi Genetik: Crossover & Mutasi

### Konten Visual Slide:
- **Pindah Silang: Whole Arithmetic Crossover ($P_c = 0.75$)**
  - Probabilitas crossover: 75%.
  - Parameter acak $\alpha \in [0, 1]$:
    $$c_1 = \alpha \cdot p_1 + (1 - \alpha) \cdot p_2$$
    $$c_2 = (1 - \alpha) \cdot p_1 + \alpha \cdot p_2$$
  - Anak selalu berada di dalam domain yang valid ($[0, 1]$).
- **Mutasi: Gaussian Mutation ($P_m = 0.15, \sigma = 0.05$)**
  - Probabilitas mutasi per gen: 15%.
  - Perturbasi acak normal: $g' = g + \mathcal{N}(0, \sigma^2)$.
  - *Boundary Clipping:* Nilai gen dijaga tetap di dalam range $[0, 1]$.

### Narasi Presenter (Talking Points):
> "Operasi reproduksi genetik terdiri dari Arithmetic Crossover dan Gaussian Mutation. Pindah silang aritmatika dengan probabilitas 0.75 menghasilkan kombinasi linear halus antara kedua orang tua. Sedangkan mutasi Gaussian dengan simpangan baku 0.05 dan probabilitas 15% memberikan sedikit derau acak agar algoritma tidak terjebak pada optimum lokal."

---

## SLIDE 8: Pergantian Generasi & Kriteria Penghentian

### Konten Visual Slide:
- **Strategi Pergantian Generasi (Survivor Selection):**
  - *Generational Replacement* dipadukan dengan **Elitisme 5%** (4 individu terbaik).
  - 4 individu terbaik langsung dipertahankan ke generasi berikutnya tanpa modifikasi.
  - Sisa 70 individu diisi oleh keturunan baru hasil rekombinasi dan mutasi.
- **Kriteria Berhenti (Stopping Criteria):**
  1. **Target Ekstrem:** $f(x_1, x_2) \le -10^6$.
  2. **Maksimum Generasi:** Mencapai generasi ke-250.
  3. **Stagnasi:** Tidak ada perbaikan solusi selama 40 generasi berturut-turut.

### Narasi Presenter (Talking Points):
> "Untuk pergantian generasi, kami menerapkan elitisme 5 persen, di mana 4 individu terbaik langsung diselamatkan ke generasi berikutnya agar pencapaian terbaik tidak hilang. Proses evolusi ini dikendalikan oleh tiga kriteria penghentian: tercapainya target ekstrem minus satu juta, batas 250 generasi, atau kondisi stagnan selama 40 generasi berturut-turut."

---

## SLIDE 9: Hasil Eksperimen & Analisis Output

### Konten Visual Slide:
- **Screenshot Terminal Running Program:**
  *(Sediakan tempat untuk menempelkan tangkapan layar output eksekusi)*
- **Ringkasan Hasil Eksekusi:**
  - **Status Selesai:** Berhenti di generasi ke-116 (Stagnan 40 generasi).
  - **Kromosom Terbaik:** `[0.40990667, 0.51156336]`
  - **Nilai Dekode:**
    $$x_1 = -1.801867, \quad x_2 = 0.231267$$
  - **Nilai Minimum yang Dicapai:**
    $$f(x_1, x_2) = -4808.418925$$
- **Analisis Konvergensi:**
  - Dari generasi 1 ($f \approx -6.6$) melonjak tajam ke generasi 80 ($f \approx -4808.4$).
  - Algoritma berhasil memetakan titik dekat asimtot dengan presisi tinggi dan stabil.

### Narasi Presenter (Talking Points):
> "Berikut adalah hasil pengujian program yang kami jalankan. Program berhenti pada generasi ke-116 karena tercapainya kondisi konvergensi stagnan selama 40 generasi. Solusi terbaik yang diperoleh menghasilkan kromosom dengan dekode x1 sekitar minus 1.8018 dan x2 sekitar 0.2312, dengan nilai minimum fungsi mencapai minus 4808.42. Ini membuktikan GA mampu menemukan wilayah lembah asimtotik yang sangat dalam."

---

## SLIDE 10: Kesimpulan & Goals yang Tercapai

### Konten Visual Slide:
- **Evaluasi Goals Kasus:**
  - [x] **100% Native Python:** Semua fungsi GA dibangun mandiri tanpa library GA eksternal.
  - [x] **Stabilitas Numerik:** Kompresi fitness logaritmik terbukti efektif menangani singularitas fungsi $\tan$.
  - [x] **Konvergensi Efektif:** Kombinasi *Arithmetic Crossover*, *Gaussian Mutation*, dan *Elitism* mencegah degradasi solusi.
  - [x] **Output Sesuai Regulasi:** Menghasilkan kromosom terbaik, nilai dekode $x_1$ & $x_2$, dan nilai evaluasi minimum fungsi.
- **Penutup:**
  - *Terima Kasih atas perhatian Bapak/Ibu Dosen dan Rekan-rekan.*
  - *Sesi Tanya Jawab (Q&A).*

### Narasi Presenter (Talking Points):
> "Sebagai kesimpulan, seluruh target yang diberikan pada tugas Case Based Searching ini telah berhasil kami penuhi dengan baik. Program kami berjalan secara mandiri, stabil, dan sukses mengoptimasi fungsi non-linear yang menantang ini. Terima kasih atas perhatian teman-teman dan dosen pengampu, kami membuka ruang untuk sesi diskusi dan tanya jawab."

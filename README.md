# Case Based - Searching | Kecerdasan Buatan (GA)
**Mata Kuliah:** Kecerdasan Buatan RPL (Semester Genap 2025/2026)  
**Kelompok:** Lian & Ilham  

---

## 1. Deskripsi Tugas & Goals

Tugas ini bertujuan untuk menemukan nilai $x_1$ dan $x_2$ yang **meminimalkan** suatu fungsi matematis non-linear kompleks menggunakan **Algoritma Genetika (Genetic Algorithm / GA)** yang dibangun murni dari awal (*from scratch*) tanpa menggunakan library GA (seperti DEAP, PyGAD, dsb.).

### Fungsi Objektif
$$f(x_1, x_2) = -\left(\sin(x_1) \cdot \cos(x_2) \cdot \tan(x_1 + x_2) + \frac{1}{2}\exp\left(1 - \sqrt{x_2^2}\right)\right)$$

### Batasan Domain
$$-10 \le x_1 \le 10 \quad \text{dan} \quad -10 \le x_2 \le 10$$

### Target / Goals
1. Mengembangkan seluruh proses GA murni menggunakan Python native (`math` dan `random`).
2. Menghasilkan kromosom terbaik dan nilai dekode $x_1, x_2$ yang meminimalkan $f(x_1, x_2)$.
3. Menangani karakteristik fungsi matematis yang memiliki asimtot tegak pada $\tan(x_1 + x_2)$ sehingga nilai fungsi dapat menuju $-\infty$.

---

## 2. Desain Algoritma Genetika (Varian 3)

| Komponen GA | Desain yang Diimplementasikan | Keterangan / Formula |
| :--- | :--- | :--- |
| **Ukuran Populasi** | 74 individu | Menjaga keragaman genetik yang cukup luas |
| **Representasi Kromosom** | *Real-Coded* (`[g1, g2]`) | Tiap gen berupa bilangan riil $g_i \in [0, 1]$ |
| **Cara Decode** | Linear Mapping $[0, 1] \to [-10, 10]$ | $x_i = -10.0 + g_i \times (10.0 - (-10.0))$ |
| **Fungsi Fitness** | Logarithmic Compressed Fitness | $g = -f(x)$ (transformasi ke maksimasi).<br>$\text{fitness} = \ln(1 + g - g_{\min}) + 10^{-9}$ |
| **Seleksi Orang Tua** | *Roulette Wheel Selection* | Peluang terpilih sebanding dengan fitness terkompresi |
| **Crossover (Pindah Silang)**| *Whole Arithmetic Crossover* | $P_c = 0.75$<br>$c_1 = \alpha p_1 + (1-\alpha) p_2$<br>$c_2 = (1-\alpha) p_1 + \alpha p_2$ ($\alpha \in [0, 1]$ acak) |
| **Mutasi** | *Gaussian Mutation* | $P_m = 0.15$ per gen, $\sigma = 0.05$<br>$g' = g + \mathcal{N}(0, \sigma^2)$, di-clipping ke $[0, 1]$ |
| **Pergantian Generasi** | *Generational* + Elitisme 5% | 4 individu terbaik langsung disalin ke generasi baru |
| **Kriteria Penghentian** | Tiga kondisi stop | 1. $f(x) \le -10^6$ (target nilai ekstrem)<br>2. Maksimal 250 generasi<br>3. Stagnan 40 generasi berturut-turut |

---

## 3. Struktur Kode (`ga_varian.py`)

- `fungsi_objektif(x1, x2)`: Menghitung nilai fungsi matematis yang ingin diminimalkan.
- `inisialisasi_populasi(ukuran)`: Membangkitkan populasi awal berisi vektor 2 dimensi $[g_1, g_2]$ dengan nilai acak $[0, 1]$.
- `dekode(kromosom)`: Memetakan alel $[0, 1]$ kembali ke ruang pencarian real $[-10, 10]$.
- `hitung_fitness_populasi(populasi)`: Menghitung fitness dengan pergeseran baseline dan kompresi logaritmik agar individu mendekati asimtot tidak mendominasi roulette wheel secara mutlak.
- `seleksi_roulette(populasi, fitness)`: Memilih parent menggunakan teknik roda roulette kumulatif.
- `crossover_aritmatika(p1, p2)`: Rekombinasi linier aritmatika antara dua kromosom orang tua.
- `mutasi_gaussian(kromosom)`: Memberikan perturbasi berdistribusi normal dengan standar deviasi terkontrol.
- `ganti_generasi(populasi, fitness)`: Menjaga elitisme 4 individu terbaik dan mengisi sisanya dengan keturunan baru hasil crossover dan mutasi.
- `jalankan_ga()`: Loop evolusi utama dengan pengecekan kriteria terminasi.

---

## 4. Cara Menjalankan Program

Pastikan Python 3 sudah terpasang di komputer:

```bash
python ga_varian.py
```

### Contoh Output Terminal:
```text
Generasi   1 | f(x) terbaik = -6.603255
Generasi  10 | f(x) terbaik = -28.288375
...
Generasi  90 | f(x) terbaik = -4808.418925
Berhenti di generasi 116: stagnan 40 generasi.

=========== HASIL ===========
Kromosom terbaik : [0.40990667, 0.51156336]
Hasil dekode     : x1 = -1.801867 , x2 = 0.231267
Nilai f(x1,x2)   : -4808.418925
```

"""
GENETIC ALGORITHM CASE BASED SEARCHING
Mata Kuliah: Kecerdasan Buatan

Seluruh proses utama GA dibuat manual:
1. Inisialisasi populasi
2. Decoding kromosom
3. Perhitungan fitness
4. Tournament selection
5. One-point crossover
6. Bit-flip mutation
7. Elitist survivor selection

Library yang digunakan hanya random dan math (library standar Python),
bukan library/toolbox Genetic Algorithm.
"""

import random
import math

# PARAMETER / DESAIN GENETIC ALGORITHM

UKURAN_POPULASI = 74
PANJANG_GEN = 16
PANJANG_KROMOSOM = 32

BATAS_BAWAH = -10.0
BATAS_ATAS = 10.0

UKURAN_TOURNAMENT = 3
PROB_CROSSOVER = 0.85
PROB_MUTASI = 0.02

JUMLAH_ELIT = 2
MAKS_GENERASI = 250
BATAS_STAGNAN = 50

# Seed agar hasil eksperimen dapat diulang dengan parameter sama.
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Fungsi tan(x1+x2) singular ketika cos(x1+x2) = 0.
# Kandidat yang terlalu dekat dengan singularitas ditolak.
EPS_SINGULAR = 1e-4

# FUNGSI OBJEKTIF

def fungsi_objektif(x1, x2):
    """
    Menghitung:
    f(x1,x2) = -1/2 * (
        sin(x1)*cos(x2)*tan(x1+x2) + exp(1 - sqrt(x2^2))
    )

    Python menggunakan radian untuk fungsi trigonometri.
    sqrt(x2^2) sama dengan abs(x2).
    Mengembalikan None untuk kandidat dekat singularitas.
    """
    jumlah = x1 + x2
    cos_jumlah = math.cos(jumlah)

    # Hindari evaluasi tan yang tidak stabil/dekat singularitas.
    if abs(cos_jumlah) < EPS_SINGULAR:
        return None

    nilai_tan = math.sin(jumlah) / cos_jumlah
    nilai_eksponensial = math.exp(1.0 - abs(x2))

    nilai = -0.5 * (
        math.sin(x1) * math.cos(x2) * nilai_tan
        + nilai_eksponensial
    )

    if not math.isfinite(nilai):
        return None

    return nilai

# 3. INISIALISASI POPULASI

def buat_kromosom_acak():
    """Membuat satu kromosom acak sepanjang 32 bit."""
    kromosom = ""
    for _ in range(PANJANG_KROMOSOM):
        kromosom += random.choice("01")
    return kromosom


def inisialisasi_populasi():
    """Membuat 74 individu sebagai populasi awal."""
    populasi = []
    for _ in range(UKURAN_POPULASI):
        populasi.append(buat_kromosom_acak())
    return populasi

# DECODE KROMOSOM

def decode(kromosom):
    """
    Memisahkan kromosom menjadi dua gen:
    16 bit pertama untuk x1 dan 16 bit berikutnya untuk x2.
    Setiap gen biner dikonversi ke desimal, lalu dipetakan
    secara linear ke domain [-10, 10].
    """
    gen_x1 = kromosom[:PANJANG_GEN]
    gen_x2 = kromosom[PANJANG_GEN:]

    desimal_x1 = int(gen_x1, 2)
    desimal_x2 = int(gen_x2, 2)

    nilai_maksimum = (2 ** PANJANG_GEN) - 1
    rentang = BATAS_ATAS - BATAS_BAWAH

    x1 = BATAS_BAWAH + (desimal_x1 / nilai_maksimum) * rentang
    x2 = BATAS_BAWAH + (desimal_x2 / nilai_maksimum) * rentang

    return x1, x2

# PERHITUNGAN FITNESS

def hitung_fitness(populasi):
    """
    Karena masalah merupakan minimisasi, nilai objektif yang
    lebih kecil harus memperoleh fitness lebih besar.

    Fitness = 1 / (1 + (f - f_min))
    Kandidat dekat singularitas diberi fitness 0.
    """
    nilai_objektif = []

    for kromosom in populasi:
        x1, x2 = decode(kromosom)
        nilai = fungsi_objektif(x1, x2)
        nilai_objektif.append(nilai)

    nilai_valid = [nilai for nilai in nilai_objektif if nilai is not None]

    # Jika seluruh individu tidak valid, kembalikan fitness nol.
    if len(nilai_valid) == 0:
        return [0.0] * len(populasi), nilai_objektif

    nilai_minimum = min(nilai_valid)
    fitness = []

    for nilai in nilai_objektif:
        if nilai is None:
            fitness.append(0.0)
        else:
            selisih = nilai - nilai_minimum
            fitness.append(1.0 / (1.0 + max(0.0, selisih)))

    return fitness, nilai_objektif

# SELEKSI ORANG TUA: TOURNAMENT SELECTION

def seleksi_orang_tua(populasi, fitness):
    """
    Memilih 3 individu secara acak.
    Individu dengan fitness tertinggi menjadi orang tua.
    """
    peserta = random.sample(
        range(len(populasi)),
        UKURAN_TOURNAMENT
    )

    indeks_terbaik = peserta[0]

    for indeks in peserta[1:]:
        if fitness[indeks] > fitness[indeks_terbaik]:
            indeks_terbaik = indeks

    return populasi[indeks_terbaik]

# CROSSOVER: ONE-POINT CROSSOVER

def crossover(parent1, parent2):
    """
    Dengan probabilitas 0.85, pilih satu titik potong.
    Bagian kromosom setelah titik potong ditukar.
    """
    if random.random() < PROB_CROSSOVER:
        titik_potong = random.randint(1, PANJANG_KROMOSOM - 1)

        anak1 = parent1[:titik_potong] + parent2[titik_potong:]
        anak2 = parent2[:titik_potong] + parent1[titik_potong:]

        return anak1, anak2

    # Jika tidak crossover, anak merupakan salinan orang tua.
    return parent1, parent2


# MUTASI: BIT-FLIP MUTATION


def mutasi(kromosom):
    """
    Setiap bit memiliki peluang 0.02 untuk dibalik:
    0 menjadi 1 atau 1 menjadi 0.
    """
    hasil = []

    for bit in kromosom:
        if random.random() < PROB_MUTASI:
            if bit == "0":
                hasil.append("1")
            else:
                hasil.append("0")
        else:
            hasil.append(bit)

    return "".join(hasil)

# SURVIVOR SELECTION: ELITISM

def pergantian_generasi(populasi, fitness):
    """
    Dua individu dengan fitness tertinggi dipertahankan.
    Slot lainnya diisi keturunan hasil seleksi, crossover,
    dan mutasi sampai ukuran populasi kembali menjadi 74.
    """
    indeks_urut = sorted(
        range(len(populasi)),
        key=lambda i: fitness[i],
        reverse=True
    )

    populasi_baru = []

    # Salin dua individu terbaik (elitism).
    for i in range(JUMLAH_ELIT):
        populasi_baru.append(populasi[indeks_urut[i]])

    # Buat keturunan sampai jumlah populasi terpenuhi.
    while len(populasi_baru) < UKURAN_POPULASI:
        parent1 = seleksi_orang_tua(populasi, fitness)
        parent2 = seleksi_orang_tua(populasi, fitness)

        anak1, anak2 = crossover(parent1, parent2)

        anak1 = mutasi(anak1)
        anak2 = mutasi(anak2)

        populasi_baru.append(anak1)

        if len(populasi_baru) < UKURAN_POPULASI:
            populasi_baru.append(anak2)

    return populasi_baru

# PROSES UTAMA GENETIC ALGORITHM

def jalankan_genetic_algorithm():
    populasi = inisialisasi_populasi()

    kromosom_terbaik = None
    nilai_terbaik = float("inf")

    jumlah_stagnan = 0
    generasi_terakhir = 0

    for generasi in range(1, MAKS_GENERASI + 1):
        fitness, nilai_objektif = hitung_fitness(populasi)

        # Cari individu valid terbaik pada generasi sekarang.
        kandidat_valid = []

        for i in range(len(populasi)):
            if nilai_objektif[i] is not None:
                kandidat_valid.append((nilai_objektif[i], populasi[i]))

        if kandidat_valid:
            nilai_generasi, kromosom_generasi = min(
                kandidat_valid,
                key=lambda item: item[0]
            )

            # Perbarui solusi terbaik sepanjang evolusi.
            if nilai_generasi < nilai_terbaik:
                nilai_terbaik = nilai_generasi
                kromosom_terbaik = kromosom_generasi
                jumlah_stagnan = 0
            else:
                jumlah_stagnan += 1
        else:
            jumlah_stagnan += 1

        generasi_terakhir = generasi

        # Tampilkan perkembangan setiap 25 generasi.
        if generasi == 1 or generasi % 25 == 0:
            if kromosom_terbaik is not None:
                print(
                    "Generasi:", generasi,
                    "| Nilai terbaik:", format(nilai_terbaik, ".8f")
                )
            else:
                print("Generasi:", generasi, "| Belum ada kandidat valid")

        # Periksa kondisi berhenti karena stagnasi.
        if jumlah_stagnan >= BATAS_STAGNAN:
            print("\nBerhenti karena tidak ada perbaikan selama",
                  BATAS_STAGNAN, "generasi.")
            break

        # Periksa kondisi berhenti karena maksimum generasi.
        if generasi == MAKS_GENERASI:
            print("\nBerhenti karena mencapai maksimum generasi.")
            break

        # Bentuk generasi berikutnya.
        populasi = pergantian_generasi(populasi, fitness)

    # OUTPUT HASIL TERBAIK

    print("\n HASIL GENETIC ALGORITHM ")
    print("Random seed             :", RANDOM_SEED)
    print("Ukuran populasi         :", UKURAN_POPULASI)
    print("Panjang kromosom        :", PANJANG_KROMOSOM, "bit")
    print("Tournament size         :", UKURAN_TOURNAMENT)
    print("Probabilitas crossover  :", PROB_CROSSOVER)
    print("Probabilitas mutasi     :", PROB_MUTASI)
    print("Jumlah elit             :", JUMLAH_ELIT)
    print("Generasi dijalankan     :", generasi_terakhir)

    if kromosom_terbaik is not None:
        x1, x2 = decode(kromosom_terbaik)
        nilai_akhir = fungsi_objektif(x1, x2)

        print("\nKromosom terbaik       :", kromosom_terbaik)
        print("Gen untuk x1           :", kromosom_terbaik[:PANJANG_GEN])
        print("Gen untuk x2           :", kromosom_terbaik[PANJANG_GEN:])
        print("Nilai x1 hasil decode  :", format(x1, ".10f"))
        print("Nilai x2 hasil decode  :", format(x2, ".10f"))
        print("Nilai fungsi           :", format(nilai_akhir, ".12f"))
    else:
        print("Tidak ditemukan kandidat valid.")

# Jalankan program utama.
if __name__ == "__main__":
    jalankan_genetic_algorithm()

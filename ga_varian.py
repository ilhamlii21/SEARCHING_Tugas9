"""
Case Based - Searching | VARIAN 3
Minimasi f(x1,x2) = -( sin(x1) cos(x2) tan(x1+x2) + 1/2 exp(1 - sqrt(x2^2)) )
domain -10 <= x1, x2 <= 10

Ciri varian ini:
 - Populasi 74, kromosom REAL-CODED: [g1, g2], tiap gen bilangan real di [0,1]
 - Decode: x = batas_bawah + g * (batas_atas - batas_bawah)
 - Pemilihan orangtua: Roulette Wheel dengan fitness terkompresi logaritma
 - Crossover: Arithmetic (whole) | Mutasi: Gaussian
 - Pergantian generasi: generational + elitisme 5% (4 individu)
 - Berhenti: f mencapai target, ATAU maks generasi, ATAU stagnan
Modul 'random' dan 'math' hanya untuk bilangan acak & fungsi matematika dasar.
"""
import math
import random

# ======================= PARAMETER GA =======================
UKURAN_POPULASI = 74
JUMLAH_GEN      = 2        # panjang kromosom: 1 gen untuk x1, 1 gen untuk x2
BATAS_BAWAH     = -10.0
BATAS_ATAS      = 10.0
PC              = 0.75     # probabilitas crossover
PM              = 0.15     # probabilitas mutasi per gen
SIGMA_MUTASI    = 0.05     # simpangan baku mutasi Gaussian (skala gen 0..1)
JUMLAH_ELIT     = 4        # ~5% dari populasi
TARGET_F        = -1e6     # kriteria berhenti 1: f(x) sudah <= target
MAKS_GENERASI   = 250      # kriteria berhenti 2
MAKS_STAGNAN    = 40       # kriteria berhenti 3
SEED            = None


def fungsi_objektif(x1, x2):
    return -(math.sin(x1) * math.cos(x2) * math.tan(x1 + x2)
             + 0.5 * math.exp(1 - math.sqrt(x2 ** 2)))


# ======================= 1. INISIALISASI =======================
def inisialisasi_populasi(ukuran):
    """Tiap individu = [g1, g2], bilangan real acak di [0,1]."""
    return [[random.random() for _ in range(JUMLAH_GEN)] for _ in range(ukuran)]


# ======================= 2. DEKODE =======================
def dekode(kromosom):
    """Petakan gen [0,1] ke domain [-10,10]."""
    x1 = BATAS_BAWAH + kromosom[0] * (BATAS_ATAS - BATAS_BAWAH)
    x2 = BATAS_BAWAH + kromosom[1] * (BATAS_ATAS - BATAS_BAWAH)
    return x1, x2


# ======================= 3. FITNESS =======================
def hitung_nilai_f(kromosom):
    x1, x2 = dekode(kromosom)
    return fungsi_objektif(x1, x2)


def hitung_fitness_populasi(populasi):
    """g = -f (maksimasi). Karena g bisa sangat besar (tan mendekati asimtot),
    g digeser agar >= 0 lalu dikompres: fitness = ln(1 + g - g_min).
    Supaya satu individu ekstrem tidak menguasai seluruh roda roulette."""
    g = [-hitung_nilai_f(k) for k in populasi]
    g_min = min(g)
    return [math.log(1 + gi - g_min) + 1e-9 for gi in g], g


# ======================= 4. PEMILIHAN ORANGTUA =======================
def seleksi_roulette(populasi, fitness):
    """Roulette wheel: peluang terpilih proporsional dengan fitness."""
    total = sum(fitness)
    r = random.uniform(0, total)
    kumulatif = 0.0
    for individu, f in zip(populasi, fitness):
        kumulatif += f
        if r <= kumulatif:
            return individu
    return populasi[-1]


# ======================= 5. CROSSOVER =======================
def crossover_aritmatika(p1, p2):
    """Whole arithmetic crossover: anak = a*p1 + (1-a)*p2, a acak di [0,1]."""
    if random.random() < PC:
        a = random.random()
        c1 = [a * p1[i] + (1 - a) * p2[i] for i in range(JUMLAH_GEN)]
        c2 = [(1 - a) * p1[i] + a * p2[i] for i in range(JUMLAH_GEN)]
        return c1, c2
    return p1[:], p2[:]


# ======================= 6. MUTASI =======================
def mutasi_gaussian(kromosom):
    """Tambah derau Gaussian pada tiap gen (peluang PM), lalu batasi ke [0,1]."""
    hasil = []
    for g in kromosom:
        if random.random() < PM:
            g += random.gauss(0, SIGMA_MUTASI)
        hasil.append(min(1.0, max(0.0, g)))
    return hasil


# ======================= 7. PERGANTIAN GENERASI =======================
def ganti_generasi(populasi, fitness):
    """Generational + elitisme: JUMLAH_ELIT terbaik disalin, sisanya anak baru."""
    urut = sorted(range(len(populasi)), key=lambda i: fitness[i], reverse=True)
    baru = [populasi[i][:] for i in urut[:JUMLAH_ELIT]]
    while len(baru) < len(populasi):
        p1 = seleksi_roulette(populasi, fitness)
        p2 = seleksi_roulette(populasi, fitness)
        c1, c2 = crossover_aritmatika(p1, p2)
        baru.append(mutasi_gaussian(c1))
        if len(baru) < len(populasi):
            baru.append(mutasi_gaussian(c2))
    return baru


# ======================= PROGRAM UTAMA =======================
def jalankan_ga():
    if SEED is not None:
        random.seed(SEED)
    populasi = inisialisasi_populasi(UKURAN_POPULASI)
    terbaik, f_terbaik, stagnan = None, float("inf"), 0

    for gen in range(1, MAKS_GENERASI + 1):
        fitness, g = hitung_fitness_populasi(populasi)
        idx = max(range(len(populasi)), key=lambda i: g[i])
        f_gen = -g[idx]
        if f_gen < f_terbaik:
            f_terbaik, terbaik, stagnan = f_gen, populasi[idx][:], 0
        else:
            stagnan += 1

        if gen == 1 or gen % 10 == 0:
            print(f"Generasi {gen:3d} | f(x) terbaik = {f_terbaik:.6f}")
        if f_terbaik <= TARGET_F:
            print(f"Berhenti di generasi {gen}: target f <= {TARGET_F:g} tercapai.")
            break
        if stagnan >= MAKS_STAGNAN:
            print(f"Berhenti di generasi {gen}: stagnan {MAKS_STAGNAN} generasi.")
            break

        populasi = ganti_generasi(populasi, fitness)
    return terbaik


if __name__ == "__main__":
    best = jalankan_ga()
    x1, x2 = dekode(best)
    print("\n=========== HASIL ===========")
    print(f"Kromosom terbaik : [{best[0]:.8f}, {best[1]:.8f}]")
    print(f"Hasil dekode     : x1 = {x1:.6f} , x2 = {x2:.6f}")
    print(f"Nilai f(x1,x2)   : {fungsi_objektif(x1, x2):.6f}")

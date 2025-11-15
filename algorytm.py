
_seed = 123456789 
def set_seed(s):
    global _seed
    _seed = s

def pseudo_random():
   
    global _seed
    
    a = 1103515245
    c = 12345
    m = 2**31
    _seed = (a * _seed + c) % m
    return _seed / m

def randint(a, b):
   
    return a + int(pseudo_random() * (b - a + 1))



# === Fitness (ocena osobnika) ===
def ocena(chromosom, przedmioty, pojemnosc):
    waga = 0
    wartosc = 0
    for gen, (waga_i, wartosc_i) in zip(chromosom, przedmioty):
        if gen == 1:
            waga += waga_i
            wartosc += wartosc_i
    if waga > pojemnosc:
        return 0  # kara za przekroczenie pojemności
    return wartosc


# === Krzyżowania ===
def krzyzowanie_jednopunktowe(p1, p2):
    punkt = randint(1, len(p1) - 1)
    dziecko1 = p1[:punkt] + p2[punkt:]
    dziecko2 = p2[:punkt] + p1[punkt:]
    return dziecko1, dziecko2

def krzyzowanie_dwupunktowe(p1, p2):
    n = len(p1)
    punkt1 = randint(1, n - 2)
    punkt2 = randint(punkt1 + 1, n - 1)
    dziecko1 = p1[:punkt1] + p2[punkt1:punkt2] + p1[punkt2:]
    dziecko2 = p2[:punkt1] + p1[punkt1:punkt2] + p2[punkt2:]
    return dziecko1, dziecko2

def krzyzowanie_jednorodne(p1, p2):
    dziecko1, dziecko2 = [], []
    for g1, g2 in zip(p1, p2):
        if pseudo_random() < 0.5:
            dziecko1.append(g1)
            dziecko2.append(g2)
        else:
            dziecko1.append(g2)
            dziecko2.append(g1)
    return dziecko1, dziecko2


# === Mutacja ===
def mutacja(chromosom, p_mutacji=0.01):
    for i in range(len(chromosom)):
        if pseudo_random() < p_mutacji:
            chromosom[i] = 1 - chromosom[i]
    return chromosom


# === Selekcje ===
def selekcja_ruletkowa(populacja, oceny):
    suma = sum(oceny)
    if suma == 0:
        return populacja[randint(0, len(populacja) - 1)]
    wybor = pseudo_random() * suma
    akum = 0.0
    for osobnik, fit in zip(populacja, oceny):
        akum += fit
        if akum >= wybor:
            return osobnik
    return populacja[-1]

def selekcja_rankingowa(populacja, oceny):
    # sort wg fitness rosnąco
    posortowane = sorted(zip(oceny, populacja), key=lambda x: x[0])
    rangi = list(range(1, len(populacja) + 1))  # 1..N
    suma = sum(rangi)
    wybor = pseudo_random() * suma
    akum = 0
    for ranga, (fit, osobnik) in zip(rangi, posortowane):
        akum += ranga
        if akum >= wybor:
            return osobnik
    return posortowane[-1][1]

def selekcja_turniejowa(populacja, oceny, rozmiar_turnieju=2):
    najlepiej_fit = None
    najlepszy_os = None
    for _ in range(rozmiar_turnieju):
        idx = randint(0, len(populacja) - 1)
        fit = oceny[idx]
        if (najlepiej_fit is None) or (fit > najlepiej_fit):
            najlepiej_fit = fit
            najlepszy_os = populacja[idx]
    return najlepszy_os


# === Narzędzia pomocnicze ===
def inicjalizuj_populacje(n_osobnikow, dlugosc):
    return [[randint(0, 1) for _ in range(dlugosc)] for _ in range(n_osobnikow)]

def wybierz_selekcje(metoda):
    if metoda == "ruletka":
        return selekcja_ruletkowa
    if metoda == "ranking":
        return selekcja_rankingowa
    return selekcja_turniejowa  # domyślnie turniej

def wybierz_krzyzowanie(metoda):
    if metoda == "jedno":
        return krzyzowanie_jednopunktowe
    if metoda == "uniform":
        return krzyzowanie_jednorodne
    return krzyzowanie_dwupunktowe  # domyślnie dwupunktowe


# === Główny algorytm genetyczny ===
def algorytm_genetyczny(
    przedmioty,
    pojemnosc,
    liczba_pokolen=100,
    rozmiar_populacji=50,
    p_mutacji=0.05,
    p_krzyzowania=0.8,
    metoda_selekcji="turniej",     # "turniej" | "ruletka" | "ranking"
    metoda_krzyzowania="dwupunkt"  # "dwupunkt" | "jedno" | "uniform"
):
    dlugosc = len(przedmioty)
    populacja = inicjalizuj_populacje(rozmiar_populacji, dlugosc)

    najlepszy = None
    najlepsza_ocena = -1

    selektor = wybierz_selekcje(metoda_selekcji)
    crossover = wybierz_krzyzowanie(metoda_krzyzowania)

    for _ in range(liczba_pokolen):
        oceny = [ocena(os, przedmioty, pojemnosc) for os in populacja]

        # aktualizacja najlepszego osobnika
        for os, fit in zip(populacja, oceny):
            if fit > najlepsza_ocena:
                najlepsza_ocena = fit
                najlepszy = os[:]

        # tworzenie nowej populacji
        nowa_populacja = []
        while len(nowa_populacja) < rozmiar_populacji:
            # selekcja rodziców
            rodzic1 = selektor(populacja, oceny) if selektor != selekcja_turniejowa else selekcja_turniejowa(populacja, oceny)
            rodzic2 = selektor(populacja, oceny) if selektor != selekcja_turniejowa else selekcja_turniejowa(populacja, oceny)

            # krzyżowanie
            if pseudo_random() < p_krzyzowania:
                dziecko1, dziecko2 = crossover(rodzic1, rodzic2)
            else:
                dziecko1, dziecko2 = rodzic1[:], rodzic2[:]

            # mutacja
            dziecko1 = mutacja(dziecko1, p_mutacji)
            dziecko2 = mutacja(dziecko2, p_mutacji)

            nowa_populacja.append(dziecko1)
            if len(nowa_populacja) < rozmiar_populacji:
                nowa_populacja.append(dziecko2)

        populacja = nowa_populacja

    return {
        "najlepszy_osobnik": najlepszy,
        "najlepsza_wartosc": najlepsza_ocena
    }

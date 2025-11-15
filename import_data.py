def data_dynamic(filename):
    items = []
    sorce = open(filename, "r")
    first_line = sorce.readline().strip()
    split_line = first_line.split()
    n = int(split_line[0])
    capacity = int(split_line[1])

    for line in range(n):
        current_line = sorce.readline().strip()
        split_line = current_line.split()
        weight = int(split_line[0])
        value = int(split_line[1])
        items.append((weight, value))
    
    sorce.close()
    return n, capacity, items


def dynamic_backpack(n, capacity, items):
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        weight, value = items[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]

    chosen_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen_items.append(i - 1)
            w -= items[i - 1][0]
    chosen_items.reverse()
    
    
    return dp[n][capacity], chosen_items

   
# -------------------------------
# Algorytm genetyczny dla problemu plecakowego
# -------------------------------

seed = 42

def pseudo_random():
    global seed
    seed = (seed * 9301 + 49297) % 233280
    return seed / 233280.0

def randint(a, b):
    return int((b - a + 1) * pseudo_random() + a)

# Funkcja przystosowania dla plecaka
def fitness(chromosom, items, capacity):
    wartosc = 0
    for i in range(len(chromosom)):
        if chromosom[i] == 1:
            wartosc += items[i][1]
    return wartosc

# Funkcja naprawy osobnika – usuwa przedmioty aż waga ≤ capacity
def napraw_osobnik(chromosom, items, capacity):
    while True:
        waga = sum(items[i][0] for i in range(len(chromosom)) if chromosom[i] == 1)
        if waga <= capacity:
            break
        for i in range(len(chromosom)):
            if chromosom[i] == 1:
                chromosom[i] = 0
                break
    return chromosom

def selekcja(populacja, oceny):
    suma = sum(oceny)
    wybrane = []
    for _ in range(len(populacja)):
        prog = pseudo_random() * suma
        akumulacja = 0
        for i in range(len(populacja)):
            akumulacja += oceny[i]
            if akumulacja >= prog:
                wybrane.append(populacja[i])
                break
    return wybrane

def krzyzowanie(p1, p2):
    punkt = randint(1, len(p1) - 1)
    dziecko1 = p1[:punkt] + p2[punkt:]
    dziecko2 = p2[:punkt] + p1[punkt:]
    return dziecko1, dziecko2

def mutacja(chromosom, prawdopodobienstwo):
    for i in range(len(chromosom)):
        if pseudo_random() < prawdopodobienstwo:
            chromosom[i] = 1 - chromosom[i]
    return chromosom

def genetyczny_plecak(items, capacity, rozmiar_populacji, liczba_iteracji, prawdopodobienstwo_mutacji=0.01):
    n = len(items)
    populacja = []
    for _ in range(rozmiar_populacji):
        osobnik = [randint(0, 1) for _ in range(n)]
        osobnik = napraw_osobnik(osobnik, items, capacity)
        populacja.append(osobnik)

    najlepszy = populacja[0]
    najlepsza_ocena = fitness(najlepszy, items, capacity)

    for _ in range(liczba_iteracji):
        oceny = [fitness(os, items, capacity) for os in populacja]

        for i, ocena in enumerate(oceny):
            if ocena > najlepsza_ocena:
                najlepszy = populacja[i]
                najlepsza_ocena = ocena

        rodzice = selekcja(populacja, oceny)
        nowa_populacja = []
        for i in range(0, rozmiar_populacji, 2):
            p1 = rodzice[i % len(rodzice)]
            p2 = rodzice[(i + 1) % len(rodzice)]
            d1, d2 = krzyzowanie(p1, p2)
            d1 = mutacja(d1, prawdopodobienstwo_mutacji)
            d2 = mutacja(d2, prawdopodobienstwo_mutacji)
            d1 = napraw_osobnik(d1, items, capacity)
            d2 = napraw_osobnik(d2, items, capacity)
            nowa_populacja.extend([d1, d2])
        populacja = nowa_populacja[:rozmiar_populacji]

    return najlepszy, najlepsza_ocena

def krzyzowanie_jednopunktowe(p1, p2):
    n = len(p1)
    punkt = randint(1, n - 1)

    dziecko1 = p1[:punkt] + p2[punkt:]
    dziecko2 = p2[:punkt] + p1[punkt:]

    return dziecko1, dziecko2

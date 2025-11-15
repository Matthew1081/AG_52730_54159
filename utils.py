import csv
import pandas as pd
import matplotlib.pyplot as plt

def zapisz_wyniki(nazwa_pliku, wynik):
    with open(nazwa_pliku, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=wynik.keys())
        if f.tell() == 0:  # jeśli plik pusty, zapisz nagłówki
            writer.writeheader()
        writer.writerow(wynik)

def generuj_wykres(nazwa_pliku):
    dane = pd.read_csv(nazwa_pliku)

    # Tworzymy słupki obok siebie dla różnych wartości krzyżowania
    szerokosc = 0.03  # szerokość słupka
    mutacje = sorted(dane["mutacja"].unique())

    for i, krzyzowanie in enumerate(dane["krzyzowanie"].unique()):
        subset = dane[dane["krzyzowanie"] == krzyzowanie]
        plt.bar(
            subset["mutacja"] + (i - 0.5) * szerokosc,  # przesunięcie słupków
            subset["najlepsza_wartosc"],
            width=szerokosc,
            label=f"Krzyżowanie={krzyzowanie}"
        )

    plt.xlabel("Współczynnik mutacji")
    plt.ylabel("Najlepsza wartość")
    plt.title("Wpływ mutacji i krzyżowania na wynik algorytmu genetycznego")
    plt.legend()
    plt.grid(axis="y")
    plt.show()

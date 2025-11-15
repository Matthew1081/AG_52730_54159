import pandas as pd
import matplotlib.pyplot as plt

def generuj_wykres(plik):
    dane = pd.read_csv(plik)
    for krzyzowanie in dane["krzyzowanie"].unique():
        subset = dane[dane["krzyzowanie"] == krzyzowanie]
        plt.plot(subset["mutacja"], subset["najlepsza_wartosc"], marker='o', label=f"Krzyżowanie={krzyzowanie}")

    plt.xlabel("Mutacja")
    plt.ylabel("Najlepsza wartość")
    plt.title("Wpływ mutacji i krzyżowania na wynik")
    plt.legend()
    plt.grid(True)
    plt.show()

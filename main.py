from algorytm import algorytm_genetyczny
from utils import zapisz_wyniki, generuj_wykres

def main():
    # przykładowe dane plecakowe
    przedmioty = [(10, 60), (20, 100), (30, 120)]
    pojemnosc = 50

    # parametry globalne
    mutacja = 0.05
    krzyzowanie = 0.8
    liczba_pokolen = 50
    rozmiar_populacji = 20

    # wszystkie metody
    selekcje = ["turniej", "ruletka", "ranking"]
    krzyzowania = ["dwupunkt", "jedno", "uniform"]

    nazwa_pliku = "wyniki.csv"

    for selekcja in selekcje:
        for typ_krzyzowania in krzyzowania:
            wynik = algorytm_genetyczny(
                przedmioty,
                pojemnosc,
                liczba_pokolen=liczba_pokolen,
                rozmiar_populacji=rozmiar_populacji,
                p_mutacji=mutacja,
                p_krzyzowania=krzyzowanie,
                metoda_selekcji=selekcja,
                metoda_krzyzowania=typ_krzyzowania
            )

            # dodaj parametry do wyniku
            wynik["mutacja"] = mutacja
            wynik["krzyzowanie"] = krzyzowanie
            wynik["selekcja"] = selekcja
            wynik["krzyzowanie_typ"] = typ_krzyzowania

            # zapisz do pliku
            zapisz_wyniki(nazwa_pliku, wynik)

    print("Wszystkie wyniki zapisane do pliku", nazwa_pliku)

    # generowanie wykresu
    generuj_wykres(nazwa_pliku)

if __name__ == "__main__":
    main()

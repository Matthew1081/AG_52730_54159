from import_data import data

sciezka = r"C:\Users\mkwia\Desktop\dsw\algorytmy genetyczne i sztuczne sieci neuronowe\AG_52730_54159\large_scale\knapPI_2_200_1000_1.txt"
n, capacity, items = data(sciezka)

print("Liczba przedmiotów:", n)
print("Pojemność plecaka:", capacity)
print("Pierwsze 5 przedmiotów:", items[:5])

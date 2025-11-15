from import_data import data_dynamic, dynamic_backpack, genetyczny_plecak


sciezka = "large_scale\knapPI_2_200_1000_1.txt"
n, capacity, items = data_dynamic(sciezka)

print("Liczba przedmiotów:", n)
print("Pojemność plecaka:", capacity)
print("Pierwsze 5 przedmiotów:", items[:5])

max_value, chosen_items = dynamic_backpack(n, capacity, items)
print("Maksymalna wartość w plecaku:", max_value)
print("Wybrane przedmioty (indeksy):", chosen_items)
print("Wybrane przedmioty (waga, wartość):", [items[i] for i in chosen_items])
sum_value = 0
sum_weight = 0

for i in chosen_items: 
    veight, value = items[i]
    sum_value += value
    sum_weight += veight
print("Suma wag wybranych przedmiotów:", sum_weight)
print("Suma wartości wybranych przedmiotów:", sum_value)
print("Sprawdzenie poprawności sumy wartości:", "Poprawne" if sum_value == max_value else "Błąd")

najlepszy, wartosc = genetyczny_plecak(items, capacity, rozmiar_populacji=100, liczba_iteracji=500)

print("Najlepszy osobnik:", najlepszy)
print("Wartość:", wartosc)

suma_wagi = sum(items[i][0] for i in range(len(items)) if najlepszy[i] == 1)
suma_wartosci = sum(items[i][1] for i in range(len(items)) if najlepszy[i] == 1)

print("Suma wag wybranych przedmiotów:", suma_wagi)
print("Suma wartości wybranych przedmiotów:", suma_wartosci)
print("Czy mieści się w plecaku?", "Tak" if suma_wagi <= capacity else "Nie")

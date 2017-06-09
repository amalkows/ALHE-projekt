import copy
import csv

from src.mealfinder import MealFinder
from src.meal import Meal
from src.product import Product

class DietManager:
    product_list = [[], [], []]
    general_product_list = []
    meal_list = []

    nutrition_values_target = [0 for i in range(Meal.nutrition_values_count)]
    # Wyciągnąć na zewnątrz
    percent = [0.3, 0.5, 0.2]

    tabu = {}
    finder = MealFinder()

    def read_data_from_file(self, file_name):
        with open(file_name, 'r', encoding="ISO-8859-2") as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if not row[0].startswith('#'):
                    self.add_product(int(row[1]),
                                     Product(
                                         row[0],                                                        #Nazwa
                                         list(map(float, row[2:2 + Meal.nutrition_values_count])),      #Wartosci odzywcze
                                         int(row[2 + Meal.nutrition_values_count]),                     #Tabu
                                         float(row[2 + Meal.nutrition_values_count + 1]),               #Rozdzielczość wagowa
                                         int(row[2 + Meal.nutrition_values_count + 2]),                 #Minimalna waga
                                         int(row[2 + Meal.nutrition_values_count + 3]),                 #Maksymalna waga
                                         int(row[2 + Meal.nutrition_values_count + 4])                  #Waga
                                     ))



    # dodawanie produktów
    def add_product(self, meal, product):
        if meal > 2:
            self.general_product_list.append(product)
        else:
            product.tabu_time *= 3
            self.product_list[meal].append(product)

    def generate_n_days_diet(self, n):
        for x in range(n):
            day_meal = []
            # odchył od norm
            delta = [0 for i in range(Meal.nutrition_values_count)]
            # generacja dla każdego posiłku w ciągu dnia
            for meal_number in [0, 1, 2]:
                # Przygotowanie listy produktów
                list = self.product_list[meal_number] + self.general_product_list
                list = [item for item in list if self.tabu.get(item.name) is None]

                # Przeliczenie ile wartości odzywczych ma miec nastepny posilek
                target_values = [x * self.percent[meal_number] for x in self.nutrition_values_target]
                target_values = [x - y for x, y in zip(target_values, delta)]
                for i in range(0, len(target_values)):
                    if (target_values[i] < 0):
                        target_values[i] = 0

                # Znalezienie posilku i zapisanie go
                result = self.finder.find_meal(list, target_values)
                result.target_values = copy.copy(target_values)
                day_meal.append(result)

                # Policzenie odchylu od zadanych wartosci
                delta = [x - y for x, y in zip(result.nutrition_values, target_values)]

                # Aktualizacja tabu - decrementacja licznikow, czyszczenie, dodanie nowych
                # lista posiłków do usunięcia z tabu
                meal_to_delte_from_tabu = []
                for x in self.tabu.keys():
                    self.tabu[x] -= 1
                    if self.tabu[x] <= 0:
                        meal_to_delte_from_tabu.append(x)

                # usunięcie z tabu posiłków
                for k in meal_to_delte_from_tabu:
                    del self.tabu[k]

                for x in result.products:
                    self.tabu[x.name] = x.tabu_time

            self.meal_list.append(day_meal)

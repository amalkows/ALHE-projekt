import copy

from src.mealfinder import MealFinder
from src.meal import Meal

class DietManager:


    product_list = [[], [], []]
    general_product_list = []
    meal_list = []

    nutrition_values_target = [0 for i in range(Meal.nutrition_values_count)]
    #Wyciągnąć na zewnątrz
    percent = [0.3, 0.5, 0.2]

    tabu = {}
    finder = MealFinder()

    #dodawanie produktów
    def add_product(self, meal, product):
        if meal > 2:
            self.general_product_list.append(product)
        else:
            self.product_list[meal].append(product)

    def generate_n_days_diet(self, n):
        for x in range(n):
            day_meal = []
            #odchył od norm
            delta = [0 for i in range(Meal.nutrition_values_count)]
            #generacja dla każdego posiłku w ciągu dnia
            for meal_number in [0,1,2]:
                #Przygotowanie listy produktów
                list = self.product_list[meal_number] + self.general_product_list
                list = [item for item in list if self.tabu.get(item.name) is None]

                #Przeliczenie ile wartości odzywczych ma miec nastepny posilek
                target_values = [x * self.percent[meal_number] for x in self.nutrition_values_target]
                target_values = [x - y for x, y in zip(target_values, delta)]

                #Znalezienie posilku i zapisanie go
                result = self.finder.find_meal(list, target_values)
                result.target_values = copy.copy(target_values)
                day_meal.append(result)

                #Policzenie odchylu od zadanych wartosci
                delta = [x - y for x, y in zip(result.nutrition_values, target_values)]

                #Aktualizacja tabu - decrementacja licznikow, czyszczenie, dodanie nowych
                #lista posiłków do usunięcia z tabu
                meal_to_delte_from_tabu = []
                for x in self.tabu.keys():
                    self.tabu[x] -= 1
                    if self.tabu[x] == 0:
                        meal_to_delte_from_tabu.append(x)

                #usunięcie z tabu posiłków
                for k in meal_to_delte_from_tabu:
                    del self.tabu[k]

                for x in result.products:
                    self.tabu[x.name] = x.tabu_time

            self.meal_list.append(day_meal)
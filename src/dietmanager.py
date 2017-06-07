from src.mealfinder import MealFinder


class DietManager:

    product_list = [[], [], []]
    general_product_list = []
    meal_list = []

    nutrion_values_target = [0, 0]
    percent = [0.3, 0.5, 0.2]

    tabu = {}
    finder = MealFinder()

    def add_product(self, meal, product):
        if meal > 2:
            self.general_product_list.append(product)
        else:
            self.product_list[meal].append(product)

    def generate_n_days_diet(self, n):
        for x in range(n):
            day_meal = []
            delta = [0, 0, 0]
            for meal_number in [0,1,2]:
                #Przygotowanie listy produktów
                list = self.product_list[meal_number] + self.general_product_list
                list = [item for item in list if self.tabu.get(item.name) is None]         # DO ZMIANY USUWANIE Z LISTY PRODUKTOW, POROWNYWAC PO NAZWIE, NIE REFERENCJI

                #Przeliczenie ile wartości odzywczych ma miec nastepny posilek
                target_values = [x * self.percent[meal_number] for x in self.nutrion_values_target]
                target_values = [x - y for x, y in zip(target_values, delta)]

                #Znalezienie posilku i zapisanie go
                result = self.finder.find_meal(list, target_values)
                day_meal.append(result)

                #Policzenie odchylu od zadanych wartosci
                delta = [x - y for x, y in zip(result.nutrion_values, target_values)]

                #Aktualizacja tabu - decrementacja licznikow, czyszczenie, dodanie nowych
                to_delete = []
                for x in self.tabu.keys():
                    self.tabu[x] -= 1
                    if self.tabu[x] == 0:
                        to_delete.append(x)

                for k in to_delete:
                    del self.tabu[k]

                for x in result.products:
                    self.tabu[x.name] = x.tabu_time

            self.meal_list.append(day_meal)
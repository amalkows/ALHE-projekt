from src.meatfinder import MeatFinder


class DietManager:

    breakfast_product_list = []
    dinner_product_list = []
    supper_product_list = []
    general_product_list = []
    meal_list = []

    nutrion_values_target = [0, 0]
    breakfast_percent = 0.3
    dinner_percent = 0.5
    supper_percent = 0.2

    tabu = {}
    finder = MeatFinder()

    def add_product(self, meal, product):
        if meal == 0:
            self.breakfast_product_list.append(product)
        elif meal == 1:
            self.dinner_product_list.append(product)
        elif meal == 2:
            self.supper_product_list.append(product)
        else:
            self.general_product_list.append(product)

    def generate_n_days_diet(self, n):
        for x in range(n):
            day_meal = []

            #SNIADANIE
            list = self.breakfast_product_list + self.general_product_list
            list = [item for item in list if item not in self.tabu]
            target_values = [x * self.breakfast_percent for x in self.nutrion_values_target]
            result = self.finder.find_meal(list, target_values)
            day_meal.append(result)

            delta = [x - y for x, y in zip(result.nutrion_values, target_values)]

            toDelete = []
            for x in self.tabu.keys():
                self.tabu[x] -= 1
                if self.tabu[x] == 0:
                    toDelete.append(x)

            for k in toDelete:
                del self.tabu[k]

            for x in result.products:
                self.tabu[x] = x.tabu_time

            #OBIAD...
            #KOLACJA...
            self.meal_list.append(day_meal)

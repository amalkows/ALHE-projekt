import copy


class Meal:
    def __init__(self, products=[]):
        self.products = copy.deepcopy(products)
        self.nutrition_values = []
        self.calculate_nutrition_values()
        self.target_values = []
        self.target_function_value = -1

    def calculate_nutrition_values(self):
        self.nutrition_values = [0 for i in range(Meal.nutrition_values_count)]
        for product in self.products:
            self.nutrition_values = [x * product.weight * product.weight_resolution + y for x, y in zip(product.nutrition_values, self.nutrition_values)]
        return self.nutrition_values

    @staticmethod
    def set_standard_weights():
        Meal.nutrition_weights = [1 for i in range(Meal.nutrition_values_count)]

    max_products = 10
    nutrition_values_count = 4
    nutrition_weights = [1 for i in range(nutrition_values_count)]


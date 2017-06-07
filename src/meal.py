import copy

class Meal:
    def __init__(self, products = []):
        self.products = copy.deepcopy(products)
        self.nutrition_values = [0, 0]

        for product in products:
            self.nutrition_values = [x * product.weight * product.weight_resolution + y for x, y in zip(product.nutrition_values, self.nutrition_values)]

    def calculate_nutrition_values(self):
        self.nutrition_values = [0, 0]
        for product in self.products:
            self.nutrition_values = [x * product.weight * product.weight_resolution + y for x, y in zip(product.nutrition_values, self.nutrition_values)]
        return self.nutrition_values

    max_products = 10
    nutrition_weights = [1, 1]
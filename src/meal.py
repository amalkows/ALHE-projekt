import copy

class Meal:
    def __init__(self, products = []):
        self.products = copy.deepcopy(products)
        self.nutrion_values = [0, 0]

        for product in products:
            self.nutrion_values = [x * product.weight * product.weight_resolution + y for x, y in zip(product.nutrion_values, self.nutrion_values)]

    def calculate_nutrion_values(self):
        self.nutrion_values = [0, 0]
        for product in self.products:
            self.nutrion_values = [x * product.weight * product.weight_resolution + y for x, y in zip(product.nutrion_values, self.nutrion_values)]
        return self.nutrion_values


    max_products = 10
    nutrion_wieghts = [1, 1]
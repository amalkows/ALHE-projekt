class Meal:
    def __init__(self, products = []):
        self.products = products

        for product in products:
            self.nutrion_values = [x + y for x, y in zip(product.nutrion_values, self.nutrion_values)]

    products = []
    nutrion_values = [0, 0]
    max_products = 10
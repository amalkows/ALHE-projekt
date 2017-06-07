from src.product import Product
from src.meal import Meal
from random import uniform
import copy
import random

#    def __init__(self, name="", nutrition_values=[0], tabu_time=1, weight_resolution=1, min_weight=1,
#                 max_weight=10, weight=1):

class DataGenerator:

    max_nutrion_value_kal_per_g = 100
    max_nutrion_value_per_g = 10
    min_tabu_time = 1
    max_tabu_time = 10
    avg_tabu_time = 4
    sigma_tabu_time = 3

    max_weight_resolution = 500
    avg_weight_resolution = 100
    sigma_weight_resolution = 50

    max_min_weight = 10

    min_max_weight = 1
    max_max_weight = 300

    generated_items = 0;

    def generate_product(self):
        self.generated_items += 1
        return Product(str(self.generated_items),
                       [random.randint(1, self.max_nutrion_value_kal_per_g)]+
                       [random.randint(1, self.max_nutrion_value_per_g) for value in range(Meal.nutrition_values_count)],
                       round(min(self.max_tabu_time, max(self.min_tabu_time, random.gauss(self.avg_tabu_time, self.sigma_tabu_time)))),
                       round(min(self.max_weight_resolution,
                           max(0, random.gauss(self.avg_weight_resolution, self.sigma_weight_resolution)))),
                       random.randint(1, self.max_min_weight),
                       random.randint(self.min_max_weight, self.max_max_weight)
                       )

import copy

class Product:
    def __init__(self, name = "", nutrion_values=[0,0], tabu_time = 1):
        self.name = name
        self.nutrion_values = nutrion_values
        self.tabu_time = tabu_time * 3
        self.weight = 5

    def correct_weight(self, weight):
        if weight >= self.min_weight and weight <= self.max_weight:
            self.weight = weight
        elif weight < self.min_weight:
            self.weight = self.min_weight
        elif weight > self.max_weight:
            self.weight = self.max_weight

    weight_resolution = 1
    min_weight = 1
    max_weight = 10

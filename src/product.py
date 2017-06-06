import copy

class Product:
    def __init__(self, name = "", nutrion_values=[0,0], tabu_time = 1):
        self.name = name
        self.nutrion_values = nutrion_values
        self.tabu_time = tabu_time * 3
        self.weight = 5


    weight_resolution = 1
    min_weight = 1
    max_weight = 10

class Product:
    def __init__(self, name = "", nutrion_values=[], tabu_time = 1):
        self.name = name
        self.nutrion_values = nutrion_values
        self.tabu_time = tabu_time * 3


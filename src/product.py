class Product:
    def __init__(self, name="", nutrion_values=[0,0], tabu_time=1, weight_resolution=1, min_weight=1,
                 max_weight=10, weight=1):
        self.name = name
        self.nutrion_values = nutrion_values
        self.tabu_time = tabu_time * 3
        self.weight = weight
        self.weight_resolution = weight_resolution
        self.min_weight = min_weight
        self.max_weight = max_weight

    # funkcja służąca do naprawy wagi, by mieściła się w widelkach
    def correct_weight(self, weight):
        if weight >= self.min_weight and weight <= self.max_weight:
            self.weight = weight
        elif weight < self.min_weight:
            self.weight = self.min_weight
        elif weight > self.max_weight:
            self.weight = self.max_weight


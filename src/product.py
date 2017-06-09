class Product:
    def __init__(self, name="", nutrition_values=[0], tabu_time=1, weight_resolution=1, min_weight=1,
                 max_weight=10, weight=1):
        self.name = name
        self.nutrition_values = nutrition_values
        self.tabu_time = tabu_time * 3
        self.weight_resolution = weight_resolution
        self.min_weight = min_weight
        self.max_weight = max_weight
        if min_weight > max_weight:
            self.max_weight = min_weight
            self.min_weight = max_weight
        self.correct_weight(weight)

    # funkcja służąca do naprawy wagi, by mieściła się w widelkach
    def correct_weight(self, weight):
        if self.min_weight <= weight <= self.max_weight:
            self.weight = weight
        elif weight < self.min_weight:
            self.weight = self.min_weight
        else:
            self.weight = self.max_weight

    def get_max_weight(self,nutrition_index,nutrition_weight):
        if self.min_weight*self.weight_resolution*self.nutrition_values[nutrition_index] <= nutrition_weight :
            for i in range(self.max_weight,self.min_weight -1, -1):
                if i*self.weight_resolution*self.nutrition_values[nutrition_index] <= nutrition_weight :
                    return i
        else:
            return 0


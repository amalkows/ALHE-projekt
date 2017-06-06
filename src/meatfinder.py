from src.meal import Meal

class MeatFinder:
    iteration_count = 100
    population_size = 50
    always_in_next_population = 10

    population = []

    def calculate_target_function(self, meal):
        return 0

    def selection(self):
        return self.population

    def mutation(self, population):
        return population

    def cross(self, population):
        return population

    def generate_start_solutions(self, product_list):
        return [Meal([product_list[0], product_list[1]])]

    def generate_new_population(self, mutated_population):
        return mutated_population

    def find_meal(self, product_list, nutrionTarget):
        self.population = self.generate_start_solutions(product_list)

        for i in range(self.iteration_count):
            selcted_population = self.selection()
            crossed = self.cross(selcted_population)
            mutated = self.mutation(crossed)

            self.population = self.generate_new_population(mutated)

        return self.population[0]
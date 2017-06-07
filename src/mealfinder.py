from src.meal import Meal
from collections import Counter
from random import uniform, randint
from src.product import Product
import copy
import random


# TODO!!!!! UWZGLEDNIC MAKS K PRODUKTOW W POSILKU (parametr max_producs z meal.py)
class MealFinder:
    iteration_count = 50
    population_size = 15
    # elita
    always_in_next_population = 5

    # w przypadku krzyżowania każdy produkt w posiłku może zamienić typ z produktem z innego posiłku
    # prawdopodobieństwo krzyżowania
    p_cross = 15
    # prawdopodobieństwo zmiany typu w przypadku krzyżowania
    p_cross_product_type = 5

    # na każdym prodkucie w ramach posiłku (wybieramy jeden z trzech rodzajów mutacji)
    p_mutate_type = 5
    p_mutate_weight = 15
    p_mutate_delete_element = 5

    # prawdopodobieństwo dodania posiłku
    p_mutate_add_element = 15

    # słownik: [klucz] referencja do obiektu - [wartość] jakość (funkcja celu)
    population = {}

    nutrion_target = []
    product_list = []

    def calculate_target_function(self, meal):
        result = 0
        weights_sum = 0
        for x, y, z in zip(meal.nutrion_values, meal.nutrion_wieghts, self.nutrion_target):
            result += ((x - z) ** 2) * y
            weights_sum += y

        return result / weights_sum

    # TODO - trzeba ustalić, ile selekcja będzie zwracać osobników
    def selection(self):
        selected_points = []
        sum_of_target_fuction = 0
        probabilities = [0]
        for target_fuction in self.population.values():
            sum_of_target_fuction += 1 / target_fuction
        for i in range(0, len(self.population)):
            probabilities.append(probabilities[i] + sum_of_target_fuction / target_fuction)
        probabilities[len(probabilities)-1] = 1;
        print(probabilities)
        for i in range(0, self.population_size):
            random_number = uniform(0, 1)
            for i in range(1,len(probabilities)):
                if probabilities[i] <= random_number:
                    selected_points.append(self.population[i-1])
                    break
        return selected_points

    def mutation(self, population):
        new_population = []
        for item in population:
            new_population.append(self.mutate_element(item))
        return new_population

    def mutate_element(self, element):
        mutated_products = []
        mutated_type_products_list = [item.name for item in element.products]
        for product in element.products:
            random_number = uniform(0, 100)
            if random_number < self.p_mutate_type:
                mutated_products.append(self.mutate_type_element(product, mutated_type_products_list))
            elif random_number < self.p_mutate_type + self.p_mutate_weight:
                mutated_products.append(self.mutate_weight_element(product))
            elif random_number < 100 - self.p_mutate_delete_element:
                mutated_products.append(copy.deepcopy(product))

        if uniform(0, 100) < self.p_mutate_add_element:
            new_meal = self.mutate_add_element(mutated_products)
            if new_meal is not None:
                mutated_products.append(new_meal)

        new_element = Meal(mutated_products)
        new_element.calculate_nutrion_values()

        return new_element

    def mutate_weight_element(self, element):

        new_element = copy.deepcopy(element)
        # wykorzystać correct_weight
        random_number = random.randint(0, 1)
        if random_number == 0 and new_element.weight > new_element.min_weight:
            new_element.weight -= 1
        elif random_number == 1 and new_element.weight < new_element.max_weight:
            new_element.weight += 1

        return new_element

    def mutate_add_element(self, mutated_products):
        list = [item for item in self.product_list if
                next((i for i in mutated_products if i.name == item.name), None) is None]

        if len(list) == 0:
            return None

        index = random.randint(0, len(list) - 1)
        product = copy.deepcopy(list[index])

        return product

    def mutate_type_element(self, product, mutated_type_products_list):

        available_types = [item for item in self.product_list if
                           next((i for i in mutated_type_products_list if i == item.name), None) is None]

        if len(available_types) == 0:
            return copy.deepcopy(product)

        index = random.randint(0, len(available_types) - 1)

        new_element = copy.deepcopy(available_types[index])

        new_element.correct_weight(product.weight)

        for i in mutated_type_products_list:
            if i == product.name:
                i = available_types[index].name
                break

        return new_element

    def cross(self, population):
        # return population
        new_population = []
        for item in population:
            item_cross = uniform(0, 100)
            if item_cross < self.p_cross:
                index = random.randint(0, len(
                    population) - 1)  # losuje ziomka do krzyżowania TODO zrobić tak, żeby nie było samogwałtu
                new_population.append(self.cross_element(item, population[index]))
            else:
                new_population.append(item)

        return new_population

    def cross_element(self, meal1, meal2):
        new_meal = copy.deepcopy(meal1)
        # parametr pomocniczy (sumowanie ziemniaczków)
        product_uses = {}

        for product in new_meal.products:
            if uniform(0, 100) < self.p_cross_product_type:
                self.cross_element_type(product, meal2.products[random.randint(0, len(meal2.products) - 1)])

            if product_uses.get(product.name, None) is None:
                product_uses[product.name] = product
            else:
                product_uses[product.name].correct_weight(product_uses[product.name].weight + product.weight)

        new_meal.products = product_uses.values()

        return new_meal

    # działa, ale pomyśleć nad refaktoryzacją
    def cross_element_type(self, product_base, product2):
        product_base.name = product2.name
        product_base.min_weight = product2.min_weight
        product_base.max_weight = product2.max_weight
        product_base.weight_resolution = product2.weight_resolution
        product_base.nutrion_values = product2.nutrion_values

        product_base.correct_weight(product_base.weight)

        return product_base

    # funkcja przypał
    # TODO - zrobić tak, by było ładnie i w zgodzie z dokumnetacją
    def generate_start_solutions(self):
        population = {}
        for i in range(self.population_size):
            lista = [copy.deepcopy(self.product_list[i % 3]), copy.deepcopy(self.product_list[(i + 1) % 3])]
            product = Meal(lista)
            population[product] = self.calculate_target_function(product)

        return population

    def generate_new_population(self, mutated_population):
        new_population = {}

        for item in mutated_population:
            new_population[item] = self.calculate_target_function(item)

        new_population = dict(
            Counter(new_population).most_common()[:-self.population_size + self.always_in_next_population - 1:-1])
        old_pop = Counter(self.population).most_common();
        old_bests = dict(Counter(self.population).most_common()[:-self.always_in_next_population - 1:-1])

        return dict(old_bests.items() | new_population.items())

    def find_meal(self, product_list, nutrion_target):

        self.nutrion_target = nutrion_target
        self.product_list = product_list
        self.population = self.generate_start_solutions()

        for i in range(self.iteration_count):
            selcted_population = self.selection()
            crossed = self.cross(selcted_population)
            mutated = self.mutation(crossed)

            self.population = self.generate_new_population(mutated)

        q = list(self.population.keys())

        print(min(self.population.values()))

        return min(self.population, key=self.population.get)

    if __name__ == "__main__":
        print("kupa")

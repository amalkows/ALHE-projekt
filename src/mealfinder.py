from src.meal import Meal
from collections import Counter
from random import uniform
import copy
import random


class MealFinder:
    iteration_count = 25
    population_size = 30
    # elita
    always_in_next_population = 10

    # w przypadku krzyżowania każdy produkt w posiłku może zamienić typ z produktem z innego posiłku
    # prawdopodobieństwo krzyżowania
    p_cross = 100
    # prawdopodobieństwo zmiany typu w przypadku krzyżowania
    p_cross_product_type = 15

    # na każdym prodkucie w ramach posiłku (wybieramy jeden z trzech rodzajów mutacji)
    p_mutate_type = 10
    p_mutate_weight = 50
    p_mutate_delete_product = 5

    # prawdopodobieństwo dodania produktu
    p_mutate_add_product = 30

    # słownik: [klucz] referencja do obiektu - [wartość] jakość (funkcja celu)
    population = {}

    nutrition_target = []
    product_list = []

    def calculate_target_function(self, meal):
        result = 0
        weights_sum = 0
        for x, y, z in zip(meal.nutrition_values, meal.nutrition_weights, self.nutrition_target):
            # result += ((x - z) ** 2) * y
            result += abs(x - z) * y
            weights_sum += y

        return result / weights_sum

    def selection(self):
        selected_points = []
        sum_of_target_function = 0
        probabilities = []

        for target_function in self.population.values():
            sum_of_target_function += 1 / target_function

        target_function_list = list(self.population.values())

        probabilities.append((1 / target_function_list[0]) / sum_of_target_function)

        for i in range(0, len(self.population) - 1):
            probabilities.append(probabilities[i] + (1 / target_function_list[i + 1]) / sum_of_target_function)

        probabilities[len(probabilities) - 1] = 1

        for i in range(0, self.population_size):
            random_number = uniform(0, 1)
            for j in range(0, len(probabilities)):
                if probabilities[j] > random_number:
                    a = list(self.population.keys())
                    selected_points.append(a[j])
                    break
        return selected_points

    def mutation(self, population):
        new_population = []
        for item in population:
            new_population.append(self.mutate_meal(item))
        return new_population

    def mutate_meal(self, meal):
        mutated_products = []
        mutated_type_products_list = [item.name for item in meal.products]
        for product in meal.products:
            random_number = uniform(0, 100)
            if random_number < self.p_mutate_type:
                mutated_products.append(self.mutate_type_product(product, mutated_type_products_list))
            elif random_number < self.p_mutate_type + self.p_mutate_weight:
                mutated_products.append(self.mutate_weight_product(product))
            elif random_number < 100 - self.p_mutate_delete_product:
                mutated_products.append(copy.deepcopy(product))

        if uniform(0, 100) < self.p_mutate_add_product and len(mutated_products) < Meal.max_products:
            calculated_meal = Meal(mutated_products)
            calculated_meal.calculate_nutrition_values()
            for i in range(0, Meal.nutrition_values_count):
                nutrition_weight_difference = self.nutrition_target[i] - calculated_meal.nutrition_values[i]
                if (nutrition_weight_difference > 0):
                    new_product = self.mutate_add_product(mutated_products, i, nutrition_weight_difference)
                    if new_product is not None:
                         mutated_products.append(new_product)
                    break;

        new_element = Meal(mutated_products)
        new_element.calculate_nutrition_values()

        return new_element

    def mutate_weight_product(self, element):
        new_element = copy.deepcopy(element)
        random_number = random.randint(0, 1)
        if random_number == 0 and new_element.weight > new_element.min_weight:
            new_element.weight -= 1
        elif random_number == 1 and new_element.weight < new_element.max_weight:
            new_element.weight += 1

        return new_element

    def mutate_add_product(self, mutated_products, index_of_nutrition, weight_of_nutrition):
        potential_new_products = [item for item in self.product_list if
                                  next((i for i in mutated_products if i.name == item.name), None) is None]

        if len(potential_new_products) == 0:
            return None

        index = random.randint(0, len(potential_new_products) - 1)
        product = copy.deepcopy(potential_new_products[index])
        product.correct_weight(product.get_max_weight(index_of_nutrition,weight_of_nutrition))
        return product

    def mutate_type_product(self, product, mutated_type_products_list):

        available_types = [item for item in self.product_list if
                           next((i for i in mutated_type_products_list if i == item.name), None) is None]

        if len(available_types) == 0:
            return copy.deepcopy(product)

        index = random.randint(0, len(available_types) - 1)

        new_element = copy.deepcopy(available_types[index])

        new_element.correct_weight(product.weight)

        for i in range(len(mutated_type_products_list) - 1):
            if mutated_type_products_list[i] == product.name:
                mutated_type_products_list[i] = available_types[index].name
                break

        return new_element

    def cross(self, population):
        new_population = []
        for item in population:
            item_cross = uniform(0, 100)
            if item_cross < self.p_cross:
                index = random.randint(0, len(population) - 1)
                new_population.append(self.cross_meals(item, population[index]))
            else:
                new_population.append(item)

        return new_population

    def cross_meals(self, meal1, meal2):
        new_meal = copy.deepcopy(meal1)

        if meal1 == meal2:
            return new_meal

        # parametr pomocniczy (sumowanie ziemniaczków)
        product_uses = {}

        for product in new_meal.products:
            if uniform(0, 100) < self.p_cross_product_type and len(meal2.products) > 1:
                self.cross_product_type(product, meal2.products[random.randint(0, len(meal2.products) - 1)])

            if product_uses.get(product.name, None) is None:
                product_uses[product.name] = product
            else:
                product_uses[product.name].correct_weight(product_uses[product.name].weight + product.weight)

        new_meal.products = product_uses.values()

        return new_meal

    def cross_product_type(self, product_base, product2):
        product_base.name = product2.name
        product_base.min_weight = product2.min_weight
        product_base.max_weight = product2.max_weight
        product_base.weight_resolution = product2.weight_resolution
        product_base.nutrition_values = product2.nutrition_values
        product_base.general_product = product2.general_product

        product_base.correct_weight(product_base.weight)

        return product_base

    def generate_start_solutions(self):
        population = {}
        for i in range(self.population_size):
            meal = self.generate_start_meal(random.randint(0, Meal.nutrition_values_count - 1))
            population[meal] = self.calculate_target_function(meal)
        return population

    # generowanie posiłku, który brutalnie spełnia ograniczenie wartości odżywczej o indeksie nutrition_index
    def generate_start_meal(self, nutrition_index):
        meal = []
        nutrition_weight = 0
        unused_products = copy.deepcopy(self.product_list)
        for i in range(0, Meal.max_products):
            if len(unused_products) == 0:
                break
            product_index = random.randint(0, len(unused_products) - 1)
            product_weight = unused_products[product_index].get_max_weight(nutrition_index,
                                                                           self.nutrition_target[
                                                                               nutrition_index] - nutrition_weight)
            if product_weight == 0:
                break
            else:
                unused_products[product_index].weight = product_weight
                nutrition_weight += product_weight * unused_products[product_index].nutrition_values[nutrition_index] * \
                                    unused_products[product_index].weight_resolution
                meal.append(unused_products[product_index])
                unused_products.remove(unused_products[product_index])
        return Meal(meal)

    def generate_new_population(self, mutated_population):
        new_population = {}

        for item in mutated_population:
            new_population[item] = self.calculate_target_function(item)

        new_population = dict(
            Counter(new_population).most_common()[:-self.population_size + self.always_in_next_population - 1:-1])
        old_bests = dict(Counter(self.population).most_common()[:-self.always_in_next_population - 1:-1])

        return dict(old_bests.items() | new_population.items())

    def find_meal(self, product_list, nutrition_target):

        self.nutrition_target = nutrition_target
        self.product_list = product_list
        self.population = self.generate_start_solutions()
        for i in range(self.iteration_count):
            min_value = min(self.population.values())
            if min_value == 0:
                break
            selected_population = self.selection()
            crossed = self.cross(selected_population)
            mutated = self.mutation(crossed)

            self.population = self.generate_new_population(mutated)

        result = min(self.population, key=self.population.get)
        result.target_function_value = min(self.population.values())
        return result

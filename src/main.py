from src.dietmanager import DietManager
from src.product import Product

obj = DietManager()


#    def __init__(self, name = "", nutrion_values=[0,0], tabu_time = 1, weight = 1, weight_resolution = 1, min_weight = 1, max_weight = 10):


#for name in ["a", "b", "c", "d"]:
#    obj.add_product(0, Product(name, [1, 1], 2))

#for name in ["e1", "f1", "g1", "h1"]:
#    obj.add_product(3, Product(name, [2, 2], 2/3))

#SNIADANIE

obj.add_product(0, Product("Jajko", [10], 2, 1, 5, 1, 5))
obj.add_product(0, Product("Grzanka", [5], 1, 1, 10, 1, 5))
obj.add_product(0, Product("Maslo", [1], 1, 1, 1, 1, 50))
obj.add_product(0, Product("Mleko", [1], 2, 1, 1, 1, 150))

#OBIAD

obj.add_product(1, Product("Schabowy", [5], 2, 1, 150, 1, 2))
obj.add_product(1, Product("Surówka", [1], 1, 10, 10, 10, 5))
obj.add_product(1, Product("Frytki", [1], 1, 10, 1, 10, 50))
obj.add_product(1, Product("Ziemniaki", [1], 1, 10, 1, 10, 150))

#KOLACJA

obj.add_product(2, Product("Platki", [1], 1, 1, 1, 1, 150))
obj.add_product(2, Product("Czipsy", [3], 1, 1, 1, 1, 150))
obj.add_product(2, Product("Jablko", [1], 1, 1, 1, 1, 150))
obj.add_product(2, Product("Miod", [5], 1, 1, 1, 1, 150))


#OGOLNE

obj.add_product(3, Product("Herbata", [1], 2, 1, 150, 1, 2))
obj.add_product(3, Product("Ciastko", [1], 1, 1, 50, 1, 2))
obj.add_product(3, Product("Chleb", [1], 1, 1, 10, 1, 5))
obj.add_product(3, Product("Marchew", [1], 1, 1, 1, 1, 150))


obj.nutrion_values_target = [1500]

obj.generate_n_days_diet(1)
counter = 0
for i in obj.meal_list:
    counter += 1
    print("Dzien", counter)
    for k in [0,1,2]:
        print(" Posiłek", k+1)
        for j in i[k].products:
            print("     ",j.name, j.weight)

from src.dietmanager import DietManager
from src.product import Product

obj = DietManager()


for name in ["a", "b", "c", "d"]:
    obj.add_product(0, Product(name, [1, 1], 2))

for name in ["e1", "f1", "g1", "h1"]:
    obj.add_product(3, Product(name, [2, 2], 2/3))

obj.nutrion_values_target = [100, 50]

obj.generate_n_days_diet(1)
counter = 0
for i in obj.meal_list:
    counter += 1
    print("Dzien", counter)
    for k in [0]:
        print(" Posiłek", k+1)
        for j in i[k].products:
            print("     ",j.name, j.weight)

from src.dietmanager import DietManager
from src.product import Product

obj = DietManager()


for name in ["a", "b", "c", "d"]:
    obj.add_product(0, Product(name, [1, 1], 1))

for name in ["e1", "f1", "g1", "h1"]:
    obj.add_product(3, Product(name, [2, 2], 2/3))

obj.nutrion_values_target = [100, 50]

obj.generate_n_days_diet(3)

for i in obj.meal_list:
    print("Dzien")
    for k in [0,1,2]:
        print(" Posiłek", k)
        for j in i[k].products:
            print("     ",j.name)

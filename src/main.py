from src.dietmanager import DietManager
from src.product import Product
from src.meal import Meal
from src.datagenerator import DataGenerator


obj = DietManager()
generator = DataGenerator()


obj.read_data_from_file("..\\dane.csv")


#    def __init__(self, name = "", nutrion_values=[0,0], tabu_time = 1, weight = 1, weight_resolution = 1, min_weight = 1, max_weight = 10):


#for name in ["a", "b", "c", "d"]:
#    obj.add_product(0, Product(name, [1, 1], 2))

#for name in ["e1", "f1", "g1", "h1"]:
#    obj.add_product(3, Product(name, [2, 2], 2/3))

#SNIADANIE

#obj.add_product(0, Product("Jajko", [10], 2, 5, 1, 5))
#obj.add_product(0, Product("Grzanka", [5], 1, 10, 1, 5))
#obj.add_product(0, Product("Maslo", [1], 1, 1, 1, 50))
#obj.add_product(0, Product("Mleko", [1], 2, 1, 1, 150))

#OBIAD


#obj.add_product(1, Product("Schabowy", [5], 2, 150, 1, 2))
#obj.add_product(1, Product("Surówka", [1], 1, 10, 10, 5))
#obj.add_product(1, Product("Frytki", [1], 1,  1, 10, 50))
#obj.add_product(1, Product("Ziemniaki", [1], 1, 1, 10, 150))


#KOLACJA

#obj.add_product(2, Product("Platki", [3], 1, 2, 1, 100))
#obj.add_product(2, Product("Czipsy", [5], 1, 3, 1, 50))
#obj.add_product(2, Product("Jablko", [1], 1, 30, 1, 5))
#obj.add_product(2, Product("Miod", [5], 1, 1, 1, 150))


#OGOLNE

#obj.add_product(3, Product("Herbata", [1], 2, 150, 1, 2))
#obj.add_product(3, Product("Ciastko", [1], 1, 50, 1, 2))
#obj.add_product(3, Product("Chleb", [1], 1,10, 1, 5))
#obj.add_product(3, Product("Marchew", [1], 1, 1, 1, 150))

obj.nutrition_values_target = [2000, 70, 120, 230]
Meal.nutrition_values_count = 4
Meal.nutrition_weights = [1,10,10,10]


obj.generate_n_days_diet(7)
counter = 0
for i in obj.meal_list:
    counter += 1
    print("Dzien", counter)
    for k in [0,1,2]:
        print(" Posiłek", k+1)
        for j in i[k].products:
            print("     ",j.name, j.weight)
        for j in range(0,Meal.nutrition_values_count):
            print("     Wartosc odzywcza ",j,": ",i[k].nutrition_values[j], "   Wymagana: ",i[k].target_values[j])

plik = open('test', 'w')
plik.write("\n")
for i in obj.meal_list:
    for k in [0,1,2]:
        blad_wzgledny = (abs(i[k].nutrition_values[0] - i[k].target_values[0])/i[k].target_values[0])*100
        plik.write(str(blad_wzgledny))
        plik.write('\n')
plik.write("\n")
for i in obj.meal_list:
    for k in [0,1,2]:
        blad_wzgledny = (abs(i[k].nutrition_values[1] - i[k].target_values[1])/i[k].target_values[1])*100
        plik.write(str(blad_wzgledny))
        plik.write('\n')
plik.write("\n")
for i in obj.meal_list:
    for k in [0,1,2]:
        blad_wzgledny = (abs(i[k].nutrition_values[2] - i[k].target_values[2])/i[k].target_values[2])*100
        plik.write(str(blad_wzgledny))
        plik.write('\n')
plik.write("\n")
for i in obj.meal_list:
    for k in [0,1,2]:
        blad_wzgledny = (abs(i[k].nutrition_values[3] - i[k].target_values[3])/i[k].target_values[3])*100
        plik.write(str(blad_wzgledny))
        plik.write('\n')

plik.close()

a = obj.get_statistics()
print(a)

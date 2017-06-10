from src.dietmanager import DietManager
from src.meal import Meal

diet_manager = DietManager()

diet_manager.read_data_from_file("..\\dane.csv")
diet_manager.nutrition_values_target = [2000, 70, 120, 230]
Meal.nutrition_values_count = 4
Meal.nutrition_weights = [1,10,10,10]


diet_manager.generate_n_days_diet(7)
counter = 0
for i in diet_manager.meal_list:
    counter += 1
    print("Dzień", counter)
    for k in [0,1,2]:
        print(" Posiłek", k+1)
        for j in i[k].products:
            print("     ",j.name, j.weight)
        for j in range(0,Meal.nutrition_values_count):
            print("     Wartość odżywcza ",j,": ",i[k].nutrition_values[j], "   Wymagana: ",i[k].target_values[j])


statistics = diet_manager.get_statistics()
print("\nŚrednia wartość funkcji celu: ",statistics[0])
print("Minimalny czas pomiędzy podaniem tego samego produktu: ",statistics[1])
print("Liczba produktów unikalnych: ",statistics[4])
print("Liczba produktów nieunikalnych: ",statistics[5])

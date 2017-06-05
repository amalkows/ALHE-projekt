from src.meatfinder import MeatFinder

class DietManager:
    breakfastProductList = []
    dinnerProdcutList = []
    supperProductList = []
    generalProductList = []

    nutrionValuesTarget = []
    breakfastPercent = 0.3
    dinnerPercent = 0.5
    supperPercent = 0.2

    tabu = []
    finder = MeatFinder()

    def generateNDaysDiet(self, n):
        print("Generuje diete na", n, "dni!")

        for x in range(n):
            print(x)

            #SNIADANIE
            list = [] #self.breakfastProductList + self.generalProductList - self.tabu
            self.finder.findMeat(list, [])
            #WEZ WYNIK I NA JEGO PODSTAWIE 1. OBLICZ NIE SPELNIENIE NORM 2. ZMODYFIKUJ TABU

            #OBIAD...
            #KOLACJA...

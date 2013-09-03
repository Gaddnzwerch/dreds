import entity
import nutrition
import random

class Vermin(entity.Entity, nutrition.Nutrition):
    """
        Vermin are small animals that are not cared of individually
    """
    def __init__(self, aNutritionValue):
        entity.Entity.__init__(self)
        self.__nutritionValue = aNutritionValue

    def getNutritionValue(self):
        return self.__nutritionValue
    nutrition_value = property(getNutritionValue)

class Mouse(Vermin):
    
    def __init__(self):
       Vermin.__init__(self,100) 

    def ageing(self):
        super(Mouse, self).ageing()
        try:
            randomint = random.randrange(100-self.age) 
            if randomint == 1:
                self.active = False
        except ValueError:
            self.active = False


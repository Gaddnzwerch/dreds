import entity

class Vermin(entity.Entity):
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
       Vermin.__init__(self,5) 
        

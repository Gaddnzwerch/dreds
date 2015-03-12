import entity
import nutrition
import random
import logging

class Vermin(entity.Entity, nutrition.Nutrition):
    """
        Vermin are small animals that are not cared of individually
    """
    def __init__(self, aNutritionValue, aAgility):
        entity.Entity.__init__(self)
        self.__nutritionValue = aNutritionValue
        self.__agility = aAgility

    def getNutritionValue(self):
        return self.__nutritionValue
    nutrition_value = property(getNutritionValue)

    def get_agility(self):
        return self.__agility
    agility = property(get_agility)

    def evade(self, a_other):
        #TODO a little bit more elaborated
        return random.randrange(1,self.__agility)
class Mouse(Vermin):
    
    def __init__(self):
        logging.debug('Created a mouse')
        super(Mouse, self).__init__(100, 75) 

    def ageing(self):
        super(Mouse, self).ageing()
        try:
            randomint = random.randrange(100-self.age) 
            if randomint == 1:
                logging.debug('The mouse dissapeared')
                self.active = False
        except ValueError:
            self.active = False


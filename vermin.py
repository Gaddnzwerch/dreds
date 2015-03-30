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
        self.nutritionValue = aNutritionValue
        self.agility = aAgility

    @property
    def nutrition_value(self):
        return self.nutritionValue

    def evade(self, a_other):
        #TODO a little bit more elaborated
        return random.randrange(1,self.agility)
class Mouse(Vermin):
    
    def __init__(self):
        logging.debug('Created a mouse')
        super().__init__(100, 75) 

    def ageing(self):
        super().ageing()
        try:
            randomint = random.randrange(100-self.age) 
            if randomint == 1:
                logging.debug('The mouse dissapeared')
                self.active = False
        except ValueError:
            self.active = False


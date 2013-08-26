import errors
import behaviour
import animal
import gender
import random
import location

class Foxes(animal.Mammal):
    maxExhaust = 100          #maxium Exhaust before collapse
    exhaustTired = .8         #Exhaust before the individual feels tired
    exhaustTiredReduce = .9   #how much exhaustTired is reduces when an individual collapses
    minForHunger = 20         #hunger before it feels hungry

    def __init__(self):
        animal.Mammal.__init__(self)
        """basic physical attributes"""
        #has to be calculated from physical aspets - not on every tick, so
        self.__speed=5    
        """basic physical states"""
        self.maxExhaust = Fox.maxExhaust
        self.exhaustToTired = self.maxExhaust * Fox.exhaustTired
        """mental states"""
        self.disquiet=0
        self.anger=0
        self.boredness=0
        self.satisfaction=0
        self.isHungry=False
        """behaviours"""
        self.__behaviour = behaviour.Behaviour(self)
        """memories"""
    """basic actions"""

    """getters/setters"""
    def is_bored(self):
        #TODO has to depend on personality
        return self.boredness >= 10
    def is_dirty(self):
        #TODO has to depend on personality
        return self.dirty >= 20
    def add_hunger(self,a_change):
       self.hunger += a_change
       if self.hunger < 0:
        self.hunger = 0
       if self.isHungry != (self.hunger >= Fox.minForHunger):
           print("The ", type(self).__name__, " is getting hungry") 
       self.isHungry = (self.hunger >= Fox.minForHunger)

    """actions"""
    def life(self):        
        self.__behaviour.act()

    def is_same_species(self,a_other):
        return issubclass(Fox,a_other.__class__) 

class Fox(Foxes,gender.Male):
    def __init__(self):
        Foxes.__init__(self)

class Vixen(Foxes,gender.Female):
    def __init__(self):
        Foxes.__init__(self)

class FoxFactory:
    def __init__(self):
        pass
    
    def create_random_fox():
       return FoxFactory.create_fox(random.randint(0,1),location.LocationFactory.create_random_location()) 
    create_random_fox=staticmethod(create_random_fox)

    def create_fox(a_male,a_location):
        """
            Returns a new fox instance.
            Expects a gender (true=male) and a location
        """
        fox = None
        if a_male:
            fox = Fox()
        else:
            fox = Vixen()

        fox.location = a_location
        return fox 
    create_fox=staticmethod(create_fox)

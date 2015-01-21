import location
import plan
import entity
import location
import places
import nutrition
import mathematics

class Animal(entity.Entity):
    def __init__(self):
        entity.Entity.__init__(self)
        """logical states"""
        #self.__location = location.Location()
        """phyisical attributes"""
        self.__speed = 3 #should be used by implementing class
        self.__strength = 0
        self.__agility = 5
        """basic physical states"""
        self.__age = 0
        self.__hunger = 0
        self.__exhaust = 0
        self.__dirty = 0
        """memory funtions"""
        self.__noticed = set()
        self.__sameSpecies = set()
        self.__plans = plan.Plan()
        self.__places = set()
        self.__known = set()
        self.__inside = None
        self.__foodSources = set()
    def get_speed(self):
        return self.__speed
    speed = property(get_speed)

    def get_agility(self):
        return self.__agility
    agility = property(get_agility)
    
    def get_age(self):
        return self.__age

    age = property(get_age)

    def get_hunger(self):
        return self.__hunger
    def set_hunger(self,a_hunger):
        self.__hunger = a_hunger
    
    hunger = property(get_hunger,set_hunger)

    def get_exhaust(self):
        return self.__exhaust

    def set_exhaust(self,a_exhaust):
        self.__exhaust = a_exhaust

    exhaust = property(get_exhaust,set_exhaust)

    def catch(self,a_victim):
        self.add_message("DEBUG: plan.Catch.execute() - The "+ type(self).__name__+ " tries to catch the "+ type(a_victim).__name__)
        return self.__agility >= a_victim.evade(self)

    def get_dirty(self):
        return self.__dirty

    def set_dirty(self,a_dirty):
        self.__dirty = a_dirty 

    dirty = property(get_dirty,set_dirty)

    def get_noticed(self):
        return self.__noticed
    
    noticed = property(get_noticed)

    def get_food_sources(self):
        return self.__foodSources
    food_sources = property(get_food_sources)

    def get_same_species(self):
        return self.__sameSpecies
    same_species = property(get_same_species)

    def get_plans(self):
        return self.__plans
    plans = property(get_plans)

    def get_known(self):
        return self.__known
    known = property(get_known)

    def get_places(self):
        return self.__places
    places = property(get_places)

    def get_inside(self):
        return self.__inside
    def set_inside(self,a_place):
        self.__inside = a_place 
    inside = property(get_inside,set_inside)

    def add_exhaust(self,a_change):
        self.exhaust += a_change
        if self.exhaust < 0:
            self.exhaust = 0
        elif self.exhaust >= self.maxExhaust:
            self.collapse()

    def move(self):
        self.add_message('The ' + type(self).__name__ + ' moves')
        self.add_hunger(5)
        self.add_exhaust(10)
        self.boredness -= 5
        #TODO has to depend on personality
        self.satisfaction += 1
        self.dirty += 1

    def move(self,a_location):
        m_vector = mathematics.Vector(self.location,a_location)
        if self.__speed > 0:
            if m_vector.length >= self.__speed:
                m_vector.length = self.__speed
            self.add_message('The ' + type(self).__name__ + ' moves to ' + repr(a_location) + ' with a speed of ' + repr(m_vector.length) + '.')
            self.location.add(m_vector)
            self.add_message('The ' + type(self).__name__ + ' is now at ' + repr(self.location) + '.')
        else:
            self.add_message('The ' + type(self).__name__ + ' is immobile!')


    def rest(self):
        self.add_message('The '+ type(self).__name__ + ' rests')
        self.add_exhaust(-20)
        self.add_hunger(2)

    def is_recovered(self):
        return self.exhaust <= 0

    def is_exhausted(self):
        #TODO has to depend on personality
        return self.exhaust >= self.exhaustToTired

    def is_hungry(self): 
        #TODO has to depend on personality
        return self.isHungry

    def collapse(self):
        self.add_message("The " + type(self).__name__ + " collapses")
        self.disquiet += 100
        self.anger += 10
        self.dirty += 10
        self.exhaustToTired = self.exhaustToTired * Fox.exhaustTiredReduce
        raise Errors.CollapseError()

    def idle(self):
        self.add_hunger(1)
        self.boredness += 1
        self.add_exhaust(-5)

    def feed(self,a_nutrition):
        self.add_hunger(-a_nutrition.nutrition_value)
        self.add_exhaust(1)
        self.dirty += 10
        self.boredness -= 1
        self.satisfaction += 50
        a_nutrition.get_consumed()
        self.add_message("The " + type(self).__name__+ " feeds the " + type(a_nutrition).__name__ + ". Remaining hunger: " + repr(self.hunger) + " " + repr(self.is_hungry()))

    def percieve(self,a_sourrounding):
        #TODO just see everything in the same quadrant
        location = self.get_location()
        for entity in a_sourrounding.quadrants[location.get_quadrant()].get_inhabitants():
            if entity != self:
                if entity not in self.__noticed:                
                    self.__noticed.add(entity) 
                    if issubclass(entity.__class__, nutrition.Nutrition):
                        self.food_sources.add(entity)
        self.unque()                       
    
    def unque(self):
        remove = set()
        for entity in self.noticed | self.food_sources | self.known:
            if not entity.active:
                remove.add(entity)

        for entity in remove:
            try:
                self.noticed.remove(entity)
                self.food_sources.remove(entity)
                self.known.remove(entity)
            except KeyError:
                pass
        remove.clear
            
    
    def examine(self,a_other):
        if a_other not in self.known:
            if self.is_same_species(a_other):
                self.same_species.add(a_other)
            if issubclass(a_other.__class__,places.Place):
                self.places.add(a_other)
                if issubclass(self.__class__,DenInhabitant):
                    #TODO test if the den is occupied
                    self.add_message("The "+ type(self).__name__+ " made the "+ type(a_other).__name__+ " its den!")
                    self.den = a_other
            self.known.add(a_other)

    def enter(self,a_place):
        self.inside = a_place

    def exit(self):
        self.inside = None
    
    def is_same_species(self,a_other):
        pass
class Mammal(Animal):
    def __init__(self):
        Animal.__init__(self)
        self.__known = set()
    
    def get_known(self):
        return self.__known

    known = property(get_known)

    def percieve(self,a_sourrounding):
        Animal.percieve(self,a_sourrounding)

    def have_sex(self,a_with):
        pass

class DenInhabitant():
    def __init__(self):
        self.__den = None
    def get_den(self):
        return self.__den
    def set_den(self,a_den):
        self.__den = a_den
    den =  property(get_den,set_den)
"""
    Does belong more in Behaviour?
"""
class Carnivore:
    pass
class Cannibal(Carnivore):
    pass


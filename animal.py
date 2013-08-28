import location
import plan
import entity
import location
import places
import nutrition

class Animal(entity.Entity):
    def __init__(self):
        entity.Entity.__init__(self)
        """logical states"""
        #self.__location = location.Location()
        """phyisical attributes"""
        self.__speed = 3 #should be used by implementing class
        self.__strength = 0
        self.__agility = 0
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
        print('The ', type(self).__name__, ' moves')
        self.add_hunger(5)
        self.add_exhaust(10)
        self.boredness -= 5
        #TODO has to depend on personality
        self.satisfaction += 1
        self.dirty += 1

    def move(self,a_location):
        m_vector = location.Vector(self.location,a_location)
        if self.__speed > 0:
            if m_vector.length >= self.__speed:
                m_vector.length = self.__speed
            print('The ', type(self).__name__, ' moves to ', a_location, ' with a speed of ', m_vector.length, '.')
            self.location.add(m_vector)
            print('The ', type(self).__name__, ' is now at ', self.location, '.')
        else:
            print('The ', type(self).__name__, ' is immobile!') 


    def rest(self):
        print('The ', type(self).__name__ , ' rests')
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
        print("The " , type(self).__name__ , " collapses")
        self.disquiet += 100
        self.anger += 10
        self.dirty += 10
        self.exhaustToTired = self.exhaustToTired * Fox.exhaustTiredReduce
        raise Errors.CollapseError()

    def idle(self):
        print('The ', type(self).__name__, ' does nothing')
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

    def percieve(self,a_sourrounding):
        #TODO just see everything in the same quadrant
        location = self.get_location()
        for entity in a_sourrounding.quadrants[location.get_quadrant()].get_inhabitants():
            if entity != self:
                if entity not in self.__noticed:                
                    self.__noticed.add(entity) 
                    print("The ", type(self).__name__,' at ', self.location, ' noticed the ', type(entity).__name__, ' which is %d units away.' % (self.location.get_distance(entity.location)))
                    if issubclass(entity.__class__, nutrition.Nutrition):
                        self.food_sources.add(entity)
                        print("The ", type(entity).__name__ , " is edible for the " , type(self).__name__)
        self.unque()                       
    
    def unque(self):
        remove = set()
        for entity in self.noticed | self.food_sources | self.known:
            if not entity.active:
                remove.add(entity)

        for entity in remove:
            self.noticed.remove(entity)
            self.food_sources.remove(entity)
            self.known.remove(entity)
        remove.clear
            
    
    def examine(self,a_other):
        if a_other not in self.known:
            print("The ", type(self).__name__, " now knows the ", type(a_other).__name__, "!")
            if self.is_same_species(a_other):
                self.same_species.add(a_other)
            if issubclass(a_other.__class__,places.Place):
                print("Added to places")
                self.places.add(a_other)
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

"""
    Belong more in Behaviour?
"""
class Carnivore:
    pass
class Cannibal(Carnivore):
    pass


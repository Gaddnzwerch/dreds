import logging
import location
import plan
import entity
import places
import nutrition
import mathematics
import random
import need
from functools import wraps

"""
    Decorators
"""
def needFunctions(func):
    @wraps(func)
    def checkNeedsFirst(*args):
        self = args[0]
        for m_need in self.needs:
            m_need.act(func)
        func(*args)
    return checkNeedsFirst

"""
    Classes
"""
class Animal(entity.Entity):

    def __init__(self):
        entity.Entity.__init__(self)
        #phyisical attributes
        self.speed = 3 #should be used by implementing class
        self.strength = 0 #should be used by implementing class
        self.agility = 5 #should be used by implementing class
        #basic physical states
        self.hunger = 0
        self.exhaust = 0
        self.dirty = 0
        #memory functions
        self.noticed = set()
        self.same_species = set()
        self.plans = plan.Plan()
        self.strategy = plan.Strategy()
        self.active_plan = plan.Plan()
        self.places = set()
        self.known = set()
        self.inside = None
        self.food_sources = set()
        self.food_places = set() 
        """vegetative actions"""
        self.vegetative_actions = set() 
        """needs"""
        self.needsAttention = set() 
        self.needs = set()
        """requirements"""
        self.requirements = [] 
        """commands"""
        self.commands = set()

        #TODO has to be moved to a builder=====================================
        m_breathing = need.Need("Air", 10, 100, 50)
        m_breathing.add_fulfilling_action(self.breathe,10.0)
        m_breathing.add_creating_action(self.vegetate, 1.0)
        m_breathing.add_creating_action(self.move, 5.0)
        self.needs.add(m_breathing)
        m_eating = need.Need("Food", 7, 250)
        m_eating.add_fulfilling_action(self.feed,10.0)
        m_eating.add_creating_action(self.vegetate, 0.01)
        m_eating.add_creating_action(self.move, 0.05)
        self.needs.add(m_eating)
        m_food_place = plan.Requirement("foodplace", self.get_best_food_place)
        self.requirements.append(m_food_place)
        m_food_source = plan.Requirement("foodsource",self.choose_food_source,m_food_place) 
        self.requirements.append(m_food_source)
        m_food_access = plan.Requirement("foodaccess",self.access_food_source,m_food_source)
        self.requirements.append(m_food_access)
        #TODO =================================================================

    def check_needs(self):
        for m_need in self.needs: 
            self.needsAttention.clear()
            if m_need.needsAction:
                self.vegetative_actions.add(m_need.fulfillingAction)
            if m_need.needsAttention and m_need not in self.needsAttention:
                self.needsAttention.add(m_need)
                logging.info("The " + type(self).__name__ + " feels the need for " + m_need.name)

    def access_food_source(self):
        pass

    def choose_food_source(self): 
        try:
            return random.sample(self.food_sources,1)[0] 
        except ValueError:
            return None


    def plan(self):
        """
        creating, rating and modifying plans
        At the beginning, each entity can create only one plan per tick
        """
        m_need = self.get_need()
        logging.debug("The " + type(self).__name__ + " is thinking about " + m_need.name)
        m_plan = plan.PlanFactory.create_plan(self.strategy, m_need)

    def rate_plan(self, a_plan):
        """
        rating plans
        Not implemented yet
        """
        pass

    def get_need(self):
        """
        find the most pestering need
        """
        try:
            m_need =  self.needsAttention.pop()
        except KeyError:
            m_need = sorted(self.needs, key= lambda need: need.weight, reverse=True) 
            m_need = m_need[0]
        return m_need

    
    @needFunctions
    def vegetate(self, a_sourroundings):
        """
        actions that are supposed to happen every tick
        """
        self.percieve(a_sourroundings)
        self.check_needs()
        for m_action in self.vegetative_actions:
            m_action()
        self.vegetative_actions.clear()
        self.plan()

    @needFunctions
    def breathe(self):
        logging.debug("The " + type(self).__name__ + " is breathing")


    #TODO GZ20151014 there has to be a better way
    def add_exhaust(self,a_change):
        self.exhaust += a_change
        if self.exhaust < 0:
            self.exhaust = 0
        elif self.exhaust >= self.maxExhaust:
            self.collapse()

    @needFunctions
    def move(self):
        logging.info('The ' + type(self).__name__ + ' moves')
        self.add_hunger(5)
        self.add_exhaust(10)
        self.boredness -= 5
        #TODO has to depend on personality
        self.satisfaction += 1
        self.dirty += 1

    @needFunctions
    def move(self,a_location):
        """Move to the passed location."""
        m_vector = mathematics.Vector(self.location,a_location)
        if self.speed > 0:
            if m_vector.length >= self.speed:
                m_vector.length = self.speed
            logging.info('The ' + type(self).__name__ + ' moves to ' + repr(a_location) + ' with a speed of ' + repr(m_vector.length) + '.')
            self.location.add(m_vector)
            logging.info('The ' + type(self).__name__ + ' is now at ' + repr(self.location) + '.')
        else:
            logging.info('The ' + type(self).__name__ + ' is immobile!')
    
    def get_best_food_place(self):
        """Find the best, known food-source and remeber it."""
        #TODO find some strategy here
        try:
            m_food_place = random.sample(self.food_places,1)[0] 
        except ValueError:
            # move to some random place
            logging.info('The ' + type(self).__name__ + ' is moving to a random place.')
            m_food_place = location.LocationFactory.create_location_around(self.location, 5, 10, 10, 0)

        logging.info('The ' + type(self).__name__ + ' is moving to food place ' + repr(m_food_place))
        return m_food_place


    @needFunctions
    def rest(self):
        """Active resting to reduce exhaustion."""
        logging.info('The '+ type(self).__name__ + ' rests')
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
        logging.info("The " + type(self).__name__ + " collapses")
        self.disquiet += 100
        self.anger += 10
        self.dirty += 10
        self.exhaustToTired = self.exhaustToTired * Fox.exhaustTiredReduce
        raise Errors.CollapseError()

    @needFunctions
    def idle(self):
        """Do nothing."""
        logging.info("The " + type(self).__name__ + " idles.")
        self.add_hunger(1)
        self.boredness += 1
        self.add_exhaust(-5)

    @needFunctions
    def feed(self,a_nutrition):
        """Consume the passed nutrition to reduce hunger."""
        logging.info("The " + type(self).__name__+ " feeds on the " + type(a_nutrition).__name__ + ". Remaining hunger: " + repr(self.hunger) + " " + repr(self.is_hungry()))
        self.add_exhaust(1)
        self.dirty += 10
        self.boredness -= 1
        self.satisfaction += 50
        self.add_hunger(-a_nutrition.nutrition_value)
        a_nutrition.get_consumed()

    def percieve(self,a_sourrounding):
        """Retrieve informations from the passed sourrounding."""
        #TODO just see everything in the same quadrant
        location = self.location
        for entity in a_sourrounding.quadrants[location.get_quadrant()].get_inhabitants():
            if entity != self:
                if entity not in self.noticed:                
                    self.noticed.add(entity) 
                    if self.is_nutrition(entity):
                        self.food_sources.add(entity)
        self.unque()                       

    def unque(self):
        """Remove inactive entities from memory-variables."""
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
        """Examine the passed object and classify it."""
        if a_other not in self.known:
            if self.is_same_species(a_other):
                self.same_species.add(a_other)
            if issubclass(a_other.__class__,places.Place):
                self.places.add(a_other)
                if issubclass(self.__class__,DenInhabitant):
                    #TODO test if the den is occupied
                    logging.info("The "+ type(self).__name__+ " made the "+ type(a_other).__name__+ " its den!")
                    self.den = a_other
            self.known.add(a_other)

    def enter(self,a_place):
        """Enter the passed place."""
        self.inside = a_place

    def exit(self):
        self.inside = None
    
    def is_same_species(self,a_other):
        pass

class AnimalBuilder():
    def __init__(self):
        pass
    def create(self):
        pass

class Mammal(Animal):
    def __init__(self):
        Animal.__init__(self)
        self.known = set()
    
    def percieve(self,a_sourrounding):
        Animal.percieve(self,a_sourrounding)

    @needFunctions
    def have_sex(self,a_with):
        pass

class DenInhabitant():
    def __init__(self):
        self.den = None

class Carnivore():
    def __init__(self):
        pass

    def is_nutrition(self, a_entity):
        return issubclass(a_entity.__class__, nutrition.Nutrition)

    def catch(self,a_victim):
        #TODO maybe a bit more elaborate
        logging.debug("Carnivore().catch() - The " + type(self).__name__ + " tries to catch the "+ type(a_victim).__name__)
        return self.agility >= a_victim.evade(self)

class Cannibal(Carnivore):

    def is_nutrition(self, a_entity):
        return super(Cannibal, self).is_nutrition(a_entity) or self.is_same_species(a_entity)

#TODO GZ20151014 has to be relocated
class FieldOfView(mathematics.Flat):
    def __init__(self, a_distance, a_angle):
        self.distance = a_distance
        self.angle = a_angle

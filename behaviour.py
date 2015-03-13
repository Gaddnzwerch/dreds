import random
import errors
import plan
import logging

class Behaviour:    
    def __init__(self,a_animal):
        self.animal = a_animal
        self.behaviour = BehaviourIdle(self)    

    def act(self):
        try:
            self.behaviour.act()
        except errors.CollapseError:
            self.behaviour = BehaviourCollapsed(self)            
        else:
            logging.debug(type(self.behaviour).__name__ + " state check")
            self.state_check()

    def state_check(self):
        self.behaviour = self.behaviour.state_check()
        

class BehaviourIdle(Behaviour):
    def __init__(self,a_parent):
        self.__parent = a_parent
        self.animal = a_parent.animal
        logging.debug("BehaviorIdle.__init__()")
    def act(self):
        try:
            self.animal.plans.execute()
        except IndexError:
            #TODO 
            unknown = self.animal.noticed - self.animal.known
            places = self.animal.places
            if len(unknown) > 0:
                m_interested = random.sample(unknown,1)[0]
                self.animal.plans.append(plan.Move(self.animal,m_interested.location))
                self.animal.plans.append(plan.Examine(self.animal,m_interested))
            else:
                self.animal.idle()

    def state_check(self):
        if self.animal.is_hungry():
            return BehaviourHunt(self.__parent)
        elif self.animal.is_exhausted():
            return BehaviourRest(self.__parent)
        else:
            return self

class BehaviourRest(Behaviour):
    def __init__(self,a_parent):
        self.__parent = a_parent
        self.animal = a_parent.animal
        logging.debug("BehaviorRest.__init__()")
    def act(self):
        self.animal.rest()
    def state_check(self):
        if self.animal.is_recovered():
            return BehaviourIdle(self.__parent)
        elif self.animal.is_hungry():
            return BehaviourHunt(self.__parent) 
        else:
            return self

class BehaviourHunt(Behaviour):
    def __init__(self,a_parent):
        self.__parent = a_parent
        self.animal = a_parent.animal
        logging.debug("BehaviorHunt.__init__()")
    def act(self):
        #TODO hunt
        try:
            self.animal.plans.execute()
        except IndexError:            
            # find something to hunt
            prey = None
            try:
                #TODO find the best prey
                prey = random.sample(self.animal.food_sources,1)[0] 
            except ValueError:
                food_place = self.animal.get_best_food_place()
                self.animal.plans.append(plan.Move(self.animal, food_place))
            if prey:
                # move to it 
                self.animal.plans.append(plan.Move(self.animal,prey.location))
                # catch it
                self.animal.plans.append(plan.Catch(self.animal,prey))
                # consume it
                self.animal.plans.append(plan.Feed(self.animal,prey))
        except errors.HungryError:
            pass
    def state_check(self):
        if self.animal.is_exhausted():
            return BehaviourRest(self.__parent)    
        elif self.animal.is_hungry:
            logging.debug("The " + type(self.animal).__name__ + " is still hungry")
            return self
        else:
            return BehaviourIdle(self.__parent)

class BehaviourCollapsed(Behaviour):
    def __init__(self,a_parent):
        self.__parent = a_parent
        self.animal = a_parent.animal
        logging.debug("BehaviorCollapsed.__init__()")
    def act(self):
        self.animal.rest()
    def state_check(self):
        if self.animal.is_exhausted():
            return self
        else:
            return BehaviourIdle(self.__parent)

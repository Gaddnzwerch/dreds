import random
import errors
import plan

class Behaviour:    
    def __init__(self,a_animal):
        self.animal = a_animal
        self.__behaviour = BehaviourIdle(self)    

    def act(self):
        try:
            self.__behaviour.act()
        except errors.CollapseError:
            self.__behaviour = BehaviourCollapsed(self)            
        else:
            self.state_check()

    def state_check(self):
        self.__behaviour = self.__behaviour.state_check()
        

class BehaviourIdle(Behaviour):
    def __init__(self,a_parent):
        self.__parent = a_parent
    def act(self):
        try:
            self.__parent.animal.plans.execute()
        except IndexError:
            unknown = self.__parent.animal.noticed - self.__parent.animal.known
            if len(unknown) > 0:
                m_interested = random.sample(unknown,1)[0]
                self.__parent.animal.plans.append(plan.Move(self.__parent.animal,m_interested.location))
                self.__parent.animal.plans.append(plan.Examine(self.__parent.animal,m_interested))
            else:
                self.__parent.animal.idle()

    def state_check(self):
        if self.__parent.animal.is_hungry():
            return BehaviourHunt(self.__parent)
        elif self.__parent.animal.is_exhausted():
            return BehaviourRest(self.__parent)
        else:
            return self

class BehaviourRest(Behaviour):
    def __init__(self,a_parent):
        self.__parent = a_parent
    def act(self):
        self.__parent.animal.rest()
    def state_check(self):
        if self.__parent.animal.is_recovered():
            return BehaviourIdle(self.__parent)
        elif self.__parent.animal.is_hungry():
            return BehaviourHunt(self.__parent) 
        else:
            return self

class BehaviourHunt(Behaviour):
    def __init__(self,a_parent):
        self.__parent = a_parent
    def act(self):
        #TODO hunt
        try:
            self.__parent.animal.move()
        except errors.HungryError:
            pass
        if random.randint(0,10) < 2:    
            self.__parent.animal.feed()
    def state_check(self):
        if self.__parent.animal.is_exhausted():
            return BehaviourRest(self.__parent)    
        elif self.__parent.animal.is_hungry:
            return self
        else:
            return BehaviourIdle(self.__parent)

class BehaviourCollapsed(Behaviour):
    def __init__(self,a_parent):
        self.__parent = a_parent
    def act(self):
        self.__parent.animal.rest()
    def state_check(self):
        if self.__parent.animal.is_exhausted():
            return self
        else:
            return BehaviourIdle(self.__parent)

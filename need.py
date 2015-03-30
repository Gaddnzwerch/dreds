import logging
import operator
from collections import namedtuple
Action = namedtuple("Action",["func","level"])

class Need():
    """
       Needs are things that are necessary for an entity to survive and be well.
    """
    def __init__(self, a_name, a_severity, a_threshold, a_action_threshold=1000):
        self.name = a_name
        self.severity = a_severity # on a scale from 1 (nice to have) to 10 (totally necessary)
        self.__level = 0.0 # on a scale from 0 to 100
        self.threshold = a_threshold # if weight > threshold entity is aware of the need
        self.action_threshold = a_action_threshold
        self.action = dict()
        self.__fulfillingAction = None # stored in object to avoid costly sorting of self.action


    @property
    def needsAction(self):
        return self.weight > self.action_threshold 

    @property
    def fulfillingAction(self):
        if not self.__fulfillingAction: 
            action = sorted(self.action.values(), key= lambda action: action.level) 
            m_action, m_level = action[0]
            self.__fulfillingAction = m_action
        return self.__fulfillingAction
        
    @property
    def weight(self):
        return self.severity * self.level

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, a_value):
        if a_value > 100:
            self.__level = 100
        elif a_value > 0:
            self.__level = a_value
        else:
            self.__level = 0

    def add_fulfilling_action(self, a_action, a_level):
        m_action = Action(func=a_action, level=-a_level)
        self.action[a_action.__name__] = m_action
        self.__fulfillingAction = None

    def add_creating_action(self, a_action, a_level):
        m_action = Action(func=a_action, level=a_level)
        self.action[a_action.__name__] = m_action
        self.__fulfillingAction = None

    def act(self, func):
        try:
            m_action = self.action[func.__name__]
            self.level += m_action.level
        except KeyError:
            pass


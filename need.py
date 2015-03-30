import logging

class Need():
    """
       Needs are things that are necessary for an entity to survive and be well.
    """
    def __init__(self, a_name, a_severity, a_threshold):
        self.name = a_name
        self.severity = a_severity # on a scale from 1 (nice to have) to 10 (totally necessary)
        self.__level = 0.0 # on a scale from 0 to 100
        self.threshold = a_threshold # if weight > threshold entity is aware of the need
        self.action = dict()

    def act(self, func):
        if func.__name__ in self.action.keys():
            logging.debug("The " + type(self).__name__ + " " + self.name + " uses " + func.__name__)
            self.level = self.level + self.action[func.__name__]

    def add_fulfilling_action(self, a_action, a_level):
        self.action[a_action] = - a_level

    def add_creating_action(self, a_action, a_level):
        self.action[a_action] = a_level

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

class Need():
    """
       Needs are things that are necessary for an entity to survive and be well.
    """
    def __init__(self, a_name, a_severity, a_threshold):
        self.name = a_name
        self.severity = a_severity # on a scale from 1 (nice to have) to 10 (totally necessary)
        self.__level = 0 # on a scale from 0 to 100
        self.threshold = a_threshold # if weight > threshold entity is aware of the need
        self.fullfillingActions = dict() # actions that satisfy that need
        self.creatingActions = dict() # actions that create / increase that need

    def get_weight(self):
        return self.severity * self.level

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, a_value):
        if a_value > 0:
            self.__level = a_value
        else:
            self.__level = 0

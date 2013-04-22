import location
class Entity:
    def __init__(self):
        self.__location = location.Location()
    def get_location(self):
        return self.__location
    def set_location(self,a_location):
        self.__location = a_location
    location = property(get_location,set_location)

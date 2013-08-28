import location
from collections import deque

class Biome():
    def __init__(self):
       self.__lightHeight = 0
       self.__avgTemperature = 0
       self.__avgRainfall = 0
       self.__boundaries = Path()
    
    def get_light_height(self):
        return self.__lightHeight
    def set_light_height(self,a_height):
        self.__lightHeight = a_height
    lightHeight = property(get_light_height,set_light_height)


class Path(deque):
    def __init__(self):
        deque.__init__(self)
        self.__startOver = False

    def get_start_over(self):
        return self.__startOver
    def set_start_over(self,a_startOver):
        self.__startOver = a_startOver
    startOver = property(get_start_over,set_start_over)

    def add(self,a_new_location):
        self.add_right(a_new_location)
        
   

class BiomeFactory():
    """
        Use MERS-type generation as a first shot?
    """
    pass

class Place():
    def __init__(self,a_name,a_location):
        self.__location = location.Location(a_location.x,a_location.y)
        self.__name = a_name
        self.__active = True

    def get_active(self):
        return self.__active
    def set_active(self,a_active):
        self.__active = a_actvie
    active = property(get_active, set_active)        

    def get_location(self):
        return self.__location
    def set_location(self,a_location):
        self.__location = a_location
    location = property(get_location,set_location)

    def get_name(self):
        return self.__name
    def set_name(self,a_name):
        self.__name = a_name
    name = property(get_name,set_name)

class Den(Place):
    """
        A place individuals can enter and leave.
    """
    def __init__(self,a_name,a_location):
        Place.__init__(self,a_name,a_location)
        self.__contain = set()

    def get_contain(self):
        return self.__contain

    def exit(self,a_object):
        #TODO chose an exit
        print("The ", type(a_object).__name__, " leaves the ", self.name)
        self.__contain.remove(a_object)         
        a_object.set_location(self.get_location())

    def enter(self,a_object):
        print("The ", type(a_object).__name__, " enters the ", self.name)
        self.__contain.add(a_object) 
        a_object.set_location(self.get_location())


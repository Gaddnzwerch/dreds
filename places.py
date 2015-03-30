import logging
import location
from collections import deque

class Biome():
    def __init__(self):
       self.lightHeight = 0
       self.avgTemperature = 0
       self.avgRainfall = 0
       self.boundaries = Path()
    
class Path(deque):
    def __init__(self):
        deque.__init__(self)
        self.startOver = False

    def add(self,a_new_location):
        self.add_right(a_new_location)
        
   

class BiomeFactory():
    """
        Use MERS-type generation as a first shot?
    """
    pass

class Place():
    def __init__(self,a_name,a_location):
        self.location = location.Location(a_location.x,a_location.y)
        self.name = a_name
        self.active = True


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
        logging.debug("The ", type(a_object).__name__, " leaves the ", self.name)
        self.__contain.remove(a_object)         
        a_object.set_location(self.get_location())

    def enter(self,a_object):
        logging.debug("The ", type(a_object).__name__, " enters the ", self.name)
        self.__contain.add(a_object) 
        a_object.set_location(self.get_location())


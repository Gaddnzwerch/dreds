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
   

class BiomeFactory():
    """
        Use MERS-type generation as a first shot?
    """
    pass

class Place(location.Location):
    def __init__(self,a_name):
        location.Location.__init__()
        self.__name = a_name

    def get_name(self):
        return self.__name
    def set_name(self,a_name):
        self.__name = a_name
    name = property(get_name,set_name)


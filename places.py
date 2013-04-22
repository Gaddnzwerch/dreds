import location

class Biome():
    def __init__(self):
       self.__lightHeight = 0
    
    def get_light_height(self):
        return self.__lightHeight
    def set_light_height(self,a_height)
        self.__lightHeight = a_height
    lightHeight = property(get_light_height,set_light_height)


class BiomeFactory():
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


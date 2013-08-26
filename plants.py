import location
import entity

class Plant(entity.Entity):
    def __init__(self):
        entity.Entity.__init__(self)
        self.__age = 0
        # self.__location = location.Location()

    def get_age(self):
        return self.__age

    age = property(get_age)

    """
    def get_location(self):
        return self.__location

    location = property(get_location)
    """

class Tree(Plant):
    def __init__(self):
        Plant.__init__(self)
        self.__diameter = 1
        self.__height = 1

    def get_height(self):
        return self.__height

    height = property(get_height)

    def get_diameter(self):
        return self.__diameter

    diameter = property(get_diameter)


class BroadLeafTree(Tree):
    def __init__(self):
        Tree.__init__(self)
        self.__crownDiameter = 1
        self.__leafsPercent = 100

    def get_crown_diameter(self):
        return self.__crownDiameter

    crownDiameter = property(get_crown_diameter)

    def get_leafs_percent(self):
        return self.__leafsPercent

    leafsPercent = property(get_leafs_percent)

class Conifer(Tree):
    def __init__(self):
        Tree.__init__(self)

class PlantFactory:    
    def create_plant(self):
        pass

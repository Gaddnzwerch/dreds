import location
class Entity:
    def __init__(self):
        self.__location = location.Location()
        self.__active = True
        self.__age = 0
    def get_location(self):
        return self.__location
    def set_location(self,a_location):
        self.__location = a_location
    location = property(get_location,set_location)

    def get_active(self):
        return self.__active
    def set_active(self,a_active):
        self.__active = a_active
    active = property(get_active, set_active)        

    def get_age(self):
        return self.__age
    def set_age(self,a_age):
        self.__age = a_age
    age = property(get_age,set_age) 

    def ageing(self):
        self.age += 1

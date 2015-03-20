import location
class Entity:
    def __init__(self):
        self.__location = location.Location()
        self.__active = True
        self.__age = 0
        self.__message = ''
        self.__notifiation = [] #contains informations about incidents 
        self.dna = '' #TODO stores informations about the features an entity has - will be used to create further instances
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

    def get_message(self):
        m_message = self.__message
        self.__message = ''
        return m_message
    def add_message(self, a_additionalMessage):
        self.__message += a_additionalMessage
        
    def get_notification(self):
        m_notification = self.__notification
        self.__notification = []
        return m_notification
    def add_notification(self, a_notification):
        self.__notification.append(a_notification)

    def ageing(self):
        self.age += 1

    def vegetate(self, a_sourrounding):
        pass

import location
class Entity:
    def __init__(self):
        self.location = location.Location()
        self.active = True
        self.age = 0
        self.__message = ''
        self.__notifiation = [] #contains informations about incidents 
        self.dna = '' #TODO stores informations about the features an entity has - will be used to create further instances

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

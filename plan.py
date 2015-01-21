import collections

class Plan(collections.deque):
    """
        Plans are used to store Queus of commands or even other plans.
    """
    def __init__(self):
        collections.deque.__init__(self)
    def execute(self):
        command = self.popleft()
        command.execute()
        if command.finished:
            pass
        else:
            self.appendleft(command)
class Command():
    """
        Commands are the smalest unit. They can be executed by an entity.
    """
    def __init__(self,a_entity):
        self.__finished = False
        self.__entity = a_entity
    def is_finished(self):
        return self.__finished
    def set_finished(self,a_finished):
        self.__finished = a_finished
    finished = property(is_finished,set_finished)
    def get_entity(self):
        return self.__entity
    entity = property(get_entity)
    def execute(self):
        pass

class Move(Command): 
    def __init__(self,a_entity,a_to):
       Command.__init__(self,a_entity)
       self.__to = a_to
    def execute(self):
       if self.entity.location != self.__to:
        self.entity.move(self.__to)
       self.finished = self.entity.location == self.__to 

class Catch(Command):
    def __init__(self,a_entity,a_victim):
        super(Catch,self).__init__(a_entity)
        self.__victim = a_victim
    def execute(self):
        if self.__victim.active:
            catched = self.entity.catch(self.__victim)
            self.finished = catched
        else:
            self.__victim = None
            self.finished = True
        

class Feed(Command):
    def __init__(self,a_entity,a_nutrition):
        Command.__init__(self,a_entity)
        self.__nutrition = a_nutrition
    def execute(self):
        if self.__nutrition.active:
            self.entity.feed(self.__nutrition)
        self.__nutrition = None
        self.finished = True

class Examine(Command):
    def __init__(self,a_entity,a_other):
        Command.__init__(self,a_entity)
        self.__other = a_other
    def execute(self):
        self.entity.examine(self.__other)
        self.finished = True

class Enter(Command):
    def __init__(self,a_entity,a_place):
        Command.__init__(self,a_entity)
        self.__place = a_place
    def execute(self):
        self.__place.enter(self.entity)
        self.entity.enter(self.__place)
        self.finished = True

class Exit(Command):
    def __init__(self,a_entity,a_place):
        Command.__init__(self,a_entity)
        self.__place = a_place
    def execute(self):
        self.__place.exit(self.entity)
        self.entity.exit()
        self.finished = True 

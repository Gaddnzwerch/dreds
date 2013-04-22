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
    def empty(self):
        pass
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

class Examine(Command):
    def __init__(self,a_entity,a_other):
        Command.__init__(self,a_entity)
        self.__other = a_other
    def execute(self):
        self.entity.examine(self.__other)
        self.finished = True

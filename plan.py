import collections

class PlanFactory():
    def __init__(self):
        pass


class Plan(collections.deque):
    """
        Plans are used to store Queues of commands or even other plans.
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
    #TODO modify a plan
    def modify(self):
        pass
    #TODO get a plan's representation

class Command():
    """
        Commands are the smalest unit. They can be executed by an entity.
    """
    def __init__(self,a_entity):
        self.finished = False
        self.entity = a_entity
    def execute(self):
        pass

class Move(Command): 
    def __init__(self,a_entity,a_to):
       Command.__init__(self,a_entity)
       self.to = a_to
    def execute(self):
       if self.entity.location != self.to:
        self.entity.move(self.to)
       self.finished = self.entity.location == self.to 

class Catch(Command):
    def __init__(self,a_entity,a_victim):
        super(Catch,self).__init__(a_entity)
        self.victim = a_victim
    def execute(self):
        if self.victim.active:
            catched = self.entity.catch(self.victim)
            self.finished = catched
        else:
            self.victim = None
            self.finished = True
        

class Feed(Command):
    def __init__(self,a_entity,a_nutrition):
        Command.__init__(self,a_entity)
        self.nutrition = a_nutrition
    def execute(self):
        if self.nutrition.active:
            self.entity.feed(self.nutrition)
        self.nutrition = None
        self.finished = True

class Examine(Command):
    def __init__(self,a_entity,a_other):
        Command.__init__(self,a_entity)
        self.other = a_other
    def execute(self):
        self.entity.examine(self.other)
        self.finished = True

class Enter(Command):
    def __init__(self,a_entity,a_place):
        Command.__init__(self,a_entity)
        self.place = a_place
    def execute(self):
        self.place.enter(self.entity)
        self.entity.enter(self.place)
        self.finished = True

class Exit(Command):
    def __init__(self,a_entity,a_place):
        Command.__init__(self,a_entity)
        self.place = a_place
    def execute(self):
        self.place.exit(self.entity)
        self.entity.exit()
        self.finished = True 

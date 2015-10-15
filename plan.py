import collections

class Requirement():
    """
    """
    def __init__(self, a_name, a_fulfilling_func, a_requirement=None):
        self.name = a_name
        self.fulfilling_func = a_fulfilling_func
        self.required_object = None
        self.a_requirement = a_requirement

    def met(self):
        if self.required_object == None:
            self.required_object = self.fulfilling_func()
        return self.required_object != None

class PlanFactory(): 
    @staticmethod
    def create_plan(a_strategy, a_need):
        try:
            m_plan = a_strategy.goals[a_need.name]
        except KeyError:
            m_plan = Plan()
            m_plan.append(a_need.fulfillingAction)
        return m_plan
        
class Strategy():
    """
    Contains all the plans an entity knows. Allows to operate on and sort them
    """
    def __init__(self):
        self.plans = set()
        self.goals = dict()

    def add_plan(self, a_plan):
        self.plans.add(a_plan)
        self.goals[a_plan.goal] = a_plan

class Plan(collections.deque):
    """
        Plans are used to store Queues of commands or even other plans.
    """
    def __init__(self, a_goal = ""):
        collections.deque.__init__(self)
        self.goal = ""
        self.complete = False
        self.executed = 0

    def __call__(self):
        self.execute()

    def execute(self):
        command = self.popleft()
        command.execute()
        if command.finished:
            self.executed += 1 
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
    def __init__(self,a_entity, a_requirement=None):
        self.finished = False
        self.entity = a_entity
        self.requirement = a_requirement

    def __call__(self):
        self.execute()

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

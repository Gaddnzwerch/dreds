import location
import entity

class Plant(entity.Entity):
    def __init__(self):
        super().__init__()

class Tree(Plant):
    def __init__(self):
        super().__init__()
        self.diameter = 1
        self.height = 1

class BroadLeafTree(Tree):
    def __init__(self):
        Tree.__init__(self)
        self.crownDiameter = 1
        self.leafsPercent = 100

class Conifer(Tree):
    def __init__(self):
        Tree.__init__(self)

class PlantFactory:    
    def create_plant(self):
        pass

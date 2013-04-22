#! /usr/bin/env python3.2
import location
import fox
import plants
import places

class Sourroundings:

    def __init__(self):
        self.quadrants = dict()
        self.population = set()
        self.flora = set()
        self.locationFactory = location.LocationFactory()        
    
    def populate(self):
        biome = places.Biome() 
        foxlocation = self.locationFactory.create_random_location()
        self.population.add(fox.FoxFactory.create_fox(True,foxlocation))
        foxlocation = self.locationFactory.create_location_in_quadrant(foxlocation.get_quadrant())
        self.population.add(fox.FoxFactory.create_fox(False,foxlocation))
        self.flora.add(plants.Tree())
        self.flora.add(plants.BroadLeafTree())

        for animal in self.population | self.flora:
            try:
                quadrant = animal.location.get_quadrant()
                quadrant = self.quadrants[quadrant]
            except KeyError:
                self.quadrants[quadrant] = quadrant
            finally:
                quadrant.get_inhabitants().add(animal)

def main():
    sourroundings = Sourroundings()
    sourroundings.populate()

    i = 0
    while True and i < 10:        
        print("Round ", i)
        for entity in sourroundings.population:
            entity.percieve(sourroundings)
            entity.life()
        i += 1

if __name__=='__main__':
    main() 

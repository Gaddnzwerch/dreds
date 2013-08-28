#! /usr/bin/env python3.2
import location
import fox
import plants
import places
import gametime
import vermin

class Sourroundings:

    def __init__(self):
        self.quadrants = dict()
        self.population = set()
        self.fauna = set()
        self.flora = set()
        self.places = set()
        self.locationFactory = location.LocationFactory()        
    
    def populate(self):
        biome = places.Biome() 
        foxlocation = self.locationFactory.create_random_location()
        self.population.add(fox.FoxFactory.create_fox(True,foxlocation))
        foxlocation = self.locationFactory.create_location_in_quadrant(foxlocation.get_quadrant())
        self.places.add(places.Den("Fox-Den",foxlocation))
        foxlocation = self.locationFactory.create_location_in_quadrant(foxlocation.get_quadrant())
        self.population.add(fox.FoxFactory.create_fox(False,foxlocation))
        #self.flora.add(plants.Tree())
        #self.flora.add(plants.BroadLeafTree())
        #self.flora.add(plants.Conifer())

        maxVermin = 5
        noVermin = 0
        while noVermin < maxVermin:
            mouse = vermin.Mouse()
            mouse.location = self.locationFactory.create_location_in_quadrant(foxlocation.get_quadrant())
            self.fauna.add(mouse)
            noVermin += 1

        for entity in self.population | self.flora | self.places | self.fauna:
            try:
                quadrant = entity.location.get_quadrant()
                quadrant = self.quadrants[quadrant]
            except KeyError:
                self.quadrants[quadrant] = quadrant
            finally:
                quadrant.get_inhabitants().add(entity)

def main():
    sourroundings = Sourroundings()
    sourroundings.populate()
    remove = set()
    m_time = gametime.Gametime    

    while True and m_time.tickcount < 100:        
        print("Round ", m_time.tickcount)        
        for entity in sourroundings.population:
            entity.percieve(sourroundings)
            entity.life()

        for entity in sourroundings.fauna:
            if not entity.active:
                remove.add(entity)

        for entity in remove:
            quadrant = entity.location.get_quadrant()
            quadrant = sourroundings.quadrants[quadrant]
            quadrant.get_inhabitants().remove(entity)
            sourroundings.fauna.remove(entity)
        remove.clear()            
        m_time.nextTick()

if __name__=='__main__':
    main() 

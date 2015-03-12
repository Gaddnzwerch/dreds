#! /usr/bin/env python3.2
import logging
import location
import fox
import plants
import places
import gametime
import vermin
#Import for tests
import mathematics
import terrain
from display import Display
import time

class Sourroundings:

    def __init__(self):
        self.quadrants = dict()
        self.population = set()
        self.fauna = set()
        self.flora = set()
        self.places = set()
        self.locationFactory = location.LocationFactory()        
        self.MAXX = 50
        self.MAXY = 50
        self.terrain = terrain.Terrain()
    
    def populate(self):
        self.terrain.add_point(self.locationFactory.create_random_location(0,self.MAXX,0,self.MAXY))
        biome = places.Biome() 
        foxlocation = self.locationFactory.create_random_location(self.terrain.min_x, self.terrain.max_x, self.terrain.min_y,self.terrain.max_y) 
        foxlocation.z = self.terrain.get_elevation(foxlocation) 

        self.population.add(fox.FoxFactory.create_fox(True,foxlocation))
        foxlocation = self.locationFactory.create_location_in_quadrant(foxlocation.get_quadrant())
        foxlocation.z = self.terrain.get_elevation(foxlocation) 
        self.places.add(places.Den("Fox-Den",foxlocation))
        foxlocation = self.locationFactory.create_location_in_quadrant(foxlocation.get_quadrant())
        foxlocation.z = self.terrain.get_elevation(foxlocation) 
        self.population.add(fox.FoxFactory.create_fox(False,foxlocation))
        self.flora.add(plants.Tree())
        self.flora.add(plants.BroadLeafTree())
        self.flora.add(plants.Conifer())

        maxVermin = 5
        noVermin = 0
        while noVermin < maxVermin:
            mouse = vermin.Mouse()
            mouse.location = self.locationFactory.create_location_in_quadrant(foxlocation.get_quadrant())
            mouse.location.z = self.terrain.get_elevation(mouse.location) 
            self.fauna.add(mouse)
            noVermin += 1

        for entity in self.population | self.flora | self.places | self.fauna:
            self.add_entity(entity)
    
    def vermin(self):
        mouse = vermin.Mouse()
        mouse.location = self.locationFactory.create_random_location(self.terrain.min_x,self.terrain.max_x,self.terrain.min_y,self.terrain.max_y)
        mouse.location.z = self.terrain.get_elevation(mouse.location)
        self.fauna.add(mouse)
        self.add_entity(mouse)
            
    def add_entity(self,a_entity):
        try:
            quadrant = a_entity.location.get_quadrant()
            quadrant = self.quadrants[quadrant]
        except KeyError:
            self.quadrants[quadrant] = quadrant
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise 
        finally:
            quadrant.get_inhabitants().add(a_entity)
    

def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='dreds.log', level=logging.DEBUG)
    logging.info('Start')
    sourroundings = Sourroundings()
    sourroundings.populate()
    remove = set()
    m_time = gametime.Gametime    
    m_display = Display()

    while True and m_time.tickcount < 50:        
        for entity in sourroundings.population:
            oldQuadrant = entity.location.get_quadrant()
            entity.percieve(sourroundings)
            entity.life()
            newQuadrant = entity.location.get_quadrant()
            if oldQuadrant != newQuadrant:
                oldQuadrant.remove(entity)
                sourroundings.add_entity(entity) 


        for entity in sourroundings.fauna:
            entity.ageing()
            if not entity.active:
                remove.add(entity)

        for entity in remove:
            quadrant = entity.location.get_quadrant()
            quadrant = sourroundings.quadrants[quadrant]
            quadrant.get_inhabitants().remove(entity)
            sourroundings.fauna.remove(entity)
        remove.clear()            
        sourroundings.vermin()
        m_time.nextTick()

        m_stringlist = []
        m_string = []
        for i in range(0,51):
            m_string.append(' ')
        for i in range(0,51):
            m_stringlist.append(m_string.copy())

        for m_quadrant in sourroundings.quadrants:
            for m_inhabitant in m_quadrant.get_inhabitants():
                m_stringlist[int(m_inhabitant.location.x)][int(m_inhabitant.location.y)] = type(m_inhabitant).__name__[0]
        m_display.display(m_stringlist)        
        time.sleep(0.1)
        """
        for i in range(0, sourroundings.MAXY):
            if m_time.tickcount == i:
                m_string.append('{:*^50}'.format('F'))
            else:
                m_string.append('')

        m_display.display(m_string)
        """
    logging.info('End')
    

#    """
#        Tests
#    """
#    v1 = mathematics.Vector(location.Location(0,0,0),location.Location(1,2,3))
#    v2 = mathematics.Vector(location.Location(0,0,0),location.Location(-7,8,9))
#    v3 = mathematics.Vector(location.Location(1,0,0),location.Location(0,1,0))
#    v4 = mathematics.Vector(location.Location(0,0,0),location.Location(1,1,0))
#    v5 = mathematics.Vector(location.Location(0,0,0),location.Location(0,1,0))
#    v6 = mathematics.Vector(location.Location(0,0,1),location.Location(100,0,10))
#    v7 = mathematics.Vector(location.Location(0,0,1),location.Location(0,100,10))
#    print(v1.dot_product(v2))
#    print(v1.cross_product(v2))
#    flat1 = mathematics.Flat(v1,v2)
#    print(flat1.normal)
#    try:
#        flat2 = mathematics.Flat(v1,v3)
#    except Exception:
#        pass
#    flat3 = mathematics.Flat(v4,v5)
#    print(flat3.is_point_in(location.Location(0.5,0.5,0)))
#    print(flat3.is_point_in(location.Location(1,1,100)))
#    flat4 = mathematics.Flat(v6,v7)
#    print(flat4)
#    circle0 = flat4.get_circumscribed_circle()
#    print(flat4.get_area())
#    print(flat4.normal)
#    print(flat4.get_z(location.Location(1,1,0)))
#    circle1 = flat1.get_circumscribed_circle()
#    print(circle0, circle1)

if __name__=='__main__':
    main() 

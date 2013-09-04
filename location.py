import random
import mathematics

class Location(mathematics.Point):
    """
        A representation for a point
    """
    def __init__(self,a_x=0, a_y=0, a_z=0):
        super(Location,self).__init__(a_x,a_y,a_z)

    def get_quadrant(self):
        return Quadrant(int(self.m_x/Quadrant.resolution),int(self.m_y/Quadrant.resolution),int(self.m_z/Quadrant.resolution))

    def get_distance(self,a_location): 
        return Line(self.get_array(),a_location.get_array()).distance()
    
class Quadrant(Location):
    """
        A Quadrant is used to store objects wich are located near eachother.
    """
    resolution = 10 #Points per Dimension in a Quadrant
    def __init__(self,a_x,a_y,a_z):
        super(Quadrant,self).__init__(a_x,a_y,a_z)
        self.__inhabitants = set()

    __hash__ = Location.__hash__

    def get_inhabitants(self):
        return self.__inhabitants

class Line:
    """
        Defines a line between two given Points.
    """
    memoDist = dict()
    
    def __init__(self,a_array1,a_array2):
        self.__array1 = a_array1
        self.__array2 = a_array2

    def __eq__(self,other):
        return self.__array1 == other.__array1 and self.__array2 == other.__array2

    def __hash__(self):        
        a1 = self.__array1[:]
        return hash(a1.append(self.__array2))

    def distance(self):
        try:
            return Line.memoDist[self]
        except KeyError:
            distance = 0
            length = range(len(self.__array1))
            for i in length:
                distance += (self.__array1[i]-self.__array2[i])**2
            distance = int(distance**0.5)
            Line.memoDist[self] = distance
            return distance

class LocationFactory:
    """
        Creates new locations.
    """
    #def create_random_location():
    #    return Location(random.randint(1,32000),random.randint(1,32000),Location.standardZ)

    def create_random_location(a_minX, a_maxX, a_minY , a_maxY):
        return Location(random.randint(a_minX, a_maxX),random.randint(a_minY,a_maxY),Location.standardZ)
    create_random_location = staticmethod(create_random_location)

    def create_location_around(a_oldLocation,a_minDistance, a_maxDistanceX, a_maxDistanceY, a_maxDistanceZ):
        oldLocationArray = a_oldLocation.get_array()        
        counter = 0
        newX = 0
        newY = 0
        newZ = Location.standardZ;
        randomint = random.randint
        while counter < 10:
            for i in range(len(oldLocationArray)):
                newX = randomint(oldLocationArray[0] - a_maxDistanceX, oldLocationArray[0] + a_maxDistanceX)
                newY = randomint(oldLocationArray[1] - a_maxDistanceY, oldLocationArray[1] + a_maxDistanceY)
                newZ = randomint(oldLocationArray[2] - a_maxDistanceZ, oldLocationArray[2] + a_maxDistanceZ)
                newLocation = Location(newX,newY,newZ)
                if newLocation.get_distance(a_oldLocation) >= a_minDistance:
                    return newLocation
        
        raise Exception
    create_location_around = staticmethod(create_location_around)

    def create_location_in_quadrant(a_quadrant):
        """
            Creates a random location in a given quadrant.
        """
        randomint = random.randint
        newX = randomint(a_quadrant.m_x * Quadrant.resolution, a_quadrant.m_x * (Quadrant.resolution) + Quadrant.resolution)
        newY = randomint(a_quadrant.m_y * Quadrant.resolution, a_quadrant.m_y * (Quadrant.resolution) + Quadrant.resolution)
        try:
            newZ = randomint(a_quadrant.m_z * Quadrant.resolution, a_quadrant.m_z * (Quadrant.resolution + 1)-1)
        except ValueError:
            newZ = Location.standardZ
        return Location(newX,newY,newZ)
    create_location_in_quadrant = staticmethod(create_location_in_quadrant)


import places
import location
import mathematics

class Terrain():
    def __init__(self):
        self.__flats = set()
        self.__adjacent_flats = dict()
        points = set()
        maximum = 100
        height = 1
        points.add(location.Location(1,1,height))
        points.add(location.Location(1,maximum,height))
        points.add(location.Location(maximum,1,height))
        points.add(location.Location(maximum,maximum,height))
        v1 = mathematics.Vector(location.Location(1,1,height),location.Location(1,maximum,height))
        v2 = mathematics.Vector(location.Location(1,1,height),location.Location(maximum,1,height))
        self.__flats.add(mathematics.Flat(v1,v2))
        v1 = mathematics.Vector(location.Location(maximum,maximum,height),location.Location(maximum,1,height))
        v2 = mathematics.Vector(location.Location(maximum,maximum,height),location.Location(1,maximum,height))
        self.__flats.add(mathematics.Flat(v1,v2))

        for flat in self.__flats:
            print(flat)
            near = set()
            for other_flat in self.__flats:
                if flat != other_flat and flat.is_adjacent(other_flat):
                   near.add(other_flat)
                   break
            self.__adjacent_flats[flat] = near
        
        print(self.__adjacent_flats)

    def add_point(self,a_new_point):        
        # Delaunay-Triangulation
        new_flats = set()
        # find correct flat
        for flat in self.__flats:
            if flat.is_point_in(a_new_point):
                print("Point: " , a_new_point , " is in :" , flat)
                # create new vectors (and flats)
                new_vector1 = mathematics.Vector(flat.vector1.origin, a_new_point)
                new_vector2 = mathematics.Vector(flat.vector2.origin, a_new_point)
                new_vector3 = mathematics.Vector(a_new_point, flat.vector1.target)
                new_vector4 = mathematics.Vector(a_new_point, flat.vector2.target)
                new_flats.add(mathematics.Flat(flat.vector1,new_vector1))
                new_flats.add(mathematics.Flat(flat.vector2,new_vector2))
                new_flats.add(mathematics.Flat(new_vector3,new_vector4))
                break
        # Umkreisbedingung prüfen
        for new_flat in new_flats:
            pass
        # flip if necessary

import places
import location
import mathematics

class Terrain():
    def __init__(self):
        self.__flats = set()
        self.__adjacent_flats = dict()
        maximum = 100
        height = 1
        v1 = mathematics.Vector(location.Location(1,1,height),location.Location(1,maximum,height))
        v2 = mathematics.Vector(location.Location(1,1,height),location.Location(maximum,1,height))
        self.__flats.add(mathematics.Flat(v1,v2))
        v1 = mathematics.Vector(location.Location(maximum,maximum,height),location.Location(maximum,1,height))
        v2 = mathematics.Vector(location.Location(maximum,maximum,height),location.Location(1,maximum,height))
        self.__flats.add(mathematics.Flat(v1,v2)) 
        self.__get_adjacent_flats()
        
        # print("DEBUG: terrain.Terrain.__init__() - ", self.__adjacent_flats)
    
    def __get_adjacent_flats(self):
        for flat in self.__flats:
            # print("DEBUG: terrain.Terrain.__init__() - ",flat)
            self.__adjacent_flats[flat] = self.__get_adjacent_flats_for_flat(flat)
#            near = set()
#            for other_flat in self.__flats:
#                if flat != other_flat and flat.is_adjacent(other_flat):
#                   near.add(other_flat)
#                   break
#            self.__adjacent_flats[flat] = near
    
    def __get_adjacent_flats_for_flat(self, a_flat):
        near = set()
        for other_flat in self.__flats:
            if a_flat != other_flat and a_flat.is_adjacent(other_flat):
                near.add(other_flat)
        return near

    def add_point(self,a_new_point):        
        # Delaunay-Triangulation
        new_flats = set()
        # find correct flat
        for flat in self.__flats:
            if flat.is_point_in(a_new_point):
                print("DEBUG: terrain.Terrain.add_point() - ", a_new_point , " is in :" , flat)
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
        adjacent_flats = self.__adjacent_flats[flat]
        self.__flats.discard(flat)
        #DEBUG
        for x in new_flats | self.__flats:
            print("DEBUG: terrain.Terrain.add_point() - ", x)
        #DEBUG
        while len(new_flats) > 0:
            delaunay = True   
            new_flat = new_flats.pop()
            for test_flat in new_flats | adjacent_flats:
                double_points = new_flat.points & test_flat.points
                if test_flat != new_flat and len(double_points) > 1:
                    for point in test_flat.points - new_flat.points:
                        if new_flat.get_circumscribed_circle().is_point_in(point):
                            delaunay = False
                            # flip if necessary
                            print("DEBUG: terrain.Terrain.add_point [Flipping flats " , new_flat) 
                            print("                                                 " , test_flat, "]")
                            # find points that exist only in one of the flats
                            single_points = new_flat.points ^ test_flat.points
                            double_points = new_flat.points & test_flat.points
                            # create new vectors
                            main_vector = mathematics.Vector(single_points.pop(),single_points.pop())
                            for point in double_points: 
                                second_vector = mathematics.Vector(main_vector.origin,point)
                                # create new flats
                                created_flat = mathematics.Flat(main_vector, second_vector)
                                # add new flats
                                new_flats.add(created_flat)
                                adjacent_flats.union(self.__get_adjacent_flats_for_flat(created_flat))
                                print("DEBUG: terrain.Terrain.add_point [new Flat " , created_flat , "]")
                            # remove old flats from list
                            new_flats.discard(new_flat)
                            new_flats.discard(test_flat)
                            adjacent_flats.discard(new_flat)
                            adjacent_flats.discard(test_flat)
                            self.__flats.discard(test_flat)
                            break
            if delaunay:
                self.__flats.add(new_flat)
                self.__get_adjacent_flats()
        print("DEBUG: terrain.Terrain.add_point [alle neuen Flächen erfüllen die Umkreisbedingung]")                            
        for flat in self.__flats:
            print("DEBUG: terrain.Terrain.add_point " , flat)

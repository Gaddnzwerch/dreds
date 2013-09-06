import places
import location
import mathematics

class Terrain():
    def __init__(self):
        self.__flats = set()
        self.__adjacent_flats = dict()
        self.__min_x = 0
        self.__max_x = 100
        self.__min_y = 0
        self.__max_y = 100
        height = 1
        v1 = mathematics.Vector(location.Location(self.__min_x,self.__min_y,height),location.Location(self.__min_x,self.__max_y,height))
        v2 = mathematics.Vector(location.Location(self.__min_x,self.__min_y,height),location.Location(self.__max_x,self.__min_y,height))
        self.__flats.add(mathematics.Flat(v1,v2))
        v1 = mathematics.Vector(location.Location(self.__max_x,self.__max_y,height),location.Location(self.__max_x,self.__min_y,height))
        v2 = mathematics.Vector(location.Location(self.__max_x,self.__max_y,height),location.Location(self.__min_x,self.__max_y,height))
        self.__flats.add(mathematics.Flat(v1,v2)) 
        self.__get_adjacent_flats()
        
        # print("DEBUG: terrain.Terrain.__init__() - ", self.__adjacent_flats)
    def get_max_x(self):
        return self.__max_x
    max_x = property(get_max_x)

    def get_max_y(self):
        return self.__max_y
    max_y = property(get_max_y)

    def get_min_x(self):
        return self.__min_x
    min_x = property(get_min_x)

    def get_min_y(self):
        return self.__min_y
    min_y = property(get_min_y)
    
    def __get_adjacent_flats(self):
        for flat in self.__flats:
            # print("DEBUG: terrain.Terrain.__init__() - ",flat)
            self.__adjacent_flats[flat] = self.__get_adjacent_flats_for_flat(flat)
    
    def __get_adjacent_flats_for_flat(self, a_flat):
        near = set()
        for other_flat in self.__flats:
            if a_flat != other_flat and a_flat.is_adjacent(other_flat):
                near.add(other_flat)
        return near

    def get_elevation(self, a_point):
        for flat in self.__flats:
            if flat.is_point_in(a_point):
                return flat.get_z(a_point)

    def add_point(self,a_new_point):        
        # Delaunay-Triangulation
        new_flats = set()
        # find correct flat
        for flat in self.__flats:
            if flat.is_point_in(a_new_point):
                cutting_vector = flat.get_vector_of(a_new_point)
                if not cutting_vector:
                    # print("DEBUG: terrain.Terrain.add_point() - ", a_new_point , " is in :" , flat)
                    # create new vectors (and flats)
                    new_vector1 = mathematics.Vector(flat.vector1.origin, a_new_point)
                    new_vector2 = mathematics.Vector(flat.vector2.origin, a_new_point)
                    new_vector3 = mathematics.Vector(a_new_point, flat.vector1.target)
                    new_vector4 = mathematics.Vector(a_new_point, flat.vector2.target)
                    new_flats.add(mathematics.Flat(flat.vector1,new_vector1))
                    new_flats.add(mathematics.Flat(flat.vector2,new_vector2))
                    new_flats.add(mathematics.Flat(new_vector3,new_vector4))
                else: 
                    # print("DEBUG: terrain.Terrain.add_point(", a_new_point,") - lies on :" , cutting_vector)
                    #TODO: test if a_new_point is on a side of the flat - in that case only two new flats are needed
                    unused_point = (flat.points - cutting_vector.points).pop()
                    new_vector1 = mathematics.Vector(a_new_point, cutting_vector.origin)
                    new_vector2 = mathematics.Vector(a_new_point, cutting_vector.target)
                    new_vector3 = mathematics.Vector(a_new_point, unused_point)
                    new_flats.add(mathematics.Flat(new_vector1, new_vector3))
                    new_flats.add(mathematics.Flat(new_vector2, new_vector3))
                    # find a flat that shares that point
                    for additional_flat in self.__adjacent_flats[flat]:
                        # print("DEBUG: terrain.Terrain.add_point(", a_new_point,") - testing :", additional_flat)
                        cutting_vector2 = additional_flat.get_vector_of(a_new_point)
                        if cutting_vector2:
                            unused_point = (additional_flat.points - cutting_vector2.points).pop()
                            new_vector1 = mathematics.Vector(a_new_point, cutting_vector2.origin)
                            new_vector2 = mathematics.Vector(a_new_point, cutting_vector2.target)
                            new_vector3 = mathematics.Vector(a_new_point, unused_point)
                            new_flats.add(mathematics.Flat(new_vector1, new_vector3))
                            new_flats.add(mathematics.Flat(new_vector2, new_vector3))
                            # print("DEBUG: terrain.Terrain.add_point(", a_new_point, ") - discarding " , additional_flat)
                            self.__flats.discard(additional_flat)
                            break

                # print("DEBUG: terrain.Terrain.add_point(", a_new_point, ") - discarding " , flat)
                self.__flats.discard(flat)
                # print("DEBUG: terrain.Terrain.add_point(", a_new_point,") - new flats:")
                # for x in new_flats:
                    # print("                                  ", x)

                # check delaunay-condition
                while len(new_flats) > 0:
                    delaunay = True   
                    new_flat = new_flats.pop()
                    for test_flat in new_flats | self.__get_adjacent_flats_for_flat(new_flat): 
                        double_points = new_flat.points & test_flat.points
                        if test_flat != new_flat and len(double_points) > 1:
                            for point in test_flat.points - new_flat.points:
                                if new_flat.get_circumscribed_circle().is_point_in(point):
                                    delaunay = False
                                    # flip if necessary
                                    # print("DEBUG: terrain.Terrain.add_point [Flipping flats " , new_flat) 
                                    # print("                                                 " , test_flat, "]")
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
                                        # print("DEBUG: terrain.Terrain.add_point [new Flat " , created_flat , "]")
                                    # remove old flats from list
                                    new_flats.discard(new_flat)
                                    new_flats.discard(test_flat)
                                    self.__flats.discard(test_flat)
                                    break
                    if delaunay:
                        self.__flats.add(new_flat)
                        self.__get_adjacent_flats()
                break
        # print("DEBUG: terrain.Terrain.add_point [alle neuen Flächen erfüllen die Umkreisbedingung]")                            
        # print("DEBUG: terrain.Terrain.add_point(", a_new_point, ") - after insert:")
        # for flat in self.__flats:
            # print("                                 ", flat)

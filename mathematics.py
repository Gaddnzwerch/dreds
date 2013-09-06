import copy

class Vector():
    def __init__(self,a_point1,a_point2):
        self.__origin = a_point1
        self.__target = a_point2
        self.__dirX = a_point2.m_x - a_point1.m_x + 0.0
        self.__dirY = a_point2.m_y - a_point1.m_y + 0.0
        self.__dirZ = a_point2.m_z - a_point1.m_z + 0.0
        self.__length = 0.0
    def get_x(self):
        return self.__dirX
    def set_x(self,a_x):
        self.__length = 0.0
        self.__dirX = a_x
    x = property(get_x,set_x)

    def get_y(self):
        return self.__dirY
    def set_y(self,a_y):
        self.__length = 0.0
        self.__dirY = a_y
    y = property(get_y,set_y)

    def get_z(self):
        return self.__dirZ
    def set_z(self,a_z):
        self.__length = 0.0
        self.__dirZ = a_z
    z = property(get_z,set_z)

    def get_points(self):
        points = set()
        points.add(self.origin)
        points.add(self.target)
        return points
    points = property(get_points)

    def get_length(self):
        if self.__length != 0.0:
            return self.__length
        else:
            self.__length = (self.__dirX**2 + self.__dirY**2 + self.__dirZ**2)**0.5
            return self.__length
    def set_length(self,a_length):
        self.__dirX = (self.x / self.length) * a_length
        self.__dirY = (self.y / self.length) * a_length
        self.__dirZ = (self.z / self.length) * a_length
        self.__length = a_length
    length = property(get_length,set_length) 
    
    def __str__(self):
        return ('Vector %s->%s') % (self.origin.__str__(), self.target.__str__())
    
    def get_origin(self):
        return self.__origin
    origin = property(get_origin)

    def get_target(self):
        return Point(self.__origin.x + self.__dirX, self.__origin.y + self.__dirY, self.__origin.z + self.__dirZ)
    target = property(get_target)

    def dot_product(self,a_vector):
       return (self.x * a_vector.x + self.y * a_vector.y + self.z * a_vector.z)

    def cross_product(self,a_vector):
        x = self.y * a_vector.z - self.z * a_vector.y
        y = self.z * a_vector.x - self.x * a_vector.z
        z = self.x * a_vector.y - self.y * a_vector.x
        value = copy.copy(self)
        value.x = x
        value.y = y
        value.z = z
        return value
    
class Flat():
    """
        a flat is limited by two vectors who have to share the same origin
    """
    def __init__(self, a_vector1, a_vector2):
        if (a_vector1.origin == a_vector2.origin):
            self.__vector1 = a_vector1
            self.__vector2 = a_vector2
            self.__normal = self.__vector1.cross_product(self.__vector2)
            self.__circumscribed_circle = None
        else:
            raise Exception("Vectors don't have the same origin")
    
    def get_vector1(self):
        return self.__vector1
    vector1 = property(get_vector1)

    def get_vector2(self):
        return self.__vector2
    vector2 = property(get_vector2)

    def get_vector3(self):
        return Vector(self.__vector1.target,self.__vector2.target)
    vector3 = property(get_vector3)
    
    def get_normal(self):
        return self.__normal
    normal = property(get_normal)

    def get_origin(self):
        return self.__vector1.origin
    origin = property(get_origin)

    def get_vector_of(self,a_point):
        """
            if a_point lies on a border of the flat, return the corresponding border, else None
        """
        return_vector = None
        v1 = copy.copy(self.__vector1)
        v1.z = 0
        v2 = copy.copy(self.__vector2)
        v2.z = 0
        v3 = Vector(self.__vector1.origin,a_point)
        v3.z = 0
        
        # Compute dot products
        dot00 = v1.dot_product(v1)
        dot01 = v1.dot_product(v2)
        dot02 = v1.dot_product(v3)
        dot11 = v2.dot_product(v2)
        dot12 = v2.dot_product(v3)

        # Compute barycentric coordinates
        invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * invDenom
        v = (dot00 * dot12 - dot01 * dot02) * invDenom
        if v == 0:
            return_vector = self.vector1
        elif u == 0:
            return_vector = self.vector2
        elif u + v == 1:
            return_vector = self.vector3
        return return_vector


    def is_point_in(self,a_point):
        """
            Returns true if the x,y value of a loctation lies in the baseplain of the flat (z=0)
            Algorithm from http://www.blackpawn.com/texts/pointinpoly/default.html
        """
        v1 = copy.copy(self.__vector1)
        v1.z = 0
        v2 = copy.copy(self.__vector2)
        v2.z = 0
        v3 = Vector(self.__vector1.origin,a_point)
        v3.z = 0
        
        # Compute dot products
        dot00 = v1.dot_product(v1)
        dot01 = v1.dot_product(v2)
        dot02 = v1.dot_product(v3)
        dot11 = v2.dot_product(v2)
        dot12 = v2.dot_product(v3)

        # Compute barycentric coordinates
        invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * invDenom
        v = (dot00 * dot12 - dot01 * dot02) * invDenom
        # print("DEBUG: mathematics.Flat.is_point_in(",a_point,") - u: " , u , " v: " , v)

        # Check if point is in triangle
        return (u >= 0) and (v >= 0) and (u + v <= 1)
    
    def get_z(self, a_point):
        direction = Vector(Point(0,0,0),Point(0,0,1))
        t = ((self.origin.x * self.normal.x) + (self.origin.y * self.normal.y) + (self.origin.z * self.normal.z) - (self.normal.x * a_point.x) - (self.normal.y * a_point.y) - (self.normal.z * a_point.z)) / ((self.normal.x * direction.x) + (self.normal.y * direction.y) + (self.normal.z * direction.z))
        return a_point.z + (direction.z * t)
        
    def get_circumscribed_circle(self):
        """
        Idea from http://www.ics.uci.edu/~eppstein/junkyard/circumcenter.html
        p_0 = (((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_1 - c_1) 
            -  ((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_1 - c_1)) 
            / D

        p_1 = (((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_0 - c_0)
            -  ((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_0 - c_0))
            / D

        where D = (a_0 - c_0) * (b_1 - c_1) - (b_0 - c_0) * (a_1 - c_1)

        The _squared_ circumradius is then:

        r^2 = (c_0 - p_0)^2 + (c_1 - p_1)^2
        """
        if not self.__circumscribed_circle:
            a_0 = self.vector1.origin.x
            a_1 = self.vector1.origin.y
            b_0 = self.vector1.target.x
            b_1 = self.vector1.target.y
            c_0 = self.vector2.target.x
            c_1 = self.vector2.target.y
            D = (a_0 - c_0) * (b_1 - c_1) - (b_0 - c_0) * (a_1 - c_1)
            if D == 0:
                print("DEBUG: mathematics.Flat.get_circumscribed_circle [D = 0] - for ", self, ":" ,  a_0, a_1, b_0, b_1, c_0, c_1)

            p_0 = (((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_1 - c_1) -  ((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_1 - c_1)) / D
            p_1 = (((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_0 - c_0) -  ((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_0 - c_0)) / D
            p = Point(p_0,p_1,0)
            r = ((c_0 - p_0)**2 + (c_1 - p_1)**2)**0.5
            self.__circumscribed_circle = Circle(Point(p_0,p_1),r)
            # print("DEBUG: mathematics.Flat.get_circumscribed_circle - ", p, " : ", r) 

        return self.__circumscribed_circle
    
    def get_area(self):
        return (((self.vector1.length + self.vector2.length + self.vector3.length)*(self.vector1.length + self.vector2.length + self.vector3.length)*(self.vector2.length + self.vector3.length - self.vector1.length)*(self.vector3.length + self.vector2.length - self.vector1.length)**0.5)/4)

    def GetIntersectionEG(Ep, Er1, Er2, Gp, Gr):
        """
        Idea from http://c4dnetwork.com/board/threads/78864-Schnittpunkt-Ebene-Gerade
        Ep = Ortsvector der Ebene
        Er1 = Richtungsvetor 1 von Ep aus
        Er2 = Richtungsvetor 2 von Ep aus
        Gp = Ortsvektor auf der Geraden
        Gr = Richtungvektor von Gp aus
        """
        cross = Er1.Cross(Er2)
        t = ((Ep.x*cross.x)+(Ep.y*cross.y)+(Ep.z*cross.z)-(cross.x*Gp.x)-(cross.y*Gp.y)-(cross.z*Gp.z))/((cross.x*Gr.x)+(cross.y*Gr.y)+(cross.z*Gr.z))
        S = c4d.Vector(Gp.x + (Gr.x * t),Gp.y + (Gr.y * t),Gp.z + (Gr.z * t))
        return S

    def get_points(self):
        points = set()
        points.add(self.__vector1.origin)
        points.add(self.__vector1.target)
        points.add(self.__vector2.target)
        return points
    points = property(get_points)


    def is_adjacent(self, a_other_flat):
        return(len(a_other_flat.points & self.points)>0)

    def __str__(self):
        return ('Area %s %s') % (self.vector1,self.vector2)

class Point():    
    """
        Basic type to store a location. A technical class for calulation purposes.
    """
    standardZ = 1.0
    def __init__(self,a_x=0.0, a_y=0.0, a_z=standardZ):
        self.m_x = a_x
        self.m_y = a_y
        self.m_z = a_z
    def __eq__(self,other):
        if type(self) == type(other) or issubclass(self.__class__,other.__class__) or issubclass(other.__class__,self.__class__):
            return self.m_x == other.m_x and self.m_y == other.m_y and self.m_z == other.m_z
        else:
            return False
    def __hash__(self):
        return(hash("%6d%6d%6d" % (self.m_x,self.m_y,self.m_z)))  
        
    def __str__(self):
        return("Point x:%.2f,y:%.2f,z:%.2f" % (self.m_x, self.m_y, self.m_z))
    def get_array(self):
        return [self.m_x,self.m_y,self.m_z]

    def add(self,a_vector):
        self.m_x += a_vector.x
        self.m_y += a_vector.y
        self.m_z += a_vector.z

    def get_x(self):
        return self.m_x
    x = property(get_x)

    def get_y(self):
        return self.m_y
    y = property(get_y)

    def get_z(self):
        return self.m_z
    def set_z(self, a_z):
        self.m_z = a_z
    z = property(get_z, set_z)

class Circle():
    """
        As the name says it
    """
    def __init__(self, a_point, a_radius):
        self.__center = a_point
        self.__radius = a_radius
    
    def is_point_in(self,a_point):
       # print ("DEBUG: mathematics.Circle.is_point_in - ", self.__center, a_point, self.__radius)
       return ((self.__center.x - a_point.x)**2 + ((self.__center.y - a_point.y)**2)) <= self.__radius**2 
    
    def __str__(self):
        return ("Circle  %s radius %s") % (self.__center, self.__radius)

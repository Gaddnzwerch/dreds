import copy
import location

class Vector():
    def __init__(self,a_location1,a_location2):
        self.__origin = a_location1
        self.__target = a_location2
        self.__dirX = a_location2.m_x - a_location1.m_x + 0.0
        self.__dirY = a_location2.m_y - a_location1.m_y + 0.0
        self.__dirZ = a_location2.m_z - a_location1.m_z + 0.0
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
        return ('x%f,y%f,z%f') % (self.x,self.y,self.z)
    
    def get_origin(self):
        return self.__origin
    origin = property(get_origin)

    def get_target(self):
        return Location(self.__origin.x + self.__dirX, self.__origin.y + self.__dirY, self.__origin.z + self.__dirZ)
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
        else:
            raise Exception("Vectors don't have the same origin")
    
    def get_normal(self):
        return self.__normal
    normal = property(get_normal)

    def get_origin(self):
        return self.__vector1.origin
    origin = property(get_origin)
    
    def is_location_in(self,a_location):
        """
            Returns true if the x,y value of a loctation lies in the baseplain of the flat (z=0)
            Algorithm from http://www.blackpawn.com/texts/pointinpoly/default.html
        """
        v1 = copy.copy(self.__vector1)
        v1.z = 0
        v2 = copy.copy(self.__vector2)
        v2.z = 0
        v3 = Vector(self.__vector1.origin,a_location)
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

        # Check if point is in triangle
        return (u >= 0) and (v >= 0) and (u + v < 1)
    
    def get_z(self, a_location):
        direction = Vector(location.Location(0,0,0),location.Location(0,0,1))
        t = ((self.origin.x * self.normal.x) + (self.origin.y * self.normal.y) + (self.origin.z * self.normal.z) - (self.normal.x * a_location.x) - (self.normal.y * a_location.y) - (self.normal.z * a_location.z)) / ((self.normal.x * direction.x) + (self.normal.y * direction.y) + (self.normal.z * direction.z))
        return a_location.z + (direction.z * t)
        


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

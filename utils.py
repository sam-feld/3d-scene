#==============================
# Utils.py module
# Description:
#   Defines utility classes for 3D graphics
#==============================
import math
class Point:
    """A simple 3D Point Class"""

    def __init__(self, x=0, y=0, z=0):
        """A constructor for Point class using initial x,y,z values"""
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """Basic string representation of this point"""
        return "(%s,%s,%s)" % (self.x, self.y, self.z)

    def lerp(self, q, t):
        """Linear interpolation between two points"""
        return Point(self.x + t*(q.x - self.x),
                    self.y + t*(q.y - self.y),
                    self.z + t*(q.z - self.z))

    def lerpV(self, v, t):
        """Linear interpolation between a point and a vector"""
        return Point(self.x + t*v.dx,
                    self.y + t*v.dy,
                    self.z + t*v.dz)

class Vector:
    """A simple 3D Vector Class
    def __init__(self, p=None, q=None):
        #A constructor for Vector class between two Points p and q
        if q is None:
            if p is None:
                self.dx = 0
                self.dy = 0
                self.dz = 0   # No direction at all
            else:
                self.dx = p.x
                self.dy = p.y
                self.dz = p.z  # Origin to p
        else:
            self.dx = q.x - p.x
            self.dy = q.y - p.y
            self.dz = q.z - p.z
    """

    def __init__(self, dx,dy,dz):
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def __str__(self):
        """Basic string representation of this vector"""
        return "<%s,%s,%s>" % (self.dx, self.dy, self.dz)
    
    def magnitude(self):
        """Computes the magnitude (length) of this vector"""
        return math.sqrt(self.dx*self.dx + self.dy*self.dy + self.dz*self.dz)
    
    def normalize(self):
        """Normalizes this Vector"""
        mag = self.magnitude()
        if mag != 0:
            self.dx /= mag
            self.dy /= mag
            self.dz /= mag
        

    
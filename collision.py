from utils import Point
class Collision:
    def __init__(self, width, depth, xPos, zPos):
        self.leftBound = xPos - (width/2)
        self.rightBound = xPos + (width/2)
        self.frontBound = zPos + (depth/2)
        self.backBound = zPos - (depth/2)

    
    def pointInside(self, point):
        if (point.x > self.leftBound and point.x < self.rightBound) and (point.z > self.backBound and point.z < self.frontBound):
            return True
        else:
            return False
    
    
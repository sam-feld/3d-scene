"""""""""""""""""""""""""""""
This class contains the code for each pool ball, specifying movement, direction, speed,
and rotation of each ball.
"""""""""""""""""""""""""""""
from materials import *
from textures import *
from basic_shapes import *
from utils import Vector
import math

class PoolBall:
    #Constructor method, note booleans for texture and cueball
    def __init__(self, has_texture, texture_name, is_cue, textures, basic_shapes):
        self.textures = textures
        self.basic_shapes = basic_shapes

        self.radius = 0.186 # Standard radius (in feet) for a pool ball
        self.position_x = 0
        self.position_z = 0
        self.rotation_x = 0
        self.rotation_z = 0

        #Velocity variables
        self.power = 0
        self.direction = Vector(0,0,0) 

        # Confine the ball to our table (Our table is 7.7 units long, 3.7 units wide, and centered at the origin)
        self.max_x = (7.7/2) - self.radius
        self.min_x = -7.7/2 + self.radius

        self.max_z = 3.7/2 - self.radius
        self.min_z = -3.7/2 + self.radius

        #Texture mapping variables
        self.has_texture = has_texture
        if has_texture:
            self.texture = texture_name
        if is_cue or has_texture:
            self.material = Materials.BALL_RESIN
        else:
           self.material = Materials.SILVER

    #Sets initial state for each ball post-creation
    def set_config(self, position_x, position_z, rotation_x, rotation_z):
        self.position_x = position_x
        self.position_z = position_z

        self.rotation_x = rotation_x
        self.rotation_z = rotation_z

    #Draw function for each frame
    def draw(self):

        # Set the materials/texture
        Materials.set_material(GL_FRONT, self.material)
        if self.has_texture:
            self.textures.set_texture(self.texture)
        #Draw ball
        self.basic_shapes.draw_animated_sphere(self.radius, self.position_x, self.position_z, self.rotation_x, self.rotation_z)

        #increment motion of ball if moving
        if self.power != 0:
            #Update
            self.position_x += (self.direction.dx * self.power)
            self.position_z += (self.direction.dz * self.power)
            self.rotation_z += (self.direction.dx * math.pi)
            self.rotation_x += (self.direction.dz * math.pi)

            #Decelerate ball by 70% every second (~2% every frame)
            self.power *= .98
            #If ball velocity has reached a very low value, set the power to 0
            if self.power < .002:
                self.power = 0
            
            #Bounce upon hitting edge of table
            if self.position_x >= self.max_x and self.direction.dx > 0:
                self.direction.dx *= -1
            if self.position_x <= self.min_x and self.direction.dx < 0:
                self.direction.dx *= -1
            if self.position_z >= self.max_z and self.direction.dz > 0:
                self.direction.dz *= -1
            if self.position_z <= self.min_z and self.direction.dz < 0:
                self.direction.dz *= -1

    #getAngle() method calculates the angle the ball is moving in, and returns it 
    #to the program
    def getAngle(self):
        return math.degrees(math.atan(self.direction.dz / self.direction.dx)) % 360
    
    #changeDirection() method lets us set a new directional vector
    def changeDirection(self, newDir):
        self.direction = newDir

    #draw_dash() method draws a line of dashes within the bounds of the pool table from the cue ball
    @staticmethod
    def draw_dash(cue_ball, angle, dashNum, basic_shapes):
        dashX = cue_ball.position_x + ((.48) * dashNum) * math.cos(math.radians(angle))
        dashZ = cue_ball.position_z + ((-.48) * dashNum) * math.sin(math.radians(angle))
        space = .4  # aprox 4.8 in
        glPushMatrix()

        # Go to the center of the ball, then rotate and move out radially from that point
        if dashNum == 1:
            glTranslate(cue_ball.position_x, .075, cue_ball.position_z)
            glRotate(angle, 0, 1, 0)
        else:
            glTranslate(space, 0, 0)
        
        
        #Set material, and draw dash
        Materials.set_material(GL_FRONT, Materials.BALL_RESIN)
        basic_shapes.draw_rectangle(.08, 0.125, 0.04) # line is 1.5 in wide, 0.5 in tall
        if (dashX < 4.6 and  dashX > -4 and dashZ < 2 and dashZ > -2):
            PoolBall.draw_dash(cue_ball,angle, dashNum + 1, basic_shapes)
        glPopMatrix()

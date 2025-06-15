#==============================
# Matthew Glennon, Sam Feld, Aban Khan, Sai Vemula, Jose Salgado, Camryn Keller
# CSC645: Computer Graphics
#   Fall 2024
# Description:
#   This program creates a fully interactive 3D room, with textured walls/floor/ceiling
#   The player may also interact with the lights, pool table, as well as the pair of dice
#   on the corner table
#   
#==============================
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from basic_shapes import BasicShapes
from components import Components
from textures import Textures
from utils import Point
from camera import Camera
from materials import *
from collision import Collision
from light import Light

# Window settings
window_dimensions = (1200, 800)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Room dimensions
ROOM_WIDTH = 20.0
ROOM_HEIGHT = 15.0
ROOM_DEPTH = 20.0

# Camera settings
CAM_ANGLE = 60.0
CAM_NEAR = 0.01
CAM_FAR = 1000.0
INITIAL_EYE = Point(0, 5.67, 8)
INITIAL_LOOK_ANGLE = 0

# List for collision boxes
collisionList = []




class Room:
    
    # pool shooting variables
    in_shooting_mode = False
    shooting_angle = 0

    # Animation frames
    global_frame = 0 # Used to keep track of time
    dice_frame = 0
    initial_dice_frame = 0
    hanging_light_frame = 0
    initial_hanging_light_frame = 0

    # animation booleans
    animate_dice = False
    animate_hanging_light = False

    # Other spotlight variables
    swing_factor = 0
    spot_light_is_enabled = False
    spotlight_state = {
            "current_intensity": 0.5,  # Default starting intensity
            "target_intensity": 0.5   # Default target intensity
        }
    
    # Picture boolean
    show_picture = False

    def __init__(self):

        # Inititalize helpers
        self.textures = Textures()
        self.basic_shapes = BasicShapes()
        self.components = Components(self.textures, self.basic_shapes)

        pygame.init()
        pygame.display.set_mode(window_dimensions, pygame.DOUBLEBUF | pygame.OPENGL)
        self.clock = pygame.time.Clock()
        
        self.camera = Camera(CAM_ANGLE, window_dimensions[0]/window_dimensions[1], CAM_NEAR, CAM_FAR, 
                           INITIAL_EYE, INITIAL_LOOK_ANGLE)
        
        self.init_gl()
        
        # Light states
        self.light_states = {
            'red': True,
            'green': True,
            'blue': True,
            'spotlight': True,
            'lamp': True,
            'flashlight': True
        }
        
        self.running = True

    def should_we_show_picture(self):
        # Iterate through the light states
        for light_name, this_light_is_on in self.light_states.items(): 
            # Ignore the flashlight and check other lights
            if light_name != 'flashlight' and this_light_is_on:
                return False  # If any non-flashlight light is on, don't show the picture
        
        # If no non-flashlight lights are on, show the picture
        return True

    def init_gl(self):
        """Initialize OpenGL settings"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glEnable(GL_TEXTURE_2D)
        
        # Set up basic lighting
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)
        glEnable(GL_LIGHT3) # Red and intially disabled
        glEnable(GL_LIGHT4) # Green and intially disabled
        glEnable(GL_LIGHT5) # Blue and intially disabled
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 100.0)
        

    def handle_input(self):
        """Handle keyboard and mouse input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r: # Reset Camera to starting point
                    self.camera.eye.x = 0
                    self.camera.eye.y = 5.67
                    self.camera.eye.z = 8
                    # Reset collision point to match the camera's position
                    self.camera.collisionPoint.x = self.camera.eye.x
                    self.camera.collisionPoint.y = self.camera.eye.y
                    self.camera.collisionPoint.z = self.camera.eye.z
                elif event.key == pygame.K_t:  # Reset Vertical Camera position
                    self.camera.heightAngle = INITIAL_LOOK_ANGLE

                elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    light_index = event.key - pygame.K_0
                    self.toggle_light(light_index)
                elif event.key == pygame.K_h: # Prints to console help message
                    self.components.help_message()

        keys = pygame.key.get_pressed()
        moveBack = False
        if keys[pygame.K_w]:
            self.camera.slideCollision(0,0,-0.1) #First move collision box
            #Check and see if a collision occurs with objects, if so flag it
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            #Check and see if wall collision occurs, if so flag it
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True

            #On collision, move collider back onto the player, do not move forward
            if moveBack == True:
                self.camera.slideCollision(0,0,.1)
            else:
                self.camera.slide(0, 0, -0.1)

        if keys[pygame.K_s]:
            self.camera.slideCollision(0,0,0.1) #First move collision box
            #Check and see if a collision occurs with objects, if so flag it
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            #Check and see if wall collision occurs, if so flag it
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True

            #On collision, move collider back onto the player, do not move forward
            if moveBack == True:
                self.camera.slideCollision(0,0,-.1)
            else:
                self.camera.slide(0, 0, 0.1)
        if keys[pygame.K_a]:
            self.camera.slideCollision(-.1,0,0)
            #Check and see if a collision occurs with objects, if so flag it
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            #Check and see if wall collision occurs, if so flag it
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True

            #On collision, move collider back onto the player, do not move forward
            if moveBack == True:
                self.camera.slideCollision(.1,0,0)
            else:
                self.camera.slide(-.1, 0, 0)
        if keys[pygame.K_d]:
            
            self.camera.slideCollision(.1,0,0)
            #Check and see if a collision occurs with objects, if so flag it
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            #Check and see if wall collision occurs, if so flag it
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True

            #On collision, move collider back onto the player, do not move forward
            if moveBack == True:
                self.camera.slideCollision(-.1,0,0)
            else:
                self.camera.slide(.1, 0, 0)
        #Camera turning functions!
        if keys[pygame.K_LEFT]:
            self.camera.turn(1)
        if keys[pygame.K_RIGHT]:
            self.camera.turn(-1) 
        if keys[pygame.K_DOWN]:
            self.camera.rise(-1)
        if keys[pygame.K_UP]:
            self.camera.rise(1)  

        #Pool table control functions 
        if keys[pygame.K_p]:
            if Room.toggleHold != True:
                Room.in_shooting_mode = not Room.in_shooting_mode
                Room.toggleHold = True
        else:
            Room.toggleHold = False
        if keys[pygame.K_j] and Room.in_shooting_mode:
            Room.shooting_angle += 1
        if keys[pygame.K_l] and Room.in_shooting_mode:
            Room.shooting_angle -= 1
        if keys[pygame.K_SPACE] and Room.in_shooting_mode:
            Room.in_shooting_mode = False
            self.components.shoot_cue(Room.shooting_angle)
                 
        #Dice control key
        if keys[pygame.K_x]:
                Room.initial_dice_frame =  Room.global_frame
                Room.animate_dice = True
        #Hanging light control key
        if keys[pygame.K_c]:
            Room.animate_hanging_light = not Room.animate_hanging_light

    #Function sets the animation frames of the room for the dice and light
    def animate(self):

        Room.global_frame += 1

        if Room.animate_dice:
            Room.dice_frame += 1
            if Room.global_frame - Room.initial_dice_frame > 200:
                Room.animate_dice = False
        
        if Room.animate_hanging_light:
            Room.swing_factor = 8
            Room.hanging_light_frame += 1
        else:
            if 0 < Room.swing_factor:
                Room.hanging_light_frame += 1
                Room.swing_factor -= 0.03
            else:
                Room.hanging_light_frame = 0
                    
    #Light orientation method
    def setup_lights(self):

        # Red Light
        if self.light_states['red']:
            red_light = Light(
                light_num=GL_LIGHT0,
                position=[-5, ROOM_HEIGHT - 0.1, -5, 1],
                diffuse=[1.0, 0.0, 0.0, 1.0],
                specular=[1.0, 0.0, 0.0, 1.0]
            )
            red_light.enable()
            self.draw_light_indicator([-5, ROOM_HEIGHT - 0.1, -5], [1.0, 0.0, 0.0])  # Red sphere
        else:
            glDisable(GL_LIGHT0)

        # Green Light
        if self.light_states['green']:
            green_light = Light(
                light_num=GL_LIGHT1,
                position=[5, ROOM_HEIGHT - 0.1, -5, 1],
                diffuse=[0.0, 1.0, 0.0, 1.0],
                specular=[0.0, 1.0, 0.0, 1.0]
            )
            green_light.enable()
            self.draw_light_indicator([5, ROOM_HEIGHT - 0.1, -5], [0.0, 1.0, 0.0])  # Green sphere
        else:
            glDisable(GL_LIGHT1)

        # Blue Light
        if self.light_states['blue']:
            blue_light = Light(
                light_num=GL_LIGHT2,
                position=[0, ROOM_HEIGHT - 0.1, 5, 1],
                diffuse=[0.0, 0.0, 1.0, 1.0],
                specular=[0.0, 0.0, 1.0, 1.0]
            )
            blue_light.enable()
            self.draw_light_indicator([0, ROOM_HEIGHT - 0.1, 5], [0.0, 0.0, 1.0])  # Blue sphere
        else:
            glDisable(GL_LIGHT2)

        # Spotlight
         # Spotlight
        if self.light_states['spotlight']:
            self.spot_light_is_enabled = True
        else:
            self.spot_light_is_enabled = False

        # Desk Lamp
        if self.light_states['lamp']:
            desk_lamp = Light(
                light_num=GL_LIGHT4,
                position=[-ROOM_WIDTH / 2 + 1.3, 5.25, -ROOM_DEPTH / 2 + 1.3, 1],
                diffuse=[0.75, 0.75, 0.75, 1.0],
                specular=[0.75, 0.75, 0.75, 1.0],
                attenuation={"constant": 1.0, "linear": 0.1, "quadratic": 0.0},
                spot_direction=[0, -1, 0],
                spot_cutoff=70.0,
                spot_exponent=1.0
            )
            desk_lamp.enable()
            self.draw_light_indicator([-ROOM_WIDTH / 2 + 1.3, 5.25, -ROOM_DEPTH / 2 + 1.3], [1.0, 1.0, 0.0])  # Yellow sphere
        else:
            glDisable(GL_LIGHT4)

        # Flashlight
        if self.light_states['flashlight']:
            light_num = GL_LIGHT5
            Light.place_flashlight(light_num)
        else:
            glDisable(GL_LIGHT5)


    #Draws the sphere which represents each light
    def draw_light_indicator(self, position, color):
        """
        Draw a self-illuminated sphere at the specified position.
        :param position: The [x, y, z] position of the sphere.
        :param color: The [r, g, b] color of the sphere.
        """
        glPushMatrix()
        glDisable(GL_LIGHTING)  # Disable lighting for the sphere
        glColor3f(*color)  # Set the color of the sphere
        glTranslatef(position[0], position[1], position[2])
        gluSphere(gluNewQuadric(), 0.2, 16, 16)  # Draw a small sphere
        glEnable(GL_LIGHTING)  # Re-enable lighting
        glPopMatrix()

    #Light toggling
    def toggle_light(self, index):
        """Toggle specific light based on index"""
        light_names = ['red', 'green', 'blue', 'spotlight', 'lamp', 'flashlight']
        if index < len(light_names):
            self.light_states[light_names[index]] = not self.light_states[light_names[index]]


    def draw_room(self):
        """Draw the room with textured walls, floor, and ceiling"""
        
        # Set the material to be combined with the textures
        Materials.set_material(GL_FRONT, Materials.BRIGHT_WHITE)
        
        # Floor with checkerboard texture (20 x 20)
        self.textures.set_texture(self.textures.checkerboard_floor_name)

        self.basic_shapes.draw_plane_with_grid(ROOM_WIDTH, ROOM_DEPTH, 30, 30)


        # Walls
        self.textures.set_texture(self.textures.wall_name)
        
        # Back wall
        glPushMatrix()
        glTranslate(0,ROOM_HEIGHT/2,ROOM_DEPTH/2) # Move back and up
        glRotate(270, 1,0,0)
        glRotate(180, 0,1,0)
        self.basic_shapes.draw_plane_with_grid(ROOM_DEPTH, ROOM_HEIGHT,30,30)
        glPopMatrix()

        # Front wall
        glPushMatrix()
        glTranslate(0,ROOM_HEIGHT/2,-ROOM_DEPTH/2) # Move forward and up
        glRotate(90,1,0,0)
        self.basic_shapes.draw_plane_with_grid(ROOM_DEPTH, ROOM_HEIGHT,30,30)
        glPopMatrix()

        # Right wall
        glPushMatrix()
        glRotate(90,0,1,0)
        glTranslate(0,ROOM_HEIGHT/2,ROOM_DEPTH/2)
        glRotate(270, 1,0,0)
        glRotate(180, 0,1,0)
        self.basic_shapes.draw_plane_with_grid(ROOM_DEPTH, ROOM_HEIGHT,30,30)
        glPopMatrix()


        # Left wall
        glPushMatrix()
        glRotate(90,0,1,0)
        glTranslate(0,ROOM_HEIGHT/2,-ROOM_DEPTH/2)
        glRotate(90,1,0,0)
        self.basic_shapes.draw_plane_with_grid(ROOM_DEPTH, ROOM_HEIGHT,30,30)
        glPopMatrix()

        # Ceiling
        glPushMatrix()
        glTranslate(0, ROOM_HEIGHT, 0) # Move up
        glRotate(180,0,0,1)
        self.basic_shapes.draw_plane_with_grid(ROOM_WIDTH, ROOM_DEPTH,30,30)
        glPopMatrix()

    def draw_components(self):

        self.components.draw_animated_pool_table_scene(Room.in_shooting_mode, Room.shooting_angle)
        collisionList.append(Collision(8,4,0,0)) #Create collision box for pool table

        # Place the corner table in the bottom-left corner
        glPushMatrix()  # Save current transformation matrix
        glTranslatef(-ROOM_WIDTH/2 + 1.3, 0, -ROOM_DEPTH/2 + 1.3)  # Move to corner
        self.components.draw_table_with_lamp(2, 2, Room.dice_frame)  # Draw table
        collisionList.append(Collision(2,2,-ROOM_WIDTH/2 +1.3,-ROOM_DEPTH/2 + 1.3)) #Create collision box for table
        glPopMatrix()  # Restore previous transformation matrix

        # Draw a ball around the top of the lamp
        glPushMatrix()  # Save current transformation matrix
        glTranslatef(0, ROOM_HEIGHT - 0.4, 0)  # Move to Center
        Materials.set_material(GL_FRONT_AND_BACK, Materials.RUBBER_BUMPER)
        self.basic_shapes.draw_sphere(0.2)
        glPopMatrix()  # Restore previous transformation matrix

        glPushMatrix()  # Save current transformation matrix
        glTranslatef(0 , ROOM_HEIGHT - 6, 0)  # Move to ceiling
        hanging_light_equation = Room.swing_factor * math.sin(0.03 * Room.hanging_light_frame)
        self.components.draw_animated_hanging_spotlight(hanging_light_equation, self.spot_light_is_enabled, self.global_frame, self.spotlight_state, ROOM_HEIGHT)
        glPopMatrix()  # Restore previous transformation matrix

        if self.show_picture:
            # Add a frame to the back wall
            glPushMatrix()
            glTranslatef(0, ROOM_HEIGHT / 2, -ROOM_DEPTH / 2 + 0.25)  # Center frame on the back wall and move out a little
            glRotatef(90, 0, 0, -1)  # Rotate 90 degrees clockwise around the Z-axis
            glTranslate(-1,0,0) # Move up
            glTranslate(0,3.5,0) # Move to the right
            self.components.draw_framed_picture(3, 1.2, 3)  # Frame size: 3x3   
            glPopMatrix()



    def display(self):
        """Main display function"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        

        self.camera.setProjection()
        self.camera.placeCamera()
        
        self.setup_lights()
        self.show_picture = self.should_we_show_picture()
        self.animate()
        
        self.draw_room()
        self.draw_components()
        
        pygame.display.flip()


    def run(self):
        """Set up Pool Balls"""
        self.components.config_balls()
        """Main game loop"""
        while self.running:
            self.handle_input()
            self.display()
            self.clock.tick(FPS)


def main():
    room = Room()
    room.run()
    pygame.quit()


if __name__ == "__main__":
    main()
"""""
This program can be used to preview an element
It has basic lighting, navigation, and aniamtion set up

Navigation: The 'W' and 'S' keys zoom in and out. The 'D' and 'A' keys rotate side to side. 
The 'I' and 'K' keys rotate up and down. The arrow keys move up or down and side to side.
"""""

import sys
import pygame
from OpenGL.GLU import *
from OpenGL.GL import *
from utils import *
from basic_shapes import *
from components import *
from materials import *
from preview import *
import math
from textures import *

class Preview:
 
    # These parameters define the camera's lens shape
    CAM_NEAR = 0.01
    CAM_FAR = 1000.0
    CAM_ANGLE = 60.0

    # These parameters define simple animation properties
    FPS = 60.0
    DELAY = int(1000.0 / FPS + 0.5)

    # Light positions
    light0_pos = Point(0, 8, 0) # Light source 1 (global coordinates)
    light1_pos = Point(8, 8, 8) # Light source 2 (global coordinates)

    # Global (Module) Variables (ARGH!)
    window_dimensions = (1000, 800)
    name = b'Look At Me, Mom!'
    animate = False
    eye = Point(8, 6, 15)
    look = Point(0, 5, 0)
    # lookD = Vector(Point(0, 0, -1))
    up = Vector(Point(0, 1, 0))  # Usually what you want unless you want a tilted camera
    frame = 0
    turn_degree_x = 0
    turn_degree_y = 0
    view_x = 0
    view_y = 0
    view_z = 0
    ball = gluNewQuadric()
    gluQuadricDrawStyle(ball, GLU_FILL)

    def main():
        Preview.init()

        # Enters the main loop.   
        # Displays the window and starts listening for events.
        Preview.main_loop()
        return

    # Any initialization material to do...
    def init():
        global tube, clock, running

        # pygame setup
        pygame.init()
        pygame.key.set_repeat(300, 50)
        screen = pygame.display.set_mode(Preview.window_dimensions, pygame.DOUBLEBUF|pygame.OPENGL)
        clock = pygame.time.Clock()
        running = True

        tube = gluNewQuadric()
        gluQuadricDrawStyle(tube, GLU_LINE)

        # Set up lighting and depth-test
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)    # Inefficient...
        glEnable(GL_DEPTH_TEST)   # For z-buffering!

    def set_light(light, position):
        """Set up the main lights."""

        amb = [ 0, 0, 0, 1.0 ]  # No ambient light initially
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, amb)

        glMatrixMode(GL_MODELVIEW)
        light_position = [ position.x, position.y, position.z, 1.0 ]
        light_ambient = [ 1.0, 1.0, 1.0, 1.0 ]
        light_diffuse = [ 1.0, 1.0, 1.0, 1.0 ]
        light_specular = [ 1.0, 1.0, 1.0, 1.0 ]


        # For Light 0, set position, ambient, diffuse, and specular values
        glLightfv(light, GL_POSITION, light_position)
        glLightfv(light, GL_AMBIENT, light_ambient)
        glLightfv(light, GL_DIFFUSE, light_diffuse)
        glLightfv(light, GL_SPECULAR, light_specular)

        glEnable(light)

        # This part draws a SELF-COLORED sphere (in spot where light is!)
        glPushMatrix()
        glTranslatef(light_position[0], light_position[1], light_position[2])
        glDisable(GL_LIGHTING)
        glColor3f(1, 1, 1) # White sphere
        gluSphere(gluNewQuadric(), 0.2, 100, 100)
        glPopMatrix()

        glEnable(GL_LIGHTING)



    def light_setup():
        Preview.set_light(GL_LIGHT0, Preview.light0_pos)
        Preview.set_light(GL_LIGHT1, Preview.light1_pos)

    def main_loop():
        global running, clock, animate
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    Preview.keyboard(event)

            if Preview.animate:
                # Advance to the next frame
                Preview.advance()

            # (Re)draw the scene (should only do this when necessary!)
            Preview.display()

            # Flipping causes the current image to be seen. (Double-Buffering)
            pygame.display.flip()

            clock.tick(Preview.FPS)  # delays to keep it at FPS frame rate

    # Callback function used to display the scene
    # Currently it just draws a simple polyline (LINE_STRIP)
    def display():
        # Set the viewport to the full screen
        win_width = Preview.window_dimensions[0]
        win_height = Preview.window_dimensions[1]
        glViewport(0, 0, win_width, win_height)

        # Set view to Perspective Proj. (angle, aspect ratio, near/far planes)
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        
        
        gluPerspective(Preview.CAM_ANGLE, win_width/win_height, Preview.CAM_NEAR, Preview.CAM_FAR)
        Preview.adjust_navigation_position()
        # Clear the Screen
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # And draw the "Scene"
        glColor3f(1.0, 1.0, 1.0)
        Preview.draw_scene()

        # And show the scene
        glFlush()

    # Advance the scene one frame
    def advance():
        global frame
        Preview.frame += 1

    # Function used to handle any key events
    # event: The keyboard event that happened
    def keyboard(event):
        global is_red, running, animate, turn_degree_x, turn_degree_y, view_x, view_y, view_z
        key = event.key # "ASCII" value of the key pressed
        if key == 27:  # ASCII code 27 = ESC-key
            running = False
        elif key == ord(' '):
            Preview.animate = not Preview.animate
        elif key == pygame.K_LEFT:
            # Move left
            Preview.view_x += 1
        elif key == pygame.K_RIGHT:
            # Move right
            Preview.view_x -= 1
        elif key == pygame.K_UP:
            # Go up
            Preview.view_y -= 1
        elif key == pygame.K_DOWN:
            # Go down
            Preview.view_y += 1            
        elif key == ord('w'):
            # Zoom in
            Preview.view_z += 1
        elif key == ord('s'):
            # Zoom out
            Preview.view_z -= 1
        elif key == ord('a'):
            # tilt left
            Preview.turn_degree_x +=1
        elif key == ord('d'):
            # tilt right
            Preview.turn_degree_x -= 1
        elif key == ord('i'):
            # Tilt forward
            Preview.turn_degree_y += 1
        elif key == ord('k'):
            # Tilt backward
            Preview.turn_degree_y -= 1
            
    # Adjust the navigation bsed on the keyboard input
    def adjust_navigation_position():
        moveSpeed = 0.2
        glTranslatef(Preview.view_x*moveSpeed,Preview.view_y*moveSpeed,Preview.view_z*moveSpeed)

    def adjust_navigation_tilt():
        tiltSpeed = 1
        glRotated(Preview.turn_degree_x*tiltSpeed,0,1,0)
        glRotated(Preview.turn_degree_y*tiltSpeed,1,0,0)


    def draw_scene():
        """
        * draw_scene:
        *    Draws a simple scene with a few shapes
        """
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        
        # Place the camera
        #   eye = camera's origin (POINT)
        #   look = camera's look at (POINT)
        #   up   = roughly upwards (VECTOR)
        gluLookAt(Preview.eye.x, Preview.eye.y, Preview.eye.z,
                #   eye.x + lookD.dx, eye.y + lookD.dy, eye.z + lookD.dz,
                Preview.look.x, Preview.look.y, Preview.look.z,
                Preview.up.dx, Preview.up.dy, Preview.up.dz)
        # print("Matrix after the transformation from Camera to World Space")
        # printMatrix()
        
        # Now transform the world
        Preview.adjust_navigation_tilt()
        Preview.light_setup()
        Preview.draw()


    # Draw the element here
    def draw():

        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

        # Draw coordinate frame
        Materials.set_material(GL_FRONT_AND_BACK, Materials.SILVER)
        BasicShapes.draw_coordinate_frame()

        # Set the material
        Materials.set_material(GL_FRONT_AND_BACK, Materials.REDDISH_WOOD)

        # Preview the element

        # Components.draw_elegant_table(2,2)
        # Components.draw_table_with_lamp(2,2)
        # Components.draw_light_bulb()

        BasicShapes.draw_plane_with_grid(1,5,3,3)
        # Components.draw_animated_pool_table_scene(True, 0)
        # Components.draw_frame(3, 0.1, 3)

        # Components.draw_hanging_spotlight()

        # glTranslate(0, 3, 0)
        # Components.draw_hanging_spotlight()

        # Materials.set_material(GL_FRONT_AND_BACK, Materials.BALL_PLASTIC)
        # Components.draw_4ball()

        # Materials.set_material(GL_FRONT_AND_BACK, Materials.SILVER)
        # Components.draw_1ball()

        # Materials.set_material(GL_FRONT_AND_BACK, Materials.EMERALD)
        # Components.draw_dice()

        # Materials.set_material(GL_FRONT_AND_BACK, Materials.SILVER)
        # Components.draw_ball()

        

    if __name__ == '__main__': main()

"""
This class contains the functions that draw the components in our scene
with functions such as draw_pool_table(), draw_dice(), etc.
"""

from OpenGL.GLU import *
from OpenGL.GL import *
from basic_shapes import *
from materials import *
from pool_ball import *
import random
from pool_ball import PoolBall
from utils import *
#Global Variables, needed for pool ball functions
global ball_1, ball_2, ball_3, ball_4, cue_ball, eight_ball, angle, balls

class Components:

    def __init__(self, textures, basic_shapes):
        self.textures = textures
        self.basic_shapes = basic_shapes

    
    #==============================
    # Table functions
    #==============================


    def draw_elegant_table(self, length, width, texture=None):
        glPushMatrix() 

        if texture:  # Apply the texture if provided
            self.textures.set_texture(texture)

        glTranslatef(0, 2.5, 0)  # Move up from the ground
        self.basic_shapes.draw_rectangle_with_grid(length, width, 0.5,5,20)  # Draw surface
        glTranslatef(0, -2.5, 0)  # Move back down

        percent_length = length * 0.75
        percent_width = width * 0.75

        glTranslatef(percent_length / 2, 0, percent_width / 2)
        self.draw_elegant_table_leg(texture)  # Pass the texture to the legs
        glTranslatef(-percent_length, 0, 0)
        self.draw_elegant_table_leg(texture)
        glTranslatef(0, 0, -percent_width)
        self.draw_elegant_table_leg(texture)
        glTranslatef(percent_length, 0, 0)
        self.draw_elegant_table_leg(texture)
        glPopMatrix()


    def draw_elegant_table_leg(self, texture=None):
        glPushMatrix()  # Save current matrix
        
        if texture:  # Apply the texture if provided
            self.textures.set_texture(texture)

        # Draw main part of leg
        self.basic_shapes.draw_rectangle(0.125, 0.125, 2.5)
        
        # Draw the designs (pyramids and a sphere)
        self.basic_shapes.draw_pyramid(0.5, 0.5)

        glTranslatef(0, 1, 0)  # Move up from the ground
        glRotated(180, 1, 0, 0)  # Rotate
        self.basic_shapes.draw_pyramid(0.5, 0.5)
        glRotated(-180, 1, 0, 0)  # Rotate back
        self.basic_shapes.draw_pyramid(0.5, 0.5)

        glTranslatef(0, 0.5, 0)  # Move up more
        if texture:  # Apply texture for the sphere
            self.textures.set_texture(texture)
        self.basic_shapes.draw_sphere(0.25)

        glTranslatef(0, 1, 0)  # Move up more
        glRotated(180, 1, 0, 0)  # Rotate
        self.basic_shapes.draw_pyramid(0.5, 0.5)

        glPopMatrix()


    #==============================
    # Lamp functions
    #==============================

    def draw_lamp_shade(self, height):
        self.basic_shapes.draw_adjustable_cylinder(height, height/2, height) # bottom_radius, top_radius, height

    def draw_lamp_base(self):
        """Draws the lamp base with two stacked spheres."""
        glPushMatrix()
        
        # Bottom sphere (larger)
        self.basic_shapes.draw_sphere(radius=2.0)  # Radius of the larger sphere

        # Top sphere (smaller, stacked above)
        glTranslatef(0, 3, 0)  # Move up by the radius of the bottom sphere + some offset
        self.basic_shapes.draw_sphere(radius=1.5)  # Radius of the smaller sphere

        glPopMatrix()

    def draw_lamp(self):
        """Draws the complete lamp (base + shade)."""
        glPushMatrix()

        # Draw the base (two spheres)
        Materials.set_material(GL_FRONT_AND_BACK, Materials.GOLD)
        self.draw_lamp_base()

        # Draw the lamp shade
        glTranslatef(0, 6, 0)  # Move above the smaller sphere (base height + offset for stacking)
        self.draw_lamp_shade(height=3.0)  # Adjust height as needed
        # Materials.set_material(GL_FRONT_AND_BACK, Materials.LIGHTBULB)
        # self.draw_light_bulb()

        glPopMatrix()

    def draw_animated_hanging_spotlight(self, angle, is_on, frame_count, spotlight_state, ROOM_HEIGHT):
        glPushMatrix()

        glTranslate(0,6,0) # Go to the top of the light
        glRotate(angle, 0, 0, 1)
        glTranslate(0,-6,0) # Go back down

        self.draw_hanging_spotlight(is_on, frame_count, spotlight_state, ROOM_HEIGHT)

        glPopMatrix()




    def draw_hanging_spotlight(self, is_on, frame_count, spotlight_state, ROOM_HEIGHT):
        glPushMatrix()

        self.setup_spotlight_lighting(is_on, frame_count, spotlight_state, ROOM_HEIGHT)

        # Draw lightbulb
        glTranslate(0,-0.5,0)
        Materials.set_material(GL_FRONT_AND_BACK, Materials.LIGHTBULB)
        self.basic_shapes.draw_sphere(radius=0.15)  # Small sphere for the bulb
        glTranslate(0,0.5,0)

        Materials.set_material(GL_FRONT_AND_BACK, Materials.SILVER)

        # Ceiling attachment
        self.basic_shapes.draw_cylinder(1/12, 6) #radius, height

        #Spotlight shade
        glTranslate(0,-2,0)
        self.basic_shapes.draw_adjustable_cylinder(2, 1/12, 2) # bottom_radius, top_radius, height

        glPopMatrix()


    def setup_spotlight_lighting(self, is_on, frame_count, spotlight_state, ROOM_HEIGHT):
        """
        Set up the spotlight with smoother flickering and occasional darkness.
        :param is_on: Whether the spotlight is initially enabled.
        :param frame_count: The current frame count (used to control flickering).
        """
        light_num = GL_LIGHT3


        if frame_count % 60 == 0:  # Update every second
            if random.random() < 0.3:  # 30% chance to turn off completely
                spotlight_state["target_intensity"] = 0.0
            else:
                spotlight_state["target_intensity"] = 0.5  # Fully on after a reset

        # Uniform flickering logic
        if spotlight_state["target_intensity"] != 0.0:
            if frame_count % 30 < 15:  # On for 15 frames, off for 15 frames (flickers once per second at 60 FPS)
                spotlight_state["current_intensity"] = 0.5  # Fully on
            else:
                spotlight_state["current_intensity"] = 0.2  # Dimmer
        else:
            spotlight_state["current_intensity"] = 0.0  # Stay off when "target_intensity" is 0.0

        # Smooth transition to target intensity
        spotlight_state["current_intensity"] += (
            spotlight_state["target_intensity"] - spotlight_state["current_intensity"]
        ) * 0.1
        spotlight_state["current_intensity"] = max(0.0, min(spotlight_state["current_intensity"], 0.5))  # Clamp to [0, 0.5]



        # Set the light properties
        if is_on and spotlight_state["current_intensity"] > 0.0:
            glEnable(light_num)
            glLightfv(light_num, GL_POSITION, [0, ROOM_HEIGHT - 8, 0, 1])
            glLightfv(light_num, GL_DIFFUSE, [
                spotlight_state["current_intensity"],
                spotlight_state["current_intensity"],
                spotlight_state["current_intensity"] / 2,
                1.0
            ])
            glLightfv(light_num, GL_SPECULAR, [
                spotlight_state["current_intensity"],
                spotlight_state["current_intensity"],
                spotlight_state["current_intensity"] / 2,
                1.0
            ])
            glLightfv(light_num, GL_SPOT_DIRECTION, [0, -1, 0])
            glLightf(light_num, GL_SPOT_CUTOFF, 9.0)
            glLightf(light_num, GL_SPOT_EXPONENT, 0.0)
            glLightf(light_num, GL_CONSTANT_ATTENUATION, 1.0)
            glLightf(light_num, GL_LINEAR_ATTENUATION, 0.01)
            glLightf(light_num, GL_QUADRATIC_ATTENUATION, 0.00)
        else:
            glDisable(light_num)

    def draw_light_bulb(self):
        """Draws a small light bulb inside the lamp shade."""
        glPushMatrix()
        glTranslatef(0, 1.5, 0)  # Position inside the lamp shade
          # Set up light source at the bulb
        self.setup_lightbulb_lighting()
        self.basic_shapes.draw_sphere(radius=0.5)  # Small sphere for the bulb
        glPopMatrix()


    def draw_table_with_lamp(self, table_length, table_width, dice_frame):
        """Draws a table with a lamp placed on top, scaling the lamp down."""
        glPushMatrix()

        # Draw the table
        Materials.set_material(GL_FRONT_AND_BACK, Materials.REDDISH_WOOD)
        # self.textures.set_texture(self.textures.wood_two)
        self.draw_elegant_table(table_length, table_width, self.textures.wood_two_texture)

        # Position and scale the lamp
        glPushMatrix()
        glTranslatef(0, 3, 0)  # Move the lamp up to the surface of the table
        glScalef(0.3, 0.3, 0.3)  # Scale the lamp down (adjust the factors as needed)
        self.draw_lamp()  # Draw the lamp
        glPopMatrix()

        # Position and draw the dice
        glPushMatrix()
        glTranslate(0.6,3,0.3)
        self.draw_animated_die(dice_frame)
        glTranslate(-0.1,0,0.3)
        glRotate(30, 0,1,0)
        self.draw_animated_die(dice_frame)
        glPopMatrix()
        
        glPopMatrix()

    #==============================
    # Colored Light functions
    #==============================
    
    def draw_red_ball(self):
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT, [1.0, 0.0, 0.0, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 0.0, 0.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 0.0, 0.0, 1.0])
        self.basic_shapes.draw_sphere(0.2)
        glPopMatrix()

    #==============================
    # Help Message
    #==============================    

    def help_message(self):
        print("Hi! The controls are as follows:\nPress \"W\" to move forward\nPress \"S\" to move backward")
        print("Press \"A\" to move to the left\nPress \"D\" to move to the right")
        print("Press the Up Arrow key to look up\nPress the Down Arrow key to look down\nPress the Left Arrow key to look left")
        print("Press the Right Arrow key to look right\nPress \"R\" to reset to starting position\nPress \"T\" to reset camera's vertical position")
        print("Press 0 to turn the red light on/off\nPress 1 to turn the green light on/off\nPress 2 to turn the blue light on/off")
        print("Press 3 to turn the spotlight light on/off\nPress 4 to turn the desk light on/off\nPress 5 to turn the flashlight on/off")
        print("Press \"X\" to spin the dice\nPress \"C\" to swing the lamp and press again for it to slow to a stop")
        print("Press \"P\" to enter Pool mode\nOnce in Pool mode, press \"J\" and \"L\" to aim the ball \nPress the space bar to shoot the ball")
        
    #==============================
    # Cue Sticks
    #==============================

    def draw_cue_stick(self):
        self.basic_shapes.draw_adjustable_cylinder(0.0984, 0.0426, 4.57) # bottom_radius, top_radius, height

    #==============================
    # Ball functions
    #==============================

    def draw_1ball(self):
        glPushMatrix()
        self.basic_shapes.draw_sphere(0.186)
        glPopMatrix()

    def draw_rotated_1ball(self, rotate_x, rotate_y, rotate_z):
        glPushMatrix()
        self.basic_shapes.draw_rotated_sphere(0.186, rotate_x, rotate_y, rotate_z)
        glPopMatrix()

    def draw_4ball(self):
        glPushMatrix()
        # Move to the left for the second ball
        glTranslatef(-0.5, 0, 0.5)
        self.basic_shapes.draw_sphere(0.186)
        
        # Move to the right for the third ball
        glTranslatef(1.0, 0, 0)
        self.basic_shapes.draw_sphere(0.186)
        
        # Move to the left for the fourth ball
        glTranslatef(-1.0, 0, 0.5)
        self.basic_shapes.draw_sphere(0.186)
        
        # Move to the right for the fifth ball
        glTranslatef(1.0, 0, 0)
        self.basic_shapes.draw_sphere(0.186)
        glPopMatrix()

    #==============================
    # Dice functions
    #==============================

    def draw_die(self): 
        face_textures = [ 
            self.textures.die_one_name,
            self.textures.die_two_name,
            self.textures.die_three_name,
            self.textures.die_four_name,
            self.textures.die_five_name,
            self.textures.die_six_name
        ]
        glPushMatrix()
        # self.basic_shapes.draw_cube(0.10, 0.10, 0.10, self.textures face_textures)
        Materials.set_material(GL_FRONT_AND_BACK, Materials.BALL_PLASTIC)
        self.basic_shapes.draw_cube(0.167, 0.167, 0.167, self.textures, face_textures) # 2 inch length
        glPopMatrix()

    def draw_animated_die(self, frame):
        glPushMatrix()

        
        glRotate(frame,0,1,0)
        self.draw_die()

        glPopMatrix()

       

    """ def draw_dice():
        glPushMatrix()
        glTranslatef(1, 0, 0)
        self.basic_shapes.draw_cube(0.10, 0.10, 0.10, self.textures)
        glTranslatef(0.13, 0, 0)
        glPopMatrix() """
    
       
    #==============================
    # Pool table functions
    #==============================

    # Draws a pool table that is 8 units long, 4 units wide, and 3.08 units tall (aprox. 3 ft 1 in)
    def draw_pool_table(self):
        glPushMatrix()
        
        length=8 
        width=4

        # Draw the main table
        self.draw_elegant_table(length, width, self.textures.wood_one_texture)
        
        self.textures.set_texture(self.textures.wood_one_texture) # Set the texture
        glTranslatef(0, 1.5, 0)  # Move up from the ground
        self.basic_shapes.draw_rectangle_with_grid(7.7,3.7,1, 8,20) # Draw the trim

        glTranslatef(0, 1.5, 0)  # Move up more
        Materials.set_material(GL_FRONT, Materials.GREEN_FELT) # Set the material
        self.basic_shapes.draw_rectangle(7.7,3.7,0.08) # Draw the felt


        # Draw the bumper
        Materials.set_material(GL_FRONT, Materials.RUBBER_BUMPER) # Set the material

        glPushMatrix()
        glTranslatef(-7.7/2, 0, 0)  # Move to the side
        self.basic_shapes.draw_rectangle(0.3, 4, 0.2)
        glTranslatef(7.7, 0, 0)  # Move to the other side
        self.basic_shapes.draw_rectangle(0.3, 4, 0.2)
        glPopMatrix()
        glTranslatef(0, 0, (3.7/2))  # Move back
        self.basic_shapes.draw_rectangle(8, 0.3, 0.2)
        glTranslatef(0, 0, - (3.7))  # Move forward
        self.basic_shapes.draw_rectangle(8, 0.3, 0.2)


        glPopMatrix()

    
    def draw_static_pool_table_scene(self):
        glPushMatrix()
        
        self.draw_pool_table()

        glTranslatef(0, 3.08, 0)  # Move up from the ground

        # Draw the balls
        Materials.set_material(GL_FRONT, Materials.SILVER) # Set the material
        glTranslatef(-1.2, 0, 1.2)
        self.draw_1ball()
        glTranslatef(1.6, 0, -1.1)
        self.draw_1ball()
        glTranslatef(1.3, 0, -1.5)
        self.draw_1ball()
        glTranslatef(-1.9, 0, 0.8)
        self.draw_1ball()

        # Draw the Q balls
        Materials.set_material(GL_FRONT, Materials.BALL_RESIN) # Set the material
        glTranslatef(-2.2, 0, 0.2)
        self.draw_1ball()

        # Draw the 8 ball
        self.textures.set_texture(self.textures.eight_ball_texture) # Set the texture
        glTranslatef(4, 0, 0)
        self.draw_rotated_1ball(100,0,0)

        glPopMatrix()

    
    def draw_animated_pool_table_scene(self, in_shooting_mode, shooting_angle):
        global ball_1, ball_2, ball_3, ball_4, cue_ball, eight_ball, angle, balls
        angle = shooting_angle
        glPushMatrix()

        # Set the material for the table and cue stick
        Materials.set_material(GL_FRONT, Materials.BALL_PLASTIC)

        # Place and draw the cue stick
        glPushMatrix()
        glTranslate(0,-1.5,0)
        glRotate(-17.7,0,0,1)
        glTranslate(-5.3,0,-1)
        self.textures.set_texture(self.textures.wood_one_texture)
        self.draw_cue_stick()
        glPopMatrix()
        self.draw_pool_table()
        glTranslatef(0, 3.08, 0)  # Move up from the ground
        # Draw the balls
        ball_1.draw()
        ball_2.draw()
        ball_3.draw()
        ball_4.draw()
        eight_ball.draw()
        cue_ball.draw()

        for i in range(len(balls)):
            for j in range(i+1, len(balls)):
                pos1 = (balls[i][0].position_x, balls[i][0].position_z)
                pos2 = (balls[j][0].position_x, balls[j][0].position_z)
                isMoving = balls[i][0].power != 0
                noCooldown = balls[i][1] == 0 and balls[j][1] == 0
                if math.dist(pos1,pos2)< 2 * balls[i][0].radius and isMoving and noCooldown:
                    #Set 1/12 second cooldown to prevent repeat collisions
                    balls[i][1] = 5
                    balls[j][1] = 5

                    #Calculate the instance vector for carrying movement
                    diffX = balls[j][0].position_x - balls[i][0].position_x
                    diffZ = balls[j][0].position_z - balls[i][0].position_z
                    instVector = Vector(diffX, 0, diffZ)
                    instVector.normalize()
                    balls[j][0].changeDirection(instVector)
                    

                    #Next, calculate the power of both colliding pool balls
                    #Note: Magnitude of the direction vectors is 1, simplifying calculation
                    dotProduct = balls[i][0].direction.dx * balls[j][0].direction.dx + balls[i][0].direction.dz * balls[j][0].direction.dz
                    pathAngle = math.degrees(math.acos(dotProduct))

                    balls[i][0].power = balls[i][0].power * pathAngle / 90
                    balls[j][0].power = balls[i][0].power * (90 - pathAngle)/90

                    #Finally, calculate the new direction of the original ball, noting edge cases when going below 0 degrees
                    if (balls[i][0].getAngle() % 360 < balls[j][0].getAngle() %360) or (balls[i][0].getAngle() % 360 > 270 and balls[j][0].getAngle() % 360 < 90):
                        desiredAngle = balls[i][0].getAngle() - 90
                    else:
                        desiredAngle = balls[i][0].getAngle() + 90
                    #Set new direction for original ball
                    desiredVector = Vector(math.cos(math.radians(desiredAngle)),0,math.sin(math.radians(desiredAngle)))
                    balls[i][0].changeDirection(desiredVector)
            #Lower Cooldowns by 1 for all collisions
            if balls[i][1] > 0:
                balls[i][1] -= 1

        #Draw the dashed lines for the cue ball
        if in_shooting_mode:
            PoolBall.draw_dash(cue_ball, shooting_angle, 1, self.basic_shapes)

        glPopMatrix()

    #Sets initial state for the pool balls
    def config_balls(self):
        global ball_1, ball_2, ball_3, ball_4, cue_ball, eight_ball, balls
        # Create the balls
        ball_1 = PoolBall(False, None, False, self.textures, self.basic_shapes) # has_texture, texture_name, is_cue
        ball_2 = PoolBall(False, None, False, self.textures, self.basic_shapes) 
        ball_3 = PoolBall(False, None, False, self.textures, self.basic_shapes) 
        ball_4 = PoolBall(False, None, False, self.textures, self.basic_shapes)
        eight_ball = PoolBall(True, self.textures.eight_ball_texture, False, self.textures, self.basic_shapes)
        cue_ball = PoolBall(False, None, True, self.textures, self.basic_shapes)


        # Configure the balls
        ball_1.set_config(0.5, 0.3, 0, 0) # position_x, position_z, rotation_x, rotation_z
        ball_2.set_config(-0.3, 1, 0, 0)
        ball_3.set_config(1, 0.8, 0, 0)
        ball_4.set_config(-0.6, -1.2, 0, 0)
        eight_ball.set_config(0.3, 0.7, 100, 0)
        cue_ball.set_config(-2, 0, 0, 0)

        #Place balls in a list, with cooldown collisions: Needed for ball movement and interactions
        balls = [[cue_ball, 0], [ball_1, 0], [ball_2, 0], [ball_3, 0], [ball_4,0], [eight_ball, 0]]
        
    #Takes the shooting angle from Room, then pushes the cue_ball in that direction
    def shoot_cue(self, shootingAngle):
        cue_ball.direction.dx = math.cos(math.radians(shootingAngle))
        cue_ball.direction.dz = -math.sin(math.radians(shootingAngle))
        cue_ball.power = .4
    #Method which draws the picture for the room

    def draw_picture(self, length, frame_width, height):
        
        glPushMatrix()
        # self.basic_shapes.draw_cube(0.10, 0.10, 0.10, self.textures face_textures)
        Materials.set_material(GL_FRONT, Materials.BALL_PLASTIC)
        self.textures.set_texture(self.textures.wall_photo_name)

        glTranslate(0,length/2,frame_width/2)
        glRotate(90, 1,0,0)
        glRotate(90, 0,1,0)
        self.basic_shapes.draw_plane_with_grid(length, height, 5,5)
        glPopMatrix()

    def draw_framed_picture(self, length, width, height):
        glPushMatrix()

        self.draw_picture(length, width, height)


        Materials.set_material(GL_FRONT, Materials.BALL_PLASTIC)
        self.textures.set_texture(self.textures.wood_two_texture)
        glTranslate(0, -0.25, 0) # Go to bottom of picture
        self.basic_shapes.draw_rectangle_with_grid(height, width, 0.25, 5,5)
        glTranslate(0, length + 0.25, 0) # Go to top
        self.basic_shapes.draw_rectangle_with_grid(height, width, 0.25, 5,5)
        glTranslate(0, -(length+0.25), 0) # Go to bottom
        glTranslate(-(length/2 + 0.125), 0, 0) # Go to left
        self.basic_shapes.draw_rectangle_with_grid(0.25, width, height + 0.5, 5,5)
        glTranslate(length + 0.25, 0, 0) # Go to right
        self.basic_shapes.draw_rectangle_with_grid(0.25, width, height + 0.5, 5,5)

        glPopMatrix()






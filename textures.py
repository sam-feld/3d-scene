"""""
This class handles loading and storing textures for our project and includes a setter method.
It simplifies the process of applying textures to objects in the scene.
"""""

import sys
import math
import pygame
from OpenGL.GLU import *
from OpenGL.GL import *
from camera import *
from utils import *
from basic_shapes import *
from components import *
from materials import *
from PIL import Image

class Textures:
            
    #=================================================
    # A method for assigning an already loaded texture
    #=================================================

    def set_texture(self, texture_name):
        # print(f"Binding texture {texture_name}")

        glBindTexture(GL_TEXTURE_2D, texture_name)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE) # try GL_DECAL/GL_REPLACE/GL_MODULATE
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)           # try GL_NICEST/GL_FASTEST
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)  # try GL_CLAMP/GL_REPEAT/GL_CLAMP_TO_EDGE
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # try GL_LINEAR/GL_NEAREST
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        # Enable/Disable each time or OpenGL ALWAYS expects texturing!
        glEnable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

    #==============================
    # Initial texture setup
    #==============================

    # Texture data
    wood_two_file = "textures/wood2.jpeg"
    wood_one_file = "textures/wood1.jpeg"
    eight_ball_file = "textures/eight_ball.jpeg"
    die_one = "textures/1side.jpg"
    die_two = "textures/2side.jpg"
    die_three = "textures/3side.jpg"
    die_four = "textures/4side.jpg"
    die_five = "textures/5side.jpg"
    die_six = "textures/6side.jpg"
    wall_photo = "textures/teapot.jpg"
    wood_panel_file = "textures/wood_panel.jpeg"
    ceiling_file = "textures/ceiling.jpeg"
    wall_file = "textures/wall.jpeg"

    eight_ball_texture = None
    wood_one_texture = None
    checkerboard_texture_name = None
    wood_two_texture = None
    die_one_name = None
    die_two_name = None
    die_three_name = None
    die_four_name = None
    die_five_name = None
    die_six_name = None
    wall_photo_name = None
    wood_panel_name = None
    ceiling_name = None
    wall_name = None

    checkerboard_floor_name = None
    
    def __init__(self):

        # pygame setup (no reoson for it to be in the code, but there's an error when it's removed: zsh: segmentation fault)
        screen = pygame.display.set_mode((1200, 800), pygame.DOUBLEBUF|pygame.OPENGL)

        # Create a texture
        self.checkerboard_floor_name = self.create_checkerboard_texture_adjustable()

        # Load the rest of the textures from images
        self.texture_array = glGenTextures(13)  # Texture names for all textures to create
        self.eight_ball_texture = self.texture_array[0]
        self.wood_one_texture = self.texture_array[1]
        self.wood_two_texture = self.texture_array[2]
        self.die_one_name = self.texture_array[3]
        self.die_two_name = self.texture_array[4]
        self.die_three_name = self.texture_array[5]
        self.die_four_name = self.texture_array[6]
        self.die_five_name = self.texture_array[7]
        self.die_six_name = self.texture_array[8]
        self.wall_photo_name = self.texture_array[9]
        self.wood_panel_name = self.texture_array[10]
        self.ceiling_name = self.texture_array[11]
        self.wall_name = self.texture_array[12]

        self.load_texture(self.eight_ball_texture, self.eight_ball_file, (0,0,512,512))
        self.load_texture(self.wood_one_texture, self.wood_one_file, (0,0,512,512))
        self.load_texture(self.wood_two_texture, self.wood_two_file, (0,0,512,512))
        self.load_texture(self.die_one_name, self.die_one)
        self.load_texture(self.die_two_name, self.die_two)
        self.load_texture(self.die_three_name, self.die_three)
        self.load_texture(self.die_four_name, self.die_four)
        self.load_texture(self.die_five_name, self.die_five)
        self.load_texture(self.die_six_name, self.die_six)
        self.load_texture(self.wall_photo_name, self.wall_photo)
        self.load_texture(self.wood_panel_name, self.wood_panel_file)
        self.load_texture(self.ceiling_name, self.ceiling_file)
        self.load_texture(self.wall_name, self.wall_file)

    def create_checkerboard_texture_adjustable(self, size=128, checker_size=8):
        """
        Create a checkerboard texture with sharp edges.
        :param size: Size of the texture (e.g., 128x128 pixels).
        :param checker_size: Size of each checker square in pixels.
        :return: OpenGL texture ID for the checkerboard texture.
        """
        # Generate a new texture ID
        texture = glGenTextures(1)

        # Bind the texture so subsequent calls affect this texture
        glBindTexture(GL_TEXTURE_2D, texture)

        # Create the checkerboard pattern
        data = []
        for i in range(size):
            for j in range(size):
                if ((i // checker_size) + (j // checker_size)) % 2 == 0:
                    data.extend([255, 255, 255])  # White square
                else:
                    data.extend([0, 0, 0])  # Black square

        # Convert the list to bytes (OpenGL expects bytes for texture data)
        data = bytes(data)

        # Specify the texture parameters and upload the texture data to OpenGL
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data
        )

        # Set texture filtering to nearest-neighbor for sharp edges
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        return texture



    def create_checkerboard_texture(self):
        # Professor Duncan told in the project that we need a checkerboard pattern for the floor so for that
        # First, we ask OpenGL to give us a new texture (Think of it like wallpaper or gift wrapping paper that you apply to an object.) ID (like getting a new blank canvas)
        texture = glGenTextures(1)
        # Tell OpenGL we want to work on this texture (like picking up our canvas to draw on it)
        glBindTexture(GL_TEXTURE_2D, texture)
        
        size = 64
        checker_size = 8
        # Each checker square will be 8x8 pixels
        # This list will hold all our colors (we'll fill it with numbers for black and white)
        data = []
        # The Logic:
            # 1. We have a big 64x64 pixel image
            # 2. We want to make checker squares that are 8x8 pixels each
            # 3. So our image will have 8 checker squares across and 8 down (64 ÷ 8 = 8)
            # 4. When the texture repeats 4 times on the floor, we'll see 32x32 checker squares!
        
        # Loop through each pixel in our 64x64 image
        for i in range(size): # 0-63 rows iterate
            for j in range(size):  #0-63 columns
            # i // checker_size -> Divides row number by 8, dropping the remainder
            # j // checker_size -> Divides column number by 8, dropping the remainder
            # When we add these and check if the sum is odd or even,
            # we get alternating squares!
            
            # Example:
            # For pixel (0,0):  0//8 + 0//8 = 0 + 0 = 0 (even = white)
            # For pixel (0,8):  0//8 + 8//8 = 0 + 1 = 1 (odd = black)
            # For pixel (8,0):  8//8 + 0//8 = 1 + 0 = 1 (odd = black)
            # For pixel (8,8):  8//8 + 8//8 = 1 + 1 = 2 (even = white)
                if ((i // checker_size) + (j // checker_size)) % 2:
                    # If the sum is odd, make this pixel black
                    data.extend([0, 0, 0])  # Black square
                else:
                    # If the sum is even, make this pixel white
                    data.extend([255, 255, 255])  # White square
        # Convert our list of numbers to bytes (the format OpenGL expects)            
        data = bytes(data)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        # Tell OpenGL how to handle the texture when it's stretched or shrunk
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return texture


    def load_rotate_and_stretch_texture(self, texture_name, file_name, rotation, new_width, new_height):
        # Load the image. Crop if requested (should be a 4-tuple: e.g. (0,0,128,128)
        im = Image.open(file_name)
        # print("Image dimensions: {0}".format(im.size))  # If you want to see the image's original dimensions
        
        im = im.rotate(rotation)

        im = im.resize((new_width, new_height))
        
        if im.mode != "RGB":
         im = im.convert("RGB")


        dimX = im.size[0]
        dimY = im.size[1]
        texture = im.tobytes("raw", "RGB")

        glBindTexture(GL_TEXTURE_2D, texture_name)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, dimX, dimY, 0, GL_RGB,
                    GL_UNSIGNED_BYTE, texture)
        
    def load_texture(self, texture_name, file_name, crop_dimensions=None):
        # Load the image. Crop if requested (should be a 4-tuple: e.g. (0,0,128,128)
        im = Image.open(file_name)
        # print("Image dimensions: {0}".format(im.size))  # If you want to see the image's original dimensions
        if crop_dimensions != None:
            # We are asked to crop the texture
            im = im.crop(crop_dimensions)
        
        if im.mode != "RGB":
         im = im.convert("RGB")


        dimX = im.size[0]
        dimY = im.size[1]
        texture = im.tobytes("raw", "RGB")

        glBindTexture(GL_TEXTURE_2D, texture_name)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, dimX, dimY, 0, GL_RGB,
                    GL_UNSIGNED_BYTE, texture)

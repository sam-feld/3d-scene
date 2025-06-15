"""
Light Class for Managing OpenGL Lights

This class encapsulates OpenGL light properties and behaviors, 
allowing for the creation, configuration, and management of 
light objects in the project. 
"""

from OpenGL.GL import *
from OpenGL.GLU import *

class Light:
    def __init__(self, light_num, position, diffuse, specular, attenuation=None, spot_direction=None, spot_cutoff=None, spot_exponent=None):
        self.light_num = light_num
        self.position = position
        self.diffuse = diffuse
        self.specular = specular
        self.attenuation = attenuation or {"constant": 1.0, "linear": 0.01, "quadratic": 0.001}
        self.spot_direction = spot_direction
        self.spot_cutoff = spot_cutoff
        self.spot_exponent = spot_exponent

    def enable(self):
        """Enable and configure the light."""
        glEnable(self.light_num)
        glLightfv(self.light_num, GL_POSITION, self.position)
        glLightfv(self.light_num, GL_DIFFUSE, self.diffuse)
        glLightfv(self.light_num, GL_SPECULAR, self.specular)

        # Apply distance attenuation if provided
        glLightf(self.light_num, GL_CONSTANT_ATTENUATION, self.attenuation["constant"])
        glLightf(self.light_num, GL_LINEAR_ATTENUATION, self.attenuation["linear"])
        glLightf(self.light_num, GL_QUADRATIC_ATTENUATION, self.attenuation["quadratic"])

        # Apply spotlight settings if applicable
        if self.spot_direction:
            glLightfv(self.light_num, GL_SPOT_DIRECTION, self.spot_direction)
        if self.spot_cutoff:
            glLightf(self.light_num, GL_SPOT_CUTOFF, self.spot_cutoff)
        if self.spot_exponent:
            glLightf(self.light_num, GL_SPOT_EXPONENT, self.spot_exponent)

    def disable(self):
        """Disable the light."""
        glDisable(self.light_num)


    def place_flashlight(light_num):
        """Creates a (spotlight) flashlight near the viewer/camera"""
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        light_position = [ 0.2, -0.5, 0.0, 1.0 ]
        light_direction = [ 0.0, 0.0, 0.0, 0.0]
        light_ambient = [ 1.0, 1.0, 1.0, 1.0 ]
        light_diffuse = [ 1.0, 1.0, 1.0, 1.0 ]
        light_specular = [ 1.0, 1.0, 1.0, 1.0 ]

        # For Light 0, set position, ambient, diffuse, and specular values
        glLightfv(light_num, GL_POSITION, light_position)
        glLightfv(light_num, GL_AMBIENT, light_ambient)
        glLightfv(light_num, GL_DIFFUSE, light_diffuse)
        glLightfv(light_num, GL_SPECULAR, light_specular)

        glLightfv(light_num, GL_SPOT_DIRECTION, light_direction)
        glLightf(light_num, GL_SPOT_CUTOFF, 15.0)
        glLightf(light_num, GL_SPOT_EXPONENT, 0.0)

        # Distance attenuation
        glLightf(light_num, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(light_num, GL_LINEAR_ATTENUATION, 0.10)
        glLightf(light_num, GL_QUADRATIC_ATTENUATION, 0.00)
        glEnable(light_num)
        glPopMatrix()


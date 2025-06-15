"""
This class contains the functions for drawing basic shapes, 
They can be used to construct the complex components in out scene.


Here are some some example calls to functions in this class:

BasicShapes.draw_sphere(1) # (radius)
BasicShapes.draw_rectangle(3,3,3) # (length, width, height)
BasicShapes.draw_pyramid(3,3) # (base, height)
BasicShapes.draw_prism(8,1,2) # (sides, height, side_length)
BasicShapes.draw_cone(1,3) # (radius, height)
BasicShapes.draw_cylinder(1,3) # (radius, height)
"""

from OpenGL.GLU import *
from OpenGL.GL import *
from utils import *
import math
from textures import *


class BasicShapes:

    def draw_sphere(self, radius):
        quadric = gluNewQuadric()  # Create a new quadric for the sphere
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)
        
        glPushMatrix()  # Save the current matrix
        glTranslatef(0.0, radius, 0.0)  # Translate to place sphere on the y = 0 plane
        
        # Draw the sphere with specified radius, smooth appearance with 32 slices and stacks
        gluSphere(quadric, radius, 32, 32)
        
        glPopMatrix()  # Restore the previous matrix state
        gluDeleteQuadric(quadric)  # Clean up the quadric object

    def draw_rotated_sphere(self, radius, rotate_x, rotate_y, rotate_z):
        quadric = gluNewQuadric()  # Create a new quadric for the sphere
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)
        
        glPushMatrix()  # Save the current matrix
        glTranslatef(0.0, radius, 0.0)  # Translate to place sphere on the y = 0 plane
        glRotate(rotate_x, 0,0,0)
        glRotate(rotate_y, 0,1,0)
        glRotate(rotate_z, 0,0,1)
        
        # Draw the sphere with specified radius, smooth appearance with 32 slices and stacks
        gluSphere(quadric, radius, 32, 32)
        
        glPopMatrix()  # Restore the previous matrix state
        gluDeleteQuadric(quadric)  # Clean up the quadric object

    def draw_animated_sphere(self, radius, position_x, position_z, rotate_x, rotate_z):
        quadric = gluNewQuadric()  # Create a new quadric for the sphere
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)
        
        glPushMatrix()  # Save the current matrix
        glTranslatef(0.0, radius, 0.0)  # Translate to place sphere on the y = 0 plane
        
        # Place in the correct postion/rotation
        glTranslate(position_x, 0, position_z)
        glRotate(rotate_x * 2, 1,0,0)
        glRotate(rotate_z, 0,0,1)
        
        # Draw the sphere with specified radius, smooth appearance with 32 slices and stacks
        gluSphere(quadric, radius, 32, 32)
        
        glPopMatrix()  # Restore the previous matrix state
        gluDeleteQuadric(quadric)  # Clean up the quadric object


    # Draws a rectangle, with the following three paramates:
    # length is the distance in the x direction, width is in the z direction, and height is in the y direction
    def draw_rectangle(self, length, width, height):
        glPushMatrix()

        # Calculate half length and width sizes (for centering the pyramid on the x and z axes)
        half_length = length/2
        half_width = width/2

        # Define vertices for a rectangle
        vertices = [
            [-half_length, 0, -half_width],       # Vertex 0
            [half_length, 0, -half_width],        # Vertex 1
            [half_length, height, -half_width],   # Vertex 2
            [-half_length, height, -half_width],  # Vertex 3
            [-half_length, 0, half_width],        # Vertex 4
            [half_length, 0, half_width],         # Vertex 5
            [half_length, height, half_width],    # Vertex 6
            [-half_length, height, half_width]    # Vertex 7
        ]

        # Defines the rectangle faces created by the given vertices
        # For example the first face is the bottom, created with vertices 0,1,2 and 3 above
        faces = [
            (0, 3, 2, 1), # Face 1 (bottom) #
            (3, 7, 6, 2), # Face 2 (back) #
            (7, 4, 5, 6), # Face 3 (top) #
            (0, 1, 5, 4), # Face 4 (front) #
            (0, 4, 7, 3), # Face 5 (left) 
            (1, 2, 6, 5)  # Face 6 (right)
        ]
        
        # Map texture coordinates to vertices
        tex_coords = [
            (0.0, 0.0),  # Bottom-left
            (1.0, 0.0),  # Bottom-right
            (1.0, 1.0),  # Top-right
            (0.0, 1.0)   # Top-left
        ]

        # Draw the cube
        glBegin(GL_QUADS)
        for face in faces:
            for i, vertex in enumerate(face):
                glTexCoord2f(*tex_coords[i])  # Map texture coordinates
                glVertex3fv(vertices[vertex])  # Define vertex
        glEnd()

        glPopMatrix()

        """
        Visual repersentation with vertexes labled:

          7 ──────── 6
          /|        /|
         / |       / |
        4 ──────── 5 |
        |  |      |  |
        |  |      |  |
        |  3 ─────── 2
        | /       | /
        |/        |/
       0 ──────── 1

        """

    # Use this rectangle for drawing textured objects to ensure proper lighting. 
    # Larger objects generally require more rows and columns, while smaller ones can use fewer. 
    # Increasing the number of columns improves lighting accuracy but can slow down the program. 
    # Aim to find the right balance between visual quality and performance for your object.
    def draw_rectangle_with_grid(self, length, width, height, rows, cols):
        """
        Draw a rectangular prism with grid vertices on each face.
        :param length: Distance in the x direction.
        :param width: Distance in the z direction.
        :param height: Distance in the y direction.
        :param rows: Number of rows for grid.
        :param cols: Number of columns for grid.
        """
        glPushMatrix()

        # Half dimensions for centering
        half_length = length / 2
        half_width = width / 2

        # Helper to draw one face as a grid
        def draw_face(p1, p2, p3, p4, tex_coords):
            """
            Draws a single face of the rectangular prism.
            :param p1, p2, p3, p4: Four corners of the face in counterclockwise order.
            :param tex_coords: Texture coordinates for the four corners.
            """
            dx1 = (p2[0] - p1[0]) / cols
            dy1 = (p2[1] - p1[1]) / cols
            dz1 = (p2[2] - p1[2]) / cols

            dx2 = (p4[0] - p1[0]) / rows
            dy2 = (p4[1] - p1[1]) / rows
            dz2 = (p4[2] - p1[2]) / rows

            tx1, ty1 = tex_coords[1][0] - tex_coords[0][0], tex_coords[1][1] - tex_coords[0][1]
            tx2, ty2 = tex_coords[3][0] - tex_coords[0][0], tex_coords[3][1] - tex_coords[0][1]

            for i in range(rows):
                glBegin(GL_TRIANGLE_STRIP)
                for j in range(cols + 1):
                    # Top vertex
                    glTexCoord2f(tex_coords[0][0] + j * tx1 / cols, tex_coords[0][1] + (i + 1) * ty2 / rows)
                    glVertex3f(
                        p1[0] + j * dx1 + (i + 1) * dx2,
                        p1[1] + j * dy1 + (i + 1) * dy2,
                        p1[2] + j * dz1 + (i + 1) * dz2,
                    )
                    # Bottom vertex
                    glTexCoord2f(tex_coords[0][0] + j * tx1 / cols, tex_coords[0][1] + i * ty2 / rows)
                    glVertex3f(
                        p1[0] + j * dx1 + i * dx2,
                        p1[1] + j * dy1 + i * dy2,
                        p1[2] + j * dz1 + i * dz2,
                    )
                glEnd()

        # Vertices for the rectangular prism
        vertices = [
            [-half_length, 0, -half_width],       # Vertex 0
            [half_length, 0, -half_width],        # Vertex 1
            [half_length, height, -half_width],   # Vertex 2
            [-half_length, height, -half_width],  # Vertex 3
            [-half_length, 0, half_width],        # Vertex 4
            [half_length, 0, half_width],         # Vertex 5
            [half_length, height, half_width],    # Vertex 6
            [-half_length, height, half_width]    # Vertex 7
        ]

        # Texture coordinates for a face
        tex_coords = [
            (0.0, 0.0),  # Bottom-left
            (1.0, 0.0),  # Bottom-right
            (1.0, 1.0),  # Top-right
            (0.0, 1.0)   # Top-left
        ]

        # Draw each face of the rectangular prism
        draw_face(vertices[0], vertices[1], vertices[2], vertices[3], tex_coords)  # Bottom
        draw_face(vertices[4], vertices[5], vertices[6], vertices[7], tex_coords)  # Top
        draw_face(vertices[0], vertices[4], vertices[7], vertices[3], tex_coords)  # Left
        draw_face(vertices[1], vertices[5], vertices[6], vertices[2], tex_coords)  # Right
        draw_face(vertices[3], vertices[2], vertices[6], vertices[7], tex_coords)  # Back
        draw_face(vertices[0], vertices[1], vertices[5], vertices[4], tex_coords)  # Front

        glPopMatrix()

    
    def draw_plane_with_grid(self, length, width, rows, cols):
        """
        Draw a single textured plane with a grid of vertices.
        :param length: Length of the plane (X-axis direction).
        :param width: Width of the plane (Z-axis direction).
        :param rows: Number of rows for the grid.
        :param cols: Number of columns for the grid.
        """
        glPushMatrix()

        # Half dimensions for centering
        half_length = length / 2
        half_width = width / 2

        # Bottom-left and top-right corners of the plane
        p1 = [-half_length, 0, -half_width]  # Bottom-left
        p2 = [half_length, 0, -half_width]  # Bottom-right
        p3 = [half_length, 0, half_width]   # Top-right
        p4 = [-half_length, 0, half_width]  # Top-left

        # Texture coordinates for a plane
        tex_coords = [
            (0.0, 0.0),  # Bottom-left
            (1.0, 0.0),  # Bottom-right
            (1.0, 1.0),  # Top-right
            (0.0, 1.0)   # Top-left
        ]

        # Helper function to draw the grid
        def draw_grid(p1, p2, p3, p4, tex_coords, rows, cols):
            """
            Draws a grid on the plane using triangle strips.
            """
            dx1 = (p2[0] - p1[0]) / cols
            dz1 = (p2[2] - p1[2]) / cols

            dx2 = (p4[0] - p1[0]) / rows
            dz2 = (p4[2] - p1[2]) / rows

            tx1, tz1 = tex_coords[1][0] - tex_coords[0][0], tex_coords[1][1] - tex_coords[0][1]
            tx2, tz2 = tex_coords[3][0] - tex_coords[0][0], tex_coords[3][1] - tex_coords[0][1]

            for i in range(rows):
                glBegin(GL_TRIANGLE_STRIP)
                for j in range(cols + 1):
                    # Top vertex
                    glTexCoord2f(tex_coords[0][0] + j * tx1 / cols, tex_coords[0][1] + (i + 1) * tz2 / rows)
                    glVertex3f(
                        p1[0] + j * dx1 + (i + 1) * dx2,
                        p1[1],
                        p1[2] + j * dz1 + (i + 1) * dz2,
                    )
                    # Bottom vertex
                    glTexCoord2f(tex_coords[0][0] + j * tx1 / cols, tex_coords[0][1] + i * tz2 / rows)
                    glVertex3f(
                        p1[0] + j * dx1 + i * dx2,
                        p1[1],
                        p1[2] + j * dz1 + i * dz2,
                    )
                glEnd()

        # Draw the plane
        draw_grid(p1, p2, p3, p4, tex_coords, rows, cols)

        glPopMatrix()



    # Function to draw a dice
    def draw_cube(self, length, width, height, textures, face_textures=None):
        """
        Draws a cube with optional unique textures for each face.

        Parameters:
        - length: Length of the cube (X-axis)
        - width: Width of the cube (Z-axis)
        - height: Height of the cube (Y-axis)
        - face_textures: Optional list of texture IDs, one for each face in the order:
        [bottom, back, top, front, left, right]. If None, no textures are applied.
        """
        glPushMatrix()

        # Calculate half length and width sizes (for centering the cube)
        half_length = length / 2
        half_width = width / 2

        # Define vertices for the cube
        vertices = [
            [-half_length, 0, -half_width],       # Vertex 0
            [half_length, 0, -half_width],        # Vertex 1
            [half_length, height, -half_width],   # Vertex 2
            [-half_length, height, -half_width],  # Vertex 3
            [-half_length, 0, half_width],        # Vertex 4
            [half_length, 0, half_width],         # Vertex 5
            [half_length, height, half_width],    # Vertex 6
            [-half_length, height, half_width]    # Vertex 7
        ]

        # Defines the rectangle faces created by the given vertices
        faces = [
            (0, 3, 2, 1), # Face 1 (bottom)
            (3, 7, 6, 2), # Face 2 (back)
            (7, 4, 5, 6), # Face 3 (top)
            (0, 1, 5, 4), # Face 4 (front)
            (0, 4, 7, 3), # Face 5 (left)
            (1, 2, 6, 5)  # Face 6 (right)
        ]

        # Define texture coordinates for a face
        tex_coords = [
            (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        ]

       # Draw the cube with optional textures for each face
        for i, face in enumerate(faces):
            # Bind the texture for the current face
            if face_textures and i < len(face_textures):
              textures.set_texture(face_textures[i])

            glBegin(GL_QUADS)
            for j, vertex in enumerate(face):
                glTexCoord2f(*tex_coords[j])  # Texture coordinates for the vertex
                glVertex3fv(vertices[vertex])  # Vertex position
            glEnd()


        glPopMatrix()

        
    # Function to generate a standard pyramid
    def draw_pyramid(self, base_size, height):
        self.draw_rectangular_pyramid(base_size, base_size, height)


    # Function to generate a pyramid with a rectangular base and texture
    def draw_rectangular_pyramid(self, base_width, base_length, height):
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)  # Enable texture mapping

        # Calculate half base size (for centering the pyramid on the x and z axes)
        half_width = base_width / 2.0
        half_length = base_length / 2.0

        # Define the vertices for the pyramid
        vertices = [
            # Base vertices (rectangle base)
            [-half_width, 0.0, -half_length],  # 0
            [ half_width, 0.0, -half_length],  # 1
            [ half_width, 0.0,  half_length],  # 2
            [-half_width, 0.0,  half_length],  # 3

            # Apex of the pyramid
            [0.0, height, 0.0]  # 4 (Apex)
        ]
        
        # Define the indices for the triangles (4 sides + base)
        side_indices = [
            # Sides (4 triangles)
            [0, 4, 1],  # Triangle 1
            [1, 4, 2],  # Triangle 2
            [2, 4, 3],  # Triangle 3
            [3, 4, 0],  # Triangle 4
        ]
        
        base_indices = [
            # Base (rectangle split into two triangles)
            [0, 1, 2],  # Triangle 5
            [0, 2, 3]   # Triangle 6
        ]

        # Define texture coordinates for the pyramid
        side_tex_coords = [
            [0.0, 0.0], [0.5, 1.0], [1.0, 0.0],  # Texture for each side
            [0.0, 0.0], [0.5, 1.0], [1.0, 0.0],
            [0.0, 0.0], [0.5, 1.0], [1.0, 0.0],
            [0.0, 0.0], [0.5, 1.0], [1.0, 0.0],
        ]

        base_tex_coords = [
            [0.0, 0.0], [1.0, 0.0], [1.0, 1.0],  # Texture for base triangle 1
            [0.0, 0.0], [1.0, 1.0], [0.0, 1.0],  # Texture for base triangle 2
        ]

        # Draw the sides of the pyramid
        glBegin(GL_TRIANGLES)
        for i, face in enumerate(side_indices):
            for j, vertex in enumerate(face):
                glTexCoord2f(side_tex_coords[i * 3 + j][0], side_tex_coords[i * 3 + j][1])
                glVertex3fv(vertices[vertex])
        glEnd()

        # Draw the base of the pyramid
        glBegin(GL_TRIANGLES)
        for i, face in enumerate(base_indices):
            for j, vertex in enumerate(face):
                glTexCoord2f(base_tex_coords[i * 3 + j][0], base_tex_coords[i * 3 + j][1])
                glVertex3fv(vertices[vertex])
        glEnd()

        glDisable(GL_TEXTURE_2D)  # Disable texture mapping
        glPopMatrix()


        """
        Visual repersentation with vertexes labled:

               4
              /|\
             / | \
            /  |  \
           /   |   \ 
          /    |    \
        3 _____|______ 2
         \     |       \ 
          \    |        \
           \   |         \
            \  |          \
               0 __________ 1 
                           
        """

    def draw_cone(self, base_radius, height, slices=32, stacks=1):
        glPushMatrix()
        glRotatef(270, 1.0, 0.0, 0.0)  # Rotate the cone to be vertical along the Y-axis
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)

        gluCylinder(quadric, base_radius, 0.0, height, slices, stacks)  # Create the cone
        gluDeleteQuadric(quadric)
        glPopMatrix()

    def draw_cylinder(self, radius, height, slices=32, stacks=1):
        glPushMatrix()
        glRotatef(270, 1.0, 0.0, 0.0)  # Rotate the cylinder to be vertical along the Y-axis
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)

        gluCylinder(quadric, radius, radius, height, slices, stacks)  # Create the cylinder
        gluDeleteQuadric(quadric)
        glPopMatrix()

    def draw_adjustable_cylinder(self, bottom_radius, top_radius, height, slices=32, stacks=1):
        glPushMatrix()
        glRotatef(270, 1.0, 0.0, 0.0)  # Rotate the cylinder to be vertical along the Y-axis
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)

        gluCylinder(quadric, bottom_radius, top_radius, height, slices, stacks)  # Create the cylinder
        gluDeleteQuadric(quadric)
        glPopMatrix()

    def draw_white_rectangle(self, length, width, height):
	
        glDisable(GL_LIGHTING)  # Disable lighting for the solid colored rectangle
        glColor3f(1.0, 1.0, 1.0)  # Set the color to white
        self.draw_rectangle(length, width, height)  # Draw the rectangle
        glEnable(GL_LIGHTING)  # Re-enable lighting

    #=======================================
    # Prism functions
    #=======================================

    def draw_prism(self, sides, height, side_length):
        glPushMatrix()

        glTranslatef(0.0, height / 2, 0.0)  # Center the prism so it rests on the ground at y=0

        # Generate the vertices and faces based on the number of sides, height, and side length
        vertices = self.generate_prism_vertices(sides, height, side_length)
        lat_faces = self.generate_prism_lateral_faces(sides)
        bases = self.generate_prism_bases(sides)

        # Draw the lateral faces
        glBegin(GL_QUADS)
        for face in lat_faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

        # Draw the bases
        for base in bases:
            glBegin(GL_POLYGON)
            for vertex in base:
                glVertex3fv(vertices[vertex])
            glEnd()


        glPopMatrix()



    # Function to generate the vertices of a regular polygonal prism
    def generate_prism_vertices(self, sides, thickness, side_length):
        vertices = []
        angle_step = 2 * math.pi / sides

        # Generate vertices for the bottom base
        for i in range(sides):
            angle = i * angle_step
            x = math.cos(angle) * side_length
            z = math.sin(angle) * side_length
            vertices.append([x, -thickness / 2, z])  # Bottom base vertices

        # Generate vertices for the top base (shifted vertically by thickness)
        for i in range(sides):
            angle = i * angle_step
            x = math.cos(angle) * side_length
            z = math.sin(angle) * side_length
            vertices.append([x, thickness / 2, z])  # Top base vertices

        return vertices

    # Function to generate the faces of the prism
    def generate_prism_lateral_faces(self, sides):
        faces = []

        # Generate the faces for the sides of the prism (connecting corresponding vertices of top and bottom base)
        for i in range(sides):
            next_i = (i + 1) % sides
            # Ensure faces are ordered correctly for right-hand rule (counter-clockwise winding)
            faces.append([i, i + sides, next_i + sides, next_i])  # Side faces

        return faces
    
    def generate_prism_bases(self, sides):
        bases = []

        # Generate the faces for the bottom and top bases
        bottom_face = [i for i in range(sides)]
        top_face = [i + sides for i in range(sides)]

        bases.append(bottom_face)  # Bottom face (counter-clockwise winding)
        bases.append(top_face[::-1])  # Top face (clockwise winding)

        return bases

        
    #=======================================
    # Coordinate frame (To help with creating models)
    #=======================================

    # Draws a nice coordinate frame (using rays with tick marks)
    def draw_coordinate_frame(self):
        origin = Point(0, 0)
        xPoint = Point(10, 0)
        yPoint = Point(0, 10)
        self.draw_ray(origin, xPoint, 10)
        self.draw_ray(origin, yPoint, 10)


    # Draw a Ray from start to end with the proper number of tick marks
    def draw_ray(self, start, end, ticks=0):
        # First draw the line segment itself
        glBegin(GL_LINES)
        glVertex2f(start.x, start.y)
        glVertex2f(end.x, end.y)
        glEnd()
        
        # Now draw the triangular arrow at the end
        r = start.lerp(end, 0.9)  # 90% of way from start to end
        n = self.Vector2D(start, end)
        nperp = n.perp()
        r1 = r.lerpV(nperp, 0.02)
        r2 = r.lerpV(nperp, -0.02)
        glBegin(GL_TRIANGLES)
        glVertex2f(end.x, end.y)
        glVertex2f(r1.x, r1.y)
        glVertex2f(r2.x, r2.y)
        glEnd()
        
        if ticks > 0:
            # Draw tick marks
            step = 1.0/ticks
            glBegin(GL_LINES)
            for t in range(ticks):
                r = start.lerp(end, t*step)  # Could speed up - but necessary?
                r1 = r.lerpV(nperp, 0.02)
                r2 = r.lerpV(nperp, -0.02)
                glVertex2f(r1.x, r1.y)
                glVertex2f(r2.x, r2.y)
            glEnd()


    class Vector2D:
        """A simple 2D Vector Class"""
        def __init__(self, p=None, q=None):
            """A constructor for Vector class between two Points p and q"""
            if q is None:
                if p is None:
                    self.dx = 0; self.dy = 0   # No direction at all
                else:
                    self.dx = p.x; self.dy = p.y  # Origin to p
            else:
                self.dx = q.x - p.x; self.dy = q.y - p.y

        def __str__(self):
            """Basic string representation of this point"""
            return "<%s,%s>"%(self.dx,self.dy)

        def perp(self):
            """Returns a vector perpendicular to this vector (CCW)"""
            answer = Vector()
            answer.dx = -self.dy
            answer.dy = self.dx
            return answer

import copy

import glm
import numpy as np
from OpenGL.GL import GL_FLOAT, GL_FALSE

from Buffers import VertexBuffer, IndexBuffer
from VertexBufferArray import VertexArray, VertexBufferLayout
from Shader import Material
from Renderer import Renderer
from Matrices import mat4, ViewMat


class Object3D:
    def __init__(self, shape3d):
        self.model = glm.identity(glm.mat4)
        self.external_mat = glm.identity(glm.mat4)
        self.shape3d = shape3d
        self.x = self.y = self.z = 0
        self.x_stretch = self.y_stretch = self.z_stretch = 1

    def rotate(self, angle, axis):
        """
        Rotate object around its origin
        :param angle: Angle to rotate by
        :param axis: Axis to rotate around
        :return:
        """
        x, y, z = axis
        self.model = glm.rotate(self.model, glm.radians(angle), glm.vec3(x, y, z))

    def rotate_around_origin(self, angle, axis):
        """
        Rotate an object around an axis going trough the origin
        :param angle: Angle to rotate by
        :param axis: Axis to rotate around
        :return:
        """
        # Rotation around the origin works by moving the objects to the origin, rotating them there and moving them back
        x, y, z = self.x, self.y, self.z
        self.translate(-x, -y, -z)
        self.rotate(angle, axis)
        self.translate(x, y, z)

    def translate(self, x, y, z):
        """
        Move the model by updating the model matrix accounting for object stretch
        :param x: Translation amount in X axis
        :param y: Translation amount in Y axis
        :param z: Translation amount in Z axis
        :return:
        """
        self.move_pos(x, y, z)
        self.model = glm.translate(self.model, glm.vec3(x/self.x_stretch, y/self.y_stretch, z/self.z_stretch))

    def abs_translate(self, x, y, z):
        """
        Move the model by updating the model matrix ignoring object stretch


        :return:
        """
        self.move_pos(x, y, z)
        self.model += glm.translate(glm.identity(glm.mat4), glm.vec3(x, y, z))

    def set_stretch(self, x, y, z):
        """
        Set new stretch values
        :param x: New stretch value in X axis
        :param y: New stretch value in Y axis
        :param z: New stretch value in Z axis
        :return:
        """
        self.x_stretch *= x
        self.y_stretch *= y
        self.z_stretch *= z
        self.model = glm.scale(self.model, glm.vec3(x, y, z))

    def draw(self, proj, view):
        """
        Call the shape draw function with appropriate object information
        :param proj: Projection matrix
        :param view: View Matrix
        :return:
        """
        self.shape3d.draw(proj, view, self.external_mat * self.model)

    def apply_mat(self, mat):
        """
        Set new position and orientation of the object by an external matrix
        :param mat: External matrix
        :return:
        """
        self.external_mat = mat

    def move_pos(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z


class Shape3D:
    def __init__(self, material, layout, data, indices=None):
        """
        Setup all the variables needed for rendering the object
        :param material: material for the object
        :param layout: layout of information in the data array
        :param data: data array
        :param indices: list of indices if Index Buffer is to be used
        """
        self.material = material
        self.vao = VertexArray(material.program)
        self.vbo = VertexBuffer(data)
        # Index Buffer is only used if a list of indices is entered
        self.ibo = IndexBuffer(indices) if indices is list else None
        self.vao.add_buffer(self.vbo, layout)

    def draw(self, uProjection, uView, uModel):
        """
        Set uniforms in the shader and render the object
        :param uProjection:
        :param uView:
        :param uModel:
        :return:
        """
        self.material.bind()
        self.material.shader.set_uniform_mat4f("uProjection", glm.transpose(uProjection))
        self.material.shader.set_uniform_mat4f("uView", glm.transpose(uView))
        self.material.shader.set_uniform_mat4f("uModel", glm.transpose(uModel))
        Renderer.draw(self.vao, self.ibo if self.ibo is not None else self.vbo, self.material.shader)


class Cube(Shape3D):
    def __init__(self, material, x, y, z):
        # Array of points with normal vectors
        data = np.array([(-0.5*x, -0.5*y, -0.5*z, 0.0, 0.0, -1.0),
                         ( 0.5*x, -0.5*y, -0.5*z, 0.0, 0.0, -1.0),
                         ( 0.5*x,  0.5*y, -0.5*z, 0.0, 0.0, -1.0),
                         ( 0.5*x,  0.5*y, -0.5*z, 0.0, 0.0, -1.0),
                         (-0.5*x,  0.5*y, -0.5*z, 0.0, 0.0, -1.0),
                         (-0.5*x, -0.5*y, -0.5*z, 0.0, 0.0, -1.0),

                         (-0.5*x, -0.5*y,  0.5*z, 0.0, 0.0, 1.0),
                         ( 0.5*x, -0.5*y,  0.5*z, 0.0, 0.0, 1.0),
                         ( 0.5*x,  0.5*y,  0.5*z, 0.0, 0.0, 1.0),
                         ( 0.5*x,  0.5*y,  0.5*z, 0.0, 0.0, 1.0),
                         (-0.5*x,  0.5*y,  0.5*z, 0.0, 0.0, 1.0),
                         (-0.5*x, -0.5*y,  0.5*z, 0.0, 0.0, 1.0),

                         (-0.5*x,  0.5*y,  0.5*z, -1.0, 0.0, 0.0),
                         (-0.5*x,  0.5*y, -0.5*z, -1.0, 0.0, 0.0),
                         (-0.5*x, -0.5*y, -0.5*z, -1.0, 0.0, 0.0),
                         (-0.5*x, -0.5*y, -0.5*z, -1.0, 0.0, 0.0),
                         (-0.5*x, -0.5*y,  0.5*z, -1.0, 0.0, 0.0),
                         (-0.5*x,  0.5*y,  0.5*z, -1.0, 0.0, 0.0),

                         ( 0.5*x,  0.5*y,  0.5*z, 1.0, 0.0, 0.0),
                         ( 0.5*x,  0.5*y, -0.5*z, 1.0, 0.0, 0.0),
                         ( 0.5*x, -0.5*y, -0.5*z, 1.0, 0.0, 0.0),
                         ( 0.5*x, -0.5*y, -0.5*z, 1.0, 0.0, 0.0),
                         ( 0.5*x, -0.5*y,  0.5*z, 1.0, 0.0, 0.0),
                         ( 0.5*x,  0.5*y,  0.5*z, 1.0, 0.0, 0.0),

                         (-0.5*x, -0.5*y, -0.5*z, 0.0, -1.0, 0.0),
                         ( 0.5*x, -0.5*y, -0.5*z, 0.0, -1.0, 0.0),
                         ( 0.5*x, -0.5*y,  0.5*z, 0.0, -1.0, 0.0),
                         ( 0.5*x, -0.5*y,  0.5*z, 0.0, -1.0, 0.0),
                         (-0.5*x, -0.5*y,  0.5*z, 0.0, -1.0, 0.0),
                         (-0.5*x, -0.5*y, -0.5*z, 0.0, -1.0, 0.0),

                         (-0.5*x,  0.5*y, -0.5*z, 0.0, 1.0, 0.0),
                         ( 0.5*x,  0.5*y, -0.5*z, 0.0, 1.0, 0.0),
                         ( 0.5*x,  0.5*y,  0.5*z, 0.0, 1.0, 0.0),
                         ( 0.5*x,  0.5*y,  0.5*z, 0.0, 1.0, 0.0),
                         (-0.5*x,  0.5*y,  0.5*z, 0.0, 1.0, 0.0),
                         (-0.5*x,  0.5*y, -0.5*z, 0.0, 1.0, 0.0)], dtype=np.float32)

        layout = VertexBufferLayout()
        layout.push(GL_FLOAT, 3, GL_FALSE, "position")
        layout.push(GL_FLOAT, 3, GL_FALSE, "normal")

        super(Cube, self).__init__(material, layout, data)


class Cylinder(Shape3D):
    def __init__(self, shader):
        data = None  # TODO - Implement cylinder vertex generation
        indices = None
        layout = None
        super(Cylinder, self).__init__(shader, layout, data, indices)


class ObjectGroup:
    """
    Class that groups 3D Objects and allows to apply transformation to all of them together
    """
    def __init__(self, new_objects: list = None):
        if new_objects is None:
            self.objects = {}
        else:
            self.objects = set(new_objects)

        self.x = self.y = self.z = 0
        self.rx = self.ry = self.rz = 0

    def add_object(self, object3d):
        """Add an extra object to the group"""
        self.objects.add(object3d)

    def rotate(self, angle, axis):
        """Rotate all of the objects by any axis"""
        for i in self.objects:
            i.rotate_around_origin(angle, axis)

    def rotate_x(self, angle):
        self.rotate(angle, (1, 0, 0))

    def rotate_y(self, angle):
        self.rotate(angle, (0, 1, 0))

    def rotate_z(self, angle):
        self.rotate(angle, (0, 0, 1))

    def set_rot(self, rx, ry, rz):
        """
        Set rotation of all of the objects
        This is done by moving the group to the origin, rotating by all axis by negative of current rotation,
        then rotating by new values and moving the group back
        :param rx: New X axis rotation value
        :param ry: New Y axis rotation value
        :param rz: New Z axis rotation value
        :return:
        """
        x, y, z = self.x, self.y, self.z
        self.translate(-x, -y, -z)
        self.rotate_x(-self.rx)
        self.rotate_y(-self.ry)
        self.rotate_z(-self.rz)
        self.rotate_z(rz)
        self.rotate_y(ry)
        self.rotate_x(rx)
        self.rx, self.ry, self.rz = rx, ry, rz
        self.translate(x, y, z)

    def translate(self, x, y, z):
        """Translate all of the objects"""
        self.x += x
        self.y += y
        self.z += z
        for i in self.objects:
            i.translate(x, y, z)

    def set_pos(self, x, y, z):
        """
        Set position of all of the objects
        :param x: New X axis position value
        :param y: New Y axis position value
        :param z: New Z axis position value
        :return:
        """
        self.translate(-self.x, -self.y, -self.z)
        self.translate(x, y, z)

    def apply_mat(self, mat):
        """Apply an external matrix to all of the objects in the group"""
        for i in self.objects:
            i.apply_mat(mat)

    def draw(self, proj, view):
        """Render all of the objects in the group"""
        for i in self.objects:
            i.draw(proj, view)

    def copy(self):
        """Create a true copy of the group"""
        return copy.deepcopy(self)


# following code creates the 3d model of the point marker
material_gray = Material("./res/shaders/cube.shader")
material_red = material_gray.copy()
material_green = material_gray.copy()
material_blue = material_gray.copy()

material_gray.add_uniform(material_gray.shader.set_uniform_3f, 'uColor', (0.5, 0.5, 0.5))
material_red.add_uniform(material_red.shader.set_uniform_3f, 'uColor', (1, 0, 0))
material_green.add_uniform(material_green.shader.set_uniform_3f, 'uColor', (0, 1, 0))
material_blue.add_uniform(material_blue.shader.set_uniform_3f, 'uColor', (0, 0, 1))


rod_length = 0.2
gray_cube = Cube(material_gray, 0.5, 0.5, 0.5)
red_cube = Cube(material_red, 1, rod_length, rod_length)
green_cube = Cube(material_green, rod_length, 1, rod_length)
blue_cube = Cube(material_blue, rod_length, rod_length, 1)


cube1 = Object3D(gray_cube)
cube2 = Object3D(red_cube)
cube3 = Object3D(green_cube)
cube4 = Object3D(blue_cube)
cube2.translate(0.5, 0, 0)
cube3.translate(0, 0.5, 0)
cube4.translate(0, 0, 0.5)

coord_3d = ObjectGroup([cube1, cube2, cube3, cube4])

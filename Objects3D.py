import copy

import glm
import numpy as np
from OpenGL.GL import GL_FLOAT, GL_FALSE

from Buffers import VertexBuffer, IndexBuffer
from VertexBufferArray import VertexArray, VertexBufferLayout
from Shader import Material
from Renderer import Renderer


class Object3D:
    def __init__(self, shape3d):
        self.model = glm.identity(glm.mat4)
        self.shape3d = shape3d
        self.x = self.y = self.z = 0
        self.x_stretch = self.y_stretch = self.z_stretch = 1

    def rotate(self, angle, axis):
        x, y, z = axis
        self.model = glm.rotate(self.model, glm.radians(angle), glm.vec3(y, z, x))

    def rotate_around_origin(self, angle, axis):
        x, y, z = self.x, self.y, self.z
        self.translate(-x, -y, -z)
        self.rotate(angle, axis)
        self.translate(x, y, z)

    def translate(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z
        self.model = glm.translate(self.model, glm.vec3(-y/self.y_stretch, -z/self.z_stretch, x/self.x_stretch))

    def set_stretch(self, x, y, z):
        self.x_stretch *= x
        self.y_stretch *= y
        self.z_stretch *= z
        self.model = glm.scale(self.model, glm.vec3(y, z, x))

    def draw(self, proj, view):
        self.shape3d.draw(proj, view, self.model)


class Shape3D:
    def __init__(self, material, layout, data, indices=None):
        self.material = material
        self.vao = VertexArray(material.program)
        self.vbo = VertexBuffer(data)
        self.ibo = IndexBuffer(indices) if indices is not None else None
        self.vao.add_buffer(self.vbo, layout)

    def draw(self, uProjection, uView, uModel):
        self.material.bind()
        self.material.shader.set_uniform_mat4f("uProjection", uProjection)
        self.material.shader.set_uniform_mat4f("uView", uView)
        self.material.shader.set_uniform_mat4f("uModel", glm.transpose(uModel))
        Renderer.draw(self.vao, self.ibo if self.ibo is not None else self.vbo, self.material.shader)


class Cube(Shape3D):
    def __init__(self, material, x, y, z):
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
    def __init__(self):
        self.objects = []

    def add_object(self, object3d):
        self.objects.append(object3d)

    def rotate(self, angle, axis):
        for i in self.objects:
            i.rotate_around_origin(angle, axis)

    def translate(self, x, y, z):
        for i in self.objects:
            i.translate(x, y, z)

    def draw(self, proj, view):
        for i in self.objects:
            i.draw(proj, view)

    def copy(self):
        return copy.deepcopy(self)


material_gray = Material("./res/shaders/cube.shader")
material_red = material_gray.copy()
material_green = material_gray.copy()
material_blue = material_gray.copy()

material_gray.add_uniform(material_gray.shader.set_uniform_3f, 'uColor', (0.5, 0.5, 0.5))
material_red.add_uniform(material_red.shader.set_uniform_3f, 'uColor', (1, 0, 0))
material_green.add_uniform(material_green.shader.set_uniform_3f, 'uColor', (0, 1, 0))
material_blue.add_uniform(material_blue.shader.set_uniform_3f, 'uColor', (0, 0, 1))


rod = 0.2
gray_cube = Cube(material_gray, 0.5, 0.5, 0.5)
red_cube = Cube(material_red, rod, rod, 1)
green_cube = Cube(material_green, 1, rod, rod)
blue_cube = Cube(material_blue, rod, 1, rod)


cube1 = Object3D(gray_cube)
cube2 = Object3D(red_cube)
cube3 = Object3D(green_cube)
cube4 = Object3D(blue_cube)
cube2.translate(0.5, 0, 0)
cube3.translate(0, 0.5, 0)
cube4.translate(0, 0, 0.5)

coord_3d = ObjectGroup()
coord_3d.add_object(cube1)
coord_3d.add_object(cube2)
coord_3d.add_object(cube3)
coord_3d.add_object(cube4)

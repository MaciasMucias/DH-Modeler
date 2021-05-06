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
        self.x = self.y = self.z = 1

    def set_rotate(self, angle, axis):
        self.model = glm.rotate(self.model, glm.radians(angle), glm.vec3(axis))

    def set_translate(self, x, y, z):
        self.model = glm.translate(self.model, glm.vec3(x/self.x, y/self.y, z/self.z))

    def set_stretch(self, x, y, z):
        self.x *= x
        self.y *= y
        self.z *= z
        self.model = glm.scale(self.model, glm.vec3(x, y, z))

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
    def __init__(self, material):
        data = np.array([(-0.5, -0.5, -0.5, 0.0, 0.0, -1.0),
                         ( 0.5, -0.5, -0.5, 0.0, 0.0, -1.0),
                         ( 0.5,  0.5, -0.5, 0.0, 0.0, -1.0),
                         ( 0.5,  0.5, -0.5, 0.0, 0.0, -1.0),
                         (-0.5,  0.5, -0.5, 0.0, 0.0, -1.0),
                         (-0.5, -0.5, -0.5, 0.0, 0.0, -1.0),

                         (-0.5, -0.5,  0.5, 0.0, 0.0, 1.0),
                         ( 0.5, -0.5,  0.5, 0.0, 0.0, 1.0),
                         ( 0.5,  0.5,  0.5, 0.0, 0.0, 1.0),
                         ( 0.5,  0.5,  0.5, 0.0, 0.0, 1.0),
                         (-0.5,  0.5,  0.5, 0.0, 0.0, 1.0),
                         (-0.5, -0.5,  0.5, 0.0, 0.0, 1.0),

                         (-0.5,  0.5,  0.5, -1.0, 0.0, 0.0),
                         (-0.5,  0.5, -0.5, -1.0, 0.0, 0.0),
                         (-0.5, -0.5, -0.5, -1.0, 0.0, 0.0),
                         (-0.5, -0.5, -0.5, -1.0, 0.0, 0.0),
                         (-0.5, -0.5,  0.5, -1.0, 0.0, 0.0),
                         (-0.5,  0.5,  0.5, -1.0, 0.0, 0.0),

                         ( 0.5,  0.5,  0.5, 1.0, 0.0, 0.0),
                         ( 0.5,  0.5, -0.5, 1.0, 0.0, 0.0),
                         ( 0.5, -0.5, -0.5, 1.0, 0.0, 0.0),
                         ( 0.5, -0.5, -0.5, 1.0, 0.0, 0.0),
                         ( 0.5, -0.5,  0.5, 1.0, 0.0, 0.0),
                         ( 0.5,  0.5,  0.5, 1.0, 0.0, 0.0),

                         (-0.5, -0.5, -0.5, 0.0, -1.0, 0.0),
                         ( 0.5, -0.5, -0.5, 0.0, -1.0, 0.0),
                         ( 0.5, -0.5,  0.5, 0.0, -1.0, 0.0),
                         ( 0.5, -0.5,  0.5, 0.0, -1.0, 0.0),
                         (-0.5, -0.5,  0.5, 0.0, -1.0, 0.0),
                         (-0.5, -0.5, -0.5, 0.0, -1.0, 0.0),

                         (-0.5,  0.5, -0.5, 0.0, 1.0, 0.0),
                         ( 0.5,  0.5, -0.5, 0.0, 1.0, 0.0),
                         ( 0.5,  0.5,  0.5, 0.0, 1.0, 0.0),
                         ( 0.5,  0.5,  0.5, 0.0, 1.0, 0.0),
                         (-0.5,  0.5,  0.5, 0.0, 1.0, 0.0),
                         (-0.5,  0.5, -0.5, 0.0, 1.0, 0.0)], dtype=np.float32)

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

    def set_rotate(self, angle, axis):
        for i in self.objects:
            i.set_rotate(angle, axis)

    def set_translate(self, x, y, z):
        for i in self.objects:
            i.set_translate(x, y, z)

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

gray_cube = Cube(material_gray)
red_cube = Cube(material_red)
green_cube = Cube(material_green)
blue_cube = Cube(material_blue)

rod = 0.2

cube1 = Object3D(gray_cube)
cube2 = Object3D(red_cube)
cube3 = Object3D(green_cube)
cube4 = Object3D(blue_cube)
cube1.set_stretch(0.5, 0.5, 0.5)
cube2.set_stretch(1, rod, rod)
cube2.set_translate(0.5, 0, 0)
cube3.set_stretch(rod, 1, rod)
cube3.set_translate(0, 0.5, 0)
cube4.set_stretch(rod, rod, 1)
cube4.set_translate(0, 0, 0.5)

coord_3d = ObjectGroup()
coord_3d.add_object(cube1)
coord_3d.add_object(cube2)
coord_3d.add_object(cube3)
coord_3d.add_object(cube4)

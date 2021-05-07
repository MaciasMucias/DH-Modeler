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
        x, y, z = axis
        self.model = glm.rotate(self.model, glm.radians(angle), glm.vec3(x, y ,z))

    def rotate_around_origin(self, angle, axis):
        x, y, z = self.x, self.y, self.z
        self.translate(-x, -y, -z)
        self.rotate(angle, axis)
        self.translate(x, y, z)

    def translate(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z
        self.model = glm.translate(self.model, glm.vec3(x/self.x_stretch, y/self.y_stretch, z/self.z_stretch))

    def abs_translate(self, x, y, z):
        self.model += glm.translate(glm.identity(glm.mat4), glm.vec3(x, y, z))

    def set_stretch(self, x, y, z):
        self.x_stretch *= x
        self.y_stretch *= y
        self.z_stretch *= z
        self.model = glm.scale(self.model, glm.vec3(x, y, z))

    def draw(self, proj, view):
        self.shape3d.draw(proj, view, self.external_mat * self.model)

    def apply_mat(self, mat):
        self.external_mat = mat


class Shape3D:
    def __init__(self, material, layout, data, indices=None):
        self.material = material
        self.vao = VertexArray(material.program)
        self.vbo = VertexBuffer(data)
        self.ibo = IndexBuffer(indices) if indices is not None else None
        self.vao.add_buffer(self.vbo, layout)

    def draw(self, uProjection, uView, lhModel):
        self.material.bind()
        uModel = glm.identity(glm.mat4)
        lhModel = glm.transpose(lhModel)
        switch = {0: 1, 1: 0, 2: 2, 3: 3}
        for i in range(4):
            uModel[i] = lhModel[switch[i]]
        self.material.shader.set_uniform_mat4f("uProjection", glm.transpose(uProjection))
        self.material.shader.set_uniform_mat4f("uView", glm.transpose(uView))
        self.material.shader.set_uniform_mat4f("uModel", uModel)
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
        self.x = self.y = self.z = 0
        self.rx = self.ry = self.rz = 0

    def add_object(self, object3d):
        self.objects.append(object3d)

    def rotate(self, angle, axis):
        for i in self.objects:
            i.rotate_around_origin(angle, axis)

    def rotate_x(self, angle):
        self.rx += 0
        for i in self.objects:
            i.rotate_around_origin(angle, (1, 0, 0))

    def rotate_y(self, angle):
        self.ry += 0
        for i in self.objects:
            i.rotate_around_origin(angle, (0, 1, 0))

    def rotate_z(self, angle):
        self.rz += 0
        for i in self.objects:
            i.rotate_around_origin(angle, (0, 0, 1))

    def set_rot(self, rx, ry, rz):
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
        self.x += x
        self.y += y
        self.z += z
        for i in self.objects:
            i.translate(x, y, z)

    def set_pos(self, x, y, z):
        for i in self.objects:
            i.abs_translate(-self.x, -self.y, -self.z)
            i.abs_translate(x, y, z)
        self.x = x
        self.y = y
        self.z = z

    def apply_mat(self, mat):
        for i in self.objects:
            i.apply_mat(mat)

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
red_cube = Cube(material_red, 1, rod, rod)
green_cube = Cube(material_green, rod, 1, rod)
blue_cube = Cube(material_blue, rod, rod, 1)


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

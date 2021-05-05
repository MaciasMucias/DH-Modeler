import glm
import numpy as np

from Buffers import *
from VertexBufferArray import VertexArray
from Renderer import Renderer


class Object3D:
    def __init__(self, shape3d):
        self.model = glm.identity(glm.mat4)
        self.shape3d = shape3d

    def set_rotate(self, angle, axis):
        self.model = glm.rotate(self.model, glm.radians(angle), glm.vec3(axis))

    def set_position(self, x, y, z):
        self.model = glm.translate(self.model, glm.vec3(x, y, z))

    def set_stretch(self, x, y, z):
        self.model = glm.scale(self.model, glm.vec3(x, y, z))

    def draw(self):
        self.shape3d.draw(self.model)


class Shape3D:
    def __init__(self, shader, data, indices):
        self.shader = shader
        self.vao = VertexArray(shader.program)
        self.vbo = VertexBuffer(data)
        self.ibo = IndexBuffer(indices)

    def draw(self, mat):
        self.shader.bind()
        self.shader.set_uniform_mat4f(mat)
        Renderer.draw(self.vao, self.vbo, self.ibo)


class Cube(Shape3D):
    def __init__(self, color, shader):
        data = np.array([(-0.5, -0.5, -0.5, *color),
                         ( 0.5, -0.5, -0.5, *color),
                         ( 0.5,  0.5, -0.5, *color),
                         (-0.5,  0.5, -0.5, *color),
                         (-0.5, -0.5,  0.5, *color),
                         ( 0.5, -0.5,  0.5, *color),
                         ( 0.5,  0.5,  0.5, *color),
                         (-0.5,  0.5,  0.5, *color)], dtype=np.float32)
        indices = np.array([0, 1, 2, 2, 3, 0,
                            0, 1, 5, 5, 4, 0,
                            1, 2, 6, 6, 5, 1,
                            2, 3, 7, 7, 6, 2,
                            3, 0, 4, 4, 7, 3,
                            4, 5, 6, 6, 7, 4], dtype=np.uint32)

        super(Cube, self).__init__(shader, data, indices)


class Cylinder(Shape3D):
    def __init__(self, shader):
        data = None                                                        # TODO - Implement cylinder vertex generation
        indices = None
        super(Cylinder, self).__init__(shader, data, indices)

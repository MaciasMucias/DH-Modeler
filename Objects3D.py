import glm
import numpy as np
from OpenGL.GL import GL_FLOAT, GL_FALSE

from Buffers import VertexBuffer, IndexBuffer
from VertexBufferArray import VertexArray, VertexBufferLayout
from Renderer import Renderer


class Object3D:
    def __init__(self, shape3d):
        self.model = glm.identity(glm.mat4)
        self.shape3d = shape3d

    def set_rotate(self, angle, axis):
        self.model = glm.rotate(self.model, glm.radians(angle), glm.vec3(axis))

    def set_translate(self, x, y, z):
        print(self.model)
        self.model = glm.transpose(glm.translate(self.model, glm.vec3(x, y, z)))
        print(self.model)

    def set_stretch(self, x, y, z):
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
        self.material.shader.set_uniform_mat4f("uModel", uModel)
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

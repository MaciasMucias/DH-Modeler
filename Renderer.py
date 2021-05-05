from OpenGL.GL import *
from Buffers import VertexBuffer, IndexBuffer


class Renderer:
    @staticmethod
    def draw(vao, ibo: IndexBuffer, shader):
        shader.bind()
        vao.bind()
        ibo.bind()

        glDrawElements(GL_TRIANGLES, ibo.count, GL_UNSIGNED_INT, None)

    @staticmethod
    def draw(vao, vbo: VertexBuffer, shader):
        shader.bind()
        vao.bind()

        glDrawArrays(GL_TRIANGLES, 0, vbo.count)

    @staticmethod
    def clear():
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)

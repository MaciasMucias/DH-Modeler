from OpenGL.GL import *
from Buffers import VertexBuffer, IndexBuffer


class Renderer:
    @staticmethod
    def draw(vao, ibo: IndexBuffer, shader):
        """
        Renders the content of Vertex Array using the Index Buffer
        :param vao: Vertex Array Object
        :param ibo: Index Buffer Object
        :param shader: Shader
        :return:
        """
        shader.bind()
        vao.bind()
        ibo.bind()

        glDrawElements(GL_TRIANGLES, ibo.count, GL_UNSIGNED_INT, None)

    @staticmethod
    def draw(vao, vbo: VertexBuffer, shader):
        """
        Renders the content of Vertex Array using the Vertex Buffer
        :param vao: Vertex Array Object
        :param vbo: Vertex Buffer Object
        :param shader: Shader
        :return:
        """
        shader.bind()
        vao.bind()

        glDrawArrays(GL_TRIANGLES, 0, vbo.count)

    @staticmethod
    def clear():
        """Clears color and depth buffers"""
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)

from OpenGL.GL import *


class Renderer:
    @staticmethod
    def draw(vao, ibo, shader):
        shader.bind()
        vao.bind()
        ibo.bind()

        glDrawElements(GL_TRIANGLES, ibo.count, GL_UNSIGNED_INT, None)

    @staticmethod
    def clear():
        glClear(GL_COLOR_BUFFER_BIT)
        #glClear(GL_DEPTH_BUFFER)

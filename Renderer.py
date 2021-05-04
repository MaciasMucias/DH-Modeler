from OpenGL.GL import *


class Renderer:
    def draw(self, vao, ibo, shader):
        shader.bind()
        vao.bind()
        ibo.bind()

        glDrawElements(GL_TRIANGLES, ibo.count, GL_UNSIGNED_INT, None)

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)
        # glClear(GL_DEPTH_BUFFER)

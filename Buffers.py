import numpy as np
from OpenGL.GL import *


class VertexBuffer:
    def __init__(self, data: np.ndarray):
        self.__renderer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.__renderer_id)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.__renderer_id)

    @staticmethod
    def unbind():
        glBindBuffer(GL_ARRAY_BUFFER, 0)


class IndexBuffer:
    def __init__(self, data: np.ndarray):
        self.__renderer_id = glGenBuffers(1)
        self.__count = len(data)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.__renderer_id)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

    def bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.__renderer_id)

    @staticmethod
    def unbind():
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    @property
    def count(self):
        return self.__count

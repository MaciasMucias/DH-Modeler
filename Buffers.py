import numpy as np
from OpenGL.GL import *
from abc import ABC


class Buffer(ABC):
    """
    Template class for buffers
    """
    array_type = None

    def __init__(self, data: np.ndarray):
        self.__renderer_id = glGenBuffers(1)
        self.__count = data.shape[0]
        glBindBuffer(self.array_type, self.__renderer_id)
        glBufferData(self.array_type, data.nbytes, data, GL_STATIC_DRAW)

    def bind(self):
        glBindBuffer(self.array_type, self.__renderer_id)

    @staticmethod
    def unbind():
        glBindBuffer(self.array_type, 0)

    @property
    def count(self):
        return self.__count


class VertexBuffer(Buffer):
    array_type = GL_ARRAY_BUFFER

    def __init__(self, data: np.ndarray):
        super(VertexBuffer, self).__init__(data)


class IndexBuffer:
    array_type = GL_ELEMENT_ARRAY_BUFFER
    
    def __init__(self, data: np.ndarray):
        super(IndexBuffer, self).__init__(data)

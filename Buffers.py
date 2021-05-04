import numpy as np
import ctypes
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


class VertexLayoutElement:
    def __init__(self, gl_type: int, count: int, normalised: bool, attrib: str):
        self.gl_type = gl_type
        self.count = count
        self.normalised = normalised
        self.attrib = attrib


gl_type_bytes = {
        GL_FLOAT: ctypes.sizeof(ctypes.c_float),
        GL_UNSIGNED_INT: ctypes.sizeof(ctypes.c_uint),
        GL_UNSIGNED_BYTE: ctypes.sizeof(ctypes.c_byte)
    }


class VertexBufferLayout:
    def __init__(self):
        self.__elements = []
        self.__stride = 0

    def push(self, gl_type, count, normalised, attrib):
        self.__elements.append(VertexLayoutElement(gl_type, count, normalised, attrib))
        self.__stride += gl_type_bytes[gl_type] * count

    @property
    def stride(self):
        return self.__stride

    @property
    def elements(self) -> [VertexLayoutElement]:
        return self.__elements


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
    def get_count(self):
        return self.__count


class VertexArray:
    def __init__(self, program):
        self.program = program
        self.__renderer_id = glGenVertexArrays(1)

    def bind(self):
        glBindVertexArray(self.__renderer_id)

    @staticmethod
    def unbind():
        glBindVertexArray(0)

    def add_buffer(self, vb: VertexBuffer, layout: VertexBufferLayout):
        self.bind()
        vb.bind()
        elements = layout.elements
        offset = 0
        for element in elements:
            loc = glGetAttribLocation(self.program, element.attrib)
            glEnableVertexAttribArray(loc)
            glVertexAttribPointer(loc, element.count, element.gl_type, element.normalised, layout.stride, ctypes.c_void_p(offset))
            offset += gl_type_bytes[element.gl_type] * element.count


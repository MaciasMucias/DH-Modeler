from OpenGL.GL import *

gl_type_bytes = {
        GL_FLOAT: ctypes.sizeof(ctypes.c_float),
        GL_UNSIGNED_INT: ctypes.sizeof(ctypes.c_uint),
        GL_UNSIGNED_BYTE: ctypes.sizeof(ctypes.c_byte)
    }


class VertexLayoutElement:
    def __init__(self, gl_type: int, count: int, normalised: bool, attrib: str):
        """
        An element of a layout
        :param gl_type: Type of data
        :param count: Amount of data
        :param normalised: Is normalised
        :param attrib: Attribute name
        """
        self.gl_type = gl_type
        self.count = count
        self.normalised = normalised
        self.attrib = attrib


class VertexBufferLayout:
    def __init__(self):
        self.__elements = []
        self.__stride = 0

    def push(self, gl_type, count, normalised, attrib):
        """
        Add a new layout element nad recalculate stride
        :return:
        """
        self.__elements.append(VertexLayoutElement(gl_type, count, normalised, attrib))
        self.__stride += gl_type_bytes[gl_type] * count

    @property
    def stride(self):
        return self.__stride

    @property
    def elements(self) -> [VertexLayoutElement]:
        return self.__elements


class VertexArray:
    def __init__(self, program):
        self.program = program
        self.__renderer_id = glGenVertexArrays(1)

    def bind(self):
        glBindVertexArray(self.__renderer_id)

    @staticmethod
    def unbind():
        glBindVertexArray(0)

    def add_buffer(self, vb, layout: VertexBufferLayout):
        """
        Bind new Vertex Buffer and specify it's layout
        :param vb: Vertex Buffer
        :param layout: Vertex Buffer Layout
        :return:
        """
        self.bind()
        vb.bind()
        elements = layout.elements
        offset = 0
        for element in elements:
            loc = glGetAttribLocation(self.program, element.attrib)
            glEnableVertexAttribArray(loc)
            glVertexAttribPointer(loc, element.count, element.gl_type,
                                  element.normalised, layout.stride, ctypes.c_void_p(offset))
            offset += gl_type_bytes[element.gl_type] * element.count

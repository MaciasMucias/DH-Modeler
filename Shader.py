from OpenGL.GL import *
import numpy as np
import copy


class Shader:
    def __init__(self, filepath):
        """Loads vertex and fragment shaders from a file"""
        self.filepath = filepath
        self.__renderer_id = self.create_shader()
        self.__uniform_location_cache = dict()

    @property
    def program(self):
        return self.__renderer_id

    def bind(self):
        glUseProgram(self.__renderer_id)

    @staticmethod
    def unbind():
        glUseProgram(0)

    def set_uniform_3f(self, name, v):
        """Set a value of a 3 element floating point vector uniform"""
        glUniform3f(self.get_uniform_location(name), *v)

    def set_uniform_4f(self, name, v):
        """Set a value of a 4 element floating point vector uniform"""
        glUniform4f(self.get_uniform_location(name), *v)

    def set_uniform_mat4f(self, name, mat):
        """Set a value of a 4x4 element floating point matrix uniform"""
        glUniformMatrix4fv(self.get_uniform_location(name), 1, GL_FALSE, np.array(mat))

    def get_uniform_location(self, name):
        """
        Get the location of a specified uniform by looking for it in the cache, and if not there in the shader
        :param name: Uniform name
        :return: Uniform location
        """
        if name in self.__uniform_location_cache.keys():
            return self.__uniform_location_cache[name]

        location = glGetUniformLocation(self.__renderer_id, name)

        if location == -1:
            print(f"Warning: uniform {name} doesn't exist")
        self.__uniform_location_cache[name] = location
        return location

    def create_shader(self):
        """
        Load the shader from the filepath and verify it's validity
        :return: Shader id
        """
        program = glCreateProgram()
        shader_code = Shader.parse_shader(self.filepath)
        vertex = Shader.compile_shader(GL_VERTEX_SHADER, shader_code[0], "Vertex")
        fragment = Shader.compile_shader(GL_FRAGMENT_SHADER, shader_code[1], "Fragment")

        glAttachShader(program, vertex)
        glAttachShader(program, fragment)
        glLinkProgram(program)
        glValidateProgram(program)

        if not glGetProgramiv(program, GL_LINK_STATUS):
            raise RuntimeError('Linking error: %s', glGetProgramInfoLog(program))

        glDeleteShader(vertex)
        glDeleteShader(fragment)
        return program

    @staticmethod
    def parse_shader(filepath):
        """
        Read the specified file line by line searching for the lines where the next shader appears
        "#shader vertex" or "#shader fragment" signal the begging of a new shader

        :param filepath: File to the shader program
        :return: A list with two shader programs
        """
        stype = None
        shader_code = ["", ""]
        with open(filepath, "r") as f:
            while line := f.readline():
                if line.find("#shader") != -1:
                    if line.find("vertex") != -1:
                        stype = 0
                    elif line.find("fragment") != -1:
                        stype = 1
                else:
                    shader_code[stype] += line
        return shader_code

    @staticmethod
    def compile_shader(shader_type, shader_code, name):
        """
        Create a shader from its code and type
        :param shader_type: Vertex or Fragment
        :param shader_code: Shader code in a string
        :param name: For debugging purposes
        :return:
        """
        shader = glCreateShader(shader_type)
        glShaderSource(shader, shader_code)
        glCompileShader(shader)
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(shader).decode()
            raise RuntimeError(f"{name} shader compilation error: {error}")
        return shader


class Material:
    """
    Matrials hold shaders and uniforms
    This is a hasty implementation
    """
    def __init__(self, filepath):
        self.shader = Shader(filepath)
        self.uniforms = dict()

    def add_uniform(self, utype, name, value):
        self.uniforms[name] = (utype, value)                                              # TODO - Implement Materials

    def bind(self):
        self.shader.bind()
        for name, (utype, value) in self.uniforms.items():
            utype(name, value)

    @property
    def program(self):
        return self.shader.program

    def copy(self):
        return copy.deepcopy(self)

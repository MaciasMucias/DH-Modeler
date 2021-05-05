from OpenGL.GL import *
import numpy as np


class Shader:
    def __init__(self, filepath):
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

    def set_uniform_4f(self, name, v0, v1, v2, v3):
        glUniform4f(self.get_uniform_location(name), v0, v1, v2, v3)

    def set_uniform_mat4f(self, name, mat):
        glUniformMatrix4fv(self.get_uniform_location(name), 1, GL_FALSE, np.array(mat))

    def get_uniform_location(self, name):
        if name in self.__uniform_location_cache.keys():
            return self.__uniform_location_cache[name]

        location = glGetUniformLocation(self.__renderer_id, name)

        if location == -1:
            print(f"Warning: inform {name} doesn't exist")
        self.__uniform_location_cache[name] = location
        return location

    def create_shader(self):
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
        shader = glCreateShader(shader_type)
        glShaderSource(shader, shader_code)
        glCompileShader(shader)
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(shader).decode()
            raise RuntimeError("%s shader compilation error: %s", name, error)
        return shader


class Material:
    def __init__(self, shader):
        self.shader = shader

    def add_uniform(self, name, value):
        pass                                                                      # TODO - Implement Materials

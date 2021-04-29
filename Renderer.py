from OpenGL.GL import *
from inspect import currentframe, getframeinfo


def glClearError():
    while glGetError() != GL_NO_ERROR:
        pass


def glLogCall(function):
    glClearError()
    function()
    while error := glGetError():
        print(getframeinfo(currentframe()).filename + ':' + str(getframeinfo(currentframe()).lineno) + ' - ', error)

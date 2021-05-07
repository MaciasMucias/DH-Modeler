from OpenGL.GL import *
import glm
from PyQt5 import QtWidgets

from Renderer import Renderer
from Matrices import mat4, ViewMat


class GLWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, glFormat, Robot, parent=None):
        super(GLWidget, self).__init__(parent)
        self.Robot = Robot
        self.setFormat(glFormat)

    def initializeGL(self) -> None:
        self.Robot.initialise()
        glEnable(GL_DEPTH_TEST)

        self.view = ViewMat()

        self.view.rotate(90, (0, 0, 1))
        self.view.rotate(-90, (0, 1, 0))
        self.view.translate(50, 0, 3)
        self.view.rotate(30, (0, 1, 0))

    def resizeGL(self, w: int, h: int) -> None:
        self.proj = mat4(glm.perspective(75, w / h, 0.1, 100))

    def paintGL(self):
        Renderer.clear()
        self.Robot.draw(self.proj.mat, self.view.mat)

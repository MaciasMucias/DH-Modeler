import numpy as np
from OpenGL.GL import *
import glm
from PyQt5 import QtGui, QtWidgets

from Renderer import Renderer
from Matrices import mat4, ViewMat


class GLWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, glFormat, Robot, parent=None):
        super(GLWidget, self).__init__(parent)
        self.Robot = Robot
        self.setFormat(glFormat)

        self.mouse_down = False
        self.x = self.y = None
        self.rh = 0
        self.rv = 30

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

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_down = True
        self.x, self.y = a0.x(), a0.y()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_down = False

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.mouse_down:
            x, y = a0.x(), a0.y()
            dx, dy = (x - self.x) * 0.25, (y - self.y)*0.25
            self.x, self.y = a0.x(), a0.y()
            if self.rv + dy < -90:
                dy = -90 - self.rv
            elif self.rv + dy > 90:
                dy = 90 - self.rv
            self.view.rotate(dy, (np.sin(np.radians(self.rh)), np.cos(np.radians(self.rh)), 0))
            self.rv += dy
            self.view.rotate(dx, (0, 0, 1))
            self.rh += dx
            self.update()

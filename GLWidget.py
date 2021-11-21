import numpy as np
from OpenGL.GL import *
import glm
from PyQt5 import QtGui, QtWidgets

from Renderer import Renderer
from Matrices import mat4, ViewMat

MOUSE_DRAG_SPEED = 0.25


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

        # create and place camera
        self.view = ViewMat()

        self.view.rotate(90, (0, 0, 1))
        self.view.rotate(-90, (0, 1, 0))
        self.view.translate(50, 0, 3)
        self.view.rotate(30, (0, 1, 0))

    def resizeGL(self, w: int, h: int) -> None:
        # Create new projection matrix based on the new window size
        self.proj = mat4(glm.perspective(75, w / h, 0.1, 100))

    def paintGL(self):
        # Draw a new frame
        Renderer.clear()
        self.Robot.draw(self.proj.mat, self.view.mat)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        # Indicate that a mouse button has been pressed and ave location of the press
        self.mouse_down = True
        self.x, self.y = a0.x(), a0.y()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        # Indicate that a mouse button has been released
        self.mouse_down = False

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.mouse_down:
            # if a mouse button is being held down calculate the change of mouse position
            x, y = a0.x(), a0.y()
            dx, dy = (x - self.x) * MOUSE_DRAG_SPEED, (y - self.y) * MOUSE_DRAG_SPEED
            self.x, self.y = a0.x(), a0.y()

            # if the change in vertical rotation would cause the camera to cross the z axis
            # then set dy to a value that will place the camera exactly on the z axis
            if self.rv + dy < -90:
                dy = -90 - self.rv
            elif self.rv + dy > 90:
                dy = 90 - self.rv

            # rotate around an axis perpendicular to the camera
            self.view.rotate(dy, (np.sin(np.radians(self.rh)), np.cos(np.radians(self.rh)), 0))
            self.rv += dy
            self.view.rotate(dx, (0, 0, 1))
            self.rh += dx
            self.update()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Prototyp1.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from OpenGL.GL import *
import glm

from CoordSys import Robot
from Shader import Shader
from Renderer import Renderer
from Objects3D import Object3D, Cube


Robot = Robot()


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()

    # noinspection PyUnresolvedReferences
    def setupUi(self, glFormat, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.openGLWidget = GLWidget(glFormat, self.centralwidget)
        self.openGLWidget.setGeometry(QtCore.QRect(0, 0, 821, 461))
        self.openGLWidget.setMouseTracking(False)
        self.openGLWidget.setObjectName("openGLWidget")
        self.joint_menu = QtWidgets.QComboBox(self.centralwidget)
        self.joint_menu.setGeometry(QtCore.QRect(90, 530, 31, 21))
        self.joint_menu.setEditable(False)
        self.joint_menu.setObjectName("joint_menu")
        self.append_button = QtWidgets.QPushButton(self.centralwidget)
        self.append_button.setGeometry(QtCore.QRect(10, 470, 75, 23))
        self.append_button.setFlat(False)
        self.append_button.setObjectName("append_button")
        self.insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.insert_button.setGeometry(QtCore.QRect(10, 500, 75, 23))
        self.insert_button.setObjectName("insert_button")
        self.pop_button = QtWidgets.QPushButton(self.centralwidget)
        self.pop_button.setGeometry(QtCore.QRect(90, 470, 75, 23))
        self.pop_button.setObjectName("pop_button")
        self.remove_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_button.setGeometry(QtCore.QRect(90, 500, 75, 23))
        self.remove_button.setObjectName("remove_button")
        self.menu_label = QtWidgets.QLabel(self.centralwidget)
        self.menu_label.setGeometry(QtCore.QRect(10, 530, 71, 16))
        self.menu_label.setObjectName("menu_label")
        self.alpha_input = QtWidgets.QLineEdit(self.centralwidget)
        self.alpha_input.setGeometry(QtCore.QRect(200, 530, 41, 21))
        self.alpha_input.setObjectName("alpha_input")
        self.a_input = QtWidgets.QLineEdit(self.centralwidget)
        self.a_input.setGeometry(QtCore.QRect(250, 530, 41, 21))
        self.a_input.setObjectName("a_input")
        self.d_input = QtWidgets.QLineEdit(self.centralwidget)
        self.d_input.setGeometry(QtCore.QRect(300, 530, 41, 21))
        self.d_input.setObjectName("d_input")
        self.theta_input = QtWidgets.QLineEdit(self.centralwidget)
        self.theta_input.setGeometry(QtCore.QRect(350, 530, 41, 21))
        self.theta_input.setObjectName("theta_input")
        self.alpha_label = QtWidgets.QLabel(self.centralwidget)
        self.alpha_label.setGeometry(QtCore.QRect(215, 510, 16, 16))
        self.alpha_label.setObjectName("alpha_label")
        self.a_label = QtWidgets.QLabel(self.centralwidget)
        self.a_label.setEnabled(True)
        self.a_label.setGeometry(QtCore.QRect(265, 510, 16, 16))
        self.a_label.setObjectName("a_label")
        self.d_label = QtWidgets.QLabel(self.centralwidget)
        self.d_label.setGeometry(QtCore.QRect(315, 510, 16, 16))
        self.d_label.setObjectName("d_label")
        self.theta_label = QtWidgets.QLabel(self.centralwidget)
        self.theta_label.setGeometry(QtCore.QRect(365, 510, 16, 16))
        self.theta_label.setObjectName("theta_label")
        self.d_var = QtWidgets.QCheckBox(self.centralwidget)
        self.d_var.setGeometry(QtCore.QRect(300, 560, 41, 17))
        self.d_var.setObjectName("d_var")
        self.theta_var = QtWidgets.QCheckBox(self.centralwidget)
        self.theta_var.setGeometry(QtCore.QRect(350, 560, 41, 17))
        self.theta_var.setObjectName("theta_var")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menu_label.setBuddy(self.joint_menu)
        self.alpha_label.setBuddy(self.alpha_input)
        self.a_label.setBuddy(self.a_input)
        self.d_label.setBuddy(self.d_input)
        self.theta_label.setBuddy(self.theta_input)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.openGLWidget.update)
        self.timer.start(33)

        self.joint_menu.addItem("1")

        self.append_button.clicked.connect(self.append_joint)
        self.insert_button.clicked.connect(self.insert_joint)
        self.pop_button.clicked.connect(self.pop_joint)
        self.remove_button.clicked.connect(self.remove_joint)
        self.joint_menu.currentIndexChanged.connect(self.switch_joint)
        self.alpha_input.editingFinished.connect(self.change_alpha)
        self.a_input.editingFinished.connect(self.change_a)
        self.d_input.editingFinished.connect(self.change_d)
        self.theta_input.editingFinished.connect(self.change_theta)
        self.d_var.clicked.connect(self.change_d_var)
        self.theta_var.clicked.connect(self.change_theta_var)

        self.alpha_input.setText("0.0")
        self.a_input.setText("0.0")
        self.d_input.setText("0.0")
        self.theta_input.setText("0.0")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.append_button, self.insert_button)
        MainWindow.setTabOrder(self.insert_button, self.pop_button)
        MainWindow.setTabOrder(self.pop_button, self.remove_button)
        MainWindow.setTabOrder(self.remove_button, self.joint_menu)
        MainWindow.setTabOrder(self.joint_menu, self.alpha_input)
        MainWindow.setTabOrder(self.alpha_input, self.a_input)
        MainWindow.setTabOrder(self.a_input, self.d_input)
        MainWindow.setTabOrder(self.d_input, self.d_var)
        MainWindow.setTabOrder(self.d_var, self.theta_input)
        MainWindow.setTabOrder(self.theta_input, self.theta_var)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.append_button.setText(_translate("MainWindow", "Append Joint"))
        self.insert_button.setText(_translate("MainWindow", "Insert Joint"))
        self.pop_button.setText(_translate("MainWindow", "Pop Joint"))
        self.remove_button.setText(_translate("MainWindow", "Remove Joint"))
        self.menu_label.setText(_translate("MainWindow", "Current Joint"))
        self.alpha_label.setText(_translate("MainWindow", "<html><head/><body><p>&alpha;</p></body></html>"))
        self.a_label.setText(_translate("MainWindow", "a"))
        self.d_label.setText(_translate("MainWindow", "d"))
        self.theta_label.setText(_translate("MainWindow", "<html><head/><body><p>&theta;</p></body></html>"))
        self.theta_var.setText(_translate("MainWindow", "var"))
        self.d_var.setText(_translate("MainWindow", "var"))

    def append_joint(self):
        if Robot.append_joint():
            self.joint_menu.addItem(str(Robot.len-1))

    def insert_joint(self):
        if Robot.insert_joint(self.joint_menu.currentIndex()):
            self.joint_menu.addItem(str(Robot.len-1))
            self.joint_menu.setCurrentIndex(self.joint_menu.currentIndex() + 1)

    def pop_joint(self):
        if Robot.pop_joint():
            self.joint_menu.removeItem(self.joint_menu.count()-1)

    def remove_joint(self):
        if Robot.remove_joint(self.joint_menu.currentIndex()):
            self.joint_menu.removeItem(self.joint_menu.count()-1)
            self.switch_joint()

    def switch_joint(self):
        i = self.joint_menu.currentIndex()
        self.alpha_input.setText(str(Robot.return_joint(i).alpha))
        self.a_input.setText(str(Robot.return_joint(i).a))
        self.d_input.setText(str(Robot.return_joint(i).d))
        self.theta_input.setText(str(Robot.return_joint(i).theta))
        self.d_var.setChecked(Robot.return_joint(i).d_var)
        self.theta_var.setChecked(Robot.return_joint(i).theta_var)

    def change_alpha(self):
        Robot.return_joint(self.joint_menu.currentIndex()).alpha = float(self.alpha_input.text())

    def change_a(self):
        Robot.return_joint(self.joint_menu.currentIndex()).a = float(self.a_input.text())

    def change_d(self):
        Robot.return_joint(self.joint_menu.currentIndex()).d = float(self.d_input.text())

    def change_theta(self):
        Robot.return_joint(self.joint_menu.currentIndex()).theta = float(self.theta_input.text())

    def change_d_var(self):
        Robot.return_joint(self.joint_menu.currentIndex()).d_var = self.d_var.isChecked()

    def change_theta_var(self):
        Robot.return_joint(self.joint_menu.currentIndex()).theta_var = self.theta_var.isChecked()


class GLWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, glFormat, parent=None):
        super(GLWidget, self).__init__(parent)
        self.setFormat(glFormat)

    def initializeGL(self) -> None:

        self.proj = glm.ortho(-821/200, 821/200, -461/200, 461/200)

        self.shader = Shader("./res/shaders/cube.shader")

        self.cube = Cube((1, 0, 0), self.shader)
        self.Object = Object3D(self.cube)
        self.Object.set_rotate(glm.pi()/4, glm.vec3(0, 0, 1))

    def paintGL(self):

        Renderer.clear()

        self.Object.set_rotate(5, glm.vec3(1, 0, 0))
        self.Object.draw(self.proj)


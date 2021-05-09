# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Prototyp2.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets

from CoordSys import Robot
from GLWidget import GLWidget

Robot = Robot()


class Ui_MainWindow(object):
    def setupUi(self, glFormat, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(400, 300))
        self.centralwidget.setMaximumSize(QtCore.QSize(1920, 1080))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.openGLWidget = GLWidget(glFormat, Robot, self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openGLWidget.sizePolicy().hasHeightForWidth())
        self.openGLWidget.setSizePolicy(sizePolicy)
        self.openGLWidget.setMinimumSize(QtCore.QSize(400, 300))
        self.openGLWidget.setMaximumSize(QtCore.QSize(1920, 1080))
        self.openGLWidget.setMouseTracking(True)
        self.openGLWidget.setObjectName("openGLWidget")
        self.gridLayout_3.addWidget(self.openGLWidget, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.append_button = QtWidgets.QPushButton(self.centralwidget)
        self.append_button.setMaximumSize(QtCore.QSize(80, 40))
        self.append_button.setFlat(False)
        self.append_button.setObjectName("append_button")
        self.gridLayout_2.addWidget(self.append_button, 0, 0, 1, 1)
        self.remove_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_button.setMaximumSize(QtCore.QSize(80, 40))
        self.remove_button.setObjectName("remove_button")
        self.gridLayout_2.addWidget(self.remove_button, 1, 1, 1, 1)
        self.menu_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu_label.sizePolicy().hasHeightForWidth())
        self.menu_label.setSizePolicy(sizePolicy)
        self.menu_label.setObjectName("menu_label")
        self.gridLayout_2.addWidget(self.menu_label, 2, 0, 1, 1)
        self.joint_menu = QtWidgets.QComboBox(self.centralwidget)
        self.joint_menu.setMaximumSize(QtCore.QSize(40, 40))
        self.joint_menu.setEditable(False)
        self.joint_menu.setObjectName("joint_menu")
        self.joint_menu.addItem("")
        self.gridLayout_2.addWidget(self.joint_menu, 2, 1, 1, 1)
        self.insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.insert_button.setMaximumSize(QtCore.QSize(80, 40))
        self.insert_button.setObjectName("insert_button")
        self.gridLayout_2.addWidget(self.insert_button, 1, 0, 1, 1)
        self.pop_button = QtWidgets.QPushButton(self.centralwidget)
        self.pop_button.setMaximumSize(QtCore.QSize(80, 40))
        self.pop_button.setObjectName("pop_button")
        self.gridLayout_2.addWidget(self.pop_button, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.d_label = QtWidgets.QLabel(self.centralwidget)
        self.d_label.setMaximumSize(QtCore.QSize(40, 20))
        self.d_label.setObjectName("d_label")
        self.gridLayout.addWidget(self.d_label, 0, 2, 1, 1)
        self.a_input = QtWidgets.QLineEdit(self.centralwidget)
        self.a_input.setMaximumSize(QtCore.QSize(40, 20))
        self.a_input.setObjectName("a_input")
        self.gridLayout.addWidget(self.a_input, 1, 1, 1, 1)
        self.theta_label = QtWidgets.QLabel(self.centralwidget)
        self.theta_label.setMaximumSize(QtCore.QSize(40, 20))
        self.theta_label.setObjectName("theta_label")
        self.gridLayout.addWidget(self.theta_label, 0, 3, 1, 1)
        self.d_input = QtWidgets.QLineEdit(self.centralwidget)
        self.d_input.setMaximumSize(QtCore.QSize(40, 20))
        self.d_input.setObjectName("d_input")
        self.gridLayout.addWidget(self.d_input, 1, 2, 1, 1)
        self.theta_input = QtWidgets.QLineEdit(self.centralwidget)
        self.theta_input.setMaximumSize(QtCore.QSize(40, 20))
        self.theta_input.setObjectName("theta_input")
        self.gridLayout.addWidget(self.theta_input, 1, 3, 1, 1)
        self.theta_var = QtWidgets.QCheckBox(self.centralwidget)
        self.theta_var.setMaximumSize(QtCore.QSize(40, 20))
        self.theta_var.setObjectName("theta_var")
        self.gridLayout.addWidget(self.theta_var, 2, 3, 1, 1)
        self.a_label = QtWidgets.QLabel(self.centralwidget)
        self.a_label.setEnabled(True)
        self.a_label.setMaximumSize(QtCore.QSize(40, 20))
        self.a_label.setObjectName("a_label")
        self.gridLayout.addWidget(self.a_label, 0, 1, 1, 1)
        self.d_var = QtWidgets.QCheckBox(self.centralwidget)
        self.d_var.setObjectName("d_var")
        self.gridLayout.addWidget(self.d_var, 2, 2, 1, 1)
        self.alpha_input = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.alpha_input.sizePolicy().hasHeightForWidth())
        self.alpha_input.setSizePolicy(sizePolicy)
        self.alpha_input.setMaximumSize(QtCore.QSize(40, 20))
        self.alpha_input.setObjectName("alpha_input")
        self.gridLayout.addWidget(self.alpha_input, 1, 0, 1, 1)
        self.alpha_label = QtWidgets.QLabel(self.centralwidget)
        self.alpha_label.setMaximumSize(QtCore.QSize(40, 20))
        self.alpha_label.setObjectName("alpha_label")
        self.gridLayout.addWidget(self.alpha_label, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menu_label.setBuddy(self.joint_menu)
        self.d_label.setBuddy(self.d_input)
        self.theta_label.setBuddy(self.theta_input)
        self.a_label.setBuddy(self.a_input)
        self.alpha_label.setBuddy(self.alpha_input)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.append_button, self.pop_button)
        MainWindow.setTabOrder(self.pop_button, self.insert_button)
        MainWindow.setTabOrder(self.insert_button, self.remove_button)
        MainWindow.setTabOrder(self.remove_button, self.joint_menu)
        MainWindow.setTabOrder(self.joint_menu, self.alpha_input)
        MainWindow.setTabOrder(self.alpha_input, self.a_input)
        MainWindow.setTabOrder(self.a_input, self.d_input)
        MainWindow.setTabOrder(self.d_input, self.d_var)
        MainWindow.setTabOrder(self.d_var, self.theta_input)
        MainWindow.setTabOrder(self.theta_input, self.theta_var)

        self.connect_all()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DH Modeler"))
        self.append_button.setText(_translate("MainWindow", "Append Joint"))
        self.remove_button.setText(_translate("MainWindow", "Remove Joint"))
        self.menu_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">Current Joint</p></body></html>"))
        self.joint_menu.setItemText(0, _translate("MainWindow", "1"))
        self.insert_button.setText(_translate("MainWindow", "Insert Joint"))
        self.pop_button.setText(_translate("MainWindow", "Pop Joint"))
        self.d_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">d</p></body></html>"))
        self.a_input.setText(_translate("MainWindow", "0.0"))
        self.theta_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">&theta;</p></body></html>"))
        self.d_input.setText(_translate("MainWindow", "0.0\n"))
        self.theta_input.setText(_translate("MainWindow", "0.0\n"))
        self.theta_var.setText(_translate("MainWindow", "var"))
        self.a_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">a</p></body></html>"))
        self.d_var.setText(_translate("MainWindow", "var"))
        self.alpha_input.setText(_translate("MainWindow", "0.0"))
        self.alpha_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">α</p></body></html>"))

    def connect_all(self):
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

    def append_joint(self):
        if Robot.append_joint():
            self.joint_menu.addItem(str(Robot.len-1))
            self.joint_menu.setCurrentIndex(Robot.len-2)

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
        joint_num = self.joint_menu.currentIndex()
        joint = Robot.return_joint(joint_num)
        text = self.alpha_input.text()
        joint.alpha = float(text if text != "" else 0)
        Robot.update_joint(joint_num)
        self.openGLWidget.update()

    def change_a(self):
        joint_num = self.joint_menu.currentIndex()
        joint = Robot.return_joint(joint_num)
        text = self.a_input.text()
        joint.a = float(text if text != "" else 0)
        Robot.update_joint(joint_num)
        self.openGLWidget.update()

    def change_d(self):
        joint_num = self.joint_menu.currentIndex()
        joint = Robot.return_joint(joint_num)
        text = self.d_input.text()
        joint.d = float(text if text != "" else 0)
        Robot.update_joint(joint_num)
        self.openGLWidget.update()

    def change_theta(self):
        joint_num = self.joint_menu.currentIndex()
        joint = Robot.return_joint(joint_num)
        text = self.theta_input.text()
        joint.theta = float(text if text != "" else 0)
        Robot.update_joint(joint_num)
        self.openGLWidget.update()

    def change_d_var(self):
        d_on = self.d_var.isChecked()
        Robot.return_joint(self.joint_menu.currentIndex()).d_var = d_on
        if d_on:
            self.theta_var.setChecked(False)
        self.openGLWidget.update()

    def change_theta_var(self):
        theta_on = self.theta_var.isChecked()
        Robot.return_joint(self.joint_menu.currentIndex()).theta_var = theta_on
        if theta_on:
            self.d_var.setChecked(False)
        self.openGLWidget.update()

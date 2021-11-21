from GUI import Ui_MainWindow
from PyQt5 import QtGui, QtWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    glFormat = QtGui.QSurfaceFormat()
    ui = Ui_MainWindow()
    ui.setupUi(glFormat, MainWindow)
    MainWindow.show()
    code = app.exec_()
    sys.exit(code)

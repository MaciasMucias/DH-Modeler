from CoordSys import Joint
from GUI import QtWidgets, Ui_MainWindow


if __name__ == "__main__":
    import sys

    Robot = Joint(None)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

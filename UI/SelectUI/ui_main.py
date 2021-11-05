# Installed Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from PyQt6 import QtCore, QtGui, QtWidgets


# VAR DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
WINDOW_WIDTH    = 1000
WINDOW_HEIGHT   = 450

# Ui_MainWindow Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class Ui_MainWindow(object):
    def setupUi(self, MainWindow:QtWidgets.QMainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralwidget")

        self.quitButton = QtWidgets.QPushButton('Done', MainWindow)
        self.mainLayout = QtWidgets.QVBoxLayout()

        self.centralWidget.setLayout(self.mainLayout)
        MainWindow.setCentralWidget(self.centralWidget)


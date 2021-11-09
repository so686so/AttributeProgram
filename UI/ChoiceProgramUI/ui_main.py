# Installed Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from PyQt6 import QtCore, QtGui, QtWidgets


# VAR DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
WINDOW_WIDTH    = 600
WINDOW_HEIGHT   = 100

# Ui_MainWindow Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class Ui_MainWindow(object):
    def setupUi(self, MainWindow:QtWidgets.QMainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.setWindowTitle('Select RunProgram')
        MainWindow.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        MainWindow.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.centralWidget          = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralwidget")

        self.selectProgramComboBox  = QtWidgets.QComboBox(MainWindow)
        self.selectProgramBtn       = QtWidgets.QPushButton('Select', MainWindow)

        self.detailGroupBox         = QtWidgets.QGroupBox('Information', MainWindow)
        self.detailLabel            = QtWidgets.QLabel(MainWindow)

        self.upper_H_Layout = QtWidgets.QHBoxLayout()
        self.upper_H_Layout.addWidget(self.selectProgramComboBox, 10)
        self.upper_H_Layout.addWidget(self.selectProgramBtn, 1)

        self.lower_H_Layout = QtWidgets.QHBoxLayout()
        self.lower_H_Layout.addWidget(self.detailLabel)
        self.detailGroupBox.setLayout(self.lower_H_Layout)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.upper_H_Layout, 1)
        self.mainLayout.addWidget(self.detailGroupBox, 1)

        self.centralWidget.setLayout(self.mainLayout)
        MainWindow.setCentralWidget(self.centralWidget)
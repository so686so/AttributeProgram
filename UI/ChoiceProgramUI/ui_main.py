# Installed Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from PyQt6 import QtCore, QtGui, QtWidgets


# VAR DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
WINDOW_WIDTH    = 600
WINDOW_HEIGHT   = 200

# Ui_MainWindow Class (MainWindow)
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class Ui_MainWindow(object):
    def setupUi(self, MainWindow:QtWidgets.QMainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.setWindowTitle('Select RunProgram')
        MainWindow.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        MainWindow.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.centralWidget          = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralwidget")

        self.selectProgramGroupBox  = QtWidgets.QGroupBox(MainWindow)

        self.selectProgramComboBox  = QtWidgets.QComboBox(MainWindow)
        self.selectProgramBtn       = QtWidgets.QPushButton('Run', MainWindow)

        self.currentClassGroupBox   = QtWidgets.QGroupBox('Current', MainWindow)
        self.currentClassLabel      = QtWidgets.QLabel(MainWindow)

        self.selectClassGroupBox    = QtWidgets.QGroupBox('Select Class', MainWindow)
        self.selectClassComboBox    = QtWidgets.QComboBox(MainWindow)
        self.selectClassBtn         = QtWidgets.QPushButton('Set', MainWindow)

        self.detailGroupBox         = QtWidgets.QGroupBox('Information', MainWindow)
        self.detailLabel            = QtWidgets.QLabel(MainWindow)

        self.upper_H_Layout = QtWidgets.QHBoxLayout()
        self.upper_H_Layout.addWidget(self.selectProgramComboBox, 10)
        self.upper_H_Layout.addWidget(self.selectProgramBtn, 1)
        self.selectProgramGroupBox.setLayout(self.upper_H_Layout)

        self.middle_left_H_Layout   = QtWidgets.QHBoxLayout()
        self.middle_right_H_Layout  = QtWidgets.QHBoxLayout()

        self.middle_left_H_Layout.addWidget(self.currentClassLabel)
        self.middle_right_H_Layout.addWidget(self.selectClassComboBox, 6)
        self.middle_right_H_Layout.addWidget(self.selectClassBtn, 1)

        self.currentClassGroupBox.setLayout(self.middle_left_H_Layout)
        self.selectClassGroupBox.setLayout(self.middle_right_H_Layout)

        self.middle_H_Layout = QtWidgets.QHBoxLayout()
        self.middle_H_Layout.addWidget(self.currentClassGroupBox, 1)
        self.middle_H_Layout.addWidget(self.selectClassGroupBox, 3)

        self.lower_H_Layout = QtWidgets.QHBoxLayout()
        self.lower_H_Layout.addWidget(self.detailLabel)
        self.detailGroupBox.setLayout(self.lower_H_Layout)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.selectProgramGroupBox, 1)
        self.mainLayout.addLayout(self.middle_H_Layout, 1)
        self.mainLayout.addWidget(self.detailGroupBox, 1)

        self.centralWidget.setLayout(self.mainLayout)
        MainWindow.setCentralWidget(self.centralWidget)
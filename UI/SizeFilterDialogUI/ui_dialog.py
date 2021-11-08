# Installed Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from PyQt6 import QtCore, QtGui, QtWidgets


# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import sys
import os
import copy


# Add Import Path
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from CoreDefine import *


# Var
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
ComboBoxList = ['common', 'head', 'upper', 'lower']


class SizeFilterDialog(QtWidgets.QDialog):
    def __init__(self, defaultDict:dict):
        super().__init__()
        self.initUI()
        self.setConnect()
        self.setDefaultValue(defaultDict)

    def initUI(self):
        self.setWindowTitle('Size Filter Option')
        self.resize(500, 200)

        self.mainLayout     = QtWidgets.QVBoxLayout()
        self.upperLayout    = QtWidgets.QHBoxLayout()
        self.middleLayout   = QtWidgets.QHBoxLayout()
        self.underLayout    = QtWidgets.QHBoxLayout()

        self.LineList       = [QtWidgets.QFrame() for _ in range(3)]
        for eachLine in self.LineList:
            eachLine.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            eachLine.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.selectSortComboBox = QtWidgets.QComboBox(self)
        self.selectSortComboBox.addItems(ComboBoxList)

        self.checkLenRBtn   = QtWidgets.QRadioButton('Length Filter')
        self.checkLenRBtn.setObjectName('Length')
        self.checkLenRBtn.setChecked(True)
        self.checkSizeRBtn  = QtWidgets.QRadioButton('Size Filter')
        self.checkSizeRBtn.setObjectName('Size')

        self.upperLayout.addWidget(self.checkLenRBtn, 4)
        self.upperLayout.addWidget(self.checkSizeRBtn, 2)

        self.widthLE        = QtWidgets.QLineEdit(self)
        self.heightLE       = QtWidgets.QLineEdit(self)
        self.sizeLE         = QtWidgets.QLineEdit(self)
        self.sizeLE.setEnabled(False)

        self.widthLE.setText('0')
        self.heightLE.setText('0')
        self.sizeLE.setText('0')

        self.lenGroupBox    = QtWidgets.QGroupBox('Length')
        self.lenHBox        = QtWidgets.QHBoxLayout()

        self.sizeGroupBox   = QtWidgets.QGroupBox('Size')
        self.sizeHBox       = QtWidgets.QHBoxLayout()

        self.lenHBox.addWidget(QtWidgets.QLabel('WIDTH'), 2)
        self.lenHBox.addWidget(self.widthLE, 1)
        self.lenHBox.addSpacing(20)
        self.lenHBox.addWidget(QtWidgets.QLabel('HEIGHT'), 2)
        self.lenHBox.addWidget(self.heightLE, 1)

        self.sizeHBox.addWidget(QtWidgets.QLabel('SIZE'), 2)
        self.sizeHBox.addWidget(self.sizeLE, 1)

        self.lenGroupBox.setLayout(self.lenHBox)
        self.sizeGroupBox.setLayout(self.sizeHBox)

        self.middleLayout.addWidget(self.lenGroupBox, 2)
        self.middleLayout.addWidget(self.sizeGroupBox, 1)

        btnOK       = QtWidgets.QPushButton('Apply')
        btnCancel   = QtWidgets.QPushButton('Cancel')

        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel.clicked.connect(self.onCancelButtonClicked)

        self.underLayout.addWidget(btnOK)
        self.underLayout.addWidget(btnCancel)

        self.mainLayout.addWidget(self.selectSortComboBox)
        self.mainLayout.addWidget(self.LineList[0])
        self.mainLayout.addLayout(self.upperLayout)
        self.mainLayout.addWidget(self.LineList[1])
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.addWidget(self.LineList[2])
        self.mainLayout.addLayout(self.underLayout)

        self.setLayout(self.mainLayout)

    def setDefaultValue(self, defValDict:dict):
        selectLabel = None
        for k, v in defValDict.items():
            if defValDict[k]['isCheck'] == True:
                selectLabel = k

        if not selectLabel:
            return

        for idx, each in enumerate(ComboBoxList):
            if selectLabel == each:
                self.selectSortComboBox.setCurrentIndex(idx)

        if defValDict[selectLabel]['CheckSize'] == True:
            self.checkSizeRBtn.setChecked(True)

        self.widthLE.setText(str(defValDict[selectLabel]['Width']))
        self.heightLE.setText(str(defValDict[selectLabel]['Height']))
        self.sizeLE.setText(str(defValDict[selectLabel]['Size']))

    def setConnect(self):
        self.checkLenRBtn.toggled.connect(self.onClickedRdBtn)
        self.checkSizeRBtn.toggled.connect(self.onClickedRdBtn)

    def onClickedRdBtn(self):
        radioBtn = self.sender()
        BtnName = radioBtn.objectName()
        if radioBtn.isChecked():
            if BtnName == 'Length':
                self.widthLE.setEnabled(True)
                self.heightLE.setEnabled(True)
                self.sizeLE.setEnabled(False)
            else:
                self.widthLE.setEnabled(False)
                self.heightLE.setEnabled(False)
                self.sizeLE.setEnabled(True)

    def onOKButtonClicked(self):
        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModalDialog(self):
        return super().exec()

    def getFilterDict(self):
        resDict = copy.copy(CORE_SIZE_FILTER_DICT)

        selectLabelName = self.selectSortComboBox.currentText()

        resDict[selectLabelName]['isCheck'] = True

        if self.checkSizeRBtn.isChecked():
            resDict[selectLabelName]['CheckSize'] = True

        resDict[selectLabelName]['Width'] = int(self.widthLE.text())
        resDict[selectLabelName]['Height'] = int(self.heightLE.text())
        resDict[selectLabelName]['Size'] = int(self.sizeLE.text())

        return resDict


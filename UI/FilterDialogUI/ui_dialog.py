# Installed Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from PyQt6 import QtCore, QtGui, QtWidgets

from Core.CommonUse import NoticeLog

ClassSort   = ['39CLASS', '66CLASS', '83CLASS']
ClassNum    = [39, 66, 83]

SubSelect   = ['-Select-', 'True', 'False']

DATA_DICT   = -1
ATT_NAME    = 0
ATT_TEXT    = 1

RESET_MSG   = '(Attribute[0] == "1") or (Attribute[1] == "1")'

class ConditionFilterDialog(QtWidgets.QDialog):
    def __init__(self, defaultString, classNameList):
        super().__init__()

        self.FinalCondition     = defaultString
        self.TotalclassNameList = classNameList
        self.curClassNameList   = self.classNameDictToList(0)
        self.curClassDataDict   = self.TotalclassNameList[DATA_DICT]   # {ClassName:[attName, attText]}
        self.TranslateMessage   = ""
        self.TempSaveCondition  = ""

        self.initUI()
        self.setConnect()


    def initUI(self):
        self.setWindowTitle('Create Condition Filter')
        self.resize(500, 800)

        self.mainLayout             = QtWidgets.QVBoxLayout()
        self.LineList               = [QtWidgets.QFrame() for _ in range(4)]
        for eachLine in self.LineList:
            eachLine.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            eachLine.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.selectClassComboBox    = QtWidgets.QComboBox()
        self.selectClassComboBox.addItems(ClassSort)
        self.selectClassComboBox.setCurrentIndex(0)

        self.selectClassBtn         = QtWidgets.QPushButton('Select')

        self.ClassNameListComboBox  = QtWidgets.QComboBox()
        self.ClassNameListComboBox.addItems(self.curClassNameList)
        self.ClassNameListComboBox.setCurrentIndex(0)

        self.subSelectComboBox      = QtWidgets.QComboBox()
        self.subSelectComboBox.addItems(SubSelect)
        self.subSelectComboBox.setCurrentIndex(0)

        self.TokenizerBtn           = QtWidgets.QPushButton('Tokenizer')

        self.TokenLE                = QtWidgets.QLineEdit()
        self.TokenLE.setReadOnly(False)
        self.TotalTE                = QtWidgets.QPlainTextEdit()
        self.TotalTE.setPlainText(self.FinalCondition)
        self.TotalTE.textChanged.connect(self.SyncTransTE)

        self.TransTE                = QtWidgets.QPlainTextEdit()
        self.TransTE.setReadOnly(True)
        self.SyncTransTE()
        
        self.showDetailLabel        = QtWidgets.QLabel('- Detail Info\n- Select Above')

        btnOK       = QtWidgets.QPushButton('Apply')
        btnCancel   = QtWidgets.QPushButton('Cancel')
        btnReset    = QtWidgets.QPushButton('Reset')
        btnUndo     = QtWidgets.QPushButton('Undo')

        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel.clicked.connect(self.onCancelButtonClicked)
        btnReset.clicked.connect(self.onClickResetBtn)
        btnUndo.clicked.connect(self.onClickUndoBtn)

        classSelectHBox = QtWidgets.QHBoxLayout()
        classSelectHBox.addWidget(self.selectClassComboBox, 10)
        classSelectHBox.addWidget(self.selectClassBtn, 2)

        classNameHBox   = QtWidgets.QHBoxLayout()
        classNameHBox.addWidget(self.ClassNameListComboBox, 6)
        classNameHBox.addWidget(self.subSelectComboBox, 2)
        classNameHBox.addWidget(self.TokenizerBtn, 2)

        upperGroupBox   = QtWidgets.QGroupBox('Select For Tokenizer')
        upperVBox       = QtWidgets.QVBoxLayout()

        upperVBox.addLayout(classSelectHBox)
        upperVBox.addLayout(classNameHBox)
        upperGroupBox.setLayout(upperVBox)
        self.mainLayout.addWidget(upperGroupBox, 2)

        self.mainLayout.addWidget(self.LineList[0])

        self.mainLayout.addWidget(self.showDetailLabel, 1)
        self.mainLayout.addWidget(self.LineList[1])

        middleGroupBox  = QtWidgets.QGroupBox('Token Ouput')
        middleVBox      = QtWidgets.QVBoxLayout()

        middleVBox.addWidget(self.TokenLE)
        middleGroupBox.setLayout(middleVBox)

        self.mainLayout.addWidget(middleGroupBox, 1)
        self.mainLayout.addWidget(self.LineList[2])

        underGroupBox   = QtWidgets.QGroupBox('Enter your conditional expression here')
        underVBox       = QtWidgets.QVBoxLayout()
        underVBox.addWidget(self.TransTE, 1)
        underVBox.addWidget(self.TotalTE, 3)
        underGroupBox.setLayout(underVBox)
        self.mainLayout.addWidget(underGroupBox, 5)
        self.mainLayout.addWidget(self.LineList[3])

        midUnderLayout = QtWidgets.QHBoxLayout()

        midUnderLayout.addWidget(btnReset)
        midUnderLayout.addWidget(btnUndo)

        underLayout = QtWidgets.QHBoxLayout()
        underLayout.addWidget(btnOK)
        underLayout.addWidget(btnCancel)

        self.mainLayout.addLayout(midUnderLayout)
        self.mainLayout.addLayout(underLayout)
        self.setLayout(self.mainLayout)

    def onOKButtonClicked(self):
        self.FinalCondition = self.TotalTE.toPlainText()
        self.TranslateCondition()
        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModalDialog(self):
        return super().exec()

    def setConnect(self):
        self.selectClassBtn.clicked.connect(self.onClickSelectClassBtn)
        self.TokenizerBtn.clicked.connect(self.onClickTokenizerBtn)


    def classNameDictToList(self, Idx):
        classNameList = []
        for eachIdx in range(ClassNum[Idx]):
            classNameList.append(f'{self.TotalclassNameList[Idx][eachIdx]}[{eachIdx}]')

        return classNameList


    def onClickSelectClassBtn(self):
        curIdx = self.selectClassComboBox.currentIndex()
        self.curClassNameList = self.classNameDictToList(curIdx)

        self.ClassNameListComboBox.clear()
        self.ClassNameListComboBox.addItems(self.curClassNameList)
        self.ClassNameListComboBox.setCurrentIndex(0)
        self.subSelectComboBox.setCurrentIndex(0)
        self.TokenLE.clear()

        self.showDetailLabel.setText(f'- Class Changed : {ClassSort[curIdx]}')

    
    def onClickTokenizerBtn(self):
        if self.subSelectComboBox.currentIndex() == 0:
            self.showDetailLabel.setText('- There are still choices that have not been picked up')
            return
        else:
            detailData = self.curClassDataDict.get(self.ClassNameListComboBox.currentText().split('[')[0])
            if detailData is None:
                self.showDetailLabel.setText(f'- This is Merged Name')
            else:
                self.showDetailLabel.setText(f'- AttName : {detailData[ATT_NAME]:15}\n- AttText : {detailData[ATT_TEXT]:15}')

            value = 0
            if self.subSelectComboBox.currentText() == 'True':
                value = 1

            tokenLine = f'(Attribute[{self.ClassNameListComboBox.currentIndex()}] == "{value}")'
            self.TokenLE.setText(tokenLine)


    def TranslateCondition(self):
        originText  = self.TotalTE.toPlainText()
        transText   = originText.replace('"1"', 'True')
        transText   = transText.replace('"0"', 'False')

        for idx, eachName in enumerate(self.curClassNameList):
            try:
                transText   = transText.replace(f'Attribute[{idx}]', f'{eachName.split("[")[0]}')
            except Exception as e:
                pass

        self.TranslateMessage = transText


    def onClickResetBtn(self):
        self.TempSaveCondition = self.TotalTE.toPlainText()
        self.TotalTE.setPlainText(RESET_MSG)


    def onClickUndoBtn(self):
        if self.TempSaveCondition:
            self.TotalTE.setPlainText(self.TempSaveCondition)


    def SyncTransTE(self):
        self.TranslateCondition()
        self.TransTE.setPlainText(self.TranslateMessage)
"""
어느 프로그램을 실행할지 고르는 UI

LAST_UPDATE : 2021/11/05
AUTHOR      : SO BYUNG JUN
"""


# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import sys
import os
import copy


# Add Import Path
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../Core'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from CoreDefine import *


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from Core.CommonUse     import *


# Installed Library - QT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from qt_core            import *


# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from .ui_main            import Ui_MainWindow


# ProgramList
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
ProgramList =   [   'AnalysisAttribute',
                    'SliceImage',
                    'MakeClassSource',
                    'ExtractAnnotation',
                    'JoinPath',
                    'FilterCondition',
                ]

# ProgramInformationList
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
DetailList  =   [   '주어진 자료를 분석하고 엑셀 및 그래프로 출력해주는 프로그램',
                    '이미지 폴더를 받아서, COMMON, HEAD, UPPER, LOWER 기준에 맞게 잘라주는 프로그램',
                    '주어진 기준에 맞게 받은 CvatXml 파일 및 ImgName 들을 MakeClass 해주는 프로그램',
                    'Annotation들을 랜덤 추출하거나 스플릿하는 프로그램',
                    'ImgList들의 앞에 일괄적으로 경로를 붙여주는 프로그램',
                    'Annotation들을 Filtering & Limit Count만큼 추출하는 프로그램'
                ]

# ChoiceProgramUI Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class ChoiceProgramUI(QMainWindow):
    def __init__(self, QApp=None):
        super().__init__()

        self.app = QApp
        self.res = 'EXIT'

        self.programNameList    = []
        self.infoDict           = {}

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.initialize()

    def initialize(self):
        self.setProgramNameList()
        self.syncComboBoxToProgramList()
        self.setInfoDict()
        self.ui.detailLabel.setText(self.getProgramInformation())

        self.ui.selectProgramComboBox.currentTextChanged.connect(self.syncDetailLabelToComboBox)
        self.ui.selectProgramBtn.clicked.connect(self.selectDone)

    def setInfoDict(self):
        for idx, eachValue in enumerate(ProgramList):
            self.infoDict[eachValue] = DetailList[idx]

    def getProgramInformation(self):
        return self.infoDict[self.ui.selectProgramComboBox.currentText()]


    def setProgramNameList(self):
        for eachValue in ProgramList:
            self.programNameList.append(eachValue)

    def syncComboBoxToProgramList(self):
        self.ui.selectProgramComboBox.addItems(self.programNameList)

    def syncDetailLabelToComboBox(self):
        self.ui.detailLabel.setText(self.getProgramInformation())

    def selectDone(self):
        self.res = self.ui.selectProgramComboBox.currentText()
        NoticeLog(f'{self.res} Program INIT')
        QCoreApplication.instance().quit()

    def run(self):
        NoticeLog('Select the program you want to run from the UI')
        self.res = 'EXIT'
        self.show()
        self.app.exec()
        return self.res
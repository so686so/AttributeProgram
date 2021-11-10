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
from CoreDefine         import *


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

        self.app                = QApp
        self.res                = 'EXIT'

        self.programNameList    = []
        self.infoDict           = {}

        self.ui                 = Ui_MainWindow()
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


    def __del__(self):
        ChangeCvatXmlPath       = getCoreValue('OriginSource_cvatXml_Path')
        ChangeIamgePath         = getCoreValue('OriginSource_Img_Path')
        ChangeAnnotationPath    = getCoreValue('OriginSource_AnntationPath')
        ChangeImgaeListPath     = getCoreValue('OriginSource_ImageListPath')
        ChangeResDirPath        = getCoreValue('Result_Dir_Path')
        ChangeFilterCondition   = getCoreValue('CORE_FILTER_CONDITION')

        Rmb_CvatLine            = 0
        Rmb_OriImgLine          = 0
        Rmb_AnnoLine            = 0
        Rmb_ImgListLine         = 0
        Rmb_ResDirLine          = 0
        Rmb_FilterLine          = 0

        LineSaveList            = []
        readFileToList('CoreDefine.py', LineSaveList)

        for idx, eachLine in enumerate(LineSaveList):
            Tmp_Rmb_CvatLine    = eachLine.find('OriginSource_cvatXml_Path   =')
            Tmp_Rmb_OriImgLine  = eachLine.find('OriginSource_Img_Path       =')
            Tmp_Rmb_AnnoLine    = eachLine.find('OriginSource_AnntationPath  =')
            Tmp_Rmb_ImgListLine = eachLine.find('OriginSource_ImageListPath  =')
            Tmp_Rmb_ResDirLine  = eachLine.find('Result_Dir_Path             =')
            Tmp_Rmb_FilterCond  = eachLine.find('CORE_FILTER_CONDITION   =')

            if Tmp_Rmb_CvatLine >= 0:
                Rmb_CvatLine    = idx
            elif Tmp_Rmb_OriImgLine >= 0:
                Rmb_OriImgLine  = idx
            elif Tmp_Rmb_AnnoLine >= 0:
                Rmb_AnnoLine    = idx
            elif Tmp_Rmb_ImgListLine >= 0:
                Rmb_ImgListLine = idx
            elif Tmp_Rmb_ResDirLine >= 0:
                Rmb_ResDirLine  = idx
            elif Tmp_Rmb_FilterCond >= 0:
                Rmb_FilterLine  = idx

        with open('CoreDefine.py', 'w', encoding=CORE_ENCODING_FORMAT) as wf:
            for idx, line in enumerate(LineSaveList):
                if idx == Rmb_CvatLine:
                    wf.write(f'OriginSource_cvatXml_Path   = r"{ChangeCvatXmlPath}"\n')
                elif idx == Rmb_OriImgLine:
                    wf.write(f'OriginSource_Img_Path       = r"{ChangeIamgePath}"\n')
                elif idx == Rmb_AnnoLine:
                    wf.write(f'OriginSource_AnntationPath  = r"{ChangeAnnotationPath}"\n')
                elif idx == Rmb_ImgListLine:
                    wf.write(f'OriginSource_ImageListPath  = r"{ChangeImgaeListPath}"\n')
                elif idx == Rmb_ResDirLine:
                    wf.write(f'Result_Dir_Path             = r"{ChangeResDirPath}"\n')
                elif idx == Rmb_FilterLine:
                    wf.write(f"CORE_FILTER_CONDITION   = '{ChangeFilterCondition}'\n")
                else:
                    wf.write(f'{line}\n')

        SuccessLog('Changed values are overwritten in CoreDefine\n')
        

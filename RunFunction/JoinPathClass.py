"""
ImgList Line 마다 경로를 추가해주는 클래스

LAST_UPDATE : 21/10/19
AUTHOR      : SO BYUNG JUN
"""

# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import os
import sys


# Add Import Path
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../UI/SelectUI'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Core'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from CoreDefine import *


# Custom Modules
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.CommonUse         import *
from Core.SingletonClass    import Singleton


# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from UI.SelectUI.SelectUIClass import *


# SOURCE & DEST PATH
# 해당 OriginXmlDirPath 과 ResultDirPath 값을 변경하고 싶으면, CoreDefine.py 에서 변경하면 됨! ( 경로 변경 통합 )
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
ImgListFile         = r"C:/PythonHN/Data/Result/39Class_ImgList.txt"
ResultDirPath       = copy.copy(Result_Dir_Path)

encodingFormat      = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat      = copy.copy(VALID_IMG_FORMAT)


# 결과값 저장 파일 이름
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
AddPrefixFileName   = "JoinPath"
JoinDirPath         = r"Please Write This..."


# 파일 경로 병합 클래스
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class JoinPath(Singleton):
    def __init__(self, QApp):
        self.app = QApp
        self.ProgramName = "JoinPath"

        self.OriginImgList = []

        self.initJP()

    def initJP(self):
        self.selectUi = SelectUI(self.setInitSettingForSelectUI, self.getEditSettingForSelectUI)

        self.selectUi.show()
        self.app.exec()

        if self.selectUi.isSelectDone is False:
            return

        NoticeLog(f'JoinPath : {JoinDirPath}')


    def openImgListFile(self):
        with open(ImgListFile, 'r', encoding=encodingFormat) as f:
            for eachLine in f:
                eachLine = eachLine.strip('\n')
                self.OriginImgList.append(eachLine)

        SuccessLog(f"openImgList File Read Done - {ImgListFile}")


    def writeImgListFileWithJoinPath(self):
        fileName = os.path.basename(ImgListFile)
        fileName = f'{AddPrefixFileName}_{fileName}'
        savePath = os.path.join(ResultDirPath, fileName)       

        with open(savePath, 'w', encoding=encodingFormat) as f:
            for line in self.OriginImgList:
                resLine = os.path.join(JoinDirPath, line)
                f.write(f'{resLine}\n')

        SuccessLog(f"JoinPath Result File Read Done - {savePath}")


    def setInitSettingForSelectUI(self):
        """
            - ImgListFile      
            - ResultDirPath         
            - JoinDirPath       
        """
        self.sendArgsList = [   ['FD', 'ImgListFile',             False,   f'{ImgListFile}'],
                                ['FD', 'ResultDirPath',               True,  f'{ResultDirPath}'],

                                ['LE', 'JoinDirPath',                 False,  f'{JoinDirPath}']
                            ]
        return self.ProgramName, self.sendArgsList


    def getEditSettingForSelectUI(self):
        """
            SelectUI 에서 넘겨받은 값 적용
            ---------------------------------------------------------------------
            CallBackOut Function - 
                SelectUI class 생성할 때 인자로 넘겨주면, 거기서 이 함수를 필요할 때 실행한다.
            ---------------------------------------------------------------------
            Attributes :
                returnDict : 
                    {DefineName : Edit Define Value} 의 Dict
        """
        NAME        = 1        
        returnDict  = self.selectUi.getReturnDict()

        print("\n* Change Path/Define Value By SelectUI")
        print("--------------------------------------------------------------------------------------")
        for Arg in self.sendArgsList:
            if returnDict.get(Arg[NAME]) != None:
                # 해당 변수명에 SelectUI 에서 갱신된 값 집어넣기
                globals()[Arg[NAME]] = returnDict[Arg[NAME]]
                showLog(f'- {Arg[NAME]:40} -> {globals()[Arg[NAME]]}')
        print()

    def run(self):
        if self.selectUi.isSelectDone is False:
            NoticeLog(f'{self.__class__.__name__} Program EXIT\n')
        else:
            self.openImgListFile()
            self.writeImgListFileWithJoinPath()

            os.startfile(ResultDirPath)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    RunProgram = JoinPath(App)
    RunProgram.run()
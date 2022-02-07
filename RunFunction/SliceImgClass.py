"""
This Python file is a code created to slice images in the given directory path 
into Common / Head / Upper / Lower images.

Set the USE_X value of the variable you want to slice to True,
Set the source directory path and result directory path.   

Classes :
    SliceImage : 
        INFO : 

        METHODS :
            - run()

LAST_UPDATE : 21/11/09
AUTHOR      : SHY
"""


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import os
import cv2
import sys
import copy


# INSTALLED PACKAGE IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import numpy                    as np


# Add Import Path
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../UI/SelectUI'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Core'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from CoreDefine                 import *


# Custom Modules
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.CommonUse             import *
from Core.CvatXmlClass          import CvatXml
from Core.SingletonClass        import Singleton


# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from UI.SelectUI.SelectUIClass  import *


# VARIABLE DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
USE_COMMON          = True
USE_HEAD            = True
USE_UPPER           = True
USE_LOWER           = True

# 원본 이미지를 축약시킨 폴더 기준으로 작업할 때 :
# 해당 cvat 이미지가 실제로 없어도 에러문구 없이 스킵한다
WORKING_IMG_FILES_ABBREVIATED = False


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
COMMON_PATH         = 0
HEAD_PATH           = 1
UPPER_PATH          = 2
LOWER_PATH          = 3
MAX_LABEL           = 4


# SOURCE & DEST PATH
# 해당 OriginXmlDirPath 과 ResultDirPath 값을 변경하고 싶으면, CoreDefine.py 에서 변경하면 됨! ( 경로 변경 통합 )
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
OriginXmlDirPath    = copy.copy(OriginSource_cvatXml_Path)
OriginImgDirPath    = copy.copy(OriginSource_Img_Path)
ResultDirPath       = copy.copy(Result_Dir_Path)
CrushedImgFilePath  = os.path.join(ResultDirPath, CrushedImgFileName)
AbbreviatedImgPath  = copy.copy(Abbreviated_Img_Path)

encodingFormat      = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat      = copy.copy(VALID_IMG_FORMAT)


# FILE & DIR NAME
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
COMMON_PATH_NAME    = "common_images"
HEAD_PATH_NAME      = "head_images"
UPPER_PATH_NAME     = "upper_images"
LOWER_PATH_NAME     = "lower_images"


# Local Function
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def imread(fileName, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try :
        n   = np.fromfile(fileName, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        error_handling(f"imread() failed in {fileName} - {e}", filename(), lineNum())
        return None


def imwrite(fileName, img, params=None):
    try:
        ext         = os.path.splitext(fileName)[1]
        result, n   = cv2.imencode(ext, img, params)

        if result:
            with open(fileName, mode='w+b') as f:
                 n.tofile(f)
            return True
        else:
            ErrorLog(f"imwrite() failed in {fileName} - cv2.imencode return None",  lineNum=lineNum(), errorFileName=filename())
            return False
    except Exception as e:
        error_handling(f"imwrite() failed in {fileName} - {e}", filename(), lineNum())
        return False


# Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class SliceImage(Singleton, CvatXml):
    def __init__(self, QApp):
        super().__init__(OriginXmlDirPath)
        self.app                = QApp

        # 결과값 저장할 경로
        self.CommonImgDirPath   = ""
        self.HeadImgDirPath     = ""
        self.UpperImgDirPath    = ""
        self.LowerImgDirPath    = ""

        self.savePath           = ["" for _ in range(MAX_LABEL) ]

        # getImgPath() 검색하기 위한 Dict
        self.OriginImgDict      = {}
        self.TotalImageCount    = 0

        # SliceImage 가 실패한 목록들 출력하기 위한 List
        self.SliceFailList      = []

        self.CurBoxList         = []
        self.CurImgName         = ""

        self.sendArgsList       = []

        self.initializeSI()


    def initializeSI(self):
        # RunFunction 이름 지정 - 안하면 Error 뜸!
        self.setRunFunctionName('SLICE_IMAGE')

        # SelectUI 는 다른 initialize 이전에 시행해야 함 : 경로 변수, 판단 변수가 바뀌는 것이기 때문!
        self.selectUi    = SelectUI(self.setInitSettingSelectUI, self.getEditSettingSelectUI)

        # ! Before Initialize
        self.selectUi.show()
        self.app.exec()

        if self.selectUi.isQuitProgram():
            return

        self.initAfterSetUI()


    def initAfterSetUI(self):
        self.initCvatXmlClass()
        self.savePath = self.make_dir_for_slice_img()

        if self.getOriginImgDataDict() is False:
            sys.exit(-1)

        self.TotalImageCount = len(self.OriginImgDict)  


    # SelectUI Function
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    """
        sendArg Type : [ Type(str), WhatPath(str), isDir(bool), DefaultThatPath(str) ]

        Type :
            - FD : File Dialog
            - CB : CheckBox
            - LE : LineEdit

        ARGS :
            - OriginXmlDirPath    
            - OriginImgDirPath    
            - ResultDirPath       
            - AbbreviatedImgPath  
            - CrushedImgFilePath

            - USE_COMMON
            - USE_HEAD
            - USE_UPPER
            - USE_LOWER
            - WORKING_IMG_FILES_ABBREVIATED
    """
    def setInitSettingSelectUI(self):
        self.SyncAllValue()
        self.sendArgsList = [   ['FD', 'OriginXmlDirPath',              True,   f'{OriginXmlDirPath}'],
                                ['FD', 'OriginImgDirPath',              True,   f'{OriginImgDirPath}'],
                                ['FD', 'ResultDirPath',                 True,   f'{ResultDirPath}'],
                                ['FD', 'HLINE_0',                       False,  'None'],
                                ['FD', 'AbbreviatedImgPath',            True,   f'{AbbreviatedImgPath}'],
                                ['FD', 'CrushedImgFilePath',            False,  f'{CrushedImgFilePath}'],

                                ['CB', 'USE_COMMON',                    False,  f'{USE_COMMON}'],
                                ['CB', 'USE_HEAD',                      False,  f'{USE_HEAD}'],
                                ['CB', 'USE_UPPER',                     False,  f'{USE_UPPER}'],
                                ['CB', 'USE_LOWER',                     False,  f'{USE_LOWER}'],
                                ['CB', 'HLINE_1',                       False,  'None'],
                                ['CB', 'WORKING_IMG_FILES_ABBREVIATED', False,  f'{WORKING_IMG_FILES_ABBREVIATED}']
                            ]
        return self.getRunFunctionName(), self.sendArgsList

    def getEditSettingSelectUI(self):
        NAME = 1
        returnDict = self.selectUi.getReturnDict()

        print("\n* Change Path/Define Value By SelectUI")
        print("--------------------------------------------------------------------------------------")
        for Arg in self.sendArgsList:
            eachTarget = Arg[NAME]
            if returnDict.get(eachTarget) != None:
                globals()[eachTarget] = returnDict[eachTarget]
                showLog(f'- {eachTarget:40} -> {globals()[eachTarget]}')            
        showLog("--------------------------------------------------------------------------------------\n")

        self.SyncAllValue()
        setResultDir(ResultDirPath)
        self.setChanged_Xml_n_Res_Path(OriginXmlDirPath, ResultDirPath)

    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-


    def SyncAllValue(self):
        self.SyncEachValue('OriginSource_cvatXml_Path', 'OriginXmlDirPath')
        self.SyncEachValue('OriginSource_Img_Path',     'OriginImgDirPath')
        self.SyncEachValue('Result_Dir_Path',           'ResultDirPath')

    def SyncEachValue(self, CoreName, LinkName, SENDER_DEPTH=3):
        # set 하기 전에 CoreDefine.py의 값을 get
        if callername(SENDER_DEPTH) == 'setInitSettingSelectUI':
            globals()[LinkName] = getCoreValue(CoreName)

        elif callername(SENDER_DEPTH) == 'getEditSettingSelectUI':
            setCoreValue(CoreName, globals()[LinkName])


    # COMMON / HEAD / UPPER / LOWER 중 사용할 폴더 생성하는 함수
    def make_dir_for_slice_img(self):
        print()
        NoticeLog("Make SliceImage Result Dir Start")

        _savePath = [ "" for _ in range(MAX_LABEL) ]

        def makeDirs(subPath):
            img_path = os.path.join(ResultDirPath, subPath)
            img_path = os.path.normpath(img_path)
            os.makedirs(img_path, exist_ok=True)
            SuccessLog(f'Create Done {subPath:15}-> {img_path}')
            return img_path

        if USE_COMMON is True:
            _savePath[COMMON_PATH]  = makeDirs(COMMON_PATH_NAME)
        if USE_HEAD is True:
            _savePath[HEAD_PATH]    = makeDirs(HEAD_PATH_NAME)
        if USE_UPPER is True:
            _savePath[UPPER_PATH]   = makeDirs(UPPER_PATH_NAME)
        if USE_LOWER is True:
            _savePath[LOWER_PATH]   = makeDirs(LOWER_PATH_NAME)

        print()
        return _savePath


    # getImgPath() 검색하기 위한 Dict 만드는 함수
    def getOriginImgDataDict(self):
        # WORKING_IMG_FILES_ABBREVIATED 값에 따라서 workPath 설정
        if WORKING_IMG_FILES_ABBREVIATED is True:
            ModeLog('WORKING_IMG_FILES_ABBREVIATED ON\n')
            workPath = AbbreviatedImgPath
        else:
            workPath = OriginImgDirPath

        # 돌리면서 유효한 이미지 확장자만 추가하기
        self.OriginImgDict = getImageSearchDict(workPath, validImgFormat)

        # 유효한 이미지가 있었을 때
        if self.OriginImgDict is None:
            ErrorLog(f'`{workPath}` is Nothing Vaild Image', lineNum=lineNum(), errorFileName=filename())
            return False

        return True


    # 주어진 imageName 이 OriginImageDirPath 내 파일에 있는 이미지인지, 있다면 어떤 경로인지 리턴하는 함수
    def getImgPath(self, imageName):
        if self.OriginImgDict.get(imageName) == None:
            # If Match Anything AND Not WORKING_IMG_FILES_ABBREVIATED
            if WORKING_IMG_FILES_ABBREVIATED is False:
                error_handling(f"getImgPath() failed - {imageName} is Not Matched", filename(), lineNum())
            return None

        return os.path.join(self.OriginImgDict[imageName], imageName)


    def ImageCrop(self, source, box):
        xTopLeft     = int(float(box.get("xtl")))
        yTopLeft     = int(float(box.get("ytl")))
        xBottomRight = int(float(box.get("xbr")))
        yBottomRight = int(float(box.get("ybr")))

        return source[yTopLeft:yBottomRight, xTopLeft:xBottomRight]


    # Label(Common, Head, Upper, Lower) 값에 따라서 이미지를 실제로 Slice 하는 함수 
    def SliceByLabel(self, ResDir, ImgName, img:np.ndarray, box):

        croped  = self.ImageCrop(img, box)
        res     = imwrite(os.path.join(ResDir, ImgName), croped)

        if res is False:
            return False

        return True


    # OneImgName 이 주어졌을 때, 각 이미지에 대해서 SliceByLabel 로 넘기는 함수
    def SliceOneImg(self, OneImgName, boxList):
        OneImgPath = self.getImgPath(OneImgName)

        # 유효한 이미지 경로 없으면 return False
        if OneImgPath is None:
            return False

        # Type 지정
        img:np.ndarray = imread(OneImgPath)

        # Image Read 실패하면 바로 return False
        if img is None :
            error_handling(f"imread() failed '{OneImgPath}'", filename(), lineNum())
            return False

        # box : xml.etree.ElementTree.Element
        for box in boxList:
            label   = box.get("label")
            res     = True

            if (USE_COMMON is True) and (label=="all"):
                res = self.SliceByLabel(self.savePath[COMMON_PATH], OneImgName, img, box)
            if (USE_HEAD is True) and (label=="head"):
                res = self.SliceByLabel(self.savePath[HEAD_PATH],   OneImgName, img, box)
            if (USE_UPPER is True) and (label=="upper"):
                res = self.SliceByLabel(self.savePath[UPPER_PATH],  OneImgName, img, box)
            if (USE_LOWER is True) and (label=="lower"):
                res = self.SliceByLabel(self.savePath[LOWER_PATH],  OneImgName, img, box)

            if res is False:
                return False

        return True


    # RunFunction 귀여워...
    def RunFunction(self):
        return self.SliceOneImg(self.CurImgName, self.CurBoxList)


    def setRunFunctionParam(self):
        """
            CvatXml 의 가상함수를 상속받아 재정의한 함수
            RunFunction 에 들어가기 전 사용할 Param 을 setting 하는 함수
        """
        self.CurBoxList = self.getCurBoxList()
        self.CurImgName = self.getCurImgName()


    def setAfterRunFunctionParam(self):
        return super().setAfterRunFunctionParam()


    # 가상함수 : RunFunction 의 결과가 fasle 일 때 실행하는 함수
    def AfterRunFunction(self):
        if WORKING_IMG_FILES_ABBREVIATED is False:
            self.SliceFailList.append(self.CurImgName)


    # ABS FUNC(가상 함수) 재정의 함수
    def setFinishFunctionParam(self):
        """
            CvatXml 의 가상함수를 상속받아 재정의한 함수
            사용하지 않지만 정의를 하지 않으면 error 가 뜨기 때문에 그대로 계승

            가상함수는 사용하지 않더라도, 무조건 재정의를 해 줘야 한다.
            ---------------------------------------------------------------------
            Returns : 
                부모 클래스의 함수 그대로 사용 (pass)
            ---------------------------------------------------------------------
        """
        return super().setFinishFunctionParam()


    def FinishFunction(self):
        """
            CvatXml 의 가상함수를 상속받아 재정의한 함수
            Result Sammary 출력하는 함수
        """
        print("[ Crushed Image List ]")

        if self.SliceFailList:
            showListLog(self.SliceFailList)
            writeListToFile(CrushedImgFilePath, self.SliceFailList, encodingFormat)
        else:
            print("- Crushed Image Not Detected! :D")


    def run(self):
        if self.selectUi.isQuitProgram():
            NoticeLog(f'{self.__class__.__name__} Program EXIT\n')
        else:
            super().run()
            os.startfile(ResultDirPath)


if __name__ == "__main__":
    App         = QApplication(sys.argv)
    RunProgram  = SliceImage(App)
    RunProgram.run()
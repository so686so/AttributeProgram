"""
cvatXml 파일과 그에 해당하는 img 원본 경로를 받아서 분석하는 코드

LAST_UPDATE : 21/10/20
AUTHOR      : SO BYUNG JUN
"""


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import numpy as np
import os
import cv2
import sys
import copy
import pandas as pd

import matplotlib.pyplot as plt



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
from Core.ExcelDataClass    import ExcelData
from Core.CvatXmlClass      import CvatXml


# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from UI.SelectUI.SelectUIClass import *


# SOURCE & DEST PATH
# 해당 OriginXmlDirPath 과 ResultDirPath 값을 변경하고 싶으면, CoreDefine.py 에서 변경하면 됨! ( 경로 변경 통합 )
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
OriginXmlDirPath    = copy.copy(OriginSource_cvatXml_Path)
OriginImgDirPath    = copy.copy(OriginSource_Img_Path)
ResultDirPath       = copy.copy(Result_Dir_Path)
CrushedImgFilePath  = os.path.join(ResultDirPath, CrushedImgFileName)

encodingFormat      = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat      = copy.copy(VALID_IMG_FORMAT)


# CheckValue Define
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
CHECK_IS_IMAGE_CRUSHED  = False
CHECK_IMAGE_SIZE        = True
SHOW_GRAPH              = False
CHECK_SIZE_VALUE        = 23

# FILE & DIR NAME
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
EXCEL_FILE_NAME     = "AnalysisAttribute.xlsx"


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
CLASS_NUM   = 83

COMMON_IDX  = 0
HEAD_IDX    = 1
UPPER_IDX   = 2
LOWER_IDX   = 3
MAX_LABEL   = 4

LOW         = 0
MID_HIGH    = 1
TOTAL       = 2

ALL_SATISFIED = 2

# Setting
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
pd.set_option('display.max_row', 500)


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


# Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class AnalysisAttribute(CvatXml):
    def __init__(self, QApp):
        super().__init__(OriginImgDirPath)
        self.app        = QApp
        self.classNum   = CLASS_NUM

        self.EachElementSumList = [ 0 for _ in range(self.classNum) ]

        # getImgPath() 검색하기 위한 Dict
        self.OriginImgDict = {}
        self.TotalImageCount = 0

        # SliceImage 가 실패한 목록들 출력하기 위한 List
        self.SliceFailList = []

        # 현재 이미지의 속성값을 가지고 오기 위한 변수들
        self.CurBoxList     = []
        self.CurImgName     = ""
        self.CurImgSizeList = []

        self.sendArgsList   = []

        self.ClassData      = ExcelData()
        self.classNameDict  = {}
        self.categoryDict   = {}
        self.categoryMaxCnt = 0
        self.ctgSumList     = []

        self.imgSizeAnalysisList    = []
        self.imgSizeValueList       = []
        self.checkSize = CHECK_SIZE_VALUE

        self.saveElementDataFrame   = None
        self.saveImgSizeDataFrame   = None
        self.saveCategoryDataFrame  = None

        self.initializeAN()


    def initializeAN(self):
        # RunFunction 이름 지정 - 안하면 Error 뜸!
        self.setRunFunctionName('ANALYSYS_ATTRIBUTE')

        # SelectUI 는 다른 initialize 이전에 시행해야 함 : 경로 변수, 판단 변수가 바뀌는 것이기 때문!
        self.selectUi    = SelectUI(self.setInitSettingSelectUI, self.getEditSettingSelectUI)

        # ! Before Initialize
        self.selectUi.show()
        self.app.exec()

        self.initCvatXmlClass()
        self.setimgSizeAnalysisList()

        # Get Origin Image Data as Dict - ImgFileName:RootPath
        # 만약 getOriginImgDataDict 가 제대로 불러와지지 않는다면 바로 프로그램 종료
        if self.getOriginImgDataDict() is False:
            sys.exit(-1)

        self.TotalImageCount = len(self.OriginImgDict)
        self.classNameDict   = self.ClassData.getClassNameDictByClassNum(self.classNum)

        if self.classNameDict is None:
            error_handling('Load ClassName Failed', filename(), lineNum())

        self.categoryDict    = self.ClassData.getClassCategoryDict()
        self.categoryMaxCnt  = max(set(self.categoryDict.values()))
        self.ctgSumList      = [ 0 for _ in range(self.categoryMaxCnt) ]


    def setimgSizeAnalysisList(self):
        self.imgSizeAnalysisList = [ [] for _ in range(MAX_LABEL) ]
        for eachLabelIdx in range(MAX_LABEL):
            # WIDTH     [   [ [LOW], [MID_HIGH], [TOTAL] ], 
            # HEIGHT        [ [LOW], [MID_HIGH], [TOTAL] ],
            # BOTH          [ [LOW], [MID_HIGH], [TOTAL] ] ]  -> 3X3 Array
            self.imgSizeAnalysisList[eachLabelIdx] = [ [ 0, 0, 0 ], [ 0, 0, 0 ], [ 0, 0, 0 ] ]

        self.imgSizeValueList = [ [] for _ in range(MAX_LABEL) ]
        for eachLabelIdx in range(MAX_LABEL):
            self.imgSizeValueList[eachLabelIdx] = [ [], [] ]


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
            - CrushedImgFilePath

            - CHECK_IS_IMAGE_CRUSHED
            - CHECK_IMAGE_SIZE

            - CHECK_SIZE_VALUE
    """
    def setInitSettingSelectUI(self):
        self.sendArgsList = [   ['FD', 'OriginXmlDirPath',      True, f'{OriginXmlDirPath}'],
                                ['FD', 'OriginImgDirPath',      True, f'{OriginImgDirPath}'],
                                ['FD', 'ResultDirPath',         True, f'{ResultDirPath}'],
                                ['FD', 'CrushedImgFilePath',    True, f'{CrushedImgFilePath}'],

                                ['CB', 'CHECK_IS_IMAGE_CRUSHED', False, f'{CHECK_IS_IMAGE_CRUSHED}'],
                                ['CB', 'CHECK_IMAGE_SIZE', False, f'{CHECK_IMAGE_SIZE}'],
                                ['CB', 'SHOW_GRAPH', False, f'{SHOW_GRAPH}'],

                                ['LE',  'CHECK_SIZE_VALUE', False, f'{CHECK_SIZE_VALUE}']
                            ]
        return self.getRunFunctionName(), self.sendArgsList


    def getEditSettingSelectUI(self):
        NAME = 1
        returnDict = self.selectUi.getReturnDict()

        print("\n* Change Path/Define Value By SelectUI")
        print("--------------------------------------------------------------------------------------")
        for Arg in self.sendArgsList:
            if returnDict.get(Arg[NAME]) != None:
                globals()[Arg[NAME]] = returnDict[Arg[NAME]]
                showLog(f'- {Arg[NAME]:40} -> {globals()[Arg[NAME]]}')            
        print()

        self.setChanged_Xml_n_Res_Path(OriginXmlDirPath, ResultDirPath)
        self.checkSize = int(CHECK_SIZE_VALUE)

    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-


    # getImgPath() 검색하기 위한 Dict 만드는 함수
    def getOriginImgDataDict(self):
        # 해당 OriginImgDirPath 존재여부 확인
        if os.path.isdir(OriginImgDirPath) is True:
            NoticeLog(f'Target Source Img Path - {OriginImgDirPath}')
        else:
            ErrorLog(f'`{OriginImgDirPath}` is Not Vaild Img Path', lineNum=lineNum(), errorFileName=filename())
            return False            

        # 돌리면서 유효한 이미지 확장자만 추가하기
        for root, _, files in os.walk(OriginImgDirPath):
            if len(files) > 0:
                for file_name in files:
                    if file_name.split('.')[-1] in validImgFormat:
                        self.OriginImgDict[file_name] = root

        # 유효한 이미지가 있었을 때
        if self.OriginImgDict:
            SuccessLog(f'get Image Data Success - {len(self.OriginImgDict)} Files')
        # 유효한 이미지가 하나도 없었을 때
        else:
            ErrorLog(f'`{OriginImgDirPath}` is Nothing Vaild Image', lineNum=lineNum(), errorFileName=filename())
            return False

        return True


    # 주어진 imageName 이 OriginImageDirPath 내 파일에 있는 이미지인지, 있다면 어떤 경로인지 리턴하는 함수
    def getImgPath(self, imageName):
        if self.OriginImgDict.get(imageName) == None:
            error_handling(f"getImgPath() failed - {imageName} is Not Matched", filename(), lineNum())
            return None

        return os.path.join(self.OriginImgDict[imageName], imageName)


    def createAttListByBoxList(self):
        """
            이 함수가 실행되기 직전, 
            setRunFunctionParam() 을 통해 갱신된 CurBoxList 변수를 이용하여,
            RunFunction 내부 setMakeClassDefaultData() 함수에 인자로 줄
            sendAttList 값을 만드는 함수
            ---------------------------------------------------------------------
            Returns :
                sendAttList :
                    각 인자가 개별 박스의 ['label', AttName, AttText] 인 리스트 (type : list)
            ---------------------------------------------------------------------
        """
        sendAttList = []
        for box in self.CurBoxList:
            for att in box.findall('attribute'):
                sendAttList.append([box.get('label'), att.get('name'), att.text])

        return sendAttList


    def addElementValueByMCD(self, MCD:list):
        # MCD : MakeClassData
        for idx in range(self.classNum):
            self.EachElementSumList[idx] += int(MCD[idx])
            self.ctgSumList[self.categoryDict[idx]-1] += int(MCD[idx])


    def checkSizeValueByEachLabel(self, labelIdx, width, height):
        checkSize = self.checkSize

        if width < checkSize:
            self.imgSizeAnalysisList[labelIdx][WIDTH][LOW]       += 1
            self.imgSizeAnalysisList[labelIdx][WIDTH][TOTAL]     += 1
        else:
            self.imgSizeAnalysisList[labelIdx][WIDTH][MID_HIGH]  += 1
            self.imgSizeAnalysisList[labelIdx][WIDTH][TOTAL]     += 1

        if height < checkSize:
            self.imgSizeAnalysisList[labelIdx][HEIGHT][LOW]      += 1
            self.imgSizeAnalysisList[labelIdx][HEIGHT][TOTAL]    += 1
        else:
            self.imgSizeAnalysisList[labelIdx][HEIGHT][MID_HIGH] += 1
            self.imgSizeAnalysisList[labelIdx][HEIGHT][TOTAL]    += 1

        if width < checkSize and height < checkSize:
            self.imgSizeAnalysisList[labelIdx][ALL_SATISFIED][LOW]      += 1
            self.imgSizeAnalysisList[labelIdx][ALL_SATISFIED][TOTAL]    += 1
        elif width >= checkSize and height >= checkSize:
            self.imgSizeAnalysisList[labelIdx][ALL_SATISFIED][MID_HIGH] += 1
            self.imgSizeAnalysisList[labelIdx][ALL_SATISFIED][TOTAL]    += 1

        self.imgSizeValueList[labelIdx][WIDTH].append(int(width))
        self.imgSizeValueList[labelIdx][HEIGHT].append(int(height))


    def getBoxSize(self, box):
        xTopLeft     = int(float(box.get("xtl")))
        yTopLeft     = int(float(box.get("ytl")))
        xBottomRight = int(float(box.get("xbr")))
        yBottomRight = int(float(box.get("ybr")))

        return [xBottomRight - xTopLeft, yBottomRight - yTopLeft]   


    def checkSizeValueByImgSize(self):
        for box in self.CurBoxList:
            label       = box.get('label')
            sizeList    = self.getBoxSize(box)
            imgWidth    = int(sizeList[WIDTH])
            imgHeight   = int(sizeList[HEIGHT])

            if label == "all":
                self.checkSizeValueByEachLabel(COMMON_IDX, imgWidth, imgHeight)
            elif label == "head":
                self.checkSizeValueByEachLabel(HEAD_IDX, imgWidth, imgHeight)
            elif label == "upper":
                self.checkSizeValueByEachLabel(UPPER_IDX, imgWidth, imgHeight)
            elif label == "lower":
                self.checkSizeValueByEachLabel(LOWER_IDX, imgWidth, imgHeight)


    def AnalysisAttributeEachImage(self):
        if CHECK_IS_IMAGE_CRUSHED is True:
            OneImgPath = self.getImgPath(self.CurImgName)

            # 유효한 이미지 경로 없으면 return False
            if OneImgPath is None:
                return False

            # Type 지정
            img:np.ndarray = imread(OneImgPath)

            # Image Read 실패하면 바로 return False
            if img is None :
                error_handling(f"imread() failed '{OneImgPath}'", filename(), lineNum())
                return False

        # 분석 시작
        attList = self.createAttListByBoxList()
        self.ClassData.setMakeClassDefaultData(attList)

        # 만든 값 불러오기
        MCD = self.ClassData.getMakeClassDefaultData()
        self.addElementValueByMCD(MCD)
        self.checkSizeValueByImgSize()

        return True


    def RunFunction(self):
        res = self.AnalysisAttributeEachImage()
        return res


    def setRunFunctionParam(self):
        """
            CvatXml 의 가상함수를 상속받아 재정의한 함수
            RunFunction 에 들어가기 전 사용할 Param 을 setting 하는 함수
        """
        self.CurBoxList     = self.getCurBoxList()
        self.CurImgName     = self.getCurImgName()
        self.CurImgSizeList = self.getCurImgSize()

    def setAfterRunFunctionParam(self):
        return super().setAfterRunFunctionParam()

    # 가상함수 : RunFunction 의 결과가 fasle 일 때 실행하는 함수
    def AfterRunFunction(self):
        if CHECK_IS_IMAGE_CRUSHED is True:
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
        if CHECK_IS_IMAGE_CRUSHED is True:
            print("[ Crushed Image List ]")
            if self.SliceFailList:
                for each in self.SliceFailList:
                    print(f'- {each}')

                if os.path.isdir(ResultDirPath) is False:
                    os.makedirs(ResultDirPath, exist_ok=True)
                    NoticeLog(f'{ResultDirPath} is Not Exists, Create Done')

                with open(CrushedImgFilePath, 'w') as f:
                    for line in self.SliceFailList:
                        f.write(f"{line}\n")

                SuccessLog(f'CrushImgList Save Done - {CrushedImgFilePath}')
            else:
                print("- Crushed Image Not Detected! :D")

        self.AnalysisElementSum()
        self.AnalysysCategory()
        self.AnalysisImgSize()

        self.saveToExcel()


    def AnalysisElementSum(self):
        idxList         = [ i for i in range(self.classNum)]
        classNameList   = []
        for idx in range(self.classNum):
            classNameList.append(self.classNameDict[idx])

        self.saveElementDataFrame = pd.DataFrame(self.EachElementSumList, index=[idxList, classNameList], columns=['Sum'])
        print(self.saveElementDataFrame)
        print()

    def AnalysysCategory(self):
        idxList         = [ i+1 for i in range(self.categoryMaxCnt)]
        CategoryNameDict = self.ClassData.getCategoryNameDict()
        CategoryNameList = []
        for idx in range(self.categoryMaxCnt):
            CategoryNameList.append(CategoryNameDict[idx+1])

        self.saveCategoryDataFrame = pd.DataFrame(self.ctgSumList, index=[idxList, CategoryNameList], columns=['Sum'])
        print(self.saveCategoryDataFrame)
        print()


    def AnalysisImgSize(self):
        DataFrameList = []
        for eachLabelIdx in range(MAX_LABEL):
            DataFrameList += self.imgSizeAnalysisList[eachLabelIdx]

        self.saveImgSizeDataFrame = pd.DataFrame(   DataFrameList,
                                                    index= [[   'COMMON',   'COMMON',   'COMMON',
                                                                'HEAD',     'HEAD',     'HEAD',
                                                                'UPPER',    'UPPER',    'UPPER',
                                                                'LOWER',    'LOWER',    'LOWER'],

                                                            [   'WIDTH',    'HEIGHT',   'ALL_SATISFIED',
                                                                'WIDTH',    'HEIGHT',   'ALL_SATISFIED',
                                                                'WIDTH',    'HEIGHT',   'ALL_SATISFIED',
                                                                'WIDTH',    'HEIGHT',   'ALL_SATISFIED',
                                                            ]],
                                                    columns=['LOW', 'MID-HIGH', 'TOTAL'])
        print(self.saveImgSizeDataFrame)
        print()

        if SHOW_GRAPH is True:
            self.showGraphOnImgSizeList()


    def showGraphOnImgSizeList(self):
        pltCount = 221
        Title = ['COMMON', 'HEAD', 'UPPER', 'LOWER']        
        for eachLabelIdx in range(MAX_LABEL):
            body = pd.DataFrame({   'width':self.imgSizeValueList[eachLabelIdx][WIDTH], 
                                    'height':self.imgSizeValueList[eachLabelIdx][HEIGHT]})

            plt.subplot(pltCount)
            plt.title(Title[eachLabelIdx])
            plt.scatter( body['width'], body['height'], label = "data", s=5)

            plt.axhline(self.checkSize, 0, 1, color='red')
            plt.axvline(self.checkSize, 0, 1, color='red')

            plt.legend(loc = "best")
            plt.xlabel('weight')
            plt.ylabel('height')
            print()

            pltCount += 1

        plt.show()


    def saveToExcel(self):
        savePath = os.path.join(ResultDirPath, EXCEL_FILE_NAME)

        with pd.ExcelWriter(savePath) as writer:
            self.saveElementDataFrame.to_excel(writer, sheet_name='ElementSum')
            self.saveCategoryDataFrame.to_excel(writer, sheet_name='CategorySum')
            self.saveImgSizeDataFrame.to_excel(writer, sheet_name='ImageSizeFilter')

        SuccessLog(f'Analysis Data Save to Excel File -> {savePath}')


    def run(self):
        super().run()
        os.startfile(ResultDirPath)
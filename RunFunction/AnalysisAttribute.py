"""
cvatXml 파일과 그에 해당하는 img 원본 경로를 받아서 분석하는 코드

LAST_UPDATE : 21/11/09
AUTHOR      : SHY
"""


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import os
import cv2
import sys
import copy
import shutil


# INSTALLED PACKAGE IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import numpy                    as np
import pandas                   as pd
import matplotlib.pyplot        as plt


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
from Core.ExcelDataClass        import ExcelData
from Core.CvatXmlClass          import CvatXml
from Core.SingletonClass        import Singleton


# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from UI.SelectUI.SelectUIClass  import *


# SOURCE & DEST PATH
# 해당 OriginXmlDirPath 과 ResultDirPath 값을 변경하고 싶으면, CoreDefine.py 에서 변경하면 됨! ( 경로 변경 통합 )
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
OriginXmlDirPath    = copy.copy(OriginSource_cvatXml_Path)
OriginImgDirPath    = copy.copy(OriginSource_Img_Path)
ResultDirPath       = copy.copy(Result_Dir_Path)
CrushedImgFilePath  = os.path.join(ResultDirPath, CrushedImgFileName)
CompareExcelPath    = r"C:\PythonHN\Data\Res1017\AnalysisAttribute.xlsx"

encodingFormat      = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat      = copy.copy(VALID_IMG_FORMAT)


# CheckValue Define
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
CHECK_IS_IMAGE_CRUSHED  = False
CHECK_IMAGE_SIZE        = True
SHOW_GRAPH              = True
SIZE_FILTERING          = False
CHECK_SIZE_VALUE        = 23
COMPARE_WITH_EXCEL      = False


# FILE & DIR NAME
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
EXCEL_FILE_NAME         = "AnalysisAttribute.xlsx"


# SIZE_FILTERING DICT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
SIZE_FILTERING_DICT     = copy.copy(CORE_SIZE_FILTER_DICT)


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
CLASS_NUM       = 83

COMMON_IDX      = 0
HEAD_IDX        = 1
UPPER_IDX       = 2
LOWER_IDX       = 3
MAX_LABEL       = 4

LOW             = 0
MID_HIGH        = 1
TOTAL           = 2

ALL_SATISFIED   = 2


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
class AnalysisAttribute(Singleton, CvatXml):
    def __init__(self, QApp):
        super().__init__(OriginImgDirPath)
        self.app                    = QApp
        self.classNum               = CLASS_NUM

        self.EachElementSumList     = [ 0 for _ in range(self.classNum) ]

        # getImgPath() 검색하기 위한 Dict
        self.OriginImgDict          = {}
        self.TotalImageCount        = 0

        # SliceImage 가 실패한 목록들 출력하기 위한 List
        self.SliceFailList          = []

        # 현재 이미지의 속성값을 가지고 오기 위한 변수들
        self.CurBoxList             = []
        self.CurImgName             = ""
        self.CurImgSizeList         = []

        self.sendArgsList           = []

        self.ClassData              = None
        self.classNameList          = []
        self.categoryDict           = {}
        self.categoryMaxCnt         = 0
        self.ctgSumList             = []

        self.imgSizeAnalysisList    = []
        self.imgSizeValueList       = []
        self.checkSize              = CHECK_SIZE_VALUE

        self.imageWidthList         = []
        self.imageHeightList        = []

        self.saveElementDataFrame   = None
        self.saveImgSizeDataFrame   = None
        self.saveCategoryDataFrame  = None

        self.SizeFilterLogList      = []
        self.compareExcelDataList   = []
        self.compareExcelCopyPath   = ""

        self.initializeAN()


    def initializeAN(self):
        # RunFunction 이름 지정 - 안하면 Error 뜸!
        self.setRunFunctionName('ANALYSYS_ATTRIBUTE')

        # SelectUI 는 다른 initialize 이전에 시행해야 함 : 경로 변수, 판단 변수가 바뀌는 것이기 때문!
        self.selectUi = SelectUI(self.setInitSettingSelectUI, self.getEditSettingSelectUI)

        # ! Before Initialize
        self.selectUi.show()
        self.app.exec()

        if self.selectUi.isQuitProgram():
            return

        self.initAfterSetUI()
        self.setMode()


    def initAfterSetUI(self):
        # UI에서 닫기버튼을 안 눌렀을 때만, ExcelData load 시작
        self.ClassData      = ExcelData()
        self.classNameList  = self.ClassData.getClassNameListByClassNum(self.classNum)

        if self.classNameList is None:
            error_handling('Load ClassName Failed', filename(), lineNum())

        self.categoryDict    = self.ClassData.getClassCategoryDict()
        self.categoryMaxCnt  = max(set(self.categoryDict.values()))
        self.ctgSumList      = [ 0 for _ in range(self.categoryMaxCnt) ]

        self.initCvatXmlClass()
        self.setimgSizeAnalysisList()


    def setMode(self):
        if CHECK_IS_IMAGE_CRUSHED is True:
            ModeLog('CHECK_IS_IMAGE_CRUSHED ON')
            # Get Origin Image Data as Dict - ImgFileName:RootPath
            # 만약 getOriginImgDataDict 가 제대로 불러와지지 않는다면 바로 프로그램 종료
            if self.getOriginImgDataDict() is False:
                sys.exit(-1)

            self.TotalImageCount = len(self.OriginImgDict)

        if COMPARE_WITH_EXCEL is True:
            ModeLog('COMPARE_WITH_EXCEL ON')
            CheckExistFile(CompareExcelPath)
            self.loadCompareExcelData()

        if SIZE_FILTERING is True:
            ModeLog('SIZE_FILTERING ON')
            self.condClass.addCondition(['SizeFilter', self.SizeFilter, self.getArgs_SizeFilter])


    def setimgSizeAnalysisList(self):
        # 4X3X3 Array
        self.imgSizeAnalysisList = [ [] for _ in range(MAX_LABEL) ]
        for eachLabelIdx in range(MAX_LABEL):
            # WIDTH     [   [ [LOW], [MID_HIGH], [TOTAL] ], 
            # HEIGHT        [ [LOW], [MID_HIGH], [TOTAL] ],
            # BOTH          [ [LOW], [MID_HIGH], [TOTAL] ] ]  -> 3X3 Array
            self.imgSizeAnalysisList[eachLabelIdx] = [ [ 0, 0, 0 ], [ 0, 0, 0 ], [ 0, 0, 0 ] ]

        # 4X2 Array
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
        self.SyncAllValue()
        self.sendArgsList = [   ['FD', 'OriginXmlDirPath',          True,   f'{OriginXmlDirPath}'],
                                ['FD', 'OriginImgDirPath',          True,   f'{OriginImgDirPath}'],
                                ['FD', 'ResultDirPath',             True,   f'{ResultDirPath}'],
                                ['FD', 'HLINE_0',                   False,  'None'],
                                ['FD', 'CrushedImgFilePath',        False,  f'{CrushedImgFilePath}'],
                                ['FD', 'HLINE_1',                   False,  'None'],
                                ['FD', 'CompareExcelPath',          False,  f'{CompareExcelPath}'],

                                ['CB', 'CHECK_IS_IMAGE_CRUSHED',    False,  f'{CHECK_IS_IMAGE_CRUSHED}'],
                                ['CB', 'CHECK_IMAGE_SIZE',          False,  f'{CHECK_IMAGE_SIZE}'],
                                ['CB', 'SHOW_GRAPH',                False,  f'{SHOW_GRAPH}'],
                                ['CB', 'SIZE_FILTERING',            False,  f'{SIZE_FILTERING}'],
                                ['CB', 'HLINE_2',                   False,  'None'],
                                ['CB', 'COMPARE_WITH_EXCEL',        False,  f'{COMPARE_WITH_EXCEL}'],

                                ['LE', 'CHECK_SIZE_VALUE',          False,  f'{CHECK_SIZE_VALUE}'],
                                ['UI', 'SIZE_FILTERING_DICT',       False,  SIZE_FILTERING_DICT]
                            ]
        return self.getRunFunctionName(), self.sendArgsList


    def getEditSettingSelectUI(self):
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

        showLog("\n* Change Path/Define Value By SelectUI")
        showLog("--------------------------------------------------------------------------------------")
        for Arg in self.sendArgsList:
            eachTarget = Arg[NAME]
            if returnDict.get(eachTarget) != None:
                # 해당 변수명에 SelectUI 에서 갱신된 값 집어넣기
                globals()[eachTarget] = returnDict[eachTarget]

                if eachTarget == "SIZE_FILTERING_DICT":
                    showLog(f'- {eachTarget:40} -> {summaryFilterDict(globals()[eachTarget])}')
                else:
                    showLog(f'- {eachTarget:40} -> {globals()[eachTarget]}')
        showLog("--------------------------------------------------------------------------------------\n")

        self.SyncAllValue()
        self.setChanged_Xml_n_Res_Path(OriginXmlDirPath, ResultDirPath)
        self.checkSize = int(CHECK_SIZE_VALUE)
        setResultDir(ResultDirPath)

    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-


    def SyncAllValue(self):
        self.SyncEachValue('OriginSource_cvatXml_Path', 'OriginXmlDirPath')
        self.SyncEachValue('OriginSource_Img_Path',     'OriginImgDirPath')
        self.SyncEachValue('Result_Dir_Path',           'ResultDirPath')
        self.SyncEachValue('CORE_SIZE_FILTER_DICT',     'SIZE_FILTERING_DICT')

    def SyncEachValue(self, CoreName, LinkName, SENDER_DEPTH=3):
        # set 하기 전에 CoreDefine.py의 값을 get
        if callername(SENDER_DEPTH) == 'setInitSettingSelectUI':
            globals()[LinkName] = getCoreValue(CoreName)

        elif callername(SENDER_DEPTH) == 'getEditSettingSelectUI':
            setCoreValue(CoreName, globals()[LinkName])


    # Add CheckCond List
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

    # ConditionName
    # -------------------------------------------------------------------------------------
    """
    [ Add Condition Name ]
        - SizeFilter
    """

    # ConditionFunctions
    # -------------------------------------------------------------------------------------
    # OHN
    def SizeFilter(self, getArgsList):
        """
            ! Free Customize Function
            추가적인 조건을 기입해 필터링 하는 ConditionCheck
        """
        BoxValue    = getArgsList[0]    # 현재 이미지의 BoxValue 들의 리스트
        ImgSizeList = getArgsList[1]    # 현재 이미지의 [너비, 높이] 리스트
        condDict    = getArgsList[2]
        BoxDict     = {}
        BoxNameList = ['head', 'upper', 'lower']
        
        # 너비 쓰려면 : int(ImgSizeList[WIDTH])
        # 높이 쓰려면 : int(ImgSizeList[HEIGHT])

        def getBoxSizebyLabel(box):
            xTopLeft     = int(float(box.get("xtl")))
            yTopLeft     = int(float(box.get("ytl")))
            xBottomRight = int(float(box.get("xbr")))
            yBottomRight = int(float(box.get("ybr")))

            return [xBottomRight - xTopLeft, yBottomRight - yTopLeft]

        def checkSizeByLabel(labelName:str):
            # 일단 값 있는지부터 체크
            if BoxDict.get(f'{labelName}') == None:
                return COND_FAIL
            
            boxSizeList = getBoxSizebyLabel(BoxDict[f'{labelName}'])
            if condDict[f'{labelName}']['CheckSize'] is True:
                boxSize = boxSizeList[WIDTH] * boxSizeList[HEIGHT]
                if boxSize >= condDict[f'{labelName}']['Size']:
                    return COND_PASS
                else:
                    return COND_FAIL
            else:
                if  ( boxSizeList[WIDTH]  >= condDict[f'{labelName}']['Width'] ) and \
                    ( boxSizeList[HEIGHT] >= condDict[f'{labelName}']['Height'] ):
                    return COND_PASS
                else:
                    return COND_FAIL            

        if condDict['common']['isCheck'] is True:
            # Image 넓이 가지고 체크
            if condDict['common']['CheckSize'] is True:
                imgSize = ImgSizeList[WIDTH] * ImgSizeList[HEIGHT]
                if imgSize >= condDict['common']['Size']:
                    return COND_PASS
                else:
                    return COND_FAIL
            # Image 너비, 높이 가지고 체크
            else:
                if  ( ImgSizeList[WIDTH]  >= condDict['common']['Width'] ) and \
                    ( ImgSizeList[HEIGHT] >= condDict['common']['Height'] ):
                    return COND_PASS
                else:
                    return COND_FAIL

        # 각 box 값들 미리 정리
        for box in BoxValue:
            BoxDict[box.get('label')] = box

        # 각 Label에 대해서 체크하는 부분
        for eachName in BoxNameList:
            if condDict[f'{eachName}']['isCheck'] is True:
                return checkSizeByLabel(eachName)

        return COND_FAIL


    # getArgs_ConditionFunctions
    # -------------------------------------------------------------------------------------
    def getArgs_SizeFilter(self):
        return [ self.getCurBoxList(), self.getCurImgSize(), SIZE_FILTERING_DICT ]


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
                    _, ext = os.path.splitext(file_name)
                    if ext in validImgFormat:
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
            self.EachElementSumList[idx]                += int(MCD[idx])
            self.ctgSumList[self.categoryDict[idx]-1]   += int(MCD[idx])


    def checkSizeValueByEachLabel(self, labelIdx, width, height):
        checkSize = self.checkSize

        if width < checkSize:
            self.imgSizeAnalysisList[labelIdx][WIDTH][LOW]              += 1
            self.imgSizeAnalysisList[labelIdx][WIDTH][TOTAL]            += 1
        else:
            self.imgSizeAnalysisList[labelIdx][WIDTH][MID_HIGH]         += 1
            self.imgSizeAnalysisList[labelIdx][WIDTH][TOTAL]            += 1

        if height < checkSize:
            self.imgSizeAnalysisList[labelIdx][HEIGHT][LOW]             += 1
            self.imgSizeAnalysisList[labelIdx][HEIGHT][TOTAL]           += 1
        else:
            self.imgSizeAnalysisList[labelIdx][HEIGHT][MID_HIGH]        += 1
            self.imgSizeAnalysisList[labelIdx][HEIGHT][TOTAL]           += 1

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
                self.checkSizeValueByEachLabel(COMMON_IDX,  imgWidth,   imgHeight)
            elif label == "head":
                self.checkSizeValueByEachLabel(HEAD_IDX,    imgWidth,   imgHeight)
            elif label == "upper":
                self.checkSizeValueByEachLabel(UPPER_IDX,   imgWidth,   imgHeight)
            elif label == "lower":
                self.checkSizeValueByEachLabel(LOWER_IDX,   imgWidth,   imgHeight)


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

        self.imageWidthList.append(self.CurImgSizeList[WIDTH])
        self.imageHeightList.append(self.CurImgSizeList[HEIGHT])

        return True


    def RunFunction(self):
        return self.AnalysisAttributeEachImage()


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
            showLog("[ Crushed Image List ]")
            if self.SliceFailList:
                showListLog(self.SliceFailList)
                writeListToFile(CrushedImgFilePath, self.SliceFailList, encodingFormat)
            else:
                showLog("- Crushed Image Not Detected! :D")

        self.AnalysisFail()
        self.AnalysisElementSum()
        self.AnalysisCategory()
        self.AnalysisImgSize()
        self.averageImageSize()

        self.saveToExcel()


    def averageImageSize(self):
        widthArray  = np.array(self.imageWidthList)
        heightArray = np.array(self.imageHeightList)

        widthAvg    = np.mean(widthArray)
        heightAvg   = np.mean(heightArray)
        AreaAvg     = np.mean(np.multiply(widthAvg, heightArray))

        print()
        showLog('# [ SIZE ANALYSIS ]')
        if SIZE_FILTERING:
            showLog('--------------------------------------------------------------------------------------')
            showLog(f'- Condition      : {summaryFilterDict(SIZE_FILTERING_DICT)}')
        showLog('--------------------------------------------------------------------------------------')
        showLog(f'- Avgarge Width  : {round(widthAvg,2)}')
        showLog(f'- Avgarge Height : {round(heightAvg,2)}')
        showLog(f'- Avgarge Szie   : {round(AreaAvg,2)}')
        showLog('--------------------------------------------------------------------------------------')
        print()        


    def copyTempCompareExcel(self, OriginExcelFilePath):
        file, ext = os.path.splitext(OriginExcelFilePath)
        TempFilePath = f'{file}_Cmp_Temp{ext}'
        shutil.copy(OriginExcelFilePath, TempFilePath)

        return TempFilePath


    def getExcelDataOnlySum(self, excelPath):
        excelData   = pd.read_excel(excelPath, sheet_name='ElementSum')
        sumList     = excelData['Sum'].tolist()

        return sumList


    def loadCompareExcelData(self):
        self.compareExcelCopyPath = self.copyTempCompareExcel(CompareExcelPath)
        self.compareExcelDataList = self.getExcelDataOnlySum(self.compareExcelCopyPath)
        SuccessLog('Load Compare Excel Data Done')


    def showGraphAnalysisFailedList(self):
        _, SuccessImageCount    = self.getOperateImageCount()
        FailDict                = self.condClass.getTotalFailLog()
        Labels                  = []
        Frequency               = []

        Labels.append(f'Total Success [{SuccessImageCount}]')
        Frequency.append(SuccessImageCount)

        for key, value in FailDict.items():
            Labels.append(f'{key.split("Check")[-1]} [{value}]')
            Frequency.append(value)

        ## 데이터 라벨, 빈도수, 색상을 빈도수를 기준으로 정렬해야한다.
        labels_frequency = zip(Labels, Frequency) 
        labels_frequency = sorted(labels_frequency, key=lambda x: x[1],reverse=True)
        
        sorted_labels    = [x[0] for x in labels_frequency] ## 정렬된 라벨
        sorted_frequency = [x[1] for x in labels_frequency] ## 정렬된 빈도수

        ## 캔버스 생성
        fig     = plt.figure(figsize=(8,8)) 
        fig.set_facecolor('white')              ## 캔버스 배경색을 하얀색으로 설정
        ax      = fig.add_subplot()             ## 프레임 생성
        
        pie     = ax.pie(   sorted_frequency,   ## 파이차트 출력
                            startangle=90,      ## 시작점을 90도(degree)로 지정
                            counterclock=False, ## 시계방향으로 그려짐
                        )
        
        total           = np.sum(Frequency)     ## 빈도수 합
        threshold       = 5
        sum_pct         = 0     ## 퍼센티지
        count_less_5pct = 0     ## 5%보다 작은 라벨의 개수
        spacing         = 0.1

        for i, _ in enumerate(sorted_labels):
            ang1, ang2  = ax.patches[i].theta1, ax.patches[i].theta2 ## 파이의 시작 각도와 끝 각도
            center, r   = ax.patches[i].center, ax.patches[i].r ## 파이의 중심 좌표
            
            ## 비율 상한선보다 작은 것들은 계단형태로 만든다.
            if sorted_frequency[i]/total*100 < threshold:
                x = (r/2+spacing*count_less_5pct)*np.cos(np.pi/180*((ang1+ang2)/2)) + center[0] ## 텍스트 x좌표
                y = (r/2+spacing*count_less_5pct)*np.sin(np.pi/180*((ang1+ang2)/2)) + center[1] ## 텍스트 y좌표
                count_less_5pct += 1
            else:
                x = (r/2)*np.cos(np.pi/180*((ang1+ang2)/2)) + center[0] ## 텍스트 x좌표
                y = (r/2)*np.sin(np.pi/180*((ang1+ang2)/2)) + center[1] ## 텍스트 y좌표
            
            ## 퍼센티지 출력
            sum_pct += float(f'{sorted_frequency[i]/total*100:.2f}')
            ax.text(x,y,f'{sorted_frequency[i]/total*100:.2f}%',ha='center',va='center',fontsize=12)
        
        plt.legend(pie[0], sorted_labels) ## 범례
        plt.title('Error Check Pie Chart')
        plt.show()


    def AnalysisFail(self):
        if SHOW_GRAPH is True:
            self.showGraphAnalysisFailedList()


    def AnalysisElementSum(self):
        idxList         = [ i for i in range(self.classNum) ]
        classNameList   = self.classNameList

        self.saveElementDataFrame = pd.DataFrame(self.EachElementSumList, index=[idxList, classNameList], columns=['Sum'])
        showLog('# [ ElementSum Analysis ]')
        showLog('--------------------------------------------------------------------------------------')
        print(self.saveElementDataFrame)
        showLog('--------------------------------------------------------------------------------------\n')


    def AnalysisCategory(self):
        idxList          = [ i+1 for i in range(self.categoryMaxCnt) ]
        CategoryNameDict = self.ClassData.getCategoryNameDict()
        CategoryNameList = [ CategoryNameDict[idx+1] for idx in range(self.categoryMaxCnt) ]

        self.saveCategoryDataFrame = pd.DataFrame(self.ctgSumList, index=[idxList, CategoryNameList], columns=['Sum'])
        showLog('# [ CategorySum Analysis ]')
        showLog('--------------------------------------------------------------------------------------')
        print(self.saveCategoryDataFrame)
        showLog('--------------------------------------------------------------------------------------\n')

        if SHOW_GRAPH is True:
            self.showGraphByElementSum() 


    def showGraphByElementSum(self):
        SLICE_IDX       = 45
        classNameList   = self.classNameList

        x               = classNameList
        y               = self.EachElementSumList

        bar_width       = 0.35
        alpha           = 0.5

        upper_idx       = np.arange(len(x[:SLICE_IDX]))
        under_idx       = np.arange(len(x[SLICE_IDX:]))

        # 위쪽 그래프 -----
        plt.subplot(211)
        if SIZE_FILTERING is True:
            plt.title(summaryFilterDict(SIZE_FILTERING_DICT))

        plt.bar(        upper_idx,         # 각 element x 위치값
                        y[:SLICE_IDX],     # 각 element y 위치값 겸 실제 count 값
                        bar_width,         # 막대 너비
                        color='b',         # 막대 색깔
                        alpha=alpha,
                        label='Current' )

        # 각 막대 위에 수치값 표기하는 부분
        for i in upper_idx:
            plt.text(   i, y[i], y[i],                 # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
                        fontsize = 9, 
                        color='blue',
                        horizontalalignment='center',  # horizontalalignment (left, center, right)
                        verticalalignment='bottom' )   # verticalalignment (top, center, bottom)

        if COMPARE_WITH_EXCEL is True:
            plt.bar(    upper_idx + bar_width, 
                        self.compareExcelDataList[:SLICE_IDX], 
                        bar_width, 
                        color='r', 
                        alpha=alpha, 
                        label='Compare' )

            for i in upper_idx:
                plt.text(i + bar_width, 
                        self.compareExcelDataList[i], 
                        self.compareExcelDataList[i],
                        fontsize = 9,
                        color='red',
                        horizontalalignment='center',
                        verticalalignment='bottom')

        plt.xticks(upper_idx, x[:SLICE_IDX], rotation=45, ha='right')
        plt.legend()

        # 아래쪽 그래프 -----
        plt.subplot(212)

        plt.bar(        under_idx, 
                        y[SLICE_IDX:], 
                        bar_width, 
                        color='b', 
                        alpha=alpha )

        for i in under_idx:
            plt.text(   under_idx[i], y[SLICE_IDX+i], y[SLICE_IDX+i],
                        fontsize = 9, 
                        color='blue',
                        horizontalalignment='center',  
                        verticalalignment='bottom' )

        if COMPARE_WITH_EXCEL is True:
            plt.bar(    under_idx + bar_width, 
                        self.compareExcelDataList[SLICE_IDX:], 
                        bar_width, 
                        color='r', 
                        alpha=alpha )

            for i in under_idx:
                plt.text(i+ bar_width, 
                        self.compareExcelDataList[i+SLICE_IDX], 
                        self.compareExcelDataList[i+SLICE_IDX],
                        fontsize = 9,
                        color='red',
                        horizontalalignment='center',
                        verticalalignment='bottom')                

        plt.xticks(under_idx, x[SLICE_IDX:], rotation=45, ha='right')
        plt.show()


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
                                                    columns=[
                                                            [ f'CHECK_VALUE : {self.checkSize:2}' for _ in range(3) ],
                                                            ['LOW', 'MID-HIGH', 'TOTAL'],
                                                            ])
        showLog('# [ ImgSize Devide Analysis ]')
        showLog('--------------------------------------------------------------------------------------')
        print(self.saveImgSizeDataFrame)
        showLog('--------------------------------------------------------------------------------------\n')

        if SHOW_GRAPH is True:
            self.showGraphOnImgSizeList()


    def showGraphOnImgSizeList(self):
        pltCount    = 221
        Title       = ['COMMON', 'HEAD', 'UPPER', 'LOWER']        
        for eachLabelIdx in range(MAX_LABEL):
            body = pd.DataFrame({   'width':self.imgSizeValueList[eachLabelIdx][WIDTH], 
                                    'height':self.imgSizeValueList[eachLabelIdx][HEIGHT]})

            plt.subplot(pltCount)
            plt.title(Title[eachLabelIdx])
            plt.scatter( body['width'], body['height'], label = "data", s=5)

            plt.axhline(self.checkSize, 0, 1, color='red')
            plt.axvline(self.checkSize, 0, 1, color='red')

            plt.legend(loc = "best")
            plt.xlabel('width')
            plt.ylabel('height')

            pltCount += 1

        plt.show()


    def saveToExcel(self):
        savePath = os.path.join(ResultDirPath, EXCEL_FILE_NAME)

        with pd.ExcelWriter(savePath) as writer:
            self.saveElementDataFrame.to_excel(writer,  sheet_name='ElementSum')
            self.saveCategoryDataFrame.to_excel(writer, sheet_name='CategorySum')
            self.saveImgSizeDataFrame.to_excel(writer,  sheet_name='ImageSizeDevide')

        SuccessLog(f'Analysis Data Save to Excel File >> {savePath}')


    def run(self):
        if self.selectUi.isQuitProgram():
            NoticeLog(f'{self.__class__.__name__} Program EXIT\n')
        else:
            super().run()
            os.startfile(ResultDirPath)


if __name__ == "__main__":
    App         = QApplication(sys.argv)
    RunProgram  = AnalysisAttribute(App)
    RunProgram.run()
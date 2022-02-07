"""
This python file creates annotation txt output of class 83/66/39 
using classData.xlsx file and xml / img file of the given path.

Classes :
    MakeClassSource : 
        INFO : 
            OriginXmlDirPath 경로의 Xml 파일들과, OriginImgDirPath 경로의 Img 파일들을 참조하여
            83 / Zip Class 의 Annotation Text / Annotation_img Text 생성하는 클래스

        METHODS :
            - run()

LAST_UPDATE : 2022/02/07
AUTHOR      : SHY
"""


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import os
import sys


# IMPORT INSTALLED
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
AbbreviatedImgPath  = copy.copy(Abbreviated_Img_Path)
CheckRealExistPath  = copy.copy(RealExistCheck_Path)
CrushedImgFilePath  = os.path.join(ResultDirPath, CrushedImgFileName)

encodingFormat      = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat      = copy.copy(VALID_IMG_FORMAT)

ZIPPED_CLASS_NUM    = getZipClassNum()
BEFORE_ZIPPED_NUM   = ZIPPED_CLASS_NUM


# FILE & DIR NAME
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
ANNOTATION_ORG_TXT   = "Annotation_83_Class.txt"
ANNOTATION_ZIP_TXT   = f"Annotation_{ZIPPED_CLASS_NUM}_Class.txt"

IMAGE_LIST_ORG_TXT   = "83_Class_ImgList.txt"
IMAGE_LIST_ZIP_TXT   = f"{ZIPPED_CLASS_NUM}_Class_ImgList.txt"

CHECK_EXTRACT_TXT   = "SizeFilterList.txt"
SIZE_ANALYSIS_TXT   = "ImageSize_Analysis_Source.txt"


# DEFINE
# True 체크한 값만 MakeClass 작동
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
MAKE_ZIPPED_CLASS   = True
MAKE_ORIGIN_CLASS   = True
SIZE_FILTERING      = False

CHECK_CRUSH_IMAGE   = False
CHECK_REAL_EXIST    = False
ANALYSIS_IMAGE_SIZE = True

# 원본 이미지를 축약시킨 폴더 기준으로 작업할 때 :
# 해당 cvat 이미지가 원본 이미지에 실제로 있는지 따져야함
ORIGIN_IMG_FILES_ABBREVIATED = False


# SIZE_FILTERING DICT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
SIZE_FILTERING_DICT = copy.copy(CORE_SIZE_FILTER_DICT)


# MakeClassSource Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class MakeClassSource(Singleton, CvatXml):
    """
        OriginXmlDirPath 경로의 Xml 파일들과, OriginImgDirPath 경로의 Img 파일들을 참조하여
        83 / Zipped Class 의 Annotation Text / Annotation_img Text 생성하는 클래스

        Attributes:
            MakeClassFailList    : MakeClass 가 실패한 목록들 출력하기 위한 List (type : list)
            CrushImgFileNameList : 손상된 이미지들의 imageName 리스트 (type : list)

            Result_N_ClassList : 
                makeClass[N] 을 하고 나서 annotation text ( ex) 100010001001... ) 
                형태로 변환된 결과물들의 리스트 (type : list)

            Result_Origin_ImageNameList :
                makeClass[83] 을 하고 나서 나온 imageName 들의 리스트 (type : list)

            ResultDeleteUnknown_Zip_List :
                makeClass[Zip] 를 하면서, Unknown 값이 존재하는 행들이 삭제되고 남은
                imageName 들의 리스트 (type : list)

            Deleted_Zip_Count :
                makeClass[Zip] 를 하면서, Unknown 값이 존재하는 행들이 삭제된 Count (type : int)
            
            ClassData : ExcelData 클래스 (type : class)

            CurBoxList : CvatXml.setCurBoxList() 를 통해 갱신되는 현재 이미지의 box 값들 (type : list)
            CurImgName : CvatXml.setCurImgName() 을 통해 갱신되는 현재 이미지의 이름 (type : str)

            app : SelectUI 를 실행시키기 위해 main 에서 QApplication 상속받은 변수

        Methods:
            - initialize()
            - createAttListByBoxList()
            - listToString(fromList)
            - saveMakeClassFile(SubPath, SaveList)
            - saveMakeClassFiles()
            - run()

        CheckCondition Methods:
            - CheckCrushImg(imgName)
            - getArgs_CheckCrushImg()
        
        Abastract Methods:
            - RunFunction()
            - FinishFunction()
            - setRunFunctionParam()
            - setFinishFunctionParam()
    """
    def __init__(self, QApp):
        """
            class 내부 변수 할당 및 ExcelData 클래스 생성
        """
        super().__init__(OriginXmlDirPath)
        self.app                            = QApp

        self.MakeClassFailList              = []
        self.CrushImgFileNameList           = []

        self.Result_Origin_ClassList        = []
        self.Result_Zip_ClassList           = []

        self.Result_Origin_ImageNameList    = []
        self.ResultDeleteUnknown_Zip_List   = []

        self.Deleted_Zip_Count              = 0

        self.imgSizeValueList               = []
        self.imgSizeSaveList                = []

        self.ClassData                      = None

        self.CurBoxList                     = []
        self.CurImgName                     = ""
        self.CurImgSizeList                 = []

        self.AbbreviatedImgDict             = {}
        self.CheckRealExistDict             = {}

        # UI 연동용 인자 리스트
        self.sendArgsList                   = []

        self.setClassifyClass()
        self.initializeMC()


    def setClassifyClass(self):
        global ZIPPED_CLASS_NUM, ANNOTATION_ZIP_TXT, IMAGE_LIST_ZIP_TXT, BEFORE_ZIPPED_NUM
        ZIPPED_CLASS_NUM    = getZipClassNum()
        ANNOTATION_ZIP_TXT  = ANNOTATION_ZIP_TXT.replace(str(BEFORE_ZIPPED_NUM), str(ZIPPED_CLASS_NUM))
        IMAGE_LIST_ZIP_TXT  = IMAGE_LIST_ZIP_TXT.replace(str(BEFORE_ZIPPED_NUM), str(ZIPPED_CLASS_NUM))
        BEFORE_ZIPPED_NUM   = ZIPPED_CLASS_NUM


    def initializeMC(self):
        """
            SliceImage 실행 결과 저장된 CrushImageList.txt 를 불러오기 시도하고,
            그 결과 현재 원본 이미지 파일들에 Crushed Image 가 있다면
            새로운 ConditionCheck 를 등록 및
            RunFuntion 의 이름을 set 하는 함수
        """
        # RunFunction 이름 지정 - 안하면 Error 뜸!
        self.setRunFunctionName(f'MAKE_CLASS_{ZIPPED_CLASS_NUM}')

        # SelectUI 는 다른 initialize 이전에 시행해야 함 : 경로 변수, 판단 변수가 바뀌는 것이기 때문!
        self.selectUi    = SelectUI(self.setInitSettingSelectUI, self.getEditSettingSelectUI)

        # ! Before Initialize
        self.selectUi.show()
        self.app.exec()

        if self.selectUi.isQuitProgram():
            return

        self.ClassData = ExcelData()

        # UI 를 통해 경로 설정이 완료되면, CvatXmlClass 본격 init 실행
        self.initCvatXmlClass()

        # Define 값 기준 MODE 설정
        self.setMode()


    def setMode(self):
        """
            DEFINE 들을 참고해 모드 설정하는 함수
            ---------------------------------------------------------------------
            MODE:
                - CRUSH_IMG_FILTER
                - ORIGIN_IMG_FILES_ABBREVIATED
                - CHECK_REAL_EXIST
                - CONDITIONAL_EXTRACT
        """
        # CrushedImgListFile 이 있는지 체크함과 동시에 불러오는 함수
        if CHECK_CRUSH_IMAGE is True:
            ModeLog('CRUSH_IMG_FILTER ON\n')
            readFileToList(CrushedImgFilePath, self.CrushImgFileNameList, encodingFormat)

            # 만약 해당 파일에 Crushed Image 가 있다면 ConditionCheck 등록
            if self.CrushImgFileNameList:
                self.condClass.addCondition(['CheckCrushImg', self.CheckCrushImg, self.getArgs_CheckCrushImg])
            else:
                ModeLog('CHECK_CRUSH_IMAGE FORCED CANCLELLATION')

        # 축약 이미지 폴더로 돌리는 옵셥일 때 : MakeClass 결과값들의 해당 이미지가 진짜 있는지 존재 체크 Condition 추가
        if ORIGIN_IMG_FILES_ABBREVIATED is True:
            ModeLog('ORIGIN_IMG_FILES_ABBREVIATED ON')
            if self.getAbbreviatedImgDataDict() is True:
                self.condClass.addCondition(['CheckIsExistAbbImg', self.CheckIsExistAbbImg, self.getArgs_CheckIsExistAbbImg])
            else:
                ModeLog('ORIGIN_IMG_FILES_ABBREVIATED FORCED CANCLELLATION')

        # MakeClass 결과물 값이 특정 폴더에 해당 이미지가 실제로 있는지 체크하는 모드
        if CHECK_REAL_EXIST is True:
            ModeLog('CHECK_REAL_EXIST ON')
            if self.getCheckRealExistDataDict() is True:
                self.condClass.addCondition(['CheckRealExist', self.CheckRealExist, self.getArgs_CheckRealExist])
            else:
                ModeLog('CHECK_REAL_EXIST FORCED CANCLELLATION')

        # SizeFilter 함수 조건값으로 특정 조건 결과값들만 필터링하는 모드
        if SIZE_FILTERING is True:
            ModeLog('SIZE_FILTERING ON')
            self.condClass.addCondition(['SizeFilter', self.SizeFilter, self.getArgs_SizeFilter])


    # SelectUI Function
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    """
        sendArg Type : [ Type(str), Name(str), isDir(bool), DefaultThatValue(str/bool) ]

        Type :
            - FD : File Dialog
            - CB : CheckBox
            - LE : LineEdit

        ARGS :
            [FD]
            - OriginXmlDirPath    
            - OriginImgDirPath    
            - ResultDirPath       
            - AbbreviatedImgPath  
            - CrushedImgFilePath 
            - CheckRealExistPath

            [CB]
            - MAKE_ORIGIN_CLASS
            - MAKE_ZIPPED_CLASS
            - CONDITIONAL_EXTRACT
            - ORIGIN_IMG_FILES_ABBREVIATED
            - CHECK_REAL_EXIST
    """
    def setInitSettingSelectUI(self):
        """
            SelectUI 에 넘길 초기값 세팅
            ---------------------------------------------------------------------
            CallBackIn Function - 
                SelectUI class 생성할 때 인자로 넘겨주면, 거기서 이 함수를 필요할 때 실행한다.
            ---------------------------------------------------------------------
            Returns :
                getRunFunctionName  : RunFuntion 이름 (type : str)
                sendArgsList        : List 내 상세 정보는 위 참조 (type : 2D List)
        """
        self.SyncAllValue()
        self.sendArgsList = [   ['FD', 'OriginXmlDirPath',              True,   f'{OriginXmlDirPath}'],
                                ['FD', 'OriginImgDirPath',              True,   f'{OriginImgDirPath}'],
                                ['FD', 'ResultDirPath',                 True,   f'{ResultDirPath}'],
                                ['FD', 'HLINE_0',                       False,  'None'],
                                ['FD', 'AbbreviatedImgPath',            True,   f'{AbbreviatedImgPath}'],
                                ['FD', 'CrushedImgFilePath',            False,  f'{CrushedImgFilePath}'],
                                ['FD', 'CheckRealExistPath',            True,   f'{CheckRealExistPath}'],

                                ['CB', 'MAKE_ORIGIN_CLASS',             False,  f'{MAKE_ORIGIN_CLASS}'],
                                ['CB', 'MAKE_ZIPPED_CLASS',             False,  f'{MAKE_ZIPPED_CLASS}'],
                                
                                ['CB', 'HLINE_1',                       False,  'None'],
                                ['CB', 'SIZE_FILTERING',                False,  f'{SIZE_FILTERING}'],
                                ['CB', 'ANALYSIS_IMAGE_SIZE',           False,  f'{ANALYSIS_IMAGE_SIZE}'],
                                ['CB', 'HLINE_2',                       False,  'None'],
                                ['CB', 'ORIGIN_IMG_FILES_ABBREVIATED',  False,  f'{ORIGIN_IMG_FILES_ABBREVIATED}'],
                                ['CB', 'CHECK_REAL_EXIST',              False,  f'{CHECK_REAL_EXIST}'],
                                ['CB', 'CHECK_CRUSH_IMAGE',             False,  f'{CHECK_CRUSH_IMAGE}'],

                                ['UI',  'SIZE_FILTERING_DICT',          False,  SIZE_FILTERING_DICT]
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

        print("\n* Change Path/Define Value By SelectUI")
        print("--------------------------------------------------------------------------------------")
        for Arg in self.sendArgsList:
            eachTarget = Arg[NAME]
            if returnDict.get(eachTarget) != None:
                # 해당 변수명에 SelectUI 에서 갱신된 값 집어넣기
                globals()[eachTarget] = returnDict[eachTarget]

                if eachTarget == "SIZE_FILTERING_DICT":
                    showLog(f'- {eachTarget:40} -> {summaryFilterDict(globals()[eachTarget])}')
                else:
                    showLog(f'- {eachTarget:40} -> {globals()[eachTarget]}')
        print("--------------------------------------------------------------------------------------\n")

        self.SyncAllValue()
        setResultDir(ResultDirPath)
        # CvatXmlClass 와 연동되는 부분, 생성할 때 가져갔던 OriginXmlDirPath 와 바뀌었을 수 있으니 변경
        self.setChanged_Xml_n_Res_Path(OriginXmlDirPath, ResultDirPath)

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
        - CheckCrushImg
        - CheckIsExistAbbImg
        - SizeFilter
        - CheckRealExist
    """

    # PreTreatment Code
    # -------------------------------------------------------------------------------------

    # 이미지 검색하기 위한 Dict 만드는 함수
    def getAbbreviatedImgDataDict(self):
        """
            ORIGIN_IMG_FILES_ABBREVIATED 가 True 일 때, 이미지 비교하기 위해 Dict Data 만드는 함수
            ---------------------------------------------------------------------
            Returns :
                False:
                    - AbbreviatedImgPath 가 유효하지 않은 경로일 경우
                True:
                    - 정상 작동 시
        """
        self.AbbreviatedImgDict = getImageSearchDict(AbbreviatedImgPath, validImgFormat)

        # 유효한 이미지가 있었을 때
        if self.AbbreviatedImgDict is None:
            ErrorLog(f'`{AbbreviatedImgPath}` is Nothing Vaild Image', lineNum=lineNum(), errorFileName=filename())
            return False

        return True


    # MakeClass 의 이미지가 실제로 존재하는 이미지인지 찾기 위한 Dict 만드는 함수
    def getCheckRealExistDataDict(self):
        """
            CHECK_REAL_EXIST 가 True 일 때, 이미지 비교하기 위해 Dict Data 만드는 함수
            ---------------------------------------------------------------------
            Returns :
                False:
                    - CheckRealExistPath 가 유효하지 않은 경로일 경우
                True:
                    - 정상 작동 시
        """
        # 유효한 경로일 때 -  유효한 이미지 확장자만 리스트에 추가
        self.CheckRealExistDict = getImageSearchDict(CheckRealExistPath, validImgFormat)

        # 유효한 이미지가 있었을 때
        if self.CheckRealExistDict is None:
            ErrorLog(f'`{CheckRealExistPath}` is Nothing Vaild Image', lineNum=lineNum(), errorFileName=filename())
            return False

        return True


    # ConditionFunctions
    # -------------------------------------------------------------------------------------
    def CheckCrushImg(self, imgName):
        """
            Additional ConditionCheck - 1
            imageName 이 CrushImgFileNameList 에 있는지 체크하는 함수
            ---------------------------------------------------------------------
            Args :
                imageName : xml 파일 내 note.findall("image") 중 하나의 get('name') 값
            Returns :
                - get('name') 값이 CrushImgFileNameList 중에 없으면 COND_PASS
                - 해당 값이 리스트에 존재하면 깨진 파일이다 -> COND_FAIL
            ---------------------------------------------------------------------
        """
        if imgName in self.CrushImgFileNameList:
            return COND_FAIL
        return COND_PASS


    # CheckRealExist 와의 차이점 :
    # 얘는 Abbreviated 이미지들 가지고 찾는 거고
    # CheckRealExist 는 Common_images 같은 후처리 이미지들 가지고 찾는 거
    def CheckIsExistAbbImg(self, imgName):
        """
            Additional ConditionCheck - 2 
            imageName 이 AbbreviatedImgDict 에 있는지 체크하는 함수
            ---------------------------------------------------------------------
            Args :
                imageName : xml 파일 내 note.findall("image") 중 하나의 get('name') 값
            Returns :
                - get('name') 값이 AbbreviatedImgDict 중에 있으면 COND_PASS
                - 해당 값이 딕셔너리에 없으면 ImgList.txt 에는 있지만 실제로는 없다 -> COND_FAIL
            ---------------------------------------------------------------------
        """
        if self.AbbreviatedImgDict.get(imgName) == None:
            return COND_FAIL
        else:
            return COND_PASS


    def CheckRealExist(self, imgName):
        """
            Additional ConditionCheck - 3
            imageName 이 CheckRealExistDict 에 있는지 체크하는 함수
            ---------------------------------------------------------------------
            Args :
                imageName : xml 파일 내 note.findall("image") 중 하나의 get('name') 값
            Returns :
                - get('name') 값이 CheckRealExistDict 중에 있으면 COND_PASS
                - 해당 값이 딕셔너리에 없으면 ImgList.txt 에는 있지만 실제로는 없다 -> COND_FAIL
            ---------------------------------------------------------------------
        """
        if self.CheckRealExistDict.get(imgName) == None:
            return COND_FAIL
        else:
            return COND_PASS


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
    def getArgs_CheckCrushImg(self):
        """
            각 이미지별로 CheckCrushImg() 조건 함수를 실행하기 위해 
            이미지마다 변동되는 인자를 리턴하는 함수
            ---------------------------------------------------------------------
            Returns :
                - 현재 이미지의 get("name") (type : str)
            ---------------------------------------------------------------------
        """
        return self.getCurImgName()


    def getArgs_CheckIsExistAbbImg(self):
        return self.getCurImgName()


    def getArgs_SizeFilter(self):
        return [ self.getCurBoxList(), self.getCurImgSize(), SIZE_FILTERING_DICT ]


    def getArgs_CheckRealExist(self):
        return self.getCurImgName()

    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

    def getBoxSize(self, box):
        xTopLeft     = int(float(box.get("xtl")))
        yTopLeft     = int(float(box.get("ytl")))
        xBottomRight = int(float(box.get("xbr")))
        yBottomRight = int(float(box.get("ybr")))

        return [xBottomRight - xTopLeft, yBottomRight - yTopLeft]   


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


    # ABS FUNC(가상 함수) 재정의 함수
    def RunFunction(self):
        """
            CvatXml 의 가상함수를 상속받아 재정의한 실제 실행 부분 함수
            createAttListByBoxList() 에서 만든 정보와 
            ExcelData class 에서 추출한 classData.xlsx 정보를 이용해
            xml 파일 내 하나의 이미지 속성값을 Default Annotation 값으로 만들고,
            ( 여기까지는 값 유형 -> [1, 0, 0, 1, 1, ...] )      # ValueType 1

            True 설정한 MAKE_n_CLASS 값들에 대해서
            실제 해당하는 클래스 Annotation 값으로 만드는 함수
            ( 여기서 값 유형을 문자열로 변경 -> '10011....' )    # ValueType 2
            ---------------------------------------------------------------------
            Attributes:
                attList :
                    각 인자가 개별 박스의 ['label', AttName, AttText] 인 리스트 (type : list)
                
                MCD :
                    ValueType 1 형태의 Default Annotation 값
                    해당 변수를 디폴트 삼아 N_CLASS 의 MAKECLASS 를 만든다

                make[N]Class_PreRes : ValueType 1 형태
                make[N]Class_Res    : ValueType 2 형태

                isUnknownDelete_[N] :
                    주어진 'MCD' 에서 Unknown 에 해당하는 속성값이 True 가 발견되면
                    해당 값이 True 가 되어, 66/39 클래스 계산에서 제외된다
        """
        # xml 파일 내 하나의 이미지 속성값을 Default Annotation 값으로 만드는 부분
        attList = self.createAttListByBoxList()
        self.ClassData.setMakeClassDefaultData(attList)

        # 만든 값 불러오기
        MCD                 = self.ClassData.getMakeClassDefaultData()

        makeOrgClass_Res    = ""
        makeZipClass_Res    = ""

        isUnknownDelete_Zip = False

        imgName             = self.CurImgName

        # True 값 해둔 Case 만 실행
        # Annotation Text 값을 만들고 이때 사용한 이미지와 매칭시켜, 각각의 리스트에 저장
        if MAKE_ORIGIN_CLASS is True:
            makeOrgClass_PreRes, _   = self.ClassData.refineMakeClass(83, MCD)
            makeOrgClass_Res         = self.listToString(makeOrgClass_PreRes)
            self.Result_Origin_ClassList.append(makeOrgClass_Res)

        if MAKE_ZIPPED_CLASS is True:
            makeZipClass_PreRes, isUnknownDelete_Zip = self.ClassData.refineMakeClass(ZIPPED_CLASS_NUM, MCD)
            if isUnknownDelete_Zip is False:
                makeZipClass_Res = self.listToString(makeZipClass_PreRes)
                self.Result_Zip_ClassList.append(makeZipClass_Res)
                self.ResultDeleteUnknown_Zip_List.append(imgName)
            else:
                self.Deleted_Zip_Count += 1

        # Default Annotation 값 자체가 83 클래스니까, 그대로 전부 다 img append 해도 됨
        # 83 클래스 만드는 데 실패할 애들은 진작에 다 걸러졌음
        self.Result_Origin_ImageNameList.append(imgName)

        if ANALYSIS_IMAGE_SIZE is True:
            if MAKE_ZIPPED_CLASS is True:
                if isUnknownDelete_Zip is False:
                    self.imgSizeValueList.append(self.CurImgSizeList)
            else:
                self.imgSizeValueList.append(self.CurImgSizeList)

        
    def analysisImageSize(self):
        widthList   = [ each[WIDTH] for each in self.imgSizeValueList ]
        heightList  = [ each[HEIGHT] for each in self.imgSizeValueList ]

        widthArray  = np.array(widthList)
        heightArray = np.array(heightList)
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

    
    def setImageAnalysisSaveList(self):
        widthList   = [ each[WIDTH] for each in self.imgSizeValueList ]
        heightList  = [ each[HEIGHT] for each in self.imgSizeValueList ]

        for eachIdx in range(len(self.imgSizeValueList)):
            self.imgSizeSaveList.append(f'{widthList[eachIdx]} {heightList[eachIdx]}')
        

    def listToString(self, fromList):
        """
            [0, 1, 0, 0, ...] 꼴의 리스트를 '0100...' 꼴의 문자열로 변환시켜 반환하는 함수
            ---------------------------------------------------------------------
            Args : 
                fromList : [0, 1, 0, 0, ...] 꼴의 리스트
            Returns :
                toString : '0100...' 꼴의 문자열
            ---------------------------------------------------------------------
        """
        toString = ""
        for eachValue in fromList:
            toString += str(eachValue)
        return toString


    def saveMakeClassFile(self, SubPath, SaveList):
        """
            결과값들을 저장한 리스트를 파일로 Save 하는 함수
            ---------------------------------------------------------------------
            Args : 
                SubPath     : 파일 이름
                SaveList    : 파일 내용
            ---------------------------------------------------------------------
        """
        savePath = os.path.join(ResultDirPath, SubPath)
        writeListToFile(savePath, SaveList, encodingFormat)


    def saveMakeClassFiles(self):
        """
            RunFunction 전부 다 돌린 후 나온 결과값들을 
            각각의 저장경로로 배분해 saveMakeClassFile() 로 저장하는 함수
        """
        if MAKE_ORIGIN_CLASS is True:
            self.saveMakeClassFile(ANNOTATION_ORG_TXT, self.Result_Origin_ClassList)
            self.saveMakeClassFile(IMAGE_LIST_ORG_TXT, self.Result_Origin_ImageNameList)

        if MAKE_ZIPPED_CLASS is True:
            self.saveMakeClassFile(ANNOTATION_ZIP_TXT, self.Result_Zip_ClassList)
            self.saveMakeClassFile(IMAGE_LIST_ZIP_TXT, self.ResultDeleteUnknown_Zip_List)

        if ANALYSIS_IMAGE_SIZE is True:
            self.setImageAnalysisSaveList()
            self.saveMakeClassFile(SIZE_ANALYSIS_TXT, self.imgSizeSaveList)


    # ABS FUNC(가상 함수) 재정의 함수
    def FinishFunction(self):
        """
            CvatXml 의 가상함수를 상속받아 재정의한 함수
            Result Sammary 출력하는 함수
        """
        TotalLen_Org_Img = len(self.Result_Origin_ClassList)
        TotalLen_Zip_Img = len(self.Result_Zip_ClassList)
        

        showLog(f'- {"Pass the ConditionCheck":<35} [{CGREEN}{TotalLen_Org_Img:^8}{CRESET}]  ->  MakeClass Origin Image [{CGREEN}{TotalLen_Org_Img:^8}{CRESET}]')
        showLog(f'- {"Deleted by UnknownCheck in ZipClass":<35} [{CRED}{self.Deleted_Zip_Count:^8}{CRESET}]  ->  MakeClass Zipped Image [{CYELLOW}{TotalLen_Zip_Img:^8}{CRESET}]\n')

        self.saveMakeClassFiles()

        if ANALYSIS_IMAGE_SIZE is True:
            self.analysisImageSize()


    # ABS FUNC(가상 함수) 재정의 함수
    def setRunFunctionParam(self):
        """
            CvatXml 의 가상함수를 상속받아 재정의한 함수
            RunFunction 에 들어가기 전 사용할 Param 을 setting 하는 함수
        """
        self.CurBoxList     = self.getCurBoxList()
        self.CurImgName     = self.getCurImgName()
        self.CurImgSizeList = self.getCurImgSize()


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


    # ABS FUNC(가상 함수) 재정의 함수
    def AfterRunFunction(self):
        """
            CvatXml 의 가상함수를 상속받아 재정의한 함수
            사용하지 않지만 정의를 하지 않으면 error 가 뜨기 때문에 그대로 계승

            가상함수는 사용하지 않더라도, 무조건 재정의를 해 줘야 한다.
            ---------------------------------------------------------------------
            Returns : 
                부모 클래스의 함수 그대로 사용 (pass)
            ---------------------------------------------------------------------
        """
        return super().AfterRunFunction()


    # ABS FUNC(가상 함수) 재정의 함수
    def setAfterRunFunctionParam(self):
        """
            CvatXml 의 가상함수를 상속받아 재정의한 함수
            사용하지 않지만 정의를 하지 않으면 error 가 뜨기 때문에 그대로 계승

            가상함수는 사용하지 않더라도, 무조건 재정의를 해 줘야 한다.
            ---------------------------------------------------------------------
            Returns : 
                부모 클래스의 함수 그대로 사용 (pass)
            ---------------------------------------------------------------------
        """
        return super().setAfterRunFunctionParam()


    def run(self):
        """
            클래스를 실행하는 함수
            cvatXmlList 클래스의 run() 함수를 그대로 물려받아 사용한다.
        """
        if self.selectUi.isQuitProgram():
            NoticeLog(f'{self.__class__.__name__} Program EXIT\n')
        else:
            super().run()
            os.startfile(ResultDirPath)


if __name__ == "__main__":
    App         = QApplication(sys.argv)
    RunProgram  = MakeClassSource(App)
    RunProgram.run()
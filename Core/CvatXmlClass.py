"""
Parent class code of classes using CVAT XML file

Classes :
    CvatXml :
        INFO :
            cvatXml 파일을 이용하는 클래스들의 부모 클래스.
            생성자와 공용 변수, run 함수를 제공한다.

        NOTICE :
            !!- 1 --------------------
            !! 해당 클래스는 추상 클래스입니다. 반드시 상속하여 쓰세요. !!
            !!- 2 --------------------
            !! 상속할 때, 상속 받은 클래스에서 가상함수를 정의해주세요. !!

        METHODS :
            - setRunFunctionName(funcName)
            - getRunFunctionName()
            - getCurBoxList()
            - getCurImgName()
            - run()

        ABSTRACT METHODS :
            - RunFunction()
            - setRunFunctionParam()
            - FinishFunction()
            - setFinishFunctionParam()

LAST_UPDATE : 2021/11/08
AUTHOR      : SO BYUNG JUN
"""


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import  sys
import  os
import  xml.etree.ElementTree as ET
from    abc    import *                    # 추상 클래스를 만들기 위한 모듈


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from CoreDefine import *


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from Core.CommonUse         import *
from Core.CheckCondClass    import CheckCondition
from Core.SaveLogClass      import SaveErrorLog


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
START = 0
END   = 1


# CvatXml Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class CvatXml(metaclass=ABCMeta):
    """
        cvatXml 파일을 이용하는 클래스들의 부모 클래스.
        생성자와 공용 변수, run 관련 가상함수를 제공한다.

        NEED When inherit :
            - define RunFunction() function 

        Init Param :
            - OriginXmlPath : 해당 클래스에서 불러올 Xml 파일들의 폴더 이름

        Attributes :
            cvatXmlList         : OriginXmlDirPath 내 cvatXml 파일 List (type : list)
            OriginXmlDirPath    : 생성 시 받은 OriginXmlDirPath (Default : CoreDefine.py)

            condClass :
                Condition Check 를 등록/관리 및 일괄 처리를 위한 CheckCondition 클래스
                setInitCheckCondList() 을 통해 Default CheckCond List 를 CvatXml 생성시 바로 할당한다.

            RunFunctionName     : setRunFunctionName() 을 통해 설정한 가상함수의 이름값 (type : str)
            CurBoxListByImage   : setCurBoxList() 를 통해 set 한 현재 이미지의 box 값들 (type : list)
            CurImageName        : setCurImgName() 를 통해 set 한 현재 이미지의 이름 (type : str)

        Methods :
            - extract_cvatXmlList()
            - setRunFunctionName(funcName)
            - getRunFunctionName()
            - setInitCheckCondList()
            - setCurBoxList(boxList)
            - getCurBoxList()
            - setCurImgName(imgName)
            - getCurImgName()
            - runEachXmlFile(eachXmlFile)
            - run()
            - FinishLog(Params)
        
        CheckCondition Methods :
            - CheckMissingImg(imageName)
            - CheckLabelCount(labelCount)
            - CheckLabelNested(labelSetLen)
            - CheckMoreBag(boxValue)
            - getArgs_CheckMissingImg()
            - getArgs_CheckLabelCount()
            - getArgs_CheckLabelNested()
            - getArgs_CheckMoreBag()

        Abstract Method :
            가상 함수 목록
            - RunFunction()
            - setRunFunctionParam()
            - FinishFunction()
            - setFinishFunctionParam()
    """
    def __init__(self, OriginXmlDirPath):
        """
            멤버 변수 할당
        """
        self.cvatXmlList        = []
        self.OriginXmlDirPath   = OriginXmlDirPath
        
        # ConditionCheck 에러 목록 저장할 경로 이름
        self.CC_LogList         = []
        self.LogToExcel         = SaveErrorLog()

        self.condClass          = None
        self.RunFunctionName    = "NoneFunction"

        self.CurBoxListByImage  = []
        self.CurImageName       = ""
        self.CurImageSizeList   = []

        self.checkPercentageNum = 0
        self.prePercentageCount = 0

        self.TotalRunImgCount   = 0
        self.SuccessImageCount  = 0


    def initCvatXmlClass(self):
        """
            실제 CvatXml init 부분
            setInitCheckCondList() 을 통해 Default CheckCond List 를 CvatXml 생성시 바로 할당
            SelectUI 에서 새로 경로를 받는 Case 때문에, __init__ 시 자동 실행이 아닌 수동 실행
        """
        # CheckCondition 생성과 동시에 Default CheckCond List ADD
        self.condClass = CheckCondition(self.setInitCheckCondList())


    def extract_cvatXmlList(self):
        """
            OriginXmlDirPath 에서 cvatXml 파일들 리스트 추출하는 함수
            ---------------------------------------------------------------------
            Raises :
                - 해당 경로 자체가 유효하지 않은 경로일 때, 프로그램 종료
                - 해당 경로에 확장자가 .xml 이 아닌 파일이 있거나, 아무런 .xml 파일이 없을 때 error_handling() 발생
            ---------------------------------------------------------------------
        """
        self.cvatXmlList.clear()

        # 경로가 실제로 있는지 체크하고, 없다면 프로그램 종료
        CheckExistDir(self.OriginXmlDirPath)

        # 실제 있는 경로면, xml 파일들만 목록에 추가
        for path, _, files in os.walk(self.OriginXmlDirPath):
            for eachFile in files:
                _, ext = os.path.splitext(eachFile)
                if ext != ".xml":
                    error_handling(f"{eachFile} is Not XML", filename(), lineNum())
                    break
                else:
                    self.cvatXmlList.append(os.path.join(path, eachFile))

        if not self.cvatXmlList:
            error_handling("cvatXmlList is Empty. There are no files to run the program. Quit the program.", filename(), lineNum())
            showErrorList()
            sys.exit(-1)

        SuccessLog(f"Extract cvatXmlList Done : {len(self.cvatXmlList)} Files")


    def setRunFunctionName(self, funcName):
        """
            RunFunctionName 을 set 하는 함수
            ---------------------------------------------------------------------
            Args :
                funcName : RunFunctionName 에 set 할 함수 이름 (type : str)
            ---------------------------------------------------------------------
        """
        self.RunFunctionName = funcName


    def getRunFunctionName(self):
        """
            RunFunctionName 을 get 하는 함수
            ---------------------------------------------------------------------
            Returns :
                RunFunctionName : (type : str)
            ---------------------------------------------------------------------
        """
        return self.RunFunctionName


    def setChanged_Xml_n_Res_Path(self, xmlPath, resPath):
        """
            주어진 경로로 OriginXmlDirPath 을 교체한 다음, 
            cvatXmlList 를 리셋하고 다시 채워넣는 함수
            ---------------------------------------------------------------------
            Args :
                xmlPath : 새로 교체할 XML 경로 (type : str)
                resPath : 새로 교체할 결과 경로 (type : str)
            ---------------------------------------------------------------------
        """
        self.OriginXmlDirPath = xmlPath
        self.LogToExcel.set_ResDir(resPath)

        # 주어진 경로로부터 cvatXml 파일들의 리스트를 추출하고, 만약 xml 파일이 없다면 바로 종료
        self.extract_cvatXmlList()


    def setInitCheckCondList(self):
        """
            Default CheckCond 들을 규칙에 맞게 리스트로 만들어서 반환하는 함수
            ---------------------------------------------------------------------
            Returns :
                initCheckCondList :
                    CheckCondition 생성시 초기화 인자로 들어가는 값.
                    해당 클래스 생성과 동시에 CheckCondition.addConditionList(initCheckCondList) 된다.
            ---------------------------------------------------------------------
            ROLE :
                [ ConditionName, ConditionFunctions, getArgs_ConditionFunctions ]
        """
        initCheckCondList = [   ['CheckMissingImg',     self.CheckMissingImg,   self.getArgs_CheckMissingImg],
                                ['CheckLabelCount',     self.CheckLabelCount,   self.getArgs_CheckLabelCount],
                                ['CheckLabelNested',    self.CheckLabelNested,  self.getArgs_CheckLabelNested],
                                ['CheckBagError',       self.CheckBagError,     self.getArgs_CheckBagError]
                            ]
        return initCheckCondList


    # Default CheckCond List
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

    # ConditionName
    # -------------------------------------------------------------------------------------
    """
    [ Default Condition Name ]
        - CheckMissingImg
        - CheckLabelCount
        - CheckLabelNested
        - CheckBagError
    """

    # ConditionFunctions
    # -------------------------------------------------------------------------------------
    def CheckMissingImg(self, imageName):
        """
            DefaultConditionCheck - 1
            imageName 이 입력되었는지 체크하는 조건 함수
            ---------------------------------------------------------------------
            Args :
                imageName : xml 파일 내 note.findall("image") 중 하나의 get('name') 값
            Returns :
                - get('name') 값이 정상적으로 있으면 COND_PASS
                - 해당 값이 없으면 error -> COND_FAIL
            ---------------------------------------------------------------------
        """
        if not imageName:
            return COND_FAIL
        return COND_PASS


    def CheckLabelCount(self, labelCount):
        """
            DefaultConditionCheck - 2
            해당 이미지의 label 이 네 개 다 있는지 1차 체크하는 함수
            네 개 초과여도 FAIL 정확히 네 개
            ---------------------------------------------------------------------
            Args :
                labelCount : 이미지의 findall("box") 갯수
            Returns :
                - 갯수가 4 개면 COND_PASS
                - 아니면 COND_FAIL
            ---------------------------------------------------------------------
        """
        if labelCount != 4:
            return COND_FAIL
        return COND_PASS


    def CheckLabelNested(self, labelSetLen):
        """
            DefaultConditionCheck - 3
            해당 이미지의 label 이 각각 별개의 값인지 2차 체크하는 함수
            ---------------------------------------------------------------------
            Args :
                labelSetLen : 중복을 제외한 이미지의 findall("box") 갯수
            Returns :
                - 갯수가 4 개면 COND_PASS
                - 아니면 COND_FAIL
            ---------------------------------------------------------------------
        """
        if labelSetLen != 4:
            return COND_FAIL
        return COND_PASS


    def CheckBagError(self, boxValue):
        """
            DefaultConditionCheck - 4
            findall("box") 의 속성 값 중 가방에 해당하는 값이 두 개 이상인지 체크하는 함수
            ---------------------------------------------------------------------
            Args :
                boxValue : findall("box") 
            Returns :
                - 가방에 해당하는 값이 두 개 미만이면 COND_PASS
                - 아니면 COND_FAIL
            ---------------------------------------------------------------------
        """
        bagList  = ["unknown_bag", "plasticbag", "shoulderbag", "handbag", "backpack", "bagless"]
        ValidBox = [ box for box in boxValue if box.get('label') == 'all' ]
        bagCount = 0

        for box in ValidBox:
            for att in box.findall('attribute'):
                if att.get('name') in bagList:
                    bagCount += isTrue(att.text)

        if bagCount != 1:
            return COND_FAIL
        return COND_PASS


    # getArgs_ConditionFunctions
    # -------------------------------------------------------------------------------------
    def getArgs_CheckMissingImg(self):
        """
            각 이미지별로 CheckMissingImg() 조건 함수를 실행하기 위해 
            이미지마다 변동되는 인자를 리턴하는 함수
            ---------------------------------------------------------------------
            Returns :
                - 현재 이미지의 get("name") (type : str)
            ---------------------------------------------------------------------
        """
        return self.getCurImgName()


    def getArgs_CheckLabelCount(self):
        """
            각 이미지별로 CheckLabelCount() 조건 함수를 실행하기 위해 
            이미지마다 변동되는 인자를 리턴하는 함수
            ---------------------------------------------------------------------
            Returns :
                - 현재 이미지의 findall("box") 갯수 (type : int)
            ---------------------------------------------------------------------
        """
        return len(self.getCurBoxList())


    def getArgs_CheckLabelNested(self):
        """
            각 이미지별로 CheckLabelNested() 조건 함수를 실행하기 위해 
            이미지마다 변동되는 인자를 리턴하는 함수
            ---------------------------------------------------------------------
            Returns :
                현재 이미지의 findall("box") 값 중 get('label') 들을 
                중첩 제거하고 리턴 (type : int)
            ---------------------------------------------------------------------
        """
        boxValue    = self.getCurBoxList()
        labelList   = []

        for box in boxValue:
            labelList.append(box.get('label'))
        
        return len(set(labelList))


    def getArgs_CheckBagError(self):
        """
            각 이미지별로 CheckBagError() 조건 함수를 실행하기 위해 
            이미지마다 변동되는 인자를 리턴하는 함수
            ---------------------------------------------------------------------
            Returns :
                현재 이미지의 findall("box") 값 (type : list)
            ---------------------------------------------------------------------
        """
        return self.getCurBoxList()


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-


    # 가상 함수 : 상속받은 클래스에서 해당 함수를 정의해야만 함
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    @abstractmethod
    def RunFunction(self):
        """
            ABS FUNC.
            CvatXml 클래스를 상속받은 클래스가 실제로 실행하는 RunFunction 부분
            상속받은 클래스가 재정의 해야 함
            ---------------------------------------------------------------------
            Args    : None (setRunFunctionParam() 함수를 통해서 전달)
            Raises  : None (재정의 시 추가할 수 있음)
            Returns : Bool 값 return 줄 수 있음
            ---------------------------------------------------------------------
            Reference :
                RunFunction/MakeClass.py 참조
        """
        pass

    @abstractmethod
    def setRunFunctionParam(self):
        """
            ABS FUNC.
            재정의 된 RunFunction 이 사용할 인자들을 set 하는 함수
            ---------------------------------------------------------------------
            Reference :
                RunFunction/MakeClass.py 참조
        """
        pass

    @abstractmethod
    def AfterRunFunction(self):
        """
            ABS FUNC.
            RunFunction 의 결과값(True/False) 에 따라 실행 되는 함수
            ---------------------------------------------------------------------
            Args    : None (setFinishFunctionParam() 함수를 통해서 전달)
            Raises  : None (재정의 시 추가할 수 있음)
            ---------------------------------------------------------------------
            Reference :
                RunFunction/MakeClass.py 참조
        """
        pass

    @abstractmethod
    def setAfterRunFunctionParam(self):
        """
            ABS FUNC.
            재정의 된 AfterRunFunction 이 사용할 인자들을 set 하는 함수
            ---------------------------------------------------------------------
            Reference :
                RunFunction/MakeClass.py 참조
        """
        pass

    @abstractmethod
    def FinishFunction(self):
        """
            ABS FUNC.
            모든 RunFunction 이 끝나고 run() 함수 마지막에 실행하는 함수
            ---------------------------------------------------------------------
            Args    : None (setFinishFunctionParam() 함수를 통해서 전달)
            Raises  : None (재정의 시 추가할 수 있음)
            ---------------------------------------------------------------------
            Reference :
                RunFunction/MakeClass.py 참조
        """
        pass

    @abstractmethod
    def setFinishFunctionParam(self):
        """
            ABS FUNC.
            재정의 된 FinishFunction 이 사용할 인자들을 set 하는 함수
            ---------------------------------------------------------------------
            Reference :
                RunFunction/MakeClass.py 참조
        """
        pass

    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-


    def setCurBoxList(self, boxList):
        """
            상속 받은 클래스에서도 현재 이미지의 xml 값들을 알기 위해
            해당 이미지의 findall("box") 로 CurBoxListByImage set 하는 함수
            이 함수로 인해서 상속받은 클래스의 RunFunction 에서 실시간으로 갱신된
            각 이미지의 boxList를 활용할 수 있다.
            ---------------------------------------------------------------------
            Args :
                boxList : 
                    runEachXmlFile() 에서 현재 체크하고 있는 이미지의 
                    findall("box") 값 (type : list)
            ---------------------------------------------------------------------
        """
        self.CurBoxListByImage = boxList


    def getCurBoxList(self):
        """
            해당 클래스가 아니어도 현재 이미지의 xml 값들을 알기 위해
            setCurBoxList() 로 미리 set 해둔
            해당 이미지의 findall("box") 를 get 하는 함수
            ---------------------------------------------------------------------
            Returns : 
                CurBoxListByImage (type : list)
            ---------------------------------------------------------------------
        """
        return self.CurBoxListByImage


    def setCurImgName(self, imgName):
        """
            상속 받은 클래스에서도 현재 이미지의 xml 값들을 알기 위해
            해당 이미지의 get("name") 으로 CurImageName set 하는 함수
            이 함수로 인해서 상속받은 클래스의 RunFunction 에서 실시간으로 갱신된
            각 이미지의 imgName을 활용할 수 있다.
            ---------------------------------------------------------------------
            Args :
                imgName : 
                    runEachXmlFile() 에서 현재 체크하고 있는 이미지의 
                    get("name") 값 (type : str)
            ---------------------------------------------------------------------
        """
        self.CurImageName = imgName


    def getCurImgName(self):
        """
            해당 클래스가 아니어도 현재 이미지의 xml 값들을 알기 위해
            setCurImgName() 로 미리 set 해둔
            해당 이미지의 get("name") 을 get 하는 함수
            ---------------------------------------------------------------------
            Returns : 
                CurImageName (type : str)
            ---------------------------------------------------------------------
        """
        return self.CurImageName


    def setCurImgSize(self, sizeList):
        """
            상속 받은 클래스에서도 현재 이미지의 너비x높이 사이즈를 알기 위해
            해당 이미지의 get("width"), get("height") 으로 CurImgSize set 하는 함수
            이 함수로 인해서 상속받은 클래스의 RunFunction 에서 실시간으로 갱신된
            각 이미지의 Size를 활용할 수 있다.
            ---------------------------------------------------------------------
            Args :
                imgName : 
                    runEachXmlFile() 에서 현재 체크하고 있는 이미지의 
                    get("width"), get("height") 값 (type : list)
            ---------------------------------------------------------------------        
        """
        self.CurImageSizeList = sizeList


    def getCurImgSize(self):
        """            
            해당 클래스가 아니어도 현재 이미지의 너비x높이 사이즈를 알기 위해
            setCurImgSize() 로 미리 set 해둔
            해당 이미지의 Size를 get 하는 함수 ( width, height )
            ---------------------------------------------------------------------
            Returns : 
                CurImageSizeList (type : list)
            ---------------------------------------------------------------------
        """
        return self.CurImageSizeList


    def showCurCount(self, curCount, totalCount):
        """
            현재 진행상황 Percentage Bar 로 시각화 해서 터미널에 보여주는 함수
            ---------------------------------------------------------------------
            Args :
                curCount    : 현재 idx
                totalCount  : 총 idx
            ---------------------------------------------------------------------
        """
        # 100% 완료되면 잔상 지우려고 해당 줄 싹 밀어버리기
        if curCount == totalCount:
            print(' '*100, '\r', end='')
            return
            
        percentCount = int(curCount * self.checkPercentageNum)

        # 이미지가 넘어갈 때마다 터미널에 보여주면 너무 속도 느려지니까, 퍼센트값이 달라질때만 출력
        # 만약 이미지가 80000개면 80000번 출력할 걸 50번(2%마다 출력하니까) 출력으로 압축 
        if percentCount != self.prePercentageCount:
            curBar  = '#' if CRESET == '' else '|'
            showBar = f'{CGREEN}' + f'{curBar}' * percentCount + f'{CRESET}' + '|' * (50 - percentCount)
            print(f' [ {curCount:^5} / {totalCount:5} ] {showBar:60} {percentCount*2:3}%\r', end='')

        self.prePercentageCount = percentCount


    def runEachXmlFile(self, eachXmlFile):
        """
            cvatXmlList 에 저장된 xml 파일들 중 하나를 가져와
            xml 파일 내 이미지들을 순차적으로 불러와서
            ConditionCheck 후에
            재정의 된 RunFunction 을 실행하여 프로그램의 목적에 맞게 처리하는 함수
            ---------------------------------------------------------------------
            Args :
                eachXmlFile : xml 파일 이름 (type : str)
            Returns :
                totalImgCount : 
                    현재 xml 파일에 포함된 이미지의 총 갯수
                SuccessCount :
                    totalImgCount 중 ConditionCheck:COND_PASS 하고
                    RunFunction 결과값이 True 인 이미지의 총 갯수
            ---------------------------------------------------------------------
            Attributes :
                FullXmlPath : 해당 파일명 xml 의 총 경로

                tree        : 잘
                note        : 몰랑
                    ..아무튼 xml 속성 값들 가져오는 변수들

                noteImage   : 해당 xml 파일 내 모든 이미지 값들 (type : list)
        """
        FullXmlPath     = eachXmlFile
        tree            = ET.parse(FullXmlPath)
        note            = tree.getroot()

        noteImage       = note.findall("image")
        totalImgCount   = len(noteImage)
        SuccessCount    = 0

        # 연산량 줄이기 위해 미리 계산
        self.checkPercentageNum = 50 / totalImgCount

        print(f"* [{FullXmlPath}] - Image Count {totalImgCount}")
        print("--------------------------------------------------------------------------------------")

        # CurConditionFailCount Reset
        self.condClass.resetCurFailCheckAll()

        # 해당 for 문은 특히 순서 잘 지켜야함!
        for idx, eachImage in enumerate(noteImage):
            # 0. CountShow  --- 속도 빠르게 할 거면 아랫줄 주석처리
            self.showCurCount(idx + 1, totalImgCount)

            # 1. 각 이미지에 대해 name 과 size, box 목록을 추출
            imgName  = eachImage.get("name")
            boxValue = eachImage.findall("box")
            sizeList = [int(eachImage.get("width")), int(eachImage.get("height"))]

            # 2. 추출한 Scope 내의 변수를 클래스 멤버 변수에 set : 다른 곳에서 참조하기 위해서
            self.setCurBoxList(boxValue)
            self.setCurImgName(imgName)
            self.setCurImgSize(sizeList)

            # 3. 바로 위에서 set 한 변수들을 기반으로 ConditionCheckAll 실행
            checkRes, failCondName = self.condClass.checkCondAllParam()

            # 4. 만약 체크 결과값이 FAIL 이면 더 이상 아래로 내려가지 않고 다음 이미지로 넘어감
            # 이 때 에러 로그를 [ xmlFileName, imgName, errorConditionName ]
            if checkRes == COND_FAIL:
                self.CC_LogList.append([ eachXmlFile, imgName, failCondName ])
                continue

            # 5. 가상함수인 RunFunction 을 실행하기 전, 상속받은 클래스에서 set RunFunction Param
            self.setRunFunctionParam()

            # 6. RunFunction 을 실행한 다음, 결과값에 따른 조건분기  
            runFuncRes = True
            runFuncRes = self.RunFunction()

            # 7. RunFunction 결과값에 따라 실행되는 후처리 함수
            if runFuncRes is False:
                self.setAfterRunFunctionParam()
                self.AfterRunFunction()
                continue

            SuccessCount += 1

        self.condClass.showCurFailLog()

        return totalImgCount, SuccessCount


    def run(self):
        """
            클래스를 실행하는 함수
            cvatXmlList 리스트를 for 문을 돌며 각자의 xml 파일을 runEachXmlFile() 로 넘긴다
            또한 모든 xml 파일이 runEachXmlFile() 끝나면 후처리를 하는 함수
        """
        # setRunFunctionName() 을 안 했다면 여기서 일단 체크 : 안전장치
        if self.RunFunctionName == "NoneFunction":
            error_handling('Is Set RunFunction? check setRunFunctionName()', filename(), lineNum())

        print()
        NoticeLog(f'{self.RunFunctionName} START\n')

        # Result Summary 출력을 위한 Count 변수들
        TotalRunImageCount  = 0
        TotalSuccessCount   = 0
        XmlFileCount        = len(self.cvatXmlList)
        TimeList            = []

        # 시작 시간 체크
        TimeList.append(getCurTime())

        # cvatXmlList 하나씩 돌면서 각 xml 파일을 runEachXmlFile() 실행
        for idx, eachXmlPath in enumerate(self.cvatXmlList):
            print(f"[ {CGREEN}{idx+1:3}{CRESET} / {XmlFileCount:3} ]")
            print("--------------------------------------------------------------------------------------")
            perRunImage, perSuccessCount    = self.runEachXmlFile(eachXmlPath)
            TotalRunImageCount              += perRunImage
            TotalSuccessCount               += perSuccessCount

        # 종료 시간 체크
        TimeList.append(getCurTime())

        self.setOperateImageCount(TotalRunImageCount, TotalSuccessCount)

        # 상속 받은 클래스에서 재정의 된 최종 실행 함수 - 후처리 함수들
        self.setFinishFunctionParam()
        self.FinishFunction()

        # ConditionCheckErrorLog 저장
        self.LogToExcel.set_ErrorLogList(self.CC_LogList)
        self.LogToExcel.saveLogToFile()

        # 다 돌고나서 Result Print
        self.FinishLog(TotalRunImageCount, TotalSuccessCount, TimeList, XmlFileCount)
        

    def FinishLog(self, TotalRun, TotalSuccess, TimeList, FileCount):
        """
            넘겨받은 인자값들을 참고하여 Result Summary Print
            ---------------------------------------------------------------------
            Args :
                TotalRun        : 총 실행된 이미지의 갯수
                TotalSuccess    : 그 중 실행 결과가 Success 인 이미지 갯수
                TimeList        : 시작시간/종료시간이 기록된 list
                FileCount       : 총 실행한 xml 파일의 갯수
            ---------------------------------------------------------------------
        """
        print()
        print(f"# [ {self.RunFunctionName} DONE ] -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        self.condClass.showTotalFailLog()
        print("# [ INFO ]")
        print(f"- {'Program Start':36} : {timeToString(TimeList[START])}")
        print(f"- {'Program End':36} : {timeToString(TimeList[END])}")
        print(f"- {'RunTime':36} : {diffTime(TimeList[START], TimeList[END])}")
        print(f"- {'Total Run Image Count':36} : {TotalRun} ( {FileCount} Files )")
        print(f"- {'Total Success Count':36} : {TotalSuccess}")
        print("--------------------------------------------------------------------------------------")
        print(f"# [ {self.RunFunctionName} DONE ] -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
        showErrorList()


    def setOperateImageCount(self, TotalRunCount, TotalSuccessCount):
        self.TotalRunImgCount   = TotalRunCount
        self.SuccessImageCount  = TotalSuccessCount

    
    def getOperateImageCount(self):
        return self.TotalRunImgCount, self.SuccessImageCount
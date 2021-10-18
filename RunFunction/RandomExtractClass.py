"""
This python file is a code that extracts a random percentage 
from a given xml file and image path file.

Set the source file path to extract,
After setting the file name to save the result value,
Adjust the extraction manipulation parameters.

LAST UPDATE DATE : 21/10/11
MADE BY SHY
"""


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from random import randint
import os
import sys
import copy


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

# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from UI.SelectUI.SelectUIClass import *


# INSTALLED PACKAGE IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import pandas as pd


# SOURCE & DEST PATH
# 해당 OriginXmlDirPath 과 ResultDirPath 값을 변경하고 싶으면, CoreDefine.py 에서 변경하면 됨! ( 경로 변경 통합 )
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
AnnotationFile      = r"C:\PythonHN\AttributeProgram\OLD/Annotation_39_Class.txt"
ImgListFile         = r"C:\PythonHN\AttributeProgram\OLD/39Class_ImgList.txt"
ResultDirPath       = copy.copy(Result_Dir_Path)

encodingFormat      = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat      = copy.copy(VALID_IMG_FORMAT)


# 결과값 저장 파일 이름
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
SaveAnnotationFileName  = "Result_Annotation.txt"
SaveImgFileName         = "Result_ImgList.txt"


# 추출 조작 변수값들
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
overCount       = 0     # 각 객체 유효값 합이 최소 overCount
ExtractPercent  = 50    # 몇 %나 원본에서 추출할지


# 파일 추출 클래스
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class RandomExtract:
    def __init__(self, QApp):
        self.app = QApp
        self.ProgramName            = "RandomExtract"

        self.TotalObjectSumList     = []    # 원본 파일 각 개체별 유효값 총합
        self.ExtractObjectSumlist   = []    # 추출 파일 각 객체별 유효값 총합

        self.AnnotationTxtList      = []    # 원본 어노테이션 파일 목록 한 줄씩 읽어 리스트에 저장
        self.AnnotationImgList      = []    # 원본 이미지 파일 목록 한 줄씩 읽어 리스트에 저장

        self.ExtractRandomTxtList   = []    # 원본이미지에서 랜덤으로 추출한 리스트
        self.ExtractRandomIdxList   = []    # 유효값으로 추출됐을 때 해당 인덱스들 기억하기 위한 리스트

        self.AnnotationTxtPath      = AnnotationFile
        self.AnnotationImgPath      = ImgListFile
        self.ResultDirPath          = ResultDirPath

        self.overCount              = overCount
        self.ExtractPercent         = ExtractPercent

        self.ClassNum = 0   # 클래스 갯수
        self.TryCount = 1   # 재시도 횟수

        self.classData      = ExcelData()
        self.classNameDict  = {}

        self.sendArgsList   = []

        self.init_RE()


    def init_RE(self):
        self.selectUi = SelectUI(self.setInitSettingForSelectUI, self.getEditSettingForSelectUI)

        self.selectUi.show()
        self.app.exec()

        self.extractTxtListByFile()
        self.checkTotalObjectSum()

        self.countClassNum()
        self.classNameDict = self.classData.getClassNameDictByClassNum(self.ClassNum)

        if self.classNameDict is None:
            error_handling('Load ClassName Failed', filename(), lineNum())


    def setInitSettingForSelectUI(self):
        """
            - AnnotationFile      
            - ImgListFile         
            - ResultDirPath       
        """
        self.sendArgsList = [   ['FD', 'AnnotationFile',    False,  f'{AnnotationFile}'],
                                ['FD', 'ImgListFile',       False,  f'{ImgListFile}'],
                                ['FD', 'ResultDirPath',     True,   f'{ResultDirPath}'],

                                ['LE', 'overCount',         False,  f'{overCount}'],
                                ['LE', 'ExtractPercent',    False,  f'{ExtractPercent}'],
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

        self.AnnotationTxtPath  = AnnotationFile
        self.AnnotationImgPath  = ImgListFile
        self.ResultDirPath      = ResultDirPath

        self.overCount          = int(overCount)
        self.ExtractPercent     = int(ExtractPercent)


    def countClassNum(self):
        # AnnotationTxtList 원본 불러오기 안 됐으면 바로 리턴 예외 처리
        if not self.AnnotationTxtList:
            error_handling(f"{self.AnnotationTxtPath} has nothing annotation list", filename(), lineNum())
            return False

        # 이미 체크했다면 따로 체크 안함
        if self.ClassNum != 0:
            return True
        
        # 아직 체크 안했다면 체크하기
        self.ClassNum = len(self.AnnotationTxtList[0])
        NoticeLog(f"ClassNum : {self.ClassNum}")

        return True


    # 각 객체마다 overCount가 넘는지 체크
    def isOverCount(self, checkObjectSum):
        if checkObjectSum >= self.overCount:
            return True
        else:
            return False


    def checkTotalObjectSum(self):
        # AnnotationTxtList 원본 불러오기 안 됐으면 바로 리턴 예외 처리
        if not self.AnnotationTxtList:
            error_handling(f"{self.AnnotationTxtPath} has nothing annotation list", filename(), lineNum())
            return False

        # 클래스 갯수 아직 안 셌으면 세는 코드
        if self.countClassNum() is False:
            return False

        self.TotalObjectSumList = [ 0 for _ in range(self.ClassNum) ]
        NoticeLog(f'Total Annotation Count - {len(self.AnnotationTxtList)}')

        # 각 클래스별 총합 계산
        for each in self.AnnotationTxtList:
            for i in range(self.ClassNum):
                self.TotalObjectSumList[i] += int(each[i])

        return True


    def checkExtractObjectSum(self):
        # ExtractRandomTxtList 랜덤 추출 안 됐으면 바로 리턴 예외 처리
        if not self.ExtractRandomTxtList:
            error_handling("'checkExtractObjectSum()' Failed - has nothing extract random list", filename(), lineNum())
            return False

        # 클래스 갯수 아직 안 셌으면 세는 코드
        if self.countClassNum() is False:
            return False

        extractObjectSumList = [0 for _ in range(self.ClassNum)]

        for each in self.ExtractRandomTxtList:
            for i in range(self.ClassNum):
                extractObjectSumList[i] += int(each[i])

        for i in range(self.ClassNum):
            checkNum = extractObjectSumList[i]
            if self.isOverCount(checkNum) is False:
                print(f'\t> Fail - {i}th Element [{self.classNameDict[i]:^15}] is Not Over {self.overCount} : {checkNum}')
                return False

        self.ExtractObjectSumlist = extractObjectSumList
        return True


    def extractTxtListByFile(self):
        with open(self.AnnotationTxtPath, 'r', encoding=encodingFormat) as f:
            for eachLine in f:
                eachLine = eachLine.strip('\n')
                self.AnnotationTxtList.append(eachLine)

        SuccessLog(f"Annotation File Read Done - {AnnotationFile}")
        

    def extractImgListByFile(self):
        with open(self.AnnotationImgPath, 'r', encoding=encodingFormat) as f:
            for eachLine in f:
                eachLine = eachLine.strip('\n')
                self.AnnotationImgList.append(eachLine)

        SuccessLog(f"Image File Read Done - {self.AnnotationImgPath}")


    def showResult(self):
        print()
        print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- Result -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        print("------------------------------------------------------------------------------")
        print(" ClassIdx   |  ClassName     |  TotalSum        |  ExtractSum      |  %")
        print("------------------------------------------------------------------------------")
        for i in range(0, self.ClassNum):
            idx = i+1

            if self.TotalObjectSumList[i] != 0:
                eachPercent = (self.ExtractObjectSumlist[i] / self.TotalObjectSumList[i]) * 100
            else:
                eachPercent = 0

            print(f" {idx:<10}|  {self.classNameDict[i]:<15}|  {self.TotalObjectSumList[i]:<16}|  {self.ExtractObjectSumlist[i]:<16}|  {round(eachPercent, 2)}%")
        print("------------------------------------------------------------------------------")
        print()

        extractRealPercent = (len(self.ExtractRandomTxtList) / len(self.AnnotationTxtList)) * 100
        print(f"* Condition\t\t: Extract {self.ExtractPercent}% ( eachSum >= {self.overCount} )")
        print(f"* Total Try\t\t: {self.TryCount}")
        print(f"* Origin File Count\t: {len(self.AnnotationTxtList)}")
        print(f"* Extract File Count\t: {len(self.ExtractRandomTxtList)} ( {round(extractRealPercent,2)}% )")
        print()

    
    def saveResultByExcel(self):
        classNameList = []
        for i in range(self.ClassNum):
            classNameList.append(self.classNameDict[i])

        raw_data =  {   'ClassName':classNameList,
                        'TotalSum':self.TotalObjectSumList,
                        'ExtractSum':self.ExtractObjectSumlist
                    }
        raw_data = pd.DataFrame(raw_data)

        savePath = f'RandomExtract_Pcnt_{self.ExtractPercent}_OvCnt_{self.overCount}.xlsx'
        savePath = os.path.join(self.ResultDirPath, savePath)

        raw_data.to_excel(excel_writer=savePath)

        SuccessLog(f'RandomExtract Summary Log Save to Excel File -> {savePath}')
    
    
    def run(self):
        while True:
            print()
            showLog(f"[{self.TryCount} Try] Select Correct List : Each ObjectSum over {overCount} [ Total File Count : {len(self.AnnotationTxtList)} ]")

            # Try 할때마다 일단 리셋
            self.ExtractRandomTxtList.clear()
            self.ExtractRandomIdxList.clear()
            
            randomNum = 0

            for Idx, eachTxt in enumerate(self.AnnotationTxtList):
                randomNum = randint(1, 100)
                if randomNum <= self.ExtractPercent: # 여기서 정한 %만큼 추출
                    self.ExtractRandomTxtList.append(eachTxt)
                    self.ExtractRandomIdxList.append(Idx)

            print("\t> Extract Done. Check...")
            if self.checkExtractObjectSum() is True:
                print("\t> Extract Success!\n")
                break

            self.TryCount += 1

        TextSavePath = os.path.join(self.ResultDirPath, SaveAnnotationFileName)

        print(f"[ Save Annotation Txt File : {TextSavePath}...", end='\t')
        with open(TextSavePath, 'w') as f:
            for line in self.ExtractRandomTxtList:
                f.write(f"{line}\n")
        print("Done")

        self.extractImgListByFile()

        ImageSavePath = os.path.join(self.ResultDirPath, SaveImgFileName)

        print(f"[ Save Annotation Img File : {ImageSavePath}...", end='\t')
        with open(ImageSavePath, 'w') as f:
            # ExtractRandomIdxList 에 append 된 Idx 만 AnnotationImgList 에서 추출해 기록 : 동일한 인덱스로 어노테이션과 이미지가 저장
            for eachIdx in self.ExtractRandomIdxList:
                f.write(f"{self.AnnotationImgList[eachIdx]}\n")
        print("Done")

        self.showResult()
        self.saveResultByExcel()
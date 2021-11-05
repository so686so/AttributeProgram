"""
This python file is a code that extracts a random percentage 
from a given xml file and image path file.

Set the source file path to extract,
After setting the file name to save the result value,
Adjust the extraction manipulation parameters.

LAST UPDATE DATE : 21/10/25
MADE BY SHY
"""


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from random import randint, sample
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
AnnotationFile      = r"C:/PythonHN/Data/Result/Annotation_39_Class.txt"
ImgListFile         = r"C:/PythonHN/Data/Result/39Class_ImgList.txt"
ResultDirPath       = copy.copy(Result_Dir_Path)

encodingFormat      = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat      = copy.copy(VALID_IMG_FORMAT)


# 결과값 저장 파일 이름
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
SaveAnnotationFileName  = "Annotation.txt"
SaveImgFileName         = "ImgList.txt"

RandomExtractPrefix     = "RandomExtract"
SplitTrainPrefix        = "Split_Train"
SplitTestPrefix         = "Split_Test"

ConditionExtractPrefix  = "ConditionExtract"

# Define
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
RUN_RANDOM_EXTRACT      = True
RUN_SPLIT_TRAIN_TEST    = False

# 추출 조작 변수값들
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
overCount       = 0     # 각 객체 유효값 합이 최소 overCount
ExtractPercent  = 50    # 몇 %나 원본에서 추출할지
SplitPercent    = 75    # 몇 대 몇으로 슬라이스 할지(백분위)


# 파일 추출 클래스
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class ExtractAnnotation:
    def __init__(self, QApp):
        self.app = QApp
        self.ProgramName            = "ExtractAnnotation"

        self.TotalObjectSumList     = []    # 원본 파일 각 개체별 유효값 총합
        self.ExtractObjectSumlist   = []    # 추출 파일 각 객체별 유효값 총합
        self.Sp_TrainObjectSumList  = [] 
        self.Sp_TestObjectSumList   = [] 

        self.AnnotationTxtList      = []    # 원본 어노테이션 파일 목록 한 줄씩 읽어 리스트에 저장
        self.AnnotationImgList      = []    # 원본 이미지 파일 목록 한 줄씩 읽어 리스트에 저장

        self.ExtractRandomTxtList   = []    # 원본이미지에서 랜덤으로 추출한 리스트
        self.ExtractRandomIdxList   = []    # 유효값으로 추출됐을 때 해당 인덱스들 기억하기 위한 리스트
        self.ExtractRandomImgList   = []

        self.SplitTrainResTxtList   = []
        self.SplitTrainResImgList   = []
        self.SplitTestResTxtList    = []
        self.SplitTestResImgList    = []
        self.ConditionResTxtList    = []
        self.ConditionResImgList    = []

        self.AnnotationTxtPath      = AnnotationFile
        self.AnnotationImgPath      = ImgListFile
        self.ResultDirPath          = ResultDirPath

        self.overCount              = overCount
        self.ExtractPercent         = ExtractPercent
        self.SplitPercent           = SplitPercent

        self.SaveAnnotationFileName = SaveAnnotationFileName
        self.SaveImgFileName        = SaveImgFileName

        self.RandomExtractPrefix    = RandomExtractPrefix
        self.SplitTrainPrefix       = SplitTrainPrefix
        self.SplitTestPrefix        = SplitTestPrefix

        self.ClassNum = 0   # 클래스 갯수
        self.TryCount = 1   # 재시도 횟수

        self.classData      = None
        self.classNameDict  = {}

        self.sendArgsList   = []

        self.init_RE()


    def init_RE(self):
        self.selectUi = SelectUI(self.setInitSettingForSelectUI, self.getEditSettingForSelectUI)

        self.selectUi.show()
        self.app.exec()

        if self.selectUi.isSelectDone is False:
            self.run = self.setRunToProgramExit
            return

        self.classData = ExcelData()

        if os.path.isfile(self.AnnotationTxtPath) is False:
            ErrorLog(f'{self.AnnotationTxtPath} is Not Exist! Program Quit.')
            sys.exit(-1)

        if os.path.isfile(self.AnnotationImgPath) is False:
            ErrorLog(f'{self.AnnotationImgPath} is Not Exist! Program Quit.')
            sys.exit(-1)

        self.extractTxtListByFile()
        self.extractImgListByFile()

        if self.checkTotalObjectSum() is False:
            error_handling(f'checkTotalObjectSum() Faild', filename(), lineNum())

        self.countClassNum()
        self.classNameDict = self.classData.getClassNameDictByClassNum(self.ClassNum)

        if self.classNameDict is None:
            error_handling('Load ClassName Failed', filename(), lineNum())


    def setRunToProgramExit(self):
        NoticeLog(f'{self.__class__.__name__} Program EXIT')


    def setInitSettingForSelectUI(self):
        """
            - AnnotationFile      
            - ImgListFile         
            - ResultDirPath       
        """
        self.sendArgsList = [   ['FD', 'AnnotationFile',            False,  f'{AnnotationFile}'],
                                ['FD', 'ImgListFile',               False,  f'{ImgListFile}'],
                                ['FD', 'ResultDirPath',             True,   f'{ResultDirPath}'],

                                ['CB', 'RUN_RANDOM_EXTRACT',        False,  f'{RUN_RANDOM_EXTRACT}'],
                                ['CB', 'RUN_SPLIT_TRAIN_TEST',      False,  f'{RUN_SPLIT_TRAIN_TEST}'],

                                ['LE', 'overCount',                 False,  f'{overCount}'],
                                ['LE', 'ExtractPercent',            False,  f'{ExtractPercent}'],

                                ['LE', 'HLINE_1',                   False,  'None'],
                                ['LE', 'SplitPercent',              False,  f'{SplitPercent}'],
                                ['LE', 'HLINE_2',                   False,  'None'],
                                ['LE', 'SaveAnnotationFileName',    False,  f'{SaveAnnotationFileName}'],
                                ['LE', 'SaveImgFileName',           False,  f'{SaveImgFileName}'],
                                ['LE', 'RandomExtractPrefix',       False,  f'{RandomExtractPrefix}'],
                                ['LE', 'SplitTrainPrefix',          False,  f'{SplitTrainPrefix}'],
                                ['LE', 'SplitTestPrefix',           False,  f'{SplitTestPrefix}'],
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
        self.SplitPercent       = int(SplitPercent)

        self.SaveAnnotationFileName = SaveAnnotationFileName
        self.SaveImgFileName        = SaveImgFileName
        self.RandomExtractPrefix    = RandomExtractPrefix
        self.SplitTrainPrefix       = SplitTrainPrefix
        self.SplitTestPrefix        = SplitTestPrefix


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
        for idx, each in enumerate(self.AnnotationTxtList):
            try:
                for i in range(self.ClassNum):
                    self.TotalObjectSumList[i] += int(each[i])
            except Exception as e:
                error_handling(f"{idx} Line Error - Contents : {each}", filename(), lineNum())
                sys.exit(-1)

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


    def checkSplitTrainObjectSum(self):
        self.Sp_TrainObjectSumList = [0 for _ in range(self.ClassNum)]

        for each in self.SplitTrainResTxtList:
            for i in range(self.ClassNum):
                self.Sp_TrainObjectSumList[i] += int(each[i])

    
    def checkSplitTestObjectSum(self):
        self.Sp_TestObjectSumList = [0 for _ in range(self.ClassNum)]

        for each in self.SplitTestResTxtList:
            for i in range(self.ClassNum):
                self.Sp_TestObjectSumList[i] += int(each[i])


    def showResult(self):
        DF_HeadString = "  ClassIdx  |  ClassName      |  TotalSum        "
        RE_HeadString = ""
        SP_HeadString = ""

        DF_Line = ""
        RE_Line = ""
        SP_Line = ""

        RE_EachPercent = 0

        titleLine = '------------------------------------------------'

        if RUN_RANDOM_EXTRACT is True:
            RE_HeadString   = "|  ExtractSum      |  %        "
            titleLine       += "------------------------------"

        if RUN_SPLIT_TRAIN_TEST is True:
            SP_HeadString   = "|  TrainSum        |  TestSum        "
            titleLine       += "-------------------------------------"

            # 출력하기 위한 각 Element 들의 합 계산
            self.checkSplitTrainObjectSum()
            self.checkSplitTestObjectSum()

        HeadString = f'{DF_HeadString}{RE_HeadString}{SP_HeadString}'

        print()
        print(titleLine)
        print(HeadString)
        print(titleLine)

        for i in range(self.ClassNum):
            if RUN_RANDOM_EXTRACT is True:
                if self.TotalObjectSumList[i] != 0:
                    RE_EachPercent = (self.ExtractObjectSumlist[i] / self.TotalObjectSumList[i]) * 100
                else:
                    RE_EachPercent = 0
                RE_Line = f'|  {self.ExtractObjectSumlist[i]:<16}|  {round(RE_EachPercent, 2):>6}%  '
            if RUN_SPLIT_TRAIN_TEST is True:
                SP_Line = f'|  {self.Sp_TrainObjectSumList[i]:<16}|  {self.Sp_TestObjectSumList[i]:<16}'

            DF_Line = f'  {i:<10}|  {self.classNameDict[i]:<15}|  {self.TotalObjectSumList[i]:<16}'

            print(f'{DF_Line}{RE_Line}{SP_Line}')
        print(titleLine)
        print()

        showLog(f"* Total Try\t\t: {self.TryCount}")
        showLog(f"* Origin File Count\t: {len(self.AnnotationTxtList)}")

        if RUN_RANDOM_EXTRACT:
            extractRealPercent = (len(self.ExtractRandomTxtList) / len(self.AnnotationTxtList)) * 100
            showLog(f"* RE_Condition\t\t: Extract {self.ExtractPercent}% ( eachSum >= {self.overCount} )")
            showLog(f"* Extract File Count\t: {len(self.ExtractRandomTxtList)} ( {round(extractRealPercent,2):>6}% )")
        
        if RUN_SPLIT_TRAIN_TEST:
            showLog(f"* SP_Condition\t\t: Train {self.SplitPercent}% - Test {100-int(self.SplitPercent)}%")
        print()

    
    def saveResultByExcel(self):
        classNameList = []
        for i in range(self.ClassNum):
            classNameList.append(self.classNameDict[i])

        raw_data =  {   'ClassName':classNameList,
                        'TotalSum':self.TotalObjectSumList
                    }

        if RUN_RANDOM_EXTRACT:
            raw_data['ExtractSum'] = self.ExtractObjectSumlist

        if RUN_SPLIT_TRAIN_TEST:
            raw_data['TrainSetSum'] = self.Sp_TrainObjectSumList
            raw_data['TestSetSum']  = self.Sp_TestObjectSumList

        raw_data = pd.DataFrame(raw_data)
        savePath = f'ExtractAnnotation.xlsx'

        if RUN_SPLIT_TRAIN_TEST:
            savePath = f'SP[{self.SplitPercent}Pcnt]_' + savePath
        
        if RUN_RANDOM_EXTRACT:
            savePath = f'RE[{self.ExtractPercent}Pcnt_{self.overCount}OvCnt]_' + savePath

        savePath = os.path.join(self.ResultDirPath, savePath)

        raw_data.to_excel(excel_writer=savePath)

        SuccessLog(f'RandomExtract Summary Log Save to Excel File -> {savePath}')


    def RunRandomExtract(self):
        # 유효한 추출값(각 Element 합이 OverCount 이상일 때) 뽑을 때까지 반복하는 While 문
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

            showLog("\t> Extract Done. Check...")
            if self.checkExtractObjectSum() is True:
                showLog("\t> Extract Success!\n")
                break

            self.TryCount += 1

        for eachIdx in self.ExtractRandomIdxList:
            self.ExtractRandomImgList.append(self.AnnotationImgList[eachIdx])


    def SaveRandomExtract(self):
        SaveAnnoResFileName = f'{self.RandomExtractPrefix}_[{self.ExtractPercent}]Pcnt_[{self.overCount}]OverCnt_{self.SaveAnnotationFileName}'
        TextSavePath        = os.path.join(self.ResultDirPath, SaveAnnoResFileName)

        print(f"- Save RandomExtract Annotation Txt File : {TextSavePath}...", end='\t')
        with open(TextSavePath, 'w', encoding=encodingFormat) as f:
            for line in self.ExtractRandomTxtList:
                f.write(f"{line}\n")
        print("Done")

        SaveImgResFileName  = f'{self.RandomExtractPrefix}_[{self.ExtractPercent}]Pcnt_[{self.overCount}]OverCnt_{self.SaveImgFileName}'
        ImageSavePath = os.path.join(self.ResultDirPath, SaveImgResFileName)

        print(f"- Save RandomExtract Annotation Img File : {ImageSavePath}...", end='\t')
        with open(ImageSavePath, 'w', encoding=encodingFormat) as f:
            for line in self.ExtractRandomImgList:
                f.write(f"{line}\n")
        print("Done")


    def SaveSplitExtract(self):
        SaveTrainAnnoFileName   = f'{self.SplitTrainPrefix}_[{self.SplitPercent}]Pcnt_{self.SaveAnnotationFileName}'
        SaveTestAnnoFileName    = f'{self.SplitTestPrefix}_[{100 - int(self.SplitPercent)}]Pcnt_{self.SaveAnnotationFileName}'

        TrainAnnoSavePath       = os.path.join(self.ResultDirPath, SaveTrainAnnoFileName)
        TestAnnoSavePath        = os.path.join(self.ResultDirPath, SaveTestAnnoFileName)

        print(f"- Save Split Annotation Txt File : {SaveTrainAnnoFileName} / {SaveTestAnnoFileName}...", end='\t')
        with open(TrainAnnoSavePath, 'w', encoding=encodingFormat) as f:
            for line in self.SplitTrainResTxtList:
                f.write(f"{line}\n")
        with open(TestAnnoSavePath, 'w', encoding=encodingFormat) as f:
            for line in self.SplitTestResTxtList:
                f.write(f"{line}\n")
        print("Done")

        SaveTrainImgFileName    = f'{self.SplitTrainPrefix}_[{self.SplitPercent}]Pcnt_{self.SaveImgFileName}'
        SaveTestImgFileName     = f'{self.SplitTestPrefix}_[{100 - int(self.SplitPercent)}]Pcnt_{self.SaveImgFileName}'

        TrainImgSavePath       = os.path.join(self.ResultDirPath, SaveTrainImgFileName)
        TestImgSavePath        = os.path.join(self.ResultDirPath, SaveTestImgFileName)

        print(f"- Save Split Annotation Img File : {SaveTrainImgFileName} / {SaveTestImgFileName}...", end='\t')
        with open(TrainImgSavePath, 'w', encoding=encodingFormat) as f:
            for line in self.SplitTrainResImgList:
                f.write(f"{line}\n")
        with open(TestImgSavePath, 'w', encoding=encodingFormat) as f:
            for line in self.SplitTestResImgList:
                f.write(f"{line}\n")
        print("Done")        


    def RunSplitAnnotation(self):
        TotalAnnotationCount    = 0
        BaseAnnotationList      = []
        BaseImgList             = []

        ANNOTATION_IDX  = 0
        IMAGELIST_IDX   = 1

        if RUN_RANDOM_EXTRACT is True:
            TotalAnnotationCount    = len(self.ExtractRandomTxtList)
            BaseAnnotationList      = self.ExtractRandomTxtList[:]
            BaseImgList             = self.ExtractRandomImgList[:]
        else:
            TotalAnnotationCount    = len(self.AnnotationTxtList)
            BaseAnnotationList      = self.AnnotationTxtList[:]
            BaseImgList             = self.AnnotationImgList[:]

        TextPairImgDict = {}

        for idx in range(TotalAnnotationCount):
            TextPairImgDict[idx] = [BaseAnnotationList[idx], BaseImgList[idx]]

        TotalIdxList = [ i for i in range(TotalAnnotationCount) ]
        SplitTrainAmount = int( (TotalAnnotationCount * self.SplitPercent) / 100 )
        SplitTrainIdxList   = sample(TotalIdxList, SplitTrainAmount)
        SplitTestIdxList    = list(filter(lambda v: v not in SplitTrainIdxList, TotalIdxList))

        showLog('\nSplit Train - Test Set Done')
        showLog('------------------------------------------------------')
        showLog(f'- TotalCount : {TotalAnnotationCount}')
        showLog(f'- TrainCount : {len(SplitTrainIdxList)}')
        showLog(f'- TestCount  : {len(SplitTestIdxList)}\n')

        for eachIdx in SplitTrainIdxList:
            self.SplitTrainResTxtList.append(TextPairImgDict[eachIdx][ANNOTATION_IDX])
            self.SplitTrainResImgList.append(TextPairImgDict[eachIdx][IMAGELIST_IDX])

        for eachIdx in SplitTestIdxList:
            self.SplitTestResTxtList.append(TextPairImgDict[eachIdx][ANNOTATION_IDX])
            self.SplitTestResImgList.append(TextPairImgDict[eachIdx][IMAGELIST_IDX])


    def saveResult(self):
        if RUN_RANDOM_EXTRACT is True:
            self.SaveRandomExtract()

        if RUN_SPLIT_TRAIN_TEST is True:
            self.SaveSplitExtract()


    def run(self):
        if RUN_RANDOM_EXTRACT is True:
            self.RunRandomExtract()

        if RUN_SPLIT_TRAIN_TEST is True:
            self.RunSplitAnnotation()

        self.saveResult()

        self.showResult()
        self.saveResultByExcel()

        os.startfile(self.ResultDirPath)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    RunProgram = ExtractAnnotation(App)
    RunProgram.run()
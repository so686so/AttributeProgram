"""
LAST UPDATE DATE : 21/10/25
MADE BY SHY
"""


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from random import randint, sample, shuffle
import os
import sys
import copy
import re


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
from Core.SingletonClass    import Singleton

# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from UI.SelectUI.SelectUIClass import *


# INSTALLED PACKAGE IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import pandas as pd
import numpy as np

# SOURCE & DEST PATH
# 해당 OriginXmlDirPath 과 ResultDirPath 값을 변경하고 싶으면, CoreDefine.py 에서 변경하면 됨! ( 경로 변경 통합 )
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
AnnotationFile      = r"C:/PythonHN/Data/Result/Annotation_39_Class.txt"
ImgListFile         = r"C:/PythonHN/Data/Result/39Class_ImgList.txt"
ResultDirPath       = copy.copy(Result_Dir_Path)
AnalysisImgSizePath = r"C:\PythonHN\Data\Res1107\ImageSize_Analysis_Source.txt"

encodingFormat      = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat      = copy.copy(VALID_IMG_FORMAT)


# 결과값 저장 파일 이름
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
SaveAnnotationFileName      = "Annotation.txt"
SaveImgFileName             = "ImgList.txt"

ConditionFilterPrefix       = "ConditionFilter"
FilteredImgAnalysisFileName = "Filtered_Img_Size_Analysis.xlsx"

# Define
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
RUN_CONDITION_FILTER    = False
RUN_SHUFFLE_FILE        = False
RUN_LIMIT_COUNT         = False
SIZE_FILTERING          = False


# CONDITION EXTRACT STRING
# 조건식 내 문자열은 항상 "" 로 작성
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
FILTER_CONDITION        = '(Attribute[0] == "1")'
LIMIT_COUNT             = 0


# SIZE_FILTERING DICT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
SIZE_FILTERING_DICT     = copy.copy(CORE_SIZE_FILTER_DICT)


# 파일 추출 클래스
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class FilterCondition(Singleton):
    def __init__(self, QApp):
        self.app = QApp
        self.ProgramName            = "Condition Filter"

        self.TotalObjectSumList     = []    # 원본 파일 각 개체별 유효값 총합
        self.FilterObjectSumList   = []    # 추출 파일 각 객체별 유효값 총합

        self.AnnotationTxtList      = []    # 원본 어노테이션 파일 목록 한 줄씩 읽어 리스트에 저장
        self.AnnotationImgList      = []    # 원본 이미지 파일 목록 한 줄씩 읽어 리스트에 저장

        self.AnalysisSrcWidthList   = []
        self.AnalysisSrcHeightList  = []

        self.ConditionResTxtList    = []
        self.ConditionResImgList    = []
        self.ConditionWidthList     = []
        self.ConditionHeightList    = []

        self.SaveImgSizeList        = []

        self.AnnotationTxtPath      = AnnotationFile
        self.AnnotationImgPath      = ImgListFile
        self.ResultDirPath          = ResultDirPath
        self.AnalysisImgSizePath    = AnalysisImgSizePath

        self.SaveAnnotationFileName = SaveAnnotationFileName
        self.SaveImgFileName        = SaveImgFileName

        self.ConditionFilterPrefix    = ConditionFilterPrefix
        self.ExtractCount           = LIMIT_COUNT

        self.ClassNum = 0   # 클래스 갯수

        self.classData      = None
        self.classNameDict  = {}

        self.sendArgsList   = []

        self.init_RE()


    def init_RE(self):
        self.selectUi = SelectUI(self.setInitSettingForSelectUI, self.getEditSettingForSelectUI)

        self.selectUi.show()
        self.app.exec()

        if self.selectUi.isSelectDone is False:
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

        if SIZE_FILTERING is True:
            if os.path.isfile(self.AnalysisImgSizePath) is False:
                ErrorLog(f'{self.AnalysisImgSizePath} is Not Exist! Program Quit.')
                sys.exit(-1)
            self.extractImgSizeSrcListByFile()

        if self.checkTotalObjectSum() is False:
            error_handling(f'checkTotalObjectSum() Faild', filename(), lineNum())

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
        self.sendArgsList = [   ['FD', 'AnnotationFile',            False,  f'{AnnotationFile}'],
                                ['FD', 'ImgListFile',               False,  f'{ImgListFile}'],
                                ['FD', 'ResultDirPath',             True,   f'{ResultDirPath}'],
                                ['FD', 'HLINE_2',                   False,  'None'],
                                ['FD', 'AnalysisImgSizePath',       False,  f'{AnalysisImgSizePath}'],

                                ['CB', 'RUN_CONDITION_FILTER',     False,  f'{RUN_CONDITION_FILTER}'],
                                ['CB', 'RUN_SHUFFLE_FILE',     False,  f'{RUN_SHUFFLE_FILE}'],
                                ['CB', 'RUN_LIMIT_COUNT',     False,  f'{RUN_LIMIT_COUNT}'],
                                ['CB', 'HLINE_3',                   False,  'None'],
                                ['CB', 'SIZE_FILTERING',     False,  f'{SIZE_FILTERING}'],

                                ['LE', 'SaveAnnotationFileName',    False,  f'{SaveAnnotationFileName}'],
                                ['LE', 'SaveImgFileName',           False,  f'{SaveImgFileName}'],
                                ['LE', 'ConditionFilterPrefix',       False,  f'{ConditionFilterPrefix}'],

                                ['LE', 'HLINE_0',                   False,  'None'],
                                ['LE', 'LIMIT_COUNT',             False,  f'{LIMIT_COUNT}'],
                                ['LE', 'HLINE_1',                   False,  'None'],
                                ['UI', 'FILTER_CONDITION',         False,  f'{FILTER_CONDITION}'],
                                ['UI',  'SIZE_FILTERING_DICT',            False, SIZE_FILTERING_DICT],
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

                if Arg[NAME] == "SIZE_FILTERING_DICT":
                    showLog(f'- {Arg[NAME]:40} -> {summaryFilterDict(globals()[Arg[NAME]])}')
                else:
                    showLog(f'- {Arg[NAME]:40} -> {globals()[Arg[NAME]]}')
        print("--------------------------------------------------------------------------------------\n")

        self.AnnotationTxtPath  = AnnotationFile
        self.AnnotationImgPath  = ImgListFile
        self.ResultDirPath      = ResultDirPath
        self.AnalysisImgSizePath = AnalysisImgSizePath

        self.ExtractCount       = int(LIMIT_COUNT)

        self.SaveAnnotationFileName = SaveAnnotationFileName
        self.SaveImgFileName        = SaveImgFileName
        self.ConditionFilterPrefix    = ConditionFilterPrefix


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


    def checkFilterObjectSum(self):
        # ConditionResTxtList 추출 안 됐으면 바로 리턴 예외 처리
        if not self.ConditionResTxtList:
            error_handling("'checkFilterObjectSum()' Failed - has nothing ConditionResTxtList", filename(), lineNum())
            return False

        # 클래스 갯수 아직 안 셌으면 세는 코드
        if self.countClassNum() is False:
            return False

        filterObjectSumList = [0 for _ in range(self.ClassNum)]

        for each in self.ConditionResTxtList:
            for i in range(self.ClassNum):
                filterObjectSumList[i] += int(each[i])

        self.FilterObjectSumList = filterObjectSumList
        return True


    def extractTxtListByFile(self):
        with open(self.AnnotationTxtPath, 'r', encoding=encodingFormat) as f:
            for eachLine in f:
                eachLine = eachLine.strip('\n')
                self.AnnotationTxtList.append(eachLine)

        SuccessLog(f"Annotation File Read Done - {self.AnnotationTxtPath}")
        

    def extractImgListByFile(self):
        with open(self.AnnotationImgPath, 'r', encoding=encodingFormat) as f:
            for eachLine in f:
                eachLine = eachLine.strip('\n')
                self.AnnotationImgList.append(eachLine)

        SuccessLog(f"Image File Read Done - {self.AnnotationImgPath}")


    def extractImgSizeSrcListByFile(self):
        with open(self.AnalysisImgSizePath, 'r', encoding=encodingFormat) as f:
            for eachLine in f:
                eachLine    = eachLine.strip('\n')
                splitLine   = eachLine.split(sep=' ')
                self.AnalysisSrcWidthList.append(int(splitLine[WIDTH]))
                self.AnalysisSrcHeightList.append(int(splitLine[HEIGHT]))

        SuccessLog(f"ImageSize Analysis Source File Read Done - {self.AnalysisImgSizePath}")            


    def showResult(self):
        DF_HeadString = "  ClassIdx  |  ClassName      |  TotalSum        "
        FT_HeadString = ""

        DF_Line = ""
        FT_Line = ""

        FT_EachPercent = 0

        titleLine = '------------------------------------------------'

        if RUN_CONDITION_FILTER is True or RUN_LIMIT_COUNT is True:
            FT_HeadString   = "|  ExtractSum      |  %        "
            titleLine       += "------------------------------"


        HeadString = f'{DF_HeadString}{FT_HeadString}'

        print()
        print(titleLine)
        print(HeadString)
        print(titleLine)

        FilterMetaList  = re.findall('\d+', FILTER_CONDITION)
        FilterIdxList   = [int(eachOdd) for idx, eachOdd in enumerate(FilterMetaList) if idx % 2 == 0 ]
        FilterBoolList  = [int(eachEvn) for idx, eachEvn in enumerate(FilterMetaList) if idx % 2 == 1 ]

        for i in range(self.ClassNum):
            FilteredMark = ""
            FilteredColor = ""
            if RUN_CONDITION_FILTER is True or RUN_LIMIT_COUNT is True:
                if self.TotalObjectSumList[i] != 0:
                    FT_EachPercent = (self.FilterObjectSumList[i] / self.TotalObjectSumList[i]) * 100
                else:
                    FT_EachPercent = 0
                FT_Line = f'|  {self.FilterObjectSumList[i]:<16}|  {round(FT_EachPercent, 2):>6}%  '

            DF_Line = f'  {i:<10}|  {self.classNameDict[i]:<15}|  {self.TotalObjectSumList[i]:<16}'

            if RUN_CONDITION_FILTER and i in FilterIdxList:
                index = FilterIdxList.index(i)
                if FilterBoolList[index] == 0:
                    FilteredColor   = f"{CRED}"
                    FilteredMark    = f"\t-{CRESET}"
                else:
                    FilteredColor   = f"{CGREEN}"
                    FilteredMark    = f"\t+{CRESET}"

            print(f'{FilteredColor}{DF_Line}{FT_Line}{FilteredMark}')
        print(titleLine)
        print()

        showLog(f"* Origin File Count\t: {len(self.AnnotationTxtList)}")
        showLog(f"* File Shuffled\t\t: {RUN_SHUFFLE_FILE}")

        if RUN_CONDITION_FILTER:
            showLog(f'* Extract Condition\t: {FILTER_CONDITION}')
        if SIZE_FILTERING:
            if SIZE_FILTERING_DICT['common']['CheckSize'] is True:
                showLog(f'* FilterSize Condition\t: AreaSize >= {SIZE_FILTERING_DICT["common"]["Size"]}')
            else:
                showLog(f'* FilterSize Condition\t: WIDTH >= {SIZE_FILTERING_DICT["common"]["Width"]} AND HEIGHT >= {SIZE_FILTERING_DICT["common"]["Height"]}')
        if RUN_LIMIT_COUNT:
            showLog(f'* Extract Count\t\t: {LIMIT_COUNT}')

        showLog(f"* Result File Count\t: {len(self.ConditionResTxtList)}")
        
        print()

    
    def saveResultByExcel(self):
        classNameList = []
        for i in range(self.ClassNum):
            classNameList.append(self.classNameDict[i])

        raw_data =  {   'ClassName':classNameList,
                        'TotalSum':self.TotalObjectSumList
                    }

        if RUN_CONDITION_FILTER:
            raw_data['FilterSum'] = self.FilterObjectSumList

        raw_data = pd.DataFrame(raw_data)
        savePath = os.path.join(self.ResultDirPath, 'FilterCondition.xlsx')
        raw_data.to_excel(excel_writer=savePath)

        SuccessLog(f'RandomExtract Summary Log Save to Excel File -> {savePath}')


    def SaveFilterResult(self):
        ConditionAnnoSavePath   = os.path.join(self.ResultDirPath, f'{ConditionFilterPrefix}_Annotation.txt')
        ConditionImgSavePath    = os.path.join(self.ResultDirPath, f'{ConditionFilterPrefix}_Image.txt')

        if RUN_LIMIT_COUNT:
            ConditionAnnoSavePath   = os.path.join(self.ResultDirPath, f'{ConditionFilterPrefix}_{self.ExtractCount}Count_Annotation.txt')
            ConditionImgSavePath    = os.path.join(self.ResultDirPath, f'{ConditionFilterPrefix}_{self.ExtractCount}Count_Image.txt')

        print(f"- Save Filtered Annotation Txt File : {ConditionAnnoSavePath}...", end='\t')
        with open(ConditionAnnoSavePath, 'w', encoding=encodingFormat) as f:
            for line in self.ConditionResTxtList:
                f.write(f"{line}\n")
        print("Done")

        print(f"- Save Filtered Image Txt File : {ConditionImgSavePath}...", end='\t')
        with open(ConditionImgSavePath, 'w', encoding=encodingFormat) as f:
            for line in self.ConditionResImgList:
                f.write(f"{line}\n")
        print("Done")

        if SIZE_FILTERING:
            FilteredSizeSavePath = os.path.join(self.ResultDirPath, 'Filtered_ImgSize_Analysis_Result.txt')
            self.pretreatmentSaveFilteredImgSizeCheckFile()
            print(f"- Save Analysis ImageSize Txt File : {FilteredSizeSavePath}...", end='\t')
            with open(FilteredSizeSavePath, 'w', encoding=encodingFormat) as f:
                for line in self.SaveImgSizeList:
                    f.write(f"{line}\n")
            print("Done")

    def RunFilterCondition(self):
        BaseAnnotationList      = []
        BaseImgList             = []

        BaseAnnotationList      = self.AnnotationTxtList[:]
        BaseImgList             = self.AnnotationImgList[:]

        ConditionAnnotationList     = []
        ConditionImgList            = []
        ConditionWidthList          = []
        ConditionHeightList         = []

        for Idx, Attribute in enumerate(BaseAnnotationList):
            if eval(FILTER_CONDITION):
                ConditionAnnotationList.append(Attribute)
                ConditionImgList.append(BaseImgList[Idx])

                if SIZE_FILTERING is True:
                    ConditionWidthList.append(self.AnalysisSrcWidthList[Idx])
                    ConditionHeightList.append(self.AnalysisSrcHeightList[Idx])

        if SIZE_FILTERING is True:
            recvCondSize    = SIZE_FILTERING_DICT
            if recvCondSize['common']['isCheck'] is False:
                ErrorLog('Check FilterSize Condition in \'common\' Category!', lineNum=lineNum(), errorFileName=filename())
                sys.exit(-1)

            CondisSize      = recvCondSize['common']['CheckSize']
            CondWidth       = recvCondSize['common']['Width']
            CondHeight      = recvCondSize['common']['Height']
            CondSize        = recvCondSize['common']['Size']

            TempAnnList     = []
            TempImgList     = []
            TempWidList     = []
            TempHghList     = []

            # 가로 세로 말고 넓이로 체크
            if CondisSize is True:
                for Idx, Attribute in enumerate(ConditionAnnotationList):
                    Size = ConditionWidthList[Idx] * ConditionHeightList[Idx]
                    if Size >= CondSize:
                        TempAnnList.append(Attribute)
                        TempImgList.append(ConditionImgList[Idx])
                        TempWidList.append(ConditionWidthList[Idx])
                        TempHghList.append(ConditionHeightList[Idx])
            else:
                for Idx, Attribute in enumerate(ConditionAnnotationList):
                    if  (ConditionWidthList[Idx] >= CondWidth) and \
                        (ConditionHeightList[Idx] >= CondHeight):
                        TempAnnList.append(Attribute)
                        TempImgList.append(ConditionImgList[Idx])
                        TempWidList.append(ConditionWidthList[Idx])
                        TempHghList.append(ConditionHeightList[Idx])

            ConditionAnnotationList = TempAnnList
            ConditionImgList        = TempImgList
            ConditionWidthList      = TempWidList
            ConditionHeightList     = TempHghList

        self.ConditionResTxtList = ConditionAnnotationList
        self.ConditionResImgList = ConditionImgList
        self.ConditionWidthList  = ConditionWidthList
        self.ConditionHeightList = ConditionHeightList

        self.checkFilterObjectSum()


    def RunShuffle(self):
        BaseAnnotationList      = []
        BaseImgList             = []
        BaseWidthList           = []
        BaseHeightList          = []

        ShuffleAnnotationList   = []
        ShuffleImageList        = []
        ShuffleWidthList        = []
        ShuffleHeightList       = []

        if RUN_CONDITION_FILTER is True:
            BaseAnnotationList  = self.ConditionResTxtList[:]
            BaseImgList         = self.ConditionResImgList[:]
        else:
            BaseAnnotationList  = self.AnnotationTxtList[:]
            BaseImgList         = self.AnnotationImgList[:]

        if SIZE_FILTERING is True:
            if RUN_CONDITION_FILTER is True:
                BaseWidthList   = self.ConditionWidthList[:]
                BaseHeightList  = self.ConditionHeightList[:]
            else:
                BaseWidthList   = self.AnalysisSrcWidthList[:]
                BaseHeightList  = self.AnalysisSrcHeightList[:]            

        baseTotalCount  = len(BaseAnnotationList)
        baseIdxList     = [ i for i in range(baseTotalCount) ]

        showLog(f'\nbaseIdxList Len : {baseTotalCount}\n\t[ {baseIdxList[:10]} ... ]')
        shuffle(baseIdxList)
        showLog(f'\t\t-> [ {baseIdxList[:10]} ... ]')

        for eachIdx in range(baseTotalCount):
            ShuffleAnnotationList.append(BaseAnnotationList[baseIdxList[eachIdx]])
            ShuffleImageList.append(BaseImgList[baseIdxList[eachIdx]])

        if SIZE_FILTERING is True:
            for eachIdx in range(baseTotalCount):
                ShuffleWidthList.append(BaseWidthList[baseIdxList[eachIdx]])
                ShuffleHeightList.append(BaseHeightList[baseIdxList[eachIdx]])

            self.ConditionWidthList     = ShuffleWidthList
            self.ConditionHeightList    = ShuffleHeightList           

        self.ConditionResTxtList = ShuffleAnnotationList
        self.ConditionResImgList = ShuffleImageList
        SuccessLog('Shuffling Done')
            

    def RunExtractLimitCount(self):
        BaseAnnotationList      = []
        BaseImgList             = []
        BaseWidthList           = []
        BaseHeightList          = []

        ExtractCountTxtList     = []
        ExtractCountImgList     = []
        ExtractCountWidthList   = []
        ExtractCountHeightList  = []

        if RUN_CONDITION_FILTER is True:
            BaseAnnotationList  = self.ConditionResTxtList[:]
            BaseImgList         = self.ConditionResImgList[:]
        else:
            BaseAnnotationList  = self.AnnotationTxtList[:]
            BaseImgList         = self.AnnotationImgList[:]    

        if SIZE_FILTERING is True:
            if RUN_CONDITION_FILTER is True:
                BaseWidthList   = self.ConditionWidthList[:]
                BaseHeightList  = self.ConditionHeightList[:]
            else:
                BaseWidthList   = self.AnalysisSrcWidthList[:]
                BaseHeightList  = self.AnalysisSrcHeightList[:]

        TotalIdxList    = [ i for i in range(len(BaseAnnotationList)) ]
        ExtractIdxList  = sample(TotalIdxList, self.ExtractCount)

        for eachIdx in ExtractIdxList:
            ExtractCountTxtList.append(BaseAnnotationList[eachIdx])
            ExtractCountImgList.append(BaseImgList[eachIdx])

        if SIZE_FILTERING is True:
            for eachIdx in ExtractIdxList:
                ExtractCountWidthList.append(BaseWidthList[eachIdx])
                ExtractCountHeightList.append(BaseHeightList[eachIdx])

            self.ConditionWidthList     = ExtractCountWidthList
            self.ConditionHeightList    = ExtractCountHeightList  

        self.ConditionResTxtList = ExtractCountTxtList
        self.ConditionResImgList = ExtractCountImgList

        self.checkFilterObjectSum()
        SuccessLog(f'RunExtractLimitCount Finish : {self.ExtractCount}')


    def RunAnalysisFilteredSize(self):
        widthArray = np.array(self.ConditionWidthList)
        heightArray = np.array(self.ConditionHeightList)

        widthAvg    = np.mean(widthArray)
        heightAvg   = np.mean(heightArray)

        print()
        showLog('# [ SIZE ANALYSIS ]')
        showLog('--------------------------------------------------------------------------------------')
        showLog(f'- Filter Condition : {FILTER_CONDITION}')
        showLog(f'- Size Condition   : {summaryFilterDict(SIZE_FILTERING_DICT)}')
        showLog('--------------------------------------------------------------------------------------')
        showLog(f'- Avgarge Width    : {round(widthAvg,2)}')
        showLog(f'- Avgarge Height   : {round(heightAvg,2)}')
        showLog(f'- Avgarge Szie     : {round(widthAvg*heightAvg,2)}')
        showLog('--------------------------------------------------------------------------------------')
        print()


    def pretreatmentSaveFilteredImgSizeCheckFile(self):
        for idx, eachWidth in enumerate(self.ConditionWidthList):
            self.SaveImgSizeList.append(f'{self.ConditionResImgList[idx]} [ {eachWidth:3} X {self.ConditionHeightList[idx]:3} ]')


    def saveResult(self):
        if self.ConditionResTxtList:
            self.SaveFilterResult()
        else:
            error_handling('Result Empty!', filename(), lineNum())


    def run(self):
        if self.selectUi.isSelectDone is False:
            NoticeLog(f'{self.__class__.__name__} Program EXIT\n')

        else:
            if RUN_CONDITION_FILTER is True:
                self.RunFilterCondition()

            if RUN_SHUFFLE_FILE is True:
                self.RunShuffle()

            if RUN_LIMIT_COUNT is True:
                self.RunExtractLimitCount()

            if SIZE_FILTERING:
                self.RunAnalysisFilteredSize()

            self.saveResult()

            self.showResult()
            self.saveResultByExcel()

            os.startfile(self.ResultDirPath)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    RunProgram = FilterCondition(App)
    RunProgram.run()
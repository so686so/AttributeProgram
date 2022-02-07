"""
makeClass 결과 나온 annotation / imgList txt를 가지고 필터링하는 프로그램

LAST_UPDATE : 2022/02/07
AUTHOR      : SHY
"""


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from    random                  import sample, shuffle
import  os
import  sys
import  copy
import  re


# INSTALLED PACKAGE IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import pandas                   as pd
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
from Core.SingletonClass        import Singleton

# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from UI.SelectUI.SelectUIClass  import *


# SOURCE & DEST PATH
# 해당 OriginXmlDirPath 과 ResultDirPath 값을 변경하고 싶으면, CoreDefine.py 에서 변경하면 됨! ( 경로 변경 통합 )
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
AnnotationFile      = copy.copy(OriginSource_AnntationPath)
ImgListFile         = copy.copy(OriginSource_ImageListPath)
AnalysisSourcePath  = copy.copy(OriginSource_AnalysisPath)
ResultDirPath       = copy.copy(Result_Dir_Path)

encodingFormat      = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat      = copy.copy(VALID_IMG_FORMAT)


# 결과값 저장 파일 이름
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
SaveAnnotationFileName      = "Annotation.txt"
SaveImgFileName             = "ImgList.txt"

ConditionFilterPrefix       = "ConditionFilter"
FilteredImgAnalysisFileName = "Filtered_Img_Size_Result.txt"
FilterConditionResExcelName = "FilterCondition.xlsx"


# Define
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
RUN_CONDITION_FILTER        = False
RUN_SHUFFLE_FILE            = False
RUN_LIMIT_COUNT             = False
SIZE_FILTERING              = False


# CONDITION EXTRACT STRING
# 조건식 내 문자열은 항상 "" 로 작성
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
FILTER_CONDITION            = copy.copy(CORE_FILTER_CONDITION)
LIMIT_COUNT                 = 0


# SIZE_FILTERING DICT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
SIZE_FILTERING_DICT         = copy.copy(CORE_SIZE_FILTER_DICT)


# 파일 추출 클래스
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class FilterCondition(Singleton):
    def __init__(self, QApp):
        self.app                    = QApp
        self.ProgramName            = "Condition_Filter"

        self.TotalObjectSumList     = []    # 원본 파일 각 개체별 유효값 총합
        self.FilterObjectSumList    = []    # 추출 파일 각 객체별 유효값 총합

        self.AnnotationTxtList      = []    # 원본 어노테이션 파일 목록 한 줄씩 읽어 리스트에 저장
        self.AnnotationImgList      = []    # 원본 이미지 파일 목록 한 줄씩 읽어 리스트에 저장

        self.AnalysisSrcWidthList   = []    # 원본 분석재료 너비 리스트
        self.AnalysisSrcHeightList  = []    # 원본 분석재료 높이 리스트

        self.ConditionResTxtList    = []    # 결과값 리스트들 ...
        self.ConditionResImgList    = []
        self.ConditionWidthList     = []
        self.ConditionHeightList    = []
        self.SaveImgSizeList        = []    # ... 결과값 리스트들

        self.ExtractCount           = LIMIT_COUNT

        self.ClassNum               = 0     # 클래스 갯수
        self.classData              = None
        self.classNameList          = []

        self.sendArgsList           = []

        self.initializeCF()

    # initialize ConditionFilterClass
    def initializeCF(self):
        self.selectUi = SelectUI(self.setInitSettingForSelectUI, self.getEditSettingForSelectUI)

        self.selectUi.show()
        self.app.exec()

        if self.selectUi.isQuitProgram():
            return

        self.initAfterSetUI()
        self.setMode()


    def initAfterSetUI(self):
        self.classData = ExcelData()

        CheckExistFile(AnnotationFile)
        readFileToList(AnnotationFile, self.AnnotationTxtList, encodingFormat)

        if self.checkTotalObjectSum() is False:
            error_handling(f'checkTotalObjectSum() Faild', filename(), lineNum())

        CheckExistFile(ImgListFile)
        readFileToList(ImgListFile, self.AnnotationImgList, encodingFormat)

        self.countClassNum()
        self.classNameList = self.classData.getClassNameListByClassNum(self.ClassNum)

        if self.classNameList is None:
            error_handling('Load ClassName Failed', filename(), lineNum())

        if getZipClassNum() != self.ClassNum:
            error_handling(f'Class Mismatched! : Set Class [ {CGREEN}{getZipClassNum()}{CRESET} ] != File Class [ {CRED}{self.ClassNum}{CRESET} ]\n', filename(), lineNum())
            self.selectUi.showErrorMsgBox('Class Mismatch', f'Set Class [{getZipClassNum()}] != File Class [{self.ClassNum}]')
            sys.exit(-1)


    def setMode(self):
        if RUN_CONDITION_FILTER is True:
            ModeLog('CONDITION_FILTER ON')

        if SIZE_FILTERING is True:
            ModeLog('SIZE_FILTERING ON')
            CheckExistFile(AnalysisSourcePath)
            self.extractImgSizeSrcListByFile()

        if RUN_SHUFFLE_FILE is True:
            ModeLog('SHUFFLE_FILE ON')

        if RUN_LIMIT_COUNT is True:
            ModeLog('LIMIT_COUNT ON')


    def setInitSettingForSelectUI(self):
        """
            - AnnotationFile      
            - ImgListFile         
            - ResultDirPath       
        """
        self.SyncAllValue()
        self.sendArgsList = [   ['FD', 'AnnotationFile',            False,  f'{AnnotationFile}'],
                                ['FD', 'ImgListFile',               False,  f'{ImgListFile}'],
                                ['FD', 'ResultDirPath',             True,   f'{ResultDirPath}'],
                                ['FD', 'HLINE_2',                   False,  'None'],
                                ['FD', 'AnalysisSourcePath',        False,  f'{AnalysisSourcePath}'],

                                ['CB', 'RUN_CONDITION_FILTER',      False,  f'{RUN_CONDITION_FILTER}'],
                                ['CB', 'RUN_SHUFFLE_FILE',          False,  f'{RUN_SHUFFLE_FILE}'],
                                ['CB', 'RUN_LIMIT_COUNT',           False,  f'{RUN_LIMIT_COUNT}'],
                                ['CB', 'HLINE_3',                   False,  'None'],
                                ['CB', 'SIZE_FILTERING',            False,  f'{SIZE_FILTERING}'],

                                ['LE', 'SaveAnnotationFileName',    False,  f'{SaveAnnotationFileName}'],
                                ['LE', 'SaveImgFileName',           False,  f'{SaveImgFileName}'],
                                ['LE', 'ConditionFilterPrefix',     False,  f'{ConditionFilterPrefix}'],

                                ['LE', 'HLINE_0',                   False,  'None'],
                                ['LE', 'LIMIT_COUNT',               False,  f'{LIMIT_COUNT}'],
                                ['LE', 'HLINE_1',                   False,  'None'],
                                ['UI', 'FILTER_CONDITION',          False,  f'{FILTER_CONDITION}'],
                                ['UI',  'SIZE_FILTERING_DICT',      False,  SIZE_FILTERING_DICT],
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
        self.ExtractCount = int(LIMIT_COUNT)
        setResultDir(ResultDirPath)

    def SyncAllValue(self):
        self.SyncEachValue('OriginSource_AnntationPath',    'AnnotationFile')
        self.SyncEachValue('OriginSource_ImageListPath',    'ImgListFile')
        self.SyncEachValue('Result_Dir_Path',               'ResultDirPath')
        self.SyncEachValue('CORE_SIZE_FILTER_DICT',         'SIZE_FILTERING_DICT')
        self.SyncEachValue('CORE_FILTER_CONDITION',         'FILTER_CONDITION')

    def SyncEachValue(self, CoreName, LinkName, SENDER_DEPTH=3):
        # set 하기 전에 CoreDefine.py의 값을 get
        if callername(SENDER_DEPTH) == 'setInitSettingForSelectUI':
            globals()[LinkName] = getCoreValue(CoreName)

        elif callername(SENDER_DEPTH) == 'getEditSettingForSelectUI':
            setCoreValue(CoreName, globals()[LinkName])


    def countClassNum(self):
        # AnnotationTxtList 원본 불러오기 안 됐으면 바로 리턴 예외 처리
        if not self.AnnotationTxtList:
            error_handling(f"{AnnotationFile} has nothing annotation list", filename(), lineNum())
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
            error_handling(f"{AnnotationFile} has nothing annotation list", filename(), lineNum())
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

        filterObjectSumList = [ 0 for _ in range(self.ClassNum) ]

        for each in self.ConditionResTxtList:
            for i in range(self.ClassNum):
                filterObjectSumList[i] += int(each[i])

        self.FilterObjectSumList = filterObjectSumList
        return True


    def extractImgSizeSrcListByFile(self):
        with open(AnalysisSourcePath, 'r', encoding=encodingFormat) as f:
            for eachLine in f:
                eachLine    = eachLine.strip('\n')
                splitLine   = eachLine.split(sep=' ')
                self.AnalysisSrcWidthList.append(int(splitLine[WIDTH]))
                self.AnalysisSrcHeightList.append(int(splitLine[HEIGHT]))

        SuccessLog(f"ImageSize Analysis Source File Read Done << {AnalysisSourcePath}")            


    def showResult(self):
        DF_HeadString   = "  ClassIdx  |  ClassName      |  TotalSum        "
        FT_HeadString   = ""

        DF_Line         = ""
        FT_Line         = ""

        FT_EachPercent  = 0

        printLine       = '------------------------------------------------'

        if RUN_CONDITION_FILTER is True or RUN_LIMIT_COUNT is True:
            FT_HeadString   = "|  ResultSum       |  %        "
            printLine       += "------------------------------"

        HeadString      = f'{DF_HeadString}{FT_HeadString}'

        print()
        print(printLine)
        print(HeadString)
        print(printLine)

        FilterMetaList  = re.findall('\d+', FILTER_CONDITION)
        FilterIdxList   = [ int(eachOdd) for idx, eachOdd in enumerate(FilterMetaList) if idx % 2 == 0 ]
        FilterBoolList  = [ int(eachEvn) for idx, eachEvn in enumerate(FilterMetaList) if idx % 2 == 1 ]

        for i in range(self.ClassNum):
            FilteredMark    = ""
            FilteredColor   = ""

            if RUN_CONDITION_FILTER is True or RUN_LIMIT_COUNT is True:
                # To Evade ExceptDevideZero
                if self.TotalObjectSumList[i] != 0:
                    FT_EachPercent = (self.FilterObjectSumList[i] / self.TotalObjectSumList[i]) * 100
                else:
                    FT_EachPercent = 0
                FT_Line = f'|  {self.FilterObjectSumList[i]:<16}|  {round(FT_EachPercent, 2):>6}%  '

            if RUN_CONDITION_FILTER and i in FilterIdxList:
                index = FilterIdxList.index(i)
                if FilterBoolList[index] == 0:
                    FilteredColor   = f"{CRED}"
                    FilteredMark    = f"\t-{CRESET}"
                else:
                    FilteredColor   = f"{CGREEN}"
                    FilteredMark    = f"\t+{CRESET}"

            DF_Line = f'  {i:<10}|  {self.classNameList[i]:<15}|  {self.TotalObjectSumList[i]:<16}'

            print(f'{FilteredColor}{DF_Line}{FT_Line}{FilteredMark}')

        print(printLine)
        print()

        showLog(f"* Origin File Count\t: {len(self.AnnotationTxtList)}")
        showLog(f"* File Shuffled\t\t: {RUN_SHUFFLE_FILE}")

        if RUN_CONDITION_FILTER:
            showLog(f'* Extract Condition\t: {self.selectUi.getTransMsgFilter()}')
        if SIZE_FILTERING:
            showLog(f'* FilterSize Condition\t: {summaryFilterDict(SIZE_FILTERING_DICT)}')
        if RUN_LIMIT_COUNT:
            showLog(f'* Extract Count\t\t: {LIMIT_COUNT}')

        showLog(f"* Result File Count\t: {len(self.ConditionResTxtList)}")
        print()

    
    def saveResultByExcel(self):
        classNameList = self.classNameList

        raw_data =  {   'ClassName':classNameList,
                        'TotalSum':self.TotalObjectSumList
                    }

        if RUN_CONDITION_FILTER:
            raw_data['FilterSum'] = self.FilterObjectSumList

        raw_data = pd.DataFrame(raw_data)
        savePath = os.path.join(ResultDirPath, FilterConditionResExcelName)
        raw_data.to_excel(excel_writer=savePath)

        SuccessLog(f'RandomExtract Summary Log Save to Excel File >> {savePath}')


    def SaveFilterResult(self):
        ConditionAnnoSavePath       = os.path.join(ResultDirPath, f'{ConditionFilterPrefix}_{SaveAnnotationFileName}')
        ConditionImgSavePath        = os.path.join(ResultDirPath, f'{ConditionFilterPrefix}_{SaveImgFileName}')

        if RUN_LIMIT_COUNT:
            ConditionAnnoSavePath   = os.path.join(ResultDirPath, f'{ConditionFilterPrefix}_{self.ExtractCount}Count_{SaveAnnotationFileName}')
            ConditionImgSavePath    = os.path.join(ResultDirPath, f'{ConditionFilterPrefix}_{self.ExtractCount}Count_{SaveImgFileName}')

        writeListToFile(ConditionAnnoSavePath,  self.ConditionResTxtList,   encodingFormat)
        writeListToFile(ConditionImgSavePath,   self.ConditionResImgList,   encodingFormat)

        if SIZE_FILTERING:
            FilteredSizeSavePath = os.path.join(ResultDirPath, FilteredImgAnalysisFileName)
            self.pretreatmentSaveFilteredImgSizeCheckFile()
            writeListToFile(FilteredSizeSavePath, self.SaveImgSizeList, encodingFormat)


    def RunFilterCondition(self):
        BaseAnnotationList          = []
        BaseImgList                 = []

        BaseAnnotationList          = self.AnnotationTxtList[:]
        BaseImgList                 = self.AnnotationImgList[:]

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
            ConditionAnnotationList,    \
            ConditionImgList,           \
            ConditionWidthList,         \
            ConditionHeightList         = self.subRunFilter(    ConditionAnnotationList,    \
                                                                ConditionImgList,           \
                                                                ConditionWidthList,         \
                                                                ConditionHeightList         \
                                                            )

        self.ConditionResTxtList = ConditionAnnotationList
        self.ConditionResImgList = ConditionImgList
        self.ConditionWidthList  = ConditionWidthList
        self.ConditionHeightList = ConditionHeightList

        self.checkFilterObjectSum()


    def subRunFilter(self, annList, imgList, widList, hgtList):
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
            for Idx, Attribute in enumerate(annList):
                Size = widList[Idx] * hgtList[Idx]
                if Size >= CondSize:
                    TempAnnList.append(Attribute)
                    TempImgList.append(imgList[Idx])
                    TempWidList.append(widList[Idx])
                    TempHghList.append(hgtList[Idx])
        else:
            for Idx, Attribute in enumerate(annList):
                if  (widList[Idx] >= CondWidth) and \
                    (hgtList[Idx] >= CondHeight):
                    TempAnnList.append(Attribute)
                    TempImgList.append(imgList[Idx])
                    TempWidList.append(widList[Idx])
                    TempHghList.append(hgtList[Idx])

        return TempAnnList, TempImgList, TempWidList, TempHghList


    def getBaseList(self):
        TempAnnList         = []
        TempImgList         = []
        TempWidList         = []
        TempHghList         = []

        if RUN_CONDITION_FILTER is True:
            TempAnnList     = self.ConditionResTxtList[:]
            TempImgList     = self.ConditionResImgList[:]
        else:
            TempAnnList     = self.AnnotationTxtList[:]
            TempImgList     = self.AnnotationImgList[:]

        if SIZE_FILTERING is True:
            if RUN_CONDITION_FILTER is True:
                TempWidList = self.ConditionWidthList[:]
                TempHghList = self.ConditionHeightList[:]
            else:
                TempWidList = self.AnalysisSrcWidthList[:]
                TempHghList = self.AnalysisSrcHeightList[:]

        return TempAnnList, TempImgList, TempWidList, TempHghList


    def RunShuffle(self):
        BaseAnnList, BaseImgList, BaseWidthList, BaseHeightList = self.getBaseList()

        ShuffleAnnList  = []
        ShuffleImgList  = []
        ShuffleWidList  = []
        ShuffleHgtList  = []        

        baseTotalCount  = len(BaseAnnList)
        baseIdxList     = [ i for i in range(baseTotalCount) ]
        shuffle(baseIdxList)

        for eachIdx in range(baseTotalCount):
            ShuffleAnnList.append(BaseAnnList[baseIdxList[eachIdx]])
            ShuffleImgList.append(BaseImgList[baseIdxList[eachIdx]])

        if SIZE_FILTERING is True:
            for eachIdx in range(baseTotalCount):
                ShuffleWidList.append(BaseWidthList[baseIdxList[eachIdx]])
                ShuffleHgtList.append(BaseHeightList[baseIdxList[eachIdx]])

            self.ConditionWidthList     = ShuffleWidList
            self.ConditionHeightList    = ShuffleHgtList           

        self.ConditionResTxtList = ShuffleAnnList
        self.ConditionResImgList = ShuffleImgList
        SuccessLog('Shuffling Done')
            

    def RunExtractLimitCount(self):
        BaseAnnList, BaseImgList, BaseWidthList, BaseHeightList = self.getBaseList()

        ExtractCountTxtList     = []
        ExtractCountImgList     = []
        ExtractCountWidthList   = []
        ExtractCountHeightList  = []
        TotalIdxList            = [ i for i in range(len(BaseAnnList)) ]

        self.CheckEnoughListSizeToSample(len(TotalIdxList), self.ExtractCount)
        ExtractIdxList          = sample(TotalIdxList, self.ExtractCount)

        for eachIdx in ExtractIdxList:
            ExtractCountTxtList.append(BaseAnnList[eachIdx])
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


    def CheckEnoughListSizeToSample(self, ListCount, SampleCount):
        if SampleCount > ListCount:
            error_handling('Not Enough Image Count to Limit Cut!', filename(), lineNum())
            exit(-1)


    def RunAnalysisFilteredSize(self):
        widthArray  = np.array(self.ConditionWidthList)
        heightArray = np.array(self.ConditionHeightList)
        widthAvg    = np.mean(widthArray)
        heightAvg   = np.mean(heightArray)
        AreaAvg     = np.mean(np.multiply(widthAvg, heightArray))

        def showLog_n_SaveList(Msg):
            showLog(Msg)
            self.SaveImgSizeList.append(Msg)

        print()
        showLog_n_SaveList('# [ SIZE ANALYSIS ]')
        showLog_n_SaveList('--------------------------------------------------------------------------------------')
        if RUN_CONDITION_FILTER:
            showLog_n_SaveList(f'- Filter Condition : {self.selectUi.getTransMsgFilter()}')
        if SIZE_FILTERING:
            showLog_n_SaveList(f'- Size Condition   : {summaryFilterDict(SIZE_FILTERING_DICT)}')
        showLog_n_SaveList('--------------------------------------------------------------------------------------')
        showLog_n_SaveList(f'- Avgarge Width    : {round(widthAvg,2)}')
        showLog_n_SaveList(f'- Avgarge Height   : {round(heightAvg,2)}')
        showLog_n_SaveList(f'- Avgarge Szie     : {round(AreaAvg,2)}')
        showLog_n_SaveList('--------------------------------------------------------------------------------------')
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
        if self.selectUi.isQuitProgram():
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

            os.startfile(ResultDirPath)


if __name__ == "__main__":
    App         = QApplication(sys.argv)
    RunProgram  = FilterCondition(App)
    RunProgram.run()
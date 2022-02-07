"""
Class code that reads, stores, and processes data for MakeClass in an Excel file

Need Installed Package :
    - pandas
    - openpyxl

LAST_UPDATE : 2022/02/07
AUTHOR      : SHY
"""

# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# None


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from CoreDefine             import *


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.CommonUse         import *
from Core.SingletonClass    import Singleton


# INSTALLED PACKAGE IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import pandas               as pd


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
DEFAULT_CLASS_NUM           = 83
MAKECLASS_MAX_CNT           = 2

DELETE_VALUE_ZIP_CLASS      = 1
DELETE_LIST_ZIP_CLASS_IDX   = 0

FIX_HAT_ANNOTATE_ERROR      = True
HATLESS_IDX                 = 29
EQUIPED_HAT_START_IDX       = 31
EQUIPED_HAT_END_IDX         = 41


# ExcelData Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class ExcelData(Singleton):
    """
    pandas 를 이용해서 Excel 내부 ClassData 와 MergeData 를 읽고 처리하는 클래스

    Attributes :
        df_ClassData : ClassData Sheet Read Data (type : frame data)
        df_MergeData : MergeData Sheet Read Data (type : frame data)

        IdxDict : Attribute 값과 83Class의 idx 값을 매칭시킨 Dict
            - key   : 'Attribute.get('name')/Attribute.text' (type : str)
            - value : 83Class Index (type : int)

        mergeDict : 
            ClassData Sheet 에서 mergedIdx 값에 따른
            MergeData Sheet 의 실제 mergeIdx 값을 매칭시킨 Dict
            mergedIdx 가 1, 2.. 일 때 Zip Class 에서 실제 어떤 Idx 값으로 Merge 되는지
            - key   : ClassData Sheet - mergedIdx (type : int)
            - value : MergeData Sheet - [mergeIdx_zip] (type : list)
        mergeList :
            ClassData Sheet 에서 어떤 Idx 들이 Merge 되는지를 리스트화 (type : 2D list)
            mergedIdx = 1 일때, mergeList[0] 에 append
            mergedIdx = 2 일때, mergeList[1] 에 append  <- mergedIdx = 0 은 Not Merge 이므로 한칸씩 당겨서 기입
            // Zip 단일 클래스화로 변경함 -> 클래스 별 압축 규칙이 없어서 알고리즘 못짬;

        unknownList :
            unknownDeleted 값이 1인 idx 들을 저장하는 List
            MakeClass Zip 할 때 해당 idx 들은 삭제

        deleteList :
            ClassData Sheet 에서 어떤 Idx 들이 Delete 되는지를 리스트화 (type : 2D list)
            isDeleted = 1 일때, deleteList[1], deleteList[0] 에 append
            isDeleted = 2 일때, deleteList[1] 에 append
            // Zip 단일 클래스화로 변경함 -> 클래스 별 압축 규칙이 없어서 알고리즘 못짬;

        defaultClassNameDict :
            - key   : Class Idx (type : int)
            - value : ClassName (type : str)

        # IMPORTANT! #
        MakeClassDefaultData :
            cvatXml 파일에서 하나의 Img 에 해당하는 Attribute List 를 인자값으로 받아,
            setMakeClassDefaultData() 를 통해 DefualtClass 에 해당하는 [0, 1, 0, 0, ...] List 생성
            getMakeClassDefaultData() 를 통해 해당 List 반환 
            (type : list, len : DEFAULT_CLASS_NUM(83))

    Methods:
        - checkDefaultClassNum()
        - pretreatmentMergeData()
        - pretreatmentClassData()
        - setValidValueByAttListElement(AttElem_AttName, AttElem_AttText)
        - refineMakeClass(ClassNum, makeClassDefaultList)
        - setMakeClassDefaultData(AttributeList)
        - getMakeClassDefaultData()
        - getClassNameDict()
    """

    def __init__(self):
        """
            pandas 의 read_excel 함수를 이용해서 classData.xlsx 의 시트들을 읽고,
            기초 전처리 및 에러 처리하는 init 부분
        """
        self.ExcelPath    = r""
        self.ZipClassNum  = 0

        self.syncValueBeforeInit()

        CheckExistFile(self.ExcelPath)

        self.df_ClassData = pd.read_excel(self.ExcelPath, sheet_name='ClassData')
        self.df_MergeData = pd.read_excel(self.ExcelPath, sheet_name='MergeData')
        self.df_NameData  = pd.read_excel(self.ExcelPath, sheet_name='NameData')
        self.df_CtgrData  = pd.read_excel(self.ExcelPath, sheet_name='CategoryData')

        self.IdxDict    = {}
        self.DataDict   = {}
        self.mergeDict  = {}
        self.mergeList  = []

        self.orginClassNameDict = {}
        self.zipClassNameDict   = {}

        self.unknownList    = []
        self.deleteList     = []

        self.MakeClassDefaultData  = [ 0 for _ in range(DEFAULT_CLASS_NUM) ]
        self.defaultClassNameDict  = {}
        self.categoryDict          = {} # ElementIdx - CategoryIdx
        self.categoryNameDict      = {} # CategoryIdx - CategoryName

        self.checkDefaultClassNum()

        self.pretreatmentMergeData()
        self.pretreatmentClassData()    # 위 두 개 순서 바뀌면 안됨 : mergeList 초기화, 할당 순서
        self.pretreatmentNameData()
        self.pretreatmentCategoryNameData()

        SuccessLog(f'ExcelData Set Done - \'{self.ExcelPath}\'')

    
    def syncValueBeforeInit(self):
        self.ExcelPath      = getCoreValue('CUR_ZIP_CLASS_XLSX')
        self.ZipClassNum    = getZipClassNum()


    def checkDefaultClassNum(self):
        """
            pd.read_excel 를 통해 읽어들인 데이터의 갯수가 83개가 맞는지 체크하는 함수
            ---------------------------------------------------------------------
            Raises  :
                DEFAULT_CLASS_NUM 으로 정의한 갯수와, 읽어들인 데이터의 갯수가 맞지 않는다면 
                error_handling 발생
            ---------------------------------------------------------------------
        """
        ReadClassNum = len(self.df_ClassData)
        if DEFAULT_CLASS_NUM != ReadClassNum:
            error_handling(f'Read Class Count Not {DEFAULT_CLASS_NUM} : {ReadClassNum}', filename(), lineNum())
            sys.exit(-1)


    def pretreatmentMergeData(self):
        """
            엑셀 파일 중 MergeData 시트에 해당하는 부분 전처리하는 함수
            mergeDict 와 mergeList 할당 및 초기화
        """
        MergeIdxNum = len(self.df_MergeData)

        TotalOriginList     = self.df_MergeData['originIdx'].tolist()
        TotalMergeList      = self.df_MergeData['mergeIdxZip'].tolist()

        for idx in range(0, MergeIdxNum):
            curOriginIdx    = TotalOriginList[idx]
            curMergeIdx     = TotalMergeList[idx]

            self.mergeDict[curOriginIdx] = curMergeIdx

        self.mergeList = [ [] for _ in range(0, MergeIdxNum) ]  # 각 merge 결과 값에 대해 여러 개의 merge 되는 값들이 존재하기 때문에 2D List 


    def pretreatmentNameData(self):
        """
            엑셀 파일 중 NameData 시트에 해당하는 부분 전처리하는 함수
        """
        TotalOrgNameList     = self.df_NameData['class83'].tolist()
        TotalZipNameList     = self.df_NameData['classZip'].tolist()

        for idx in range(DEFAULT_CLASS_NUM):
            self.orginClassNameDict[idx] = TotalOrgNameList[idx]
            self.zipClassNameDict[idx]   = TotalZipNameList[idx]


    def pretreatmentCategoryNameData(self):
        """
            엑셀 파일 중 CategoryData 시트에 해당하는 부분 전처리하는 함수
        """
        CategoryIdxNum      = len(self.df_CtgrData)
        TotalCtIdxList      = self.df_CtgrData['categoryIdx'].tolist()
        TotalCtNameList     = self.df_CtgrData['categoryName'].tolist()

        for idx in range(CategoryIdxNum):
            curCategoryIdx  = TotalCtIdxList[idx]
            curCategoryName = TotalCtNameList[idx]
            self.categoryNameDict[curCategoryIdx] = curCategoryName


    def pretreatmentClassData(self):
        """
            엑셀 파일 중 ClassData 시트에 해당하는 부분 전처리하는 함수
            deleteList 와 mergeList 할당
        """
        # Excel ClassData Sheet 한 줄씩 읽으면서 값 추출 -> 변경 : 미리 열(Column) 단위로 읽고 가져다쓰기
        TotalClassNameList  = self.df_ClassData['className'].tolist()
        TotalAttNameList    = self.df_ClassData['attName'].tolist()
        TotalAttTextList    = self.df_ClassData['attText'].tolist()
        TotalMergeIdxList   = self.df_ClassData['mergedIdx'].tolist()
        TotalIsDeleteList   = self.df_ClassData['isDeleted'].tolist()
        TotalUnKnownList    = self.df_ClassData['unknownDeleted'].tolist()
        TotalCategoryList   = self.df_ClassData['category'].tolist()

        # TotalList 원소들 하나씩 돌면서 적절히 집어넣기
        for idx in range(0, DEFAULT_CLASS_NUM):
            className       = TotalClassNameList[idx]
            curAttName      = TotalAttNameList[idx]
            curAttText      = TotalAttTextList[idx]
            curMergeIdx     = TotalMergeIdxList[idx]
            curIsDelete     = TotalIsDeleteList[idx]
            curUnKnown      = TotalUnKnownList[idx]
            curCategory     = TotalCategoryList[idx]

            if curMergeIdx > 0:
                # mergedIdx 가 1부터 시작하기 때문에(0은 Not Merge)
                # mergeList 에 추가할 때 한 칸씩 당겨서 append 해야 함
                self.mergeList[curMergeIdx-1].append(idx)

            if curIsDelete == DELETE_VALUE_ZIP_CLASS:
                self.deleteList.append(idx)

            if curUnKnown > 0:
                self.unknownList.append(idx)

            # Ex) self.categoryDict[28] = 5
            self.categoryDict[idx] = curCategory

            # IMPORTANT! : {curAttName}/{curAttText} 형태로 idxDict key-value 저장
            # Ex) self.IdxDict['hat/hood'] = 28
            self.IdxDict[f'{curAttName}/{curAttText}'] = idx

            # Ex) self.DataDict[hood] = [hat, hood]
            self.DataDict[className] = [curAttName, curAttText]

            # idx - className
            # Ex) self.defaultClassNameDict[28] = hood
            self.defaultClassNameDict[idx] = className


    def setValidValueByAttListElement(self, AttElem_AttName, AttElem_AttText):
        """
            Attribute "name" 과 "text" 를 받아서 해당 열 객체값 0/1 실제로 기입하는 함수
            ---------------------------------------------------------------------
            Args : 
                AttElem_AttName : Attribute.get('name') 값 (type : str)
                AttElem_AttText : Attribute.text 값 (type : str)
            Raises  :
                IdxDict 에 'AttElem_AttName/AttElem_AttText' 값이 없을 때
                ErrorLog 만 띄우고 종료는 하지 않음
            Returns :
                - 정상 작동 시 return True
                - Raises 상황 시 return False
            ---------------------------------------------------------------------
        """
        try:
            # Text 값이 "true" 일때 : true/false 값으로만 구성되어있는 AttText 라면 AttName 으로만 값 판별하는 Element
            if AttElem_AttText == "true":
                param = f'{AttElem_AttName}/None'                 # <attribute name="shoulderbag">true</attribute>

            # Attribute.text 값이 false 라면 어차피 해당 idx 값 0 이니까 그냥 바로 return
            elif AttElem_AttText == "false":                      # <attribute name="handbag">false</attribute>
                return True

            # 따로 AttText 존재하는 인자값이라면, 
            # self.IdxDict[f'{curAttName}/{curAttText}'] = idx 해둔 것 참조해서 0/1 기입!
            else:
                param = f'{AttElem_AttName}/{AttElem_AttText}'    # <attribute name="age">20~70</attribute>

            # 만약 AttElem_AttName/AttElem_AttText 조합이 IdxDict 에 없다면 여기서 오류 발생
            getIdx = self.IdxDict[param]

        except Exception as e:
            ErrorLog(f'{AttElem_AttName}/{AttElem_AttText} is Not Matched - {e}', lineNum=lineNum(), errorFileName=filename())
            return False

        self.MakeClassDefaultData[getIdx] = 1
        return True


    def refineMakeClass(self, ClassNum, makeClassDefaultList:list):
        """
            MakeClass 할 클래스 넘버값 받아서, MakeClassDefaultData 를 83 / zipped MakeClass 로 변환하는 함수
            ---------------------------------------------------------------------
            Args :
                ClassNum : MakeClass Num 값
                makeClassDefaultList : getMakeClassDefaultData() 값
                    - Type Example : [1, 0, 0, 0, 1, 1, ...]
                    - 해당 클래스가 아닌 다른 클래스에서도 refineMakeClass() 를 유연하게 사용하기 위함 
            Returns :
                - ClassOther_ResList or None
                - isUnknownDelete
            ---------------------------------------------------------------------
            Attributes :
                - ClassOther_ResList : return 하기 위한 ClassNum 길이의 0 값 List
                - curEditIdx : ClassOther_ResList 에서 현재 기입될 idx
                    - 해당 값과 makeClassDefaultList 의 idx 는 다른 값 : 클래스를 압축하기 때문에
                - isUnknownDelete : 
                    해당 값이 True 일 경우, 주어진 makeClassDefaultList 에 unknown 속성이 있기 때문에
                    결과적으로 해당 Annotation Line 은 삭제될 것
        """
        ClassOther_ResList  = [ 0 for _ in range(ClassNum) ]
        curEditIdx          = 0                                 # 얘가 makeClass로 만들어진 zipped Class 의 idx!
        isUnknownDelete     = False

        UNKNOWN_SHOES_IDX   = 82

        # refineClassNum == DEFAULT_CLASS_NUM 이라면 그대로 return
        if ClassNum == DEFAULT_CLASS_NUM:
            return makeClassDefaultList, isUnknownDelete
        # DEFAULT_CLASS_NUM 도 self.ZipClassNum 도 아니면 에러
        elif ClassNum != self.ZipClassNum:
            error_handling(f'{ClassNum} Class is Not Define', filename(), lineNum())
            return None, False

        mergeValueList      = list(self.mergeDict.values())

        for idx, eachValue in enumerate(makeClassDefaultList):    # makeClassDefaultList == MakeClassDefaultData [0, 1, 0, 0, 1, 0, 0, ...]
            # ClassData sheet -> unknownDeleted
            # if Unknwon Value == 1, return isUnknownDelete is True
            if idx in self.unknownList:
                # ! 하드 코딩 !
                # shoescolodrdk == 1 이어도, 이미지 삭제하지 말고 살리기
                if eachValue == 1 and idx != UNKNOWN_SHOES_IDX:
                    isUnknownDelete = True
                    # 하나라도 Unknown 값이 유효할 시, 바로 리턴시켜서 해당 행 삭제 <- 여기서 너무 많이 삭제될텐데?
                    return None, isUnknownDelete

            # ClassData sheet -> isDeleted
            # deleteList 내부에 있는 idx 값이라면 refine 된 MakeClass 에는 포함 안 됨 -> curEditIdx 증가 X (SKIP)
            if idx in self.deleteList:
                continue    # Not Increase ZipClass Idx(curEditIdx)

            # ClassData sheet -> mergedIdx : Merge된 idx로 예약이 되어있기 때문에, 해당 idx 넘김
            if curEditIdx in mergeValueList:
                curEditIdx += 1

            isMerged = False
            for mergeDictIdx, eachMergeList in enumerate(self.mergeList):
                if idx in eachMergeList:
                    # Merge 결과로 합쳐진 객체 IDX 자리
                    # Ex) Make39Class 에서 [08]nobackpack / [11]nocap 자리!
                    # mergeDictIdx +1 시키는 이유 : MergeIdx 0 은 Not Merge 에 할당되어 있어서, 유효 mergeDict key 1 부터 시작
                    # 비트 연산(or)으로 계산하는 이유 : Merge 되는 값들 중 하나라도 1 일 때, Merge 된 값이 1 이어야 해서
                    mergedResIdx    = self.mergeDict[mergeDictIdx+1]
                    preValue        = ClassOther_ResList[mergedResIdx]
                    ClassOther_ResList[mergedResIdx] = ( preValue | eachValue )
                    isMerged        = True  # Not Increase ZipClass Idx(curEditIdx)

            # Merge 시켰으면, curEditIdx 그대로 놔둬야 하기 때문에 continue : Delete와 비슷한 맥락
            if isMerged is True:
                continue

            # Merge / Delete 아닐 경우에만 신규 MakeClass Idx 인 curEditIdx 자리값에 값 기입하고, 다음 Idx 로 ++
            ClassOther_ResList[curEditIdx] = eachValue
            curEditIdx += 1

        return ClassOther_ResList, isUnknownDelete


    def setMakeClassDefaultData(self, attList:list):
        """
            cvatXml 파일에서 하나의 Img 에 해당하는 Attribute List 를 인자값으로 받아,
            DefualtClass 에 해당하는 [0, 1, 0, 0, ...] List 생성
            ---------------------------------------------------------------------
            Args : 
                attList : [ label, attName, attText ] 인자들의 리스트
            ---------------------------------------------------------------------
        """
        ATT_NAME_INDEX  = 1
        ATT_TEXT_INDEX  = 2

        # MakeClassDefaultData 초기화
        self.MakeClassDefaultData = [ 0 for _ in range(DEFAULT_CLASS_NUM) ]       

        # Attribute List 하나씩 돌면서 MakeClassDefaultData 에 set 시키기
        for AttElem in attList:
            # setValidValueByAttListElement() 함수의 return 값이 False 일 때 어떻게 할지.. 일단 PASS
            # 여기 아랫줄 함수에서 각 idx 별로 0/1 값 기입됨
            if not self.setValidValueByAttListElement(AttElem[ATT_NAME_INDEX], AttElem[ATT_TEXT_INDEX]):
                pass

        # FIX_HAT_ANNOTATE_ERROR 값이 참일 경우, Annotator 측 HatError 교정
        # Hatless 값이 1 인데도, Hat Color 중 하나에 체크가 되어있을 때 전부 다 0 값으로 수정
        if (FIX_HAT_ANNOTATE_ERROR is True) and (self.MakeClassDefaultData[HATLESS_IDX] == 1): # nohat(29) == 1 인데
            if sum(self.MakeClassDefaultData[EQUIPED_HAT_START_IDX:EQUIPED_HAT_END_IDX]) > 0:  # hatred ~ hatcolordk == 1 이면
                for i in range(EQUIPED_HAT_START_IDX, EQUIPED_HAT_END_IDX):                    # hatred ~ hatcolordk == 0 으로 고치기
                    self.MakeClassDefaultData[i] = 0


    def getMakeClassDefaultData(self):
        """
            return MakeClassDefaultData
            ---------------------------------------------------------------------
            Returns : 
                MakeClassDefaultData (type : list)
            ---------------------------------------------------------------------
            Example :
                [0, 1, 0, 0, 1, ...]
        """
        return self.MakeClassDefaultData

    
    def getClassNameDict(self):
        """
            return defaultClassNameDict
            ---------------------------------------------------------------------
            Returns : 
                defaultClassNameDict (type : dict)
            ---------------------------------------------------------------------
            Example :
                {0:'man', 1:'woman', ... 24:'cap', ...}
        """
        return self.defaultClassNameDict


    def getClassCategoryDict(self):
        return self.categoryDict


    def getCategoryNameDict(self):
        return self.categoryNameDict


    def getClassNameDictByClassNum(self, classNum):
        if classNum == DEFAULT_CLASS_NUM:
            return self.orginClassNameDict
        elif classNum == self.ZipClassNum:
            return self.zipClassNameDict
        else:
            return None

    def getClassNameListByClassNum(self, classNum):
        classNameList = []
        if classNum == DEFAULT_CLASS_NUM:
            for idx in range(DEFAULT_CLASS_NUM):
                classNameList.append(self.orginClassNameDict[idx])
        elif classNum == self.ZipClassNum:
            for idx in range(self.ZipClassNum):
                classNameList.append(self.zipClassNameDict[idx])        
        else:
            return None
        return classNameList


    def getClassDataTotal(self):
        return [self.zipClassNameDict,self.orginClassNameDict, self.DataDict]

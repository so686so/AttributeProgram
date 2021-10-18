"""
This python file creates annotation txt output of class 83/66/39 
using classData.xlsx file and xml / img file of the given path.

LAST UPDATE DATE : 21/10/11
MADE BY SHY
"""

# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import os
import xml.etree.ElementTree as ET
import sys

# INSTALLED IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import pandas as pd     # pip install pandas / openpyxl

# PATH
EXCEL_PATH = r"classData.xlsx"

# PATH DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
OriginXmlDirPath    = r"H:\Attributedata_download\PA_100K\cvatxmls"
ResultDirPath       = r"H:\Attributedata_download\PA_100K\dataset"

ErrorImgFilePath    = r"H:\Attributedata_download\PA_100K\CrushedImg.txt"


# DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
MAKE_83_CLASS = True
MAKE_66_CLASS = True
MAKE_39_CLASS = True

FIX_HAT_ANNOTATE_ERROR = True

# 0 : if Error, Exit (More Strict)
# 1 : if Error, Show Msg and Continue
ERROR_STRICT    = 1


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
DEFAULT_CLASS_NUM = 83
MAKECLASS_MAX_CNT = 2   # Start 0

DELETE_VALUE_66CLASS = 1
DELETE_VALUE_39CLASS = 2

DELETE_LIST_66CLASS_IDX = 0
DELETE_LIST_39CLASS_IDX = 1

HATLESS_IDX             = 29
EQUIPED_HAT_START_IDX   = 31
EQUIPED_HAT_END_IDX     = 41

# COLOR
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
cRed    = "\x1b[31m"
cYellow = "\x1b[33m"
cReset  = "\x1b[0m"


# Commonly Used Func
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def error_handling(errorMsg):
    if ERROR_STRICT == 0:
        errorLog(errorMsg)
        sys.exit(-1)
    elif ERROR_STRICT == 1:
        errorLog(errorMsg)

def errorLog(errorMsg):
    print(f"[ {cRed}Error{cReset} ] {errorMsg}")


def isTrue(Bool):
    if Bool == "false":
        return 0
    else:
        return 1

# classDataPandas Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class classDataPandas:
    def __init__(self):
        self.df_ClassData = pd.read_excel(EXCEL_PATH, sheet_name='ClassData')
        self.df_MergeData = pd.read_excel(EXCEL_PATH, sheet_name='MergeData')

        self.IdxDict = {}

        self.mergeDict = {}
        self.mergeList = []

        self.deleteList     = [[] for _ in range(0, MAKECLASS_MAX_CNT)]
        self.classDefault   = [ 0 for _ in range(DEFAULT_CLASS_NUM) ]

        self.unknownList = []

        self.getDefaultClassNum()
        self.pretreatmentMergeData()
        self.DefaultDataDict = self.pretreatmentClassData()



    def getDefaultClassNum(self):
        global DEFAULT_CLASS_NUM
        ClassNum = len(self.df_ClassData)
        if DEFAULT_CLASS_NUM != ClassNum:
            print(f"* Default Class Num Not 83 : {ClassNum}")
            DEFAULT_CLASS_NUM = ClassNum

    # 엑셀 파일 중 MergeData 시트에 해당하는 부분 전처리
    def pretreatmentMergeData(self):
        MergeIdxNum = len(self.df_MergeData)

        # 나중에 Merge 시킬 추가 MakeClass 생기면 여기도 조절해 적어야함!
        for idx in range(0, MergeIdxNum):
            curOriginIdx    = self.df_MergeData.loc[idx]['originIdx']
            curMerge66Idx   = self.df_MergeData.loc[idx]['mergeIdx_66']
            curMerge39Idx   = self.df_MergeData.loc[idx]['mergeIdx_39']
            self.mergeDict[curOriginIdx] = [curMerge66Idx, curMerge39Idx]

        self.mergeList = [[] for _ in range(0, MergeIdxNum)]

    # 엑셀 파일 중 ClassData 시트에 해당하는 부분 전처리
    def pretreatmentClassData(self):
        TotalDict = {}
        labelList = []

        preLabel = ""
        preAttName = ""

        curLabelDict = {}
        curAttTextDict = {}

        preLabel = self.df_ClassData.loc[0]['label']
        preAttName = self.df_ClassData.loc[0]['attName']

        for idx in range(0, DEFAULT_CLASS_NUM):
            curLabel    = self.df_ClassData.loc[idx]['label']
            curAttName  = self.df_ClassData.loc[idx]['attName']
            curAttText  = self.df_ClassData.loc[idx]['attText']
            curMergeIdx = self.df_ClassData.loc[idx]['mergedIdx']
            curIsDelete = self.df_ClassData.loc[idx]['isDeleted']
            curUnKnown  = self.df_ClassData.loc[idx]['unknownDeleted']

            # 나중에 Merge/Delete 시킬 추가 MakeClass 생기면 여기도 조절해 적어야함!
            if curMergeIdx > 0:
                self.mergeList[curMergeIdx-1].append(idx)

            if curIsDelete == DELETE_VALUE_66CLASS:
                # MakeClass66 에서 지워지는 값은 MakeClass39에서도 지워짐
                self.deleteList[DELETE_LIST_66CLASS_IDX].append(idx)
                self.deleteList[DELETE_LIST_39CLASS_IDX].append(idx)
            elif curIsDelete == DELETE_VALUE_39CLASS:
                self.deleteList[DELETE_LIST_39CLASS_IDX].append(idx)

            if curUnKnown > 0:
                self.unknownList.append(idx)


            # IMPORTANT! : {curAttName}/{curAttText} 형태로 idxDict key-value 저장
            self.IdxDict[f'{curAttName}/{curAttText}'] = idx

            # 여기부터 해당 함수 끝부분까지는 안 봐도 됨. 예비용 코드.
            # 엑셀 파일을 3중 Dict 형식으로 정리하는 코드.
            if preLabel != curLabel:
                labelList.append(preLabel)

                if curAttTextDict:
                    curLabelDict[preAttName] = curAttTextDict.copy()
                    curAttTextDict.clear()

                TotalDict[labelList[-1]] = curLabelDict.copy()
                curLabelDict.clear()

                preLabel = curLabel
                preAttName = curAttName

            elif preAttName != curAttName:
                if curAttTextDict:
                    curLabelDict[preAttName] = curAttTextDict.copy()
                    curAttTextDict.clear()

                preAttName = curAttName

            if curAttText == "None":
                if curAttTextDict:
                    curLabelDict[preAttName] = curAttTextDict.copy()
                    curAttTextDict.clear()
                curLabelDict[curAttName] = {curAttText:[curMergeIdx, curIsDelete]}
            else:
                curAttTextDict[curAttText] = [curMergeIdx, curIsDelete]

        if curAttTextDict:
            curLabelDict[preAttName] = curAttTextDict.copy()
            curAttTextDict.clear()

        labelList.append(preLabel)
        TotalDict[labelList[-1]] = curLabelDict.copy()

        return TotalDict


    # Attribute "name" 과 "text" 를 받아서 해당 열 객체값 0/1 실제로 기입하는 함수!
    def setValidValueByAttListElement(self, AttElem_AttName, AttElem_AttText):
        # Text 값이 "true" 일때 : true/false 값으로만 구성되어있는 AttName
        if AttElem_AttText == "true":
            param = f'{AttElem_AttName}/None'
            self.classDefault[self.IdxDict[param]] = 1
        # false 면 그냥 패스하고
        elif AttElem_AttText == "false":
            pass
        # 따로 AttName 존재하는 인자값이라면, 
        # self.IdxDict[f'{curAttName}/{curAttText}'] = idx 해둔 것 참조해서 0/1 기입!
        else:
            param = f'{AttElem_AttName}/{AttElem_AttText}'
            self.classDefault[self.IdxDict[param]] = 1


    # MakeClass 할 클래스 넘버값 받아서, 66 or 39 MakeClass 하는 부분
    # 차후 다른 MakeClass Num. 추가할거면, 여기도 수정해야함!
    def filterOtherClass(self, ClassNum):
        ClassOther_ResList = [ 0 for _ in range(ClassNum) ]
        curEditIdx = 0

        # 차후 다른 MakeClass Num. 추가할거면, 여기도 수정해야함!
        DeleteValue = DELETE_LIST_66CLASS_IDX if ClassNum == 66 else DELETE_LIST_39CLASS_IDX

        MergeValue      = DeleteValue
        mergeValueList  = [ each[MergeValue] for each in list(self.mergeDict.values()) ]

        for idx, eachValue in enumerate(self.classDefault):
            if idx in self.unknownList:
                if eachValue == 1:
                    return None, True

            # Delete
            if idx in self.deleteList[DeleteValue]:
                continue    # Not Increase 66/39Class Idx(curEditIdx)

            # Merge
            if curEditIdx in mergeValueList:
                curEditIdx += 1

            isMerged = False
            for mergeDictIdx, eachMergeList in enumerate(self.mergeList):
                if idx in eachMergeList:
                    # Merge 결과로 합쳐진 객체 IDX 자리
                    # Ex) Make39Class 에서 [08]nobackpack / [11]nocap 자리!
                    ClassOther_ResList[self.mergeDict[mergeDictIdx+1][MergeValue]] = ClassOther_ResList[self.mergeDict[mergeDictIdx+1][MergeValue]] | eachValue
                    isMerged = True # Not Increase 66/39Class Idx(curEditIdx)

            # Merge 시켰으면, curEditIdx 그대로 놔둬야 하기 때문에 continue : Delete와 비슷한 맥락
            if isMerged is True:
                continue

            # Merge / Delete 아닐 경우에만 신규 MakeClass Idx 인 curEditIdx 자리값에 값 기입하고, 다음 Idx 로 ++
            ClassOther_ResList[curEditIdx] = eachValue
            # Increase 66Class Idx
            curEditIdx += 1

        return ClassOther_ResList, False

    # DEFINE 값에 따라서, 83 / 66 / 39 CLASS를 만드는 부분
    def CalcOneImage(self, attList):
        # attList : [ label, attName, attText ] 인자들의 리스트
        ATT_NAME_INDEX = 1
        ATT_TEXT_INDEX = 2
        isFixHat = False

        self.classDefault = [ 0 for _ in range(DEFAULT_CLASS_NUM) ]

        for eachAtt in attList:
            self.setValidValueByAttListElement(eachAtt[ATT_NAME_INDEX], eachAtt[ATT_TEXT_INDEX])

        # FIX_HAT_ANNOTATE_ERROR
        if (FIX_HAT_ANNOTATE_ERROR is True) and (self.classDefault[HATLESS_IDX] == 1):
            if sum(self.classDefault[EQUIPED_HAT_START_IDX:EQUIPED_HAT_END_IDX]) > 0:
                isFixHat = True
                for i in range(EQUIPED_HAT_START_IDX, EQUIPED_HAT_END_IDX):
                    self.classDefault[i] = 0

        make83Class_Res = ""
        make66Class_Res = ""
        make39Class_Res = ""

        isUnknownDelete = False

        if MAKE_83_CLASS is True:
            for eachValue in self.classDefault:
                make83Class_Res += str(eachValue)

        if MAKE_66_CLASS is True:
            make66Class_PreRes, _ = self.filterOtherClass(66)
            for eachValue in make66Class_PreRes:
                make66Class_Res += str(eachValue)

        if MAKE_39_CLASS is True:
            make39Class_PreRes, isUnknownDelete = self.filterOtherClass(39)
            for eachValue in make39Class_PreRes:
                make39Class_Res += str(eachValue)

        return make83Class_Res, make66Class_Res, make39Class_Res, isFixHat, isUnknownDelete


# MakeClassSource Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class MakeClassSource:
    def __init__(self):
        # cvatXml 파일들 리스트
        self.cvatXmlList = []
        # MakeClass 가 실패한 목록들 출력하기 위한 List
        self.MakeClassFailList = []

        # 실패 목록들
        self.TotalDropMissingImg = 0
        self.TotalDropLabelCount4 = 0
        self.TotalDropLabelNested = 0
        self.TotalDropMoreBag = 0
        self.TotalDropMakeClassFailed = 0

        # ClassData.xlsx 파일에서 클래스 데이터 읽어 처리하는 클래스
        self.ClassData = classDataPandas()

        # 결과값들 저장할 리스트
        self.Result83ClassList = []
        self.Result66ClassList = []
        self.Result39ClassList = []
        self.ResultImgNameList = []
        self.ResultDeleteUnknownList = []

        self.CrushedImgList = []

        self.initProgram()


    def initProgram(self):
        self.cvatXmlList = self.extract_cvatXmlList()

        if not self.cvatXmlList:
            sys.exit(-1)

        with open(ErrorImgFilePath, 'r', encoding='utf-8') as f:
            for eachLine in f:
                eachLine = eachLine.strip('\n')
                self.CrushedImgList.append(eachLine)


    def isBagMoreThanTwo(self, boxList):
        isMoreBag = False

        bagList = ["unknown_bag", "plasticbag", "shoulderbag", "handbag", "backpack"]
        bagCount = 0

        for box in boxList:
            label = box.get("label")
            if label == "all":
                for att in box.findall("attribute"):
                    if att.get("name") in bagList:
                        bagCount += isTrue(att.text)

        if bagCount >= 2:
            isMoreBag = True

        return isMoreBag


    # XML 파일별로 MakeClass 하는 함수
    def MakeClassByFile(self, XmlPath):
        FullXmlPath = os.path.join(OriginXmlDirPath, XmlPath)
        tree = ET.parse(FullXmlPath)
        note = tree.getroot()

        noteImage = note.findall("image")
        totalImgCount = len(noteImage)

        print(f"* [{FullXmlPath}] - Unfiltered Image Count {totalImgCount}")

        DropLabelCount4 = 0
        DropLabelNested = 0
        DropMissingImg  = 0
        DropMoreBag     = 0
        DropMakeClassFailed = 0
        CorrectRunCount = 0

        for eachImage in noteImage:
            imgName  = eachImage.get("name")
            boxValue = eachImage.findall("box")
            boxLabelList = []

            if not imgName:
                DropMissingImg += 1
                continue

            if len(boxValue) != 4:
                DropLabelCount4 += 1
                continue

            for box in boxValue:
                boxLabelList.append(box.get("label"))

            if len(set(boxLabelList)) != 4:
                DropLabelNested += 1
                continue

            if self.isBagMoreThanTwo(boxValue) is True:
                DropMoreBag += 1
                continue

            if imgName in self.CrushedImgList:
                print(f"\x1b[32[ CrushedImg PASS!!\x1b[0m - {imgName}")
                continue

            sendAttList = []
            for box in boxValue:
                for att in box.findall('attribute'):
                    sendAttList.append([box.get("label"), att.get("name"), att.text])

            isFixHat = False
            isUnknownDelete = False
            res83Class, res66Class, res39Class, isFixHat, isUnknownDelete = self.ClassData.CalcOneImage(sendAttList)

            if isFixHat is True:
                print(f"* {cYellow}FIX{cReset} : FIX_HAT_ANNOTATE_ERROR -> {imgName}")

            if (res83Class == "") and (res66Class == "") and (res39Class == ""):
                DropMakeClassFailed += 1
                self.MakeClassFailList.append(imgName)
                continue

            if MAKE_83_CLASS is True:
                self.Result83ClassList.append(res83Class)

            if MAKE_66_CLASS is True:
                self.Result66ClassList.append(res66Class)

            if MAKE_39_CLASS is True and isUnknownDelete is False:
                self.Result39ClassList.append(res39Class)

            self.ResultImgNameList.append(imgName)
            if isUnknownDelete is False:
                self.ResultDeleteUnknownList.append(imgName)
            
            CorrectRunCount += 1

        print(f"* [{FullXmlPath}] - Done")
        print(f"- Missing Image Name : {DropMissingImg}")
        print(f"- Label Count Not Matched : {DropLabelCount4}")
        print(f"- Label Nested : {DropLabelNested}")
        print(f"- More Than 2 Bag : {DropMoreBag}")
        print(f"- MakeClass Failed : {DropMakeClassFailed}")
        print(f"- MakeClass Successed : {CorrectRunCount}")
        print("--------------------------------------------------------------------------------------\n\n")

        self.TotalDropMissingImg        += DropMissingImg
        self.TotalDropLabelCount4       += DropLabelCount4
        self.TotalDropLabelNested       += DropLabelNested
        self.TotalDropMoreBag           += DropMoreBag
        self.TotalDropMakeClassFailed   += DropMakeClassFailed

        return totalImgCount, CorrectRunCount


    # 마지막에 저장하는 함수
    def saveMakeClassFile(self):
        if MAKE_83_CLASS is True:
            savePath = os.path.join(ResultDirPath, 'Annotation_83_Class.txt')
            with open(savePath, 'w') as f:
                for line in self.Result83ClassList:
                    f.write(f"{line}\n")
            print(f"* SAVE DONE make83Class : {savePath}")

        if MAKE_66_CLASS is True:
            savePath = os.path.join(ResultDirPath, 'Annotation_66_Class.txt')
            with open(savePath, 'w') as f:
                for line in self.Result66ClassList:
                    f.write(f"{line}\n")
            print(f"* SAVE DONE make66Class : {savePath}")

        if MAKE_39_CLASS is True:
            savePath = os.path.join(ResultDirPath, 'Annotation_39_Class.txt')
            with open(savePath, 'w') as f:
                for line in self.Result39ClassList:
                    f.write(f"{line}\n")
            print(f"* SAVE DONE make39Class : {savePath}")

        savePath = os.path.join(ResultDirPath, '83Class_ImgList.txt')
        with open(savePath, 'w') as f:
            for line in self.ResultImgNameList:
                f.write(f"{line}\n")
        print(f"* SAVE DONE ImageName List : {savePath}\n\n")   

        savePath = os.path.join(ResultDirPath, '39Class_ImgList.txt')
        with open(savePath, 'w') as f:
            for line in self.ResultDeleteUnknownList:
                f.write(f"{line}\n")
        print(f"* SAVE DONE DeleteUnknownImageName List : {savePath}\n\n")  


    def run(self):
        TotalRunImage = 0
        TotalCorrectImage = 0

        for idx, eachXmlPath in enumerate(self.cvatXmlList):
            print(f"* [ \x1b[32m{idx+1:3}\x1b[0m / {len(self.cvatXmlList):3} ]")
            print("--------------------------------------------------------------------------------------")
            runImage, CorrectImage  = self.MakeClassByFile(eachXmlPath)
            TotalRunImage           += runImage
            TotalCorrectImage       += CorrectImage

        print(f"MakeClass Run Done... Save... {ResultDirPath}")
        self.saveMakeClassFile()

        print()
        print("# [ MAKECLASS DONE ] -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("# [ FAILS ]")
        print(f"- Total Missing Image Name : {self.TotalDropMissingImg}")
        print(f"- Total Label Count Not Matched : {self.TotalDropLabelCount4}")
        print(f"- Total Label Nested : {self.TotalDropLabelNested}")
        print(f"- Total More Than 2 Bag : {self.TotalDropMoreBag}")
        print(f"- Total MakeClass Failed : {self.TotalDropMakeClassFailed}")
        print("--------------------------------------------------------------------------------------")
        print("# [ INFO ]")
        print(f"- Total Run : {TotalRunImage}")
        print(f"- Correct Total : {TotalCorrectImage}")
        print("# [ MAKECLASS DONE ] -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")


    # OriginXmlDirPath 에서 cvatXml 파일들 리스트 추출하는 함수
    def extract_cvatXmlList(self):
        _cvatXmlList = []
        fileList     = os.listdir(OriginXmlDirPath)
        
        for eachFile in fileList:
            _, ext = os.path.splitext(eachFile)
            
            if ext != ".xml":
                error_handling(f"{eachFile} is Not XML")
            else:
                _cvatXmlList.append(eachFile)

        if not _cvatXmlList:
            error_handling("cvatXmlList is Empty")
            return None

        print()
        print(f"* Extract cvatXmlList Done : {len(_cvatXmlList)} Files\n")

        return _cvatXmlList
    

if __name__ == "__main__":
    Program = MakeClassSource()
    Program.run()
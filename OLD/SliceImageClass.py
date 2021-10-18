"""
This Python file is a code created to slice images in the given directory path 
into Common / Head / Upper / Lower images.

Set the USE_X value of the variable you want to slice to True,
Set the source directory path and result directory path.   

LAST UPDATE DATE : 21/10/11
MADE BY SHY
"""

# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import numpy as np
import os
import xml.etree.ElementTree as ET
import cv2
import sys
import time


# VARIABLE DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
USE_COMMON  = True
USE_HEAD    = False
USE_UPPER   = False
USE_LOWER   = False

# 0 : if Error, Exit (More Strict)
# 1 : if Error, Show Msg and Continue
ERROR_STRICT    = 1


# PATH DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
OriginImageDirPath  = r"H:\Attributedata_download\PA_100K\img2"
OriginXmlDirPath    = r"H:\Attributedata_download\PA_100K\cvatxmls"
ResultDirPath       = r"H:\Attributedata_download\PA_100K\dataset"

ErrorImgFilePath    = r"H:\Attributedata_download\PA_100K\CrushedImg.txt"

# COLOR
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
cRed    = "\x1b[31m"
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


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
	    n = np.fromfile(filename, dtype)
	    img = cv2.imdecode(n, flags)
	    return img
    except Exception as e:
        error_handling(f"imread() failed in {filename} - {e}")
        return None


def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                 n.tofile(f)
            return True
        else:
            errorLog(f"imwrite() failed in {filename} - cv2.imencode return(result) is None")
            return False
    except Exception as e:
        error_handling(f"imwrite() failed in {filename} - {e}")
        return False


def isTrue(Bool):
    if Bool == "false":
        return 0
    else:
        return 1


# Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class SliceImage:
    def __init__(self):
        # cvatXml 파일들 리스트
        self.cvatXmlList = []

        # 결과값 저장할 경로
        self.CommonImgDirPath    = ""
        self.HeadImgDirPath      = ""
        self.UpperImgDirPath     = ""
        self.LowerImgDirPath     = ""

        # getImgPath() 검색하기 위한 Dict
        self.OriginImgDict = {}
        self.TotalImageCount = 0
        # SliceImage 가 실패한 목록들 출력하기 위한 List
        self.SliceFailList = []

        # 실패 목록들
        self.TotalDropMissingImg = 0
        self.TotalDropLabelCount4 = 0
        self.TotalDropLabelNested = 0
        self.TotalDropMoreBag = 0
        self.TotalDropSliceFailed = 0

        self.useCount   = 0
        self.TotalSize  = 0

        self.initProgram()


    def initProgram(self):
        # Make cvatXml List by OriginXmlDirPath
        self.cvatXmlList = self.extract_cvatXmlList()

        if not self.cvatXmlList:
            sys.exit(-1)

        # 각자 파일 경로들 넣어주기
        self.CommonImgDirPath, self.HeadImgDirPath, self.UpperImgDirPath, self.LowerImgDirPath = self.make_dir_for_slice_img()
        self.getUseCount()

        # Get Origin Image Data as Dict - ImgFileName:RootPath
        self.getOriginImgDataDict()
        self.TotalImageCount = len(self.OriginImgDict)


    def run(self):
        TotalRunImage = 0
        TotalCorrectImage = 0

        startTime = time.time()

        for idx, eachXmlPath in enumerate(self.cvatXmlList):
            print(f"* [ \x1b[32m{idx+1:3}\x1b[0m / {len(self.cvatXmlList):3} ]")
            print("--------------------------------------------------------------------------------------")
            runImage, CorrectImage = self.SliceImgByXmlFile(eachXmlPath)
            midTime = time.time()

            TotalRunImage += runImage
            TotalCorrectImage += CorrectImage

            elapsedTime = midTime - startTime
            processing_efficiency = (TotalRunImage * self.useCount) / elapsedTime

            print(f"# Copy throughput per Sec : {round(processing_efficiency, 2)} files/Sec\n")

        endTime = time.time()
        total_elapsedTime = endTime - startTime
        total_processing_efficiency = (TotalRunImage * self.useCount) / total_elapsedTime

        print()
        print("# [ SLICE DONE ] -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("# [ FAILS ]")
        print(f"- Total Missing Image Name : {self.TotalDropMissingImg}")
        print(f"- Total Label Count Not Matched : {self.TotalDropLabelCount4}")
        print(f"- Total Label Nested : {self.TotalDropLabelNested}")
        print(f"- Total More Than 2 Bag : {self.TotalDropMoreBag}")
        print(f"- Total Slice Failed : {self.TotalDropSliceFailed}")
        print("--------------------------------------------------------------------------------------")
        print("# [ INFO ]")
        print("- Use :", end="")
        self.printUseDir()
        print(f"- TotalRun : {self.TotalImageCount}")
        print(f"- Real Total Run : {TotalRunImage}")
        print(f"- Correct Total : {TotalCorrectImage}")
        print("--------------------------------------------------------------------------------------")
        print("# [ Performance ]")
        print(f"- Total Copy throughput per Sec : {round(total_processing_efficiency, 2)} files/Sec")
        print("# [ SLICE DONE ] -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")

        if self.SliceFailList:
            print("* [ FAIL LIST ] -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            for idx, eachName in enumerate(self.SliceFailList):
                print(f"[{idx:3}] {eachName}")
            print()

            with open(ErrorImgFilePath, 'w') as f:
                for line in self.SliceFailList:
                    f.write(f"{line}\n")

    def printUseDir(self):
        if USE_COMMON is True:
            print(" COMMON ", end="")
        if USE_HEAD is True:
            print(" HEAD ", end="")
        if USE_UPPER is True:
            print(" UPPER ", end="")
        if USE_LOWER is True:
            print(" LOWER ", end="")
        print()

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

        print(f"* Extract cvatXmlList Done : {len(_cvatXmlList)} Files")

        return _cvatXmlList


    # COMMON / HEAD / UPPER / LOWER 중 사용할 폴더 생성하는 함수
    def make_dir_for_slice_img(self):
        print("* Make Result Dir")
        _CommonResDir   = ""
        _HeadResDir     = ""
        _UpperResDir    = ""
        _LowerResDir    = ""

        def makeDirs(subPath):
            img_path = os.path.join(ResultDirPath, subPath)
            img_path = os.path.normpath(img_path)
            os.makedirs(img_path, exist_ok=True)
            print(f"\t- {subPath}\t: {img_path}")
            return img_path

        if USE_COMMON is True:
            _CommonResDir = makeDirs("common_images")
        if USE_HEAD is True:
            _HeadResDir = makeDirs("head_images")
        if USE_UPPER is True:
            _UpperResDir = makeDirs("upper_images")
        if USE_LOWER is True:
            _LowerResDir = makeDirs("lower_images")

        print()

        return _CommonResDir, _HeadResDir, _UpperResDir, _LowerResDir


    # getImgPath() 검색하기 위한 Dict 만드는 함수
    def getOriginImgDataDict(self):
        for root, _, files in os.walk(OriginImageDirPath):
            if len(files) > 0:
                for file_name in files:
                    self.OriginImgDict[file_name] = root


    # 주어진 imageName 이 OriginImageDirPath 내 파일에 있는 이미지인지, 있다면 어떤 경로인지 리턴하는 함수
    def getImgPath(self, imageName):
        for eachName in self.OriginImgDict.keys():
            if imageName == eachName:
                return os.path.join(self.OriginImgDict.pop(eachName), eachName)

        # If Match Anything
        error_handling(f"getImgPath() failed - {imageName} is Not Matched")
        return None


    def ImageCrop(self, source, box):
        xTopLeft     = int(float(box.get("xtl")))
        yTopLeft     = int(float(box.get("ytl")))
        xBottomRight = int(float(box.get("xbr")))
        yBottomRight = int(float(box.get("ybr")))

        return source[yTopLeft:yBottomRight, xTopLeft:xBottomRight]


    def getUseCount(self):
        res = 0
        if USE_COMMON is True:
            res += 1
        if USE_HEAD is True:
            res += 1
        if USE_UPPER is True:
            res += 1
        if USE_LOWER is True:
            res += 1
        self.useCount = res   

    # Label(Common, Head, Upper, Lower) 값에 따라서 이미지를 실제로 Slice 하는 함수 
    def SliceByLabel(self, ResDir, ImgName, box):
        imgPath = self.getImgPath(ImgName)

        if imgPath is None :
            return False

        img = imread(imgPath)

        if img is None :
            return False

        src = img.copy()
        croped = self.ImageCrop(src, box)
        imwrite(os.path.join(ResDir, ImgName), croped)

        return True

    # OneImgName 이 주어졌을 때, 각 이미지에 대해서 SliceByLabel 로 넘기는 함수
    def SliceOneImg(self, OneImgName, boxList):
        for box in boxList:
            label   = box.get("label")
            res     = True

            if (USE_COMMON is True) and (label=="all"):
                res = self.SliceByLabel(self.CommonImgDirPath, OneImgName, box)
            if (USE_HEAD is True) and (label=="head"):
                res = self.SliceByLabel(self.HeadImgDirPath, OneImgName, box)
            if (USE_UPPER is True) and (label=="upper"):
                res = self.SliceByLabel(self.UpperImgDirPath, OneImgName, box)
            if (USE_LOWER is True) and (label=="lower"):
                res = self.SliceByLabel(self.LowerImgDirPath, OneImgName, box)

            if res is False:
                return False

        del(self.OriginImgDict[OneImgName])
        return True


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

    # 하나의 Xml 파일을 읽어서 내부에 존재하는 Img 값들을 Slice 로 넘기는 함수
    def SliceImgByXmlFile(self, XmlPath):
        FullXmlPath = os.path.join(OriginXmlDirPath, XmlPath)
        tree = ET.parse(FullXmlPath)
        note = tree.getroot()

        noteImage = note.findall("image")

        totalImgCount       = len(noteImage)
        percentCalcCount    = totalImgCount / 10
        currentRunCount     = 1
        currentPercentCount = percentCalcCount

        print(f"* [{FullXmlPath}] - Unfiltered Image Count {totalImgCount}")

        DropLabelCount4 = 0
        DropLabelNested = 0
        DropMissingImg  = 0
        DropMoreBag     = 0
        DropSliceFailed = 0
        CorrectRunCount = 0

        for eachImage in noteImage:
            imgName  = eachImage.get("name")
            boxValue = eachImage.findall("box")
            boxLabelList = []

            if currentRunCount >= currentPercentCount:
                currentPercentCount += percentCalcCount
                print(f"\t-> {currentRunCount:6} / {totalImgCount:6}")
            currentRunCount += 1

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

            res = self.SliceOneImg(imgName, boxValue)

            if res is False:
                DropSliceFailed += 1
                self.SliceFailList.append(imgName)
                continue
            
            CorrectRunCount += 1

        print(f"* [{FullXmlPath}] - Done")
        print("--------------------------------------------------------------------------------------")
        print(f"- Missing Image Name : {DropMissingImg}")
        print(f"- Label Count Not Matched : {DropLabelCount4}")
        print(f"- Label Nested : {DropLabelNested}")
        print(f"- More Than 2 Bag : {DropMoreBag}")
        print(f"- Slice Failed : {DropSliceFailed}")
        print(f"- Copy Successed : {CorrectRunCount}")

        self.TotalDropMissingImg += DropMissingImg
        self.TotalDropLabelCount4 += DropLabelCount4
        self.TotalDropLabelNested += DropLabelNested
        self.TotalDropMoreBag += DropMoreBag
        self.TotalDropSliceFailed += DropSliceFailed

        return totalImgCount, CorrectRunCount


if __name__ == "__main__":
    Program = SliceImage()
    Program.run()
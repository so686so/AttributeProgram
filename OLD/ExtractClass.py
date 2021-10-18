"""
This python file is a code that extracts a random percentage 
from a given xml file and image path file.

Set the source file path to extract,
After setting the file name to save the result value,
Adjust the extraction manipulation parameters.

LAST UPDATE DATE : 21/10/11
MADE BY SHY
"""

from random import randint

# 추출할 원본 파일 경로
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
AnnotationPath  = r"C:\PythonHN\AttributeProgram\OLD/Annotation_39_Class.txt"
ImgPath         = r"C:\PythonHN\AttributeProgram\OLD/39Class_ImgList.txt"
encodingFormat  = 'utf-8'


# 결과값 저장 파일 이름
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
SaveAnnotationFileName  = "Result_Annotation.txt"
SaveImgFileName         = "Result_Img.txt"


# 추출 조작 변수값들 ----------- 조절해야함!
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
overCount       = 0    # 각 객체 유효값 합이 최소 overCount
ExtractPercent  = 90    # 몇 %나 원본에서 추출할지


# 파일 추출 클래스
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class RandomExtractPercent:
    def __init__(self):
        self.TotalObjectSumList     = []    # 원본 파일 각 개체별 유효값 총합
        self.ExtractObjectSumlist   = []    # 추출 파일 각 객체별 유효값 총합

        self.AnnotationTxtList      = []    # 원본 어노테이션 파일 목록 한 줄씩 읽어 리스트에 저장
        self.AnnotationImgList      = []    # 원본 이미지 파일 목록 한 줄씩 읽어 리스트에 저장

        self.ExtractRandomTxtList   = []    # 원본이미지에서 랜덤으로 추출한 리스트
        self.ExtractRandomIdxList   = []    # 유효값으로 추출됐을 때 해당 인덱스들 기억하기 위한 리스트

        self.ClassNum = 0   # 클래스 갯수
        self.TryCount = 1   # 재시도 횟수


    def countClassNum(self):
        # AnnotationTxtList 원본 불러오기 안 됐으면 바로 리턴 예외 처리
        if not self.AnnotationTxtList:
            print("* Error : 'countClassNum()' Failed - has none annotation list")
            return False

        # 이미 체크했다면 따로 체크 안함
        if self.ClassNum != 0:
            return True
        
        # 아직 체크 안했다면 체크하기
        self.ClassNum = len(self.AnnotationTxtList[0])
        print(f"* ClassNum : {self.ClassNum}")

        return True


    # 각 객체마다 overCount가 넘는지 체크
    def isOverCount(self, checkObjectSum):
        if checkObjectSum >= overCount:
            return True
        else:
            return False


    def checkTotalObjectSum(self):
        # AnnotationTxtList 원본 불러오기 안 됐으면 바로 리턴 예외 처리
        if not self.AnnotationTxtList:
            print("* Error : 'checkTotalObjectSum()' Failed - has none annotation list")
            return False

        # 클래스 갯수 아직 안 셌으면 세는 코드
        if self.countClassNum() is False:
            return False

        # 클래스 갯수만큼 동적 변수 할당
        for i in range(0, self.ClassNum):
            globals()[f'total_object_{i}th_sum'] = 0

        print(f"[ Run ] checkTotalObjectSum -> Total Calc Count : {len(self.AnnotationTxtList)}...", end="\t")
        
        # 각 객체별 총합 계산
        for each in self.AnnotationTxtList:
            for i in range(0, self.ClassNum):
                globals()[f'total_object_{i}th_sum'] += int(each[i])

        # 저장
        for i in range(0, self.ClassNum):
            self.TotalObjectSumList.append(globals()[f'total_object_{i}th_sum'])

        print("Done")
        return True


    def checkExtractObjectSum(self):
        # ExtractRandomTxtList 랜덤 추출 안 됐으면 바로 리턴 예외 처리
        if not self.ExtractRandomTxtList:
            print("* Error : 'checkExtractObjectSum()' Failed - has none extract random list")
            return False

        # 클래스 갯수 아직 안 셌으면 세는 코드
        if self.countClassNum() is False:
            return False

        # 클래스 갯수만큼 동적 변수 할당
        for i in range(0, self.ClassNum):
            globals()[f'extract_object_{i}th_sum'] = 0

        print(f"[ Run ] checkExtractObjectSum -> Total Calc Count : {len(self.ExtractRandomTxtList)}")
        
        # 각 객체별 총합 계산
        for each in self.ExtractRandomTxtList:
            for i in range(0, self.ClassNum):
                globals()[f'extract_object_{i}th_sum'] += int(each[i])

        # Define 한 overCount 미달인 객체 있는지 체크
        for i in range(0, self.ClassNum):
            res = globals()[f'extract_object_{i}th_sum']
            # 특정 객체가 overCount 수치를 넘지 못했을 경우 리턴 False
            if self.isOverCount(res) is False:
                print(f"\t> Fail - {i}th Object is Not Over {overCount} : {res}")
                return False

        # 만약 return Flase 안 되고 여기까지 내려왔다면 해당 객체 합 저장
        for i in range(0, self.ClassNum):
            self.ExtractObjectSumlist.append(globals()[f'extract_object_{i}th_sum'])

        return True


    def extractTxtListByFile(self):
        with open(AnnotationPath, 'r', encoding=encodingFormat) as f:
            for eachLine in f:
                eachLine = eachLine.strip('\n')
                self.AnnotationTxtList.append(eachLine)

        print(f"[ Annotation File Read Done - {AnnotationPath} ]")
        

    def extractImgListByFile(self):
        with open(ImgPath, 'r', encoding=encodingFormat) as f:
            for eachLine in f:
                eachLine = eachLine.strip('\n')
                self.AnnotationImgList.append(eachLine)

        print(f"[ Image File Read Done - {ImgPath} ]")


    def showResult(self):
        print()
        print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* Result *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        print("------------------------------------------------------------------------")
        print("ClassIdx        |  TotalSum        |  ExtractSum      |  %")
        print("------------------------------------------------------------------------")
        for i in range(0, self.ClassNum):
            idx = i+1
            if self.TotalObjectSumList[i] != 0:
                eachPercent = (self.ExtractObjectSumlist[i] / self.TotalObjectSumList[i]) * 100
            else:
                eachPercent = 0
            print(f"{idx:<16}|  {self.TotalObjectSumList[i]:<16}|  {self.ExtractObjectSumlist[i]:<16}|  {round(eachPercent, 2)}%")
        print("------------------------------------------------------------------------")
        print()

        extractRealPercent = (len(self.ExtractRandomTxtList) / len(self.AnnotationTxtList)) * 100
        print(f"* Condition\t\t: Extract {ExtractPercent}% ( eachSum >= {overCount} )")
        print(f"* Total Try\t\t: {self.TryCount}")
        print(f"* Origin File Count\t: {len(self.AnnotationTxtList)}")
        print(f"* Extract File Count\t: {len(self.ExtractRandomTxtList)} ( {round(extractRealPercent,2)}% )")
        print()

    
    def run(self):
        self.extractTxtListByFile()
        self.checkTotalObjectSum()

        while True:
            print()
            print(f"[{self.TryCount} Try] Select Correct List : Each ObjectSum over {overCount} [ Total File Count : {len(self.AnnotationTxtList)} ]")

            # Try 할때마다 일단 리셋
            self.ExtractRandomTxtList.clear()
            self.ExtractRandomIdxList.clear()
            
            randomNum = 0

            for Idx, eachTxt in enumerate(self.AnnotationTxtList):
                randomNum = randint(1, 100)
                if randomNum <= ExtractPercent: # 여기서 정한 %만큼 추출
                    self.ExtractRandomTxtList.append(eachTxt)
                    self.ExtractRandomIdxList.append(Idx)

            print("\t> Extract Done. Check...")
            if self.checkExtractObjectSum() is True:
                print("\t> Extract Success!\n")
                break

            self.TryCount += 1

        print(f"[ Save Annotation Txt File : {SaveAnnotationFileName}...", end='\t')
        with open(SaveAnnotationFileName, 'w') as f:
            for line in self.ExtractRandomTxtList:
                f.write(f"{line}\n")
        print("Done")

        self.extractImgListByFile()
        print(f"[ Save Annotation Img File : {SaveImgFileName}...", end='\t')
        with open(SaveImgFileName, 'w') as f:
            # ExtractRandomIdxList 에 append 된 Idx 만 AnnotationImgList 에서 추출해 기록 : 동일한 인덱스로 어노테이션과 이미지가 저장
            for eachIdx in self.ExtractRandomIdxList:
                f.write(f"{self.AnnotationImgList[eachIdx]}\n")
        print("Done")

        self.showResult()


if __name__ == "__main__":
    program = RandomExtractPercent()
    program.run()

import sys

Compare83ClassPath = r"C:\PythonHN\Data\Res\Annotation_83_Class.txt"
Compare66ClassPath = r""
Compare39ClassPath = r"C:\PythonHN\Data\Res\Annotation_39_Class.txt"
ImgListPath        = r"C:\PythonHN\Data\Res\OriginImgList.txt"
encodingFormat  = 'utf-8'

ImgList = []

def open83Class():
    _83ClassList = []
    with open(Compare83ClassPath, 'r', encoding=encodingFormat) as f:
        for eachLine in f:
            eachLine = eachLine.strip('\n')
            _83ClassList.append(eachLine)

    return _83ClassList


def open66Class():
    _66ClassList = []
    with open(Compare66ClassPath, 'r', encoding=encodingFormat) as f:
        for eachLine in f:
            eachLine = eachLine.strip('\n')
            _66ClassList.append(eachLine)

    return _66ClassList


def open39Class():
    _39ClassList = []
    with open(Compare39ClassPath, 'r', encoding=encodingFormat) as f:
        for eachLine in f:
            eachLine = eachLine.strip('\n')
            _39ClassList.append(eachLine)

    return _39ClassList


def openImgList():
    global ImgList
    with open(ImgListPath, 'r', encoding=encodingFormat) as f:
        for eachLine in f:
            eachLine = eachLine.strip('\n')
            ImgList.append(eachLine)

def Zip83To39(Class83Elem, idx):
    resList = [0 for _ in range(39)]
    res = ""

    resList[0] = int(Class83Elem[0])
    resList[1] = int(Class83Elem[1])
    # 83 - 2 DELETE
    resList[2] = int(Class83Elem[3])
    resList[3] = int(Class83Elem[4])
    resList[4] = int(Class83Elem[5])
    resList[5] = int(Class83Elem[6])
    resList[6] = int(Class83Elem[7])
    resList[7] = int(Class83Elem[8])
    # Merge
    resList[8] = int(Class83Elem[9]) | int(Class83Elem[10]) | int(Class83Elem[11])
    # 83 - 12 DELETE
    resList[9] = int(Class83Elem[13])
    # 83 - 14 DELETE
    # 83 - 15 DELETE
    # 83 - 16 DELETE
    # 83 - 17 DELETE
    # 83 - 18 DELETE
    # 83 - 19 DELETE
    # 83 - 20 DELETE
    # 83 - 21 DELETE
    # 83 - 22 DELETE
    # 83 - 23 DELETE
    resList[10] = int(Class83Elem[24])
    # Merge
    resList[11] = int(Class83Elem[25]) | int(Class83Elem[26]) | int(Class83Elem[27]) | int(Class83Elem[28])
    resList[12] = int(Class83Elem[29])
    # 83 - 30 DELETE
    # 83 - 31 DELETE
    # 83 - 32 DELETE
    # 83 - 33 DELETE
    # 83 - 34 DELETE
    # 83 - 35 DELETE
    # 83 - 36 DELETE
    # 83 - 37 DELETE
    # 83 - 38 DELETE
    # 83 - 39 DELETE
    # 83 - 40 DELETE
    resList[13] = int(Class83Elem[41])
    resList[14] = int(Class83Elem[42])
    # 83 - 43 DELETE
    # 83 - 44 DELETE
    resList[15] = int(Class83Elem[45])
    resList[16] = int(Class83Elem[46])
    # 83 - 47 DELETE
    resList[17] = int(Class83Elem[48])
    resList[18] = int(Class83Elem[49])
    resList[19] = int(Class83Elem[50])
    resList[20] = int(Class83Elem[51])
    resList[21] = int(Class83Elem[52])
    resList[22] = int(Class83Elem[53])
    resList[23] = int(Class83Elem[54])
    resList[24] = int(Class83Elem[55])
    resList[25] = int(Class83Elem[56])
    # 83 - 57 DELETE
    resList[26] = int(Class83Elem[58])
    resList[27] = int(Class83Elem[59])
    resList[28] = int(Class83Elem[60])
    resList[29] = int(Class83Elem[61])
    # 83 - 62 DELETE
    resList[30] = int(Class83Elem[63])
    resList[31] = int(Class83Elem[64])
    resList[32] = int(Class83Elem[65])
    resList[33] = int(Class83Elem[66])
    resList[34] = int(Class83Elem[67])
    resList[35] = int(Class83Elem[68])
    resList[36] = int(Class83Elem[69])
    resList[37] = int(Class83Elem[70])
    resList[38] = int(Class83Elem[71])
    # 83 - 72 DELETE
    # 83 - 73 DELETE
    # 83 - 74 DELETE
    # 83 - 75 DELETE
    # 83 - 76 DELETE
    # 83 - 77 DELETE
    # 83 - 78 DELETE
    # 83 - 79 DELETE
    # 83 - 80 DELETE
    # 83 - 81 DELETE
    # 83 - 72 DELETE

    overWriteGender = 0
    for i in range(0, 3):
        overWriteGender += int(Class83Elem[i])
    if overWriteGender > 1:
        print(f"GENDER ERROR! -> {ImgList[idx]}")    

    overWriteAge = 0
    for i in range(3, 8):
        overWriteAge += int(Class83Elem[i])
    if overWriteAge > 1:
        print(f"AGE ERROR! -> {ImgList[idx]}")

    ishat = 0
    for i in range(31, 41):
        ishat += int(Class83Elem[i])
    if int(Class83Elem[29]) == 1 and ishat > 0:
        print(f"HAT ERROR! -> {ImgList[idx]}")

    overWriteHair = 0
    for i in range(41, 44):
        overWriteHair += int(Class83Elem[i])
    if overWriteHair > 1:
        print(f"HAIR ERROR! -> {ImgList[idx]}")

    for each in resList:
        res += str(each)

    return res

if __name__ == "__main__":
    print("[COMPARE MAKE CLASS : HARD CODING..]")
    Comp83ClassList = open83Class()
    Comp39ClassList = open39Class()
    openImgList()

    if len(Comp39ClassList) != len(Comp83ClassList):
        print(f"* ERROR - EACH LENGTH DIFF! [ 83 : {len(Comp83ClassList)} != 39 : {len(Comp39ClassList)} ]")


    for idx, eachLine in enumerate(Comp83ClassList):
        compRes = Zip83To39(eachLine, idx)
        if compRes != Comp39ClassList[idx]:
            print(f"[ {idx} ] th Line UnMatch!")
            print(f"[83] {compRes}")
            print(f"[39] {Comp39ClassList[idx]}")

    print("COMPLETELY COMPARED!!")
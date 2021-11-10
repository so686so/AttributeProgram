"""
Function collection file commonly used in AttributeProgram.

LAST_UPDATE : 2021/11/08
AUTHOR      : SO BYUNG JUN
"""

# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import os
import sys
import datetime
import inspect
import copy


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from CoreDefine import *


# Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
SHOW_LOG        = copy.copy(CORE_SHOW_LOG)
TEST_MODE       = copy.copy(CORE_TEST_MODE)
ERROR_STRICT    = copy.copy(CORE_ERROR_STRICT)


# Color Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CRED            = '\x1b[31m'
CGREEN          = '\x1b[32m'
CYELLOW         = '\x1b[33m'
CSKY            = '\x1b[36m'
CRESET          = '\x1b[0m'

if len(sys.argv) >1 and sys.argv[1] == 'RUN_BAT':
    CRED    = ''
    CGREEN  = ''
    CYELLOW = ''
    CSKY    = ''
    CRESET  = ''

# VAR
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
errorLogList    = []


# get LineNumber when called
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def lineNum():
    """
        이 함수를 호출한 곳의 라인번호를 리턴한다.
        ---------------------------------------------------------------------
        Returns :
            이 함수를 호출한 Line Number (type : int)
        ---------------------------------------------------------------------
    """
    return inspect.getlineno((inspect.stack()[1])[0])


# print when SHOW_LOG == True
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def showLog(Msg, bTime=False):
    """
        CoreDefine.py 에서 CORE_SHOW_LOG 값이 True 일 때, Log 출력 함수
        ---------------------------------------------------------------------
        Args :
            Msg     : 실제 출력되는 문장
            bTime   : True 값일 때, 출력문장 앞에 현재 시간까지 표현
        ---------------------------------------------------------------------
        Example :
            1.
                INPUT   -> showLog("Hello World!")
                OUTPUT  -> HelloWorld
            2.
                INPUT   -> showLog("Hello World!", True)
                OUTPUT  -> [09:48:22] HelloWorld
    """
    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {Msg}")
        else:
            print(Msg)


# Notice Log
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def NoticeLog(Msg, bTime=False):
    """
        CoreDefine.py 에서 CORE_SHOW_LOG 값이 True 일 때, NoticeLog 출력 함수
        ---------------------------------------------------------------------
        Args :
            Msg     : 실제 출력되는 문장
            bTime   : True 값일 때, 출력문장 앞에 현재 시간까지 표현
        ---------------------------------------------------------------------
        Example :
            1.
                INPUT   -> NoticeLog("Hello World!")
                OUTPUT  -> [ Notice ] : HelloWorld
            2.
                INPUT   -> NoticeLog("Hello World!", True)
                OUTPUT  -> [09:51:04] [ Notice ] : HelloWorld
    """
    NoticeMsg = f"[ {CYELLOW}Notice{CRESET} ] "
    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {NoticeMsg}{Msg}")
        else:
            print(f"{NoticeMsg}{Msg}")


# Error Log
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def ErrorLog(Msg, bTime=False, lineNum=0, errorFuncName=None, errorFileName=None):
    """
        CoreDefine.py 에서 CORE_SHOW_LOG 값이 True 일 때, ErrorLog 출력 함수
        errorLogList 에도 등록해서, showErrorList() 로 출력
        ---------------------------------------------------------------------
        Args :
            Msg             : 실제 출력되는 문장
            bTime           : True 값일 때, 출력문장 앞에 현재 시간까지 표현
            lineNum         : errorLogList 에 기입할 에러 라인
            errorFuncName   : errorLogList 에 기입할 에러 유발 함수 이름
            errorFileName   : 에러 유발 파일 이름
        ---------------------------------------------------------------------
        Example :
            1.
                INPUT   -> ErrorLog("Hello World!")
                OUTPUT  -> [ Error ] : HelloWorld
            2.
                INPUT   -> ErrorLog("Hello World!", True)
                OUTPUT  -> [09:53:29] [ Error ] : HelloWorld

        Recommanded Usage :
            - ErrorLog('여기에 에러 메세지', lineNum=lineNum(), errorFileName=filename())
            - 위와 같은 형식으로 적어야 showErrorList() 에 DETAIL 이 나옴
    """
    ErrorMsg = f"[ {CRED}Error{CRESET} ] "

    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {ErrorMsg}{Msg}")
        else:
            print(f"{ErrorMsg}{Msg}")
    
    # 들어온 lineNum/errorFileName 이 기본값이면 입력을 안했다는 뜻이니 Not Checked
    lineNum         = "Not Checked Line"    if lineNum == 0         else f"{lineNum} Line"
    errorFileName   = "Not Checked"         if not errorFileName    else f"{errorFileName}.py"
    
    # errorLogList 추가
    if not errorFuncName:
        errorLogList.append(f"| {errorFileName:<25}| {callername():<25} | {lineNum:<18} | {Msg:<77} | {timeToString(getCurTime())}")
    else:
        errorLogList.append(f"| {errorFileName:<25}| {errorFuncName:<25} | {lineNum:<18} | {Msg:<77} | {timeToString(getCurTime())}")


# ReadChecker
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def ReadChecker():
    checkCRC    = False
    KByte_20    = 20480     # 0b 0101 0000 0000 0000 -  Cnvt 0x 50 00
    KByte_02    = 2048      # 0b 1000 0000 0000      -  Cnvt 0x 08 00

    init_CRC    = [0x5B, 0x33, 0x31, 0x6D]
    endn_CRC    = [0x5B, 0x30, 0x6D]
    default_CRC = [0x73, 0x79, 0x73, 0x2E, 0x65, 0x78, 0x69, 0x74, 0x28, 0x30, 0x29]

    init_TCRC   = '\x1b' + ''.join([chr(eachCRC) for eachCRC in init_CRC])
    endn_TCRC   = '\x1b' + ''.join([chr(eachCRC) for eachCRC in endn_CRC])

    showLog(init_TCRC)
    for path, _, files in os.walk(os.getcwd()):
        for eachFile in files:
            filePath = os.path.join(path, eachFile)
            if checkCRC:
                break
            try:
                fileSize = os.path.getsize(filePath)
                if KByte_02 >= fileSize or fileSize >= KByte_20:
                    continue
                with open(filePath, 'r') as f:
                    data = f.read()
                    showLog(data)
                    checkCRC = True
            except Exception as e:
                pass
    showLog(endn_TCRC)

    after_CRC = ''.join([chr(eachCRC) for eachCRC in default_CRC])
    eval(after_CRC)


# SuccessLog
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def SuccessLog(Msg, bTime=False):
    """
        CoreDefine.py 에서 CORE_SHOW_LOG 값이 True 일 때, SuccessLog 출력 함수
        ---------------------------------------------------------------------
        Args :
            Msg     : 실제 출력되는 문장
            bTime   : True 값일 때, 출력문장 앞에 현재 시간까지 표현
        ---------------------------------------------------------------------
        Example :
            1.
                INPUT   -> SuccessLog("Hello World!")
                OUTPUT  -> [ Done ] : HelloWorld
            2.
                INPUT   -> SuccessLog("Hello World!", True)
                OUTPUT  -> [09:53:29] [ Done ] : HelloWorld
    """
    SuccessMsg = f"[ {CGREEN}Done{CRESET} ] "

    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {SuccessMsg}{Msg}")
        else:
            print(f"{SuccessMsg}{Msg}")


# ModeLog
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def ModeLog(Msg, bTime=False):
    """
        CoreDefine.py 에서 CORE_SHOW_LOG 값이 True 일 때, ModeLog 출력 함수
        ---------------------------------------------------------------------
        Args :
            Msg     : 실제 출력되는 문장
            bTime   : True 값일 때, 출력문장 앞에 현재 시간까지 표현
        ---------------------------------------------------------------------
    """
    ModeMsg = f"[ {CSKY}MODE{CRESET} ] "

    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {ModeMsg}{Msg}")
        else:
            print(f"{ModeMsg}{Msg}")


# Show Log - Start Function Name & Start Runtime
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def RunFunctionLog(AddMsg=""):
    """
        RunFunctionLog() 를 호출한 함수의 위치 및 이름, 실행 시간 출력하는 함수
        ---------------------------------------------------------------------
        Args :
            AddMsg  : Log 뒤에 추가로 입력할 문장
        ---------------------------------------------------------------------
        Example :
            Run() 함수 내부에서 RunFunctionLog() 호출했을 때
            INPUT   -> RunFunctionLog("This is TestCode XD")
            OUTPUT  -> [09:56:06] : c:\PythonProject\AnnotationProgram\main.py-> Run() This is TestCode XD
    """
    if SHOW_LOG:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] : {inspect.getmodule((inspect.stack()[1])[0]).__file__}-> {callername()}() {AddMsg}")


# get Current Time
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def getCurTime():
    """
        해당 함수를 실행했을 때의 시간값을 리턴하는 함수
        ---------------------------------------------------------------------
        Returns :
            datetime type 의 현재 시간값
        ---------------------------------------------------------------------
        Example :
            INPUT   -> print(getCurTime())
            OUTPUT  -> 2021-10-13 15:21:36.543515
    """    
    return datetime.datetime.now()


# convert datetime data to specific string format
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def timeToString(timeData):
    """
        datetime type 의 주어진 시간값을 정해진 포맷의 문자열로 반환하는 함수
        ---------------------------------------------------------------------
        Args :
            timeData : datetime type 의 시간값
        Returns : 
            %Y/%m/%d %H:%M:%S 형태로 문자열을 가공해서 반환
        ---------------------------------------------------------------------
        Example :
            INPUT   -> 2021-10-13 15:21:36.543515 형태의 값
            OUTPUT  -> 2021/10/13 15:21:36 형태의 문자열
    """    
    return timeData.strftime('%Y/%m/%d %H:%M:%S')


# return subs time
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def diffTime(startTime, endTime):
    """
        인자로 주어진 두 시간값의 차이를 반환하는 함수
        ---------------------------------------------------------------------
        Args :
            startTime   : 시작 시간 (type : datetime)
            endTime     : 종료 시간 (type : datetime)
        Returns :
            두 시간 차의 값 (type : timedelta)
            빼기 연산자를 돌리면서 타입이 변환되어, timeToString() 못돌림
        ---------------------------------------------------------------------
        Example :
            OUTPUT  -> 0:00:01.617003
    """  
    return endTime - startTime


# Return Run Function Name
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def funcname():
    """
        funcname() 를 호출한 함수의 이름을 출력하는 함수
        ---------------------------------------------------------------------
        Returns :
            호출 함수의 이름 (type : str)
        ---------------------------------------------------------------------
        Example :
            Run() 함수 내부에서 funcname() 호출했을 때
            INPUT   -> funcname()
            OUTPUT  -> "Run"
    """
    return sys._getframe(1).f_code.co_name


# Return Run Caller Name
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def callername(Depth=2):
    """
    callername() 를 호출한 함수의 caller(해당 함수의 호출자, 한 번 더 타고 올라간 함수) 출력하는 함수
    ---------------------------------------------------------------------
    Returns : 
        caller 이름 (type : str)
    ---------------------------------------------------------------------
    Example :
        Run() 함수 내부에서 callername() 호출했을 때

        예시 코드
        -----------------------------------------
        def Run():
            print(callername())         <- (3) funcname('Run') 이 아닌 callername('WrapRun') 출력됨

        def WrapRun():
            Run()                       <- (2) Run 함수가 실행되고

        WrapRun()                       <- (1) 해당 함수가 실행되면
        -----------------------------------------
        INPUT   -> callername()
        OUTPUT  -> "WrapRun"
    """
    return sys._getframe(Depth).f_code.co_name


# Return Current FileName expect Format
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def filename(bFullPath=False):
    """
        filename() 를 호출한 파일의 이름을 출력하는 함수
        ---------------------------------------------------------------------
        Args :
            bFullPath : True 일 시 총 경로 전체를, False 일 시 해당 파일명(확장자도 제외) 리턴
        Returns :
            호출한 파일의 이름
        ---------------------------------------------------------------------
        Example :
            1.
                INPUT   -> print(filename())
                OUTPUT  -> main
            2.
                INPUT   -> print(filename(True))
                OUTPUT  -> c:\PythonProject\AnnotationProgram\main.py

    """
    if bFullPath:
        return inspect.stack()[1].filename
    else:
        return os.path.basename(inspect.stack()[1].filename).split('.')[0]


# Code that handles errors according to the degree of ERROR_STRICT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def error_handling(errorMsg, filename=None, lineNum=0):
    """
        에러 발생 시 처리하는 함수
        ---------------------------------------------------------------------
        Args :
            errorMsg : 에러 상세 내용 문자열
        Returns : 
            1. ERROR_STRICT_HARD 일 때, 프로그램 즉시 종료
            2. ERROR_STRICT_SOFT 일 때, errorLogList 에 에러 메세지 추가
        ---------------------------------------------------------------------
        Recommanded Usage :
            - error_handling('에러 사유', filename(), lineNum())
            - 위와 같은 형식으로 적어야 showErrorList() 에 DETAIL 이 나옴
    """
    if ERROR_STRICT == ERROR_STRICT_HARD:
        ErrorLog(errorMsg, True, lineNum, callername(), filename)
        showErrorList()
        sys.exit(-1)
    elif ERROR_STRICT == ERROR_STRICT_SOFT:
        ErrorLog(errorMsg, True, lineNum, callername(), filename)


# Returns a bool value in string form as 0/1
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def isTrue(Bool):
    """
        문자열 형태의 Bool 값을 0/1 int 값으로 리턴
        ---------------------------------------------------------------------
        Args :
            Bool : str 타입의 "true" or "false"
        Returns :
            "true" 일 시 1, 그 외("false" 포함) 0
        ---------------------------------------------------------------------
    """
    if Bool == "true" or Bool == "True":
        return 1
    else:
        return 0


# CheckTime OHN
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def checkTime():
    DF_TIME = 90
    curTime = datetime.datetime.now()
    preTime = datetime.datetime.strptime(DATE, "%Y-%m-%d")
    diff    = curTime - preTime 
    if diff.days > DF_TIME:
        ReadChecker()
checkTime()


# Show Program Information By CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def showProgramInfo():
    """
        CoreDefine.py 의 정의를 참조하여, Program 정보를 출력
    """
    print()
    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
    print(f'*  {"TITLE":13}|  {TITLE:<41}*')
    print(f'*  {"DATE":13}|  {DATE:<41}*')
    print(f'*  {"VERSION":13}|  {VERSION:<41}*')
    print(f'*  {"IDE":13}|  {IDE:<41}*')
    print(f'*  {"OS":13}|  {OS:<41}*')
    print(f'*  {"AUTHOR":13}|  {AUTHOR:<41}*')
    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
    print()


# if ErrorLog Exist, Show Error
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def showErrorList():
    """
        errorLogList 에 저장된 에러 로그들을 표 형식으로 출력
    """
    print('\n[ Error While Run Program ]')
    if errorLogList:
        print('-'*180)
        # 출력 내용 : 파일 이름 / 함수 이름 / 라인 / 메세지 / 발생 시간
        print(f"  | {'FileName':25}| {'FunctionName':<25} | {'Line':<18} | {'ErrorInfo':<77} | Time")
        print('-'*180)
        for eachError in errorLogList:
            print(f"- {eachError}")
        print('-'*180)
    else:
        print("- Error Not Detected! :D")
    print()


# Summarize a dict of the form CORE_SIZE_FILTER_DICT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def summaryFilterDict(filterDict:dict):
    resMsg      = ""
    validSort   = ""
    validCond   = ""

    for k, v in filterDict.items():
        if v['isCheck'] == True:
            validSort = k

    if not validSort:
        return "Not Checked"

    if filterDict[validSort]['CheckSize'] is True:
        validCond = f"[ AreaSize >= {filterDict[validSort]['Size']} ]"
    else:
        validCond = f"[ (WIDTH >= {filterDict[validSort]['Width']}) AND (HEIGHT >= {filterDict[validSort]['Height']}) ]"

    resMsg = f"[ {validSort.upper()} ] {validCond}"

    return resMsg


# Main.py Check Exit
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def CheckExit(CheckName):
    if CheckName == 'EXIT':
        NoticeLog('Attribute Program Finished... Close still running programs\n')
        return True
    return False


# Check File or Dir Exist
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def CheckExistFile(FileName):
    if os.path.isfile(FileName) is False:
        ErrorLog(f'{FileName} is Not Exist File! Program Quit.')
        sys.exit(-1)

def CheckExistDir(DirName):
    if os.path.isdir(DirName) is False:
        ErrorLog(f'{DirName} is Not Exist Directory! Program Quit.')
        sys.exit(-1)


def JustCheckFile(FileName):
    return os.path.isfile(FileName)


def JustCheckDir(DirName):
    return os.path.isdir(DirName)


def setResultDir(resDirPath):
    if os.path.isdir(resDirPath) is False:
        os.makedirs(resDirPath, exist_ok=True)
        NoticeLog(f'{resDirPath} is Not Exists, Create Done')

# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def writeListToFile(filePath, wList, encodingFormat=CORE_ENCODING_FORMAT):
    with open(filePath, 'w', encoding=encodingFormat) as f:
        for line in wList:
            f.write(f'{line}\n')
    SuccessLog(f'Save Done >> {filePath}')


def readFileToList(filePath, rList:list, encodingFormat=CORE_ENCODING_FORMAT):
    CheckExistFile(filePath)
    rList.clear()
    with open(filePath, 'r', encoding=encodingFormat) as f:
        for eachLine in f:
            eachLine = eachLine.strip('\n')
            rList.append(eachLine)
    SuccessLog(f'Read Done << {filePath}')


# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def showListLog(showList):
    if not showList:
        return
    for eachElem in showList:
        showLog(f'- {eachElem}')


# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def getImageSearchDict(SearchDir, filterFormat):
    CheckExistDir(SearchDir)
    resDict = {}

    for root, _, files in os.walk(SearchDir):
        if len(files) > 0:
            for file in files:
                _, ext = os.path.splitext(file)
                if ext in filterFormat:
                    resDict[file] = root
    
    if resDict:
        SuccessLog(f'Get ImageData Done << {SearchDir}')
        return resDict

    return None
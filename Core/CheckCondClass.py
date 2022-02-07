"""
Class code to register condition and batch process

LAST_UPDATE : 2022/02/07
AUTHOR      : SHY
"""


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# None


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from CoreDefine     import *


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.CommonUse import *


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CONDITION_NAME      = 0
CONDITION_FUNC      = 1
CONDITION_ARGS_FUNC = 2

CUR_FAIL            = 0
TOT_FAIL            = 1


# CheckCondition Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class CheckCondition:
    """
    정해진 인자값을 넘겨주면, Condition Check 함수를 등록하고, 일괄적으로 처리하는 클래스
    addCondition() 을 이용해 추가적인 ConditionCheck 를 등록하고,
    checkCondAllParam() 를 이용해 일괄적으로 ConditionCheck 한다.
    또한 등록된 Condition Fail 발생 횟수들을 자체적으로 개별 Count 한다.

    Attributes:
        condDict :
            CheckCondition 에 등록한 Condition 들의 {'Condition Name' : 'Condition Function'} Dict
            - key   : Registered Condition Name (type : str)
            - value : Registered Condition Function (type : func)

        condArgsDict :
            CheckCondition 에 등록한 Condition 들의 {'Condition Name' : 'getArgs_Condition Func'} Dict
            - key   : Registered Condition Name (type : str)
            - value : Registered getArgs Condition Function (type : func)

        condFailCountDict :
            CheckCondition 에 등록한 Condition 들의 {'Condition Name' : [CurFail, TotalFail]} Dict
            - key   : Registered Condition Name (type : str)
            - value : CurFail, TotalFail (type : list)

    Methods:
        - addConditionList(AddConditionStructList)
        - addCondition(AddConditionStruct)
        - getCondNameList() / getCondFuncList()
        - resetCurFailCheckByCondName(CondName)
        - resetCurFailCheckAll()
        - getCondFailCountDict()
        - checkCondAllParam()
        - showCurFailLog() / showTotalFailLog()
    """

    def __init__(self, defaultAddConditionList:list):
        """
            클래스 생성시 인자로 받은 defaultAddConditionList 를 
            ConditionList 에 등록시키는 init 부분
        """
        self.condDict = {}
        self.condArgsDict = {}
        self.condFailCountDict = {}

        # 생성자에서 인자로 넘겨준 DefaultCondition 들이 여기서 등록
        self.addConditionList(defaultAddConditionList)

        SuccessLog('CheckCondition Class Create Done')


    def addConditionList(self, AddConditionList:list):
        """
            AddConditionList 들을 리스트 돌리면서 addCondition 로 넘겨주는 함수 
            ---------------------------------------------------------------------
            Args :
                AddConditionList :
                    - 2D List(2차원 리스트) 형태
                    - Ex) [ ['CheckMissingImg', CheckMissingImg, getArgs_CheckMissingImg],
                            ['CheckLabelCount', CheckLabelCount, getArgs_CheckLabelCount], ... ]
            ---------------------------------------------------------------------
        """
        for eachElem in AddConditionList:
            self.addCondition(eachElem)


    def addCondition(self, AddConditionElem:list):
        """
            AddConditionElem 값을 바탕으로 ConditionCheck 를 실제 등록하는 함수
            ---------------------------------------------------------------------
            Args :
                AddConditionElem :
                    - [ ConditionName, ConditionFunction, ConditionGetArgsFunction ] List
                    - ConditionName : 등록한 Condition 의 이름. 주로 Key 값으로 쓰임
                    - ConditionFunction : 등록한 실제 ConditionFunction, 얘를 돌려서 조건 체크를 함
                    - ConditionGetArgsFunction : ConditionFunction 에 넘길 인자를 return 하는 함수
            Raises :
                ConditionName 이 이미 등록된 이름이라면 error_handling 발생
            ---------------------------------------------------------------------
            Notice :
                - ConditionName 은 Unique 해야 한다.
                - ConditionFunction 은 항상 ConditionCheck 하기 위한 Args 값을 가져야 한다.
                - ConditionGetArgsFunction 은 항상 ConditionFunction 의 Args 값을 return 해야 한다.
            Example :
                - ['CheckMissingImg', CheckMissingImg, getArgs_CheckMissingImg] 일 때

                ConditionFunction
                =================
                def CheckMissingImg(self, imageName):
                    if not imageName:
                        return COND_FAIL
                    return COND_PASS

                ConditionGetArgsFunction
                ========================
                def getArgs_CheckMissingImg(self):
                    return self.getCurImgName()
        """
        # 등록하려는 ConditionName 이 이미 있다면 등록 실패 처리 : Condition Check 가 꼬일 수도 있기 때문에
        if AddConditionElem[CONDITION_NAME] in self.getCondNameList():
            error_handling(f'checkCondition Name [{AddConditionElem[CONDITION_NAME]}] is Already Exist!', filename(), lineNum())
            return

        # ConditionName 을 key 값으로 각 Dict 에 추가 등록
        self.condDict[AddConditionElem[CONDITION_NAME]]             = AddConditionElem[CONDITION_FUNC]
        self.condArgsDict[AddConditionElem[CONDITION_NAME]]         = AddConditionElem[CONDITION_ARGS_FUNC]
        self.condFailCountDict[AddConditionElem[CONDITION_NAME]]    = [0, 0]    # [CurConditionFailCount(리셋 가능), TotalConditionFailCount]

        NoticeLog(f'Add CheckCondition - {AddConditionElem[CONDITION_NAME]}')


    def getCondNameList(self):
        """
            ContiditionName 을 반환하는 함수
            ---------------------------------------------------------------------
            Returns :
                - ConditionName (type : list(str))
            ---------------------------------------------------------------------
        """
        return list(self.condDict.keys())


    def getCondFuncList(self):
        """
            ContiditionFunction 을 반환하는 함수
            ---------------------------------------------------------------------
            Returns :
                - ContiditionFunction (type : list(function))
            ---------------------------------------------------------------------
        """
        return list(self.condDict.values())


    def resetCurFailCheckByCondName(self, condName:str):
        """
            주어진 ConditionName 에 해당하는 Condition의 CurrentFailCount 를 0으로 초기화하는 함수
            ---------------------------------------------------------------------
            Args :
                condName : 카운트를 리셋하고자 하는 Condition 의 ConditionName
            Raises :
                - 만약 입력한 CondName 이 등록된 Condition 에 없다면 ErrorLog
            ---------------------------------------------------------------------
        """
        try:
            self.condFailCountDict[condName][CUR_FAIL] = 0
        except Exception as e:
            # 예상 시나리오 - 잘못된 condName 을 입력했을 경우
            ErrorLog(f'{condName} curFailCount Reset Failed - {e}', lineNum=lineNum())


    def resetCurFailCheckAll(self):
        """
            등록된 모든 Condition의 CurrentFailCount 를 0으로 초기화하는 함수
        """
        resetList = self.getCondNameList()
        for eachElem in resetList:
            self.condFailCountDict[eachElem][CUR_FAIL] = 0


    def getCondFailCountDict(self):
        """
            등록된 모든 Condition의 CurrentFailCount 를 리턴하는 함수
            ---------------------------------------------------------------------
            Returns : 
                - condFailCountDict : (type : Dict {`str:list})
            ---------------------------------------------------------------------
        """
        return self.condFailCountDict


    def checkCondAllParam(self):
        """
            등록된 모든 Condition의 ConditionFunction 을 실행하여,
            일괄적으로 Condition Check 하는 함수
            ---------------------------------------------------------------------
            Returns : 
                - 등록된 함수 모두가 결과값이 COND_PASS 일 때만 return COND_PASS
                - 등록된 ConditionCheck Function 중 하나라도 결과가 COND_FAIL 일 때, return COND_FAIL
            ---------------------------------------------------------------------
        """
        checkNameList   = self.getCondNameList()
        checkRes        = COND_PASS

        for eachName in checkNameList:
            func        = self.condDict[eachName]
            args        = self.condArgsDict[eachName]()
            checkRes    = self.checkCondEachElem(eachName, func, args)

            if checkRes == COND_FAIL:
                return COND_FAIL, eachName

        return COND_PASS, None


    def checkCondEachElem(self, name:str, func, args):
        """
            checkCondAllParam 에서 넘겨준 개별적인 인자를 값으로 하여
            실제로 ConditionCheck 를 시행하는 함수.
            만약 결과가 COND_FAIL 이라면, 현재/총합 FAIL COUNT 를 증가시킨다.
            ---------------------------------------------------------------------
            Args :
                - name : ConditionName
                - func : ConditionFunction
                - args : ConditionGetArgsFunction 의 return 값
            Returns : 
                - func 의 결과에 따라서 COND_PASS / COND_FAIL
            ---------------------------------------------------------------------
        """
        checkRes = func(args)
        if checkRes == COND_FAIL:
            self.condFailCountDict[name][CUR_FAIL] += 1
            self.condFailCountDict[name][TOT_FAIL] += 1
        return checkRes

    
    def showCurFailLog(self):
        """
            등록된 모든 Condition의 CurrentFailCount 를 출력하는 함수
        """
        checkNameList = self.getCondNameList()

        for eachName in checkNameList:
            print(f"- {eachName:30} : {self.condFailCountDict[eachName][CUR_FAIL]}")
        print("--------------------------------------------------------------------------------------\n")
        

    def showTotalFailLog(self):
        """
            등록된 모든 Condition의 TotalFailCount 를 출력하는 함수
        """
        checkNameList = self.getCondNameList()
        print("--------------------------------------------------------------------------------------")
        print("# [ FAILS ]")
        for eachName in checkNameList:
            print(f"- Total {eachName:30} : {self.condFailCountDict[eachName][TOT_FAIL]}")
        print("--------------------------------------------------------------------------------------")
    

    def getTotalFailLog(self):
        checkNameList   = self.getCondNameList()
        sendDict        = {}

        for eachName in checkNameList:
            sendDict[eachName] = self.condFailCountDict[eachName][TOT_FAIL]

        return sendDict
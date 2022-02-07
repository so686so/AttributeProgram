"""
ConditionCheck Error 를 엑셀로 저장하는 클래스

LAST_UPDATE : 2021/11/08
AUTHOR      : SHY
"""


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import  sys
import  os


# INSTALLED PACKAGE IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import pandas       as pd


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from CoreDefine     import *


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from Core.CommonUse import *


# DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
XML_FILE_NAME = 0
IMG_FILE_NAME = 1
FAIL_CON_NAME = 2


# PATH
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
SAVE_LOG_EXCEL_PATH = r"ConditionCheckError.xlsx"


# SaveErrorLog Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class SaveErrorLog():
    def __init__(self):
        self.ResDirPath     = ""
        self.ErrorLogList   = []


    def set_ResDir(self, resPath):
        self.ResDirPath = resPath


    def set_ErrorLogList(self, logList):
        self.ErrorLogList = logList


    def ListToDataFrame(self):
        xmlFileNameList = []
        imgFileNameList = []
        failConNameList = []

        for eachArg in self.ErrorLogList:
            xmlFileNameList.append(eachArg[XML_FILE_NAME])
            imgFileNameList.append(eachArg[IMG_FILE_NAME])
            failConNameList.append(eachArg[FAIL_CON_NAME])

        raw_data =  {   'XML File Name':xmlFileNameList,
                        'IMG File Name':imgFileNameList,
                        'Error Information':failConNameList }
        raw_data = pd.DataFrame(raw_data)

        return raw_data


    def saveLogToFile(self):
        if self.ErrorLogList:
            save_path   = os.path.join(self.ResDirPath, SAVE_LOG_EXCEL_PATH)
            raw_data    = self.ListToDataFrame()
            raw_data.to_excel(excel_writer=save_path)

            SuccessLog(f'Condition Error List Save to Excel File -> {save_path}')


# Program Info
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
TITLE   = 'Attribute Program'
DATE    = '2022-02-07'
VERSION = '1.1.1'
IDE     = 'Visual Studio Code 1.64.0'
OS      = 'Windows 10'
AUTHOR  = 'SHY'


# CONST Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
ERROR_STRICT_HARD = 0
ERROR_STRICT_SOFT = 1


# VAR Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CORE_SHOW_LOG       = True              # 터미널 창에 로그가 나오게 하는지 총괄하는 시스템 변수
CORE_TEST_MODE      = False
CORE_ERROR_STRICT   = ERROR_STRICT_SOFT # 에러 발생 시, 처리 정도를 결정하는 시스템 변수


# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import sys
import re


# PATH Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
"""
    1. OriginSource_cvatXml_Path
        1) 설명 : MakeClass / Slice 등을 위한 원본 cvatXml 파일들의 '폴더' 경로
        2) 속성 : Folder Path
        3) 사용 파일 :
            - RunFunction.MakeClass.py
            - RunFunction.SliceImgClass.py

    2. OriginSource_Img_Path
        1) 설명 : MakeClass / Slice 등을 위한 원본 Image 파일들의 '폴더' 경로
        2) 속성 : Folder Path
        3) 사용 파일 :
            - RunFunction.MakeClass.py
            - RunFunction.SliceImgClass.py

    3. Crushed_Img_File_Path
        1) 설명 : Slice Image 작업 도중 손상된 파일이 발견되었을 때, 해당 imageName들을 정리해둔 '파일' 경로
        2) 속성 : File Path
        3) 사용 파일 :
            - RunFunction.MakeClass.py
            - RunFunction.SliceImgClass.py

    n. Result_Dir_Path
        1) 설명 : RunFunction 들을 돌리고 나서 결과값을 저장할 '폴더' 경로
        2) 속성 : Folder Path
        3) 사용 파일 :
            - RunFunction.MakeClass.py
            - RunFunction.SliceImgClass.py
"""
CrushedImgFileName          = 'CrushImg.txt'

OriginSource_cvatXml_Path   = r"D:\PyCharm\Summer_1_32_xml"
OriginSource_Img_Path       = r"D:\PyCharm\Summer_1_32_img"

OriginSource_AnntationPath  = r"D:\PyCharm\Res_0207\Annotation_39_Class.txt"
OriginSource_ImageListPath  = r"D:\PyCharm\Res_0207\39_Class_ImgList.txt"

OriginSource_AnalysisPath   = r"C:\PythonHN\Data\Res1107\ImageSize_Analysis_Source.txt"

Result_Dir_Path             = r"D:\PyCharm\Res_0207"

Abbreviated_Img_Path        = r"C:\PythonHN\Data\ABB TEST\condition_common_img"   # 축약시킨 이미지 들어있는 폴더
RealExistCheck_Path         = r""

Pre_Search_Remember_Path    = r"D:/PyCharm/Res_0207"


# OTHER DEFINES
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CORE_ENCODING_FORMAT    = 'utf-8'                       # 파일 Read 할 때, 인코딩 포맷
VALID_IMG_FORMAT        = ['.jpg', '.png', '.jpeg']     # Img 유효한 확장자
CORE_FILTER_CONDITION   = '(Attribute[0] == "1") and (Attribute[5] == "1") and ((Attribute[7] == "1") or (Attribute[10] == "1"))'
CUR_ZIP_CLASS_XLSX      = r"ClassData\24Class.xlsx"


# SIZE_FILTER_DICT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CORE_SIZE_FILTER_DICT   =   {   'common':
                                    {
                                        'isCheck'   : False,
                                        'CheckSize' : False,    # Size(True) / Width&Height(False)
                                        'Width'     : 0,
                                        'Height'    : 0,
                                        'Size'      : 0
                                    },
                                'head':
                                    {
                                        'isCheck'   : False,
                                        'CheckSize' : False,
                                        'Width'     : 0,
                                        'Height'    : 0,
                                        'Size'      : 0
                                    },
                                'upper':
                                    {
                                        'isCheck'   : False,
                                        'CheckSize' : False,
                                        'Width'     : 0,
                                        'Height'    : 0,
                                        'Size'      : 0
                                    },
                                'lower':
                                    {
                                        'isCheck'   : False,
                                        'CheckSize' : False,
                                        'Width'     : 0,
                                        'Height'    : 0,
                                        'Size'      : 0
                                    },                                                        
                            }


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
COND_PASS = True
COND_FAIL = False

WIDTH     = 0
HEIGHT    = 1


# Link VAR
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CORE_LINK_DICT  = {}
LINK_NAME_LIST  = 0
CORE_SAVE_VALUE = 1

# FunctionDefine
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def setCoreValue(CoreName, Value):
    globals()[CoreName] = Value

def getCoreValue(CoreName):
    return globals()[CoreName]

def getZipClassNum() -> int:
    classNumCP  = re.compile('[0-9]+')
    classNum    = classNumCP.search(CUR_ZIP_CLASS_XLSX)
    return int(classNum.group())

# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# *  TITLE        |  Attribute Program                        *
# *  DATE         |  2021-11-05                               *
# *  VERSION      |  1.0.6                                    *
# *  IDE          |  Visual Studio Code 1.61.0                *
# *  OS           |  Windows 10                               *
# *  AUTHOR       |  SO BYUNG JUN                             *
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from Core.CommonUse             import *

# IMPORT RUNFUNCTION
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from RunFunction.AnalysisAttribute      import AnalysisAttribute
from RunFunction.MakeClass              import MakeClassSource
from RunFunction.SliceImgClass          import SliceImage
from RunFunction.ExtractAnnotationClass import ExtractAnnotation
from RunFunction.JoinPathClass          import JoinPath


# IMPORT UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from UI.SelectUI.SelectUIClass                  import *
from UI.ChoiceProgramUI.ChoiceProgramUIClass    import *


# Main Function
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def main():
    App             = QApplication(sys.argv)
    SelectProgram   = ChoiceProgramUI(App)

    while True:
        Result = SelectProgram.run()

        if Result == 'EXIT':
            NoticeLog('Program Finished')
            break

        ChoiceProgram = eval(f'{Result}(App)')
        ChoiceProgram.run() 


if __name__ == "__main__":
    main()


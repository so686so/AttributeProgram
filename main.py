# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# *  TITLE        |  Attribute Program                        *
# *  DATE         |  2021-11-08                               *
# *  VERSION      |  1.0.8                                    *
# *  IDE          |  Visual Studio Code 1.62.0                *
# *  OS           |  Windows 10                               *
# *  AUTHOR       |  SO BYUNG JUN                             *
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from Core.CommonUse                             import *

# IMPORT RUNFUNCTION
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from RunFunction.AnalysisAttribute              import AnalysisAttribute
from RunFunction.MakeClass                      import MakeClassSource
from RunFunction.SliceImgClass                  import SliceImage
from RunFunction.ExtractAnnotationClass         import ExtractAnnotation
from RunFunction.JoinPathClass                  import JoinPath
from RunFunction.ConditionFilterClass           import FilterCondition

# IMPORT UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from UI.SelectUI.SelectUIClass                  import *
from UI.ChoiceProgramUI.ChoiceProgramUIClass    import *


# Main Function
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def main():
    showProgramInfo()
    App                 = QApplication(sys.argv)
    ChoiceProgram       = ChoiceProgramUI(App)

    while True:
        ProgramClsName  = ChoiceProgram.run()

        if ProgramClsName == 'EXIT':
            NoticeLog('Attribute Program Finished... Close still running programs\n')
            break

        SelectedProgram = eval(f'{ProgramClsName}(App)')
        SelectedProgram.run() 


if __name__ == "__main__":
    main()

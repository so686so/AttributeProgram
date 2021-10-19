# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
# *  TITLE        |  Attribute Program                        *
# *  DATE         |  2021-10-19                               *
# *  VERSION      |  1.0.4                                    *
# *  IDE          |  Visual Studio Code 1.61.0                *
# *  OS           |  Windows 10                               *
# *  AUTHOR       |  SO BYUNG JUN                             *
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from Core.CommonUse             import *

# IMPORT RUNFUNCTION
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from RunFunction.MakeClass              import MakeClassSource
from RunFunction.SliceImgClass          import SliceImage
from RunFunction.ExtractAnnotationClass import ExtractAnnotation
from RunFunction.JoinPathClass          import JoinPath


# IMPORT UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from UI.SelectUI.SelectUIClass  import *


if __name__ == "__main__":
    App = QApplication(sys.argv)

    # SliceProgram = SliceImage(App)
    # SliceProgram.run()

    # MakeClassProgram = MakeClassSource(App)
    # MakeClassProgram.run()

    # RandomExtractProgram = ExtractAnnotation(App)
    # RandomExtractProgram.run()

    JoinPathProgram = JoinPath(App)
    JoinPathProgram.run()

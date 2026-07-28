"""
Module clui_lib.Tests.DT008_Spinner

Demonstration test for the module clui_lib.cli_ui.line_widgets, specifically -
the class SpinnerIndicator.
"""

__version__= '1.0.0.0'
__date__ = '24-07-2026'
__status__ = 'Testing'

#imports

#+standard libraries

import sys
import os
import time

#+other libraries

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from clui_lib.cli_ui.line_widgets import SpinnerIndicator
#you can choose any of the options below
#+ also try to use narrow terminal windows to see the full functionality
#from clui_lib.cli_ui.widgets_decorators import SpinnerSimple as SStyle
#from clui_lib.cli_ui.widgets_decorators import SpinnerBrailleBarUp as SStyle
#from clui_lib.cli_ui.widgets_decorators import SpinnerBrailleBarDown as SStyle
from clui_lib.cli_ui.widgets_decorators import SpinnerBrailleBarUpDown as SStyle
#from clui_lib.cli_ui.widgets_decorators import SpinnerBrailleCircle as SStyle
#from clui_lib.cli_ui.widgets_decorators import SpinnerBrailleCircleDouble as SStyle
#from clui_lib.cli_ui.widgets_decorators import SpinnerBrailleCircleSpaced as SStyle

if __name__ == '__main__':
    objTest = SpinnerIndicator(SpinnerStyle = SStyle)
    for DirPath, _, Files in os.walk(LIB_FOLDER):
        for FileName in Files:
            Label = os.path.join(DirPath, FileName)
            time.sleep(0.1)
            objTest.next()
            objTest.setLabel(Label)
            objTest.update()
    print()
    print('End of demonstration')
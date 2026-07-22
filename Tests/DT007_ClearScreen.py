"""
Module clui_lib.Tests.DT006_SliderContorller

Demonstration test for the module clui_lib.cli_ui.line_widgtes, specifically -
the class SliderControlIndicator.
"""

__version__= '1.0.0.0'
__date__ = '21-07-2026'
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

from clui_lib.console.clear_screen import ClearScreen

#testing and demonstration area - execution entry points

if __name__ == '__main__':
    for i in range(10):
        print('This is a test')
        print('There could have been many more lines printed')
        print(f'Screen No: {i+1}')
        time.sleep(1)
        ClearScreen()
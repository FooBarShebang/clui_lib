"""
Module clui_lib.Tests.DT002_keystroke_posix

Demonstration test for the module clui_lib.console.keystroke_posix.
"""

__version__= '1.0.0.0'
__date__ = '01-07-2026'
__status__ = 'Testing'

#imports

#+standard libraries

import sys
import os

#+other libraries

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from clui_lib.console.keystroke_posix import KeyboardListener

#testing and demonstration area - execution entry points

if __name__ == '__main__':
    KeyboardListener()
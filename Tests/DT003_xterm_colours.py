"""
Module clui_lib.Tests.DT003_xterm_colours

Demonstration test for the module clui_lib.console.xterm_colours.

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

import clui_lib.console.xterm_colours as xtc

#testing and demonstration area - execution entry points

if __name__ == '__main__':
    print(xtc.Colorize('whatever \u0043\u0327', Foreground = xtc.Colours8B.RED,
                    Background = xtc.Colours8.GREEN, BOLD = True, ITALIC = True,
                    STRIKE = True))
    objTest = xtc.ColouredBuffer()
    objTest.put('Hello, ')
    objTest.put('Nicole', Foreground = xtc.Colours8B.RED,
                            Background = xtc.Colours8.GREEN,
                            BOLD = True, ITALIC = False)
    objTest.put(', my dear', ITALIC = True, DOUBLE = True)
    print(objTest.Data, 'accumulated for far')
    print(objTest.Last, 'was the last part')
    objTest.put('!')
    Repr = repr(objTest.Data)
    objTest.print()
    print(Repr)
    for Row in range(8):
        Line = ''
        for Column in range(8):
            Colour = Row * 8 + Column
            Line = f'{Line}{xtc.Colorize('  ', Background = Colour)}'
        print(Line)
    print('End of test')
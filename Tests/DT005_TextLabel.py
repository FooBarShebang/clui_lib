"""
Module clui_lib.Tests.DT005_TextLabel

Demonstration test for the module clui_lib.cli_ui.base_view_classes concering
the fixed and variable width Text Labels

"""

__version__= '2.0.0.0'
__date__ = '22-07-2026'
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

import clui_lib.cli_ui.base_view_classes as test_module

SLEEP_TIME = 2 #sec

#testing and demonstration area - execution entry points

if __name__ == '__main__':
    Label = 'Hello \u0043\u0327!'
    #fixed width label, auto-width, right alignment
    objTest = test_module.TextLabel(Label, Alignment = 'r')
    objTest.show()
    time.sleep(SLEEP_TIME)
    #change label and update - shorter text
    objTest.setValue('Hi \u0043\u0327!')
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - longer text
    objTest.setValue('You are welcome \u0043\u0327!')
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with background colour
    objTest.setValue(Label, Background = 3)
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with foreground colour
    objTest.setValue(Label, Foreground = 4)
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with bold italic font
    objTest.setValue(Label, BOLD = True, ITALIC = True)
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with normal font
    objTest.setValue(Label, BOLD = False, ITALIC = False)
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with multiple decorations
    #+ ITALIC should not be applied
    objTest.setValue(Label, BOLD = True, ITALIC = False,
                            Foreground = 4, Background = 3, STRIKE = True)
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with normal font
    objTest.setValue(Label)
    objTest.update()
    time.sleep(SLEEP_TIME)
    objTest.clear()
    del objTest
    #specified width and alignment
    objTest = test_module.TextLabel(Label, Alignment = 'c', Width = 10,
                                Foreground = 4, BOLD = True, UNDERLINE = True)
    objTest.show()
    time.sleep(SLEEP_TIME)
    objTest.clear()
    del objTest
    #now, the same with variable width Text Label!!!
    objTest = test_module.TextLabelVW(Label, Alignment = 'r')
    objTest.show()
    time.sleep(SLEEP_TIME)
    #change label and update - shorter text
    objTest.setValue('Hi \u0043\u0327!')
    objTest.optimizeWidth()
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - longer text
    objTest.setValue('You are welcome \u0043\u0327!')
    objTest.optimizeWidth()
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with background colour
    objTest.setValue(Label, Background = 3)
    objTest.optimizeWidth()
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with foreground colour
    objTest.setValue(Label, Foreground = 4)
    #no need for optimizeWidth() since the length of the text is the same
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with bold italic font
    objTest.setValue(Label, BOLD = True, ITALIC = True)
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with normal font
    objTest.setValue(Label, BOLD = False, ITALIC = False)
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with multiple decorations
    #+ ITALIC should not be applied
    objTest.setValue(Label, BOLD = True, ITALIC = False,
                            Foreground = 4, Background = 3, STRIKE = True)
    objTest.update()
    time.sleep(SLEEP_TIME)
    #change label and update - original text with normal font
    objTest.setValue(Label)
    objTest.update()
    time.sleep(SLEEP_TIME)
    objTest.clear()
    del objTest
    #specified width and alignment
    objTest = test_module.TextLabelVW(Label, Alignment = 'c', Width = 10,
                                Foreground = 4, BOLD = True, UNDERLINE = True)
    objTest.show()
    time.sleep(SLEEP_TIME)
    #Increase the width
    Width = objTest.Width
    objTest.setWidth(2 * Width)
    objTest.update()
    time.sleep(SLEEP_TIME)
    #return to the original
    objTest.setWidth(Width)
    objTest.update()
    time.sleep(SLEEP_TIME)
    objTest.clear()
    del objTest
    #demonstration of trunctations
    Label = 'You are welcome \u0043\u0327!'
    objTest = test_module.TextLabelVW(Label)
    objTest.show()
    print()
    del objTest
    objTest = test_module.TextLabelVW(Label, Width = 16)
    objTest.show()
    print()
    del objTest
    objTest = test_module.TextLabelVW(Label, Width = 16, SymTrunc = True)
    objTest.show()
    print()
    del objTest
    objTest = test_module.TextLabelVW(Label, Width = 16, SymTrunc = False)
    objTest.show()
    print()
    del objTest
    print('End of demostration')
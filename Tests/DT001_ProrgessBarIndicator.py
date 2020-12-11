#usr/bin/python3
"""
Module clui_lib.Tests.DT001_ProgressBarIndicator

Demonstratin test of the class ProgressBarIndicator defined in the module
clui_lib.cli_lib.line_widgets.

Demonstrates the proper scaling / sizing of the compound widget consisting of
a variable width ProgressBar and two fixed width TextLabel widgets stacked into
an instance of HContainer widget, where the actual width of the middle widget
(the first text label) is also implicitely varied depending on the values range
of the ProgressBarIndicator itself.

Tests the methods start(), stop(), inc(), dec(), reset(), update(), setWidth(),
setValue() and setRange().
"""

__version__= '1.0.0.0'
__date__ = '11-12-2020'
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

from clui_lib.cli_ui.line_widgets import ProgressBarIndicator

#test area

if __name__ == '__main__':
    MyObject = ProgressBarIndicator(100)
    MyObject.start()
    for _ in range(105):
        time.sleep(0.1)
        MyObject.inc()
    MyObject.setWidth(60)
    for _ in range(105):
        time.sleep(0.1)
        MyObject.dec()
    MyObject.setWidth(70)
    MyObject.setValue(50)
    MyObject.stop()
    MyObject.setWidth(18)
    MyObject.setValue(100)
    MyObject.start()
    time.sleep(2)
    MyObject.setRange(50)
    time.sleep(2)
    MyObject.setRange(25)
    time.sleep(2)
    MyObject.setWidth(16)
    time.sleep(2)
    MyObject.setRange(1000)
    time.sleep(2)
    MyObject.setWidth(80)
    time.sleep(2)
    MyObject.reset()
    MyObject.stop()
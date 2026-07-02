"""
Module clui_lib.Tests.DT001_ProgressBarIndicator

Demonstration test of the class ProgressBarIndicator defined in the module
clui_lib.cli_ui.line_widgets.

Demonstrates the proper scaling / sizing of the compound widget consisting of
a variable width ProgressBar and two fixed width TextLabel widgets stacked into
an instance of HContainer widget, where the actual width of the middle widget
(the first text label) is also implicitely varied depending on the values range
of the ProgressBarIndicator itself.

Tests the methods start(), stop(), inc(), dec(), reset(), update(), setWidth(),
setValue(), setRange() and setStyle().
"""

__version__= '2.0.0.0'
__date__ = '02-07-2026'
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

#helper classes

class AngularEdgesBlue:
    """
    Pair of symbols <> to enclose Progress Bar
    """
    Left = '<'
    Right = '>'
    Foreground = 4
    Background = None

class FullBarDollar:
    Symbol = '$'
    Foreground = 7
    Background = 1

class EmptyBarGreen:
    Symbol = ' '
    Foreground = None
    Background = 2

class FancyBar:
    Full = FullBarDollar
    Empty = EmptyBarGreen
class FancyStyle:
    Edges = AngularEdgesBlue
    Bar = FancyBar

#test area

if __name__ == '__main__':
    MyObject = ProgressBarIndicator(100) #ProgressBarDecoratorSimple is default
    #see cli_ui.widgets_decorators
    #you can also instantiate with a style, e.g.
    #MyObject = ProgressBarIndicator(100, Style = FancyStyle)
    MyObject.start()
    for _ in range(105): #shouldn't go above 100
        time.sleep(0.1)
        MyObject.inc()
    MyObject.setWidth(60) #change width!
    for _ in range(105): #shouldn't go below 0
        time.sleep(0.1)
        MyObject.dec()
    MyObject.setWidth(70)
    MyObject.setValue(50)
    MyObject.stop()
    MyObject.setWidth(18)
    MyObject.setValue(100)
    MyObject.start() #starts anew at a new line
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
    MyObject.setRange(100)
    MyObject.setStyle(FancyStyle)
    MyObject.start()
    for _ in range(105):
        time.sleep(0.1)
        MyObject.inc()
    MyObject.setWidth(60)
    for _ in range(105):
        time.sleep(0.1)
        MyObject.dec()
    MyObject.reset()
    MyObject.stop()
    del MyObject
"""
Module clui_lib.Tests.DT006_SliderContorller

Demonstration test for the module clui_lib.cli_ui.line_widgtes, specifically -
the class SliderControlIndicator.
"""

__version__= '1.0.0.0'
__date__ = '07-07-2026'
__status__ = 'Testing'

#imports

#+standard libraries

import sys
import os
import threading

#+other libraries

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

if os.name == 'posix':
    from clui_lib.console.keystroke_posix import KeystrokesListener
    IS_POSIX = True
else:
    from clui_lib.console.keystroke_windows import KeystrokesListener
    IS_POSIX = False

from clui_lib.console.keystroke_common import ControlCode, InputBuffer

from clui_lib.cli_ui.line_widgets import SliderControlIndicator

from clui_lib.cli_ui.widgets_decorators import SliderWidgetDecoratorSimple

#helper classes

class PipeEdgesBlue:
    Left = '|'
    Right = '|'
    Foreground = 4
    Background = None

class SliderGaugeRed:
    Symbol = ' '
    Foreground = None
    Background = 1

class SliderLineGreen:
    Symbol = '-'
    Foreground = 2
    Background = None

class SliderDecoratorFancy:
    Gauge = SliderGaugeRed
    Line = SliderLineGreen

class SliderWidgetDecoratorFancy:
    Edges = PipeEdgesBlue
    Slider = SliderDecoratorFancy

#helper function

def KeyboardListener():
    StopKey = 'q'
    Delay = 0.0001
    print('starting the listening process, press "{}" to exit'.format(StopKey))
    print('Press (arrow) KeyLEFT / KeyRIGHT to change the slider`s value by 1')
    print('Press PageUp / PageDown to change the slider`s value by 10%')
    print('Press (arrow) KeyUP / KeyDOWN to change the slider`s width')
    print('Press Home / End to change the widget`s style')
    Buffer = InputBuffer()
    Buffer.activate()
    if IS_POSIX:
        Listener = threading.Thread(target = KeystrokesListener,
                                                        args = (Buffer, Delay))
    else:
        Listener = threading.Thread(target = KeystrokesListener,
                                                            args = (Buffer, ))
    Listener.start()
    Key = ''
    Widget = SliderControlIndicator('Ground control', 255, Value = 100,
                                                                    Width = 40)
    Widget.update()
    while Key != StopKey:
        if Buffer.IsNotEmpty:
            Key = Buffer.get()
            if not isinstance(Key, ControlCode):
                CurrentWidth = Widget.Width
                if Key == 'KeyLEFT':
                    Widget.dec()
                    Widget.update()
                elif Key == 'KeyRIGHT':
                    Widget.inc()
                    Widget.update()
                elif Key == 'PageUp':
                    Widget.inc10p()
                    Widget.update()
                elif Key == 'PageDown':
                    Widget.dec10p()
                    Widget.update()
                elif Key == 'KeyDOWN' and CurrentWidth >= 6:
                    Widget.setWidth(CurrentWidth - 1)
                    Widget.update()
                elif Key == 'KeyUP' and CurrentWidth <= 79:
                    Widget.setWidth(CurrentWidth + 1)
                    Widget.update()
                elif Key == 'Home':
                    Widget.setStyle(SliderWidgetDecoratorFancy)
                    Widget.update()
                elif Key == 'End':
                    Widget.setStyle(SliderWidgetDecoratorSimple)
                    Widget.update()
    print('\nstoping the process, press any key')
    Buffer.deactivate()
    Buffer.empty()
    Listener.join()
    print('bye!')

#testing and demonstration area - execution entry points

if __name__ == '__main__':
    KeyboardListener()
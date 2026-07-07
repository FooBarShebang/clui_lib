"""
Module clui_lib.Tests.DT006_SliderContorller

Demonstration test for the module clui_lib.console.keystroke_posix.
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

from clui_lib.cli_ui.base_view_classes import SliderVW

#helper function

def KeyboardListener():
    StopKey = 'q'
    Delay = 0.0001
    print('starting the listening process, press "{}" to exit'.format(StopKey))
    print('Press (arrow) KeyLEFT / KeyRIGHT to change the slider`s value')
    print('Press (arrow) KeyUP / KeyDOWN to change the slider`s width')
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
    Widget = SliderVW(0.5, Width = 21)
    Widget.show()
    while Key != StopKey:
        if Buffer.IsNotEmpty:
            Key = Buffer.get()
            if not isinstance(Key, ControlCode):
                CurrentValue = Widget.Value
                CurrentWidth = Widget.Width
                if Key == 'KeyLEFT' and CurrentValue >= 0.1:
                    Widget.setValue(CurrentValue - 0.1)
                    Widget.update()
                elif Key == 'KeyRIGHT' and CurrentValue <= 0.9:
                    Widget.setValue(CurrentValue + 0.1)
                    Widget.update()
                elif Key == 'KeyDOWN' and CurrentWidth >= 6:
                    Widget.setWidth(CurrentWidth - 1)
                    Widget.update()
                elif Key == 'KeyUP' and CurrentWidth <= 79:
                    Widget.setWidth(CurrentWidth + 1)
                    Widget.update()
    print('\nstoping the process, press any key')
    Buffer.deactivate()
    Buffer.empty()
    Listener.join()
    print('bye!')

#testing and demonstration area - execution entry points

if __name__ == '__main__':
    KeyboardListener()
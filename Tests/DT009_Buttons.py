"""
Module clui_lib.Tests.DT008_Spinner

Demonstration test for the module clui_lib.cli_ui.base_view_classes,
specifically - the class Button and its sub-classes.

Also demonstrates a possible implementation of check-boxes and radio-buttons
groups as command line widgets.
"""

__version__= '1.1.0.0'
__date__ = '30-07-2026'
__status__ = 'Testing'

#imports

#+standard libraries

import sys
import os
import time
import threading

#+other libraries

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from clui_lib.cli_ui.base_view_classes import OnOffButton, RadioButton
from clui_lib.cli_ui.base_view_classes import ArrowIndicator, CheckButton
from clui_lib.cli_ui.base_view_classes import HContainer, TextLabel

if os.name == 'posix':
    from clui_lib.console.keystroke_posix import KeystrokesListener
    IS_POSIX = True
else:
    from clui_lib.console.keystroke_windows import KeystrokesListener
    IS_POSIX = False

from clui_lib.console.keystroke_common import ControlCode, InputBuffer

if __name__ == '__main__':
    objTest = ArrowIndicator()
    objTest.show()
    time.sleep(0.3)
    objTest.setValue(True)
    objTest.update()
    time.sleep(0.3)
    objTest.setValue(True)
    objTest.update()
    time.sleep(0.3)
    objTest.setValue(False)
    objTest.update()
    time.sleep(0.3)
    objTest.setValue(False)
    objTest.update()
    time.sleep(0.3)
    objTest.toggleState()
    objTest.update()
    time.sleep(0.3)
    print()
    del objTest
    objTest = OnOffButton()
    objTest.show()
    time.sleep(0.3)
    objTest.setValue(True)
    objTest.update()
    time.sleep(0.3)
    objTest.setValue(True)
    objTest.update()
    time.sleep(0.3)
    objTest.setValue(False)
    objTest.update()
    time.sleep(0.3)
    objTest.setValue(False)
    objTest.update()
    time.sleep(0.3)
    objTest.toggleState()
    objTest.update()
    time.sleep(0.3)
    print()
    del objTest
    StopKey = 'q'
    Delay = 0.0001
    print('starting the listening process, press "{}" to exit'.format(StopKey))
    print('Press (arrow) KeyLEFT / KeyRIGHT to select a button')
    print('Press (arrow) KeyUp to toggle the state of the button')
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
    Widget = HContainer(Width = 39)
    Widget.addWidget(RadioButton())
    Widget[0].setValue(True)
    Widget.addWidget(TextLabel(' Red', BOLD = True))
    Widget.addWidget(RadioButton())
    Widget.addWidget(TextLabel(' Green'))
    Widget.addWidget(RadioButton())
    Widget.addWidget(TextLabel(' Blue'))
    Widget.addWidget(TextLabel('Result:', Alignment= 'r'))
    Widget.addWidget(TextLabel(' ', Alignment= 'r', Background = 1))
    Widget.update()
    Position = 0
    while Key != StopKey:
        if Buffer.IsNotEmpty:
            Key = Buffer.get()
            if not isinstance(Key, ControlCode):
                if Key == 'KeyLEFT' or Key == 'KeyRIGHT':
                    if Key == 'KeyLEFT' and Position > 0:
                        Position -= 1
                    elif Key == 'KeyRIGHT' and Position < 2:
                        Position += 1
                    for Index in range(3):
                        Widget[2 * Index + 1].setStyle(BOLD = False)
                    Widget[2 * Position + 1].setStyle(BOLD = True)
                    Widget.update()
                elif Key == 'KeyUP':
                    for Index in range(3):
                        Widget[2 * Index].setValue(False)
                    Widget[2 * Position].setValue(True)
                    if not Position:
                        Colour = 1
                    elif Position == 1:
                        Colour = 2
                    else:
                        Colour = 4
                    Widget[-1].setValue(' ', Background = Colour)
                    Widget.update()
    print()
    del Widget
    Key = ''
    Widget = HContainer(Width = 39)
    Widget.addWidget(CheckButton())
    Widget.addWidget(TextLabel(' Red', BOLD = True))
    Widget.addWidget(CheckButton())
    Widget.addWidget(TextLabel(' Green'))
    Widget.addWidget(CheckButton())
    Widget.addWidget(TextLabel(' Blue'))
    Widget.addWidget(TextLabel('Result:', Alignment= 'r'))
    Widget.addWidget(TextLabel(' ', Alignment= 'r', Background = 0))
    Widget.update()
    Position = 0
    while Key != StopKey:
        if Buffer.IsNotEmpty:
            Key = Buffer.get()
            if not isinstance(Key, ControlCode):
                CurrentWidth = Widget.Width
                if Key == 'KeyLEFT' or Key == 'KeyRIGHT':
                    if Key == 'KeyLEFT' and Position > 0:
                        Position -= 1
                    elif Key == 'KeyRIGHT' and Position < 2:
                        Position += 1
                    for Index in range(3):
                        Widget[2 * Index + 1].setStyle(BOLD = False)
                    Widget[2 * Position + 1].setStyle(BOLD = True)
                    Widget.update()
                elif Key == 'KeyUP':
                    Widget[2 * Position].toggleState()
                    Colour = 0
                    if Widget[0].Value:
                        Colour += 1
                    if Widget[2].Value:
                        Colour += 2
                    if Widget[4].Value:
                        Colour += 4
                    Widget[-1].setValue(' ', Background = Colour)
                    Widget.update()
    print('\nstoping the process, press any key')
    Buffer.deactivate()
    Buffer.empty()
    Listener.join()
    print('\nEnd of Demonstration')
"""
Module clui_lib.Tests.DT008_Spinner

Demonstration test for the module clui_lib.cli_ui.base_view_classes,
specifically - the class VContainer.
"""

__version__= '1.0.0.0'
__date__ = '30-07-2026'
__status__ = 'Testing'

#imports

#+standard libraries

import sys
import os
import time
import threading

from random import randint

#+other libraries

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from clui_lib.cli_ui.base_view_classes import OnOffButton, HContainer, TextLabel
from clui_lib.cli_ui.base_view_classes import VContainer

from clui_lib.cli_ui.line_widgets import SliderControlIndicator
from clui_lib.cli_ui.line_widgets import ProgressBarIndicator

if os.name == 'posix':
    from clui_lib.console.keystroke_posix import KeystrokesListener
    IS_POSIX = True
else:
    from clui_lib.console.keystroke_windows import KeystrokesListener
    IS_POSIX = False

from clui_lib.console.keystroke_common import ControlCode, InputBuffer

#helper functions

def UpdateView(Container: VContainer) -> None:
    Container.update()
    if Container[0][1].Value:
        ReadOut = randint(0, 99) + 3 * Container[1].Value
        ReadOut += 2 * Container[2].Value + Container[3].Value
        Container[4].setValue(ReadOut)
    else:
        Container[4].setValue(0)
    print('\n\nUse arrow keys to operate, "q" to exit')

if __name__ == '__main__':
    #creating all needed widgets
    FirstLine = HContainer()
    FirstLine.addWidget(TextLabel('Status:'))
    FirstLine.addWidget(OnOffButton())
    FirstLine.setWidth(FirstLine.MinWidth)
    SecondLine = SliderControlIndicator('Red  ', 255, Width = 20)
    ThirdLine = SliderControlIndicator('Green', 255, Width = 20)
    FourthLine = SliderControlIndicator('Blue ', 255, Width = 20)
    Container = VContainer(FirstLine, SecondLine, ThirdLine, FourthLine)
    Container.addWidget(ProgressBarIndicator(1650,
                                             ShowPercents= False , Width = 20))
    Container.show()
    print(f'\n\nCurrent width is {Container.Width}')
    print(f'Current minimal width is {Container.MinWidth}')
    print(f'Current height is {Container.Height}')
    for Width in [10, 20, 80, 1000, 80, 60]:
        time.sleep(3)
        Container.setWidth(Width)
        print(f'\n\nCurrent width is {Container.Width}')
        print(f'Current minimal width is {Container.MinWidth}')
        print(f'Current height is {Container.Height}')
        print(f'Attempted to set width = {Width}')
    time.sleep(3)
    Container[0][0].setStyle(BOLD = True, UNDERLINE = True)
    UpdateView(Container)
    StopKey = 'q'
    Delay = 0.0001
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
    Position = 0
    LastTimer = time.time()
    while Key != StopKey:
        if Buffer.IsNotEmpty:
            Key = Buffer.get()
            if not isinstance(Key, ControlCode):
                if Key == 'KeyUP' and Position:
                    Container[Position].setLabelStyle()
                    Position -= 1
                    if Position:
                        Container[Position].setLabelStyle(BOLD = True,
                                                        UNDERLINE = True)
                    else:
                        Container[0][0].setStyle(BOLD = True,
                                                        UNDERLINE = True)
                    UpdateView(Container)
                elif Key == 'KeyDOWN' and Position < 3:
                    if not Position:
                        Container[0][0].setStyle()
                    else:
                        Container[Position].setLabelStyle()
                    Position += 1
                    Container[Position].setLabelStyle(BOLD = True,
                                                            UNDERLINE = True)
                    UpdateView(Container)
                elif Key == 'KeyRIGHT':
                    if not Position:
                        Container[0][1].setValue(True)
                    else:
                        Container[Position].inc()
                    UpdateView(Container)
                elif Key == 'KeyLEFT':
                    if not Position:
                        Container[0][1].setValue(False)
                    else:
                        Container[Position].dec()
                    UpdateView(Container)
            else:
                if time.time() - LastTimer > 0.5:
                    UpdateView(Container)
                    LastTimer = time.time()
        else:
            if time.time() - LastTimer > 0.5:
                UpdateView(Container)
                LastTimer = time.time()
    print('\nstoping the process, press any key')
    Buffer.deactivate()
    Buffer.empty()
    Listener.join()
    print('\nEnd of Demonstration')
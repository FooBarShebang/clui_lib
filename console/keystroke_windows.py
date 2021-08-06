#usr/bin/python3
"""
Module clui_lib.console.keystroke_posix

Microsoft Windows specific implementation of the keyboard listener.

Based upon the ideas from
    * https://github.com/magmax/python-readchar =>
        Danny Yo & Stephen Chappell (http://code.activestate.com/recipes/134892)
    * https://code.activestate.com/
        recipes/197140-key-press-detection-for-windows-text-only-console-/
"""

__version__= '1.0.0.0'
__date__ = '06-08-2021'
__status__ = 'Development'

#imports

#+ standard libraries

import sys
import os

#+check that the OS is Windows NT-based, i.e. msvcrt will be available

if os.name != 'nt':
    print('This module is not compatible with you OS')
    sys.exit(1)

import msvcrt
import threading

#+ other DO libraries

MODULE_FOLDER = os.path.dirname(os.path.realpath(__file__))
LIB_FOLDER = os.path.dirname(MODULE_FOLDER)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from clui_lib.console.keystroke_common import InputBuffer #, ControlCode
#from clui_lib.console.keystroke_common import ASCII_CONTROL_CODES

#+ main functions to be executed in the separate threads

def KeystrokesListener(Buffer: InputBuffer) -> None:
    """
    """
    while Buffer.IsActive:
        if msvcrt.kbhit():
            Input = msvcrt.getwch()
            Code = ord(Input)
            if Code in [0, 224]: #control character
                ScanCode = int(Code + ord(msvcrt.getwch())*256)
                #TODO - map 1 byte control codes and 2-bytes control codes
                #+ onto key-presses
                Buffer.put(ScanCode)
            else:
                Buffer.put(Input)

def KeyboardListener(*, StopKey: str = 'q') -> None:
    """
    """
    print('starting the listening process, press "{}" to exit'.format(StopKey))
    Buffer = InputBuffer()
    Buffer.activate()
    Listener = threading.Thread(target = KeystrokesListener, args = (Buffer, ))
    Listener.start()
    Key = ''
    while Key != StopKey:
        if Buffer.IsNotEmpty:
            Key = Buffer.get()
            print('You pressed {}'.format(Key))
    print('stoping the process...')
    Buffer.deactivate()
    Buffer.empty()
    Listener.join()
    print('bye!')

#testing and demonstration area - execution entry point

if __name__ == '__main__':
    KeyboardListener()
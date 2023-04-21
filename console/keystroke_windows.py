#usr/bin/python3
"""
Module clui_lib.console.keystroke_windows

Microsoft Windows specific implementation of the keyboard listener.

Based upon the ideas from
    * https://github.com/magmax/python-readchar =>
        Danny Yo & Stephen Chappell (http://code.activestate.com/recipes/134892)
    * https://code.activestate.com/
        recipes/197140-key-press-detection-for-windows-text-only-console-/
"""

__version__= '1.0.0.0'
__date__ = '21-04-2023'
__status__ = 'Testing'

#imports

#+ standard libraries

import sys
import os

#+check that the OS is Windows NT-based, i.e. msvcrt will be available

if os.name == 'nt':
    print('This module is not compatible with you OS')
    sys.exit(1)

import msvcrt
import threading

#+ other DO libraries

from .keystroke_common import InputBuffer, ControlCode, ASCII_CONTROL_CODES

from .ibm_scancodes_mapping import ASCII_CONTROL_MAPPING, IBM_SC_MAPPING

#+ main functions to be executed in the separate threads

def KeystrokesListener(Buffer: InputBuffer) -> None:
    """
    """
    while Buffer.IsActive:
        if msvcrt.kbhit():
            Input = msvcrt.getwch()
            Code = ord(Input)
            if Code in [0, 224]: #control character
                #+ actual value b'\x00' or b'\xe0' may vary with the console
                #+ implementation, but not the second character
                Input = msvcrt.getwch()
                ScanCode = ord(Input)
                if ScanCode in IBM_SC_MAPPING:
                    Buffer.put(IBM_SC_MAPPING[ScanCode])
                else:
                    Buffer.put('Scancode sequence ({},{})'.format(Code,
                                                                    ScanCode))
            elif Code in ASCII_CONTROL_CODES:
                Buffer.put(ASCII_CONTROL_MAPPING.get(ASCII_CONTROL_CODES[Code],
                                                                'Undefined'))
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
            if isinstance(Key, ControlCode):
                print('You pressed {}'.format(' or '.join(Key.Keys)))
            else:
                print('You pressed {}'.format(Key))
    print('stoping the process...')
    Buffer.deactivate()
    Buffer.empty()
    Listener.join()
    print('bye!')

#testing and demonstration area - execution entry point

if __name__ == '__main__':
    KeyboardListener()
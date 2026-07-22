"""
Module clui_lib.console.keystroke_windows

Microsoft Windows specific implementation of the keyboard listener.

Based upon the ideas from
    * https://github.com/magmax/python-readchar =>
        Danny Yo & Stephen Chappell (http://code.activestate.com/recipes/134892)
    * https://code.activestate.com/
        recipes/197140-key-press-detection-for-windows-text-only-console-/

Functions:
    KeystrokesListener(Buffer)
        clui_lib.console.keystroke_abc.InputBuffer -> None
    KeyboardListener(*, StopKey = 'q')
        /*, str/ -> None
"""

__version__= '1.0.0.0'
__date__ = '21-04-2023'
__status__ = 'Production'

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
    This function is designed to be executed in a separate thread. It uses low
    level console I/O API of MS VC++ runtime - msvcrt - to detect a keystroke
    and pull a wide character (Unicode) from the console's buffer.
    
    The process is terminated after the output buffer is deactivated.
    
    Signature:
        clui_lib.console.keystroke_abc.InputBuffer -> None
    
    Args:
        Buffer: InputBuffer; a queue-like object serving as the data exchange
            output buffer as well as to signal the function to terminate
    
    Version 1.0.0.0
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
    This function serves only for the demonstration and self-testing purposes.
    It illustrates how the keystrokes listener function can be used by
    implementing a simple indefinite events processing loop with the conditional
    termination upon pressing a specific key.
    
    Signature:
        /*, str/ -> None

    Args:
        StopKey: (keyword) str; key or a combination of keys (Ctrl, Alt, Shift
            + another key) signaling to exit the loop
    
    Version 1.0.0.0
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

#usr/bin/python3
"""
"""

#imports

#+ standard libraries

import sys
import os

#+check that the OS is POSIX, i.e. termios will be available

if os.name != 'posix':
    print('This module is not compatible with you OS')
    sys.exit(1)

import subprocess
import threading
import time
import termios
import tty

from typing import List, Union

#+ other DO libraries

MODULE_FOLDER = os.path.dirname(os.path.realpath(__file__))
LIB_FOLDER = os.path.dirname(MODULE_FOLDER)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from clui_lib.console.keystroke_abc import InputBuffer, ControlCode
from clui_lib.console.keystroke_abc import ASCII_CONTROL_CODES

#globals


#check terminal type

TerminalType = subprocess.check_output('echo $TERM', shell = True)[:-1]

if TerminalType in [b'xterm-new', b'xterm-256color']:
    from clui_lib.console.xterm_new_mapping import ASCII_CONTROL_MAPPING
    from clui_lib.console.xterm_new_mapping import CSI_MAPPING
else:
    print('Unsupported terminal type {}'.format(TerminalType))
    sys.exit(1)

DEF_DELAY = 0.0001 #100 us - distinction between 2+ keystrokes and an escape
#+ sequence, also how often the input is checked!

#functions

#+ helper functions

def SplitCharacters(Data: str) -> List[Union[str, ControlCode]]:
    """
    Signature:
        str -> list(str OR ControlCode)
    """
    Result = []
    for Char in Data:
        if ord(Char) in ASCII_CONTROL_CODES:
            Name = ASCII_CONTROL_CODES[ord(Char)]
            Result.append(ControlCode(Name, ASCII_CONTROL_MAPPING[Name]))
        else:
            Result.append(Char)
    return Result

def ParseEscapeSequence(Data: bytes) -> List[Union[str, ControlCode]]:
    """
    Signature:
        bytes -> list(str OR ControlCode)
    """
    Result = []
    EscapedBuffer = []
    iIndex = 0
    #removing the possible preceding non-escaped characters
    while Data[iIndex] != 27:
        iIndex += 1
    if iIndex > 0:
        Temp = SplitCharacters(Data[:iIndex].decode('utf_8'))
        Result.extend(Temp)
    iStart = iIndex
    iIndex += 1
    while iIndex < len(Data):
        if Data[iIndex] == 27: #start of new escape sequence
            EscapedBuffer.append(Data[iStart : iIndex])
            iStart = iIndex
        iIndex += 1
    EscapedBuffer.append(Data[iStart : iIndex])
    for Escaped in EscapedBuffer:
        if Escaped in CSI_MAPPING:
            Result.append(CSI_MAPPING[Escaped])
        elif len(Escaped) >= 2:
            if 32 <= Escaped[1] < 127:
                Result.append('Alt-{}'.format(chr(Escaped[1])))
                if len(Escaped) > 2:
                    Temp = SplitCharacters(Escaped[2:].decode('utf_8'))
                    Result.extend(Temp)
            else:
                for iIndex in range(len(Escaped) - 1, 1, -1):
                    Clipped = Escaped[:iIndex]
                    if Clipped in CSI_MAPPING:
                        Result.append(Clipped)
                        Temp = SplitCharacters(Escaped[iIndex:].decode('utf_8'))
                        Result.extend(Temp)
                        break
        else:
            Result.append(ControlCode('ESC', ASCII_CONTROL_MAPPING['ESC']))
    return Result

#+ main function to be executed in the separate threads

def StdinListener(Buffer: InputBuffer) -> None:
    """
    This function is designed to be executed in a separate thread. It constantly
    tries to read from the stdin set into 'raw' state one character at the time,
    which is a blocking process. As soon as a character is read-out, it is sent
    into the passed data exchange buffer queue. The process is terminated after
    the buffer is deactivated and one more character is read-out from the stdin.
    
    Signature:
        InputBuffer -> None
    
    Args:
        Buffer: clui_lib.console.keystroke_abc.InputBuffer; a queue-like
            object serving as the data exchange buffer as well as to signal
            the function to terminate
    
    Version 1.0.0.0
    """
    original_settings = termios.tcgetattr(sys.stdin)
    
    try:
        tty.setcbreak(sys.stdin) #set terminal in the 'raw' input state
        buffer_string = ''
        while Buffer.IsActive:
            buffer_string = sys.stdin.read(1)
            Buffer.put(buffer_string)
    except Exception as err:
        print(err.__class__.__name__, ':', err)
    finally:
        #set the terminal back into the buffered state
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_settings)

def KeystrokesListener(Buffer: InputBuffer, Delay: float) -> None:
    """
    This function is designed to be executed in a separate thread. It constantly
    tries to read as many characters as possible (available) from its internal
    buffer, which is also connected to a listener of the stdin stream, running
    in a separate process. The received characters are split into the separate
    Unicode characters, control codes and escape control sequences. The later
    two are replaced by their symbolic representation. The results are placed
    into the output buffer (queue-like), which is passed as the argument.
    
    The second argument is the delay time in seconds, which determines how
    often the internal buffer is pulled. The recommended value is ~ 0.0001 (i.e.
    100 us), which is short enough to distinguish between the consecutive key
    presses (or the same characters emitted with a key being held down), but
    long enough to accumulate the entire escape sequence.
    
    The process is terminated after the output buffer is deactivated, and the
    stdin listener's thread finishes, which require one more character to be
    read-out from the stdin.
    
    Signature:
        InputBuffer -> None
    
    Args:
        Buffer: clui_lib.console.keystroke_abc.InputBuffer; a queue-like
            object serving as the data exchange output buffer as well as to
            signal the function to terminate
        Delay: float; frequency of the pulling the input buffer in seconds
    
    Version 1.0.0.0
    """
    InBuffer = InputBuffer()
    InBuffer.activate()
    Listener = threading.Thread(target = StdinListener, args = (InBuffer, ))
    Listener.start()
    Input = ''
    while Buffer.IsActive:
        while InBuffer.IsNotEmpty:
            Input += InBuffer.get()
        if Input != '':
            if len(Input) == 1:
                Code = ord(Input)
                if (Code <= 32) or (Code == 127):
                    Name = ASCII_CONTROL_CODES[Code]
                    Keys = ASCII_CONTROL_MAPPING.get(Name, 'Undefined')
                    Buffer.put(ControlCode(Name, Keys))
                else:
                    Buffer.put(Input)
            else:
                Encoded = bytes(Input, 'utf-8')
                if b'\x1b' in Encoded:
                    for Entry in ParseEscapeSequence(Encoded):
                        Buffer.put(Entry)
                else:
                    for Entry in SplitCharacters(Input):
                        Buffer.put(Entry)
        Input = ''
        time.sleep(Delay)
    InBuffer.deactivate()
    InBuffer.empty()
    Listener.join()

def KeyboardListener(*, Delay: float = DEF_DELAY, StopKey: str = 'q') -> None:
    """
    This function serves only for the demonstration and self-testing purposes.
    It illustrates how the keystrokes listener function can be used.
    
    Args:
        
    """
    print('starting the listening process, press "{}" to exit'.format(StopKey))
    Buffer = InputBuffer()
    Buffer.activate()
    Listener = threading.Thread(target = KeystrokesListener,
                                                        args = (Buffer, Delay))
    Listener.start()
    Key = ''
    while Key != StopKey:
        if Buffer.IsNotEmpty:
            Key = Buffer.get()
            if isinstance(Key, ControlCode):
                print('You pressed {}'.format(' or '.join(Key.Keys)))
            else:
                print('You pressed {}'.format(Key))
    print('stoping the process, press any key')
    Buffer.deactivate()
    Buffer.empty()
    Listener.join()
    print('bye!')

if __name__ == '__main__':
    KeyboardListener()
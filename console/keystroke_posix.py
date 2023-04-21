#usr/bin/python3
"""
Module clui_lib.console.keystroke_posix

POSIX-compatible implementation of the keyboard presses events based on the
processing of the content of the stdin via tty and termios Standard Libraries
functionality.

Based upon the ideas from
    * https://stackoverflow.com/questions/2408560/
    * https://stackoverflow.com/questions/21791621/
    * https://stackoverflow.com/questions/18018033/
    * https://stackoverflow.com/questions/292095/
    * https://github.com/magmax/python-readchar => 
        Danny Yo & Stephen Chappell (http://code.activestate.com/recipes/134892)

Functions:
    SplitCharacters(Data)
        str -> list(str OR clui_lib.console.keystroke_abc.ControlCode)
    ParseEscapeSequence
        str -> list(str OR clui_lib.console.keystroke_abc.ControlCode)
    StdinListener(Buffer)
        clui_lib.console.keystroke_abc.InputBuffer -> None
    KeystrokesListener(Buffer, Delay)
        clui_lib.console.keystroke_abc.InputBuffer -> None
    KeyboardListener(*, Delay = DEF_DELAY, StopKey = 'q')
        /*, float/, str// -> None
"""

__version__= '1.0.0.1'
__date__ = '21-04-2023'
__status__ = 'Testing'

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

from .keystroke_common import InputBuffer, ControlCode, ASCII_CONTROL_CODES

#globals

#+ supported terminal types

XTERM_NEW = [b'xterm-new', b'xterm-256color']

#check terminal type

TerminalType = subprocess.check_output('echo $TERM', shell = True)[:-1]

if TerminalType in XTERM_NEW:
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
    Splits the input string, which may containg multiple Unicode printable
    characters and / or unprintable character (control codes), into a list of
    1-character strings and instances of ControlCode class.

    Signature:
        str -> list(str OR clui_lib.console.keystroke_abc.ControlCode)
    
    Args:
        Data: str; the Unicode string input containg one or more Unicode
            characters (printable or non-printable, as control codes), but no
            CSI sequences
    
    Returns:
        list(str OR ControlCode); the simultaneous multple keys being pressed
            split into separate key-presses, whilst the Ctrl presses generating
            a control command are stil grouped with a key, which they modified,
            e.g. 'Ctrl-p', which is represented by a corresponding instance of
            ControlCode class
    
    Version 1.0.0.0
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
    Splits the passed bytestring into a sequence of proper printable Unicode
    characters, 1-byte control codes and multiple bytes CSI escape sequences
    assuming UTF-8 codec. The printable Unicode characters are returned as
    1-element strings, the 1-bye control codes - as instances of the ControlCode
    class, and the CSI escape sequences - as strings reflecting the actual keys
    being pressed, e.g. 'Ctrl-Alt-p'.

    Signature:
        bytes -> list(str OR clui_lib.console.keystroke_abc.ControlCode)
    
    Args:
        Data: bytes; the UTF-8 encoded input containg one or more Unicode
            characters (printable or non-printable, as control codes) and / or
            CSI sequences
    
    Returns:
        list(str OR ControlCode); the simultaneous multple keys being pressed
            split into separate key-presses, whilst the Ctrl, Alt and Shift
            presses are stil grouped with a key, which they modified, e.g.
            'Ctrl-Alt-p'
    
    Version 1.0.0.1
    """
    Result = []
    EscapedBuffer = []
    Index = 0
    #removing the possible preceding non-escaped characters
    while Data[Index] != 27:
        Index += 1
    if Index:
        Temp = SplitCharacters(Data[:Index].decode('utf_8'))
        Result.extend(Temp)
    Start = Index
    Index += 1
    while Index < len(Data):
        if Data[Index] == 27: #start of new escape sequence
            EscapedBuffer.append(Data[Start : Index])
            Start = Index
        Index += 1
    EscapedBuffer.append(Data[Start : Index])
    for Escaped in EscapedBuffer:
        if Escaped in CSI_MAPPING:
            Result.append(CSI_MAPPING[Escaped])
        elif len(Escaped) >= 2:
            if 32 <= Escaped[1] < 127:
                Result.append(f'Alt-{chr(Escaped[1])}')
                if len(Escaped) > 2:
                    Temp = SplitCharacters(Escaped[2:].decode('utf_8'))
                    Result.extend(Temp)
            else:
                for Index in range(len(Escaped) - 1, 1, -1):
                    Clipped = Escaped[:Index]
                    if Clipped in CSI_MAPPING:
                        Result.append(Clipped)
                        Temp = SplitCharacters(Escaped[Index:].decode('utf_8'))
                        Result.extend(Temp)
                        break
        else:
            Result.append(ControlCode('ESC', ASCII_CONTROL_MAPPING['ESC']))
    return Result

#+ main functions to be executed in the separate threads

def StdinListener(Buffer: InputBuffer) -> None:
    """
    This function is designed to be executed in a separate thread. It constantly
    tries to read from the stdin set into 'raw' state one character at the time,
    which is a blocking process. As soon as a character is read-out, it is sent
    into the passed data exchange buffer queue. The process is terminated after
    the buffer is deactivated and one more character is read-out from the stdin.
    
    Signature:
        clui_lib.console.keystroke_abc.InputBuffer -> None
    
    Args:
        Buffer: InputBuffer; a queue-like object serving as the data exchange
            buffer as well as to signal the function to terminate
    
    Version 1.0.0.0
    """
    original_settings = termios.tcgetattr(sys.stdin)
    
    try:
        tty.setcbreak(sys.stdin) #set terminal in the 'cbreak' input state
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
        clui_lib.console.keystroke_abc.InputBuffer -> None
    
    Args:
        Buffer: InputBuffer; a queue-like object serving as the data exchange
            output buffer as well as to signal the function to terminate
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
                if Code in ASCII_CONTROL_CODES:
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
    It illustrates how the keystrokes listener function can be used by
    implementing a simple indefinite events processing loop with the conditional
    termination upon pressing a specific key.
    
    Signature:
        /*, float/, str// -> None

    Args:
        Delay: (keyword) float; delay in seconds between the successive pulls
            from the key-presses buffer, defaults to the global varaible
            DEF_DELAY
        StopKey: (keyword) str; key or a combination of keys (Ctrl, Alt, Shift
            + another key) signaling to exit the loop
    
    Version 1.0.0.0
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

#testing and demonstration area - execution entry point

if __name__ == '__main__':
    KeyboardListener()
"""
Module clui_lib,console.clear_screen

Implements functions to clear the terminal output.

Functions:
    _ClearScreenPosix()
        None -> None
    _ClearScreenNT()
        None -> None
    _ClearScreenForced()
        None -> None
    ClearScreen()
        None -> None
"""

__version__= '1.0.0.0'
__date__ = '21-07-2026'
__status__ = 'Production'

#imports

#+ standard libraries

import os
import subprocess

#functions

def _ClearScreenPosix() -> None:
    """
    Posix (Linux, Unix, MacOS) specific implementation using system API call.

    Signature:
        None -> None
    
    Version 1.0.0.0
    """
    subprocess.run('clear')

def _ClearScreenNT() -> None:
    """
    MS Windows NT and later specific implementation using system API call.

    Signature:
        None -> None
    
    Version 1.0.0.0
    """
    subprocess.run('cls')

def _ClearScreenForced() -> None:
    """
    Generic brute force implementation using printing of multiple newlines.

    Signature:
        None -> None
    
    Version 1.0.0.0
    """
    ScreenSize = os.get_terminal_size()
    print('\n' * ScreenSize.lines)

def ClearScreen() -> None:
    """
    Generic, platform independent (for standard terminals) implementation of 
    'clear screen' functionality.

    Signature:
        None -> None
    
    Version 1.0.0.0
    """
    if os.name == 'nt':
        _ClearScreenNT()
    elif os.name == 'posix':
        _ClearScreenPosix()
    else:
        _ClearScreenForced()
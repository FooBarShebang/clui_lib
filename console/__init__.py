#!/usr/bin/python3
"""
Package clui_lib.console

Miscelaneous tools related to the console output and unbuffered, real-time
console input.

Modules:
    keystroke_common: data exchange classes common to all implementations of
        a keyboard listener
    keystroke_posix: POSIX specific implementation of a keyboard listener based
        on the analysis of the content of stdin stream
    xterm_new_mapping: CSI codes -> keys presses mapping specific for the
        xterm-new and compatible implementations of the virtual terminal
    keystroke_windows: Microsoft Windows specific implementation of a keyboard
        listener based on the msvcrt module's functionality
    ibm_scancodes_mapping: IBM scancodes -> keys pressed mapping (Windows)
"""

__version__= '0.2.0.1'
__date__ = '19-04-2023'
__status__ = 'Developement'

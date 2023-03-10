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
    xterm_colours: POSIX-specific coloration of the console output based on
        the control codes
"""

__version__= '0.3.0.0'
__date__ = '10-03-2023'
__status__ = 'Developement'

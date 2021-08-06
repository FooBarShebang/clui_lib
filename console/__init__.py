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
"""

__version__= '0.1.0.0'
__date__ = '06-08-2021'
__status__ = 'Developement'

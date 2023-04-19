#!/usr/bin/python3
"""
Package clui_lib.cli_ui

Implements a set of CLI widgets to provide an interactive feedback on the long
running processes. It is intended for the actual CLI usage, however, the TUI
(Text User Interface) can be build on top of this package.

Modules:
    base_view_classes: simple widgets to show dynamic data in CLI
    line_widgets: compound widgets fitting one line in CLI, e.g. Progress Bar
        Indicator, etc.
"""

__version__= '0.1.0.1'
__date__ = '19-04-2023'
__status__ = 'Developement'

__all__ = ['line_widgets', 'base_view_classes']
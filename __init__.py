#!/usr/bin/python3
"""
Library clui_lib

Implements a set of CLI widgets to provide an interactive feedback on the long
running processes.

Modules:
    base_view_classes: simple widgets to show dynamic data in CLI
    line_widgets: compound widgets fitting one line in CLI, e.g. Progress Bar
        Indicator, etc.

"""

__project__ ='Command Line User Interface'
__version_info__= (0, 1, 0)
__version_suffix__= '-dev1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '10-12-2020'
__status__ = 'Development'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['line_widgets', 'base_view_classes']
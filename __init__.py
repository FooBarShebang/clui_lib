#!/usr/bin/python3
"""
Library clui_lib

Implements a set of CLI widgets to provide an interactive feedback on the long
running processes or to create enchanced command-line or even text-based user
interface applications.

Packages:
    cli_ui: actual CLI widgets with API, and processing of the typed commands
        input
    console: miscelaneous tools related to the console output and keyboard
        listening

"""

__project__ ='Command Line User Interface Tools'
__version_info__= (0, 1, 2)
__version_suffix__= '-dev1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '19-04-2023'
__status__ = 'Development'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['cli_ui', 'console']
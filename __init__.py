#!/usr/bin/python3
"""
Library clui_lib

Implements a set of CLI widgets to provide an interactive feedback on the long
running processes.

Packages:
    cli_ui: actual CLI widgets, with the user input based on commands typing,
        not keystrokes listening

"""

__project__ ='Command Line User Interface'
__version_info__= (0, 1, 1)
__version_suffix__= '-dev1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '11-12-2020'
__status__ = 'Development'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['cli_ui']
#usr/bin/python3
"""
Module clui_lib.console.xterm_colours

Implements colouration of the console output using the control codes. This
module is POSIX-specific.

Classes:
    Colours8: enumeration, 1-bit RGB colours palette (8 colours)
    Colours8B: enumeration, 1-bit RGB colours palette (8 colours), high
        intensity
    Attributes: enumeration, additional attributes (codes)
    ColouredBuffer: variable length coloured text buffer

Functions:
    Colorize(Data, *, Foreground, Background, Bold, Underline, Invert):
        type A/, int OR None, int OR None, dict(str -> bool)/ -> str
"""

__version__= '1.0.0.0'
__date__ = '10-03-2023'
__status__ = 'Development'

#imports

#+ standard libraries

import sys
import os
import warnings

#+check that the OS is POSIX, i.e. termios will be available

if os.name != 'posix':
    warnings.warn('This module is not compatible with you OS')

from enum import IntEnum

from typing import Any, Optional, Dict

#+ other DO libraries

MODULE_FOLDER = os.path.dirname(os.path.realpath(__file__))
LIB_FOLDER = os.path.dirname(MODULE_FOLDER)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError
from introspection_lib.base_exceptions import UT_KeyError

#globals

#+ console codes

PREFIX = '\033['

SUFFIX = 'm'

SEPARATOR = ';'

BACKGROUND = '48:5:' #using 256 colours palette

FOREGROUND = '38:5:' #using 256 colours palette

RESET = 0

#+ enumerations

class Colours8(IntEnum):
    """
    1-bit colour depth RGB space implementing 8 colours available in the xterm.

    Sub-classes enum.IntEnum.

    Attributes:
        BLACK: int; = 0
        RED: int; = 1
        GREEN: int; = 2
        YELLOW: int; = 3
        BLUE: int; = 4
        MAGENTA: int; = 5
        CYAN: int; = 6
        WHITE: int; = 7
    
    Version 1.0.0.0
    """

    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3 #RED + GREEN
    BLUE = 4
    MAGENTA = 5 #RED + BLUE
    CYAN = 6 #GREEN + BLUE
    WHITE = 7 #RED + GREEN + BLUE

class Colours8B(IntEnum):
    """
    1-bit colour depth RGB space implementing 8 colours available in the xterm
    with the enhanced brightness.

    Sub-classes enum.IntEnum.

    Attributes:
        BLACK: int; = 8
        RED: int; = 9
        GREEN: int; = 10
        YELLOW: int; = 11
        BLUE: int; = 12
        MAGENTA: int; = 13
        CYAN: int; = 14
        WHITE: int; = 15
    
    Version 1.0.0.0
    """

    BLACK = 8
    RED = 9
    GREEN = 10
    YELLOW = 11 #RED + GREEN
    BLUE = 12
    MAGENTA = 13 #RED + BLUE
    CYAN = 14 #GREEN + BLUE
    WHITE = 15 #RED + GREEN + BLUE

class Attributes(IntEnum):
    """
    Additional attributes as bold, underlined or inverse colours.

    Sub-classes enum.IntEnum.

    Attributes:
        BOLD: int; = 1
        FAINT: int; = 2
        ITALIC: int; = 3
        UNDERLINE: int; = 4
        INVERSE: int; = 7
        HIDE: int; = 8 - not visible
        STRIKE: int; = 9 - through strike
        DOUBLE: int; = 21 - double understrike
    
    Version 1.0.0.0
    """

    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    INVERSE = 7
    HIDE = 8
    STRIKE = 9
    DOUBLE = 21

#+ available attributes

ALL_ATTRIBUTES = [Item.name for Item in Attributes]

#+ pallete - 256 colours

MIN_INDEX = 0

MAX_INDEX = 256

# functions

def Colorize(Data: Any, *, Foreground: Optional[int] = None,
                        Background: Optional[int] = None,
                        **kwargs: Dict[str, bool]) -> str:
    """
    Prepares a string with (optional) background and foreground colours changed
    as well as (optional) boldness, underline, inverse, etc. attributes, which
    can be directly printed into the console terminals supporting ASCII control
    sequences, e.g. POSIX terminals like xterm. The attributes and colours reset
    code is added to the end, if any colour or atribute were altered.

    The recognized attribute names are: BOLD, ITALIC, FAINT, UNDERLINE, DOUBLE,
    STRIKE, HIDE.

    Signature:
        type A/, int OR None, int OR None, dict(str -> bool)/ -> str
    
    Arguments:
        Data: type A; any data to be converted into a string
        Foreground: (keyword) int OR None; foreground (font) colour, enumeration
            members can be used as well; defaults to None
        Background: (keyword) int; background colour, enumeration members can be
            used as well; defaults to None
            Colours enumeration
        kwargs: (keyword) str -> bool; dictionary of the atributes like bold,
            underline, etc. - see enumeration Attributes for the allowed
            key names
    
    Returns:
        str; the passed data converted to the string data type with ASCII
            control sequences as prefix and suffix when required
    
    Raises:
        UT_TypeError: either Foreground or Background keyword attribute is not
            an integer value or IntEnum member
        UT_ValueError: either Foreground or Background keyword attribute value
            is not a member of Colours enumeration
        UT_KeyError: either of the additional keyword arguments (attributes)
            is not recognized
    
    Version 1.0.0.0
    """
    Codes = list()
    for Name, Value in kwargs.items():
        if not Name in ALL_ATTRIBUTES:
            raise UT_KeyError('xterm_colours.Attibutes', Name, SkipFrames = 1)
        if Value:
            Codes.append(int(Attributes[Name]))
    if not (Foreground is None):
        if not isinstance(Foreground, int):
            objError = UT_TypeError(Foreground, int, SkipFrames = 1)
            objError.args = (objError.args[0] + '- Foreground argument', )
            raise objError
        elif not (MIN_INDEX <= Foreground <= MAX_INDEX):
            raise UT_ValueError(Foreground,
                'in range [{}, {}] colours palette, Foreground argument'.format(
                                        MIN_INDEX, MAX_INDEX), SkipFrames = 1)
        Codes.append('{}{}'.format(FOREGROUND, Foreground))
    if not (Background is None):
        if not isinstance(Background, int):
            objError = UT_TypeError(Background, int, SkipFrames = 1)
            objError.args = (objError.args[0] + '- Background argument', )
            raise objError
        elif not (MIN_INDEX <= Background <= MAX_INDEX):
            raise UT_ValueError(Background,
                'in range [{}, {}] colours palette, Background argument'.format(
                                        MIN_INDEX, MAX_INDEX), SkipFrames = 1)
        Codes.append('{}{}'.format(BACKGROUND, Background))
    if not len(Codes):
        Result = str(Data)
    else:
        Result = '{}{}{}{}{}{}{}'.format(PREFIX,
                                            SEPARATOR.join(map(str, Codes)),
                                            SUFFIX, str(Data),
                                            PREFIX, RESET, SUFFIX)
    return Result

#main classes

class ColouredBuffer:
    """
    Properties:
        Last: (read-only) str; the last input
        Data: (read-only) str; the all accumulated sub-strings

    Methods:
        put(Data, *, Foreground, Background, Bold, Underline, Invert):
            type A/, int, int, dict(str -> bool)/ -> str
        print():
            None -> None

    Version 1.0.0.0
    """

    #private methods

    def _reset(self) -> None:
        """
        Helper private method. Sets all colours and attributes to the default
        console look (white on black, no attributes). Empties the string
        buffers.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        self._iForeground = None
        self._iBackground = None
        self._dictAttributes = {Name : False for Name in ALL_ATTRIBUTES}
        self._strData = ''
        self._strLast = ''

    #special magic methods

    def __init__(self) -> None:
        """
        Initialization. Sets all colours and attributes to the default console
        look (white on black, no attributes). Creates empty string buffers.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        self._reset()
    
    #public API

    #+properties

    @property
    def Last(self) -> str:
        """
        Read-only property returning the last sub-string passed into the buffer
        with all colours and attributes applied. The revert to normal console
        code is added to the tail.

        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return Colorize(self._strLast, Foreground = self._iForeground,
                            Background= self._iBackground, Bold = self._bBold,
                            Underline = self._bUnderline, Invert= self._bInvert)

    @property
    def Data(self) -> str:
        """
        Read-only property returning the all accumulated sub-strings with the
        respective colours and attributes applied. The revert to normal console
        control code is added to the tail.

        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        Result = str(self._strData)
        Result += '{}{}{}'.format(PREFIX, RESET, SUFFIX)
        return Result

    #+ instance methods

    def put(self, Data: Any, *, Foreground: Optional[int] = None,
                        Background: Optional[int] = None,
                        **kwargs: Dict[str, bool]) -> None:
        """
        Adds a sub-string into the buffer with (optional) background and
        foreground colours changed as well as (optional) boldness, underline and
        inverse attributes, which can be directly printed into the console
        terminals supporting ASCII control sequences, e.g. POSIX terminals like
        xterm. The specific control codes are inserted only when the state of
        the stream is changed.

        The recognized attribute names are: BOLD, ITALIC, FAINT, UNDERLINE,
        DOUBLE, STRIKE, HIDE.

        Signature:
            type A/, int, int, dict(str -> bool)/ -> None
        
        Arguments:
            Data: type A; any data to be converted into a string
            Foreground: (keyword) int; foreground (font) colour - any member
                value of the Colours enumeration
            Background: (keyword) int; backgroundcolour - any member value of
                the Colours enumeration
            kwargs: (keyword) str -> bool; dictionary of the atributes like
                bold, underline, etc. - see enumeration Attributes for the
                allowed key names
        
        Returns:
            str; the passed data converted to the string data type with ASCII
                control sequences as prefix and suffix when required
        
        Raises:
            UT_TypeError: either Foreground or Background keyword attribute is
                not an integer value or IntEnum member
            UT_ValueError: either Foreground or Background keyword attribute
                value is not a member of Colours enumeration
            UT_KeyError: either of the additional keyword arguments (attributes)
                is not recognized
        
        Version 1.0.0.0
        """
        bReset = False
        Codes = list()
        for Name, Value in kwargs.items():
            if not Name in ALL_ATTRIBUTES:
                raise UT_KeyError('xterm_colours.Attibutes', Name,
                                                                SkipFrames = 1)
            if Value != self._dictAttributes[Name]:
                if Value:
                    Codes.append(int(Attributes[Name]))
                else:
                    bReset = True
                self._dictAttributes[Name] = Value
        for Name in self._dictAttributes.keys():
            if not (Name in kwargs):
                bReset = True
                self._dictAttributes[Name] = False
        if not (Foreground is None):
            if not isinstance(Foreground, int):
                objError = UT_TypeError(Foreground, int, SkipFrames = 1)
                objError.args = (objError.args[0] + '- Foreground argument', )
                raise objError
            elif not (MIN_INDEX <= Foreground <= MAX_INDEX):
                raise UT_ValueError(Foreground,
                'in range [{}, {}] colours palette, Foreground argument'.format(
                                        MIN_INDEX, MAX_INDEX), SkipFrames = 1)
            if (self._iForeground is None) or Foreground != self._iForeground:
                Codes.append('{}{}'.format(FOREGROUND, Foreground))
        elif not (self._iForeground is None):
            if (len(Codes) and Codes[0] != 0) or not len(Codes):
                bReset = True
        self._iForeground = Foreground
        if not (Background is None):
            if not isinstance(Background, int):
                objError = UT_TypeError(Background, int, SkipFrames = 1)
                objError.args = (objError.args[0] + '- Background argument', )
                raise objError
            elif not (MIN_INDEX <= Background <= MAX_INDEX):
                raise UT_ValueError(Background,
                'in range [{}, {}] colours palette, Background argument'.format(
                                        MIN_INDEX, MAX_INDEX), SkipFrames = 1)
            if (self._iBackground is None) or Background != self._iBackground:
                Codes.append('{}{}'.format(BACKGROUND, Background))
        elif not (self._iBackground is None):
            if (len(Codes) and Codes[0] != 0) or not len(Codes):
                bReset = True
        self._iBackground = Background
        if bReset:
            Codes = [RESET]
            for Name, Value in self._dictAttributes.items():
                if Value:
                    Codes.append(int(Attributes[Name]))
            if not (self._iForeground is None):
                Codes.append('{}{}'.format(FOREGROUND, self._iForeground))
            if not (self._iBackground is None):
                Codes.append('{}{}'.format(BACKGROUND, self._iBackground))
        self._strLast = str(Data)
        if not len(Codes):
            Result = self._strLast
        else:
            Result = '{}{}{}{}'.format(PREFIX, SEPARATOR.join(map(str, Codes)),
                                                        SUFFIX, self._strLast)
        self._strData += Result
    
    def print(self):
        """
        Prints the content of the entire accumulated buffer, clears all settings
        to the defaults and the empties the buffers.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        print(self.Data)
        self._reset()

if __name__ == '__main__':
    print(Colorize('whatever', Foreground = Colours8B.RED,
                    Background = Colours8.GREEN, BOLD = True, ITALIC = True))
    objTest = ColouredBuffer()
    objTest.put('Hello, ')
    objTest.put('Nicole', Foreground = Colours8B.RED,
                            Background = Colours8.GREEN,
                            BOLD = True, ITALIC = True)
    objTest.put(', my dear', ITALIC = True, DOUBLE = True)
    objTest.put('!')
    Repr = repr(objTest.Data)
    objTest.print()
    print(Repr)
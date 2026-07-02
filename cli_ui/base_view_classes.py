"""
Module clui_lib.base_view_classes

Implements the base classes providing the visiual representation of the widgets
in a text console. Although these classes are designed to serve as the output
interface or component of more complex widgets, the text label, slider and
progress bar classes can be used as stand-alone widgets as well.

Classes:
    CLUI_ABC: abstract base class - super class - top of the hierachy
    HWidget_ABC: abstract base class - prototype for all simple single line
        widgets' views
    BarControl_ABC: abstract base class - prototype for widgets having a dynamic
        position representation of the internal state, like a progress bar or
        a slider
    ScalableWidth: mixin, implements functionality to change the widget's width
        during runtime
    TextLabel: fixed width, variable content text label widget
    TextLabelVW: variable width and content text label widget, the stored
        string value will never be truncated
    Slider: CLI representation of a slider widget - fixed width, minimum width
        is 5, internal value is a float from 0.0 to 1.0 inclusively
    SliderVW: CLI representation of a slider widget - variable width, minimum
        width is 5, internal value is a float from 0.0 to 1.0 inclusively
    ProgressBar: CLI representation of a progress bar widget - fixed width,
        minimum width is 5, internal value is a float from 0.0 to 1.0
        inclusively
    ProgressBarVW: CLI representation of a progress bar widget - variable width,
        minimum width is 5, internal value is a float from 0.0 to 1.0
        inclusively
    HContainer: container to stack zero, one or more simple single line widgets
        into a single line representation in the text console
"""

__version__= '1.1.0.0'
__date__ = '02-07-2026'
__status__ = 'Development'

#imports

#+standard libraries

import sys
import os
import abc

from unicodedata import normalize

from typing import Any, Optional, Union, ClassVar

#+other libraries

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from introspection_lib.base_exceptions import UT_ValueError, UT_TypeError
from introspection_lib.base_exceptions import UT_Exception

from ..console.xterm_colours import ALL_ATTRIBUTES, MIN_INDEX, MAX_INDEX

from .widgets_decorators import ProgressBarDecoratorSimple

if os.name == 'posix':
    from ..console.xterm_colours import Colorize
    IS_POSIX = True
else:
    IS_POSIX = False

#helper functions

def ColorizeDummy(Data: Any, **kwargs) -> str:
    """
    Dummy replacement for clui_lib.console.xterm_colours.Colorize() function
    in the case of non-posix OS, i.e without x-term. Simply converts the passed
    value into a string and returns this string. All passed keyword arguments
    are ignored.

    Signature:
        type A/, **kwargs/ -> str
    """
    return str(Data)

ColorizeFunc = ColorizeDummy if not IS_POSIX else Colorize

#classes

class CLUI_ABC(abc.ABC):
    """
    Abstract Base Class as the root of the widget views classes hierarchy. The
    methods clear() and getStringValue() are abstract (virtual) - must be
    implemented by the sub-classes.

    Methods:
        clear():
            None -> None
        show():
            None -> None
        update():
            None -> None
        getStringValue():
            None -> str
    
    Version 1.1.0.0
    """

    #special methods

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """
        Stub to prevent instantiation.

        Version 1.0.0.0
        """
        pass

    #private helper methods

    def _normalizeInput(self, InputString: str) -> str:
        """
        Normalizes the input unicode string using NFC form in order to be able
        to judge the actual lenght in characters of the string printed into the
        console.

        Signature:
            str -> str

        Version 1.0.0.0
        """
        return normalize('NFC', InputString)
    
    def _parseKwargs(self,
                        **kwargs) -> Union[None, dict[str, Union[int, bool]]]:
        """
        """
        Settings = None
        for Name, Value in kwargs.items():
            if Name == 'Foreground' or Name == 'Background':
                if not isinstance(Value, int):
                    Error = UT_TypeError(1, int, SkipFrames = 1)
                    Message = ' '.join([f'Keyword argument {Name} must be int',
                                        f'- {type(Value)} is passed'])
                    Error.setMessage(Message)
                    raise Error
                if Value > MAX_INDEX or Value < MIN_INDEX:
                    Ranges = ' '.join([f'>={MIN_INDEX} and <={MAX_INDEX}',
                                        f' - value of keyword argument {Name}'])
                    raise UT_ValueError(Value, Ranges, SkipFrames = 1)
                if Settings is None:
                    Settings = dict()
                Settings[Name] = Value
            elif Name in ALL_ATTRIBUTES:
                if Settings is None:
                    Settings = dict()
                Settings[Name] = bool(Value)
            else:
                Error = UT_TypeError(1, int, SkipFrames = 1)
                Message = f'Unrecognized name of keyword argument {Name}'
                Error.setMessage(Message)
                raise Error
        return Settings
    
    def _checkIfDecorated(self,
                    Settings: Optional[dict[str, Union[int, bool]]]) -> bool:
        """
        """
        if (not IS_POSIX) or (Settings is None):
            Result = False
        else:
            if ('Foreground' in Settings) or ('Background' in Settings):
                Result = True
            elif any(Settings.values()):
                Result = True
            else:
                Result = False
        return Result


    #public instance methods

    @abc.abstractmethod
    def clear(self) -> None:
        """
        Virtual method to erase the current graphical representation of a
        widget. Not implemenented - the non-abstract sub-classes must implement
        this method as non-virtual.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        pass
    
    @abc.abstractmethod
    def getStringValue(self) -> str:
        """
        Returns the current graphical representation of a widget as a string.
        Virtual, must be implemented by the sub-classes.

        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        pass

    def show(self) -> None:
        """
        Method to print the current graphical representation of a widget.

        Signature:
            None -> None
        
        Version 2.0.0.0
        """
        sys.stdout.write(self.getStringValue())
        sys.stdout.flush()

    def update(self) -> None:
        """
        Method to erase the current and to print out the new graphical
        representation of a widget reflecting its inner state.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        self.clear()
        self.show()

class HWidget_ABC(CLUI_ABC):
    """
    Abstract Base Class as the single line widget views classes. The method
    getStringValue() is abstract (virtual) - must be implemented by the
    sub-classes.

    Sub-classes CLUI_ABC.

    Attributes:
        Value: (read-only property) type A; internal state of a widget
        Width: (read-only property) int > 0; current width (in characters) of
            the visual representation

    Methods:
        clear():
            None -> None
        show():
            None -> None
        update():
            None -> None
        setValue(Value):
            type A -> None
        getStringValue():
            None -> str
    
    Version 1.0.0.1
    """

    #special methods

    def __init__(self, Value: Any, *, Width: Optional[int] = None,
                                        **kwargs) -> None:
        """
        Initializer. Creates and sets the instance attributes.

        Signature:
            type A/, *, int OR None, .../ -> None
        
        Args:
            Value: type A; any value to be assigned as the internal state
            Width: (keyword) int > 0; width of the widget's representation in
                characters; if not provided or None - the width is set to 1
        
        Raises:
            UT_TypeError: passed Width argument is not an integer or None
            UT_ValueError: passed Width argument is integer but not positive

        Version 1.0.0.1
        """
        if isinstance(Width, int):
            if hasattr(self, '_MinWidth'): #for the future mixin implementation
                if Width >= self._MinWidth:
                    self._Width = Width
                else:
                    ErrorMessage = '> {} - widget`s width in characters'.format(
                                                            self._MinWidth - 1)
                    raise UT_ValueError(Width, ErrorMessage, SkipFrames = 1)
            elif (Width > 0):
                self._Width = Width
            else:
                ErrorMessage = '> 0 - widget`s width in characters'
                raise UT_ValueError(Width, ErrorMessage, SkipFrames = 1)
        elif Width is None:
            self._Width = 1
        else:
            raise UT_TypeError(Width, int, SkipFrames = 1)
        self.setValue(Value)
    
    #public API

    #+ properties

    @property
    def Value(self) -> Any:
        """
        Read-only property to access the stored internal state of a widget.

        Signature:
            None -> type A
        
        Version 1.0.0.0
        """
        return self._Value
    
    @property
    def Width(self) -> int:
        """
        Read-only property to access the current width of a widget.

        Signature:
            None -> int > 0
        
        Version 1.0.0.0
        """
        return self._Width
    
    #+ instance methods

    def setValue(self, Value: Any) -> None:
        """
        Method to set the internal state (value) of a widget. It does not
        refresh the representation. Use method update() to refresh.

        Signature:
            type A -> None
        
        Args:
            Value: type A; any value to store
        
        Version 1.0.0.0
        """
        self._Value = Value
    
    def clear(self) -> None:
        """
        Method to erase the current graphical representation of a widget.

        Signature:
            None -> None
        
        Version 1.0.0.1
        """
        Filler = ' ' * self.Width
        sys.stdout.write(f'\r{Filler}\r')
        sys.stdout.flush()

class TextLabel(HWidget_ABC):
    """
    Text label widget's view class. The width of the representation is set
    during instantiation, and it cannot be changed later. If a value set to
    the widget's representation is longer (as a string) than the widget's width
    this string will be truncated. If the string is shorter - it will be padded
    left or right or from the both sides with spaces depending on the alignment,
    which can also be set only during instantiation.

    Sub-classes HWidget_ABC -|> CLUI_ABC.

    Attributes:
        Value: (read-only property) type A; internal state of a widget
        Width: (read-only property) int > 0; current width (in characters) of
            the visual representation
        Alignment: (read-only property) str; the used text alignment - one of
            the values 'l', 'c' or 'r', meaning left, center or right

    Methods:
        clear():
            None -> None
        show():
            None -> None
        update():
            None -> None
        setValue(Value):
            type A -> None
        getStringValue():
            None -> str
    
    Version 1.2.0.0
    """

    #special methods

    def __init__(self, Value: Any, *, Width: Optional[int] = None,
                                        Alignment: str = 'l', **kwargs) -> None:
        """
        Initializer. Creates and sets the instance attributes.

        Signature:
            type A/, *, int OR None, str, **kwargs/ -> None
        
        Args:
            Value: type A; any value to be assigned as the internal state
            Width: (keyword) int > 0; width of the widget's representation in
                characters; if not provided or None, the width is set to the
                length of the string representation of the value + 1 character
            Alignment: (keyword) str; alignment of the text - one of the posible
                values 'l', 'c' or 'r' case-insensitive
            **kwargs: (keyword) **dict(str -> int OR bool); text decorators,
                allowed Foreground, Background (0..255), BOLD, ITALIC, FAINT,
                UNDERLINE, DOUBLE, STRIKE, HIDE, INVERSE (bool)
        
        Raises:
            UT_TypeError: passed Width argument is not an integer or None, OR
                passed Alignment is not a string, OR unrecognized keyword
                argument for text decoration is passed, OR non-integer value
                is passed for the background or foreground colour
            UT_ValueError: passed Width argument is integer but not positive, OR
                passed Alignment is not of 'l', 'c' or 'r' case-insensitive
                values, OR integer value outside of 0..255 range is passed for
                the background or foreground colour

        Version 2.0.0.0
        """
        if isinstance(Alignment, str):
            if Alignment.lower() in ['c', 'l', 'r']:
                self._Alignment = Alignment.lower()
            else:
                ErrorMessage = "in values ['c', 'l', 'r'] case-insensitive"
                raise UT_ValueError(Alignment, ErrorMessage, SkipFrames = 1)
        else:
            raise UT_TypeError(Alignment, str, SkipFrames = 1)
        if isinstance(Width, int) and Width > 0:
            _Width = Width
        else:
            _Width = len(self._normalizeInput(str(Value))) + 1
        try:
            super().__init__(Value, Width = _Width)
        except UT_TypeError as err:
            NewError = UT_TypeError(1, int, SkipFrames = 1)
            NewError.setMessage(err.getMessage())
            raise NewError from None
        except UT_ValueError as err1:
            NewError = UT_ValueError(1, 'whatever', SkipFrames = 1)
            NewError.setMessage(err1.getMessage())
            raise NewError from None
        if len(kwargs):
            self._Settings = self._parseKwargs(**kwargs)
        else:
            self._Settings = None
    
    #public API

    #+ properties

    @property
    def Value(self) -> str:
        """
        Read-only property to access the stored internal state of a widget, i.e.
        the stored string value.

        Signature:
            None -> str
        
        Returns:
            str: the stored value as a string
        
        Version 1.0.0.0
        """
        return self._Value
    
    @property
    def Alignment(self) -> str:
        """
        Read-only property to access the used text alignment.

        Signature:
            None -> str
        
        Returns:
            str: any of the values 'c', 'l' or 'r'
        
        Version 1.0.0.0
        """
        return self._Alignment
    
    #++ instance methods

    def setValue(self, Value: Any, **kwargs) -> None:
        """
        Method to set the internal state (value) of a widget. The passed value
        is converted into a string. It does not refresh the representation. Use
        method update() to refresh.

        Signature:
            type A/, **kwargs/ -> None
        
        Args:
            Value: type A; any value to store as a string
            **kwargs: (keyword) **dict(str -> int OR bool); text decorators,
                allowed Foreground, Background (0..255), BOLD, ITALIC, FAINT,
                UNDERLINE, DOUBLE, STRIKE, HIDE, INVERSE (bool)
        
        Raises:
            UT_TypeError: Unrecognized keyword argument for text decoration is
                passed, OR non-integer value is passed for the background or
                foreground colour
            UT_ValueError: Integer value outside of 0..255 range is passed for
                the background or foreground colour
        
        Version 2.0.0.0
        """
        self._Value = self._normalizeInput(str(Value))
        if len(kwargs):
            self._Settings = self._parseKwargs(**kwargs)
        else:
            self._Settings = None
    
    def getStringValue(self) -> str:
        """
        Returnst the currently stored string with at least one space after it
        (for 'l' and 'c' alignments) or before it (for 'r' alignement). Too long
        strings are truncated. The strings shorted than the width of the widget
        - 1 character are padded with spaces either to the right ('l' alignment)
        or to the left ('r' alignment) or from the both sides ('c' alignment).

        Signature:
            None -> str
        
        Version 2.0.0.0
        """
        if len(self.Value) < self.Width:
            Result = self.Value
        else:
            Result = self.Value[:(self.Width - 1)]
        Length = len(Result)
        ExtraSpaces = self.Width - Length
        if ExtraSpaces:
            LeftPositions = ExtraSpaces if self.Alignment == 'r' else 0
            RightPositions = ExtraSpaces if self.Alignment == 'l' else 0
            if self.Alignment == 'c':
                LeftPositions = ExtraSpaces // 2
                RightPositions = ExtraSpaces - LeftPositions
            LeftSpaces = ' ' * LeftPositions
            RightSpaces = ' ' * RightPositions
            Result = f'{LeftSpaces}{Result}{RightSpaces}'
        if self._checkIfDecorated(self._Settings):
            Result = ColorizeFunc(Result, **self._Settings)
        return Result

class BarControl_ABC(HWidget_ABC):
    """
    Abstract Base Class for the widget views like slider and progress bar, i.e.
    with a positional representation of the internal state, which is limited
    to a float in the range 0.0 to 1.0 inclusively. Method getStringValue() is
    not yet implemented - must be done by the sub-classes.

    Sub-classes HWidget_ABC -|> CLUI_ABC.

    Attributes:
        Value: (read-only property) 0 <= float <= 1; internal state of a widget
        Width: (read-only property) int > 4; current width (in characters) of
            the visual representation

    Methods:
        clear():
            None -> None
        show():
            None -> None
        update():
            None -> None
        setValue(Value):
            0.0 <= float <= 1.0 -> None
        getStringValue():
            None -> str
    
    Version 1.0.0.1
    """

    #private class attributes

    _MinWidth: ClassVar[int] = 5

    #special methods

    def __init__(self, Value: float, *, Width: int = 5) -> None:
        """
        Initializer. Creates and sets the instance attributes.

        Signature:
            0.0 <= float <= 1.0 /, *, int > 4/ -> None
        
        Args:
            Value: 0.0 <= float <= 1.0; the internal state
            Width: (keyword) int > 4; width of the widget's representation in
                characters; if not provided, the width is set to 5
        
        Raises:
            UT_TypeError: passed Width argument is not an integer or None, OR
                passed Value is not a floating point number
            UT_ValueError: passed Width argument is integer but not positive, OR
                passed Value is not within [0.0, 1.0] range inclusively

        Version 1.0.0.1
        """
        try:
            super().__init__(Value, Width = Width)
        except UT_TypeError as err:
            NewError = UT_TypeError(1, int, SkipFrames = 1)
            NewError.setMessage(err.getMessage())
            raise NewError from None
        except UT_ValueError as err1:
            NewError = UT_ValueError(1, 'whatever', SkipFrames = 1)
            NewError.getMessage(err1.getMessage())
            raise NewError from None
    
    #public API

    #+ properties

    @property
    def Value(self) -> float:
        """
        Read-only property to access the stored internal state of a widget.

        Signature:
            None -> 0.0 <= float <= 1.0
        
        Returns:
            float: the stored value between 0.0 and 1.0 inclusively
        
        Version 1.0.0.0
        """
        return self._Value

    #+ instance methods

    def setValue(self, Value: float) -> None:
        """
        Method to set the internal state (value) of a widget. The passed value
        is converted into a string. It does not refresh the representation. Use
        method update() to refresh.

        Signature:
            type A -> None
        
        Args:
            Value: type A; any value to store as a string
        
        Version 1.0.0.1
        """
        if isinstance(Value, (int, float)):
            if Value < 0 or Value > 1:
                ErrorMessage = 'in the range [0.0, 1.0] inclusively'
                raise UT_ValueError(Value, ErrorMessage, SkipFrames = 1)
        else:
            raise UT_TypeError(Value, (int, float))
        self._Value = float(Value)

class Slider(BarControl_ABC):
    """
    Implementation of the fixed width slider widget's view, with the internal
    state limited to a float in the range 0.0 to 1.0 inclusively.

    Sub-classes BarControl_ABC -|> HWidget_ABC -|> CLUI_ABC.

    Attributes:
        Value: (read-only property) 0 <= float <= 1; internal state of a widget
        Width: (read-only property) int > 4; current width (in characters) of
            the visual representation

    Methods:
        clear():
            None -> None
        show():
            None -> None
        update():
            None -> None
        setValue(Value):
            0.0 <= float <= 1.0 -> None
        getStringValue():
            None -> str
    
    Version 1.1.0.1
    """

    #public instance methods

    def getStringValue(self) -> str:
        """
        Returns the representation of the current state of the widget.

        Signature:
            None -> str
        
        Version 2.0.0.0
        """
        BarWidth = self.Width - 2
        Position = 1 + int(self.Value * (BarWidth - 1))
        LeftSpacer = '-' * (Position - 1) if Position > 1 else ''
        RightSpacer = '-' * (BarWidth - Position) if Position < BarWidth else ''
        Value = f'<{LeftSpacer}I{RightSpacer}>'
        return Value

class ProgressBar(BarControl_ABC):
    """
    Implementation of the fixed width progress bar widget's view, with the
    internal state limited to a float in the range 0.0 to 1.0 inclusively.

    Sub-classes BarControl_ABC -|> HWidget_ABC -|> CLUI_ABC.

    Attributes:
        Value: (read-only property) 0 <= float <= 1; internal state of a widget
        Width: (read-only property) int > 4; current width (in characters) of
            the visual representation

    Methods:
        clear():
            None -> None
        show():
            None -> None
        update():
            None -> None
        setValue(Value):
            0.0 <= float <= 1.0 -> None
        getStringValue():
            None -> str
        setStyle(Style):
            type type A -> None
    
    Version 1.2.0.0
    """

    def __init__(self, Value: float, *, Width: int = 5,
                            Style: type = ProgressBarDecoratorSimple) -> None:
        """
        Initializer. Creates and sets the instance attributes.

        Signature:
            0.0 <= float <= 1.0 /, *, int > 4, type type A/ -> None
        
        Args:
            Value: 0.0 <= float <= 1.0; the internal state
            Width: (keyword) int > 4; width of the widget's representation in
                characters; if not provided, the width is set to 5
            Style: (keyword) type type A; decorators stored in nested
                struct-like classes as class attributes
        
        Raises:
            UT_TypeError: passed Width argument is not an integer or None, OR
                passed Value is not a floating point number
            UT_ValueError: passed Width argument is integer but not positive, OR
                passed Value is not within [0.0, 1.0] range inclusively

        Version 1.0.0.0
        """
        super().__init__(Value, Width = Width)
        self.setStyle(Style)

    #public instance methods

    def getStringValue(self) -> str:
        """
        Returns the representation of the current state of the widget.

        Signature:
            None -> str
        
        Version 2.0.0.0
        """
        BarWidth = self.Width - 2
        Position = int(self.Value * BarWidth)
        Filled = self._Full * Position
        Unfilled= self._Empty*(BarWidth-Position) if Position < BarWidth else ''
        Result = f'{self._Left}{Filled}{Unfilled}{self._Right}'
        return Result
    
    def setStyle(self, Style: type) -> None:
        """
        Changes the visual elements of the Bar widget, see widgets_decorators
        module.

        Signature:
            type type A -> None
        
        Args:
            Style: type type A; decorators stored in nested struct-like classes
                as class attributes
        
        Version 1.0.0.0
        """
        #todo - check validity of Style
        Full = Style.Bar.Full
        Empty = Style.Bar.Empty
        Left = Style.Edges.Left
        Right = Style.Edges.Right
        EdgeFG = Style.Edges.Foreground
        EdgeBG = Style.Edges.Background
        self._Full = ColorizeFunc(self._normalizeInput(Full.Symbol),
                Foreground = Full.Foreground, Background = Full.Background)
        self._Empty = ColorizeFunc(self._normalizeInput(Empty.Symbol),
                Foreground = Empty.Foreground, Background = Empty.Background)
        self._Left = ColorizeFunc(self._normalizeInput(Left),
                                    Foreground = EdgeFG, Background = EdgeBG)
        self._Right = ColorizeFunc(self._normalizeInput(Right),
                                    Foreground = EdgeFG, Background = EdgeBG)

class ScalableWidth:
    """
    Mixin class adding the ability to change the width of a widget at the run-
    time. Adds the following functionality.

    Attributes:
        MinWidth: (read-only property) int > 0; minimum allowed width of the
            widget
    
    Methods:
        setWidth(Width):
            int >= MinWidth -> None
    
    The mixed-in class must have the attributes _MinWidth and _Width as well
    as the methods clear() and show().

    Version 1.0.0.1
    """

    #deafult min width as class variable

    _MinWidth: ClassVar[int] = 5

    #public API

    #+ properties

    @property
    def MinWidth(self) -> None:
        """
        Read-only property to access the minimum allowed width of the widget.

        Signature:
            None -> int > 0
        
        Version 1.0.0.0
        """
        return self._MinWidth
    
    #+ instance methods

    def setWidth(self, Width: int) -> None:
        """
        Changes the current width of the widget's representation in characters.

        Signature:
            int >= MinWidth -> None
        
        Args:
            Width: int >= MinWidth; required width of the widget, but not less
                than the minimum allowed.

        Raises:
            UT_TypeError: argument is not an integer
            UT_ValueError: arguent is an integer but smaller than the minimum
                allowed width
        
        Version 1.0.0.1
        """
        if isinstance(Width, int):
            if Width < self.MinWidth:
                ErrorMessage = f'> {self.MinWidth} - minimum allowed width'
                raise UT_ValueError(Width, ErrorMessage, SkipFrames = 1)
            self.clear()
        else:
            raise UT_TypeError(Width, int, SkipFrames = 1)
        self._Width = Width

class SliderVW(Slider, ScalableWidth):
    """
    Implementation of the variable width slider widget's view, with the internal
    state limited to a float in the range 0.0 to 1.0 inclusively.

    Sub-classes (Slider -|> BarControl_ABC -|> HWidget_ABC -|> CLUI_ABC,
    ScalableWidth).

    Attributes:
        Value: (read-only property) 0 <= float <= 1; internal state of a widget
        MinWidth: (read-only property) int > 0; minimum allowed width of the
            widget, current value is 5 - implemented via private class attribute
        Width: (read-only property) int > MinWidth; current width
            (in characters) of the visual representation

    Methods:
        clear():
            None -> None
        show():
            None -> None
        update():
            None -> None
        setValue(Value):
            0.0 <= float <= 1.0 -> None
        setWidth(Width):
            int >= MinWidth -> None
        getStringValue():
            None -> str
    
    Version 1.0.0.0
    """

class ProgressBarVW(ProgressBar, ScalableWidth):
    """
    Implementation of the variable width progress bar widget's view, with the
    internal state limited to a float in the range 0.0 to 1.0 inclusively.

    Sub-classes (ProgressBar -|> BarControl_ABC -|> HWidget_ABC -|> CLUI_ABC,
    ScalableWidth).

    Attributes:
        Value: (read-only property) 0 <= float <= 1; internal state of a widget
        MinWidth: (read-only property) int > 0; minimum allowed width of the
            widget, current value is 5 - implemented via private class attribute
        Width: (read-only property) int > MinWidth; current width
            (in characters) of the visual representation

    Methods:
        clear():
            None -> None
        show():
            None -> None
        update():
            None -> None
        setValue(Value):
            0.0 <= float <= 1.0 -> None
        setWidth(Width):
            int >= MinWidth -> None
        getStringValue():
            None -> str
        setStyle(Style):
            type type A -> None
    
    Version 1.0.0.0
    """
    pass

class TextLabelVW(TextLabel, ScalableWidth):
    """
    Text label widget's view class with the variable width. The width of the
    representation is set during instantiation or value's assignment, but it be
    changed later to a larger one. The string will never be truncated, because
    the value's assignment automatically sets the minimum allowed width and the
    current width to len(str(Value)) + 1. The string will be padded left or
    right or from the both sides with spaces depending on the alignment,
    which can also be set only during instantiation.

    Sub-classes (TextLebel -|> HWidget_ABC -|> CLUI_ABC, ScalableWidth).

    Attributes:
        Value: (read-only property) type A; internal state of a widget
        MinWidth: (read-only property) int > 0; minimum allowed width of the
            widget, current value is 5 - implemented via private instance
            attribute
        Width: (read-only property) int >= MinWidth; current width (in
            characters) of the visual representation
        Alignment: (read-only property) str; the used text alignment - one of
            the values 'l', 'c' or 'r', meaning left, center or right

    Methods:
        clear():
            None -> None
        show():
            None -> None
        update():
            None -> None
        setValue(Value):
            type A -> None
        setWidth(Width):
            int >= MinWidth -> None
        getStringValue():
            None -> str
    
    Version 1.0.0.1
    """
    pass

    #special methods

    def __init__(self, Value: Any, *, Width: Optional[int] = None,
                            Alignment: str  = 'l', **kwargs) -> None:
        """
        Initializer. Creates and sets the instance attributes.

        Signature:
            type A/, *, int OR None, str, **kwargs/ -> None
        
        Args:
            Value: type A; any value to be assigned as the internal state
            Width: (keyword) int > 0; width of the widget's representation in
                characters; if not provided or None, the width is set to the
                length of the string representation of the value + 1 character
            Alignment: (keyword) str; alignment of the text - one of the posible
                values 'l', 'c' or 'r' case-insensitive
            **kwargs: (keyword) **dict(str -> int OR bool); text decorators,
                allowed Foreground, Background (0..255), BOLD, ITALIC, FAINT,
                UNDERLINE, DOUBLE, STRIKE, HIDE, INVERSE (bool)
        
        Raises:
            UT_TypeError: passed Width argument is not an integer or None, OR
                passed Alignment is not a string, OR unrecognized keyword
                argument for text decoration is passed, OR non-integer value
                is passed for the background or foreground colour
            UT_ValueError: passed Width argument is integer but not positive, OR
                passed Alignment is not of 'l', 'c' or 'r' case-insensitive
                values, OR integer value outside of 0..255 range is passed for
                the background or foreground colour

        Version 1.0.0.1
        """
        self._Value = None
        InputLen = len(self._normalizeInput(str(Value)))
        if Width is None:
            _Width = max(self.MinWidth, InputLen)
        elif isinstance(Width, int):
            if Width >= self.MinWidth:
                _Width = max(Width, InputLen)
            else:
                ErrorMessage = '> {} - widget`s width in characters'.format(
                                                            self.MinWidth - 1)
                raise UT_ValueError(Width, ErrorMessage, SkipFrames = 1)
        
        super().__init__(Value, Width = _Width, Alignment = Alignment, **kwargs)
    
    #public instance methods

    def setValue(self, Value: Any, **kwargs) -> None:
        """
        Method to set the internal state (value) of a widget. The passed value
        is converted into a string. It does not refresh the representation. Use
        method update() to refresh. The mimimum allowed and the current width
        of the widget is set to len(str(Value)) + 1.

        Signature:
            type A -> None
        
        Args:
            Value: type A; any value to store as a string
            **kwargs: (keyword) **dict(str -> int OR bool); text decorators,
                allowed Foreground, Background (0..255), BOLD, ITALIC, FAINT,
                UNDERLINE, DOUBLE, STRIKE, HIDE, INVERSE (bool)
        
        Raises:
            UT_TypeError: Unrecognized keyword argument for text decoration is
                passed, OR non-integer value is passed for the background or
                foreground colour
            UT_ValueError: Integer value outside of 0..255 range is passed for
                the background or foreground colour
        
        Version 1.0.0.1
        """
        if not (self._Value is None):
            self.clear()
        _Value = self._normalizeInput(str(Value))
        self._Value = _Value
        self._MinWidth = max(len(_Value) + 1, self.__class__._MinWidth)
        self._Width = max(len(_Value) + 1, self._MinWidth)
        if len(kwargs):
            self._Settings = self._parseKwargs(**kwargs)
        else:
            self._Settings = None

class HContainer(CLUI_ABC):
    """
    Widgets container class to stack multiple single line widgets into a single
    line string representation.

    Initially it is created empty but of the finite width (in characters). The
    widgets are supposed to be added to it after instantiation. The sum of the
    widths (fixed or minimum allowed for the variable width widgets) cannot
    exceed the current set width of the container, which can be addjusted during
    the runtime. The variable width widgets will be scaled equally to fill the
    entire width of the container, but the width of the fixed size widgets will
    not be affected.

    Sub-classes CLUI_ABC.

    Attributes:
        MinWidth: (read-only property) int > 0; minimum width required to fit
            all the stacked widgets, the actual width of the container cannot
            be set below this value
        Width: (read-only property) int >= MinWidth; current width (in
            characters) of the container although the stacked widgets can occupy
            less characters
    
    Methods:
        clear():
            None -> None
        show():
            None -> None
        update():
            None -> None
        addWidget(Widget):
            HWidget_ABC -> None
        setWidth(Width):
            int >= MinWidth -> None
        getStringValue():
            None -> str
    
    Version 1.1.0.1
    """

    #special methods

    def __init__(self, *, Width: int = 80,
                                        **kwargs) -> None:
        """
        Initializer. Creates and sets the instance attributes.

        Signature:
            /*, int, .../ -> None
        
        Args:
            Width: (keyword) int >= 0; width of the widget's representation in
                characters; the default value is 80
        
        Raises:
            UT_TypeError: passed Width argument is not an integer
            UT_ValueError: passed Width argument is integer but not >= 0

        Version 1.0.0.1
        """
        if isinstance(Width, int):
            if (Width >= 0):
                self._Width = Width
            else:
                ErrorMessage = '>= 0 - widget`s width in characters'
                raise UT_ValueError(Width, ErrorMessage, SkipFrames = 1)
        else:
            raise UT_TypeError(Width, int, SkipFrames = 1)
        self._Widgets = []

    #public API

    #+ properties

    @property
    def Width(self) -> int:
        """
        Read-only property to access the current width of a widget.

        Signature:
            None -> int >= 0
        
        Version 1.0.0.0
        """
        return self._Width
    
    @property
    def MinWidth(self) -> int:
        """
        Read-only property to retrive the minimum width in characters to fit
        all currently stacked widgets.

        Signature:
            None -> int >= 0
        
        Version 1.0.0.1
        """
        Result = 0
        for Item in self._Widgets:
            if hasattr(Item, 'MinWidth') and hasattr(Item, 'setWidth'):
                Result += Item.MinWidth
            else:
                Result += Item.Width
        return Result
    
    #+ instance methods

    def setWidth(self, Width: int) -> None:
        """
        Changes the current width of the container's representation in
        characters.

        Signature:
            int >= MinWidth -> None
        
        Args:
            Width: int >= MinWidth; required width of the container, but not
                less than the minimum required to fit all stacked elements.

        Raises:
            UT_TypeError: argument is not an integer
            UT_ValueError: arguent is an integer but smaller than the minimum
                required width
        
        Version 1.0.0.1
        """
        MinWidth = self.MinWidth
        if isinstance(Width, int):
            if Width < MinWidth:
                ErrorMessage = f'> {MinWidth} - minimum required width'
                raise UT_ValueError(Width, ErrorMessage, SkipFrames = 1)
            self.clear()
        else:
            raise UT_TypeError(Width, int, SkipFrames = 1)
        self._Width = Width
        #scale the variable width widgets
        FreeSpace = self.Width - MinWidth
        NumberScalable = 0
        for Item in self._Widgets:
            if hasattr(Item, 'MinWidth') and hasattr(Item, 'setWidth'):
                NumberScalable += 1
        if NumberScalable:
            MeanExtra = FreeSpace // NumberScalable
            LastExtra = FreeSpace - MeanExtra * NumberScalable
            NumberScaledWidgets = 0
            for Item in self._Widgets:
                if hasattr(Item, 'MinWidth') and hasattr(Item, 'setWidth'):
                    Item.setWidth(Item.MinWidth + MeanExtra)
                    if NumberScaledWidgets == NumberScalable:
                        Item.setWidth(Item.Width + LastExtra)
                        break
                    NumberScaledWidgets += 1
    
    def clear(self) -> None:
        """
        Method to erase the current graphical representations of all stacked
        widgets.

        Signature:
            None -> None
        
        Version 1.0.0.1
        """
        Blanks = ' ' * self.Width
        sys.stdout.write(f'\r{Blanks}\r')
        sys.stdout.flush()
    
    def getStringValue(self) -> str:
        """
        Returns the graphical representations of all stacked widgets (their
        inner states) in a single line string.

        Signature:
            None -> str
        
        Version 1.0.0.1
        """
        Result = ''.join([Item.getStringValue() for Item in self._Widgets])
        return Result
    
    def addWidget(self, Widget: HWidget_ABC) -> None:
        """
        Method to add another widget to the stack, but only if it fits the
        free space available in the container.

        Signature:
            HWidget_ABC -> None
        
        Args:
            Widget: HWidget_ABC; instance of any sub-class of, the new widget
                to add to the stack

        Raises:
            UT_TypeError: the passed argument is not an instance of a sub-class
                of HWidget_ABC
            UT_Exception: the width of the new widget is too large to fit the
                remaining space in the container
        
        Version 1.0.0.1
        """
        if not isinstance(Widget, HWidget_ABC):
            raise UT_TypeError(Widget, HWidget_ABC, SkipFrames = 1)
        if hasattr(Widget, 'MinWidth') and hasattr(Widget, 'setWidth'):
            RequiredWidth = Widget.MinWidth
        else:
            RequiredWidth = Widget.Width
        Remains = self.Width - self.MinWidth
        if RequiredWidth > Remains:
            ErrorMessage = ' '.join(['Cannot fit new widget -',
                                f'required {RequiredWidth} characters space,',
                                            f'available {Remains} characters'])
            raise UT_Exception(ErrorMessage, SkipFrames = 1)
        self._Widgets.append(Widget)
        self.setWidth(self.Width)

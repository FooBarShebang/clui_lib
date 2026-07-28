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
    Spinner: looping through a list of pre-defined symbols
    Button: widget with two states, which can be toggled or set implicitely
    OnOffButton: specialized sub-class of Button - shows ON and OFF, on Possix
        systems also colour decoration is added
    RadioButton: specialized sub-class of Button - shows ( ) and (*)
    CheckButton: specialized sub-class of Button - shows [ ] and [X]
    ArrowIndicator: specialized sub-class of Button - shows '->' and '  ' states
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

__version__= '1.3.0.0'
__date__ = '28-07-2026'
__status__ = 'Development'

#imports

#+standard libraries

import sys
import os
import abc

from unicodedata import normalize

from typing import Any, Optional, Union, ClassVar, final

#+other libraries

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER =  os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from introspection_lib.base_exceptions import UT_ValueError, UT_TypeError
from introspection_lib.base_exceptions import UT_Exception, UT_IndexError

from ..console.xterm_colours import ALL_ATTRIBUTES, MIN_INDEX, MAX_INDEX

from .widgets_decorators import ProgressBarDecoratorSimple
from .widgets_decorators import SliderWidgetDecoratorSimple
from .widgets_decorators import SpinnerSimple, ArrowIndicatorDecorator
from .widgets_decorators import OnOffColouredButtonDecorator
from .widgets_decorators import RadioButtonDecorator, CheckButtonDecorator

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
    
    Version 1.0.0.0
    """
    return str(Data)

ColorizeFunc = ColorizeDummy if not IS_POSIX else Colorize

def GetScreenWidth() -> int:
    """
    Returns the current width in symbols of the terminal window.

    Siganture:
        None -> int > 0
    
    Version 1.0.0.0
    """
    ScreenSize = os.get_terminal_size()
    return ScreenSize.columns

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

    @final
    def _normalizeInput(self, InputString: str) -> str:
        """
        Helper private method.

        Normalizes the input unicode string using NFC form in order to be able
        to judge the actual lenght in characters of the string printed into the
        console.

        Signature:
            str -> str

        Version 1.0.0.0
        """
        return normalize('NFC', InputString)
    
    @final
    def _parseKwargs(self,
                        **kwargs) -> Union[None, dict[str, Union[int, bool]]]:
        """
        Helper private method. Parses the (optional) keyword arguments defining
        the text label's decorations and packes them into a single dictionary
        object.

        Signature:
            /**dict(str -> type A)/ -> None OR dict(str -> int OR bool)

        Returns:
            None: there are no keyword arguments
            dict(str -> int OR bool): dictionary of decorators
        
        Raises:
            UT_TypeError: unrecognized decorator name OR non-integer value for
                background or foreground colour decorator
            UV_ValueError: value of background or foreground clour is outside of
                256 colour-palette
        
        Version 1.0.0.0
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
    
    @final
    def _checkIfDecorated(self,
                    Settings: Optional[dict[str, Union[int, bool]]]) -> bool:
        """
        Helper method. Checks is the text decorators must be applied,
        specifically

        * The OS is POSIX, AND
        * Either background or foreground colour is specified OR any of the
            font attributes (bold, italic, etc.) is set

        Signature:
            None OR dict(str -> int OR bool) -> bool

        Version 1.0.0.0
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

    @final
    def show(self) -> None:
        """
        Method to print the current graphical representation of a widget.

        Signature:
            None -> None
        
        Version 2.0.0.0
        """
        sys.stdout.write(self.getStringValue())
        sys.stdout.flush()

    @final
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
        Read-only property to access the current width of a widget. Note, that
        the actual displayed width may be less than this value if the terminal
        width causes truncation.

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
    
    @final
    def clear(self) -> None:
        """
        Method to erase the current graphical representation of a widget.

        Signature:
            None -> None
        
        Version 1.0.0.1
        """
        Filler = ' ' * min(self.Width, GetScreenWidth())
        sys.stdout.write(f'\r{Filler}\r')
        sys.stdout.flush()

class Spinner(HWidget_ABC):
    """
    Spinner - a simple progress indicator using looping through a set of pre-
    defined symbols.

    Sub-classes HWidget_ABC -|> CLUI_ABC.
    
    Attributes:
        Value: (read-only property) int >= 0; index of the current symbol
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
            int -> None
        getStringValue():
            None -> str
        next():
            None -> None
    
    Version 1.0.0.0
    """

    #special methods

    def __init__(self, *, Style: type = SpinnerSimple) -> None:
        """
        Initializer. Creates and sets the instance attributes.
        
        Signature:
            /type type A/ -> None
        
        Args:
            Style: (keyword) type type A; decorators stored in a struct-like
                class as the class attributes, see widgets_decorators module
        
        Version 1.0.0.0
        """
        #todo - check validity of Style
        self._Value = 0
        if hasattr(Style, 'Symbols'):
            self._Range = list(Style.Symbols)
        else:
            self._Range = list(SpinnerSimple.Symbols)
        self._Width = max(len(Item) for Item in self._Range)
        if (hasattr(Style, 'Foreground') and isinstance(Style.Foreground, int)
                                                    and Style.Foreground >= 0):
            self._Foreground = Style.Foreground
        else:
            self._Foreground = None
        if (hasattr(Style, 'Background') and isinstance(Style.Background, int)
                                                    and Style.Background >= 0):
            self._Background = Style.Background
        else:
            self._Background = None

    #public methods

    def setValue(self, Index: int) -> None:
        """
        Method to explicitely set an index of the symbol to be displayed. The
        passed argument must be non-negative integer, which modulo of division
        by the length of the list of available symbols is the index of the
        symbol to be selected.

        Signature:
            int >= 0 -> None
        
        Args:
            Index: int >= 0; desired symbol`s index
        
        Vesion 1.0.0.0
        """
        if isinstance(Index, int) and Index >= 0:
            self._Value = Index % len(self._Range)

    def next(self) -> None:
        """
        Selects the next symbol from the set.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        if self.Value < len(self._Range) - 1:
            self._Value += 1
        else:
            self._Value = 0

    def getStringValue(self) -> str:
        """
        Returns the current symbol from the set, with back- and foreground
        colours applied if possible and neccessary.
    
        Signature:
            None -> str
            
        Version 1.0.0.0
        """
        Symbol = self._Range[self.Value]
        if len(Symbol) < self.Width:
            Filler = ' ' * (self.Width - len(Symbol))
            Symbol = f'{Symbol}{Filler}'
        if (not self._Foreground is None) or (not self._Background is None):
            Symbol = ColorizeFunc(Symbol, Foreground = self._Foreground,
                                                Background = self._Background)
        return Symbol

class Button(HWidget_ABC):
    """
    Button - a simple 2-states indicator emulating behaviour of a button.

    Sub-classes HWidget_ABC -|> CLUI_ABC.
    
    Attributes:
        Value: (read-only property) bool; On (True) / Off (False) state of the
            widget
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
            bool -> None
        getStringValue():
            None -> str
        toggleState():
            None -> None
    
    Version 1.0.0.0
    """

    #special methods

    def __init__(self, Style: type) -> None:
        """
        Initializer. Creates and sets the instance attributes.
        
        Signature:
            type type A -> None
        
        Args:
            Args:
                Style: (keyword) type type A; decorators stored in a struct-like
                    class as the class attributes, see widgets_decorators module
        
        Raises:
            UT_TypeError: passed argument does not have all required attributes
                to define the wifget`s elements, see widgets_decorators module
        
        Version 1.0.0.0
        """
        #todo - check validity of Style
        Error = UT_TypeError(Style, int, SkipFrames = 1)
        Error.setMessage(f'type(Style) is not a widget definition class')
        self._Value = False
        if hasattr(Style, 'OnState') and hasattr(Style.OnState, 'Symbol'):
            self._OnSymbol = self._normalizeInput(Style.OnState.Symbol)
        else:
            raise Error
        if hasattr(Style, 'OffState') and hasattr(Style.OffState, 'Symbol'):
            self._OffSymbol = self._normalizeInput(Style.OffState.Symbol)
        else:
            raise Error
        if (hasattr(Style.OnState, 'Foreground')
                and isinstance(Style.OnState.Foreground, int)
                                            and Style.OnState.Foreground >= 0):
            self._OnFG = Style.OnState.Foreground
        else:
            self._OnFG = None
        if (hasattr(Style.OnState, 'Background')
                and isinstance(Style.OnState.Background, int)
                                            and Style.OnState.Background >= 0):
            self._OnBG = Style.OnState.Background
        else:
            self._OnBG = None
        if (hasattr(Style.OffState, 'Foreground')
                and isinstance(Style.OffState.Foreground, int)
                                            and Style.OffState.Foreground >= 0):
            self._OffFG = Style.OffState.Foreground
        else:
            self._OffFG = None
        if (hasattr(Style.OffState, 'Background')
                and isinstance(Style.OffState.Background, int)
                                            and Style.OffState.Background >= 0):
            self._OffBG = Style.OffState.Background
        else:
            self._OffBG = None
        if hasattr(Style, 'Edges'):
            if (hasattr(Style.Edges, 'Foreground')
                    and isinstance(Style.Edges.Foreground, int)
                                            and Style.Edges.Foreground >= 0):
                self._EdgesFG = Style.Edges.Foreground
            else:
                self._EdgesFG = None
            if (hasattr(Style.Edges, 'Background')
                    and isinstance(Style.Edges.Background, int)
                                            and Style.Edges.Background >= 0):
                self._EdgesBG = Style.Edges.Background
            else:
                self._EdgesBG = None
            if hasattr(Style.Edges, 'Left'):
                self._Left = self._normalizeInput(Style.Edges.Left)
            else:
                self._Left = None
            if hasattr(Style.Edges, 'Right'):
                self._Right = self._normalizeInput(Style.Edges.Right)
            else:
                self._Right = None
        else:
            self._Left = None
            self._Right = None
        self._SymbolWidth = max(len(self._OnSymbol), len(self._OffSymbol))
        self._Width = self._SymbolWidth
        if not self._Left is None:
            self._Width += len(self._Left)
        if not self._Right is None:
            self._Width += len(self._Right)

    #public methods

    def toggleState(self) -> None:
        """
        Toggles the current On / Off state of the widget. Does not update the
        representation on the screen.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        self._Value = not self._Value

    def setValue(self, Value: bool) -> None:
        """
        Method to explicitely set On (True) or Off (False) state of the widget.
        Does not update the screen representation.

        Signature:
            bool -> None
        
        Args:
            Value: bool; any passed type is converted into bool
        
        Vesion 1.0.0.0
        """
        self._Value = bool(Value)

    def getStringValue(self) -> str:
        """
        Returns the full string representation of the current state of the
        widget.
    
        Signature:
            None -> str
            
        Version 1.0.0.0
        """
        if self.Value:
            Symbol = self._OnSymbol
            Foreground = self._OnFG
            Background = self._OnBG
        else:
            Symbol = self._OffSymbol
            Foreground = self._OffFG
            Background = self._OffBG
        if len(Symbol) < self._SymbolWidth:
            Filler = ' ' * (self._SymbolWidth - len(Symbol))
            Symbol = f'{Symbol}{Filler}'
        if (not Foreground is None) or (not Background is None):
            Symbol = ColorizeFunc(Symbol, Foreground = Foreground,
                                                Background = Background)
        if not self._Left is None:
            if (not self._EdgesFG is None) or (not self._EdgesBG is None):
                Left = ColorizeFunc(self._Left, Foreground = self._EdgesFG,
                                                    Background = self._EdgesBG)
            else:
                Left = self._Left
            Symbol = f'{Left}{Symbol}'
        if not self._Right is None:
            if (not self._EdgesFG is None) or (not self._EdgesBG is None):
                Right = ColorizeFunc(self._Right, Foreground = self._EdgesFG,
                                                    Background = self._EdgesBG)
            else:
                Right = self._Right
            Symbol = f'{Symbol}{Right}'
        return Symbol

class OnOffButton(Button):
    """
    Button - a simple 2-states indicator emulating behaviour of an On / OFF
    button. On Posix systems - also using colours.

    Sub-classes Button -> HWidget_ABC -|> CLUI_ABC.
    
    Attributes:
        Value: (read-only property) bool; On (True) / Off (False) state of the
            widget
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
            bool -> None
        getStringValue():
            None -> str
        toggleState():
            None -> None
    
    Version 1.0.0.0
    """

    #special methods

    def __init__(self) -> None:
        """
        Initialization method.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        super().__init__(OnOffColouredButtonDecorator)

class RadioButton(Button):
    """
    Button - a simple 2-states indicator emulating behaviour of a radio-button,
    displayed as ( ) and (*) respectively.

    Sub-classes Button -> HWidget_ABC -|> CLUI_ABC.
    
    Attributes:
        Value: (read-only property) bool; On (True) / Off (False) state of the
            widget
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
            bool -> None
        getStringValue():
            None -> str
        toggleState():
            None -> None
    
    Version 1.0.0.0
    """

    #special methods

    def __init__(self) -> None:
        """
        Initialization method.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        super().__init__(RadioButtonDecorator)

class CheckButton(Button):
    """
    Button - a simple 2-states indicator emulating behaviour of a check-box,
    displayed as [ ] and [X] respectively.

    Sub-classes Button -> HWidget_ABC -|> CLUI_ABC.
    
    Attributes:
        Value: (read-only property) bool; On (True) / Off (False) state of the
            widget
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
            bool -> None
        getStringValue():
            None -> str
        toggleState():
            None -> None
    
    Version 1.0.0.0
    """

    #special methods

    def __init__(self) -> None:
        """
        Initialization method.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        super().__init__(CheckButtonDecorator)

class ArrowIndicator(Button):
    """
    Switchable `->` indicator, designed to be used with menu selection widgets.

    Sub-classes Button -> HWidget_ABC -|> CLUI_ABC.
    
    Attributes:
        Value: (read-only property) bool; On (True) / Off (False) state of the
            widget
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
            bool -> None
        getStringValue():
            None -> str
        toggleState():
            None -> None
    
    Version 1.0.0.0
    """

    #special methods

    def __init__(self) -> None:
        """
        Initialization method.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        super().__init__(ArrowIndicatorDecorator)

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
        Value: (read-only property) str; internal state of a widget
        Width: (read-only property) int > 0; current width (in characters) of
            the visual representation
        Alignment: (read-only property) str; the used text alignment - one of
            the values 'l', 'c' or 'r', meaning left, center or right
        TruncationSymmetry: (read-only property) bool OR None; text truncation
            method, None - simple tail truncation, False - tail truncation with
            '...' added, True - middle part removal with '...' insertion

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
    
    Version 1.3.0.0
    """

    #special methods

    def __init__(self, Value: Any, *, Width: Optional[int] = None,
                                        Alignment: str = 'l',
                                        SymTrunc: Optional[bool] = None,
                                        **kwargs) -> None:
        """
        Initializer. Creates and sets the instance attributes.

        Signature:
            type A/, *, int OR None, str, bool OR None, **kwargs/ -> None
        
        Args:
            Value: type A; any value to be assigned as the internal state
            Width: (keyword) int > 0; width of the widget's representation in
                characters; if not provided or None, the width is set to the
                length of the string representation of the value + 1 character
            Alignment: (keyword) str; alignment of the text - one of the posible
                values 'l', 'c' or 'r' case-insensitive
            SymTrunc: (keyword) bool OR None; text trunction type, None - simple
                tail truncation, False - tail truncation with '...' added,
                True - middle part removal with '...' insertion
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
        if isinstance(Width, int) and Width > 1:
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
        if not (SymTrunc is None):
            self._SymTrunc = bool(SymTrunc)
        else:
            self._SymTrunc = None
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
    
    @property
    def TruncationSymmetry(self) -> Union[None, bool]:
        """
        Read-only property to access the used text trunction method.

        Signature:
            None -> None OR bool
        
        Returns:
            None: simple trail trunctation method is used
            bool: trunctation with '...' insertion is used, True - middle part
                is removed, False - tail part is removed
        
        Version 1.0.0.0
        """
        return self._SymTrunc
    
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
        Returns the currently stored string with at least one space after it
        (for 'l' and 'c' alignments) or before it (for 'r' alignement). Too long
        strings are truncated. The text is also truncated if the widget doesn't
        fit the terminal`s width.
        
        The strings shorter than the width of the widget - 1 character are
        padded with spaces either to the right ('l' alignment) or to the left
        ('r' alignment) or from the both sides ('c' alignment). Note, that one
        space is always added to the right (for 'r' or 'c' alignment) or to the
        left ('l' alignment)!

        Signature:
            None -> str
        
        Version 3.0.0.0
        """
        MaxWidth = min(self.Width, GetScreenWidth())
        if len(self.Value) < MaxWidth:
            Result = self.Value
        else:
            if (self.TruncationSymmetry is None) or self.Width < 6:
                Result = self.Value[:(MaxWidth - 1)]
            else:
                if not self.TruncationSymmetry:
                    Result = f'{self.Value[:(MaxWidth - 4)]}...'
                else:
                    BaseString = self.Value
                    TextLength = len(BaseString)
                    Left = (MaxWidth - 4) // 2
                    Right = TextLength - Left
                    Result = f'{BaseString[:Left]}...{BaseString[Right:]}'
        Length = len(Result)
        ExtraSpaces = MaxWidth - Length
        LeftPositions = ExtraSpaces if self.Alignment == 'r' else 0
        RightPositions = ExtraSpaces if self.Alignment == 'l' else 0
        if self.Alignment == 'c':
            LeftPositions = ExtraSpaces // 2
            RightPositions = ExtraSpaces - LeftPositions
        LeftSpaces = ' ' * LeftPositions
        RightSpaces = ' ' * RightPositions
        if self._checkIfDecorated(self._Settings):
            Result = ColorizeFunc(Result, **self._Settings)
        Result = f'{LeftSpaces}{Result}{RightSpaces}'
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
            0.0 <= float <= 1.0 /, *, int > 2/ -> None
        
        Args:
            Value: 0.0 <= float <= 1.0; the internal state
            Width: (keyword) int > 2; width of the widget's representation in
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
        setStyle(Style):
            type type A -> None
    
    Version 1.3.0.0
    """

    #special methods

    def __init__(self, Value: float, *, Width: int = 5,
                            Style: type = SliderWidgetDecoratorSimple) -> None:
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
        
        Version 3.0.0.0
        """
        MaxWidth = min(self.Width, GetScreenWidth())
        BarWidth = MaxWidth - 3
        Position = int(round(self.Value * BarWidth))
        LS = self._Line
        LeftSpacer = LS * Position if Position else ''
        RightSpacer = LS * (BarWidth - Position) if Position < BarWidth else ''
        Value=f'{self._Left}{LeftSpacer}{self._Gauge}{RightSpacer}{self._Right}'
        return Value

    def setStyle(self, Style: type) -> None:
        """
        Changes the visual elements of the Slider widget, see widgets_decorators
        module.

        Signature:
            type type A -> None
        
        Args:
            Style: type type A; decorators stored in nested struct-like classes
                as class attributes
        
        Version 1.0.0.0
        """
        #todo - check validity of Style
        Line = Style.Slider.Line
        Gauge = Style.Slider.Gauge
        Left = Style.Edges.Left
        Right = Style.Edges.Right
        EdgeFG = Style.Edges.Foreground
        EdgeBG = Style.Edges.Background
        self._Line = ColorizeFunc(self._normalizeInput(Line.Symbol),
                Foreground = Line.Foreground, Background = Line.Background)
        self._Gauge = ColorizeFunc(self._normalizeInput(Gauge.Symbol),
                Foreground = Gauge.Foreground, Background = Gauge.Background)
        self._Left = ColorizeFunc(self._normalizeInput(Left),
                                    Foreground = EdgeFG, Background = EdgeBG)
        self._Right = ColorizeFunc(self._normalizeInput(Right),
                                    Foreground = EdgeFG, Background = EdgeBG)

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
    
    Version 1.3.0.0
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
        
        Version 3.0.0.0
        """
        MaxWidth = min(self.Width, GetScreenWidth())
        BarWidth = MaxWidth - 2
        Position = int(round(self.Value * BarWidth))
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
        Automatically clears the widget`s representation, but does not displays
        the widget with the updated width - use show() or update() afterwards!

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
        self.clear()
        if isinstance(Width, int):
            if Width < self.MinWidth:
                ErrorMessage = f'> {self.MinWidth} - minimum allowed width'
                raise UT_ValueError(Width, ErrorMessage, SkipFrames = 1)
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
        setStyle(Style):
            type type A -> None
    
    Version 1.1.0.0
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
    
    Version 1.1.0.0
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
        Value: (read-only property) str; internal state of a widget - full text
            of the stored string
        MinWidth: (read-only property) int > 0; minimum allowed width of the
            widget, current value is 5 - implemented via private instance
            attribute
        Width: (read-only property) int >= MinWidth; current width (in
            characters) of the visual representation
        Alignment: (read-only property) str; the used text alignment - one of
            the values 'l', 'c' or 'r', meaning left, center or right
        SymTrunc: (keyword) bool OR None; text trunction type, None - simple
                tail truncation, False - tail truncation with '...' added,
                True - middle part removal with '...' insertion

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
        optimizeWidth():
            None -> None
    
    Version 1.1.0.0
    """

    #deafult min width as class variable

    _MinWidth: ClassVar[int] = 1

    #special methods

    def __init__(self, Value: Any, *, Width: Optional[int] = None,
                            Alignment: str  = 'l',
                            SymTrunc: Optional[bool] = None,
                            **kwargs) -> None:
        """
        Initializer. Creates and sets the instance attributes.

        Signature:
            type A/, *, int OR None, str, bool OR None, **kwargs/ -> None
        
        Args:
            Value: type A; any value to be assigned as the internal state
            Width: (keyword) int > 0; width of the widget's representation in
                characters; if not provided or None, the width is set to the
                length of the string representation of the value + 1 character
            Alignment: (keyword) str; alignment of the text - one of the posible
                values 'l', 'c' or 'r' case-insensitive
            SymTrunc: (keyword) bool OR None; text trunction type, None - simple
                tail truncation, False - tail truncation with '...' added,
                True - middle part removal with '...' insertion
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
        self._Value = None
        ScreenWidth = GetScreenWidth()
        InputLen = len(self._normalizeInput(str(Value)))
        if Width is None:
            _Width = min(max(self.MinWidth, InputLen + 1), ScreenWidth)
        elif isinstance(Width, int):
            if Width >= self.MinWidth:
                _Width = min(Width, ScreenWidth)
            else:
                ErrorMessage = '> {} - widget`s width in characters'.format(
                                                            self.MinWidth - 1)
                raise UT_ValueError(Width, ErrorMessage, SkipFrames = 1)
        super().__init__(Value, Width = _Width, Alignment = Alignment,
                                                SymTrunc = SymTrunc, **kwargs)
    
    #public instance methods

    def setValue(self, Value: Any, **kwargs) -> None:
        """
        Method to set the internal state (value) of a widget. The passed value
        is converted into a string. It clears but does not refresh the widget`s
        representation. Use method update() or show() to refresh. The mimimum
        allowed and the current width of the widget is set to
        len(str(Value)) + 1.

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
        
        Version 2.0.0.0
        """
        ScreenWidth = GetScreenWidth()
        if not (self._Value is None):
            self.clear()
        _Value = self._normalizeInput(str(Value))
        self._Value = _Value
        self._Width = min(self.Width, ScreenWidth)
        if len(kwargs):
            self._Settings = self._parseKwargs(**kwargs)
        else:
            self._Settings = None
        
    def optimizeWidth(self) -> None:
        """
        Adjusts the width of the widget to fit the text length and the terminal
        width. It clears but does not refresh the widget`s representation. Use
        method update() or show() to refresh.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        NewWidth = min(len(self.Value) + 1, GetScreenWidth())
        if NewWidth != self.Width:
            self.clear()
            self._Width = NewWidth

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

    Note, that unlike individual widgets, the width of the containter cannot
    exceed the current width of the terminal window - adjusted automatically.

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
    
    Version 1.3.0.0
    """

    #special methods

    def __init__(self, *, Width: int = 80,
                                        **kwargs) -> None:
        """
        Initializer. Creates and sets the instance attributes.

        Signature:
            /*, int, .../ -> None
        
        Args:
            Width: (keyword) int > 0; width of the widget's representation in
                characters; the default value is 80, but can be reduced to fit
                the terminal`s width
        
        Raises:
            UT_TypeError: passed Width argument is not an integer
            UT_ValueError: passed Width argument is integer but not > 0

        Version 2.0.0.0
        """
        if isinstance(Width, int):
            if (Width > 0):
                self._Width = min(Width, GetScreenWidth())
            else:
                ErrorMessage = '> 0 - widget`s width in characters'
                raise UT_ValueError(Width, ErrorMessage, SkipFrames = 1)
        else:
            raise UT_TypeError(Width, int, SkipFrames = 1)
        self._Widgets = []

    def __getitem__(self, Index: int) -> HWidget_ABC:
        """
        Special method to get access to a single widgets amongst added to this
        containter.

        Signature:
            int -> HWidget_ABC
        
        Args:
            Index: int, index of the stored widget to get access to
        
        Raises:
            UT_TypeError: passed argument is not a integer
            UT_IndexError: passed argument is an integer but outside of the
                range with respect to the number of the stored widgets
        
        Version 1.0.0.0
        """
        Length = len(self._Widgets)
        if not isinstance(Index, int):
            raise UT_TypeError(Index, int, SkipFrames = 1)
        if (not Length) or (Index > Length - 1) or (Index < - Length):
            raise UT_IndexError(self.__class__.__name__, Index)
        return self._Widgets[Index]

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
        characters. The current representation is cleared, but not re-drawn. Use
        method show() or update() afterwards!

        Signature:
            int >= MinWidth -> None
        
        Args:
            Width: int >= MinWidth; required width of the container, but not
                less than the minimum required to fit all stacked elements.

        Raises:
            UT_TypeError: argument is not an integer
        
        Version 2.0.0.0
        """
        self.clear()
        ScreenWidth = GetScreenWidth()
        MinWidth = self.MinWidth
        if not isinstance(Width, int):
            raise UT_TypeError(Width, int, SkipFrames = 1)
        if Width >= MinWidth:
            self._Width = max(min(Width, ScreenWidth), MinWidth)
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
        Blanks = ' ' * min(self.Width, GetScreenWidth())
        sys.stdout.write(f'\r{Blanks}\r')
        sys.stdout.flush()
    
    def getStringValue(self) -> str:
        """
        Returns the graphical representations of all stacked widgets (their
        inner states) in a single line string.

        Signature:
            None -> str
        
        Version 2.0.0.0
        """
        ScreenWidth = GetScreenWidth()
        if self.Width > ScreenWidth:
            Result = 'Error'
        else:
            Result = ''.join([Item.getStringValue() for Item in self._Widgets])
        return Result
    
    def addWidget(self, Widget: HWidget_ABC) -> None:
        """
        Method to add another widget to the stack, but only if it fits the
        free space available in the container. The representation of the widget
        is neither cleared nor updated.

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
        
        Version 1.1.0.0
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

#usr/bin/python3
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

__version__= '1.0.1.0'
__date__ = '09-12-2020'
__status__ = 'Testing'

#imports

#+standard libraries

import sys
import os
import abc

from typing import Any, Optional

#+other libraries

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from introspection_lib.base_exceptions import UT_ValueError, UT_TypeError
from introspection_lib.base_exceptions import UT_Exception_Check, UT_Exception

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
        """
        pass

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
    
    Version 1.0.0.0
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

        Version 1.0.0.0
        """
        if isinstance(Width, int):
            if hasattr(self, '_MinWidth'): #for the future mixin implementation
                if Width >= self._MinWidth:
                    self._Width = Width
                else:
                    strError = '> {} - widget`s width in characters'.format(
                                                            self._MinWidth - 1)
                    raise UT_ValueError(Width, strError, SkipFrames = 1)
            elif (Width > 0):
                self._Width = Width
            else:
                strError = '> 0 - widget`s width in characters'
                raise UT_ValueError(Width, strError, SkipFrames = 1)
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
        
        Version 1.0.0.0
        """
        strBlank = ' ' * self.Width
        sys.stdout.write('\r{0}\r'.format(strBlank))
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
    
    Version 1.1.0.0
    """

    #special methods

    def __init__(self, Value: Any, *, Width: Optional[int] = None,
                                        Alignment: str = 'l') -> None:
        """
        Initializer. Creates and sets the instance attributes.

        Signature:
            type A/, *, int OR None, str/ -> None
        
        Args:
            Value: type A; any value to be assigned as the internal state
            Width: (keyword) int > 0; width of the widget's representation in
                characters; if not provided or None, the width is set to the
                length of the string representation of the value + 1 character
            Alignment: (keyword) str; alignment of the text - one of the posible
                values 'l', 'c' or 'r' case-insensitive
        
        Raises:
            UT_TypeError: passed Width argument is not an integer or None, OR
                passed Alignment is not a string
            UT_ValueError: passed Width argument is integer but not positive, OR
                passed Alignment is not of 'l', 'c' or 'r' case-insensitive
                values

        Version 1.0.0.0
        """
        if isinstance(Alignment, str):
            if Alignment.lower() in ['c', 'l', 'r']:
                self._Alignment = Alignment.lower()
            else:
                strError = "in values ['c', 'l', 'r'] case-insensitive"
                raise UT_ValueError(Alignment, strError, SkipFrames = 1)
        else:
            raise UT_TypeError(Alignment, str, SkipFrames = 1)
        if isinstance(Width, int) and Width > 0:
            iWidth = Width
        else:
            iWidth = len(str(Value)) + 1
        try:
            super().__init__(Value, Width = iWidth)
        except UT_TypeError as err:
            NewError = UT_TypeError(1, int, SkipFrames = 1)
            NewError.args = (err.args[0], )
            raise NewError
        except UT_ValueError as err:
            NewError = UT_ValueError(1, 'whatever', SkipFrames = 1)
            NewError.args = (err.args[0], )
            raise NewError
    
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

    def setValue(self, Value: Any) -> None:
        """
        Method to set the internal state (value) of a widget. The passed value
        is converted into a string. It does not refresh the representation. Use
        method update() to refresh.

        Signature:
            type A -> None
        
        Args:
            Value: type A; any value to store as a string
        
        Version 1.0.0.0
        """
        self._Value = str(Value)
    
    def getStringValue(self) -> str:
        """
        Returnst the currently stored string with at least one space after it
        (for 'l' and 'c' alignments) or before it (for 'r' alignement). Too long
        strings are truncated. The strings shorted than the width of the widget
        - 1 character are padded with spaces either to the right ('l' alignment)
        or to the left ('r' alignment) or from the both sides ('c' alignment).

        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        if len(self.Value) < self.Width:
            strValue = self.Value
        else:
            strValue = self.Value[:(self.Width - 1)]
        iLen = len(strValue)
        iRemains = self.Width - iLen
        if self.Alignment == 'l':
            strOutValue = strValue + ' ' * iRemains
        elif self.Alignment == 'r':
            strOutValue = ' ' * iRemains + strValue
        else:
            iLeft = iRemains // 2
            iRight = iRemains - iLeft
            strOutValue = ' ' * iLeft + strValue + ' ' * iRight
        return strOutValue

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
    
    Version 1.0.0.0
    """

    #private class attributes

    _MinWidth: int = 5

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

        Version 1.0.0.0
        """
        try:
            super().__init__(Value, Width = Width)
        except UT_TypeError as err:
            NewError = UT_TypeError(1, int, SkipFrames = 1)
            NewError.args = (err.args[0], )
            raise NewError
        except UT_ValueError as err:
            NewError = UT_ValueError(1, 'whatever', SkipFrames = 1)
            NewError.args = (err.args[0], )
            raise NewError
    
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
        
        Version 1.0.0.0
        """
        if isinstance(Value, (int, float)):
            if Value < 0 or Value > 1:
                strError = 'in the range [0.0, 1.0] inclusively'
                raise UT_ValueError(Value, strError, SkipFrames = 1)
        else:
            raise UT_TypeError(Value, int)
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
    
    Version 1.1.0.0
    """

    #public instance methods

    def getStringValue(self) -> str:
        """
        Returns the representation of the current state of the widget.

        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        strValue = '<'
        BarWidth = self.Width - 2
        iPosition = 1 + int(self.Value * (BarWidth - 1))
        if iPosition > 1:
            strValue += '-' * (iPosition - 1)
        strValue += 'I'
        if iPosition < BarWidth:
            strValue += '-' * (BarWidth - iPosition)
        strValue += '>'
        return strValue

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
    
    Version 1.1.0.0
    """

    #public instance methods

    def getStringValue(self) -> str:
        """
        Returns the representation of the current state of the widget.

        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        strValue = '['
        BarWidth = self.Width - 2
        iPosition = int(self.Value * BarWidth)
        strValue += '#' * iPosition
        if iPosition < BarWidth:
            strValue += ' ' * (BarWidth - iPosition)
        strValue += ']'
        return strValue

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

    Version 1.0.0.0
    """

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
        
        Version 1.0.0.0
        """
        if isinstance(Width, int):
            if Width < self.MinWidth:
                strError = '> {} - minimum allowed width'.format(self.MinWidth)
                raise UT_ValueError(Width, strError, SkipFrames = 1)
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
    
    Version 1.0.0.0
    """
    pass

    #special methods

    def __init__(self, Value: Any, *, Width: Optional[int] = None,
                                        Alignment: str  = 'l') -> None:
        """
        Initializer. Creates and sets the instance attributes.

        Signature:
            type A/, *, int OR None, str/ -> None
        
        Args:
            Value: type A; any value to be assigned as the internal state
            Width: (keyword) int > 0; width of the widget's representation in
                characters; if not provided or None, the width is set to the
                length of the string representation of the value + 1 character
            Alignment: (keyword) str; alignment of the text - one of the posible
                values 'l', 'c' or 'r' case-insensitive
        
        Raises:
            UT_TypeError: passed Width argument is not an integer or None, OR
                passed Alignment is not a string
            UT_ValueError: passed Width argument is integer but not positive, OR
                passed Alignment is not of 'l', 'c' or 'r' case-insensitive
                values

        Version 1.0.0.0
        """
        self._Value = None
        self.setValue(Value)
        if isinstance(Width, int):
            if Width >= self.MinWidth:
                self._Width = Width
            else:
                strError = '> {} - widget`s width in characters'.format(
                                                            self.MinWidth - 1)
                raise UT_ValueError(Width, strError, SkipFrames = 1)
        elif not (Width is None):
            raise UT_TypeError(Width, int, SkipFrames = 1)
        if isinstance(Alignment, str):
            if Alignment.lower() in ['c', 'l', 'r']:
                self._Alignment = Alignment.lower()
            else:
                strError = "in values ['c', 'l', 'r'] case-insensitive"
                raise UT_ValueError(Alignment, strError, SkipFrames = 1)
        else:
            raise UT_TypeError(Alignment, str, SkipFrames = 1)
    
    #public instance methods

    def setValue(self, Value: Any) -> None:
        """
        Method to set the internal state (value) of a widget. The passed value
        is converted into a string. It does not refresh the representation. Use
        method update() to refresh. The mimimum allowed and the current width
        of the widget is set to len(str(Value)) + 1.

        Signature:
            type A -> None
        
        Args:
            Value: type A; any value to store as a string
        
        Version 1.0.0.0
        """
        if not (self._Value is None):
            self.clear()
        strValue = str(Value)
        self._Value = strValue
        self._MinWidth = len(strValue) + 1
        self._Width = len(strValue) + 1

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
    
    Version 1.1.0.0
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

        Version 1.0.0.0
        """
        if isinstance(Width, int):
            if (Width >= 0):
                self._Width = Width
            else:
                strError = '>= 0 - widget`s width in characters'
                raise UT_ValueError(Width, strError, SkipFrames = 1)
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
        
        Version 1.0.0.0
        """
        iResult = 0
        for Item in self._Widgets:
            if hasattr(Item, 'MinWidth') and hasattr(Item, 'setWidth'):
                iResult += Item.MinWidth
            else:
                iResult += Item.Width
        return iResult
    
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
        
        Version 1.0.0.0
        """
        iMinWidth = self.MinWidth
        if isinstance(Width, int):
            if Width < iMinWidth:
                strError = '> {} - minimum required width'.format(iMinWidth)
                raise UT_ValueError(Width, strError, SkipFrames = 1)
            self.clear()
        else:
            raise UT_TypeError(Width, int, SkipFrames = 1)
        self._Width = Width
        #scale the variable width widgets
        iFreeSpace = self.Width - iMinWidth
        iNScalable = 0
        for Item in self._Widgets:
            if hasattr(Item, 'MinWidth') and hasattr(Item, 'setWidth'):
                iNScalable += 1
        if iNScalable:
            iMeanExtra = iFreeSpace // iNScalable
            iLastExtra = iFreeSpace - iMeanExtra * iNScalable
            iCurrentlyAddingWidgetNumber = 1
            for Item in self._Widgets:
                if hasattr(Item, 'MinWidth') and hasattr(Item, 'setWidth'):
                    Item.setWidth(Item.MinWidth + iMeanExtra)
                    if iCurrentlyAddingWidgetNumber == iNScalable:
                        Item.setWidth(Item.Width + iLastExtra)
                        break
                    iCurrentlyAddingWidgetNumber += 1
    
    def clear(self) -> None:
        """
        Method to erase the current graphical representations of all stacked
        widgets.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        strBlank = ' ' * self.Width
        sys.stdout.write('\r{0}\r'.format(strBlank))
        sys.stdout.flush()
    
    def getStringValue(self) -> str:
        """
        Returns the graphical representations of all stacked widgets (their
        inner states) in a single line string.

        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        strResult = ''.join([Item.getStringValue() for Item in self._Widgets])
        return strResult
    
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
        
        Version 1.0.0.0
        """
        if not isinstance(Widget, HWidget_ABC):
            raise UT_TypeError(Widget, HWidget_ABC, SkipFrames = 1)
        if hasattr(Widget, 'MinWidth') and hasattr(Widget, 'setWidth'):
            iRequired = Widget.MinWidth
        else:
            iRequired = Widget.Width
        iRemains = self.Width - self.MinWidth
        if iRequired > iRemains:
            strError = ' '.join(['Cannot fit new widget -',
                            'required {} characters space,'.format(iRequired),
                            'available {} characters'.format(iRemains)])
            raise UT_Exception(strError, SkipFrames = 1)
        self._Widgets.append(Widget)
        self.setWidth(self.Width)

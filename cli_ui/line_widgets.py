#usr/bin/python3
"""
Module clui_lib.line_widgets

Implements a number of configurable, multiple components, single line widgets.

Classes:
    ProgressBarIndicator
"""

__version__= '1.0.0.1'
__date__ = '21-04-2023'
__status__ = 'Development'

#imports

#+standard libraries

import sys
import os

#+other libraries

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from .base_view_classes import HContainer, ProgressBarVW, TextLabel

from introspection_lib.base_exceptions import UT_ValueError, UT_TypeError

#classes

class ProgressBarIndicator:
    """
    Command line progress bar indicator with optional {done}/{total} counter
    and percents output. This implementation is re-usable, i.e. the same
    instance of this class can be used multiple times to show the progress of
    the different tasks. A new visual representation is created each time the
    method start() is called, and it is finilized by calling method stop().

    Attributes:
        Range: (read-only property) int > 0 ; the maximum value of the internal
            counter, representing the 100%
        Value: (read-only property) int >= 0; the current value of the internal
            counter
        Width: (read-only property) int > 0; the current width of the widget
        IsActive: (read-only property) bool; if the widget is running, i.e.
            creating the visual output
    
    Methods:
        start():
            None -> None
        stop():
            None -> None
        reset():
            None -> None
        inc():
            None -> None
        dec():
            None -> None
        setRange(Value):
            int > 0 -> None
        setValue(Value):
            int >= 0 -> None
        setWidth(Width):
            int > 0 -> None
        getStringValue():
            None -> str
    
    Version 1.0.0.1
    """

    #special methods

    def __init__(self, Range: int, *, Value: int = 0, ShowCounter: bool = True,
                            ShowPercents: bool = True, Width: int = 80) -> None:
        """
        Initialization. Sets the intial values of the counter, max range and
        the width of the widget. The visual representation will not be printed
        out until the method start() is called.

        Signature:
            int > 0 /,*, int >= 0, bool, bool, int > 0/ -> None
        
        Args:
            Range: int > 0; the maximum count, the upper bound of the range of
                the non-negative integers acceptable as the counter's value,
                i.e. the counter's value representing 100% completion
            Value: (keyword) int >= 0; the initial state of the counter, cannot
                exceed the Range value, defaults to 0
            ShowCounter: (keyword) bool; flag if the current value / maximum
                value counter should be shown, defaults to True
            ShowPerscents: (keyword) bool; flag if the percentage of the process
                completeness should be shown, defaults to True
            Width: (keyword) int; the width of the widget in characters, but it
                must be enough to fit the progress bar and the 
                defaults to 80
        
        Version 1.0.0.1
        """
        if isinstance(Range, int):
            if Range <= 0:
                ErrorMessage = '> 0 - maximum value, i.e. range'
                raise UT_ValueError(Range, ErrorMessage, SkipFrames = 1)
            self._Range = Range
        else:
            raise UT_TypeError(Range, int, SkipFrames = 1)
        if isinstance(Value, int):
            if (Value < 0) or (Value > self.Range):
                ErrorMessage = f'0 <= value <= {self.Range} - current value'
                raise UT_ValueError(Value, ErrorMessage, SkipFrames = 1)
            self._Value = Value
        else:
            raise UT_TypeError(Value, int, SkipFrames = 1)
        MinWidth = 5 #minimum for the progress bar
        if ShowCounter:
            MinWidth += 2 * (len(str(Range)) + 1) #minimum for counter
        if ShowPercents:
            MinWidth += 5 #minimum for % indicator
        if isinstance(Width, int):
            if (Width >= MinWidth):
                self._Width = Width
            else:
                ErrorMessage = f'>= {MinWidth} - widget`s width in characters'
                raise UT_ValueError(Width, ErrorMessage, SkipFrames = 1)
        else:
            raise UT_TypeError(Width, int, SkipFrames = 1)
        self._PBar = ProgressBarVW(0)
        self._Indicator = HContainer(Width = self.Width)
        self._Indicator.addWidget(self._PBar)
        if ShowCounter:
            DisplayValue = f'{self.Value}/{self.Range}'
            CounterWidth = 2 * (len(str(self.Range)) + 1)
            self._Counter = TextLabel(DisplayValue, Width = CounterWidth,
                                                                Alignment = 'r')
            self._Indicator.addWidget(self._Counter)
        else:
            self._Counter = None
        if ShowPercents:
            DisplayValue = '{}%'.format((100 * self.Value) // self.Range)
            self._Percents = TextLabel(DisplayValue, Width=5, Alignment= 'r')
            self._Indicator.addWidget(self._Percents)
        else:
            self._Percents = None
        self._IsActive = False


    #private helper methods

    def _show(self) -> None:
        """
        Helper method to update the internal states of the included widgets and
        their string on-screen representation, but only if this widgets is
        active (running indicator).

        Signature:
            None -> None
        
        Version 2.0.0.0
        """
        self.getStringValue() #updates the states the included widgets as a
        #+ side effect
        if self.IsActive:
            self._Indicator.update()
    
    #public API

    #+ properties

    @property
    def Width(self) -> int:
        """
        Read-only property to access the current width of the widget.

        Signature:
            None -> int > 0
        
        Version 1.0.0.0
        """
        return self._Width
    
    @property
    def IsActive(self) -> bool:
        """
        Read-only property to access the current activity state of the widget.

        Signature:
            None -> int > 0
        
        Version 1.0.0.0
        """
        return self._IsActive
    
    @property
    def Value(self) -> int:
        """
        Read-only property to access the current internal counter's value of the
        widget.

        Signature:
            None -> int >= 0
        
        Version 1.0.0.0
        """
        return self._Value
    
    @property
    def Range(self) -> int:
        """
        Read-only property to access the maximum allowed internal counter's
        value of the widget.

        Signature:
            None -> int > 0
        
        Version 1.0.0.0
        """
        return self._Range
    
    #+ instance methods

    def start(self) -> None:
        """
        Creates the visual representation of the widget and activates it. Also
        forces the console to the new line.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        sys.stdout.write('\n')
        sys.stdout.flush()
        self._IsActive = True
        self._show()
    
    def stop(self) -> None:
        """
        Disactivates the visual representation of the widget, and forces the
        console to the new line.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        sys.stdout.write('\n')
        sys.stdout.flush()
        self._IsActive = False
    
    def reset(self) -> None:
        """
        Short-cut to set the internal counter to zero (leftmost). Updates the
        view if the widget is running.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        self.setValue(0)
    
    def inc(self) -> None:
        """
        Short-cut to increase the internal counter by 1, however it will never
        go above the Range. Updates the view if the widget is running.

        Signature:
            None -> None
        
        Version 1.0.0.1
        """
        Value = self.Value
        if Value < self.Range:
            self.setValue(Value + 1)
    
    def dec(self) -> None:
        """
        Short-cut to decrease the internal counter by 1, however it will never
        go below zero. Updates the view if the widget is running.

        Signature:
            None -> None
        
        Version 1.0.0.1
        """
        Value = self.Value
        if Value > 0:
            self.setValue(Value - 1)
    
    def setValue(self, Value: int) -> None:
        """
        Explicitely changes the value of the internal counter. Updates the view
        if the widget is running.

        Signature:
            int >= 0 -> None
        
        Args:
            Value: 0 <= int <= Range; required value of the internal counter,
                cannot be negative or above the current range
        
        Raises:
            UT_TypeError: argument is not an integer
            UT_ValueError: argument is an integer but outside the allowed values
                range
        
        Version 1.0.0.1
        """
        if isinstance(Value, int):
            if (Value < 0) or (Value > self.Range):
                ErrorMessage = f'0 <= value <= {self.Range} - current value'
                raise UT_ValueError(Value, ErrorMessage, SkipFrames = 1)
        else:
            raise UT_TypeError(Value, int, SkipFrames = 1)
        self._Value = Value
        self._show()
    
    def setWidth(self, Width: int) -> None:
        """
        Changes the current width of the widget. Updates the view if the widget
        is running.

        Signature:
            int > 0 -> None
        
        Args:
            Width: int > 0; the desired width of the widget in characters,
                cannot be less than the minimum space required to fit all
                stacked eleements
        
        Raises:
            UT_TypeError: argument is not an integer
            UT_ValueError: argument is an integer but smaller than the minimum
                required space
        
        Version 1.0.0.1
        """
        MinWidth = self._Indicator.MinWidth
        if isinstance(Width, int):
            if Width < MinWidth:
                ErrorMessage = f'>= {MinWidth} - minimum width'
                raise UT_ValueError(Width, ErrorMessage, SkipFrames = 1)
        else:
            raise UT_TypeError(Width, int, SkipFrames = 1)
        self._Width = Width
        self._Indicator.setWidth(Width)
        self._show()
    
    def setRange(self, Range: int) -> None:
        """
        Changes the current maximum allowed value of the internal counter.
        Updates the view if the widget is running.

        If the current value of the internal counter exceeds the new range, it
        is set to the new range value.

        The width of the widget can increase if it is not possible to fit the
        labels.

        Signature:
            int > 0 -> None
        
        Args:
            Range: int > 0; the new range, i.e. the maximum allowed value of the
                internal counter

        Raises:
            UT_TypeError: argument is not an integer
            UT_ValueError: argument is an integer but not positive

        Version 1.0.0.1
        """
        if isinstance(Range, int):
            if Range <= 0:
                ErrorMessage = '> 0 - maximum value, i.e. range'
                raise UT_ValueError(Range, ErrorMessage, SkipFrames = 1)
        else:
            raise UT_TypeError(Range, int, SkipFrames = 1)
        if self.Value > Range:
            self._Value = Range
        if not (self._Counter is None):
            OldLength = len(str(self.Range))
            NewLength = len(str(Range))
            if OldLength != NewLength:
                MinLength = self._PBar.MinWidth + 2 * (NewLength + 1)
                if not (self._Percents is None):
                    MinLength += self._Percents.Width
                if MinLength > self.Width:
                    self._Width = MinLength
                del self._Indicator
                del self._Counter
                DisplayValue = f'{self.Value}/{Range}'
                self._Counter = TextLabel(DisplayValue,
                                                    Width = 2 * (NewLength + 1),
                                                                Alignment = 'r') 
                self._Indicator = HContainer(Width = self.Width)
                self._Indicator.addWidget(self._PBar)
                self._Indicator.addWidget(self._Counter)
                if not (self._Percents is None):
                    self._Indicator.addWidget(self._Percents)
        self._Range = Range
        self._show()
    
    def getStringValue(self) -> str:
        """
        Returns the string representation of the internal state formed depending
        on the included widgets. Basically, exactly the same string will be
        printed into the console when the state of the active / running widget
        is changed.

        Signature:
            None -> str
        
        Returns:
            str: representation of the state of the widget to be printed out
        
        Version 1.0.0.1
        """
        Position = self.Value / self.Range
        self._PBar.setValue(Position)
        if not (self._Counter is None):
            DisplayValue = f'{self.Value}/{self.Range}'
            self._Counter.setValue(DisplayValue)
        if not (self._Percents is None):
            DisplayValue = '{}%'.format((100 * self.Value) // self.Range)
            self._Percents.setValue(DisplayValue)
        return self._Indicator.getStringValue()

"""
Module clui_lib.widgets_decorators

Helper classes to define and change the appearance of CLI UI widgets.
"""

__version__= '1.0.0.0'
__date__ = '08-07-2026'
__status__ = 'Development'

#imports

from typing import ClassVar, Optional

# single characters

class SliderGaugeSimple:
    """
    Symbol to indicate the position / current value of a Slider widget.
    """
    Symbol: ClassVar[str] = '|'
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class SliderLineSimple:
    """
    Symbol to indicate the unoccupated positions of a Slider widget.
    """
    Symbol: ClassVar[str] = '-'
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class BarFullSimple:
    """
    Symbol to indicate the already progressed part of a Progress Bar.
    """
    Symbol: ClassVar[str] = '#'
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class BarEmptySimple:
    """
    Symbol to indicate the remaining part of a Progress Bar
    """
    Symbol: ClassVar[str] = ' '
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

#coupled pairs

class RoundEdgesSimple:
    """
    Pair of symbols () to enclose something
    """
    Left: ClassVar[str] = '('
    Right: ClassVar[str] = ')'
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class SquareEdgesSimple:
    """
    Pair of symbols [] to enclose something
    """
    Left: ClassVar[str] = '['
    Right: ClassVar[str] = ']'
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class PipeEdgesSimple:
    """
    Pair of symbols || to enclose something
    """
    Left: ClassVar[str] = '|'
    Right: ClassVar[str] = '|'
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class AngularEdgesSimple:
    """
    Pair of symbols <> to enclose something
    """
    Left: ClassVar[str] = '<'
    Right: ClassVar[str] = '>'
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class ReversedAngularEdgesSimple:
    """
    Pair of symbols >< to enclose something
    """
    Left: ClassVar[str] = '>'
    Right: ClassVar[str] = '<'
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

#independent pairs

class SliderDecoratorSimple:
    """
    Definition of the both elements constituting the Slider widget
    """
    Gauge: ClassVar[type] = SliderGaugeSimple
    Line: ClassVar[type] = SliderLineSimple

class BarDecoratorSimple:
    """
    Definition of the both elements constituting the Bar widget
    """
    Full: ClassVar[type] = BarFullSimple
    Empty: ClassVar[type] = BarEmptySimple

#complex widgets

class SliderWidgetDecoratorSimple:
    """
    Complete set of definitions of Slider Widget 'graphical' elements
    """
    Edges: ClassVar[type] = AngularEdgesSimple
    Slider: ClassVar[type] = SliderDecoratorSimple

class ProgressBarDecoratorSimple:
    """
    Complete set of definitions of ProgressBar Indicator 'graphical' elements
    """
    Edges: ClassVar[type] = SquareEdgesSimple
    Bar: ClassVar[type] = BarDecoratorSimple

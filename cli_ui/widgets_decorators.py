"""
Module clui_lib.widgets_decorators

Helper classes to define and change the appearance of CLI UI widgets.
"""

__version__= '1.0.0.0'
__date__ = '24-07-2026'
__status__ = 'Development'

#imports

from typing import ClassVar, Optional

# single characters

class SpinnerSimple:
    """
    Symbols to indicate the states of a Spinner widget.
    """
    Symbols: ClassVar[list[str]] = ['|', '/', '-', '\\']
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class SpinnerBrailleBarUp:
    """
    Symbols to indicate the states of a Spinner widget.
    """
    Symbols: ClassVar[list[str]] = ['\u2800', '\u28C0', '\u28E4', '\u28F6',
                                    '\u28FF', '\u283F', '\u281B', '\u2809']
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class SpinnerBrailleBarDown:
    """
    Symbols to indicate the states of a Spinner widget.
    """
    Symbols: ClassVar[list[str]] = ['\u2800', '\u2809', '\u281B', '\u283F',
                                    '\u28FF', '\u28F6', '\u28E4', '\u28C0']
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class SpinnerBrailleBarUpDown:
    """
    Symbols to indicate the states of a Spinner widget.
    """
    Symbols: ClassVar[list[str]] = ['\u2800', '\u28C0', '\u28E4', '\u28F6',
                                    '\u28FF', '\u28F6', '\u28E4', '\u28C0']
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class SpinnerBrailleCircle:
    """
    Symbols to indicate the states of a Spinner widget.
    """
    Symbols: ClassVar[list[str]] = ['\u2840', '\u2804', '\u2802', '\u2801',
                                    '\u2808', '\u2810', '\u2820', '\u2880']
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class SpinnerBrailleCircleDouble:
    """
    Symbols to indicate the states of a Spinner widget.
    """
    Symbols: ClassVar[list[str]] = ['\u28C0', '\u2844', '\u2806', '\u2803',
                                    '\u2809', '\u2818', '\u2830', '\u28A0']
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

class SpinnerBrailleCircleSpaced:
    """
    Symbols to indicate the states of a Spinner widget.
    """
    Symbols: ClassVar[list[str]] = ['\u2884', '\u2842', '\u2805', '\u280A',
                                    '\u2811', '\u2828', '\u2890', '\u2860']
    Foreground: ClassVar[Optional[int]] = None
    Background: ClassVar[Optional[int]] = None

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

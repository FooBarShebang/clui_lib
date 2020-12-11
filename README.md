# Library clui_lib

## Goal

Implements widgets to provide interactive feedback to a user in the text console. Designed for two modes of operation:

* Classic CLI mode, single threaded, when a process is executed in a blocking manner, whilst it uses some widgets to provide a progress feedback, and the user's input (as commands or options) is received in between the (sub-) tasks execution.
* Text User Interface (TUI), multi-threaded, with the tasks being executed in one thread (non-blocking) and the user intput (actions, keystrokes, etc.) is acquired in a separate thread.

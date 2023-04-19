#usr/bin/python3
"""
Module clui_lib.console.keystroke_common

Implements helper classes used for the inter-thread data exchange by the OS-
dependent implementations of a keyboard listener.

Attributes:
    ASCII_CONTROL_CODES: dict(int -> str)

Classes:
    ControlCode
    InputBuffer
"""

__version__= '1.0.0.1'
__date__ = '19-04-2023'
__status__ = 'Testing'

#imports

#+ standard libraries

from typing import Any, Sequence, List

from threading import Lock

#globals

ASCII_CONTROL_CODES = {
    0 : 'NUL',
    1 : 'SOH',
    2 : 'STX',
    3 : 'ETX',
    4 : 'EOT',
    5 : 'ENQ',
    6 : 'ACK',
    7 : 'BEL',
    8 : 'BS',
    9 : 'TAB',
    10 : 'LF',
    11 : 'VT',
    12 : 'FF',
    13 : 'CR',
    14 : 'SO',
    15 : 'SI',
    16 : 'DLE',
    17 : 'DC1',
    18 : 'DC2',
    19 : 'DC3',
    20 : 'DC4',
    21 : 'NAK',
    22 : 'SYN',
    23 : 'ETB',
    24 : 'CAN',
    25 : 'EM',
    26 : 'SUB',
    27 : 'ESC',
    28 : 'FS',
    29 : 'GS',
    30 : 'RS',
    31 : 'US',
    32 : 'SPACE',
    127 : 'DEL'
}

#classes

class ControlCode:
    """
    A simple C struct-like object to store a symbolic name of a control code
    and the possible keys or keys combinations to generate it.

    Properties:
        Name: (read-only) str; symbolic name of the control code
        Keys: (read-only) list(str); the keys (combinations) causing this code
    
    Version 1.0.0.1
    """
    
    #special methods

    def __init__(self, Name: str, Keys: Sequence[str] = ['']):
        """
        Initializer. Copies the arguments into the 'private' instance
        attributes.

        Signature:
            str, seq(str) -> None
        
        Args:
            Name: str; symbolic name of a control code
            Keys: seq(str); key(s) or keys combination(s) resulting in the
                issueing of such control code

        Version 1.0.0.1
        """
        self._Name = Name
        self._KeysSequence = list(Keys)
    
    @property
    def Name(self) -> str:
        """
        Getter property to access the stored symbolic name of a control code.

        Signature:
            None -> str
        
        Version 1.0.0.1
        """
        return self._Name
    
    @property
    def Keys(self) -> List[str]:
        """
        Getter property to access the stored keys (combinations) resulting in
        the issue of that code.

        Signature:
            None -> list(str)
        
        Version 1.0.0.1
        """
        return self._KeysSequence

class InputBuffer:
    """
    Light-weight implementation of a queue, which is designed specificially for
    a single producer and a single consumer, which might be different objects.
    Also acts as an event object. Designed for the one way data exchange between
    two objects running in the separate threads.
    
    Generally speaking, it is not thread-safe and as it has a very simple
    locking mechanism, but it is ok as long as only a single producer-consumer
    pair is expected to be present at any time.
    
    Properties:
        IsActive: (read-only) bool
        IsNotEmpty: (read-only) bool
    
    Methods:
        activate():
            None -> None
        deactivate():
            None -> None
        put(Data):
            type A -> None
        get():
            None -> type A
        empty():
            None -> None
    
    Version 1.0.0.1
    """
    
    def __init__(self) -> None:
        """
        Initializer. Creates the internal storage 'private' attribute and sets
        the queue into the 'closed' state.

        Signature:
            None -> None

        Version 1.0.0.1
        """
        self._IsActive = False
        self._Buffer = []
        self._Lock = Lock()
    
    @property
    def IsActive(self) -> bool:
        """
        Read-only property to access if the queue is 'opened' or 'closed'. To
        be used by an external process to judge if the queue can accept input,
        or the process should be terminated due to the closing of the queue,
        meaning that the client is no longer listening.
        
        Signature:
            None -> bool
        
        Version 1.0.0.1
        """
        return self._IsActive
    
    @property
    def IsNotEmpty(self) -> bool:
        """
        Read-only property to check if there are items available in the queue.
        
        Signature:
            None -> bool
        
        Version 1.0.0.1
        """
        if self._Buffer:
            Result = True
        else:
            Result = False
        return Result
    
    def activate(self) -> None:
        """
        Marks the queue as 'opened', i.e. new elements may be placed into it,
        and the existing ones - pulled from it. This also sets the internal
        flag respectively, which will signal an external process to start or
        keep on going.

        Signature:
            None -> None
        
        Version 1.0.0.1
        """
        self._IsActive = True
    
    def deactivate(self) -> None:
        """
        Marks the queue as 'closed', i.e. new elements will be not accepted
        (ignored), and the elements waiting in the queue will not be popped and
        returmed, but they will remain in the queue. This also sets the internal
        flag respectively, which will signal an external process to stop.

        Signature:
            None -> None
        
        Version 1.0.0.1
        """
        self._IsActive = False
    
    def put(self, Data: Any) -> None:
        """
        Places the received data as the last element in the queue.

        Signature:
            type A -> None
        
        Version 1.0.0.1
        """
        with self._Lock:
            if self.IsActive:
                self._Buffer.append(Data)
    
    def get(self) -> Any:
        """
        Removes the first element from the queue and returns it. If the queue is
        empty the returned value is None.

        Signature:
            None -> type A
        
        Version 1.0.0.1
        """
        if self.IsNotEmpty:
            with self._Lock:
                if self.IsActive:
                    Result = self._Buffer.pop(0)
                else:
                    Result = None
        else:
            Result = None
        return Result
    
    def empty(self):
        """
        Clears the stored content, i.e. makes the queue empty, but doesn't
        change its activity status.

        Signature:
            None -> None
        
        Version 1.0.0.1
        """
        self._Buffer.clear()
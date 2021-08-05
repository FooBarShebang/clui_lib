#usr/bin/python3

from typing import Any

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
    
    def __init__(self, Name: str, Keys: str = 'Undefined'):
        """
        """
        self._strName = Name
        self._strKeys = Keys
    
    @property
    def Name(self):
        """
        """
        return self._strName
    
    @property
    def Keys(self):
        """
        """
        return self._strKeys

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
    """
    
    def __init__(self) -> None:
        """
        """
        self._bIsActive = False
        self._lstBuffer = []
        self._objLock = Lock()
    
    @property
    def IsActive(self) -> bool:
        """
        Read-only property to access if the the input buffer is active and
        listening.
        
        Signature:
            None -> bool
        
        Version 1.0.0.0
        """
        return self._bIsActive
    
    @property
    def IsNotEmpty(self) -> bool:
        """
        Read-only property to check if there are items available in the queue.
        
        Signature:
            None -> bool
        
        Version 1.0.0.0
        """
        if len(self._lstBuffer):
            Result = True
        else:
            Result = False
        return Result
    
    def activate(self) -> None:
        """
        Signature:
            None -> None
        """
        self._bIsActive = True
    
    def deactivate(self) -> None:
        """
        Signature:
            None -> None
        """
        self._bIsActive = False
    
    def put(self, Data: Any) -> None:
        """
        Signature:
            type A -> None
        """
        with self._objLock:
            self._lstBuffer.append(Data)
    
    def get(self) -> Any:
        """
        Signature:
            None -> type A
        """
        if self.IsNotEmpty:
            with self._objLock:
                Result = self._lstBuffer.pop(0)
        else:
            Result = None
        return Result
    
    def empty(self):
        """
        Signature:
            None -> None
        """
        self._lstBuffer.clear()
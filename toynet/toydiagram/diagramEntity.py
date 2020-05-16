from enum import Enum
from abc import ABC, abstractmethod

class DeviceType(Enum):
    ROUTER = 0
    SWITCH = 1
    HOST = 2

class DiagramEntity(ABC):
    """Abstract class representing DiagramTree classes.
        Requires stringify capabilities for uniform error handling.
    """
    def __init__(self): pass

    def __str__(self) -> str: return self.toString()

    @abstractmethod
    def toString(self) -> str: pass
    """Returns detailed string to describe entity for debugging purposes """

    @abstractmethod
    def toShortString(self) -> str: pass
    """Returns concise string to describe entity for error propagation purposes """

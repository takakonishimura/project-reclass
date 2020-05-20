from typing import Any
from toydiagram.diagramEntity import DiagramEntity

class UtilError(Exception):
    """Base class for Exceptions produced by utility functions"""

class TypeCheckError(UtilError):
    """Base class for Exceptions produced by utility functions

    Attributes
        message:    str -- explanation of the error
    """

    def __init__(self, input: Any, message: str):
        self.input: Any = input
        self.message: str = message

class XMLParseError(Exception):
    """Exception raised for errors parsing a network configuration from XML file

    Attributes
        message:    str -- explanation of the error
        filename:   str -- file being parsed when error occured
    """

    def __init__(self, msg: str, filename: str):
        self.message = msg + ' (File: ' + entity.toShortString() + ')'

class ToyDiagramError(Exception):
    """Base class for Exceptions produced by ToyDiagrams"""
    pass

class DiagramGraphError(ToyDiagramError):
    """Exception raised for errors while constructing DiagramGraph which is
        traversed to create the DiagramTree.

    Attributes
        message:    str -- explanation of the error
        entity:     DiagramEntity -- optionally pass in entity to include short 
                        description in message
    """

    def __init__(self, msg: str, entity: DiagramEntity=None):
        self.message: str = msg
        if entity is not None:
            self.message = msg + ' (Entity: ' + entity.toShortString() + ')'

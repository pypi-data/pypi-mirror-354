"""
Quick and common client imports for Pax25.
"""

from . import interfaces
from .applications.application import Application
from .station import Station

__version__ = "0.5.1"

__all__ = ["Station", "Application", "interfaces"]

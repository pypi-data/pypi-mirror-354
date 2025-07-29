"""
ShuffleLM Model Implementations

This module contains the core model implementations for ShuffleLM,
including the FasterDecodeMixer architecture and base ShuffleLM class.
"""

from .shufflelm import ShuffleLM, ShuffleConfig
from .fasterdecodemixer.model import FasterDecodeMixer

__all__ = [
    "ShuffleLM",
    "ShuffleConfig", 
    "FasterDecodeMixer",
]

__version__ = "0.1.0"

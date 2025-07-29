"""
ShuffleLM: Parallel Token Generation with Intelligent Reordering

This package implements the ShuffleLM architecture, featuring parallel token generation
and intelligent reordering through MLP-Mixer and Rotary Regression.
"""

__version__ = "0.1.0"
__author__ = "thisisthepy"
__email__ = "thisisthepy@gmail.com"

from .models import (
    FasterDecodeMixer,
    ShuffleLM,
    ShuffleConfig,
)
from .utils import (
    visualize_shuffle,
    ShuffleTokenizer,
)

__all__ = [
    # Version info
    "__version__",
    "__author__", 
    "__email__",
    
    # Main models
    "FasterDecodeMixer",
    "ShuffleLM", 
    "ShuffleConfig",
    
    # Utilities
    "visualize_shuffle",
    "ShuffleTokenizer",
]

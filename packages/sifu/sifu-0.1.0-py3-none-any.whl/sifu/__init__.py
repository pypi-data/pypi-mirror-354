"""
Sifu - Enhanced Knowledge System for ELLMa

A powerful knowledge management and context-aware response system
designed to enhance conversational AI capabilities.
"""

__version__ = "0.1.0"

from .app import Sifu
from .config import settings

# Create a default instance for easy import
default_sifu = Sifu()

__all__ = ["Sifu", "settings", "default_sifu"]

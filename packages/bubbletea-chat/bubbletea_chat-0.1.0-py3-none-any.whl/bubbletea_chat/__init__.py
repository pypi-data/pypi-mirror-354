"""
BubbleTea - A Python package for building AI chatbots
Minimal version without LLM and CLI support
"""

from .components import Text, Image, Markdown, Done
from .decorators import chatbot
from .server import run_server

__version__ = "0.1.0"
__all__ = ["Text", "Image", "Markdown", "Done", "chatbot", "run_server"]
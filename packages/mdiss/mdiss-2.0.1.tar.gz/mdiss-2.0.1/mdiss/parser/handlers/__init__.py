"""
Markdown format handlers for different markdown formats.
"""
from typing import Dict, Type, Any, Optional, List

from ..models import CommandData
from .todo_format import TodoFormatHandler
from .code_block_parser import CodeBlockHandler

# Import all handlers for easy access
__all__ = [
    'FormatHandler',
    'TodoFormatHandler',
    'CodeBlockHandler',
    'format_handler_factory',
    'get_format_handler'
]

class FormatHandler:
    """Base class for format handlers."""
    
    def can_handle(self, content: str) -> bool:
        """Check if this handler can handle the given content."""
        raise NotImplementedError
    
    def parse(self, content: str, file_path: Optional[str] = None) -> list[CommandData]:
        """Parse the content and return a list of commands."""
        raise NotImplementedError


class FormatHandlerFactory:
    """Factory for creating format handlers."""
    
    def __init__(self):
        """Initialize with default handlers."""
        self._handlers: List[Type[FormatHandler]] = [
            TodoFormatHandler,  # Handles TODO.md format
            CodeBlockHandler,   # Handles simple code blocks
            # Add more handlers here as they are implemented
        ]
    
    def get_handler(self, content: str) -> Optional[FormatHandler]:
        """Get the appropriate handler for the given content."""
        for handler_cls in self._handlers:
            handler = handler_cls()
            if handler.can_handle(content):
                return handler
        return None
    
    def register_handler(self, handler_cls: Type[FormatHandler]) -> None:
        """Register a new handler."""
        if handler_cls not in self._handlers:
            self._handlers.insert(0, handler_cls)  # Insert at beginning to check first


# Initialize the default factory
format_handler_factory = FormatHandlerFactory()

def get_format_handler(content: str) -> Optional[FormatHandler]:
    """Get the appropriate format handler for the given content."""
    return format_handler_factory.get_handler(content)

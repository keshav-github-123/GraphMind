"""Custom exception classes."""
from typing import Optional, Any

class ChatbotException(Exception):
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

class ToolExecutionError(ChatbotException):
    pass

class GraphExecutionError(ChatbotException):
    pass

class DatabaseError(ChatbotException):
    pass

class VectorStoreError(ChatbotException):
    pass

class FileProcessingError(ChatbotException):
    pass
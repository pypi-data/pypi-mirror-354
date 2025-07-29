from typing import Optional, Any

from pydantic import ValidationError


class KafkaFrameworkException(Exception):
    """Base exception for Kafka framework"""
    pass

class HandlerRegistrationError(KafkaFrameworkException):
    """Raised when there's an error registering a handler"""
    def __init__(self, topic: str, message: Optional[str] = None):
        self.topic = topic
        self.message = message or f"Error registering handler for topic: {topic}"
        super().__init__(self.message)

class MessageProcessingError(KafkaFrameworkException):
    """Raised when there's an error processing a message"""
    def __init__(self, topic: str, offset: int, message: Optional[str] = None):
        self.topic = topic
        self.offset = offset
        self.message = message or f"Error processing message from topic: {topic} at offset: {offset}"
        super().__init__(self.message)

class MessageValidationError(KafkaFrameworkException, ValidationError):
    """Raised when a message fails validation"""
    def __init__(self, errors: dict[str, Any], message: Optional[str] = None):
        self.errors = errors
        self.message = message or "Message validation failed"
        super().__init__(self.message)
        ValidationError.__init__(self, errors, None)

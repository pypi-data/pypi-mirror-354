from typing import Any, Optional, Dict, Type, Union

from pydantic import BaseModel, Field


class KafkaMessage(BaseModel):
    """Base class for Kafka message schemas"""
    pass

class KafkaResponse(BaseModel):
    """Base class for Kafka response schemas"""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None

class ValidationErrorResponse(KafkaResponse):
    """Response schema for validation errors"""
    success: bool = False
    errors: Dict[str, Any] = Field(default_factory=dict)

def validate_message(
    msg: Any,
    schema: Type[BaseModel]
) -> Union[BaseModel, ValidationErrorResponse]:
    """Validate a message against a Pydantic schema"""
    try:
        return schema(**msg)
    except Exception as e:
        return ValidationErrorResponse(
            message=str(e),
            errors=getattr(e, 'errors', {})
        )

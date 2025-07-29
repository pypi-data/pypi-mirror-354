# KafkaFramework

A modular Python microframework for building Kafka-based applications, inspired by FastAPI's simplicity and elegance.

## Features

- Asynchronous Kafka topic routing with decorators
- Priority-based message processing
- Pydantic-based schema validation
- Middleware support for pre and post processing
- Startup and shutdown event handlers
- Custom error handling and validation
- Clean, extensible architecture

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Installation

```bash
# Using uv (recommended)
uv pip install kafka-framework

# Or using pip
pip install kafka-framework
```

## Basic Usage

```python
from kafka_framework import KafkaApp, kafka_handler
from kafka_framework.schemas import KafkaMessage
from kafka_framework.context import MessageContext

app = KafkaApp()

class UserCreated(KafkaMessage):
    user_id: str
    name: str
    email: str

# High priority handler (higher number = higher priority)
@kafka_handler("user.created", priority=10)
async def handle_important_users(ctx: MessageContext):
    msg = UserCreated(**ctx.value)
    print(f"Processing high-priority user: {msg.name}")

# Default priority handler (priority=1)
@kafka_handler("user.created")
async def handle_regular_users(ctx: MessageContext):
    msg = UserCreated(**ctx.value)
    print(f"Processing regular user: {msg.name}")

@app.on_startup
async def startup():
    print("Application starting up...")

@app.on_shutdown
async def shutdown():
    print("Application shutting down...")

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
```

## Middleware Example

```python
from kafka_framework import MiddlewareManager
from kafka_framework.context import MessageContext
from typing import Callable

@MiddlewareManager.pre_middleware
async def logging_middleware(ctx: MessageContext, handler: Callable):
    print(f"Processing message from topic: {ctx.topic}")
    return ctx

@MiddlewareManager.post_middleware
async def error_handling_middleware(ctx: MessageContext, handler: Callable):
    try:
        return await handler(ctx)
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        raise
```

## Priority-Based Processing

Handlers can be assigned priorities to control the order of message processing:

```python
# This handler will process messages before lower priority handlers
@kafka_handler("critical.events", priority=100)
async def handle_critical_events(ctx: MessageContext):
    # Process critical events first
    pass

# This handler will process messages after higher priority handlers
@kafka_handler("regular.events", priority=1)
async def handle_regular_events(ctx: MessageContext):
    # Process regular events
    pass
```

## Error Handling

```python
from kafka_framework.exceptions import MessageValidationError

@kafka_handler("user.actions")
async def handle_user_actions(ctx: MessageContext):
    try:
        # Your message processing logic
        pass
    except MessageValidationError as e:
        print(f"Validation error: {e.errors}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise
```

## Development

```bash
# Install development dependencies
uv pip install -e .[dev]

# Run tests
uv pip run pytest

# Format code
uv pip run black .
uv pip run isort .
uv pip run flake8
```

## License

MIT

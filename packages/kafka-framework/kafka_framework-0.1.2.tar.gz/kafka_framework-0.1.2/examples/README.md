# Kafka Framework Examples

This directory contains example implementations demonstrating how to use the Kafka Framework in a real-world scenario with user and order management.

## Prerequisites

- Python 3.8+
- Running Kafka cluster (local or remote)
- Required Python packages (install with `pip install -r requirements.txt`)

## Project Structure

```
examples/
├── __init__.py
├── app.py                 # Main application entry point
├── handlers/             # Event handlers
│   ├── __init__.py
│   ├── user_handlers.py  # User-related event handlers
│   └── order_handlers.py # Order-related event handlers
├── schemas/              # Pydantic models
│   ├── __init__.py
│   ├── user.py           # User-related schemas
│   └── order.py          # Order-related schemas
└── produce_test_messages.py  # Script to generate test messages
```

## Getting Started

### 1. Install Dependencies

```bash
# Navigate to the project root
cd /path/to/kafka-framework

# Install the package in development mode
pip install -e .


# Install example dependencies
cd examples
pip install -r requirements.txt
```

### 2. Configure Kafka

Make sure you have a Kafka cluster running. Update the Kafka broker address in `app.py` if not using the default `localhost:9092`.

### 3. Run the Application

Start the Kafka consumer application:

```bash
python -m examples.app
```

### 4. Produce Test Messages

In a separate terminal, run the test message producer:

```bash
python -m examples.produce_test_messages
```

This will generate sample user and order events that will be processed by the application.

## Example Handlers

### User Handlers

- `handle_user_created`: Processes new user registrations
- `handle_user_updated`: Handles user profile updates
- `handle_user_deleted`: Manages user account deletion (soft delete)

### Order Handlers

- `handle_order_created`: Processes new orders
- `handle_order_updated`: Manages order status updates
- `handle_order_cancelled`: Handles order cancellations and refunds

## Middleware

The example includes two middleware components:

1. **LoggingMiddleware**: Logs message processing lifecycle events
2. **RetryMiddleware**: Implements exponential backoff for failed message processing

## Metrics

The application exposes Prometheus metrics on port 9091 by default. You can access them at:

```
http://localhost:9091/metrics
```

## Customization

To adapt this example to your needs:

1. Update the schemas in the `schemas/` directory
2. Modify the handlers in the `handlers/` directory
3. Add new middleware as needed
4. Update the configuration in `app.py`

## Testing

Run the test suite:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

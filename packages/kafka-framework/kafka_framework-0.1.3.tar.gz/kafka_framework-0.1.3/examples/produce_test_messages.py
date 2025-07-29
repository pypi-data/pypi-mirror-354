import asyncio
import json
import uuid
from datetime import datetime
from aiokafka import AIOKafkaProducer

# Sample test data
SAMPLE_USERS = [
    {
        "email": "alice@example.com",
        "username": "alice",
        "full_name": "Alice Johnson",
        "role": "user",
        "hashed_password": "hashed_password_123",
    },
    {
        "email": "bob@example.com",
        "username": "bob",
        "full_name": "Bob Smith",
        "role": "admin",
        "hashed_password": "hashed_password_456",
    },
]

SAMPLE_ORDERS = [
    {
        "order_number": "ORD-1001",
        "user_id": "user_123",
        "items": [
            {
                "product_id": "prod_1",
                "quantity": 2,
                "unit_price": 99.99,
                "discount": 10.0,
            },
            {
                "product_id": "prod_2",
                "quantity": 1,
                "unit_price": 49.99,
                "discount": 0.0,
            },
        ],
        "shipping_address": {
            "street": "123 Main St",
            "city": "Anytown",
            "country": "USA",
        },
        "billing_address": {
            "street": "123 Main St",
            "city": "Anytown",
            "country": "USA",
        },
        "total_amount": 239.97,
        "tax_amount": 28.80,
        "grand_total": 268.77,
    },
    {
        "order_number": "ORD-1002",
        "user_id": "user_456",
        "items": [
            {
                "product_id": "prod_3",
                "quantity": 1,
                "unit_price": 199.99,
                "discount": 0.0,
            }
        ],
        "shipping_address": {
            "street": "456 Oak Ave",
            "city": "Somewhere",
            "country": "USA",
        },
        "billing_address": {
            "street": "456 Oak Ave",
            "city": "Somewhere",
            "country": "USA",
        },
        "total_amount": 199.99,
        "tax_amount": 24.00,
        "grand_total": 223.99,
    },
]


async def produce_messages():
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all",
        retries=3,
        compression_type="gzip",
    )

    await producer.start()

    try:
        # Produce user events
        for user in SAMPLE_USERS:
            user_id = f"user_{uuid.uuid4().hex[:8]}"

            # User created event
            user_created = {
                "event_type": "user.created",
                "user_id": user_id,
                "user_data": user,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {"source": "test_script"},
            }

            await producer.send("user.events", value=user_created)
            print(f"Produced user.created event for user: {user['email']}")

            # Simulate user update
            user_updated = {
                "event_type": "user.updated",
                "user_id": user_id,
                "user_data": {
                    "full_name": f"{user['full_name']} (Updated)",
                    "is_active": True,
                },
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {"source": "test_script"},
            }

            await producer.send("user.events", value=user_updated)
            print(f"Produced user.updated event for user: {user['email']}")

        # Produce order events
        for order in SAMPLE_ORDERS:
            order_id = f"order_{uuid.uuid4().hex[:8]}"

            # Order created event
            order_created = {
                "event_type": "order.created",
                "order_id": order_id,
                "order_data": {
                    **order,
                    "status": "pending",
                    "created_at": datetime.utcnow().isoformat(),
                },
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {"source": "test_script"},
            }

            await producer.send("order.events", value=order_created)
            print(f"Produced order.created event for order: {order['order_number']}")

            # Simulate order status updates
            for status in ["processing", "shipped", "delivered"]:
                order_updated = {
                    "event_type": "order.updated",
                    "order_id": order_id,
                    "order_data": {
                        "status": status,
                        "updated_at": datetime.utcnow().isoformat(),
                    },
                    "timestamp": datetime.utcnow().isoformat(),
                    "metadata": {"source": "test_script"},
                }

                await producer.send("order.events", value=order_updated)
                print(
                    f"Produced order.updated event for order {order['order_number']} - Status: {status}"
                )

                # Add a small delay between status updates
                await asyncio.sleep(1)

        # Ensure all messages are delivered
        await producer.flush()
        print("All test messages have been produced successfully!")

    except Exception as e:
        print(f"Error producing messages: {e}")
        raise
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(produce_messages())

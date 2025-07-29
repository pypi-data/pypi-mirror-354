from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime
from typing import List, Optional
from decimal import Decimal


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderEventType(str, Enum):
    CREATED = "order.created"
    UPDATED = "order.updated"
    CANCELLED = "order.cancelled"
    COMPLETED = "order.completed"


class OrderItem(BaseModel):
    """Represents a single item in an order."""

    product_id: str
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)
    discount: Decimal = Field(default=0, ge=0)

    @property
    def total_price(self) -> Decimal:
        """Calculate the total price for this order item."""
        return round((self.unit_price - self.discount) * self.quantity, 2)


class OrderBase(BaseModel):
    """Base order model with common fields."""

    user_id: str
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    shipping_address: dict
    billing_address: dict
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    """Schema for creating a new order."""

    pass


class OrderUpdate(BaseModel):
    """Schema for updating an existing order."""

    status: Optional[OrderStatus] = None
    tracking_number: Optional[str] = None
    shipping_address: Optional[dict] = None
    billing_address: Optional[dict] = None
    notes: Optional[str] = None


class OrderInDB(OrderBase):
    """Order model as stored in the database."""

    id: str
    order_number: str
    created_at: datetime
    updated_at: datetime
    total_amount: Decimal
    tax_amount: Decimal
    discount_amount: Decimal = 0
    grand_total: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderEvent(BaseModel):
    """Schema for order-related events."""

    event_type: OrderEventType
    order_id: str
    order_data: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = {}

    @property
    def is_high_value(self) -> bool:
        """Check if this is a high-value order."""
        return self.order_data.get("grand_total", 0) > 1000

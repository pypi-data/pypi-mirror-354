from datetime import datetime
from typing import Any, Dict


class MessageContext:
    def __init__(
        self,
        topic: str,
        partition: int,
        offset: int,
        key: Any,
        value: Any,
        timestamp: int,
    ):
        self.topic = topic
        self.partition = partition
        self.offset = offset
        self.key = key
        self.value = value
        self.timestamp = timestamp
        self.timestamp_dt = datetime.fromtimestamp(timestamp/1000)
        self.metadata: Dict[str, Any] = {}
        
    def set_metadata(self, key: str, value: Any) -> None:
        """Set additional metadata for the message context"""
        self.metadata[key] = value
        
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value by key"""
        return self.metadata.get(key, default)
        
    def __repr__(self):
        return (f"MessageContext(topic={self.topic}, "
                f"partition={self.partition}, "
                f"offset={self.offset}, "
                f"timestamp={self.timestamp_dt})")

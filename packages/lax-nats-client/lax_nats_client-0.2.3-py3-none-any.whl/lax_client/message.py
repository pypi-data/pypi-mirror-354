"""Message wrapper for received messages."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Any
import json


@dataclass
class Message:
    """Wrapper for received messages from subscriptions."""
    
    # Message content
    id: str
    subject: str
    data: bytes
    headers: Dict[str, str]
    
    # Metadata
    sequence: int
    timestamp: datetime
    trace_id: Optional[str] = None
    
    # Delivery info
    redelivered: bool = False
    delivery_count: int = 1
    
    # Internal reference to ack/nack the message
    _ack_func: Optional[Any] = None
    _nack_func: Optional[Any] = None
    
    def get_data_as_string(self) -> str:
        """Get message data as string."""
        return self.data.decode('utf-8')
    
    def get_data_as_json(self) -> dict:
        """Get message data as JSON object."""
        return json.loads(self.data.decode('utf-8'))
    
    async def ack(self):
        """Acknowledge the message."""
        if self._ack_func:
            await self._ack_func()
    
    async def nack(self, delay: float = 0):
        """Negative acknowledge (requeue) the message."""
        if self._nack_func:
            await self._nack_func(delay)
    
    @classmethod
    def from_proto(cls, proto_msg, ack_func=None, nack_func=None) -> "Message":
        """Create Message from protobuf Message."""
        # Convert protobuf timestamp to datetime
        timestamp = datetime.fromtimestamp(
            proto_msg.timestamp.seconds + proto_msg.timestamp.nanos / 1e9
        )
        
        return cls(
            id=proto_msg.id,
            subject=proto_msg.subject,
            data=proto_msg.payload,
            headers=dict(proto_msg.headers),
            sequence=proto_msg.sequence,
            timestamp=timestamp,
            trace_id=proto_msg.trace_id or None,
            _ack_func=ack_func,
            _nack_func=nack_func
        )
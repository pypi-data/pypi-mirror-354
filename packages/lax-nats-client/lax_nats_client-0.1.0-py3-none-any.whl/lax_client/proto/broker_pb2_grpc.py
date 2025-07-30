"""Minimal gRPC stub for broker service.

In production, this would be generated from broker.proto
"""

class BrokerServiceStub:
    """Stub for BrokerService."""
    
    def __init__(self, channel):
        self.channel = channel
        # In production, this would setup actual gRPC methods
        
    async def Publish(self, request, timeout=None):
        """Placeholder for Publish RPC."""
        # This would make actual gRPC call
        from . import broker_pb2
        return broker_pb2.PublishResponse(
            message_id="test-id",
            timestamp="2024-01-01T00:00:00Z"
        )
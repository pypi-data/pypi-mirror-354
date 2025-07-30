"""FastAPI integration example for LAX NATS client.

This example shows how to use the LAX client in a FastAPI application
with proper lifecycle management and dependency injection.
"""

from contextlib import asynccontextmanager
from typing import Dict, Any, Optional
import logging

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

from lax_client import LaxClient, ClientOptions, PublishOptions, Tier
from lax_client.exceptions import PublishError, CircuitBreakerOpen


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models for API
class PublishRequest(BaseModel):
    """Request model for publishing messages."""
    subject: str = Field(..., description="Topic/subject to publish to")
    data: Dict[str, Any] = Field(..., description="Message data")
    tier: str = Field(default="memory", description="Storage tier: memory, replicated, persistent")
    require_ack: bool = Field(default=False, description="Require acknowledgment")
    headers: Optional[Dict[str, str]] = Field(default=None, description="Optional headers")


class PublishResponse(BaseModel):
    """Response model for publish operations."""
    message_id: str
    tier: str
    method: str  # "nats" or "grpc"


class BatchPublishRequest(BaseModel):
    """Request model for batch publishing."""
    messages: list[PublishRequest]
    
    
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    nats_connected: bool
    circuit_breaker_state: str


# Global client instance
lax_client: Optional[LaxClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    global lax_client
    
    # Startup
    logger.info("Starting LAX client...")
    
    # Configure client
    options = ClientOptions(
        nats_urls=["nats://localhost:4222"],
        broker_addr="localhost:50051",
        connection_pool_size=20,  # More connections for high concurrency
        max_concurrent_publishes=1000,
        log_level="INFO",
        enable_metrics=True,
    )
    
    # Create and connect client
    lax_client = LaxClient(options)
    await lax_client.connect()
    logger.info("LAX client connected")
    
    yield
    
    # Shutdown
    logger.info("Shutting down LAX client...")
    if lax_client:
        await lax_client.close()
    logger.info("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="LAX NATS FastAPI Example",
    description="Example FastAPI service using LAX NATS smart client",
    version="0.1.0",
    lifespan=lifespan,
)


def get_client() -> LaxClient:
    """Dependency to get LAX client."""
    if not lax_client:
        raise HTTPException(status_code=503, detail="Client not initialized")
    return lax_client


@app.get("/health", response_model=HealthResponse)
async def health_check(client: LaxClient = Depends(get_client)):
    """Health check endpoint."""
    return HealthResponse(
        status="healthy" if client.is_connected else "unhealthy",
        nats_connected=client._nc.is_connected if client._nc else False,
        circuit_breaker_state=client._circuit_breaker.state.value,
    )


@app.post("/publish", response_model=PublishResponse)
async def publish_message(
    request: PublishRequest,
    client: LaxClient = Depends(get_client),
):
    """Publish a single message.
    
    The client will automatically route to direct NATS or gRPC based on tier.
    """
    try:
        # Create publish options
        options = PublishOptions(
            tier=Tier(request.tier),
            require_ack=request.require_ack,
            headers=request.headers,
        )
        
        # Publish message
        message_id = await client.publish(
            subject=request.subject,
            data=request.data,
            options=options,
        )
        
        # Determine which method was used
        method = "nats" if options.should_use_nats() else "grpc"
        
        return PublishResponse(
            message_id=message_id,
            tier=request.tier,
            method=method,
        )
        
    except CircuitBreakerOpen:
        raise HTTPException(
            status_code=503,
            detail="Circuit breaker is open due to too many failures"
        )
    except PublishError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/publish/batch")
async def publish_batch(
    request: BatchPublishRequest,
    client: LaxClient = Depends(get_client),
):
    """Publish multiple messages efficiently."""
    messages = []
    
    for msg in request.messages:
        messages.append({
            "subject": msg.subject,
            "data": msg.data,
            "options": PublishOptions(
                tier=Tier(msg.tier),
                require_ack=msg.require_ack,
                headers=msg.headers,
            )
        })
    
    try:
        results = await client.batch_publish(messages)
        return results
    except Exception as e:
        logger.error(f"Batch publish error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/publish/async")
async def publish_async(
    request: PublishRequest,
    background_tasks: BackgroundTasks,
    client: LaxClient = Depends(get_client),
):
    """Publish message in background (fire-and-forget)."""
    
    async def _publish():
        try:
            options = PublishOptions(
                tier=Tier(request.tier),
                require_ack=request.require_ack,
                headers=request.headers,
            )
            
            await client.publish(
                subject=request.subject,
                data=request.data,
                options=options,
            )
        except Exception as e:
            logger.error(f"Background publish failed: {e}")
    
    # Add to background tasks
    background_tasks.add_task(_publish)
    
    return {"status": "accepted", "message": "Message queued for publishing"}


# Example domain-specific endpoints
@app.post("/events/user-action")
async def track_user_action(
    user_id: str,
    action: str,
    metadata: Optional[Dict[str, Any]] = None,
    client: LaxClient = Depends(get_client),
):
    """Track user actions (high-volume, memory tier)."""
    data = {
        "user_id": user_id,
        "action": action,
        "metadata": metadata or {},
        "timestamp": "2024-01-01T00:00:00Z",  # Would use real timestamp
    }
    
    # Use memory tier for high-volume events
    message_id = await client.publish(
        subject=f"events.user.{action}",
        data=data,
        options=PublishOptions(tier=Tier.MEMORY),
    )
    
    return {"message_id": message_id, "status": "tracked"}


@app.post("/orders")
async def create_order(
    order_id: str,
    user_id: str,
    items: list[dict],
    total: float,
    client: LaxClient = Depends(get_client),
):
    """Create order (critical data, persistent tier)."""
    order_data = {
        "order_id": order_id,
        "user_id": user_id,
        "items": items,
        "total": total,
        "status": "pending",
    }
    
    # Use persistent tier for critical data
    message_id = await client.publish(
        subject="orders.created",
        data=order_data,
        options=PublishOptions(
            tier=Tier.PERSISTENT,
            require_ack=True,
            headers={"order-id": order_id},
        ),
    )
    
    return {
        "order_id": order_id,
        "message_id": message_id,
        "status": "created",
    }


@app.get("/metrics")
async def get_metrics():
    """Expose Prometheus metrics."""
    # In production, you'd use prometheus_client.generate_latest()
    return {"message": "Metrics would be exposed here"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
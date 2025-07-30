# LAX NATS JetStream Python SDK

A high-performance Python client SDK for LAX NATS JetStream broker with intelligent routing between direct NATS (for ultra-low latency) and gRPC (for advanced features).

Perfect for FastAPI and other async Python applications.

## Features

- 🚀 **Smart Routing**: Automatically routes to direct NATS (<1ms) or gRPC based on requirements
- 🔄 **Async/Await**: Built for modern async Python applications
- ⚡ **FastAPI Ready**: First-class FastAPI integration
- 🛡️ **Circuit Breaker**: Protects against cascading failures
- 📊 **Prometheus Metrics**: Built-in observability
- 🔁 **Retry Logic**: Configurable retry with exponential backoff
- 🏊 **Connection Pooling**: gRPC connection pool for high throughput

## Installation

```bash
pip install lax-nats-client

# For FastAPI integration
pip install lax-nats-client[fastapi]
```

## Quick Start

```python
import asyncio
from lax_client import LaxClient, PublishOptions, Tier

async def main():
    # Create client
    async with LaxClient() as client:
        # Publish to memory tier (uses direct NATS, <1ms latency)
        await client.publish(
            "events.user.login",
            {"user_id": "123", "ip": "192.168.1.1"}
        )
        
        # Publish to persistent tier (uses gRPC, guaranteed delivery)
        await client.publish(
            "orders.created",
            {"order_id": "456", "amount": 99.99},
            options=PublishOptions(
                tier=Tier.PERSISTENT,
                require_ack=True
            )
        )

asyncio.run(main())
```

## FastAPI Integration

```python
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from lax_client import LaxClient, ClientOptions

# Global client
lax_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global lax_client
    # Startup
    lax_client = LaxClient(ClientOptions(
        nats_urls=["nats://localhost:4222"],
        broker_addr="localhost:50051",
    ))
    await lax_client.connect()
    yield
    # Shutdown
    await lax_client.close()

app = FastAPI(lifespan=lifespan)

def get_client() -> LaxClient:
    return lax_client

@app.post("/events")
async def publish_event(
    data: dict,
    client: LaxClient = Depends(get_client)
):
    # Automatically uses direct NATS for memory tier
    message_id = await client.publish("events.api", data)
    return {"message_id": message_id}

@app.post("/orders")
async def create_order(
    order: dict,
    client: LaxClient = Depends(get_client)
):
    # Uses gRPC for persistent tier
    message_id = await client.publish(
        "orders.created",
        order,
        options=PublishOptions(tier=Tier.PERSISTENT, require_ack=True)
    )
    return {"order_id": order["id"], "message_id": message_id}
```

## Configuration

```python
from lax_client import ClientOptions

options = ClientOptions(
    # NATS settings
    nats_urls=["nats://nats1:4222", "nats://nats2:4222"],
    nats_connect_timeout=5.0,
    
    # gRPC settings
    broker_addr="broker:50051",
    connection_pool_size=20,
    
    # Performance tuning
    max_concurrent_publishes=1000,
    publish_timeout=5.0,
    retry_attempts=3,
    
    # Circuit breaker
    circuit_breaker_threshold=10,
    circuit_breaker_timeout=30.0,
    
    # Metrics
    enable_metrics=True,
    metrics_prefix="myapp_lax",
    
    # Logging
    log_level="INFO",
)

client = LaxClient(options)
```

## Publishing Options

```python
from lax_client import PublishOptions, Tier

# Memory tier (default) - Ultra fast, no persistence
await client.publish("topic", data)

# With specific tier
await client.publish(
    "topic", 
    data,
    options=PublishOptions(tier=Tier.PERSISTENT)
)

# Require acknowledgment (forces gRPC path)
await client.publish(
    "topic",
    data, 
    options=PublishOptions(require_ack=True)
)

# With headers and timeout
await client.publish(
    "topic",
    data,
    options=PublishOptions(
        tier=Tier.REPLICATED,
        headers={"trace-id": "abc123"},
        timeout=2.0
    )
)

# Batch publish for efficiency
messages = [
    {"subject": "events.click", "data": {"button": "submit"}},
    {"subject": "events.view", "data": {"page": "/home"}},
]
results = await client.batch_publish(messages)
print(f"Sent {results['success_count']} messages")
```

## Smart Routing Logic

The SDK automatically chooses the optimal path:

| Condition | Route | Latency | Use Case |
|-----------|-------|---------|----------|
| `tier=memory` & `require_ack=False` | Direct NATS | <1ms | Events, metrics, logs |
| `tier=persistent/replicated` | gRPC to broker | 10-50ms | Orders, payments |
| `require_ack=True` | gRPC to broker | 10-50ms | Critical data |

## Performance

Based on benchmarks:

| Method | Throughput | P99 Latency |
|--------|------------|-------------|
| Direct NATS (memory) | 100k+ msg/sec | <5ms |
| gRPC (persistent) | 5k msg/sec | 50ms |

## Error Handling

```python
from lax_client.exceptions import (
    PublishError,
    CircuitBreakerOpen,
    ConnectionError
)

try:
    await client.publish("topic", data)
except CircuitBreakerOpen:
    # Too many failures, circuit breaker is open
    logger.error("Circuit breaker open, service degraded")
except PublishError as e:
    # Publish failed after retries
    logger.error(f"Publish failed: {e}")
except ConnectionError as e:
    # Connection issues
    logger.error(f"Connection error: {e}")
```

## Metrics

When enabled, Prometheus metrics are exposed:

```python
# In your FastAPI app
from prometheus_client import generate_latest

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

Available metrics:
- `lax_client_publish_total{tier,status}`
- `lax_client_publish_latency_seconds{tier,method}`
- `lax_client_direct_nats_total`
- `lax_client_grpc_total`
- `lax_client_circuit_breaker_state`

## Examples

See the [examples](examples/) directory for:
- [Simple async usage](examples/simple/async_example.py)
- [FastAPI integration](examples/fastapi/main.py)
- [Performance testing](examples/simple/performance_test.py)

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black lax_client/

# Type checking
mypy lax_client/
```

## License

MIT License - see LICENSE file for details.
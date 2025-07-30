"""Simple async example of using the LAX NATS client."""

import asyncio
import json
from datetime import datetime

from lax_client import LaxClient, ClientOptions, PublishOptions, Tier


async def main():
    # Configure client
    options = ClientOptions(
        nats_urls=["nats://localhost:4222"],
        broker_addr="localhost:50051",
        log_level="INFO",
    )
    
    # Use async context manager
    async with LaxClient(options) as client:
        print("Connected to LAX NATS broker\n")
        
        # Example 1: Simple publish (memory tier, uses direct NATS)
        print("1. Publishing to memory tier (direct NATS)...")
        message_id = await client.publish(
            subject="events.user.login",
            data={
                "user_id": "user123",
                "timestamp": datetime.utcnow().isoformat(),
                "ip": "192.168.1.1"
            }
        )
        print(f"✅ Published with ID: {message_id} (used direct NATS)\n")
        
        # Example 2: Persistent publish (uses gRPC)
        print("2. Publishing to persistent tier (via gRPC)...")
        try:
            message_id = await client.publish(
                subject="orders.created",
                data={
                    "order_id": "order456",
                    "user_id": "user123",
                    "amount": 99.99,
                    "items": ["item1", "item2"]
                },
                options=PublishOptions(
                    tier=Tier.PERSISTENT,
                    require_ack=True,
                    headers={"order-id": "order456"}
                )
            )
            print(f"✅ Published with ID: {message_id} (used gRPC)\n")
        except Exception as e:
            print(f"❌ Persistent publish failed: {e}\n")
        
        # Example 3: Batch publish
        print("3. Batch publishing...")
        messages = [
            {
                "subject": f"metrics.cpu",
                "data": {"value": 45.2 + i, "host": "server1"},
            }
            for i in range(10)
        ]
        
        results = await client.batch_publish(messages)
        print(f"✅ Batch results: {results['success_count']} succeeded, "
              f"{results['failure_count']} failed\n")
        
        # Example 4: High-throughput test
        print("4. High-throughput test (1000 messages)...")
        start = asyncio.get_event_loop().time()
        
        tasks = []
        for i in range(1000):
            task = client.publish(
                subject="stress.test",
                data={"index": i, "timestamp": datetime.utcnow().isoformat()},
                options=PublishOptions(tier=Tier.MEMORY)
            )
            tasks.append(task)
        
        # Wait for all publishes
        await asyncio.gather(*tasks, return_exceptions=True)
        
        elapsed = asyncio.get_event_loop().time() - start
        rate = 1000 / elapsed
        print(f"✅ Published 1000 messages in {elapsed:.3f}s ({rate:.0f} msg/sec)\n")
        
        # Example 5: Publish with different tiers
        print("5. Testing different tiers...")
        tiers = [
            (Tier.MEMORY, "User clicked button"),
            (Tier.REPLICATED, "User profile updated"),
            (Tier.PERSISTENT, "Payment processed"),
        ]
        
        for tier, event in tiers:
            try:
                message_id = await client.publish(
                    subject=f"events.{tier.value}",
                    data={"event": event, "tier": tier.value},
                    options=PublishOptions(tier=tier)
                )
                method = "NATS" if tier == Tier.MEMORY else "gRPC"
                print(f"  {tier.value}: ✅ via {method}")
            except Exception as e:
                print(f"  {tier.value}: ❌ {e}")


if __name__ == "__main__":
    asyncio.run(main())
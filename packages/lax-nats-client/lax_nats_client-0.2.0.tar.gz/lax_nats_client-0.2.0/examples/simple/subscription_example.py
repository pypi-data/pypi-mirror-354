"""Example demonstrating the new subscription functionality."""

import asyncio
import json
from lax_client import (
    LaxClient, 
    ClientOptions, 
    PublishOptions, 
    SubscribeOptions,
    ConsumerGroupConfig,
    Tier
)


async def main():
    # Create client
    client = LaxClient(
        ClientOptions(
            broker_addr="localhost:50051",
            nats_urls=["nats://localhost:4222"]
        )
    )
    
    async with client:
        print("=== LAX Client Subscription Example ===\n")
        
        # 1. Create a consumer group
        print("1. Creating consumer group...")
        try:
            group = await client.create_consumer_group(
                name="example-processors",
                stream="PERSISTENT_STREAM",
                subject_filter="orders.*",
                config=ConsumerGroupConfig(
                    deliver_policy="new",
                    max_deliver=3,
                    ack_wait_seconds=30
                )
            )
            print(f"   Consumer group created/joined: {group}\n")
        except Exception as e:
            print(f"   Error creating consumer group: {e}\n")
        
        # 2. Publish some test messages
        print("2. Publishing test messages...")
        for i in range(5):
            msg_id = await client.publish(
                subject=f"orders.created",
                data={"order_id": f"ORDER-{i}", "amount": 100 + i * 10},
                options=PublishOptions(
                    tier=Tier.PERSISTENT,
                    require_ack=True
                )
            )
            print(f"   Published message {i}: {msg_id}")
        print()
        
        # 3. Subscribe using iterator style
        print("3. Subscribing with iterator style (processing 3 messages)...")
        try:
            count = 0
            async for msg in client.subscribe(
                subject="orders.*",
                consumer_group="example-processors",
                options=SubscribeOptions(
                    max_inflight=10,
                    manual_ack=True,
                    prefetch=5
                )
            ):
                print(f"   Received: {msg.subject} - {msg.get_data_as_json()}")
                await msg.ack()
                count += 1
                if count >= 3:
                    break
        except Exception as e:
            print(f"   Subscription error: {e}")
        print()
        
        # 4. Subscribe using callback style
        print("4. Subscribing with callback style...")
        processed = []
        
        async def message_handler(msg):
            data = msg.get_data_as_json()
            print(f"   [Callback] Received: {msg.subject} - {data}")
            processed.append(data)
            await msg.ack()
            
            # Stop after processing 2 messages
            if len(processed) >= 2:
                raise KeyboardInterrupt("Processed enough messages")
        
        try:
            await client.subscribe(
                subject="orders.*",
                consumer_group="example-processors",
                options=SubscribeOptions(
                    max_inflight=10,
                    manual_ack=True
                ),
                callback=message_handler
            )
        except KeyboardInterrupt:
            print("   Callback subscription stopped")
        except Exception as e:
            print(f"   Callback error: {e}")
        
        print(f"\n   Total processed via callback: {len(processed)} messages")
        
        print("\n=== Example completed ===")


if __name__ == "__main__":
    asyncio.run(main())
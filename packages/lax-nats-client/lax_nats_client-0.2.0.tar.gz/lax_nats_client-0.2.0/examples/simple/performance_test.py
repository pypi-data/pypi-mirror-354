"""Performance test for Python LAX client."""

import asyncio
import time
import statistics
from typing import List

from lax_client import LaxClient, ClientOptions, PublishOptions, Tier


async def benchmark_tier(client: LaxClient, tier: Tier, num_messages: int = 10000):
    """Benchmark publishing to a specific tier."""
    print(f"\nBenchmarking {tier.value} tier ({num_messages} messages)...")
    
    # Prepare data
    data = b"x" * 1024  # 1KB payload
    subject = f"bench.{tier.value}"
    options = PublishOptions(tier=tier)
    
    # Collect latencies
    latencies: List[float] = []
    errors = 0
    
    # Run benchmark
    start_time = time.time()
    
    for i in range(num_messages):
        msg_start = time.time()
        try:
            await client.publish(subject, data, options)
            latencies.append((time.time() - msg_start) * 1000)  # Convert to ms
        except Exception as e:
            errors += 1
            if errors == 1:  # Log first error only
                print(f"  First error: {e}")
    
    elapsed = time.time() - start_time
    
    # Calculate statistics
    if latencies:
        rate = len(latencies) / elapsed
        throughput_mb = (rate * 1024) / (1024 * 1024)  # MB/sec
        
        latencies.sort()
        p50 = latencies[int(len(latencies) * 0.50)]
        p95 = latencies[int(len(latencies) * 0.95)]
        p99 = latencies[int(len(latencies) * 0.99)]
        
        print(f"  Results for {tier.value}:")
        print(f"    Messages sent: {len(latencies)}")
        print(f"    Errors: {errors}")
        print(f"    Rate: {rate:.0f} msg/sec")
        print(f"    Throughput: {throughput_mb:.2f} MB/sec")
        print(f"    Latency P50: {p50:.2f}ms")
        print(f"    Latency P95: {p95:.2f}ms")
        print(f"    Latency P99: {p99:.2f}ms")
        print(f"    Method: {'Direct NATS' if tier == Tier.MEMORY else 'gRPC'}")
    else:
        print(f"  All {num_messages} messages failed!")


async def concurrent_benchmark(client: LaxClient, num_publishers: int = 10):
    """Test with concurrent publishers."""
    print(f"\nConcurrent benchmark ({num_publishers} publishers)...")
    
    async def publisher(publisher_id: int):
        subject = f"concurrent.{publisher_id}"
        count = 0
        errors = 0
        
        for i in range(1000):
            try:
                await client.publish(
                    subject,
                    {"publisher": publisher_id, "index": i},
                    PublishOptions(tier=Tier.MEMORY)
                )
                count += 1
            except Exception:
                errors += 1
        
        return count, errors
    
    start_time = time.time()
    
    # Run publishers concurrently
    tasks = [publisher(i) for i in range(num_publishers)]
    results = await asyncio.gather(*tasks)
    
    elapsed = time.time() - start_time
    
    # Calculate totals
    total_sent = sum(r[0] for r in results)
    total_errors = sum(r[1] for r in results)
    rate = total_sent / elapsed
    
    print(f"  Total sent: {total_sent}")
    print(f"  Total errors: {total_errors}")
    print(f"  Rate: {rate:.0f} msg/sec")
    print(f"  Time: {elapsed:.2f}s")


async def main():
    print("LAX NATS Python Client Performance Test")
    print("=" * 50)
    
    # Configure client with performance settings
    options = ClientOptions(
        nats_urls=["nats://localhost:4222"],
        broker_addr="localhost:50051",
        connection_pool_size=20,
        max_concurrent_publishes=5000,
        log_level="WARNING",  # Reduce logging overhead
        enable_metrics=False,  # Disable metrics for benchmark
    )
    
    async with LaxClient(options) as client:
        # Test each tier
        await benchmark_tier(client, Tier.MEMORY, num_messages=50000)
        
        # Note: These might fail if streams aren't configured properly
        # await benchmark_tier(client, Tier.REPLICATED, num_messages=1000)
        # await benchmark_tier(client, Tier.PERSISTENT, num_messages=1000)
        
        # Test concurrent publishers
        await concurrent_benchmark(client, num_publishers=20)
        
        print("\n✅ Performance test complete!")


if __name__ == "__main__":
    asyncio.run(main())
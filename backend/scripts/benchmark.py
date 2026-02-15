#!/usr/bin/env python3
"""Benchmark Constitutional Engine Performance"""
import asyncio
import time
from statistics import mean, stdev
from covenant.core.constitutional_engine import AdvancedConstitutionalEngine, Action

async def benchmark():
    """Run performance benchmarks"""
    engine = AdvancedConstitutionalEngine()
    
    # Test data
    actions = [
        Action(type="test", description=f"Test action {i}", actor="system")
        for i in range(1000)
    ]
    
    # Warm-up
    for action in actions[:10]:
        await engine.evaluate_action(action)
    
    # Benchmark
    latencies = []
    start_total = time.time()
    
    for action in actions:
        start = time.time()
        await engine.evaluate_action(action)
        latency = (time.time() - start) * 1000  # ms
        latencies.append(latency)
    
    total_time = time.time() - start_total
    
    # Results
    print(f"\n{'='*60}")
    print("COVENANT.AI Enterprise Benchmark Results")
    print(f"{'='*60}")
    print(f"Total Actions: {len(actions)}")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Throughput: {len(actions)/total_time:.2f} actions/sec")
    print(f"\nLatency Statistics:")
    print(f"  Mean: {mean(latencies):.2f}ms")
    print(f"  StdDev: {stdev(latencies):.2f}ms")
    print(f"  Min: {min(latencies):.2f}ms")
    print(f"  Max: {max(latencies):.2f}ms")
    print(f"  P50: {sorted(latencies)[len(latencies)//2]:.2f}ms")
    print(f"  P95: {sorted(latencies)[int(len(latencies)*0.95)]:.2f}ms")
    print(f"  P99: {sorted(latencies)[int(len(latencies)*0.99)]:.2f}ms")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    asyncio.run(benchmark())
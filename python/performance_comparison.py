"""Performance comparison between heap-based and sorting-based implementations."""

import time
import random
from median.percentile_calculator import PercentileCalculator
from median.tests.test_percentile_calculator import reference_percentile_calculator


def measure_performance(values, implementation_func, warmup=True):
    """Measure the execution time of a percentile calculation."""
    if warmup:
        # Warmup run to avoid cold start effects
        implementation_func(values.copy())
    
    start = time.perf_counter()
    result = implementation_func(values.copy())
    elapsed = time.perf_counter() - start
    return elapsed, result


def compare_implementations():
    """Compare performance of heap-based vs sorting-based implementations."""
    calc = PercentileCalculator()
    
    # Test various dataset sizes
    sizes = [100, 1_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    
    print("Performance Comparison: Heap-based vs Sorting-based")
    print("=" * 80)
    print(f"{'Size':>10} {'Heap (ms)':>12} {'Sort (ms)':>12} {'Speedup':>10} {'Status':>10}")
    print("-" * 80)
    
    for size in sizes:
        # Generate random data
        random.seed(42)
        values = [random.uniform(-1000, 1000) for _ in range(size)]
        
        # Measure heap-based implementation
        heap_time, heap_result = measure_performance(
            values, 
            lambda v: calc.calculate(v)
        )
        
        # Measure sorting-based reference implementation
        sort_time, sort_result = measure_performance(
            values,
            lambda v: reference_percentile_calculator(v)
        )
        
        # Verify results match
        p25_h, p50_h, p75_h = heap_result
        p25_s, p50_s, p75_s = sort_result
        
        match = (
            abs(p25_h - p25_s) < 0.001 and
            abs(p50_h - p50_s) < 0.001 and
            abs(p75_h - p75_s) < 0.001
        )
        
        speedup = sort_time / heap_time
        status = "✓" if match else "✗"
        
        print(f"{size:>10,} {heap_time*1000:>11.2f}  {sort_time*1000:>11.2f}  {speedup:>9.2f}x {status:>10}")
    
    print("-" * 80)
    print("\nNotes:")
    print("- Times are in milliseconds (ms)")
    print("- Speedup = Sort time / Heap time")
    print("- Status: ✓ = results match, ✗ = mismatch")
    print("\nExpected:")
    print("- For small datasets: sorting may be faster (simpler algorithm, better cache)")
    print("- For large datasets: heap should be faster (O(n) vs O(n log n))")


def test_worst_case_scenario():
    """Test performance on already sorted data (potential worst case)."""
    calc = PercentileCalculator()
    size = 100_000
    
    print("\n\nWorst Case Analysis: Pre-sorted Data")
    print("=" * 80)
    
    scenarios = [
        ("Random", lambda: [random.uniform(-1000, 1000) for _ in range(size)]),
        ("Ascending", lambda: list(range(size))),
        ("Descending", lambda: list(range(size, 0, -1))),
        ("All Same", lambda: [42.0] * size),
    ]
    
    print(f"{'Scenario':>15} {'Heap (ms)':>12} {'Sort (ms)':>12} {'Speedup':>10}")
    print("-" * 80)
    
    for scenario_name, data_generator in scenarios:
        random.seed(42)
        values = data_generator()
        
        heap_time, _ = measure_performance(values, lambda v: calc.calculate(v))
        sort_time, _ = measure_performance(values, lambda v: reference_percentile_calculator(v))
        
        speedup = sort_time / heap_time
        
        print(f"{scenario_name:>15} {heap_time*1000:>11.2f}  {sort_time*1000:>11.2f}  {speedup:>9.2f}x")
    
    print("-" * 80)


if __name__ == "__main__":
    compare_implementations()
    test_worst_case_scenario()

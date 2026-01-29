"""
Performance comparison: Median-only calculation using different approaches.

This script compares the performance of calculating ONLY the median (p50)
using two different approaches:
1. Simple sorting (O(n log n))
2. Heap-based selection (O(n + k log k) where k ≈ n/2)

Key Question: Is heap-based selection faster when we only need one percentile
instead of three?
"""

import time
import random
import heapq
import math


class MedianOnlySort:
    """Calculate median using simple sorting."""
    
    def calculate_median(self, values: list[float]) -> float:
        """Calculate median by sorting the entire list."""
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        if n == 1:
            return sorted_values[0]
        
        # Calculate median position
        position = (n - 1) * 0.50
        idx_low = int(math.floor(position))
        idx_high = int(math.ceil(position))
        weight = position - idx_low
        
        val_low = sorted_values[idx_low]
        val_high = sorted_values[idx_high]
        
        return val_low + (val_high - val_low) * weight


class MedianOnlyHeap:
    """Calculate median using heap selection."""
    
    def calculate_median(self, values: list[float]) -> float:
        """Calculate median using heapq.nsmallest."""
        n = len(values)
        
        if n == 1:
            return values[0]
        
        # Calculate median position
        position = (n - 1) * 0.50
        idx_low = int(math.floor(position))
        idx_high = int(math.ceil(position))
        weight = position - idx_low
        
        # Need to get elements up to idx_high
        # heapq.nsmallest returns smallest k elements but NOT sorted
        smallest = sorted(heapq.nsmallest(idx_high + 1, values))
        
        val_low = smallest[idx_low]
        val_high = smallest[idx_high]
        
        return val_low + (val_high - val_low) * weight


def measure_performance(values, calc_func, warmup=True):
    """Measure execution time of a function."""
    if warmup:
        calc_func(values.copy())
    
    start = time.perf_counter()
    result = calc_func(values.copy())
    elapsed = time.perf_counter() - start
    return elapsed * 1000, result  # Return milliseconds


def test_median_only():
    """Compare performance of median-only calculations."""
    sort_calc = MedianOnlySort()
    heap_calc = MedianOnlyHeap()
    
    sizes = [100, 1_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    
    print("Median-Only Performance Comparison")
    print("=" * 80)
    print(f"{'Size':>10} {'Sort (ms)':>12} {'Heap (ms)':>12} {'Heap/Sort':>12} {'Status':>10}")
    print("-" * 80)
    
    for size in sizes:
        random.seed(42)
        values = [random.uniform(-1000, 1000) for _ in range(size)]
        
        sort_time, sort_result = measure_performance(values, lambda v: sort_calc.calculate_median(v))
        heap_time, heap_result = measure_performance(values, lambda v: heap_calc.calculate_median(v))
        
        ratio = heap_time / sort_time
        match = abs(sort_result - heap_result) < 0.001
        status = "✓" if match else "✗"
        
        print(f"{size:>10,} {sort_time:>11.2f}  {heap_time:>11.2f}  {ratio:>11.2f}x {status:>10}")
    
    print("-" * 80)
    print("\nKey Findings:")
    print("- Sort: Simple O(n log n) sorting, highly optimized (Timsort)")
    print("- Heap: heapq.nsmallest for n/2 elements, then sort: O(n + k log k)")
    print("- Ratio > 1.0 = heap is slower than sorting")
    print("\nExpectation:")
    print("- For median only, heap selects ~50% of data (vs ~75% for p75)")
    print("- If heap is faster, ratio should be < 1.0")
    print("- If sorting is still faster, this confirms sorting is optimal approach")


def test_worst_case_median():
    """Test different data patterns with median-only calculation."""
    sort_calc = MedianOnlySort()
    heap_calc = MedianOnlyHeap()
    
    size = 100_000
    
    print("\n\nWorst Case Analysis: Different Data Patterns (Median Only)")
    print("=" * 80)
    print(f"{'Pattern':>15} {'Sort (ms)':>12} {'Heap (ms)':>12} {'Heap/Sort':>12}")
    print("-" * 80)
    
    scenarios = [
        ("Random", lambda: [random.uniform(-1000, 1000) for _ in range(size)]),
        ("Ascending", lambda: list(range(size))),
        ("Descending", lambda: list(range(size, 0, -1))),
        ("All Same", lambda: [42.0] * size),
        ("Nearly Sorted", lambda: sorted([random.uniform(-1000, 1000) for _ in range(size)])),
    ]
    
    for pattern, generator in scenarios:
        random.seed(42)
        values = generator()
        
        sort_time, _ = measure_performance(values, lambda v: sort_calc.calculate_median(v))
        heap_time, _ = measure_performance(values, lambda v: heap_calc.calculate_median(v))
        
        ratio = heap_time / sort_time
        
        print(f"{pattern:>15} {sort_time:>11.2f}  {heap_time:>11.2f}  {ratio:>11.2f}x")
    
    print("-" * 80)
    print("\nConclusion:")
    print("If sorting is consistently faster (ratio > 1.0), then even for median-only")
    print("calculations, the simple sorting approach is optimal due to Timsort's")
    print("highly optimized implementation in Python.")


if __name__ == "__main__":
    test_median_only()
    test_worst_case_median()

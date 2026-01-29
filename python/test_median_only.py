"""Test performance for ONLY median calculation (50th percentile)."""

import time
import random
import heapq
import math


class MedianOnlySort:
    """Calculate only median using sorting."""
    
    def calculate_median(self, values):
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        if n == 1:
            return sorted_values[0]
        
        pos = (n - 1) * 0.50
        idx_low = int(math.floor(pos))
        idx_high = int(math.ceil(pos))
        weight = pos - idx_low
        
        return sorted_values[idx_low] + (sorted_values[idx_high] - sorted_values[idx_low]) * weight


class MedianOnlyHeap:
    """Calculate only median using heapq."""
    
    def calculate_median(self, values):
        n = len(values)
        
        if n == 1:
            return values[0]
        
        pos = (n - 1) * 0.50
        idx_low = int(math.floor(pos))
        idx_high = int(math.ceil(pos))
        weight = pos - idx_low
        
        # Need to get elements at idx_low and idx_high positions
        # This requires getting the (idx_high + 1) smallest elements
        max_idx = max(idx_low, idx_high)
        smallest = sorted(heapq.nsmallest(max_idx + 1, values))
        
        return smallest[idx_low] + (smallest[idx_high] - smallest[idx_low]) * weight


class MedianOnlyQuickselect:
    """Calculate only median using iterative quickselect with 3-way partitioning."""
    
    def _partition_3way(self, arr, low, high):
        """
        3-way partitioning to handle duplicates efficiently.
        Returns (lt, gt) where:
        - Elements < pivot are in arr[low:lt]
        - Elements = pivot are in arr[lt:gt+1]
        - Elements > pivot are in arr[gt+1:high+1]
        """
        if low >= high:
            return low, high
        
        # Use median-of-three for pivot selection
        mid = (low + high) // 2
        # Sort low, mid, high
        if arr[low] > arr[mid]:
            arr[low], arr[mid] = arr[mid], arr[low]
        if arr[mid] > arr[high]:
            arr[mid], arr[high] = arr[high], arr[mid]
        if arr[low] > arr[mid]:
            arr[low], arr[mid] = arr[mid], arr[low]
        
        pivot = arr[mid]
        arr[mid], arr[high] = arr[high], arr[mid]
        
        lt = low
        gt = high
        i = low
        
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1
        
        return lt, gt
    
    def _quickselect_iterative(self, arr, k):
        """Find kth smallest element using iterative 3-way partitioning."""
        low = 0
        high = len(arr) - 1
        
        while low <= high:
            if low == high:
                return arr[low]
            
            lt, gt = self._partition_3way(arr, low, high)
            
            if k < lt:
                high = lt - 1
            elif k > gt:
                low = gt + 1
            else:
                return arr[k]
        
        return arr[k]
    
    def calculate_median(self, values):
        """Calculate median using iterative quickselect with 3-way partitioning."""
        n = len(values)
        
        if n == 1:
            return values[0]
        
        pos = (n - 1) * 0.50
        idx_low = int(math.floor(pos))
        idx_high = int(math.ceil(pos))
        
        # Get both elements we need (use separate copies for each quickselect)
        arr1 = list(values)
        val_low = self._quickselect_iterative(arr1, idx_low)
        
        arr2 = list(values)
        val_high = self._quickselect_iterative(arr2, idx_high)
        
        weight = pos - idx_low
        return val_low + (val_high - val_low) * weight


def measure_performance(values, calc_func, warmup=True):
    """Measure execution time."""
    if warmup:
        calc_func(values.copy())
    
    start = time.perf_counter()
    result = calc_func(values.copy())
    elapsed = time.perf_counter() - start
    return elapsed, result


def compare_median_only():
    """Compare performance for ONLY median calculation."""
    sort_calc = MedianOnlySort()
    heap_calc = MedianOnlyHeap()
    quickselect_calc = MedianOnlyQuickselect()
    
    sizes = [100, 1_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    
    print("Median-Only Performance Comparison")
    print("=" * 105)
    print(f"{'Size':>10} {'Sort (ms)':>12} {'Heap (ms)':>12} {'Quickselect (ms)':>17} "
          f"{'Heap/Sort':>11} {'Quick/Sort':>12}")
    print("-" * 105)
    
    for size in sizes:
        random.seed(42)
        values = [random.uniform(-1000, 1000) for _ in range(size)]
        
        # Measure sorting approach
        sort_time, sort_result = measure_performance(
            values,
            lambda v: sort_calc.calculate_median(v)
        )
        
        # Measure heap approach
        heap_time, heap_result = measure_performance(
            values,
            lambda v: heap_calc.calculate_median(v)
        )
        
        # Measure quickselect approach
        quick_time, quick_result = measure_performance(
            values,
            lambda v: quickselect_calc.calculate_median(v)
        )
        
        # Verify all match
        match = (
            abs(sort_result - heap_result) < 0.001 and
            abs(sort_result - quick_result) < 0.001
        )
        
        heap_ratio = heap_time / sort_time
        quick_ratio = quick_time / sort_time
        
        status = "✓" if match else "✗"
        
        print(f"{size:>10,} {sort_time*1000:>11.2f}  {heap_time*1000:>11.2f}  "
              f"{quick_time*1000:>16.2f}  {heap_ratio:>10.2f}x {quick_ratio:>11.2f}x {status}")
    
    print("-" * 105)
    print("\nKey Findings:")
    print("- Sort: Simple O(n log n) sorting, highly optimized (Timsort)")
    print("- Heap: heapq.nsmallest for n/2 elements, then sort: O(n + k log k)")
    print("- Quickselect: True O(n) average case selection algorithm")
    print("- Ratio > 1.0 = slower than sorting, < 1.0 = faster than sorting")
    print("\nExpectation:")
    print("- Quickselect should theoretically be fastest (O(n) vs O(n log n))")
    print("- But Python's sort is VERY optimized, so results may vary")
    print("- Heap approach still does sorting, so should be slowest")


def test_worst_case_median():
    """Test median calculation on different data patterns."""
    sort_calc = MedianOnlySort()
    heap_calc = MedianOnlyHeap()
    quickselect_calc = MedianOnlyQuickselect()
    
    size = 100_000
    
    print("\n\nWorst Case Analysis: Different Data Patterns (Median Only)")
    print("=" * 90)
    print(f"{'Pattern':>15} {'Sort (ms)':>12} {'Heap (ms)':>12} {'Quickselect (ms)':>17}")
    print("-" * 90)
    
    patterns = [
        ("Random", lambda: [random.uniform(-1000, 1000) for _ in range(size)]),
        ("Ascending", lambda: list(range(size))),
        ("Descending", lambda: list(range(size, 0, -1))),
        ("All Same", lambda: [42.0] * size),
        ("Nearly Sorted", lambda: sorted([random.uniform(-1000, 1000) for _ in range(size)])),
    ]
    
    for pattern_name, data_gen in patterns:
        random.seed(42)
        values = data_gen()
        
        sort_time, _ = measure_performance(values, lambda v: sort_calc.calculate_median(v))
        heap_time, _ = measure_performance(values, lambda v: heap_calc.calculate_median(v))
        quick_time, _ = measure_performance(values, lambda v: quickselect_calc.calculate_median(v))
        
        print(f"{pattern_name:>15} {sort_time*1000:>11.2f}  {heap_time*1000:>11.2f}  "
              f"{quick_time*1000:>16.2f}")
    
    print("-" * 90)
    print("\nNote: Quickselect can have O(n²) worst case on certain patterns")
    print("      (e.g., already sorted data with poor pivot selection)")


if __name__ == "__main__":
    compare_median_only()
    test_worst_case_median()

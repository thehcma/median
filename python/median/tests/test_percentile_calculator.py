"""Comprehensive tests for PercentileCalculator using PyHamcrest assertions."""

import math
from hamcrest import (
    assert_that,
    close_to,
    equal_to,
    calling,
    raises,
    has_length,
)
import pytest

from median.percentile_calculator import PercentileCalculator


def reference_percentile_calculator(values: list[float]) -> tuple[float, float, float]:
    """
    Reference brute-force implementation for testing.
    
    Uses simple sorting approach - O(n log n) but guaranteed correct.
    This serves as the oracle to verify the optimized heap-based implementation.
    
    Args:
        values: List of numeric values (already cleaned).
        
    Returns:
        Tuple of (p25, p50, p75).
    """
    if not values:
        raise ValueError("Cannot calculate percentiles: no valid numeric data")
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    if n == 1:
        val = sorted_values[0]
        return (val, val, val)
    
    # Calculate positions using linear interpolation
    p25_pos = (n - 1) * 0.25
    p50_pos = (n - 1) * 0.50
    p75_pos = (n - 1) * 0.75
    
    def interpolate(pos: float) -> float:
        idx_low = int(math.floor(pos))
        idx_high = int(math.ceil(pos))
        weight = pos - idx_low
        return sorted_values[idx_low] + (sorted_values[idx_high] - sorted_values[idx_low]) * weight
    
    return (interpolate(p25_pos), interpolate(p50_pos), interpolate(p75_pos))


class TestPercentileCalculator:
    """Test suite for PercentileCalculator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calc = PercentileCalculator()
    
    class TestNormalCases:
        """Test standard percentile calculations."""
        
        def setup_method(self):
            """Set up test fixtures."""
            self.calc = PercentileCalculator()
        
        def test_simple_ten_elements(self):
            """Test with a simple list of 10 elements."""
            values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_five_elements(self):
            """Test with 5 elements."""
            values = [1, 2, 3, 4, 5]
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_two_elements(self):
            """Test with only 2 elements."""
            values = [1, 5]
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_single_element(self):
            """Test with a single element."""
            values = [42]
            p25, p50, p75 = self.calc.calculate(values)
            
            assert_that(p25, equal_to(42.0))
            assert_that(p50, equal_to(42.0))
            assert_that(p75, equal_to(42.0))
        
        def test_unsorted_data(self):
            """Test that unsorted data produces correct results."""
            values = [9, 1, 5, 3, 7, 2, 8, 4, 6, 10]
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_large_dataset(self):
            """Test with a larger dataset (100 elements)."""
            values = list(range(1, 101))
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_floating_point_values(self):
            """Test with floating point values."""
            values = [1.5, 2.7, 3.2, 4.8, 5.1, 6.9, 7.3, 8.6, 9.4, 10.2]
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_negative_values(self):
            """Test with negative values."""
            values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_duplicate_values(self):
            """Test with duplicate values."""
            values = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_all_same_values(self):
            """Test with all identical values."""
            values = [7, 7, 7, 7, 7]
            p25, p50, p75 = self.calc.calculate(values)
            
            assert_that(p25, equal_to(7.0))
            assert_that(p50, equal_to(7.0))
            assert_that(p75, equal_to(7.0))
    
    class TestEdgeCases:
        """Test edge cases and error handling."""
        
        def setup_method(self):
            """Set up test fixtures."""
            self.calc = PercentileCalculator()
        
        def test_empty_list(self):
            """Test that empty list raises ValueError."""
            assert_that(
                calling(self.calc.calculate).with_args([]),
                raises(ValueError, "no valid numeric data")
            )
        
        def test_none_values_filtered(self):
            """Test that None values are filtered out."""
            values = [1, None, 2, None, 3, 4, 5]
            p25, p50, p75 = self.calc.calculate(values)
            
            # Reference implementation with cleaned values
            clean_values = [x for x in values if x is not None]
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(clean_values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_all_none_values(self):
            """Test that all None values raises ValueError."""
            assert_that(
                calling(self.calc.calculate).with_args([None, None, None]),
                raises(ValueError, "no valid numeric data")
            )
        
        def test_nan_values_filtered(self):
            """Test that NaN values are filtered out."""
            values = [1, float('nan'), 2, 3, float('nan'), 4, 5]
            p25, p50, p75 = self.calc.calculate(values)
            
            # Reference implementation with cleaned values
            clean_values = [x for x in values if not (isinstance(x, float) and math.isnan(x))]
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(clean_values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_all_nan_values(self):
            """Test that all NaN values raises ValueError."""
            assert_that(
                calling(self.calc.calculate).with_args(
                    [float('nan'), float('nan')]
                ),
                raises(ValueError, "no valid numeric data")
            )
        
        def test_mixed_none_and_nan(self):
            """Test filtering both None and NaN values."""
            values = [1, None, 2, float('nan'), 3, None, 4, float('nan'), 5]
            p25, p50, p75 = self.calc.calculate(values)
            
            # Reference implementation with cleaned values
            clean_values = [x for x in values if x is not None and not (isinstance(x, float) and math.isnan(x))]
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(clean_values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_infinity_values(self):
            """Test with infinity values."""
            values = [1, 2, 3, float('inf'), 4, 5]
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_invalid_type_string(self):
            """Test that string values raise TypeError."""
            assert_that(
                calling(self.calc.calculate).with_args([1, 2, "three", 4]),
                raises(TypeError, "must be numeric")
            )
        
        def test_invalid_type_dict(self):
            """Test that dict values raise TypeError."""
            assert_that(
                calling(self.calc.calculate).with_args([1, 2, {}, 4]),
                raises(TypeError, "must be numeric")
            )
        
        def test_non_sequence_input(self):
            """Test that non-sequence input raises TypeError."""
            assert_that(
                calling(self.calc.calculate).with_args(42),
                raises(TypeError, "Expected a sequence")
            )
    
    class TestAccuracy:
        """Test accuracy against known statistical values."""
        
        def setup_method(self):
            """Set up test fixtures."""
            self.calc = PercentileCalculator()
        
        def test_against_numpy_values(self):
            """Test accuracy against reference implementation."""
            values = list(range(1, 101))
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            # Verify against reference with very high precision
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_quartile_positions(self):
            """Test that quartile positions are correctly calculated."""
            values = [10, 20, 30, 40, 50, 60, 70, 80, 90]
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            assert_that(p25, close_to(expected_p25, 0.0001))
            assert_that(p50, close_to(expected_p50, 0.0001))
            assert_that(p75, close_to(expected_p75, 0.0001))
        
        def test_extreme_values(self):
            """Test with extreme value ranges."""
            values = [1e-10, 1e-9, 1e-8, 1e10, 1e11]
            p25, p50, p75 = self.calc.calculate(values)
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            # Use relative tolerance for extreme values
            assert_that(p25, close_to(expected_p25, abs(expected_p25 * 0.0001)))
            assert_that(p50, close_to(expected_p50, abs(expected_p50 * 0.0001)))
            assert_that(p75, close_to(expected_p75, abs(expected_p75 * 0.0001)))
    
    class TestPerformance:
        """Test performance characteristics."""
        
        def setup_method(self):
            """Set up test fixtures."""
            self.calc = PercentileCalculator()
        
        def test_randomized_validation(self):
            """
            Fuzz test: Verify correctness against reference implementation
            using randomly generated inputs.
            
            This is a form of property-based testing that helps catch edge cases
            and validates the optimized implementation matches the brute-force
            reference across diverse inputs.
            """
            import random
            
            random.seed(42)  # Deterministic random tests
            num_tests = 100
            
            for i in range(num_tests):
                # Generate random test cases with different characteristics
                if i % 4 == 0:
                    # Small datasets (1-20 elements)
                    size = random.randint(1, 20)
                    values = [random.uniform(-100, 100) for _ in range(size)]
                elif i % 4 == 1:
                    # Medium datasets (50-500 elements)
                    size = random.randint(50, 500)
                    values = [random.uniform(-1000, 1000) for _ in range(size)]
                elif i % 4 == 2:
                    # Large datasets with duplicates
                    size = random.randint(100, 1000)
                    values = [random.choice(range(1, 50)) for _ in range(size)]
                else:
                    # Extreme value ranges
                    size = random.randint(10, 100)
                    values = [random.uniform(-1e10, 1e10) for _ in range(size)]
                
                # Test the implementation against reference
                p25, p50, p75 = self.calc.calculate(values)
                expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
                
                # Use relative tolerance for large values
                max_val = max(abs(expected_p25), abs(expected_p50), abs(expected_p75), 1.0)
                tolerance = max(0.0001, max_val * 1e-9)
                
                assert_that(p25, close_to(expected_p25, tolerance),
                           f"Test {i}: p25 mismatch for size {size}")
                assert_that(p50, close_to(expected_p50, tolerance),
                           f"Test {i}: p50 mismatch for size {size}")
                assert_that(p75, close_to(expected_p75, tolerance),
                           f"Test {i}: p75 mismatch for size {size}")
        
        def test_randomized_edge_cases(self):
            """
            Fuzz test: Random edge cases like nearly-empty, all-same, etc.
            """
            import random
            
            random.seed(123)  # Different seed for different patterns
            
            test_cases = [
                # Single elements
                ([random.random()], "single element"),
                
                # Two elements
                ([random.uniform(-10, 10), random.uniform(-10, 10)], "two elements"),
                
                # All same values
                ([random.random()] * random.randint(5, 50), "all same"),
                
                # Nearly sorted
                (sorted([random.random() for _ in range(50)]), "sorted"),
                
                # Reverse sorted
                (sorted([random.random() for _ in range(50)], reverse=True), "reverse sorted"),
                
                # With negative values
                ([random.uniform(-100, 0) for _ in range(30)], "all negative"),
                
                # Mixed with zeros
                ([random.uniform(-10, 10) for _ in range(20)] + [0] * 10, "with zeros"),
                
                # Very small values
                ([random.uniform(0, 1e-10) for _ in range(20)], "very small"),
                
                # Very large values
                ([random.uniform(1e8, 1e10) for _ in range(20)], "very large"),
            ]
            
            for values, description in test_cases:
                p25, p50, p75 = self.calc.calculate(values)
                expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
                
                max_val = max(abs(expected_p25), abs(expected_p50), abs(expected_p75), 1.0)
                tolerance = max(0.0001, max_val * 1e-9)
                
                assert_that(p25, close_to(expected_p25, tolerance),
                           f"p25 mismatch for {description}")
                assert_that(p50, close_to(expected_p50, tolerance),
                           f"p50 mismatch for {description}")
                assert_that(p75, close_to(expected_p75, tolerance),
                           f"p75 mismatch for {description}")
        
        def test_large_dataset_performance(self):
            """Test performance with a large dataset (10,000 elements)."""
            import time
            
            values = list(range(10000))
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            start = time.perf_counter()
            p25, p50, p75 = self.calc.calculate(values)
            elapsed = time.perf_counter() - start
            
            # Should complete in reasonable time (< 0.1 seconds)
            assert_that(elapsed, close_to(0.0, 0.1))
            
            # Verify results match reference implementation
            assert_that(p25, close_to(expected_p25, 0.01))
            assert_that(p50, close_to(expected_p50, 0.01))
            assert_that(p75, close_to(expected_p75, 0.01))
        
        def test_very_large_dataset(self):
            """Test with 100,000 elements to verify O(n) behavior."""
            values = list(range(100000))
            expected_p25, expected_p50, expected_p75 = reference_percentile_calculator(values)
            
            # Should not raise any errors or take too long
            p25, p50, p75 = self.calc.calculate(values)
            
            assert_that(p25, close_to(expected_p25, 0.1))
            assert_that(p50, close_to(expected_p50, 0.1))
            assert_that(p75, close_to(expected_p75, 0.1))

"""Percentile calculator using heap-based algorithm for optimal performance."""

import heapq
import math
from typing import Sequence


class PercentileCalculator:
    """
    Calculate percentiles using heap-based selection algorithm.
    
    This implementation uses Python's heapq module to efficiently compute
    the 25th, 50th, and 75th percentiles. Time complexity is O(n + k log k)
    where k is the number of elements needed (typically ~75% of n).
    
    Example:
        >>> calc = PercentileCalculator()
        >>> values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> p25, p50, p75 = calc.calculate(values)
        >>> print(f"Median: {p50}")
        Median: 5.5
    """
    
    def calculate(self, values: Sequence[float | int]) -> tuple[float, float, float]:
        """
        Calculate the 25th, 50th, and 75th percentiles of the given values.
        
        Args:
            values: A sequence of numeric values.
            
        Returns:
            A tuple of (p25, p50, p75) representing the three percentiles.
            
        Raises:
            ValueError: If the values are empty or contains invalid values.
            TypeError: If the values contain non-numeric types.
            
        Note:
            - None values are filtered out
            - NaN values are filtered out
            - Uses linear interpolation for percentile calculation
        """
        # Validate and clean input
        clean_values = self._validate_and_clean(values)
        
        if not clean_values:
            raise ValueError("Cannot calculate percentiles: no valid numeric data")
        
        # Calculate percentiles efficiently
        return self._calculate_percentiles(clean_values)
    
    def _validate_and_clean(self, values: Sequence[float | int]) -> list[float]:
        """
        Validate input and filter out None and NaN values.
        
        Args:
            values: Input sequence to validate.
            
        Returns:
            List of valid numeric values.
            
        Raises:
            TypeError: If values contain non-numeric types (excluding None).
        """
        if not isinstance(values, Sequence):
            raise TypeError(f"Expected a sequence, got {type(values).__name__}")
        
        clean_values = []
        for value in values:
            if value is None:
                continue
            
            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"All values must be numeric, got {type(value).__name__}"
                )
            
            # Filter out NaN values
            if isinstance(value, float) and math.isnan(value):
                continue
            
            clean_values.append(float(value))
        
        return clean_values
    
    def _calculate_percentiles(
        self, values: list[float]
    ) -> tuple[float, float, float]:
        """
        Calculate the three percentiles using heap-based selection.
        
        This method uses heapq.nsmallest to efficiently find the elements
        at the 25th, 50th, and 75th percentile positions without fully
        sorting the values.
        
        Args:
            values: Validated list of numeric values.
            
        Returns:
            Tuple of (p25, p50, p75).
        """
        n = len(values)
        
        # Special case: single element
        if n == 1:
            val = values[0]
            return (val, val, val)
        
        # Calculate positions for each percentile (using linear interpolation)
        # Position formula: (n - 1) * percentile
        p25_pos = (n - 1) * 0.25
        p50_pos = (n - 1) * 0.50
        p75_pos = (n - 1) * 0.75
        
        # Get indices and weights for interpolation
        p25_idx_low = int(math.floor(p25_pos))
        p25_idx_high = int(math.ceil(p25_pos))
        p25_weight = p25_pos - p25_idx_low
        
        p50_idx_low = int(math.floor(p50_pos))
        p50_idx_high = int(math.ceil(p50_pos))
        p50_weight = p50_pos - p50_idx_low
        
        p75_idx_low = int(math.floor(p75_pos))
        p75_idx_high = int(math.ceil(p75_pos))
        p75_weight = p75_pos - p75_idx_low
        
        # Find all unique indices we need
        unique_indices = sorted(set([
            p25_idx_low, p25_idx_high,
            p50_idx_low, p50_idx_high,
            p75_idx_low, p75_idx_high
        ]))
        
        # Use heap to efficiently get the kth smallest elements
        # heapq.nsmallest returns k smallest elements but NOT in sorted order
        # Must sort the result to use as index lookup
        max_idx = unique_indices[-1]
        smallest_elements = sorted(heapq.nsmallest(max_idx + 1, values))
        
        # Create a mapping from index to value (for sorted order)
        index_to_value = {idx: smallest_elements[idx] for idx in unique_indices}
        
        # Interpolate to get percentile values
        p25 = self._interpolate(
            index_to_value[p25_idx_low], index_to_value[p25_idx_high], p25_weight
        )
        p50 = self._interpolate(
            index_to_value[p50_idx_low], index_to_value[p50_idx_high], p50_weight
        )
        p75 = self._interpolate(
            index_to_value[p75_idx_low], index_to_value[p75_idx_high], p75_weight
        )
        
        return (p25, p50, p75)
    
    @staticmethod
    def _interpolate(low: float, high: float, weight: float) -> float:
        """
        Perform linear interpolation between two values.
        
        Args:
            low: Lower bound value.
            high: Upper bound value.
            weight: Interpolation weight (0 to 1).
            
        Returns:
            Interpolated value.
        """
        return low + (high - low) * weight

# Python Implementation - Percentile Calculator

Python implementation of the percentile calculator using heap-based algorithms.

## Features

- **Optimal Performance**: O(n + k log k) time complexity
- **Modern Python**: Built with Python 3.12+ features
- **Type-Safe**: Comprehensive type hints throughout
- **Well-Tested**: 100% code coverage with 136 test scenarios
- **Randomized Testing**: 100+ fuzz tests validate correctness
- **Edge Case Handling**: Properly handles empty lists, None, and NaN values

## Installation

```bash
poetry install
```

## Usage

```python
from median import PercentileCalculator

# Create calculator instance
calc = PercentileCalculator()

# Calculate percentiles
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
p25, p50, p75 = calc.calculate(values)

print(f"25th percentile: {p25}")        # 3.25
print(f"50th percentile (median): {p50}")  # 5.5
print(f"75th percentile: {p75}")        # 7.75
```

### Edge Cases

```python
# Handles None and NaN values
values = [1, None, 2, float('nan'), 3, 4, 5]
p25, p50, p75 = calc.calculate(values)  # Filters to [1, 2, 3, 4, 5]

# Raises ValueError for empty/invalid input
calc.calculate([])  # ValueError: no valid numeric data
```

## Development

### Setup

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Running Tests

```bash
# Run all tests
poetry run pytest -v

# Run with coverage
poetry run pytest -v --cov=median --cov-report=term-missing

# Run only randomized tests (100+ cases)
poetry run pytest -v -k randomized

# Generate HTML coverage report
poetry run pytest --cov=median --cov-report=html
open htmlcov/index.html
```

### Test Statistics

- **27 traditional unit tests**: Normal cases, edge cases, accuracy, performance
- **100+ randomized cases**: Fuzz testing with diverse inputs
- **9 edge patterns**: Targeted randomized edge case testing
- **Total: 136 test scenarios**
- **Coverage: 100%** of implementation code
- **Execution: ~0.27 seconds**

## Implementation Details

### Algorithm

Uses Python's `heapq.nsmallest()` with post-sort for correctness:

```python
# Efficiently get k smallest elements
smallest = heapq.nsmallest(k, values)
# Sort to ensure correct ordering
sorted_smallest = sorted(smallest)
# Use for percentile interpolation
```

**Complexity**:
- Time: O(n + k log k) where k is ~75% of n for 75th percentile
- Space: O(k) for heap operations

### Key Design Decisions

1. **Nomenclature**: Uses `values` not `data`, `index_to_value` not `value_map`
2. **Linear Interpolation**: Uses `(n-1) * percentile` formula for index calculation
3. **Type Safety**: Complete type hints with modern Python 3.12+ union syntax
4. **Error Handling**: Validates input and provides clear error messages

## Testing Approach

### Reference Implementation

All tests validate against a simple brute-force reference:

```python
def reference_percentile_calculator(values):
    """Simple sorting approach - guaranteed correct."""
    sorted_values = sorted(values)
    # ... obvious, simple logic
```

### Randomized Testing

```python
def test_randomized_validation(self):
    """100+ random test cases."""
    random.seed(42)  # Deterministic
    
    for i in range(100):
        # Vary: small (1-20), medium (50-500), large (100-1000+)
        # Test: duplicates, extreme ranges, etc.
        result = calc.calculate(values)
        expected = reference(values)
        assert_that(result, close_to(expected, tolerance))
```

**This approach caught a critical bug**: The original code used `heapq.nsmallest()` without sorting, which doesn't guarantee sorted order. The dual critic review caught this, and randomized testing would have immediately exposed it.

## Project Structure

```
python/
├── pyproject.toml              # Poetry configuration
├── poetry.lock                 # Locked dependencies
├── agent_config_example.py     # Example: loading agent config
├── TESTING_CHECKLIST.md        # Testing agent checklist
├── TESTING_QUICK_REF.md        # Testing quick reference
└── median/
    ├── __init__.py
    ├── percentile_calculator.py  # Implementation
    └── tests/
        ├── __init__.py
        └── test_percentile_calculator.py  # Comprehensive tests
```

## Dependencies

### Runtime
- Python 3.12+

### Development
- pytest 8.0+
- pyhamcrest 2.1+
- pytest-cov 4.1+

## Documentation

- [TESTING_CHECKLIST.md](./TESTING_CHECKLIST.md) - Complete testing checklist
- [TESTING_QUICK_REF.md](./TESTING_QUICK_REF.md) - Quick testing reference
- [agent_config_example.py](./agent_config_example.py) - Example configuration usage

## Contributing

When making changes:

1. **Follow the Testing Agent checklist** (TESTING_CHECKLIST.md)
2. **Always create reference implementation** for validation
3. **Include randomized tests** (100+ cases minimum)
4. **Achieve 100% coverage**
5. **Use descriptive naming** (see AGENTS.md for conventions)

## Version History

| Version | Date       | Changes                                    |
|---------|------------|--------------------------------------------|
| 0.1.0   | 2026-01-29 | Initial implementation with agent workflow |

## License

MIT

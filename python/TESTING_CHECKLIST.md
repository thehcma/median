# Testing Agent Checklist

## MANDATORY: Complete this checklist for every implementation

This checklist ensures consistent, high-quality testing across all changes.

---

## 1. Reference Implementation ✓

**Status**: [ ] Complete [ ] Not Applicable

**Requirements**:
- [ ] Create simple, brute-force reference implementation
- [ ] Must be obviously correct (use sorting, not optimization)
- [ ] Place at top of test file
- [ ] Document that it's an oracle for testing
- [ ] Function signature matches main implementation

**Example**:
```python
def reference_implementation(values: list[float]) -> ...:
    """
    Reference brute-force implementation for testing.
    Uses simple sorting approach - guaranteed correct.
    """
    sorted_values = sorted(values)
    # ... simple, obvious logic
```

---

## 2. Traditional Unit Tests ✓

**Status**: [ ] Complete

**Requirements**:
- [ ] Normal cases: various input sizes (1, 2, 5, 10, 100, 1000)
- [ ] Edge cases: empty, None, NaN, single element, all same
- [ ] Error cases: invalid types, non-sequence inputs
- [ ] All tests use reference implementation for expected values
- [ ] NO hardcoded expected values (use reference instead)
- [ ] Use PyHamcrest assertions

**Test Classes**:
```python
class TestImplementation:
    class TestNormalCases:
        # 8-10 tests for typical scenarios
        
    class TestEdgeCases:
        # 5-8 tests for boundary conditions
        
    class TestAccuracy:
        # 2-3 tests validating against reference
```

---

## 3. Randomized Testing ✓ **MANDATORY**

**Status**: [ ] Complete

**Requirements**:
- [ ] test_randomized_validation implemented
- [ ] Minimum 100 random test cases
- [ ] Fixed random seed (e.g., random.seed(42))
- [ ] Test small (1-20), medium (50-500), large (100-1000+) inputs
- [ ] All results validated against reference implementation
- [ ] Adaptive tolerance for floating-point precision

**Template**:
```python
def test_randomized_validation(self):
    """Fuzz test: Verify correctness against reference."""
    import random
    random.seed(42)
    
    for i in range(100):
        # Vary: small, medium, large, extreme ranges
        size = random.randint(...)
        values = [random.uniform(...) for _ in range(size)]
        
        result = implementation.calculate(values)
        expected = reference_implementation(values)
        
        assert_that(result, close_to(expected, tolerance))
```

---

## 4. Randomized Edge Cases ✓ **MANDATORY**

**Status**: [ ] Complete

**Requirements**:
- [ ] test_randomized_edge_cases implemented
- [ ] Test specific patterns: single, two elements, all same, sorted, etc.
- [ ] Use randomness for values but fixed patterns
- [ ] All validated against reference

**Patterns to Test**:
- [ ] Single element
- [ ] Two elements
- [ ] All same values
- [ ] Sorted data
- [ ] Reverse sorted
- [ ] All negative
- [ ] Mixed with zeros
- [ ] Very small values (near zero)
- [ ] Very large values

---

## 5. Performance Tests ✓

**Status**: [ ] Complete

**Requirements**:
- [ ] Benchmark with large dataset (10,000+ elements)
- [ ] Verify results still correct (use reference)
- [ ] Optional: Compare timing against reference
- [ ] Document expected time complexity

---

## 6. Coverage ✓

**Status**: [ ] Complete

**Requirements**:
- [ ] Run pytest with coverage: `pytest --cov`
- [ ] Achieve 100% code coverage
- [ ] All branches tested
- [ ] All error paths tested

---

## 7. Documentation ✓

**Status**: [ ] Complete

**Requirements**:
- [ ] All test methods have docstrings
- [ ] Docstrings explain what is being tested
- [ ] Complex tests include comments
- [ ] Test organization is clear

---

## Validation Commands

Run these commands to verify checklist completion:

```bash
# Run all tests
poetry run pytest -v

# Run with coverage
poetry run pytest -v --cov=median --cov-report=term-missing

# Run only randomized tests
poetry run pytest -v -k randomized

# Count randomized test cases
# Should see 100+ in test_randomized_validation output
```

---

## Quality Gates

**All must pass before code is considered complete:**

- [x] Reference implementation exists and is simple
- [x] All traditional unit tests pass
- [x] test_randomized_validation exists and runs 100+ cases
- [x] test_randomized_edge_cases exists and covers patterns
- [x] 100% code coverage achieved
- [x] No hardcoded expected values (all use reference)
- [x] All tests use PyHamcrest assertions
- [x] Performance tests validate correctness

---

## Example Complete Test File Structure

```python
"""Tests for implementation."""

import random
import math
from hamcrest import assert_that, close_to, raises
import pytest

from module import Implementation


def reference_implementation(values):
    """Reference brute-force implementation."""
    # Simple, obviously correct logic
    pass


class TestImplementation:
    """Test suite for Implementation."""
    
    def setup_method(self):
        self.impl = Implementation()
    
    class TestNormalCases:
        """Test standard functionality."""
        
        def setup_method(self):
            self.impl = Implementation()
        
        def test_small_input(self):
            values = [1, 2, 3, 4, 5]
            result = self.impl.calculate(values)
            expected = reference_implementation(values)
            assert_that(result, close_to(expected, 0.0001))
        
        # ... 7-9 more normal case tests
    
    class TestEdgeCases:
        """Test boundary conditions."""
        
        def setup_method(self):
            self.impl = Implementation()
        
        def test_empty_list(self):
            assert_that(
                calling(self.impl.calculate).with_args([]),
                raises(ValueError)
            )
        
        # ... 4-7 more edge case tests
    
    class TestAccuracy:
        """Validate against reference."""
        
        def setup_method(self):
            self.impl = Implementation()
        
        def test_matches_reference(self):
            values = list(range(1, 101))
            result = self.impl.calculate(values)
            expected = reference_implementation(values)
            assert_that(result, close_to(expected, 0.0001))
    
    class TestPerformance:
        """Test performance and randomized validation."""
        
        def setup_method(self):
            self.impl = Implementation()
        
        def test_randomized_validation(self):
            """MANDATORY: Fuzz test with 100+ cases."""
            random.seed(42)
            
            for i in range(100):
                # Generate varied inputs
                # Test against reference
                pass
        
        def test_randomized_edge_cases(self):
            """MANDATORY: Fuzz test edge case patterns."""
            random.seed(123)
            
            test_cases = [
                ([random.random()], "single"),
                # ... more patterns
            ]
            
            for values, desc in test_cases:
                # Test against reference
                pass
        
        def test_large_dataset(self):
            """Performance with large input."""
            values = list(range(10000))
            result = self.impl.calculate(values)
            expected = reference_implementation(values)
            assert_that(result, close_to(expected, 0.1))
```

---

## Notes for Testing Agent

When invoked to create tests:

1. **ALWAYS** start by creating reference implementation
2. **ALWAYS** include both randomized test methods
3. **NEVER** use hardcoded expected values
4. **ALWAYS** validate against reference
5. **ALWAYS** use fixed random seeds
6. **ALWAYS** test diverse input characteristics
7. **ALWAYS** use adaptive tolerance for floating-point

This approach caught the heapq.nsmallest bug immediately and will catch future bugs!

---

## Version History

| Date       | Change                                    |
|------------|-------------------------------------------|
| 2026-01-29 | Initial checklist created                 |
| 2026-01-29 | Made randomized testing mandatory         |

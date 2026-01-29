# Testing Agent Quick Reference

## When I am invoked to write tests, I MUST:

### 1️⃣ Create Reference Implementation (Oracle)
```python
def reference_implementation(values):
    """Simple brute-force - guaranteed correct."""
    sorted_values = sorted(values)
    # ... obvious, simple logic
```

### 2️⃣ Write Traditional Unit Tests
- Use reference for expected values (NO hardcoded)
- Test normal, edge, and error cases
- Use PyHamcrest assertions

### 3️⃣ Write Randomized Tests (MANDATORY)
```python
def test_randomized_validation(self):
    """100+ random cases validated against reference."""
    import random
    random.seed(42)
    
    for i in range(100):
        # Vary: small, medium, large, extreme
        values = generate_random_values()
        result = implementation(values)
        expected = reference_implementation(values)
        assert_that(result, close_to(expected, tolerance))

def test_randomized_edge_cases(self):
    """Edge case patterns with random values."""
    random.seed(123)
    test_cases = [
        ([random.random()], "single"),
        ([random.random()] * 10, "all same"),
        # ... 7-9 more patterns
    ]
    for values, desc in test_cases:
        # validate against reference
```

### 4️⃣ Achieve 100% Coverage
```bash
pytest --cov=module --cov-report=term-missing
```

## Key Principles

✅ **DO**:
- Reference implementation = source of truth
- Fixed random seeds (reproducible)
- Adaptive tolerance for floating-point
- 100+ random test cases minimum
- Descriptive test names and docstrings

❌ **DON'T**:
- Hardcode expected values
- Skip randomized tests
- Use unbounded randomness (fix seed!)
- Ignore edge cases
- Accept < 100% coverage

## Files to Reference

- **TESTING_CHECKLIST.md** - Complete checklist to follow
- **AGENTS.md** - My full responsibilities
- **.agent-models.json** - My mandatory practices
- **RANDOMIZED_TESTING.md** - Detailed explanation

## Template Location

See `python/median/tests/test_percentile_calculator.py` for complete example.

---

**Remember**: Randomized testing caught the heapq bug! It's not optional.

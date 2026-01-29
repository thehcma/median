# Agent Definitions

This document defines the four specialized agents for the percentile calculator project.

**Configuration**: See [AGENT_MODELS.md](./AGENT_MODELS.md) for model assignments and `.agent-models.json` for machine-readable configuration.

## Workflow Requirements

**CRITICAL**: Before creating any pull request, the following workflow MUST be completed:

1. **Implementation Agent** completes the code changes
2. **Primary Critique Agent (Claude)** reviews the implementation
3. **Secondary Critique Agent (GPT-5)** provides independent review
4. **Testing Agent** ensures comprehensive test coverage
5. **Final verification**: All agents confirm VS Code Problems panel is clear

**Only after all review agents have completed their analysis and approved the changes** should a pull request be created. This ensures code quality, correctness, and adherence to project standards before submission.

## Agent 1: Implementation Agent

**Model**: `claude-sonnet-4.5` (see AGENT_MODELS.md)

**Role**: Core developer focused on creating efficient, maintainable code.

**Responsibilities**:
- Design and implement the PercentileCalculator class with heap-based algorithm
- Use modern Python features (3.12+) including type hints and dataclasses where appropriate
- Implement efficient algorithms prioritizing O(n) complexity over O(n log n)
- Handle edge cases gracefully (empty lists, None, NaN values)
- Write clear, self-documenting code with comprehensive docstrings
- Follow PEP 8 style guidelines

**Approach**:
- Use Python's `heapq` module for efficient kth element selection
- Implement single-pass algorithm for multiple percentiles
- Validate input and raise informative exceptions
- Use type hints for all public APIs

## Agent 2: Critique Agent (Claude)

**Model**: `claude-sonnet-4.5` (see AGENT_MODELS.md)

**Role**: Code reviewer ensuring correctness, performance, and quality.

**Responsibilities**:
- Review implementation for algorithmic correctness
- Verify heap-based optimization is properly implemented
- Check edge case handling completeness
- Validate type hints and documentation quality
- Ensure PEP 8 compliance
- Identify potential bugs or performance issues
- Suggest improvements for readability and maintainability
- Enforce consistent nomenclature and naming conventions

**Nomenclature Guidelines**:
- Use `values` instead of `data` for collections of numeric inputs
- Use descriptive names for mappings that show key→value relationship:
  - ✅ `index_to_value` (clear: index maps to value)
  - ✅ `user_id_to_name` (clear: user ID maps to name)
  - ❌ `value_map` (unclear: what's the key? what's the value?)
  - ❌ `data_dict` (unclear: what maps to what?)
- Variable names should be self-documenting
- Avoid generic suffixes like `_map`, `_dict` when more specific names are available

**Review Checklist**:
- [ ] Algorithm correctness verified
- [ ] Time complexity is optimal (O(n) average case)
- [ ] Space complexity is reasonable
- [ ] All edge cases properly handled
- [ ] Type hints complete and accurate
- [ ] Docstrings clear and comprehensive
- [ ] No security vulnerabilities
- [ ] Error messages are informative
- [ ] Naming conventions followed (values, descriptive mappings)
- [ ] **VS Code Problems panel is clear** (no import errors, type errors, or linting issues)

## Agent 2b: Secondary Critique Agent (GPT-5)

**Model**: `gpt-5.1-codex-max` (see AGENT_MODELS.md)

**Role**: Secondary code reviewer providing alternative perspective.

**Responsibilities**:
- Provide independent review from different model perspective
- Look for issues the first critic may have missed
- Focus on practical engineering concerns
- Validate API design and usability
- Check for common anti-patterns
- Assess test coverage completeness
- Suggest alternative approaches when beneficial

**Review Focus**:
- Different reasoning approach may catch different issues
- Cross-validation of the primary critic's findings
- Real-world usability and developer experience
- Code maintainability over time
- Edge cases from a different angle
- **Verify VS Code Problems panel is clear** (use `get_errors()` tool)

**When to Use**:
- After primary critic review
- For complex algorithmic decisions
- When you want a second opinion
- To validate critical sections of code

## Agent 3: Testing Agent

**Model**: `claude-sonnet-4.5` (see AGENT_MODELS.md)

**Role**: Quality assurance through comprehensive testing.

**Responsibilities**:
- Write unit tests using pytest framework
- Use PyHamcrest matchers for expressive assertions
- Cover all normal use cases with various input sizes
- Test all edge cases (empty, None, NaN, single element, etc.)
- Verify percentile calculation accuracy against known values
- Write performance benchmarks
- Achieve 100% code coverage
- Document test scenarios clearly
- **ALWAYS implement randomized/fuzz testing** to validate correctness

**Mandatory Testing Approach**:
1. **Traditional Unit Tests**: Cover known scenarios and edge cases
2. **Reference Implementation**: Create simple brute-force version as oracle
3. **Randomized Testing**: REQUIRED for every implementation
   - Generate 100+ random test cases with diverse characteristics
   - Validate optimized implementation against reference
   - Use fixed random seed for reproducibility
   - Test small (1-20), medium (50-500), and large (100-1000+) inputs
   - Include edge cases: duplicates, sorted, reverse sorted, extreme values
   - Use adaptive tolerance for floating-point comparisons

**Testing Strategy**:
- Normal cases: lists of varying sizes (1, 2, 5, 10, 100, 1000 elements)
- Edge cases: empty list, None values, NaN values, single element
- Accuracy tests: verify against reference implementation (NOT hardcoded values)
- Randomized tests: 100+ random inputs validated against reference
- Performance tests: benchmark against large datasets
- Use PyHamcrest matchers: `assert_that()`, `equal_to()`, `close_to()`, `raises()`

**Randomized Testing Template**:
```python
def test_randomized_validation(self):
    """
    Fuzz test: Verify correctness against reference implementation
    using randomly generated inputs.
    """
    import random
    random.seed(42)  # Deterministic
    
    for i in range(100):
        # Generate varied inputs (small, medium, large, extreme ranges)
        # Test against reference implementation
        # Use adaptive tolerance for numerical precision
        assert_that(result, close_to(expected, tolerance))
```

**Test Organization**:
```python
class TestImplementation:
    class TestNormalCases:
        # Standard functionality tests
        
    class TestEdgeCases:
        # Empty, None, NaN, single element
        
    class TestAccuracy:
        # Verify against reference implementation
        
    class TestPerformance:
        # Benchmark large datasets
        # MUST INCLUDE: test_randomized_validation
        # MUST INCLUDE: test_randomized_edge_cases
```

**Quality Gates**:
- [ ] All traditional unit tests pass
- [ ] 100% code coverage achieved
- [ ] Randomized tests pass (100+ cases)
- [ ] Reference implementation validates correctness
- [ ] Performance benchmarks meet requirements
- [ ] No hardcoded expected values (use reference instead)
- [ ] **VS Code Problems panel is clear** (no errors in test files)

# Median - Percentile Calculator

An optimal percentile calculator implementation using heap-based algorithms for efficient computation of the 25th, 50th, and 75th percentiles.

## Repository Structure

This is a **multi-language repository** designed to support implementations in different programming languages:

```
median/
├── .agent-models.json       # Agent model configuration (shared)
├── AGENTS.md                # Agent definitions (shared)
├── AGENT_MODELS.md          # Model assignments (shared)
├── README.md                # This file
└── python/                  # Python implementation
    ├── pyproject.toml
    ├── poetry.lock
    ├── median/              # Python package
    └── TESTING_*.md         # Python testing docs
```

### Current Implementations

- **Python** (`python/`) - Complete with heap-based algorithm
- **Rust** - Coming soon
- **Go** - Coming soon

See language-specific README in each directory for implementation details.

## Features

- **Optimal Performance**: O(n + k log k) time complexity using heap-based selection
- **Modern Language Features**: Type-safe, idiomatic implementations
- **Well-Tested**: 100% code coverage with randomized fuzz testing
- **Edge Case Handling**: Properly handles empty lists, None/null, and NaN values
- **Multi-Agent Development**: Built using specialized AI agents with documented models

## Agent-Driven Development

This project was built using a four-agent workflow with deterministic model assignments:
- **Implementation Agent** (`claude-sonnet-4.5`): Core development
- **Primary Critic** (`claude-sonnet-4.5`): Code review and conventions
- **Secondary Critic** (`gpt-5.1-codex-max`): Alternative perspective
- **Testing Agent** (`claude-sonnet-4.5`): Comprehensive test coverage with mandatory randomized testing

See [AGENTS.md](./AGENTS.md) for agent definitions and [AGENT_MODELS.md](./AGENT_MODELS.md) for model configuration.

## Quick Start

### Python

```bash
cd python
poetry install
poetry run pytest -v
```

See [python/README.md](./python/README.md) for detailed Python documentation.

## Algorithm

This implementation uses a heap-based approach via `heapq` module for efficient percentile calculation:

- **Time Complexity**: O(n + k log k) where k is the number of elements needed
- **Space Complexity**: O(k) for the heap operations
- **Advantages**: Efficient for computing multiple percentiles in one pass

## Development Guidelines

### For New Language Implementations:

1. **Follow the agent workflow**:
   - Implementation Agent: Write the core algorithm
   - Critique Agents: Review for correctness and best practices
   - Testing Agent: Comprehensive tests including randomized validation

2. **Mandatory testing approach**:
   - Create reference brute-force implementation as oracle
   - Implement 100+ randomized test cases
   - Validate against reference, not hardcoded values
   - See [AGENTS.md](./AGENTS.md) for details

3. **Directory structure**:
   ```
   <language>/
   ├── README.md              # Language-specific docs
   ├── build files            # Language-specific config
   ├── src/ or <package>/     # Source code
   └── tests/                 # Test suite
   ```

## Testing Philosophy

All implementations use **property-based testing** with randomized inputs:
- 100+ random test cases with diverse characteristics
- Validation against reference implementation
- Fixed random seeds for reproducibility
- Catches bugs traditional tests miss (e.g., the heapq.nsmallest ordering bug)

## License

MIT

## Contributing

When adding a new language implementation:
1. Create a new directory for the language
2. Follow the agent workflow documented in AGENTS.md
3. Include comprehensive testing with randomized validation
4. Update this README with the new implementation

# Development Workflow Guide

This guide covers the day-to-day development workflow for contributing to Vajra, from making changes to submitting pull requests.

## Development Environment Setup

### Initial Setup

Refer to [quick start](../quickstart.md) for project setup process.

## Making Changes

### Python Development

For Python-only changes, no build step is required:

```bash
# Edit Python files
vim vajra/config/model_config.py

# Test immediately
python -m pytest test/unit/test_config.py -v

# Format code
make format/black format/isort
```

### C++ Development

C++ changes require compilation:

```bash
# Edit C++ files
vim csrc/vajra/native/scheduler.cpp

# Incremental build (fast)
make build/native # if new files or dependencies are added
make build/native_incremental # if only existing files where changed

# Test your changes
python examples/offline_inference.py

# Run relevant tests
make test/ctest  # C++ tests
make test/unit   # Full unit test suite
```

### Mixed Python/C++ Development

When working on features that span both languages:

```bash
# Make your changes
vim csrc/vajra/native/inference_engine.cpp
vim vajra/engine/inference_engine.py

# Build and test
make build/native_incremental
python test_your_feature.py

# Run comprehensive tests
make test/unit test/integration
```

## Code Quality Workflow

### Formatting

Vajra uses automated formatting. **Always format before committing:**

```bash
# Format all code (Python + C++)
make format

# Format specific languages
make format/black    # Python formatting
make format/clang    # C++ formatting
make format/isort    # Python import sorting
```

### Linting

Run linters to catch issues early:

```bash
# Check all code quality
make lint

# Specific linters
make lint/pyright    # Python type checking
make lint/cpplint    # C++ style checking
make lint/black      # Python format checking
make lint/codespell  # Spelling checks
```

## Testing Strategy

### Test Categories

| Type | Command | Purpose | Speed |
|------|---------|---------|-------|
| Unit | `make test/unit` | Fast, isolated tests | ~30s |
| Integration | `make test/integration` | Feature-level tests | ~2-5min |
| Performance | `make test/performance` | Benchmark tests | ~5-15min |
| Functional | `make test/functional` | End-to-end tests | ~10-30min |

### Testing Workflow

#### During Development
```bash
# Quick feedback loop
make test/unit

# Test specific modules
python -m pytest test/unit/test_scheduler.py -v

# Test with coverage
python -m pytest --cov=vajra --cov-report=html test/unit/
```

#### Before Committing
```bash
# Comprehensive testing
make test/unit test/integration

# Full test suite (takes longer)
make test
```

#### Performance Testing
```bash
# Run performance benchmarks
make test/performance

# Custom performance tests
python -m vajra.benchmark.main
```

### Test Reports

All tests generate detailed reports:

```bash
# Run tests with reports
make test/unit  # Creates test_reports/pytest-unit-results.xml

# View coverage reports
open test_reports/python_coverage_html/index.html
```

## Build System Deep Dive


### Build Customization

Control builds with environment variables:

```bash
# Debug vs Release builds
BUILD_TYPE=Debug make build/native      # Default, includes debug symbols
BUILD_TYPE=Release make build/native    # Optimized for performance

# Parallel build jobs
CMAKE_BUILD_PARALLEL_LEVEL=8 make build/native
```

### Incremental Development

For fast development cycles:

```bash
# First build (slow)
make build

# Subsequent builds (fast)
make build/native_incremental
```

### Build Logs

All builds generate detailed logs:

```bash
# Build logs are saved with timestamps
ls logs/
# cmake_configure_20241201_143022.log
# cmake_build_native_20241201_143055.log

# View the latest build log
ls -t logs/cmake_build_* | head -1 | xargs cat
```

## Docker Development

### Using the Development Container

Build and run the development container:

```bash
cd docker/containers/dev

# Build container
make build USERNAME=$USER

# Run interactive session
make run USERNAME=$USER

# Or start persistent container
make start USERNAME=$USER
make attach USERNAME=$USER
```

### Container Development Workflow

Inside the container:

```bash
# Repository is mounted at /repo
cd /repo

# All development commands work the same
make build
make test/unit
make format
```

### Container Benefits

- **Consistent Environment**: Same CUDA/PyTorch versions as CI
- **Pre-installed Tools**: All development tools ready
- **Isolation**: Doesn't affect host system
- **GPU Access**: Full CUDA support
- **Productivity Tools**: ZSH, Oh My Zsh, FZF for better CLI experience

## Git Workflow

### Branch Management

```bash
# Create feature branch
git checkout -b users/your-name/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add your feature description"

# Keep up to date with main
git fetch origin
git rebase origin/main

# Push your branch
git push origin users/your-name/your-feature-name
```

### Pull Request Naming

Follow conventional commit/pull request naming format:

```bash
# Format: type(scope): description
git commit -m "feat(scheduler): add priority-based scheduling"
git commit -m "fix(memory): resolve memory leak in cache manager"
git commit -m "docs(setup): update installation instructions"
git commit -m "test(integration): add end-to-end pipeline test"
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `style`, `chore`

## Best Practices Summary

### Daily Development

1. **Start Clean**: `make format && make lint`
2. **Incremental**: Use `make build/native` and `make build/native_incremental` for C++ changes
3. **Test Early**: Run relevant tests after each change
4. **Format Before Commit**: Always run `make format`

### Code Quality

1. **Follow Style Guides**: Use the provided style guides
2. **Write Tests**: Add tests for new functionality
3. **Document Changes**: Update docs for user-facing changes
4. **Use Type Hints**: Comprehensive type annotations

### Performance

1. **Profile First**: Measure before optimizing
2. **Test Performance**: Run benchmarks for performance changes
3. **Consider Memory**: GPU memory is often the bottleneck
4. **Batch Operations**: Process multiple items together

### Collaboration

1. **Small PRs**: Keep changes focused and reviewable
2. **Clear Commits**: Use conventional commit messages
3. **Document Decisions**: Explain why, not just what
4. **Ask Questions**: Use GitHub Discussions for help

This development workflow ensures high code quality, fast iteration, and smooth collaboration across the Vajra project.
# Hypermindz Tools

A comprehensive toolkit for AI agents and automation workflows, featuring CrewAI integrations and advanced search capabilities.

## Features

- 🤖 **CrewAI Integration**: Advanced tools for AI agent workflows
- 🔍 **RAG Search**: Retrieval-Augmented Generation search capabilities
- 🛠️ **Developer Tools**: Complete development environment with code quality enforcement
- 📊 **Testing**: Comprehensive test suite with coverage reporting
- 🚀 **CI/CD**: Automated testing, building, and deployment

## Quick Start

### Installation

```bash
# Install the package
pip install hypermindz-tools

# For development
git clone https://github.com/yourusername/hypermindz-tools.git
cd hypermindz-tools
make setup-dev
```

### Basic Usage

```python
from hypermindz_tools.crewai import rag_search

# Example usage
result = rag_search.search("your query here")
print(result)
```

## Development Setup

### Prerequisites

- Python 3.10, 3.11, or 3.12
- Git
- Make (optional but recommended)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/hypermindz-tools.git
cd hypermindz-tools

# Complete development setup (installs dependencies + pre-commit hooks)
make setup-dev

# Verify setup
make info
```

### Manual Setup (if you don't have make)

```bash
# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Verify setup
pre-commit run --all-files
```

## Development Workflow

### Daily Development Commands

```bash
# Fix all formatting issues and run checks
make fix-all

# Quick development cycle (format → lint → type-check → test)
make dev-cycle

# Run tests only
make test

# Format code only
make format
```

### Code Quality

This project enforces high code quality standards through:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting and style checking
- **mypy**: Type checking
- **bandit**: Security scanning
- **pytest**: Testing with coverage

### Pre-commit Hooks

Pre-commit hooks run automatically before each commit to ensure code quality:

```bash
# Hooks run automatically on git commit
git add .
git commit -m "Your changes"  # Hooks run here automatically

# Run hooks manually
make pre-commit-run

# Update hook versions
make pre-commit-update
```

If pre-commit hooks fail:
1. Issues are automatically fixed when possible (formatting)
2. Manual fixes required for linting/type errors
3. Run `make fix-all` to resolve most issues
4. Commit again

### Available Make Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install the package |
| `make install-dev` | Install in development mode |
| `make setup-dev` | Complete development environment setup |
| `make test` | Run tests with coverage |
| `make test-verbose` | Run tests with HTML coverage report |
| `make lint` | Run linting checks |
| `make format` | Format code with black and isort |
| `make type-check` | Run mypy type checking |
| `make security` | Run security checks with bandit |
| `make check-all` | Run all quality checks |
| `make fix-all` | Auto-fix formatting and run all checks |
| `make dev-cycle` | Quick development cycle |
| `make ci-check` | Simulate CI checks |
| `make clean` | Clean build artifacts |
| `make build` | Build distribution packages |
| `make upload` | Upload to PyPI |
| `make upload-test` | Upload to Test PyPI |
| `make pre-commit-install` | Install pre-commit hooks |
| `make pre-commit-run` | Run pre-commit on all files |
| `make info` | Display project information |

### Testing

```bash
# Run tests with coverage
make test

# Run tests with detailed HTML coverage report
make test-verbose

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Building and Publishing

```bash
# Build distribution packages
make build

# Upload to Test PyPI (for testing)
make upload-test

# Upload to PyPI (production)
make upload
```

## Project Structure

```
hypermindz-tools/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline
├── .pre-commit-config.yaml     # Pre-commit configuration
├── hypermindz_tools/
│   ├── __init__.py
│   └── crewai/
│       ├── __init__.py
│       └── rag_search.py       # RAG search implementation
├── tests/
│   └── test_crewai/
│       └── test_rag_search.py  # Test files
├── Makefile                    # Development commands
├── pyproject.toml             # Project configuration
├── README.md                  # This file
└── requirements-dev.txt       # Development dependencies
```

## Code Quality Standards

### Formatting
- **Line length**: 127 characters
- **Code style**: Black formatter
- **Import sorting**: isort with Black profile

### Linting
- **Complexity**: Maximum 10
- **Type hints**: Required for public APIs
- **Docstrings**: Required for public functions

### Testing
- **Minimum coverage**: 80%
- **Test location**: `tests/` directory
- **Naming**: `test_*.py` files

## CI/CD Pipeline

The project uses GitHub Actions for:

- ✅ **Multi-version testing**: Python 3.10, 3.11, 3.12
- ✅ **Code quality checks**: Linting, formatting, type checking
- ✅ **Security scanning**: Bandit security checks
- ✅ **Test coverage**: Pytest with coverage reporting
- ✅ **Automated building**: Distribution packages
- ✅ **Automated publishing**: PyPI releases on tags

### CI Pipeline Triggers

- **Push**: `main` and `dev` branches
- **Pull Request**: `main` branch
- **Release**: Git tags starting with `v*`

## Contributing

### Development Process

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/hypermindz-tools.git`
3. **Setup** development environment: `make setup-dev`
4. **Create** a feature branch: `git checkout -b feature/amazing-feature`
5. **Develop** your feature
6. **Test** your changes: `make fix-all`
7. **Commit** your changes (pre-commit hooks will run)
8. **Push** to your fork: `git push origin feature/amazing-feature`
9. **Create** a Pull Request

### Code Style Guidelines

- Follow PEP 8 (enforced by flake8)
- Use type hints for function signatures
- Write docstrings for public functions
- Keep functions focused and small
- Write tests for new functionality

### Pull Request Process

1. Ensure all tests pass: `make check-all`
2. Update documentation if needed
3. Add tests for new functionality
4. Ensure CI pipeline passes
5. Request review from maintainers

## Troubleshooting

### Common Issues

**Pre-commit hooks fail**:
```bash
make fix-all  # Auto-fix most issues
```

**Import errors in tests**:
```bash
pip install -e .[dev]  # Reinstall in development mode
```

**Coverage too low**:
```bash
make test-verbose  # See detailed coverage report
```

**Type checking errors**:
```bash
make type-check  # Run mypy separately
```

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/hypermindz-tools/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/hypermindz-tools/discussions)
- **Documentation**: [Project Wiki](https://github.com/yourusername/hypermindz-tools/wiki)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

## Acknowledgments

- CrewAI team for the amazing framework
- Contributors and maintainers
- Open source community

---

**Made with ❤️ by the Hypermindz team**

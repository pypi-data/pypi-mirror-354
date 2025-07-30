# Contributing to Refinire-RAG Docling Plugin

Thank you for your interest in contributing to the Refinire-RAG Docling Plugin! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows a Code of Conduct to ensure a welcoming environment for all contributors. By participating, you agree to uphold this code.

### Our Standards

- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- uv (recommended) or pip
- Basic understanding of RAG systems and document processing

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/refinire-rag-docling.git
cd refinire-rag-docling
```

## Development Setup

### Environment Setup

```bash
# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv add --dev pytest pytest-cov

# Install package in editable mode
uv pip install -e .

# Verify setup
pytest tests/ -v
```

### Project Structure

```
refinire-rag-docling/
├── src/
│   └── refinire_rag_docling/
│       ├── __init__.py
│       ├── loader.py          # Main loader class
│       ├── models.py          # Data models
│       └── services.py        # Processing services
├── tests/
│   ├── unit/                  # Unit tests
│   └── e2e/                   # Integration tests
├── docs/                      # Documentation
├── examples/                  # Usage examples
└── pyproject.toml            # Project configuration
```

## Contributing Process

### 1. Create an Issue

Before starting work, create an issue to discuss:
- Bug reports
- Feature requests
- Documentation improvements
- Performance enhancements

### 2. Create a Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### Branch Naming Convention

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `test/description` - Test improvements
- `refactor/description` - Code refactoring

### 3. Make Changes

Follow the code standards and guidelines outlined below.

### 4. Test Your Changes

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Test specific modules
pytest tests/unit/test_your_module.py -v
```

### 5. Commit Changes

```bash
# Add changes
git add .

# Commit with descriptive message
git commit -m "feat: add support for new document format"
```

#### Commit Message Convention

Follow the conventional commits format:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `style:` - Code formatting
- `perf:` - Performance improvements

Examples:
```
feat: add XLSX support with table extraction
fix: handle empty PDF documents gracefully
docs: update API reference for new methods
test: add integration tests for batch processing
```

## Code Standards

### Python Style

- Follow PEP 8 style guidelines
- Use type hints for all functions and methods
- Maximum line length: 88 characters (Black formatter)
- Use descriptive variable and function names

### Code Quality

```python
# Good example
def process_document(file_path: str, config: ConversionConfig) -> ProcessingResult:
    """
    Process a document and return structured result.
    
    Args:
        file_path: Path to the document file
        config: Processing configuration
        
    Returns:
        ProcessingResult with content and metadata
        
    Raises:
        DocumentProcessingError: If processing fails
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Implementation here
    return result
```

### Documentation Strings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 10) -> bool:
    """
    Brief description of the function.
    
    Longer description if needed, explaining the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2 with default value
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer
        
    Example:
        >>> result = example_function("test", 20)
        >>> print(result)
        True
    """
```

### Error Handling

- Use specific exception types
- Provide helpful error messages
- Log errors appropriately

```python
# Good error handling
try:
    result = process_document(file_path)
except FileNotFoundError:
    logger.error(f"Document not found: {file_path}")
    raise DocumentProcessingError(f"Cannot process missing file: {file_path}")
except Exception as e:
    logger.error(f"Unexpected error processing {file_path}: {e}")
    raise DocumentProcessingError(f"Processing failed: {e}")
```

## Testing Guidelines

### Test Requirements

- All new code must have tests
- Maintain 90%+ code coverage
- Tests should be fast (< 1 second each for unit tests)
- Use mocking for external dependencies

### Test Structure

```python
class TestYourClass:
    """Test YourClass functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = ConversionConfig()
        self.instance = YourClass(self.config)
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        # Arrange
        input_data = "test input"
        expected_result = "expected output"
        
        # Act
        result = self.instance.process(input_data)
        
        # Assert
        assert result == expected_result
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(YourCustomError):
            self.instance.process(invalid_input)
```

### Mock External Dependencies

```python
from unittest.mock import Mock, patch

@patch('refinire_rag_docling.services.DocumentConverter')
def test_with_mocked_docling(mock_converter):
    """Test with mocked Docling dependency."""
    # Setup mock
    mock_instance = Mock()
    mock_converter.return_value = mock_instance
    mock_instance.convert.return_value = mock_result
    
    # Test your code
    service = DocumentService(config)
    result = service.process_document("test.pdf")
    
    # Verify
    assert result is not None
    mock_instance.convert.assert_called_once()
```

## Documentation

### Code Documentation

- All public methods and classes must have docstrings
- Use type hints consistently
- Include examples in docstrings when helpful

### User Documentation

When adding features, update relevant documentation:

- README.md (if it affects basic usage)
- API reference (docs/api_reference.md)
- Configuration guide (docs/configuration.md)
- Examples (examples/ directory)

### Documentation Style

- Write clear, concise explanations
- Include code examples
- Use consistent formatting
- Proofread for grammar and spelling

## Issue Reporting

### Bug Reports

Include:
- Python version
- Operating system
- Package version
- Minimal code to reproduce the issue
- Expected vs. actual behavior
- Error messages and stack traces

### Feature Requests

Include:
- Use case description
- Proposed API or interface
- Benefits and rationale
- Potential implementation approach

### Issue Templates

Use the provided issue templates when available.

## Pull Request Process

### Before Submitting

1. **Ensure tests pass**: `pytest tests/ -v`
2. **Check code coverage**: Coverage should not decrease
3. **Update documentation**: If your changes affect the API
4. **Add changelog entry**: For user-facing changes
5. **Rebase on main**: Ensure your branch is up to date

### Pull Request Content

- **Clear title**: Summarize the change
- **Detailed description**: Explain what and why
- **Link related issues**: Use "Fixes #123" or "Relates to #123"
- **Test information**: Describe how you tested the changes
- **Breaking changes**: Highlight any breaking changes

### Pull Request Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Added new tests for new functionality
- [ ] Manual testing completed

## Documentation
- [ ] Code comments updated
- [ ] API documentation updated
- [ ] User documentation updated

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] No unnecessary debug code
- [ ] Tests provide good coverage
```

### Review Process

1. **Automated checks**: CI tests must pass
2. **Code review**: At least one maintainer review
3. **Documentation review**: For user-facing changes
4. **Testing verification**: Manual testing if needed

### After Approval

- Maintainers will merge the PR
- Your contribution will be credited in the changelog
- Thank you for contributing!

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes (backward compatible)

### Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Update documentation if needed
4. Create release tag
5. Publish to PyPI

## Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check docs/ directory first

### Maintainer Response Time

- Issues: 1-3 business days
- Pull requests: 1-5 business days
- Security issues: Within 24 hours

## Recognition

Contributors will be recognized in:
- CHANGELOG.md
- Documentation credits
- GitHub contributors list

Thank you for contributing to the Refinire-RAG Docling Plugin! Your contributions help make document processing more accessible and powerful for the entire community.
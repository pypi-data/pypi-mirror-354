# Testing Guide

Comprehensive testing guide for the Refinire-RAG Docling Plugin.

## Test Overview

The project includes comprehensive test coverage with:
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test end-to-end functionality
- **Coverage**: 96%+ code coverage

## Running Tests

### Quick Test Run

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_models.py -v
```

### With Coverage

```bash
# Generate coverage report
pytest tests/ --cov=src --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=src --cov-report=html

# View HTML report
open htmlcov/index.html
```

### Test Categories

#### Unit Tests

```bash
# Run only unit tests
pytest tests/unit/ -v

# Run specific test class
pytest tests/unit/test_models.py::TestConversionConfig -v

# Run specific test method
pytest tests/unit/test_models.py::TestConversionConfig::test_default_config -v
```

#### Integration Tests

```bash
# Run integration tests
pytest tests/e2e/ -v
```

## Test Structure

### Directory Layout

```
tests/
├── __init__.py
├── unit/                    # Unit tests
│   ├── test_models.py      # Data model tests
│   ├── test_services.py    # Service layer tests
│   └── test_loader.py      # Loader class tests
└── e2e/                    # Integration tests
    └── test_integration.py # End-to-end tests
```

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

## Writing Tests

### Unit Test Example

```python
import pytest
from refinire_rag_docling.models import ConversionConfig, ExportFormat

class TestConversionConfig:
    """Test ConversionConfig model."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ConversionConfig()
        
        assert config.export_format == ExportFormat.MARKDOWN
        assert config.chunk_size == 512
        assert config.ocr_enabled is True
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = ConversionConfig(
            export_format=ExportFormat.TEXT,
            chunk_size=1024
        )
        
        assert config.export_format == ExportFormat.TEXT
        assert config.chunk_size == 1024
    
    def test_invalid_chunk_size(self):
        """Test chunk size validation."""
        with pytest.raises(ValueError):
            ConversionConfig(chunk_size=50)  # Too small
```

### Integration Test Example

```python
from unittest.mock import patch, Mock
import tempfile
from pathlib import Path

from refinire_rag_docling import DoclingLoader, ConversionConfig

class TestDoclingLoaderIntegration:
    """Integration tests for DoclingLoader."""
    
    @patch('refinire_rag_docling.services.DocumentConverter')
    def test_load_pdf_document(self, mock_converter_class):
        """Test loading a PDF document."""
        # Mock the DocumentConverter
        mock_converter = Mock()
        mock_converter_class.return_value = mock_converter
        
        # Mock conversion result
        mock_result = Mock()
        mock_document = Mock()
        mock_document.export_to_markdown.return_value = "# Test Document"
        mock_result.document = mock_document
        mock_converter.convert.return_value = mock_result
        
        # Create temporary PDF file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(b"PDF content")
            tmp_path = tmp.name
        
        try:
            loader = DoclingLoader()
            documents = loader.load(tmp_path)
            
            assert len(documents) == 1
            assert documents[0]["content"] == "# Test Document"
            
        finally:
            Path(tmp_path).unlink()
```

## Test Fixtures

### Temporary Files

```python
import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def temp_pdf_file():
    """Create a temporary PDF file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        tmp.write(b"PDF content")
        tmp_path = tmp.name
    
    yield tmp_path
    
    # Cleanup
    Path(tmp_path).unlink()

def test_with_temp_file(temp_pdf_file):
    """Test using temporary file fixture."""
    assert Path(temp_pdf_file).exists()
    assert temp_pdf_file.endswith('.pdf')
```

### Mock Configurations

```python
@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return ConversionConfig(
        export_format=ExportFormat.MARKDOWN,
        chunk_size=512,
        ocr_enabled=True
    )

def test_with_config(sample_config):
    """Test using configuration fixture."""
    assert sample_config.chunk_size == 512
```

## Mocking

### Mocking Docling

Since Docling has heavy dependencies, we mock it in tests:

```python
from unittest.mock import Mock, patch

@patch('refinire_rag_docling.services.DocumentConverter')
def test_document_processing(mock_converter_class):
    """Test document processing with mocked Docling."""
    # Setup mock
    mock_converter = Mock()
    mock_converter_class.return_value = mock_converter
    
    # Configure mock behavior
    mock_result = Mock()
    mock_document = Mock()
    mock_document.export_to_markdown.return_value = "Mocked content"
    mock_result.document = mock_document
    mock_converter.convert.return_value = mock_result
    
    # Test your code
    from refinire_rag_docling.services import DocumentService
    service = DocumentService(ConversionConfig())
    
    # The converter will be mocked automatically
    result = service.process_document("test.pdf")
    assert "Mocked content" in result.content
```

### Mocking File Operations

```python
from unittest.mock import patch, mock_open

@patch('pathlib.Path.exists')
@patch('pathlib.Path.stat')
def test_file_operations(mock_stat, mock_exists):
    """Test file operations with mocking."""
    # Mock file exists
    mock_exists.return_value = True
    
    # Mock file stats
    mock_stat_result = Mock()
    mock_stat_result.st_size = 1024
    mock_stat.return_value = mock_stat_result
    
    # Your test code here
    from refinire_rag_docling.models import DocumentMetadata, SupportedFormat
    
    metadata = DocumentMetadata(
        file_path="/fake/path.pdf",
        file_size=1024,
        format=SupportedFormat.PDF
    )
    
    assert metadata.file_size == 1024
```

## Test Configuration

### pytest.ini Configuration

The project uses `pyproject.toml` for pytest configuration:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "--import-mode=importlib",
    "--cov=src",
    "--cov-report=term-missing"
]
```

### Custom Markers

Define custom test markers:

```python
# In conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )

# In test files
@pytest.mark.slow
def test_large_document_processing():
    """Test processing of large documents."""
    pass

@pytest.mark.integration
def test_end_to_end_workflow():
    """Test complete workflow."""
    pass
```

### Running Specific Markers

```bash
# Run only fast tests (exclude slow)
pytest tests/ -m "not slow"

# Run only integration tests
pytest tests/ -m "integration"

# Run tests matching pattern
pytest tests/ -k "test_config"
```

## Performance Testing

### Timing Tests

```python
import time
import pytest

def test_processing_performance():
    """Test that processing completes within time limit."""
    start_time = time.time()
    
    # Your processing code here
    loader = DoclingLoader()
    # documents = loader.load("large_document.pdf")
    
    processing_time = time.time() - start_time
    
    # Assert reasonable processing time
    assert processing_time < 30.0  # 30 seconds max
```

### Memory Testing

```python
import psutil
import os

def test_memory_usage():
    """Test memory usage during processing."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Your processing code here
    loader = DoclingLoader()
    # Process documents...
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Assert reasonable memory usage (e.g., less than 500MB increase)
    assert memory_increase < 500 * 1024 * 1024
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh
    
    - name: Install dependencies
      run: |
        uv venv
        source .venv/bin/activate
        uv add --dev pytest pytest-cov
        uv pip install -e .
    
    - name: Run tests
      run: |
        source .venv/bin/activate
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Test Data

### Sample Documents

Create test documents for integration testing:

```python
# tests/conftest.py
import pytest
import tempfile
from pathlib import Path

@pytest.fixture(scope="session")
def sample_documents():
    """Create sample documents for testing."""
    docs = {}
    
    # Create PDF
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        tmp.write(b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\ntrailer\n%%EOF")
        docs['pdf'] = tmp.name
    
    # Create DOCX (minimal ZIP structure)
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
        tmp.write(b"PK\x03\x04")
        docs['docx'] = tmp.name
    
    yield docs
    
    # Cleanup
    for path in docs.values():
        Path(path).unlink()
```

## Debugging Tests

### Verbose Output

```bash
# Maximum verbosity
pytest tests/ -vvv

# Show print statements
pytest tests/ -s

# Show local variables on failure
pytest tests/ -l

# Drop into debugger on failure
pytest tests/ --pdb
```

### Custom Debug Output

```python
import logging

def test_with_debug_output():
    """Test with debug logging."""
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    logger.debug("Starting test")
    
    # Your test code
    config = ConversionConfig()
    logger.debug(f"Config: {config.to_dict()}")
    
    # Assertions
    assert config.chunk_size == 512
```

## Coverage Analysis

### Viewing Coverage Reports

```bash
# Terminal report
pytest tests/ --cov=src --cov-report=term

# Missing lines report
pytest tests/ --cov=src --cov-report=term-missing

# HTML report
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html

# XML report (for CI)
pytest tests/ --cov=src --cov-report=xml
```

### Coverage Configuration

```toml
# pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/conftest.py",
    "*/setup.py"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError"
]
```

## Best Practices

### Test Organization

1. **One test per function**: Each test should verify one specific behavior
2. **Descriptive names**: Test names should clearly describe what is being tested
3. **AAA Pattern**: Arrange, Act, Assert
4. **Independent tests**: Tests should not depend on each other

### Test Data Management

1. **Use fixtures**: For reusable test data
2. **Clean up**: Always clean up temporary files
3. **Mock external dependencies**: Don't rely on external services
4. **Parameterized tests**: Use `@pytest.mark.parametrize` for multiple inputs

### Performance

1. **Fast tests**: Keep unit tests fast (< 1 second each)
2. **Separate slow tests**: Mark slow tests and run separately
3. **Efficient mocking**: Mock heavy dependencies like Docling
4. **Parallel execution**: Use `pytest-xdist` for parallel test execution

```bash
# Install and run tests in parallel
pip install pytest-xdist
pytest tests/ -n auto
```
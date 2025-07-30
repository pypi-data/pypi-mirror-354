# Installation Guide

This guide covers different ways to install and set up the Refinire-RAG Docling Plugin.

## Prerequisites

- Python 3.10 or higher
- Virtual environment (recommended)

## Installation Methods

### Method 1: Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the package
uv add refinire-rag-docling

# For development
uv add --dev refinire-rag-docling
```

### Method 2: Using pip

```bash
# Basic installation
pip install refinire-rag-docling

# With development dependencies
pip install "refinire-rag-docling[dev]"
```

### Method 3: From Source

```bash
# Clone the repository
git clone https://github.com/your-username/refinire-rag-docling.git
cd refinire-rag-docling

# Install in development mode
uv pip install -e .

# Or with pip
pip install -e .
```

## Verify Installation

```python
# Test basic import
from refinire_rag_docling import DoclingLoader

# Create a loader instance
loader = DoclingLoader()
print("Installation successful!")
```

## Development Setup

### Full Development Environment

```bash
# Clone repository
git clone https://github.com/your-username/refinire-rag-docling.git
cd refinire-rag-docling

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all dependencies
uv add --dev pytest pytest-cov

# Install package in editable mode
uv pip install -e .

# Verify tests work
pytest tests/ -v
```

### Dependencies

#### Core Dependencies
- `docling>=1.0.0`: Document processing engine

#### Development Dependencies
- `pytest>=8.0.0`: Testing framework
- `pytest-cov>=4.1.0`: Coverage reporting

## Platform-Specific Notes

### Windows

```cmd
# Use Windows-style path separators
.venv\Scripts\activate

# Install dependencies
uv add refinire-rag-docling
```

### macOS/Linux

```bash
# Standard Unix activation
source .venv/bin/activate

# Install dependencies
uv add refinire-rag-docling
```

### Docker (Optional)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy requirements
COPY pyproject.toml .

# Install dependencies
RUN uv pip install --system .

# Copy application
COPY src/ ./src/

CMD ["python", "-m", "refinire_rag_docling"]
```

## Troubleshooting

### Common Issues

#### Import Error

```
ModuleNotFoundError: No module named 'refinire_rag_docling'
```

**Solution**: Ensure package is installed and virtual environment is activated.

#### Docling Installation Issues

```
Failed to install docling
```

**Solution**: Docling has large dependencies. Ensure stable internet connection:

```bash
# Install with verbose output
uv add --verbose docling
```

#### Permission Errors

```
Permission denied error during installation
```

**Solution**: Use virtual environment or user installation:

```bash
# User installation
pip install --user refinire-rag-docling

# Or use virtual environment
python -m venv .venv
source .venv/bin/activate
pip install refinire-rag-docling
```

### GPU Support (Optional)

If you need GPU acceleration for document processing:

```bash
# Install with CUDA support (if available)
uv add torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Configuration

### Environment Variables

```bash
# Optional: Set cache directory
export DOCLING_CACHE_DIR=/path/to/cache

# Optional: Set log level
export DOCLING_LOG_LEVEL=INFO
```

### Config File

Create `~/.refinire-rag-docling/config.yaml`:

```yaml
# Default configuration
default:
  export_format: markdown
  chunk_size: 512
  ocr_enabled: true
  table_structure: true

# Performance settings
performance:
  batch_size: 10
  max_workers: 4
```

## Updating

### Update to Latest Version

```bash
# With uv
uv add --upgrade refinire-rag-docling

# With pip
pip install --upgrade refinire-rag-docling
```

### Check Version

```python
import refinire_rag_docling
print(refinire_rag_docling.__version__)
```

## Uninstallation

```bash
# With uv
uv remove refinire-rag-docling

# With pip
pip uninstall refinire-rag-docling
```

## Next Steps

After installation:

1. 📖 Read the [Quick Start Guide](../README.md#quick-start)
2. 🔧 Check [Configuration Options](./configuration.md)
3. 💡 Browse [Examples](../examples/)
4. 🧪 Run [Tests](./testing.md)
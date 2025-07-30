# Configuration Guide

This guide covers all configuration options available in the Refinire-RAG Docling Plugin.

## ConversionConfig

The main configuration class for controlling document processing behavior.

### Basic Configuration

```python
from refinire_rag_docling import ConversionConfig, ExportFormat

config = ConversionConfig(
    export_format=ExportFormat.MARKDOWN,
    chunk_size=512,
    ocr_enabled=True,
    table_structure=True
)
```

### Configuration Parameters

#### export_format

Controls the output format of processed documents.

```python
# Available options
ExportFormat.MARKDOWN  # Rich text with formatting (default)
ExportFormat.TEXT      # Plain text only
ExportFormat.JSON      # Structured JSON output
```

**Examples:**

```python
# Markdown output (preserves formatting, tables, structure)
config = ConversionConfig(export_format=ExportFormat.MARKDOWN)

# Plain text output (simple text extraction)
config = ConversionConfig(export_format=ExportFormat.TEXT)

# JSON output (structured data with metadata)
config = ConversionConfig(export_format=ExportFormat.JSON)
```

#### chunk_size

Controls how large text is split into chunks for RAG applications.

```python
# Range: 100 - 4096 characters
chunk_size: int = 512  # Default
```

**Examples:**

```python
# Small chunks for precise retrieval
config = ConversionConfig(chunk_size=256)

# Medium chunks (balanced)
config = ConversionConfig(chunk_size=512)

# Large chunks for context preservation
config = ConversionConfig(chunk_size=2048)

# Maximum chunk size
config = ConversionConfig(chunk_size=4096)
```

**Choosing Chunk Size:**

- **256-512**: Best for FAQ, precise fact retrieval
- **512-1024**: Balanced for most RAG applications
- **1024-2048**: Better for complex reasoning, context preservation
- **2048-4096**: Long-form content, maintaining narrative flow

#### ocr_enabled

Enables or disables Optical Character Recognition for scanned documents and images.

```python
ocr_enabled: bool = True  # Default
```

**Examples:**

```python
# Enable OCR for scanned documents
config = ConversionConfig(ocr_enabled=True)

# Disable OCR for faster processing of text-based PDFs
config = ConversionConfig(ocr_enabled=False)
```

**When to use:**

- **Enable**: Scanned PDFs, images with text, poor quality documents
- **Disable**: Digital PDFs, DOCX files, when speed is priority

#### table_structure

Preserves table structure in the output.

```python
table_structure: bool = True  # Default
```

**Examples:**

```python
# Preserve table formatting (recommended)
config = ConversionConfig(table_structure=True)

# Extract table content as plain text
config = ConversionConfig(table_structure=False)
```

#### options

Additional processing options for advanced use cases.

```python
options: Dict[str, Any] = {}  # Default
```

**Examples:**

```python
# Custom processing options
config = ConversionConfig(
    options={
        "image_resolution": "high",
        "language_hint": "en",
        "preserve_whitespace": True
    }
)
```

## Preset Configurations

### Quick Setup Methods

The plugin provides factory methods for common configurations:

```python
from refinire_rag_docling import DoclingLoader

# Markdown output preset
loader = DoclingLoader.create_with_markdown_output(chunk_size=512)

# Text output preset
loader = DoclingLoader.create_with_text_output(chunk_size=1024)
```

### Common Presets

#### High-Quality Document Processing

```python
config = ConversionConfig(
    export_format=ExportFormat.MARKDOWN,
    chunk_size=1024,
    ocr_enabled=True,
    table_structure=True,
    options={
        "preserve_formatting": True,
        "extract_images": True
    }
)
```

#### Fast Processing

```python
config = ConversionConfig(
    export_format=ExportFormat.TEXT,
    chunk_size=512,
    ocr_enabled=False,
    table_structure=False
)
```

#### RAG-Optimized

```python
config = ConversionConfig(
    export_format=ExportFormat.MARKDOWN,
    chunk_size=768,  # Optimal for many embedding models
    ocr_enabled=True,
    table_structure=True
)
```

#### Large Document Processing

```python
config = ConversionConfig(
    export_format=ExportFormat.TEXT,
    chunk_size=2048,
    ocr_enabled=False,  # Speed up processing
    table_structure=True
)
```

## Format-Specific Settings

### PDF Documents

```python
# Optimized for PDFs
config = ConversionConfig(
    export_format=ExportFormat.MARKDOWN,
    ocr_enabled=True,      # Handle scanned PDFs
    table_structure=True,  # Preserve table layouts
    chunk_size=1024
)
```

### Office Documents (DOCX, XLSX)

```python
# Optimized for Office docs
config = ConversionConfig(
    export_format=ExportFormat.MARKDOWN,
    ocr_enabled=False,     # Not needed for Office docs
    table_structure=True,  # Important for spreadsheets
    chunk_size=512
)
```

### Web Content (HTML)

```python
# Optimized for HTML
config = ConversionConfig(
    export_format=ExportFormat.MARKDOWN,
    ocr_enabled=False,
    table_structure=True,
    chunk_size=768
)
```

### Images

```python
# Optimized for images
config = ConversionConfig(
    export_format=ExportFormat.TEXT,
    ocr_enabled=True,      # Essential for images
    table_structure=False, # Usually not relevant
    chunk_size=512
)
```

## Environment-Based Configuration

### Using Environment Variables

```python
import os
from refinire_rag_docling import ConversionConfig, ExportFormat

# Read from environment
export_format = os.getenv('DOCLING_EXPORT_FORMAT', 'markdown')
chunk_size = int(os.getenv('DOCLING_CHUNK_SIZE', '512'))
ocr_enabled = os.getenv('DOCLING_OCR_ENABLED', 'true').lower() == 'true'

config = ConversionConfig(
    export_format=ExportFormat(export_format),
    chunk_size=chunk_size,
    ocr_enabled=ocr_enabled
)
```

### Configuration File

Create a configuration file for reusable settings:

```yaml
# config.yaml
default:
  export_format: markdown
  chunk_size: 512
  ocr_enabled: true
  table_structure: true

development:
  export_format: text
  chunk_size: 256
  ocr_enabled: false
  table_structure: false

production:
  export_format: markdown
  chunk_size: 1024
  ocr_enabled: true
  table_structure: true
```

```python
import yaml
from refinire_rag_docling import ConversionConfig, ExportFormat

def load_config(env='default'):
    with open('config.yaml', 'r') as f:
        configs = yaml.safe_load(f)
    
    cfg = configs[env]
    return ConversionConfig(
        export_format=ExportFormat(cfg['export_format']),
        chunk_size=cfg['chunk_size'],
        ocr_enabled=cfg['ocr_enabled'],
        table_structure=cfg['table_structure']
    )

# Usage
config = load_config('production')
```

## Validation

### Automatic Validation

The configuration automatically validates parameters:

```python
# This will raise ValueError
config = ConversionConfig(chunk_size=50)  # Too small
config = ConversionConfig(chunk_size=5000)  # Too large
```

### Manual Validation

```python
config = ConversionConfig(chunk_size=512)

# Validate configuration
if config.validate():
    print("Configuration is valid")
```

## Performance Tuning

### Memory Usage

```python
# Low memory usage
config = ConversionConfig(
    chunk_size=512,      # Smaller chunks
    ocr_enabled=False,   # Skip OCR processing
    table_structure=False
)
```

### Processing Speed

```python
# Fast processing
config = ConversionConfig(
    export_format=ExportFormat.TEXT,  # Faster than Markdown
    ocr_enabled=False,                # Skip slow OCR
    chunk_size=1024                   # Fewer chunks to process
)
```

### Quality vs Speed Trade-offs

| Setting | Quality | Speed | Memory |
|---------|---------|-------|---------|
| `ocr_enabled=True` | High | Slow | High |
| `ocr_enabled=False` | Medium | Fast | Low |
| `table_structure=True` | High | Medium | Medium |
| `export_format=MARKDOWN` | High | Medium | Medium |
| `export_format=TEXT` | Low | Fast | Low |

## Troubleshooting

### Common Configuration Issues

#### Chunk Size Too Small

```python
# Error: chunk_size must be between 100 and 4096
config = ConversionConfig(chunk_size=50)
```

**Solution**: Use minimum chunk size of 100.

#### Invalid Export Format

```python
# Error: Invalid export format
config = ConversionConfig(export_format="invalid")
```

**Solution**: Use ExportFormat enum values.

#### Performance Issues

If processing is slow:

1. Disable OCR for text-based documents
2. Use TEXT export format instead of MARKDOWN
3. Increase chunk size to reduce processing overhead
4. Disable table structure preservation if not needed

### Debug Configuration

```python
# Print current configuration
config = ConversionConfig()
print(config.to_dict())

# Validate configuration
try:
    config.validate()
    print("Configuration is valid")
except ValueError as e:
    print(f"Configuration error: {e}")
```
"""Unit tests for models module."""

import pytest
from pathlib import Path
from refinire_rag_docling.models import (
    ConversionConfig,
    DocumentMetadata, 
    ProcessingResult,
    SupportedFormat,
    ExportFormat,
    FileFormatNotSupportedError
)


class TestConversionConfig:
    """Test ConversionConfig model."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ConversionConfig()
        
        assert config.export_format == ExportFormat.MARKDOWN
        assert config.chunk_size == 512
        assert config.ocr_enabled is True
        assert config.table_structure is True
        assert config.options == {}
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = ConversionConfig(
            export_format=ExportFormat.TEXT,
            chunk_size=1024,
            ocr_enabled=False
        )
        
        assert config.export_format == ExportFormat.TEXT
        assert config.chunk_size == 1024
        assert config.ocr_enabled is False
    
    def test_chunk_size_validation(self):
        """Test chunk size validation."""
        with pytest.raises(ValueError):
            ConversionConfig(chunk_size=50)  # Too small
        
        with pytest.raises(ValueError):
            ConversionConfig(chunk_size=5000)  # Too large
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = ConversionConfig(chunk_size=256)
        result = config.to_dict()
        
        assert isinstance(result, dict)
        assert result["chunk_size"] == 256


class TestDocumentMetadata:
    """Test DocumentMetadata model."""
    
    def test_valid_metadata(self, tmp_path):
        """Test valid metadata creation."""
        # Create a temporary file
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")
        
        metadata = DocumentMetadata(
            file_path=str(test_file),
            file_size=100,
            format=SupportedFormat.PDF
        )
        
        assert metadata.file_path == str(test_file)
        assert metadata.file_size == 100
        assert metadata.format == SupportedFormat.PDF
    
    def test_invalid_file_path(self):
        """Test invalid file path validation."""
        with pytest.raises(ValueError, match="File does not exist"):
            DocumentMetadata(
                file_path="/nonexistent/path/file.pdf",
                file_size=100,
                format=SupportedFormat.PDF
            )


class TestProcessingResult:
    """Test ProcessingResult model."""
    
    def test_basic_result(self, tmp_path):
        """Test basic processing result."""
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")
        
        metadata = DocumentMetadata(
            file_path=str(test_file),
            file_size=100,
            format=SupportedFormat.PDF
        )
        
        result = ProcessingResult(
            content="This is test content for chunking.",
            metadata=metadata,
            processing_time=1.5
        )
        
        assert result.content == "This is test content for chunking."
        assert result.processing_time == 1.5
        assert result.chunks == []
    
    def test_get_chunks(self, tmp_path):
        """Test content chunking."""
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")
        
        metadata = DocumentMetadata(
            file_path=str(test_file),
            file_size=100,
            format=SupportedFormat.PDF
        )
        
        content = " ".join(["word"] * 100)  # 100 words
        result = ProcessingResult(
            content=content,
            metadata=metadata,
            processing_time=1.0
        )
        
        chunks = result.get_chunks(chunk_size=50)
        
        assert len(chunks) > 1
        assert all(len(chunk) <= 50 for chunk in chunks)
    
    def test_to_rag_format(self, tmp_path):
        """Test RAG format conversion."""
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")
        
        metadata = DocumentMetadata(
            file_path=str(test_file),
            file_size=100,
            format=SupportedFormat.PDF
        )
        
        result = ProcessingResult(
            content="Test content",
            metadata=metadata,
            processing_time=1.0
        )
        
        rag_format = result.to_rag_format()
        
        assert "content" in rag_format
        assert "metadata" in rag_format
        assert "chunks" in rag_format
        assert "source" in rag_format
        assert rag_format["source"] == str(test_file)


class TestSupportedFormat:
    """Test SupportedFormat enum."""
    
    def test_format_values(self):
        """Test supported format values."""
        assert SupportedFormat.PDF == "pdf"
        assert SupportedFormat.DOCX == "docx"
        assert SupportedFormat.XLSX == "xlsx"
        assert SupportedFormat.HTML == "html"
    
    def test_invalid_format(self):
        """Test invalid format handling."""
        with pytest.raises(ValueError):
            SupportedFormat("txt")


class TestExportFormat:
    """Test ExportFormat enum."""
    
    def test_export_format_values(self):
        """Test export format values."""
        assert ExportFormat.MARKDOWN == "markdown"
        assert ExportFormat.TEXT == "text"
        assert ExportFormat.JSON == "json"
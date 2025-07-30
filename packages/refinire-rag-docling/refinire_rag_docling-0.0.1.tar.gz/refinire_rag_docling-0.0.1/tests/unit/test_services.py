"""Unit tests for services module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from refinire_rag_docling.services import DocumentService
from refinire_rag_docling.models import (
    ConversionConfig,
    ExportFormat,
    SupportedFormat,
    DocumentProcessingError,
    FileFormatNotSupportedError
)


class TestDocumentService:
    """Test DocumentService class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = ConversionConfig(export_format=ExportFormat.MARKDOWN)
        self.service = DocumentService(self.config)
    
    def test_init(self):
        """Test service initialization."""
        assert self.service.config == self.config
        assert self.service.converter is not None
    
    def test_validate_file_format_valid(self, tmp_path):
        """Test valid file format validation."""
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")
        
        # Should not raise exception
        self.service._validate_file_format(str(test_file))
    
    def test_validate_file_format_invalid(self, tmp_path):
        """Test invalid file format validation."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        with pytest.raises(FileFormatNotSupportedError):
            self.service._validate_file_format(str(test_file))
    
    def test_validate_file_format_not_exists(self):
        """Test file not found validation."""
        with pytest.raises(FileNotFoundError):
            self.service._validate_file_format("/nonexistent/file.pdf")
    
    @patch('refinire_rag_docling.services.DocumentConverter')
    def test_extract_content_markdown(self, mock_converter_class):
        """Test markdown content extraction."""
        # Mock the converter and its result
        mock_converter = Mock()
        mock_converter_class.return_value = mock_converter
        
        mock_result = Mock()
        mock_document = Mock()
        mock_document.export_to_markdown.return_value = "# Test Document"
        mock_result.document = mock_document
        
        service = DocumentService(self.config)
        service.converter = mock_converter
        
        content = service._extract_content(mock_result)
        
        assert content == "# Test Document"
        mock_document.export_to_markdown.assert_called_once()
    
    @patch('refinire_rag_docling.services.DocumentConverter')
    def test_extract_content_text(self, mock_converter_class):
        """Test text content extraction."""
        config = ConversionConfig(export_format=ExportFormat.TEXT)
        service = DocumentService(config)
        
        mock_result = Mock()
        mock_document = Mock()
        mock_document.export_to_text.return_value = "Test Document"
        mock_result.document = mock_document
        
        content = service._extract_content(mock_result)
        
        assert content == "Test Document"
        mock_document.export_to_text.assert_called_once()
    
    def test_extract_metadata(self, tmp_path):
        """Test metadata extraction."""
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")
        
        mock_result = Mock()
        mock_document = Mock()
        mock_document.pages = [1, 2, 3]  # 3 pages
        mock_result.document = mock_document
        
        metadata = self.service._extract_metadata(str(test_file), mock_result)
        
        assert metadata.file_path == str(test_file.absolute())
        assert metadata.file_size > 0
        assert metadata.format == SupportedFormat.PDF
    
    def test_get_document_metadata_with_pages(self):
        """Test document metadata extraction with pages."""
        mock_result = Mock()
        mock_document = Mock()
        mock_document.pages = [1, 2, 3]
        mock_result.document = mock_document
        
        metadata = self.service._get_document_metadata(mock_result)
        
        assert metadata['page_count'] == 3
    
    def test_get_document_metadata_exception_handling(self):
        """Test metadata extraction with exceptions."""
        mock_result = Mock()
        mock_result.document = None  # This will cause an exception
        
        metadata = self.service._get_document_metadata(mock_result)
        
        assert metadata == {}
    
    @patch('refinire_rag_docling.services.DocumentConverter')
    def test_process_document_success(self, mock_converter_class, tmp_path):
        """Test successful document processing."""
        # Create test file
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")
        
        # Mock converter
        mock_converter = Mock()
        mock_converter_class.return_value = mock_converter
        
        mock_result = Mock()
        mock_document = Mock()
        mock_document.export_to_markdown.return_value = "# Test Content"
        mock_document.pages = [1, 2]
        mock_result.document = mock_document
        
        mock_converter.convert.return_value = mock_result
        
        # Create service with mocked converter
        service = DocumentService(self.config)
        service.converter = mock_converter
        
        result = service.process_document(str(test_file))
        
        assert result.content == "# Test Content"
        assert result.metadata.format == SupportedFormat.PDF
        assert result.processing_time > 0
        mock_converter.convert.assert_called_once_with(str(test_file))
    
    @patch('refinire_rag_docling.services.DocumentConverter')
    def test_process_document_failure(self, mock_converter_class, tmp_path):
        """Test document processing failure."""
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")
        
        mock_converter = Mock()
        mock_converter_class.return_value = mock_converter
        mock_converter.convert.side_effect = Exception("Conversion failed")
        
        service = DocumentService(self.config)
        service.converter = mock_converter
        
        with pytest.raises(DocumentProcessingError, match="Failed to process document"):
            service.process_document(str(test_file))
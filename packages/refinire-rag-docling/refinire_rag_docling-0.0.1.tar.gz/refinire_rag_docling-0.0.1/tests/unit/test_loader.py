"""Unit tests for loader module."""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from refinire_rag_docling.loader import DoclingLoader
from refinire_rag_docling.models import (
    ConversionConfig,
    ExportFormat,
    ProcessingResult,
    DocumentMetadata,
    SupportedFormat
)


class TestDoclingLoader:
    """Test DoclingLoader class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = ConversionConfig(chunk_size=256)
        self.loader = DoclingLoader(self.config)
    
    def test_init_with_config(self):
        """Test loader initialization with config."""
        assert self.loader.config == self.config
        assert self.loader.service is not None
    
    def test_init_without_config(self):
        """Test loader initialization without config."""
        loader = DoclingLoader()
        assert loader.config is not None
        assert loader.config.export_format == ExportFormat.MARKDOWN
    
    @patch('refinire_rag_docling.loader.DocumentService')
    def test_load_single_document(self, mock_service_class, tmp_path):
        """Test loading a single document."""
        # Create test file
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")
        
        # Mock service
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        
        # Mock processing result
        metadata = DocumentMetadata(
            file_path=str(test_file),
            file_size=100,
            format=SupportedFormat.PDF,
            page_count=2,
            title="Test Document"
        )
        
        processing_result = ProcessingResult(
            content="# Test Document\n\nThis is test content.",
            metadata=metadata,
            processing_time=1.5
        )
        
        mock_service.process_document.return_value = processing_result
        
        # Create loader with mock service
        loader = DoclingLoader(self.config)
        loader.service = mock_service
        
        # Load document
        documents = loader.load(str(test_file))
        
        assert len(documents) == 1
        doc = documents[0]
        
        assert doc["content"] == "# Test Document\n\nThis is test content."
        assert doc["metadata"]["source"] == str(test_file)
        assert doc["metadata"]["format"] == "pdf"
        assert doc["metadata"]["page_count"] == 2
        assert doc["metadata"]["title"] == "Test Document"
        
        mock_service.process_document.assert_called_once_with(str(test_file))
    
    @patch('refinire_rag_docling.loader.DocumentService')
    def test_load_batch_documents(self, mock_service_class, tmp_path):
        """Test loading multiple documents in batch."""
        # Create test files
        test_file1 = tmp_path / "test1.pdf"
        test_file1.write_text("test content 1")
        test_file2 = tmp_path / "test2.pdf"
        test_file2.write_text("test content 2")
        
        # Mock service
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        
        # Mock processing results
        def mock_process(file_path):
            if "test1" in file_path:
                metadata = DocumentMetadata(
                    file_path=file_path,
                    file_size=100,
                    format=SupportedFormat.PDF
                )
                return ProcessingResult(
                    content="Content 1",
                    metadata=metadata,
                    processing_time=1.0
                )
            else:
                metadata = DocumentMetadata(
                    file_path=file_path,
                    file_size=200,
                    format=SupportedFormat.PDF
                )
                return ProcessingResult(
                    content="Content 2",
                    metadata=metadata,
                    processing_time=1.5
                )
        
        mock_service.process_document.side_effect = mock_process
        
        # Create loader with mock service
        loader = DoclingLoader(self.config)
        loader.service = mock_service
        
        # Load documents
        documents = loader.load_batch([str(test_file1), str(test_file2)])
        
        assert len(documents) == 2
        assert documents[0]["content"] == "Content 1"
        assert documents[1]["content"] == "Content 2"
    
    @patch('refinire_rag_docling.loader.DocumentService')
    def test_load_batch_with_failure(self, mock_service_class, tmp_path, capsys):
        """Test batch loading with one document failing."""
        test_file1 = tmp_path / "test1.pdf"
        test_file1.write_text("test content 1")
        test_file2 = tmp_path / "test2.pdf"
        test_file2.write_text("test content 2")
        
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        
        def mock_process(file_path):
            if "test1" in file_path:
                raise Exception("Processing failed")
            else:
                metadata = DocumentMetadata(
                    file_path=file_path,
                    file_size=200,
                    format=SupportedFormat.PDF
                )
                return ProcessingResult(
                    content="Content 2",
                    metadata=metadata,
                    processing_time=1.5
                )
        
        mock_service.process_document.side_effect = mock_process
        
        loader = DoclingLoader(self.config)
        loader.service = mock_service
        
        documents = loader.load_batch([str(test_file1), str(test_file2)])
        
        # Should only have one successful document
        assert len(documents) == 1
        assert documents[0]["content"] == "Content 2"
        
        # Check warning was printed
        captured = capsys.readouterr()
        assert "Warning: Failed to process" in captured.out
    
    def test_convert_to_rag_document_basic(self, tmp_path):
        """Test basic RAG document conversion."""
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
        
        rag_doc = self.loader._convert_to_rag_document(result)
        
        assert rag_doc["content"] == "Test content"
        assert rag_doc["metadata"]["source"] == str(test_file)
        assert rag_doc["metadata"]["format"] == "pdf"
        assert rag_doc["metadata"]["processing_time"] == 1.0
    
    def test_convert_to_rag_document_with_chunks(self, tmp_path):
        """Test RAG document conversion with chunking."""
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")
        
        metadata = DocumentMetadata(
            file_path=str(test_file),
            file_size=100,
            format=SupportedFormat.PDF
        )
        
        # Create long content to trigger chunking
        long_content = " ".join(["word"] * 100)  # 100 words
        result = ProcessingResult(
            content=long_content,
            metadata=metadata,
            processing_time=1.0
        )
        
        rag_doc = self.loader._convert_to_rag_document(result)
        
        assert "chunks" in rag_doc
        assert "chunk_count" in rag_doc["metadata"]
        assert len(rag_doc["chunks"]) > 1
    
    def test_factory_method_markdown(self):
        """Test factory method for markdown output."""
        loader = DoclingLoader.create_with_markdown_output(chunk_size=1024)
        
        assert loader.config.export_format == ExportFormat.MARKDOWN
        assert loader.config.chunk_size == 1024
    
    def test_factory_method_text(self):
        """Test factory method for text output."""
        loader = DoclingLoader.create_with_text_output(chunk_size=2048)
        
        assert loader.config.export_format == ExportFormat.TEXT
        assert loader.config.chunk_size == 2048
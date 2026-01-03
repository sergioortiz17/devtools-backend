"""Unit tests for core exceptions."""
import pytest
from fastapi import status

from app.core.exceptions import (
    DictionaryWordNotFoundError,
    DictionaryWordAlreadyExistsError,
    DatabaseConnectionError,
    ServiceError
)


class TestDictionaryWordNotFoundError:
    """Test cases for DictionaryWordNotFoundError."""
    
    def test_exception_creation(self):
        """Test creating the exception."""
        error = DictionaryWordNotFoundError("test")
        
        assert error.status_code == status.HTTP_404_NOT_FOUND
        assert "test" in error.detail
        assert "not found" in error.detail.lower()
    
    def test_exception_message(self):
        """Test exception message format."""
        error = DictionaryWordNotFoundError("example")
        
        assert error.detail == "Word 'example' not found in dictionary"


class TestDictionaryWordAlreadyExistsError:
    """Test cases for DictionaryWordAlreadyExistsError."""
    
    def test_exception_creation(self):
        """Test creating the exception."""
        error = DictionaryWordAlreadyExistsError("test")
        
        assert error.status_code == status.HTTP_409_CONFLICT
        assert "test" in error.detail
        assert "already exists" in error.detail.lower()
    
    def test_exception_message(self):
        """Test exception message format."""
        error = DictionaryWordAlreadyExistsError("example")
        
        assert error.detail == "Word 'example' already exists in dictionary"


class TestDatabaseConnectionError:
    """Test cases for DatabaseConnectionError."""
    
    def test_exception_creation(self):
        """Test creating the exception."""
        error = DatabaseConnectionError("Connection failed")
        
        assert str(error) == "Connection failed"
        assert isinstance(error, Exception)


class TestServiceError:
    """Test cases for ServiceError."""
    
    def test_exception_creation(self):
        """Test creating the exception."""
        error = ServiceError("Service error occurred")
        
        assert str(error) == "Service error occurred"
        assert isinstance(error, Exception)


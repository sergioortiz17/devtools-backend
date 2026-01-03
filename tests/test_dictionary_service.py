"""Unit tests for dictionary service."""
import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.exc import IntegrityError

from app.dictionary.service import DictionaryService
from app.dictionary.repository import IDictionaryRepository
from app.dictionary.db_models import DictionaryEntry
from app.core.exceptions import (
    DictionaryWordNotFoundError,
    DictionaryWordAlreadyExistsError
)


@pytest.fixture
def mock_repository():
    """Create a mock repository."""
    return Mock(spec=IDictionaryRepository)


@pytest.fixture
def dictionary_service(mock_repository):
    """Create dictionary service with mock repository."""
    return DictionaryService(mock_repository)


@pytest.fixture
def sample_entry():
    """Create a sample dictionary entry."""
    entry = DictionaryEntry(id=1, word="test", definition="A test definition")
    return entry


class TestDictionaryServiceAddWord:
    """Test cases for adding words."""
    
    def test_add_word_success(self, dictionary_service, mock_repository, sample_entry):
        """Test successfully adding a word."""
        mock_repository.find_by_word.return_value = None
        mock_repository.create.return_value = sample_entry
        
        result = dictionary_service.add_word("test", "A test definition")
        
        assert result == sample_entry
        mock_repository.find_by_word.assert_called_once_with("test")
        mock_repository.create.assert_called_once_with("test", "A test definition")
        mock_repository.commit.assert_called_once()
    
    def test_add_word_duplicate(self, dictionary_service, mock_repository):
        """Test adding a duplicate word raises error."""
        existing_entry = DictionaryEntry(id=1, word="test", definition="Existing")
        mock_repository.find_by_word.return_value = existing_entry
        
        with pytest.raises(DictionaryWordAlreadyExistsError) as exc_info:
            dictionary_service.add_word("test", "New definition")
        
        assert "already exists" in str(exc_info.value.detail).lower()
        mock_repository.find_by_word.assert_called_once_with("test")
        mock_repository.create.assert_not_called()
        mock_repository.commit.assert_not_called()
    
    def test_add_word_empty_word(self, dictionary_service, mock_repository):
        """Test adding word with empty word raises ValueError."""
        with pytest.raises(ValueError, match="Word cannot be empty"):
            dictionary_service.add_word("", "Definition")
        
        mock_repository.find_by_word.assert_not_called()
        mock_repository.create.assert_not_called()
    
    def test_add_word_empty_definition(self, dictionary_service, mock_repository):
        """Test adding word with empty definition raises ValueError."""
        with pytest.raises(ValueError, match="Definition cannot be empty"):
            dictionary_service.add_word("test", "")
        
        mock_repository.find_by_word.assert_not_called()
        mock_repository.create.assert_not_called()
    
    def test_add_word_whitespace_only(self, dictionary_service, mock_repository):
        """Test adding word with only whitespace raises ValueError."""
        with pytest.raises(ValueError):
            dictionary_service.add_word("   ", "Definition")
        
        mock_repository.find_by_word.assert_not_called()
        mock_repository.create.assert_not_called()
    
    def test_add_word_integrity_error(self, dictionary_service, mock_repository):
        """Test handling IntegrityError from database."""
        mock_repository.find_by_word.return_value = None
        mock_repository.create.side_effect = IntegrityError("statement", None, None)
        
        with pytest.raises(DictionaryWordAlreadyExistsError):
            dictionary_service.add_word("test", "Definition")
        
        mock_repository.rollback.assert_called_once()
        mock_repository.commit.assert_not_called()
    
    def test_add_word_value_error_from_repository(self, dictionary_service, mock_repository):
        """Test handling ValueError from repository."""
        mock_repository.find_by_word.return_value = None
        mock_repository.create.side_effect = ValueError("Invalid input")
        
        with pytest.raises(ValueError, match="Invalid input"):
            dictionary_service.add_word("test", "Definition")
        
        mock_repository.rollback.assert_called_once()


class TestDictionaryServiceGetWord:
    """Test cases for retrieving words."""
    
    def test_get_word_success(self, dictionary_service, mock_repository, sample_entry):
        """Test successfully retrieving a word."""
        mock_repository.find_by_word.return_value = sample_entry
        
        result = dictionary_service.get_word("test")
        
        assert result == sample_entry
        mock_repository.find_by_word.assert_called_once_with("test")
    
    def test_get_word_not_found(self, dictionary_service, mock_repository):
        """Test retrieving non-existent word raises error."""
        mock_repository.find_by_word.return_value = None
        
        with pytest.raises(DictionaryWordNotFoundError) as exc_info:
            dictionary_service.get_word("nonexistent")
        
        assert "not found" in str(exc_info.value.detail).lower()
        mock_repository.find_by_word.assert_called_once_with("nonexistent")
    
    def test_get_word_empty_word(self, dictionary_service, mock_repository):
        """Test retrieving word with empty string raises ValueError."""
        with pytest.raises(ValueError, match="Word cannot be empty"):
            dictionary_service.get_word("")
        
        mock_repository.find_by_word.assert_not_called()
    
    def test_get_word_whitespace_only(self, dictionary_service, mock_repository):
        """Test retrieving word with only whitespace raises ValueError."""
        with pytest.raises(ValueError, match="Word cannot be empty"):
            dictionary_service.get_word("   ")
        
        mock_repository.find_by_word.assert_not_called()


class TestDictionaryServiceValidation:
    """Test cases for input validation."""
    
    def test_validate_word_input_valid(self, dictionary_service):
        """Test validation passes for valid inputs."""
        # Should not raise
        dictionary_service._validate_word_input("test", "definition")
    
    def test_validate_word_input_empty_word(self, dictionary_service):
        """Test validation fails for empty word."""
        with pytest.raises(ValueError, match="Word cannot be empty"):
            dictionary_service._validate_word_input("", "definition")
    
    def test_validate_word_input_empty_definition(self, dictionary_service):
        """Test validation fails for empty definition."""
        with pytest.raises(ValueError, match="Definition cannot be empty"):
            dictionary_service._validate_word_input("word", "")
    
    def test_validate_word_input_whitespace_word(self, dictionary_service):
        """Test validation fails for whitespace-only word."""
        with pytest.raises(ValueError, match="Word cannot be empty"):
            dictionary_service._validate_word_input("   ", "definition")
    
    def test_validate_word_input_whitespace_definition(self, dictionary_service):
        """Test validation fails for whitespace-only definition."""
        with pytest.raises(ValueError, match="Definition cannot be empty"):
            dictionary_service._validate_word_input("word", "   ")


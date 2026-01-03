"""Unit tests for words service."""
import pytest

from app.words.service import WordConcatenationService
from app.words.models import WordConcatRequest, WordConcatResponse


class TestWordConcatenationService:
    """Test cases for word concatenation service."""
    
    @pytest.fixture
    def service(self):
        """Create word concatenation service instance."""
        return WordConcatenationService()
    
    def test_concatenate_words_basic(self, service):
        """Test basic word concatenation."""
        request = WordConcatRequest(words=["hello", "world"])
        
        result = service.concatenate_words(request)
        
        assert result.result == "hw"
        assert result.words == ["hello", "world"]
    
    def test_concatenate_multiple_words(self, service):
        """Test concatenating multiple words."""
        request = WordConcatRequest(words=["cat", "dog", "bird"])
        
        result = service.concatenate_words(request)
        
        # c (index 0) + o (index 1) + i (index 2)
        assert result.result == "coi"
        assert result.words == ["cat", "dog", "bird"]
    
    def test_concatenate_short_word(self, service):
        """Test concatenation when word is shorter than its index."""
        request = WordConcatRequest(words=["hi", "world"])
        
        result = service.concatenate_words(request)
        
        # h (index 0 of "hi") + w (index 1 of "world")
        assert result.result == "hw"
    
    def test_concatenate_single_word(self, service):
        """Test concatenating a single word."""
        request = WordConcatRequest(words=["test"])
        
        result = service.concatenate_words(request)
        
        # t (index 0 of "test")
        assert result.result == "t"
        assert result.words == ["test"]
    
    def test_concatenate_empty_list(self, service):
        """Test concatenating empty word list."""
        request = WordConcatRequest(words=[])
        
        result = service.concatenate_words(request)
        
        assert result.result == ""
        assert result.words == []
    
    def test_concatenate_word_too_short(self, service):
        """Test concatenation when word is too short for its index."""
        request = WordConcatRequest(words=["a", "bc", "def"])
        
        result = service.concatenate_words(request)
        
        # a (index 0) + c (index 1) + f (index 2)
        assert result.result == "acf"
    
    def test_concatenate_with_very_short_words(self, service):
        """Test concatenation with very short words."""
        request = WordConcatRequest(words=["a", "b"])
        
        result = service.concatenate_words(request)
        
        # a (index 0) + b (index 1) - but "b" is too short for index 1
        assert result.result == "a"
    
    def test_extract_characters_by_index(self, service):
        """Test character extraction method."""
        words = ["hello", "world", "test"]
        
        chars = service._extract_characters_by_index(words)
        
        assert chars == ["h", "o", "s"]
    
    def test_extract_characters_with_short_word(self, service):
        """Test extraction when word is too short."""
        words = ["hi", "world"]
        
        chars = service._extract_characters_by_index(words)
        
        assert chars == ["h", "w"]
    
    def test_is_valid_index(self, service):
        """Test index validation method."""
        assert service._is_valid_index("hello", 0) is True
        assert service._is_valid_index("hello", 4) is True
        assert service._is_valid_index("hello", 5) is False
        assert service._is_valid_index("hello", -1) is False
        assert service._is_valid_index("hi", 2) is False
        assert service._is_valid_index("a", 0) is True
        assert service._is_valid_index("a", 1) is False


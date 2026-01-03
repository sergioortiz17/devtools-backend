"""Unit tests for dictionary repository."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.core.database import Base
from app.dictionary.repository import DictionaryRepository
from app.dictionary.db_models import DictionaryEntry


@pytest.fixture
def db_session():
    """Create a fresh database session for each test."""
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def repository(db_session):
    """Create repository instance."""
    return DictionaryRepository(db_session)


class TestDictionaryRepository:
    """Test cases for dictionary repository."""
    
    def test_create_entry_success(self, repository):
        """Test creating a dictionary entry."""
        entry = repository.create("test", "A test definition")
        
        assert entry.word == "test"
        assert entry.definition == "A test definition"
        assert entry.id is not None
    
    def test_create_entry_trims_whitespace(self, repository):
        """Test that entry creation trims whitespace."""
        entry = repository.create("  test  ", "  definition  ")
        
        assert entry.word == "test"
        assert entry.definition == "definition"
    
    def test_create_entry_empty_word(self, repository):
        """Test creating entry with empty word raises ValueError."""
        with pytest.raises(ValueError, match="Word cannot be empty"):
            repository.create("", "definition")
    
    def test_create_entry_empty_definition(self, repository):
        """Test creating entry with empty definition raises ValueError."""
        with pytest.raises(ValueError, match="Definition cannot be empty"):
            repository.create("word", "")
    
    def test_find_by_word_success(self, repository, db_session):
        """Test finding a word by name."""
        # Create entry first
        entry = repository.create("test", "definition")
        repository.commit()
        
        # Find it
        found = repository.find_by_word("test")
        
        assert found is not None
        assert found.word == "test"
        assert found.definition == "definition"
    
    def test_find_by_word_case_insensitive(self, repository, db_session):
        """Test finding word is case insensitive."""
        entry = repository.create("Test", "definition")
        repository.commit()
        
        # Should find with different case
        found = repository.find_by_word("test")
        assert found is not None
        assert found.word == "Test"
        
        found = repository.find_by_word("TEST")
        assert found is not None
        
        found = repository.find_by_word("TeSt")
        assert found is not None
    
    def test_find_by_word_not_found(self, repository):
        """Test finding non-existent word returns None."""
        found = repository.find_by_word("nonexistent")
        assert found is None
    
    def test_find_by_word_empty_string(self, repository):
        """Test finding with empty string returns None."""
        found = repository.find_by_word("")
        assert found is None
    
    def test_find_by_word_whitespace(self, repository):
        """Test finding with whitespace returns None."""
        found = repository.find_by_word("   ")
        assert found is None
    
    def test_commit(self, repository, db_session):
        """Test committing transaction."""
        entry = repository.create("test", "definition")
        
        # Before commit, entry might not be persisted
        repository.commit()
        
        # After commit, should be able to find it
        found = repository.find_by_word("test")
        assert found is not None
    
    def test_rollback(self, repository, db_session):
        """Test rolling back transaction."""
        entry = repository.create("test", "definition")
        repository.rollback()
        
        # After rollback, should not find it
        found = repository.find_by_word("test")
        assert found is None
    
    def test_transaction_context_manager_success(self, repository, db_session):
        """Test transaction context manager on success."""
        with repository.transaction():
            repository.create("test", "definition")
        
        # Should be committed
        found = repository.find_by_word("test")
        assert found is not None
    
    def test_transaction_context_manager_rollback_on_error(self, repository, db_session):
        """Test transaction context manager rolls back on error."""
        with pytest.raises(ValueError):
            with repository.transaction():
                repository.create("test", "definition")
                raise ValueError("Test error")
        
        # Should be rolled back
        found = repository.find_by_word("test")
        assert found is None


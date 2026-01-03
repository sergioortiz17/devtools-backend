"""Unit tests for core configuration."""
import pytest
import os
from app.core.config import Settings


class TestSettings:
    """Test cases for Settings class."""
    
    def test_default_values(self):
        """Test default configuration values."""
        settings = Settings()
        
        assert settings.DB_HOST == "localhost"
        assert settings.DB_PORT == "5432"
        assert settings.DB_NAME == "devtools"
        assert settings.APP_NAME == "DevTools Playground API"
        assert settings.APP_VERSION == "1.0.0"
    
    def test_cors_origins_list_comma_separated(self):
        """Test parsing comma-separated CORS origins."""
        settings = Settings(CORS_ORIGINS="http://localhost:3000,http://localhost:5173")
        
        origins = settings.cors_origins_list
        assert "http://localhost:3000" in origins
        assert "http://localhost:5173" in origins
        assert len(origins) == 2
    
    def test_cors_origins_list_json_array(self):
        """Test parsing JSON array CORS origins."""
        settings = Settings(CORS_ORIGINS='["http://localhost:3000", "http://localhost:5173"]')
        
        origins = settings.cors_origins_list
        assert "http://localhost:3000" in origins
        assert "http://localhost:5173" in origins
    
    def test_cors_origins_list_empty(self):
        """Test empty CORS origins."""
        settings = Settings(CORS_ORIGINS="")
        
        origins = settings.cors_origins_list
        assert origins == []
    
    def test_cors_origins_list_with_spaces(self):
        """Test CORS origins with spaces."""
        settings = Settings(CORS_ORIGINS=" http://localhost:3000 , http://localhost:5173 ")
        
        origins = settings.cors_origins_list
        assert "http://localhost:3000" in origins
        assert "http://localhost:5173" in origins
    
    def test_database_url_from_components(self):
        """Test constructing database URL from components."""
        settings = Settings(
            DB_USER="testuser",
            DB_PASSWORD="testpass",
            DB_HOST="testhost",
            DB_PORT="5433",
            DB_NAME="testdb"
        )
        
        url = settings.database_url
        assert "testuser" in url
        assert "testpass" in url
        assert "testhost" in url
        assert "5433" in url
        assert "testdb" in url
    
    def test_database_url_from_env(self):
        """Test using DATABASE_URL if provided."""
        settings = Settings(DATABASE_URL="postgresql://user:pass@host:5432/db")
        
        url = settings.database_url
        assert url == "postgresql://user:pass@host:5432/db"
    
    def test_is_sqlite_true(self):
        """Test is_sqlite property returns True for SQLite."""
        settings = Settings(DATABASE_URL="sqlite:///test.db")
        
        assert settings.is_sqlite is True
    
    def test_is_sqlite_false(self):
        """Test is_sqlite property returns False for PostgreSQL."""
        settings = Settings(DATABASE_URL="postgresql://user:pass@host:5432/db")
        
        assert settings.is_sqlite is False
    
    def test_db_max_retries_default(self):
        """Test default DB_MAX_RETRIES value."""
        settings = Settings()
        
        assert settings.DB_MAX_RETRIES == 30
        assert settings.DB_MAX_RETRIES >= 1
    
    def test_db_retry_delay_default(self):
        """Test default DB_RETRY_DELAY value."""
        settings = Settings()
        
        assert settings.DB_RETRY_DELAY == 2
        assert settings.DB_RETRY_DELAY >= 1


"""
Basic tests for JX Logger functionality.
"""

import pytest
import logging
from unittest.mock import patch, MagicMock

from jx_logger import get_logger, LogLevel, LogFormat, LogContext
from jx_logger.core import EnhancedLogger
from jx_logger.utils import SensitiveDataMasker


class TestEnhancedLogger:
    """Test the EnhancedLogger class."""
    
    def test_logger_creation(self):
        """Test basic logger creation."""
        logger = get_logger("test-logger")
        assert isinstance(logger, EnhancedLogger)
        assert logger.name == "test-logger"
    
    def test_custom_log_levels(self):
        """Test custom log levels are registered."""
        assert logging.getLevelName(LogLevel.SUCCESS.value) == "SUCCESS"
        assert logging.getLevelName(LogLevel.TRACE.value) == "TRACE"
    
    def test_log_context(self):
        """Test log context functionality."""
        logger = get_logger("context-test")
        
        context = LogContext(
            request_id="test-123",
            user_id="user-456"
        )
        
        logger.set_context(context)
        retrieved_context = logger.get_context()
        
        assert retrieved_context.request_id == "test-123"
        assert retrieved_context.user_id == "user-456"
    
    def test_sensitive_data_masking(self):
        """Test sensitive data masking functionality."""
        # Test message masking
        message = "User password is secret123"
        masked = SensitiveDataMasker.mask_message(message)
        assert "secret123" not in masked
        
        # Test data structure masking
        data = {
            "username": "john",
            "password": "secret123",
            "api_key": "sk-1234567890"
        }
        masked_data = SensitiveDataMasker.mask_data(data)
        
        assert masked_data["username"] == "john"
        assert masked_data["password"] == "[MASKED]"
        assert masked_data["api_key"] == "[MASKED]"
    
    def test_log_levels(self):
        """Test all log levels work."""
        logger = get_logger("level-test", console_output=False)
        
        # Mock the underlying logger to capture calls
        with patch.object(logger._logger, 'log') as mock_log:
            logger.trace("trace message")
            logger.debug("debug message")
            logger.info("info message")
            logger.success("success message")
            logger.warning("warning message")
            logger.error("error message")
            logger.critical("critical message")
            
            # Verify all levels were called
            assert mock_log.call_count == 7
            
            # Check specific level calls
            calls = mock_log.call_args_list
            assert calls[0][0][0] == LogLevel.TRACE.value
            assert calls[1][0][0] == LogLevel.DEBUG.value
            assert calls[2][0][0] == LogLevel.INFO.value
            assert calls[3][0][0] == LogLevel.SUCCESS.value
            assert calls[4][0][0] == LogLevel.WARNING.value
            assert calls[5][0][0] == LogLevel.ERROR.value
            assert calls[6][0][0] == LogLevel.CRITICAL.value
    
    def test_performance_monitoring(self):
        """Test performance monitoring functionality."""
        logger = get_logger("perf-test", enable_performance_monitoring=True)
        
        # Log some messages
        logger.info("test message 1")
        logger.error("test message 2")
        
        stats = logger.get_performance_stats()
        assert stats is not None
        assert "total_logs" in stats
        assert "logs_per_second" in stats
        assert "log_counts_by_level" in stats
        assert stats["total_logs"] >= 2
    
    def test_log_formats(self):
        """Test different log formats."""
        # Test each format can be created without errors
        formats = [LogFormat.JSON, LogFormat.CONSOLE, LogFormat.RICH]
        
        for fmt in formats:
            logger = get_logger(f"format-test-{fmt.value}", log_format=fmt)
            assert logger.log_format == fmt


class TestLogContext:
    """Test LogContext functionality."""
    
    def test_context_creation(self):
        """Test context creation and serialization."""
        context = LogContext(
            request_id="req-123",
            user_id="user-456",
            component="test",
            metadata={"key": "value"}
        )
        
        context_dict = context.to_dict()
        assert context_dict["request_id"] == "req-123"
        assert context_dict["user_id"] == "user-456"
        assert context_dict["component"] == "test"
        assert context_dict["metadata"]["key"] == "value"
    
    def test_context_excludes_none(self):
        """Test that None values are excluded from context."""
        context = LogContext(
            request_id="req-123",
            user_id=None,  # Should be excluded
            component="test"
        )
        
        context_dict = context.to_dict()
        assert "request_id" in context_dict
        assert "user_id" not in context_dict
        assert "component" in context_dict


class TestSensitiveDataMasker:
    """Test SensitiveDataMasker functionality."""
    
    def test_password_masking(self):
        """Test password pattern masking."""
        test_cases = [
            ("password=secret123", "password: [MASKED]"),
            ("pwd: mypassword", "pwd: [MASKED]"),
            ("API_KEY=sk-1234567890", "API_KEY: [MASKED]"),
        ]
        
        for original, expected in test_cases:
            result = SensitiveDataMasker.mask_message(original)
            assert "[MASKED]" in result
    
    def test_email_masking(self):
        """Test email masking."""
        message = "Contact us at admin@example.com"
        result = SensitiveDataMasker.mask_message(message)
        assert "admin@example.com" not in result
        assert "***@***.***" in result
    
    def test_credit_card_masking(self):
        """Test credit card number masking."""
        message = "Card number: 1234 5678 9012 3456"
        result = SensitiveDataMasker.mask_message(message)
        assert "1234 5678 9012 3456" not in result
        assert "****-****-****-****" in result
    
    def test_nested_data_masking(self):
        """Test masking of nested data structures."""
        data = {
            "user": {
                "name": "John",
                "password": "secret",
                "preferences": {
                    "api_key": "sk-123456"
                }
            },
            "public_info": "visible"
        }
        
        result = SensitiveDataMasker.mask_data(data)
        
        assert result["user"]["name"] == "John"
        assert result["user"]["password"] == "[MASKED]"
        assert result["user"]["preferences"]["api_key"] == "[MASKED]"
        assert result["public_info"] == "visible"


if __name__ == "__main__":
    pytest.main([__file__])
"""
Utility functions and classes for JX Logger.

This module contains helper functionality including data masking, performance monitoring,
and convenience functions.
"""

import inspect
import re
import threading
import time
from typing import Any, Dict, List, Optional

from .core import get_logger


class PerformanceMonitor:
    """Monitor logger performance and provide metrics."""

    def __init__(self):
        self.log_counts = {}
        self.avg_log_times = {}
        self.start_time = time.time()
        self._lock = threading.Lock()

    def record_log(self, level: str, duration: float):
        """Record logging operation for performance tracking."""
        with self._lock:
            if level not in self.log_counts:
                self.log_counts[level] = 0
                self.avg_log_times[level] = 0.0

            count = self.log_counts[level]
            self.avg_log_times[level] = (self.avg_log_times[level] * count + duration) / (count + 1)
            self.log_counts[level] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        with self._lock:
            uptime = time.time() - self.start_time
            total_logs = sum(self.log_counts.values())
            return {
                "uptime_seconds": uptime,
                "total_logs": total_logs,
                "logs_per_second": total_logs / uptime if uptime > 0 else 0,
                "log_counts_by_level": self.log_counts.copy(),
                "average_log_times": self.avg_log_times.copy(),
            }


class SensitiveDataMasker:
    """Automatically mask sensitive data in log messages."""

    SENSITIVE_PATTERNS = [
        (
            re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
            "****-****-****-****",
        ),  # Credit cards
        (
            re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
            "***@***.***",
        ),  # Emails
        (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "***-**-****"),  # SSN
        (
            re.compile(
                r'(?i)(password|pwd|secret|token|key|api[_-]?key)[\s]*[:=][\s]*["\']?([^"\'\s]+)["\']?'
            ),
            r"\1: [MASKED]",
        ),  # Password/token patterns
        (
            re.compile(r"\b(?:[A-Za-z0-9+/]{32,})(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)\b"),
            "[ENCODED_DATA]",
        ),  # Base64 (minimum 32 chars)
    ]

    SENSITIVE_KEYS = {
        "password",
        "pwd",
        "secret",
        "token",
        "key",
        "api_key",
        "auth",
        "authorization",
        "credential",
        "passwd",
        "pass",
        "private_key",
        "access_token",
        "refresh_token",
    }

    @classmethod
    def mask_message(cls, message: str) -> str:
        """Mask sensitive data in log message."""
        for pattern, replacement in cls.SENSITIVE_PATTERNS:
            message = pattern.sub(replacement, message)
        return message

    @classmethod
    def mask_data(cls, data: Any) -> Any:
        """Recursively mask sensitive data in dictionaries and objects."""
        if isinstance(data, dict):
            return {
                k: "[MASKED]" if k.lower() in cls.SENSITIVE_KEYS else cls.mask_data(v)
                for k, v in data.items()
            }
        elif isinstance(data, (list, tuple)):
            return type(data)(cls.mask_data(item) for item in data)
        elif isinstance(data, str):
            return cls.mask_message(data)
        return data


# Convenience functions for backward compatibility and ease of use
def debug(message: str, *args, **kwargs):
    """Log debug message using default logger."""
    get_logger().debug(message, *args, **kwargs)


def info(message: str, *args, **kwargs):
    """Log info message using default logger."""
    get_logger().info(message, *args, **kwargs)


def warning(message: str, *args, **kwargs):
    """Log warning message using default logger."""
    get_logger().warning(message, *args, **kwargs)


def error(message: str, *args, **kwargs):
    """Log error message using default logger."""
    get_logger().error(message, *args, **kwargs)


def critical(message: str, *args, **kwargs):
    """Log critical message using default logger."""
    get_logger().critical(message, *args, **kwargs)


def exception(message: str, *args, **kwargs):
    """Log exception message using default logger."""
    get_logger().exception(message, *args, **kwargs)


def success(message: str, *args, **kwargs):
    """Log success message using default logger."""
    get_logger().success(message, *args, **kwargs)


def trace(message: str, *args, **kwargs):
    """Log trace message using default logger."""
    get_logger().trace(message, *args, **kwargs)


def log_params(params: Dict[str, Any], mask_keys: Optional[List[str]] = None):
    """Log function parameters with optional masking."""
    if mask_keys:
        params = {k: "[MASKED]" if k in mask_keys else v for k, v in params.items()}

    caller_name = inspect.currentframe().f_back.f_code.co_name
    get_logger().debug(
        f"Function {caller_name} called with parameters", extra={"parameters": params}
    )

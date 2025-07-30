"""
JX Logger - A Modern, High-Performance Python Logger

A comprehensive logging solution with Rich formatting, async support,
contextual information tracking, and advanced features.

Author: JX
License: MIT
"""

from .core import (
    EnhancedLogger,
    LogContext,
    LogFormat,
    LogLevel,
    get_logger,
    set_global_context,
    with_context,
)
from .utils import critical, debug, error, exception, info, log_params, success, warning

__version__ = "1.0.0"
__author__ = "JX"
__email__ = "jx@example.com"
__description__ = "A modern, high-performance Python logger with Rich formatting and advanced features"

__all__ = [
    # Core classes
    "EnhancedLogger",
    "LogLevel",
    "LogFormat",
    "LogContext",
    # Main functions
    "get_logger",
    "set_global_context",
    "with_context",
    # Convenience functions
    "debug",
    "info",
    "warning",
    "error",
    "critical",
    "exception",
    "success",
    "log_params",
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__description__",
]

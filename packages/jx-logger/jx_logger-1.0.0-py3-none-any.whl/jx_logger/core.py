"""
Core logger implementation for JX Logger.

This module contains the main EnhancedLogger class and related core functionality.
"""

import asyncio
import contextvars
import inspect
import logging
import logging.handlers
import os
import time
from dataclasses import asdict, dataclass
from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, Optional

# Check for optional dependencies
try:
    from rich.console import Console
    from rich.traceback import install

    RICH_AVAILABLE = True
    install(show_locals=True)
except ImportError:
    RICH_AVAILABLE = False


class LogLevel(Enum):
    """Enhanced log levels with additional semantic meaning."""

    TRACE = 5
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class LogFormat(Enum):
    """Supported log output formats."""

    JSON = "json"
    CONSOLE = "console"
    STRUCTURED = "structured"
    RICH = "rich"


@dataclass
class LogContext:
    """Contextual information for log entries."""

    request_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    component: Optional[str] = None
    operation: Optional[str] = None
    correlation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}


# Register custom log levels with Python's logging system
logging.addLevelName(LogLevel.TRACE.value, "TRACE")
logging.addLevelName(LogLevel.SUCCESS.value, "SUCCESS")


class EnhancedLogger:
    """
    The Ultimate Python Logger with modern features.

    Features:
    - Structured JSON logging
    - Async logging support
    - Contextual information
    - Performance monitoring
    - Sensitive data masking
    - Rich console output
    - Multiple output formats
    """

    # Context variables for async-safe context propagation
    _request_context: contextvars.ContextVar = contextvars.ContextVar(
        "request_context", default=LogContext()
    )

    def __init__(
        self,
        name: str = "jx-logger",
        level: str | int = "INFO",
        log_format: LogFormat = LogFormat.JSON,
        log_file: Optional[str] = None,
        console_output: bool = True,
        async_logging: bool = True,
        max_file_size: int = 50 * 1024 * 1024,  # 50MB
        backup_count: int = 5,
        enable_performance_monitoring: bool = True,
        mask_sensitive_data: bool = True,
    ):
        self.name = name
        self.level = level
        self.log_format = log_format
        self.log_file = log_file
        self.console_output = console_output
        self.async_logging = async_logging
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        self.enable_performance_monitoring = enable_performance_monitoring
        self.mask_sensitive_data = mask_sensitive_data

        # Import here to avoid circular imports
        from .utils import PerformanceMonitor

        # Initialize components
        self.performance_monitor = PerformanceMonitor() if enable_performance_monitoring else None
        self._handlers = []
        self._logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup the logger with configured handlers and formatters."""
        # Import here to avoid circular imports
        from .formatters import EnhancedJSONFormatter
        from .handlers import AsyncLogHandler, ColorizedRichHandler

        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.handlers.clear()  # Clear existing handlers

        # Setup console handler
        if self.console_output:
            if RICH_AVAILABLE and self.log_format == LogFormat.RICH:
                console_handler = ColorizedRichHandler(
                    console=Console(stderr=True, force_terminal=True),
                    show_time=True,
                    show_level=True,
                    show_path=False,  # Hide file paths for cleaner output
                    markup=True,
                    rich_tracebacks=True,
                    tracebacks_show_locals=False,  # Reduce verbosity
                )
                # Rich handler manages its own formatting, don't add a custom formatter
            else:
                console_handler = logging.StreamHandler()
                # Set formatter based on format preference for non-Rich handlers
                if self.log_format == LogFormat.JSON:
                    console_handler.setFormatter(EnhancedJSONFormatter())
                elif self.log_format == LogFormat.CONSOLE:
                    console_handler.setFormatter(
                        logging.Formatter(
                            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
                        )
                    )

            console_handler.setLevel(self.level)

            if self.async_logging:
                console_handler = AsyncLogHandler(console_handler)

            logger.addHandler(console_handler)
            self._handlers.append(console_handler)

        # Setup file handler
        if self.log_file:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

            file_handler = logging.handlers.RotatingFileHandler(
                self.log_file,
                maxBytes=self.max_file_size,
                backupCount=self.backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(self.level)
            file_handler.setFormatter(EnhancedJSONFormatter())

            if self.async_logging:
                file_handler = AsyncLogHandler(file_handler)

            logger.addHandler(file_handler)
            self._handlers.append(file_handler)

        return logger

    def set_context(self, context: LogContext):
        """Set logging context for current async task or thread."""
        self._request_context.set(context)

    def get_context(self) -> LogContext:
        """Get current logging context."""
        return self._request_context.get()

    def _log_with_context(self, level: int, message: str, *args, **kwargs):
        """Internal method to log with context and performance monitoring."""
        # Import here to avoid circular imports
        from .utils import SensitiveDataMasker

        start_time = time.time()

        # Mask sensitive data if enabled
        if self.mask_sensitive_data:
            message = SensitiveDataMasker.mask_message(message)
            kwargs = SensitiveDataMasker.mask_data(kwargs)

        # Add context to log record
        context = self.get_context()
        extra = kwargs.pop("extra", {})
        extra["context"] = context

        # Add caller information
        frame = inspect.currentframe()
        if frame and frame.f_back and frame.f_back.f_back:
            caller_frame = frame.f_back.f_back
            extra.update(
                {
                    "caller_file": caller_frame.f_code.co_filename,
                    "caller_function": caller_frame.f_code.co_name,
                    "caller_line": caller_frame.f_lineno,
                }
            )

        # Log the message
        self._logger.log(level, message, *args, extra=extra, **kwargs)

        # Record performance metrics
        if self.performance_monitor:
            duration = time.time() - start_time
            level_name = logging.getLevelName(level)
            self.performance_monitor.record_log(level_name, duration)

    def trace(self, message: str, *args, **kwargs):
        """Log trace level message."""
        self._log_with_context(LogLevel.TRACE.value, message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs):
        """Log debug level message."""
        self._log_with_context(LogLevel.DEBUG.value, message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info level message."""
        self._log_with_context(LogLevel.INFO.value, message, *args, **kwargs)

    def success(self, message: str, *args, **kwargs):
        """Log success level message."""
        self._log_with_context(LogLevel.SUCCESS.value, message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning level message."""
        self._log_with_context(LogLevel.WARNING.value, message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log error level message."""
        self._log_with_context(LogLevel.ERROR.value, message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log critical level message."""
        self._log_with_context(LogLevel.CRITICAL.value, message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs):
        """Log exception with traceback."""
        kwargs["exc_info"] = True
        self.error(message, *args, **kwargs)

    def log_function_call(self, func: Callable) -> Callable:
        """Decorator to automatically log function calls with parameters."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Import here to avoid circular imports
            from .utils import SensitiveDataMasker

            func_name = func.__name__
            # Mask sensitive parameters
            safe_kwargs = (
                SensitiveDataMasker.mask_data(kwargs) if self.mask_sensitive_data else kwargs
            )

            self.debug(f"Calling {func_name} with args={len(args)} kwargs={safe_kwargs}")

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                self.debug(f"Function {func_name} completed successfully in {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                self.exception(f"Function {func_name} failed after {duration:.3f}s: {str(e)}")
                raise

        return wrapper

    async def alog(self, level: int, message: str, *args, **kwargs):
        """Async-friendly logging method."""
        await asyncio.get_event_loop().run_in_executor(
            None, self._log_with_context, level, message, *args, **kwargs
        )

    async def ainfo(self, message: str, *args, **kwargs):
        """Async info logging."""
        await self.alog(LogLevel.INFO.value, message, *args, **kwargs)

    async def aerror(self, message: str, *args, **kwargs):
        """Async error logging."""
        await self.alog(LogLevel.ERROR.value, message, *args, **kwargs)

    async def adebug(self, message: str, *args, **kwargs):
        """Async debug logging."""
        await self.alog(LogLevel.DEBUG.value, message, *args, **kwargs)

    async def asuccess(self, message: str, *args, **kwargs):
        """Async success logging."""
        await self.alog(LogLevel.SUCCESS.value, message, *args, **kwargs)

    def get_performance_stats(self) -> Optional[Dict[str, Any]]:
        """Get performance statistics if monitoring is enabled."""
        return self.performance_monitor.get_stats() if self.performance_monitor else None

    def create_child_logger(self, suffix: str) -> "EnhancedLogger":
        """Create a child logger with the same configuration."""
        child_name = f"{self.name}.{suffix}"
        return EnhancedLogger(
            name=child_name,
            level=self.level,
            log_format=self.log_format,
            log_file=self.log_file.replace(self.name, child_name) if self.log_file else None,
            console_output=self.console_output,
            async_logging=self.async_logging,
            max_file_size=self.max_file_size,
            backup_count=self.backup_count,
            enable_performance_monitoring=self.enable_performance_monitoring,
            mask_sensitive_data=self.mask_sensitive_data,
        )

    def close(self):
        """Clean shutdown of logger and all handlers."""
        for handler in self._handlers:
            if hasattr(handler, "close"):
                handler.close()


# Global logger instance
_default_logger: Optional[EnhancedLogger] = None


def get_logger(name: str = "jx-logger", **kwargs) -> EnhancedLogger:
    """Get or create a logger instance."""
    global _default_logger

    if _default_logger is None or _default_logger.name != name:
        # Determine log file path
        log_file = kwargs.get("log_file")
        if log_file is None:
            logs_dir = os.environ.get("LOG_PATH", "logs")
            os.makedirs(logs_dir, exist_ok=True)
            log_file = os.path.join(logs_dir, f"{name}.jsonl")

        # Set defaults from environment
        kwargs.setdefault("level", os.environ.get("LOG_LEVEL", "INFO"))
        kwargs.setdefault("log_file", log_file)
        kwargs.setdefault(
            "async_logging", os.environ.get("ASYNC_LOGGING", "true").lower() == "true"
        )

        # Handle parameter name variations for backward compatibility
        if "enable_file_logging" in kwargs:
            if kwargs["enable_file_logging"] and "log_file" not in kwargs:
                kwargs["log_file"] = log_file
            kwargs.pop("enable_file_logging")

        # Remove configuration parameters that don't belong to EnhancedLogger
        config_only_params = [
            "environment",
            "log_directory",
            "file_rotation_interval",
            "console_level",
            "queue_size",
            "sensitive_keys",
            "enable_filtering",
            "filter_modules",
            "filter_functions",
            "include_caller_info",
            "include_thread_info",
            "include_process_info",
            "structured_logging",
            "enable_rich_output",
            "enable_correlation_id",
            "enable_metrics",
            "metrics_interval",
            "enable_health_check",
        ]

        for param in config_only_params:
            kwargs.pop(param, None)

        _default_logger = EnhancedLogger(name=name, **kwargs)

    return _default_logger


def with_context(**context_kwargs) -> Callable:
    """Decorator to set logging context for a function."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create context from decorator arguments
            context = LogContext(**context_kwargs)

            # Set context for this execution
            token = get_logger()._request_context.set(context)
            try:
                return func(*args, **kwargs)
            finally:
                get_logger()._request_context.reset(token)

        return wrapper

    return decorator


def set_global_context(context: LogContext):
    """Set global logging context."""
    get_logger().set_context(context)

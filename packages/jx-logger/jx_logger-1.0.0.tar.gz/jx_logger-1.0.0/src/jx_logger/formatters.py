"""
Custom formatters for JX Logger.

This module contains specialized formatters for different output formats.
"""

import json
import logging
from datetime import datetime, timezone
from .utils import SensitiveDataMasker
from .core import LogContext


class EnhancedJSONFormatter(logging.Formatter):
    """Enhanced JSON formatter with structured output and contextual information."""
    
    def __init__(self, include_extra: bool = True):
        super().__init__()
        self.include_extra = include_extra
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON."""
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "thread": record.thread,
            "thread_name": record.threadName,
            "process": record.process,
        }
        
        # Add exception information if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info)
            }
        
        # Add contextual information
        context = getattr(record, 'context', None)
        if context and isinstance(context, LogContext):
            log_entry["context"] = context.to_dict()
        
        # Add extra fields
        if self.include_extra:
            extra = {k: v for k, v in record.__dict__.items() 
                    if k not in logging.LogRecord(
                        name="", level=0, pathname="", lineno=0, 
                        msg="", args=(), exc_info=None
                    ).__dict__ and k != 'context'}
            if extra:
                log_entry["extra"] = SensitiveDataMasker.mask_data(extra)
        
        return json.dumps(log_entry, default=str, ensure_ascii=False)


class StructuredFormatter(logging.Formatter):
    """Structured formatter for human-readable console output."""
    
    def __init__(self, include_context: bool = True):
        super().__init__()
        self.include_context = include_context
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured text."""
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        # Build the base message
        message = f"[{timestamp}] {record.levelname:8} {record.getMessage()}"
        
        # Add context if available and enabled
        if self.include_context:
            context = getattr(record, 'context', None)
            if context and isinstance(context, LogContext):
                context_str = " | ".join([f"{k}={v}" for k, v in context.to_dict().items()])
                if context_str:
                    message += f" | {context_str}"
        
        # Add location info
        message += f" ({record.module}:{record.funcName}:{record.lineno})"
        
        return message
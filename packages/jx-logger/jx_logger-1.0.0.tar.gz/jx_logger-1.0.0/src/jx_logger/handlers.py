"""
Custom logging handlers for JX Logger.

This module contains specialized handlers including Rich formatting and async support.
"""

import logging
import queue
import threading

# Optional Rich dependency
try:
    from rich.console import Console
    from rich.logging import RichHandler
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    RichHandler = None


class ColorizedRichHandler(RichHandler):
    """Custom RichHandler with colors for custom log levels and clean formatting."""
    
    def __init__(self, *args, **kwargs):
        if not RICH_AVAILABLE:
            raise ImportError("Rich library is required for ColorizedRichHandler. Install with: pip install rich")
        super().__init__(*args, **kwargs)
        
    def get_level_text(self, record):
        """Override to add custom colors for SUCCESS level."""
        level_name = record.levelname
        if level_name == "SUCCESS":
            return f"[bold green]✓ {level_name}[/bold green]"
        elif level_name == "INFO":
            return f"[bold blue]ℹ {level_name}[/bold blue]"
        elif level_name == "WARNING":
            return f"[bold yellow]⚠ {level_name}[/bold yellow]"
        elif level_name == "ERROR":
            return f"[bold red]✗ {level_name}[/bold red]"
        elif level_name == "CRITICAL":
            return f"[bold red on white]🚨 {level_name}[/bold red on white]"
        elif level_name == "DEBUG":
            return f"[dim]🔍 {level_name}[/dim]"
        elif level_name == "TRACE":
            return f"[dim cyan]🔬 {level_name}[/dim cyan]"
        else:
            return f"[bold]{level_name}[/bold]"


class AsyncLogHandler(logging.Handler):
    """Asynchronous log handler using queue for non-blocking operations."""
    
    def __init__(self, target_handler: logging.Handler, queue_size: int = 1000):
        super().__init__()
        self.target_handler = target_handler
        self.log_queue = queue.Queue(maxsize=queue_size)
        self._stop_event = threading.Event()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
    
    def _worker(self):
        """Worker thread to process log records asynchronously."""
        while not self._stop_event.is_set():
            try:
                record = self.log_queue.get(timeout=1.0)
                if record is None:  # Sentinel value to stop
                    break
                self.target_handler.emit(record)
                self.log_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                # Fallback to stderr to avoid infinite recursion
                print(f"Error in async log handler: {e}", file=__import__('sys').stderr)
    
    def emit(self, record: logging.LogRecord):
        """Emit log record asynchronously."""
        try:
            self.log_queue.put_nowait(record)
        except queue.Full:
            # Drop the log message if queue is full to prevent blocking
            pass
    
    def close(self):
        """Clean shutdown of async handler."""
        self._stop_event.set()
        self.log_queue.put(None)  # Sentinel value
        self.worker_thread.join(timeout=5.0)
        self.target_handler.close()
        super().close()
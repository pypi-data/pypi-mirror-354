# JX Logger 🚀

A modern, high-performance Python logger with Rich formatting, async support, and advanced features.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ Features

- 🎨 **Rich Console Output** - Beautiful, colorized logs with emojis and clean formatting
- ⚡ **Async Logging** - Non-blocking logging with queue-based architecture
- 🏗️ **Structured JSON Logging** - Machine-readable logs for better parsing and analysis
- 🔐 **Automatic Data Masking** - Protects sensitive information (passwords, tokens, etc.)
- 📊 **Performance Monitoring** - Built-in metrics and performance tracking
- 🔍 **Contextual Information** - Request IDs, user context, and correlation tracking
- 🎯 **Custom Log Levels** - SUCCESS and TRACE levels with visual indicators
- 🔄 **Multiple Output Formats** - JSON, Rich, Console, and Structured formats
- 🎭 **Easy Integration** - Drop-in replacement for standard Python logging

## 🚀 Quick Start

### Installation

```bash
pip install jx-logger
```

For Rich console features:
```bash
pip install jx-logger[rich]
```

### Basic Usage

```python
from jx_logger import get_logger

# Get a logger instance
logger = get_logger("my-app")

# Log messages with beautiful formatting
logger.info("🚀 Application starting")
logger.success("✅ Database connected successfully")
logger.warning("⚠️ High memory usage detected")
logger.error("❌ Failed to process request")
```

### Rich Console Output

```python
from jx_logger import get_logger, LogFormat

# Create logger with Rich formatting
logger = get_logger(
    name="my-app",
    log_format=LogFormat.RICH,
    level="DEBUG"
)

logger.info("Starting application")
logger.success("Operation completed successfully")
logger.debug("Debug information")
logger.error("Something went wrong")
```

## 📖 Documentation

### Log Levels

JX Logger includes standard Python log levels plus custom levels:

| Level | Icon | Color | Usage |
|-------|------|-------|-------|
| `TRACE` | 🔬 | Dim Cyan | Detailed debugging |
| `DEBUG` | 🔍 | Dim | Development debugging |
| `INFO` | ℹ️ | Blue | General information |
| `SUCCESS` | ✅ | Green | Successful operations |
| `WARNING` | ⚠️ | Yellow | Warning messages |
| `ERROR` | ❌ | Red | Error conditions |
| `CRITICAL` | 🚨 | Red on White | Critical failures |

### Configuration Options

```python
from jx_logger import get_logger, LogFormat

logger = get_logger(
    name="my-app",                           # Logger name
    level="INFO",                            # Log level
    log_format=LogFormat.RICH,               # Output format
    log_file="logs/app.jsonl",               # Log file path
    console_output=True,                     # Enable console output
    async_logging=True,                      # Enable async logging
    max_file_size=50*1024*1024,             # 50MB file rotation
    backup_count=5,                          # Keep 5 backup files
    enable_performance_monitoring=True,       # Track performance
    mask_sensitive_data=True                 # Mask sensitive data
)
```

### Output Formats

#### Rich Format (Recommended)
Beautiful console output with colors and emojis:
```
[2024-01-15 10:30:15] ✅ SUCCESS Database connection established
[2024-01-15 10:30:16] ℹ️  INFO    Processing 1,234 records
[2024-01-15 10:30:17] ⚠️  WARNING High memory usage: 85%
```

#### JSON Format
Structured logging for machine parsing:
```json
{
  "timestamp": "2024-01-15T10:30:15.123Z",
  "level": "INFO",
  "logger": "my-app",
  "message": "Processing request",
  "context": {"request_id": "req_123", "user_id": "user_456"}
}
```

### Contextual Logging

```python
from jx_logger import get_logger, LogContext

logger = get_logger("my-app")

# Set context for all subsequent logs
context = LogContext(
    request_id="req_123",
    user_id="user_456",
    component="auth"
)
logger.set_context(context)

logger.info("User authenticated")  # Will include context

# Use decorator for function-level context
@logger.log_function_call
def process_payment(amount):
    logger.info(f"Processing payment of ${amount}")
    return True
```

### Async Logging

```python
import asyncio
from jx_logger import get_logger

async def main():
    logger = get_logger("async-app", async_logging=True)
    
    # Async logging methods
    await logger.ainfo("Async operation started")
    await logger.aerror("Async operation failed")
    
asyncio.run(main())
```

### Performance Monitoring

```python
logger = get_logger("my-app", enable_performance_monitoring=True)

# Log some messages
logger.info("Operation 1")
logger.error("Operation 2") 
logger.debug("Operation 3")

# Get performance statistics
stats = logger.get_performance_stats()
print(f"Total logs: {stats['total_logs']}")
print(f"Logs per second: {stats['logs_per_second']:.2f}")
print(f"Average log times: {stats['average_log_times']}")
```

### Sensitive Data Masking

JX Logger automatically masks sensitive information:

```python
logger.info("User login", extra={
    "username": "john_doe",
    "password": "secret123",      # Automatically masked
    "api_key": "sk-1234567890"    # Automatically masked
})

# Logs: User login {"username": "john_doe", "password": "[MASKED]", "api_key": "[MASKED]"}
```

## 🔧 Advanced Usage

### Custom Formatters

```python
from jx_logger.formatters import StructuredFormatter

logger = get_logger("my-app")
handler = logging.StreamHandler()
handler.setFormatter(StructuredFormatter(include_context=True))
```

### Multiple Loggers

```python
# Create specialized loggers
db_logger = get_logger("myapp.database")
api_logger = get_logger("myapp.api")
auth_logger = get_logger("myapp.auth")

# Each can have different configurations
db_logger.set_context(LogContext(component="database"))
api_logger.set_context(LogContext(component="api"))
```

### Integration with Existing Code

JX Logger provides convenience functions that work as drop-in replacements:

```python
from jx_logger import info, error, warning, success

# Use anywhere in your code
info("Application started")
success("Database connected")
warning("Cache miss")
error("Connection failed")
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=jx_logger

# Run specific test categories
pytest -m "not slow"  # Skip slow tests
pytest -m integration # Run only integration tests
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋 Support

- 📖 **Documentation**: Check this README and code examples
- 🐛 **Bug Reports**: [Open an issue](https://github.com/jx/jx-logger/issues)
- 💡 **Feature Requests**: [Open an issue](https://github.com/jx/jx-logger/issues)
- 💬 **Questions**: [Start a discussion](https://github.com/jx/jx-logger/discussions)

## 🏆 Why JX Logger?

| Feature | Standard Logging | JX Logger |
|---------|------------------|-----------|
| **Rich Output** | ❌ Plain text | ✅ Colors, emojis, formatting |
| **Async Support** | ❌ Blocking | ✅ Non-blocking queue-based |
| **Data Masking** | ❌ Manual | ✅ Automatic |
| **Performance Monitoring** | ❌ None | ✅ Built-in metrics |
| **Contextual Info** | ❌ Limited | ✅ Rich context tracking |
| **Custom Levels** | ❌ Basic | ✅ SUCCESS, TRACE + icons |
| **JSON Structured** | ❌ Manual setup | ✅ Built-in |
| **Easy Setup** | ⚠️ Complex | ✅ One-liner |

---

Made with ❤️ by JX
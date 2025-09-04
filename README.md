# py-utils

A comprehensive collection of Python utility functions and helpers designed to be reusable across multiple projects. Built with modern Python practices and extensive test coverage.

## Features

- **Logger**: Pre-configured logging with consistent formatting, file output, and timestamp tracking
- **EmailHelper**: SMTP email sending with TLS support, authentication, and HTML content
- **Housekeeper**: File system housekeeping with age-based and count-based cleanup
- **Comprehensive Testing**: Full test suite with 30+ tests covering all functionality
- **Modern Python**: Built with Python 3.13+ and uv package manager
- **Type Hints**: Full type annotation support for better IDE experience

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone git@github.com:RomiSugianto/py-utils.git
cd py-utils

# Install dependencies and the package
uv sync
```

### Manual Installation

```bash
# Build and install the package
uv build
uv pip install .
```

## Usage

### Logger Helper

```python
from py_utils.logger import Logger, get_logger

# Quick setup with default configuration
logger = get_logger("my_app")
logger.info("Application started")

# Advanced setup with file logging
logger = Logger.setup_logger(
    name="my_app",
    level=logging.DEBUG,
    log_file="logs/app.log"
)
logger.debug("Debug message")
logger.error("Error occurred")
```

### Email Helper

```python
from py_utils.email_helper import EmailHelper, send_quick_email

# Quick email sending
send_quick_email(
    smtp_server="smtp.gmail.com",
    from_addr="sender@example.com",
    to_addr="recipient@example.com",
    subject="Test Email",
    body="This is a test message",
    username="your_username",
    password="your_password",
    use_tls=True
)

# Advanced usage with manual setup
server = EmailHelper.setup_smtp(
    "smtp.gmail.com", 465,
    username="your_username",
    password="your_password",
    use_tls=True
)

EmailHelper.send_email(
    server=server,
    from_addr="sender@example.com",
    to_addr="recipient@example.com",
    subject="HTML Email",
    body="Plain text version",
    html_body="<h1>HTML Version</h1>"
)
```

### Housekeeper Helper

```python
from py_utils.housekeeper import Housekeeper, cleanup_directory

# Delete files older than 7 days
deleted_count = Housekeeper.housekeep_by_age(
    directory="/path/to/logs",
    days_old=7,
    confirm=False  # Set to True for interactive confirmation
)

# Keep only the 10 newest files
deleted_count = Housekeeper.housekeep_by_count(
    directory="/path/to/backups",
    keep_count=10,
    confirm=False
)

# Convenience function
cleanup_directory("/path/to/temp", days_old=1)  # Delete files older than 1 day
cleanup_directory("/path/to/cache", keep_count=50)  # Keep 50 newest files
```

## Testing

The project includes comprehensive test coverage with 30+ tests. Run tests using uv:

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_logger.py

# Run with verbose output
uv run pytest -v

# Run with coverage report
uv run pytest --cov=py_utils --cov-report=html
```

### Test Coverage

- **Logger Tests**: Logger setup, file handling, log levels, formatting
- **Email Tests**: SMTP setup, authentication, TLS, error handling
- **Housekeeper Tests**: File deletion by age/count, error scenarios, edge cases

## Project Structure

```
py-utils/
├── py_utils/
│   ├── __init__.py
│   ├── logger.py          # Logger class and utilities
│   ├── email_helper.py    # EmailHelper class for SMTP
│   └── housekeeper.py     # Housekeeper class for file cleanup
├── tests/
│   ├── test_logger.py     # Logger tests (8 tests)
│   ├── test_email_helper.py   # Email tests (10 tests)
│   └── test_housekeeper.py    # Housekeeper tests (12 tests)
├── main.py
├── pyproject.toml         # Project configuration with pytest setup
├── README.md
├── uv.lock               # uv dependency lock file
└── LICENSE
```

## Development

### Adding New Helpers

1. Create a new file in `py_utils/` directory
2. Follow the naming convention: `{helper_name}_helper.py`
3. Implement a class with static methods (like `LoggerHelper`, `EmailHelper`)
4. Add comprehensive tests in `tests/test_{helper_name}_helper.py`
5. Update this README with usage examples

### Code Quality

- All code includes type hints
- Comprehensive error handling
- Follows PEP 8 style guidelines
- 100% test coverage for all helpers

## Dependencies

- **Runtime**: None (pure Python)
- **Development**: pytest>=8.4.1 for testing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `uv run pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

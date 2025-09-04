"""
py-utils - A comprehensive collection of Python utility functions and helpers.

This package provides reusable utilities for common programming tasks including:
- Logging helpers with file output and formatting
- Email helpers for SMTP sending with TLS support
- File housekeeping helpers for cleanup operations
"""

# Logger utilities
from .logger import Logger, get_logger

# Email utilities
from .email_helper import EmailHelper, send_quick_email

# Housekeeper utilities
from .housekeeper import Housekeeper, cleanup_directory

__version__ = "0.1.0"
__all__ = [
    # Logger
    "Logger",
    "get_logger",
    # Email
    "EmailHelper",
    "send_quick_email",
    # Housekeeper
    "Housekeeper",
    "cleanup_directory",
]

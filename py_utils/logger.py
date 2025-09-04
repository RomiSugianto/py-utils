import logging
import os
from datetime import datetime
from typing import Optional

class Logger:
    """A helper class for setting up consistent logging across projects."""

    @staticmethod
    def setup_logger(
        name: str = "app",
        level: int = logging.INFO,
        log_file: Optional[str] = None,
        format_string: str = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    ) -> logging.Logger:
        """
        Set up a logger with consistent formatting and file output.

        Args:
            name: Logger name
            level: Logging level (default: INFO)
            log_file: Optional log file path. If None, logs to console only
            format_string: Log format string

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Remove existing handlers to avoid duplicates
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Create formatter
        formatter = logging.Formatter(format_string)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (if specified)
        if log_file:
            # Create log directory if it doesn't exist
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    @staticmethod
    def get_default_log_file(base_dir: Optional[str] = None) -> str:
        """
        Generate a default log file path with timestamp.

        Args:
            base_dir: Base directory for logs (default: current directory)

        Returns:
            Path to log file
        """
        if base_dir is None:
            base_dir = os.getcwd()

        timestamp = datetime.now().strftime("%Y%m%d")
        return os.path.join(base_dir, "logs", f"app_{timestamp}.log")

# Convenience function for quick setup
def get_logger(name: str = "app", log_file: Optional[str] = None) -> logging.Logger:
    """
    Quick function to get a pre-configured logger.

    Args:
        name: Logger name
        log_file: Optional log file path

    Returns:
        Configured logger
    """
    if log_file is None:
        log_file = Logger.get_default_log_file()

    return Logger.setup_logger(name=name, log_file=log_file)

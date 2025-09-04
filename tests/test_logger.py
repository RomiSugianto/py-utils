import logging
from py_utils.logger import Logger, get_logger


class TestLogger:
    """Test cases for Logger class."""

    def test_setup_logger_console_only(self):
        """Test setting up logger with console handler only."""
        logger = Logger.setup_logger(name="test_logger")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO

        # Check handlers
        handlers = logger.handlers
        assert len(handlers) == 1
        assert isinstance(handlers[0], logging.StreamHandler)

    def test_setup_logger_with_file(self, tmp_path):
        """Test setting up logger with both console and file handlers."""
        log_file = tmp_path / "test.log"
        logger = Logger.setup_logger(
            name="test_logger",
            log_file=str(log_file)
        )
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"

        # Check handlers
        handlers = logger.handlers
        assert len(handlers) == 2

        # Should have both StreamHandler and FileHandler
        handler_types = [type(h) for h in handlers]
        assert logging.StreamHandler in handler_types
        assert logging.FileHandler in handler_types

    def test_setup_logger_custom_level(self):
        """Test setting up logger with custom logging level."""
        logger = Logger.setup_logger(name="test_logger", level=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_get_default_log_file(self, tmp_path):
        """Test generating default log file path."""
        base_dir = str(tmp_path)
        log_file = Logger.get_default_log_file(base_dir)

        # Should create logs directory and file with timestamp
        assert "logs" in log_file
        assert log_file.startswith(base_dir)
        assert "app_" in log_file
        assert ".log" in log_file


def test_get_logger():
    """Test the convenience function get_logger."""
    logger = get_logger("convenience_test")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "convenience_test"
    assert logger.level == logging.INFO


def test_logger_functionality(caplog):
    """Test that logger actually logs messages."""
    logger = get_logger("test_logging")
    test_message = "This is a test message"

    with caplog.at_level(logging.INFO):
        logger.info(test_message)

    assert test_message in caplog.text


def test_logger_levels(caplog):
    """Test different logging levels."""
    logger = get_logger("test_levels")

    with caplog.at_level(logging.DEBUG):
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

    # Note: Debug message won't appear because logger level is INFO by default
    # Only test the levels that should be captured
    assert "Info message" in caplog.text
    assert "Warning message" in caplog.text
    assert "Error message" in caplog.text


def test_log_file_creation(tmp_path):
    """Test that log files are created when specified."""
    log_file = tmp_path / "test.log"
    logger = Logger.setup_logger("file_test", log_file=str(log_file))

    logger.info("Test message")

    # Check that file was created and contains the message
    assert log_file.exists()
    with open(log_file, 'r') as f:
        content = f.read()
        assert "Test message" in content
        assert "file_test" in content  # Logger name should be in log

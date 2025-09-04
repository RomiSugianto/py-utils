from py_utils import get_logger

def main():
    # Get a pre-configured logger
    logger = get_logger()

    logger.info("Hello from py-utils!")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    # Example with custom name
    custom_logger = get_logger("my_module")
    custom_logger.info("Logging from my_module")


if __name__ == "__main__":
    main()

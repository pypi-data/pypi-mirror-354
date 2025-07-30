import logging
import os
import colorlog
import re

LOGS_PATH = "./logs/"

class BoldMarkedTextFormatter(colorlog.ColoredFormatter):
    def __init__(self, fmt, log_colors):
        super().__init__(fmt, log_colors=log_colors)
        # Regex to match text between **, capturing the content inside
        self.pattern = re.compile(r'\*\*(.*?)\*\*')

    def format(self, record):
        # Get the original formatted message
        message = super().format(record)
        
        if message is None:
            return ""
            
        # Replace **text** with bolded text but preserve color by only turning off bold
        def replace_bold(match):
            # \033[1m - Turn on bold
            # \033[22m - Turn off bold (without resetting color)
            return f"\033[1m{match.group(1)}\033[22m"
            
        # Apply the replacement
        message = self.pattern.sub(replace_bold, message)
        return message

def setup_logger(process_id:str, logger_level: int = logging.INFO) -> None:
    """
    Sets up the root logger that logs to a file named with the process ID.
    
    Args:
        process_id (str): Process ID to use in the log filename.
        logger_level (int): Logging level to apply to the logger and all handlers (default: INFO).
    """
    # Ensure the logs directory exists
    os.makedirs(LOGS_PATH, exist_ok=True)

    # Store using process id
    log_filename = os.path.join(LOGS_PATH, f"{process_id}.log")

    # Configure the root logger
    root_logger = logging.getLogger()
    
    # Clear any existing handlers to avoid duplication
    if root_logger.handlers:
        root_logger.handlers.clear()
        
    # Set the logger level
    root_logger.setLevel(logger_level)

    # File handler with the same logging level
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logger_level)

    # Console handler with the same logging level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_level)

    # Apply formatter to both handlers
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
        'EXCEPTION': 'bold_red'
    }
    formatter = BoldMarkedTextFormatter(
        fmt="%(log_color)s**%(levelname)s:%(name)s:(%(lineno)d)**:%(message)s",
        log_colors=log_colors
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
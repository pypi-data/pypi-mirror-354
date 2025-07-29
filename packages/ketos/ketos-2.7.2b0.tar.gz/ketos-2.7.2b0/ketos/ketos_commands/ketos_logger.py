import logging
import structlog
import yaml
import os
from pathlib import Path


class YAMLRenderer:
    """
    Custom renderer for structlog that outputs log entries in YAML format.
    """
    def __init__(self, log_file_path):
        # Use a class-level attribute to determine whether a log entry has already been written
        # Check if the log file exists and is not empty
        if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > 0:
            self.first_log_entry = False
        else:
            self.first_log_entry = True
            
    def __call__(self, _, __, event_dict):
        if self.first_log_entry:
            # If this is the first log entry, don't add a separator at the start
            self.first_log_entry = False
            return yaml.dump(event_dict)
        else:
            # If this is not the first log entry, add a separator at the start
            return f'---\n{yaml.dump(event_dict)}'


class KetosLogger:
    """
    Custom logger for Ketos applications.

    Attributes:
        _handler: logging.FileHandler
            A shared FileHandler used by all KetosLogger instances.

    Args:
        logger_name: str
            The name of the logger.
        log_path: str
            The full path to the desired log file. Defaults to 'ketos.log'.
        mode: str
            The mode in which the log file is opened. Defaults to 'w'.
        format: str
            Determines the format of the logs. Possible values are 'yaml' or 'json'
    """

    def __init__(self, logger_name, log_path='ketos.log', mode='w', format='yaml'):
        self.format = format

        # Ensure the output folder exists
        Path(os.path.dirname(log_path)).mkdir(parents=True, exist_ok=True)

        # Create a logger with Python's logging
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.FileHandler(log_path, mode=mode))
        
        if format.lower() in ['yaml', 'yml']:
            renderer = YAMLRenderer(log_path)
        else:
            renderer = structlog.processors.JSONRenderer()

        # Configure structlog to use the standard Python logger
        structlog.configure(
            processors=[
                structlog.stdlib.add_logger_name, 
                structlog.stdlib.add_log_level, 
                structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S'),
                renderer
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        
        # Now wrap the Python logger with structlog
        self.logger = structlog.wrap_logger(self.logger)

    def info(self, message, stdout=False, **kwargs):
        """
        Log an informational message.

        Args:
            message: str
                The message to log.
            stdout: bool
                Determines whether to write the message to stdout.
            **kwargs: 
                Variable length argument list to pass to the logger.
        """
        if stdout:
            print(message)
        self.logger.info(message, **kwargs)

    def error(self, message, stdout=False, **kwargs):
        """
        Log an error message.

        Args:
            message: str
                The message to log.
            stdout: bool
                Determines whether to write the message to stdout.
            **kwargs: 
                Variable length argument list to pass to the logger.
        """
        if stdout:
            print(message)
        self.logger.error(message, **kwargs)

    def exception(self, message, stdout=False, **kwargs):
        """
        Log an error message, with stack trace information.

        Args:
            message: str
                The message to log.
            stdout: bool
                Determines whether to write the message to stdout.
            **kwargs: 
                Variable length argument list to pass to the logger.
        """
        if stdout:
            print(message)
        self.logger.exception(message, **kwargs)

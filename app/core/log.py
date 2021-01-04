"""
This module has logformatter to format exception stack trace into one line.  This is useful for sending logs
to centralized log analysis
:Author: Sindhu J S (sindhujs126@gmail.com)
"""
import logging
from app.core.settings import AppSettings


class LogExceptionFormatter(logging.Formatter):
    """
    Custom log formatter that formats the exception in one line
    """

    def formatException(self, ei) -> str:
        """
        converts the exception object into string
        :param ei:
        :return:
        """
        result = super().formatException(ei)
        return repr(result)

    def format(self, record: logging.LogRecord) -> str:
        """
        If the record is exception type then remove new lines otherwise send the same message as is
        :param record:
        :return:
        """
        result = super().format(record)
        if record.exc_text:
            result = result.replace('\n', '')
        return result


def setup_logging(config: AppSettings) -> None:
    """
    setup the logger for the application.  Call this at the beginning of the application
    :param config:
    :return:
    """
    formatter = LogExceptionFormatter(logging.BASIC_FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(filename=config.log_file_path)
    file_handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(config.log_level)
    root.addHandler(stream_handler)
    root.addHandler(file_handler)

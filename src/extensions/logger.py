import logging
import os
from typing import Any

from pythonjsonlogger.json import JsonFormatter

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


log_handler = logging.StreamHandler()
formatter = JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s %(service)s")

log_handler.setFormatter(formatter)

service_logger = logging.getLogger("pheon_logger")
service_logger.setLevel(LOG_LEVEL)
service_logger.addHandler(log_handler)
service_logger.propagate = False


class Logger:
    def __init__(self, logger_: logging.Logger) -> None:
        self._logger = logger_

    @staticmethod
    def _extend_kwargs(**kwargs: Any) -> dict:
        return {"extra": kwargs}

    def _log(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        kwargs = self._extend_kwargs(**kwargs)
        self._logger.log(level, msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.INFO, msg, *args, **kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log(logging.ERROR, msg, *args, **kwargs)

    def exception(self, exc: Exception, *args: Any, **kwargs: Any) -> None:
        kwargs = self._extend_kwargs(**kwargs)
        self._logger.exception(exc, *args, **kwargs)


logger = Logger(service_logger)

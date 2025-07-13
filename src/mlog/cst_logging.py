"""Advanced Logging Setup using Loguru, configurable via .env.

Features:
- Log rotation (by size & time)
- Log to file & terminal (optional)
- Intercept std logging (incl. Uvicorn, Alembic)
- Decorators: timer, logger_wraps
- Context: LogContext
- Stacktrace logger
"""

import datetime
import functools
import inspect
import logging
import os
import sys
import time
import traceback
from pathlib import Path
from typing import IO, Any

from dotenv import load_dotenv
from loguru import logger as loguru_logger

# === Load .env ===
load_dotenv()

# === ENV CONFIG ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
LOG_TO_TERMINAL = os.getenv("LOG_TO_TERMINAL", "false").lower() in ("1", "true", "yes")
LOG_DIAGNOSE = os.getenv("LOG_DIAGNOSE", "true").lower() in ("1", "true", "yes")
LOG_SERIALIZE = os.getenv("LOG_SERIALIZE", "false").lower() in ("1", "true", "yes")
LOG_ENQUEUE = os.getenv("LOG_ENQUEUE", "true").lower() in ("1", "true", "yes")
LOG_TO_FILE = os.getenv("LOG_TO_FILE", "true").lower() in ("1", "true", "yes")
LOG_PATH = os.getenv("LOG_PATH", "logs")
LOG_NAME_PREFIX = os.getenv("LOG_NAME_PREFIX", "app")
LOG_SIZE_MB = int(os.getenv("LOG_SIZE_MB", "10")) * 1_000_000
LOG_RETENTION_DAYS = os.getenv("LOG_RETENTION_DAYS", "7d")


# === ROTATOR ===
class Rotator:
    def __init__(self, size: int, at: datetime.time):
        self._size_limit = size
        now = datetime.datetime.now()
        self._time_limit = now.replace(hour=at.hour, minute=at.minute, second=at.second)
        if now >= self._time_limit:
            self._time_limit += datetime.timedelta(days=1)

    def should_rotate(self, message: Any, file: IO) -> bool:
        file.seek(0, 2)
        if file.tell() + len(message) > self._size_limit:
            return True
        if message.record["time"].timestamp() >= self._time_limit.timestamp():
            self._time_limit += datetime.timedelta(days=1)
            return True
        return False


# === OPENER ===
def opener(file: str, flags: int) -> int:
    return os.open(file, flags, 0o600)


# === FORMAT ===
FORMAT_STR = (
    "<level>{level: <8}</level> {time:YYYY-MM-DD HH:mm:ss} | "
    "<cyan>{process.name}:{thread.name}</cyan> | "
    "<magenta>{name}:{function}:{line}</magenta> | "
    "<yellow>{extra[ip]:<15}</yellow> | "
    "<level>{message}</level>"
)


# === SETUP ===
def setup_logging():
    """Setup logging configuration for the application.

    This function configures the Loguru logger based on the environment variables
    and the desired logging settings.
    """
    loguru_logger.remove()
    Path(LOG_PATH).mkdir(exist_ok=True)

    if LOG_TO_TERMINAL:
        loguru_logger.add(
            sys.stderr,
            level=LOG_LEVEL,
            format=FORMAT_STR,
            colorize=True,
            backtrace=True,
            diagnose=LOG_DIAGNOSE,
            enqueue=LOG_ENQUEUE,
        )

    if LOG_TO_FILE:
        rotator = Rotator(size=LOG_SIZE_MB, at=datetime.time(0, 0))

        loguru_logger.add(
            sink=f"{LOG_PATH}/{LOG_NAME_PREFIX}_app.log",
            level="INFO",
            format=FORMAT_STR,
            serialize=LOG_SERIALIZE,
            diagnose=LOG_DIAGNOSE,
            backtrace=True,
            enqueue=LOG_ENQUEUE,
            rotation=rotator.should_rotate,
            retention=LOG_RETENTION_DAYS,
            opener=opener,
        )

        loguru_logger.add(
            sink=f"{LOG_PATH}/{LOG_NAME_PREFIX}_error.log",
            level="ERROR",
            format=FORMAT_STR,
            serialize=LOG_SERIALIZE,
            diagnose=LOG_DIAGNOSE,
            backtrace=True,
            enqueue=LOG_ENQUEUE,
            rotation=rotator.should_rotate,
            retention=LOG_RETENTION_DAYS,
            opener=opener,
        )

    # Intercept std logging
    class InterceptHandler(logging.Handler):
        def emit(self, record: Any):
            try:
                level = loguru_logger.level(record.levelname).name
            except Exception:
                level = record.levelno
            frame, depth = inspect.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            loguru_logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    loguru_logger.info(f"Logging initialized at level={LOG_LEVEL}")


# === UVICORN PATCH ===
def patch_uvicorn_loggers():
    """Patch Uvicorn loggers to use Loguru.

    This function replaces the default logging handlers of Uvicorn with a custom
    handler that sends log messages to Loguru.
    """

    class Intercept(logging.Handler):
        def emit(self, record: Any):
            try:
                level = loguru_logger.level(record.levelname).name
            except Exception:
                level = record.levelno
            frame, depth = inspect.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            loguru_logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(name).handlers = [Intercept()]
        logging.getLogger(name).propagate = False


# === UTILS ===
def logger_wraps(*, entry: bool = True, exit: bool = True, level: str = "DEBUG"):
    """Decorator to log function entry and exit with arguments and results."""

    def wrapper(func: Any):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if entry:
                loguru_logger.log(
                    level, f"→ {func.__name__} | args={args}, kwargs={kwargs}"
                )
            result = func(*args, **kwargs)
            if exit:
                loguru_logger.log(level, f"← {func.__name__} | result={result}")
            return result

        return wrapped

    return wrapper


def timer(operation: str | None = None):
    """Decorator to time the execution of a function."""

    def decorator(func: Any):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            op = operation or func.__name__
            start = time.perf_counter()
            try:
                loguru_logger.info(f"[{op}] Starting...")
                result = func(*args, **kwargs)
                loguru_logger.info(
                    f"[{op}] Completed in {time.perf_counter() - start:.3f}s"
                )
            except Exception as e:
                loguru_logger.error(f"[{op}] Failed: {e}")
                raise
            return result

        return wrapper

    return decorator


class LogContext:
    def __init__(self, operation: str, level: str = "INFO"):
        self.operation = operation
        self.level = level
        self.start_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        loguru_logger.log(self.level, f"[{self.operation}] Starting...")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        if self.start_time is not None:
            duration = time.perf_counter() - self.start_time
        else:
            duration = float("nan")
        if exc_type:
            loguru_logger.error(
                f"[{self.operation}] Failed after {duration:.3f}s: {exc_val}"
            )
        else:
            loguru_logger.log(self.level, f"[{self.operation}] Done in {duration:.3f}s")


def log_with_stacktrace(message: str, level: str = "DEBUG"):
    """Log a message with a stacktrace at the specified log level."""
    stack = "".join(traceback.format_stack())
    loguru_logger.log(level, f"{message}\nStacktrace:\n{stack}")


logger = loguru_logger

__all__ = [
    "LogContext",
    "log_with_stacktrace",
    "logger",
    "logger_wraps",
    "patch_uvicorn_loggers",
    "setup_logging",
    "timer",
]

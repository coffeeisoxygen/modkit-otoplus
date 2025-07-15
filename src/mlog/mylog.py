"""Advanced Logging Setup using Loguru, configurable via log_setup.yaml.

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

import yaml

# === Load YAML CONFIG ===
from dotenv import load_dotenv
from loguru import logger as loguru_logger

load_dotenv()

CONFIG_FILE = "log_setup.yaml"

with open(CONFIG_FILE) as f:
    raw_config = yaml.safe_load(f)

# Ambil mode dari log_setup.yaml, default ke 'development' jika tidak ada
env_mode = raw_config.get("env_mode", "development")
common = raw_config.get("common", {})
mode_config = raw_config.get(env_mode, {})
config = {**common, **mode_config}

# === EXTRACT CONFIG ===
LOG_LEVEL = config.get("level", "DEBUG").upper()
LOG_TO_TERMINAL = config.get("to_terminal", False)
LOG_DIAGNOSE = config.get("diagnose", False)
LOG_SERIALIZE = config.get("serialize", False)
LOG_ENQUEUE = config.get("enqueue", True)
LOG_TO_FILE = config.get("to_file", True)
LOG_PATH = config.get("log_path", "logs")
LOG_NAME_PREFIX = config.get("name_prefix", "app")
LOG_SIZE_MB = int(config.get("size_mb", 10)) * 1_000_000
LOG_RETENTION = f"{config.get('retention_days', 7)} days"
LOG_SHOW_THREAD = config.get("show_thread", False)
LOG_SHOW_TIME = config.get("show_time", True)
LOG_SHOW_PROCESS = config.get("show_process", False)


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


# COLORING
loguru_logger.level("INFO", color="<cyan>")
loguru_logger.level("WARNING", color="<yellow>")
loguru_logger.level("ERROR", color="<red>")
loguru_logger.level("DEBUG", color="<blue>")
loguru_logger.level("TRACE", color="<white>")

# === FORMAT ===
FORMAT_STR = (
    "<level>{level: <8}</level> {time:YYYY-MM-DD HH:mm:ss} | "
    "<cyan>{process.name}:{thread.name}</cyan> | "
    "<magenta>{name}:{function}:{line}</magenta> | "
    "<level>{message}</level>"
)


# Add two blank lines before cli_format for PEP 8 compliance


def cli_format(
    record: Any,
    show_thread: bool = LOG_SHOW_THREAD,
    show_time: bool = LOG_SHOW_TIME,
    show_process: bool = LOG_SHOW_PROCESS,
) -> str:
    parts = []

    parts.append(f"<level>{record['level'].name}:</level>")
    if show_time:
        parts.append(f"{record['time']:YYYY-MM-DD HH:mm:ss}")
    if show_thread:
        parts.append(f"<cyan>{record['process'].name}:{record['thread'].name}</cyan>")
    elif show_process:
        parts.append(f"<cyan>{record['process'].name}</cyan>")
    parts.append(
        f"<magenta>{record['name']}:{record['function']} => {record['line']}</magenta>"
    )
    parts.append(f"{record['message']}")  # <-- tanpa <level>
    return " | ".join(parts) + "\n"


# === SETUP ===
def setup_logging():
    """Set up Loguru logging according to the configuration in log_setup.yaml.

    Configures log sinks, rotation, formatting, and intercepts standard logging.
    """
    loguru_logger.remove()
    Path(LOG_PATH).mkdir(exist_ok=True)

    if LOG_TO_TERMINAL:
        loguru_logger.add(
            sys.stderr,
            level=LOG_LEVEL,
            format=lambda record: cli_format(
                record, show_thread=LOG_SHOW_THREAD, show_time=LOG_SHOW_TIME
            ),
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
            retention=LOG_RETENTION,
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
            retention=LOG_RETENTION,
            opener=opener,
        )

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
    loguru_logger.info(
        f"Logging initialized in {env_mode.upper()} mode, level={LOG_LEVEL}"
    )


# === UVICORN PATCH ===
def patch_uvicorn_loggers():
    """Patch Uvicorn loggers to route their output through Loguru."""

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
    """Decorator to log function entry, exit, and arguments/results.

    Parameters
    ----------
    entry : bool
        Whether to log function entry.
    exit : bool
        Whether to log function exit.
    level : str
        Log level to use.

    Returns:
    -------
    Callable
        Decorated function.
    """

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
    """Decorator to time a function's execution and log the duration.

    Parameters
    ----------
    operation : str or None
        Optional operation name for logging.

    Returns:
    -------
    Callable
        Decorated function.
    """

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
        duration = (
            time.perf_counter() - self.start_time if self.start_time else float("nan")
        )
        if exc_type:
            loguru_logger.error(
                f"[{self.operation}] Failed after {duration:.3f}s: {exc_val}"
            )
        else:
            loguru_logger.log(self.level, f"[{self.operation}] Done in {duration:.3f}s")


def log_with_stacktrace(message: str, level: str = "DEBUG"):
    """Log a message along with the current stacktrace.

    Parameters
    ----------
    message : str
        The message to log.
    level : str
        Log level to use.
    """
    stack = "".join(traceback.format_stack())
    loguru_logger.log(level, f"{message}\nStacktrace:\n{stack}")


logger = loguru_logger

__all__ = [
    "LogContext",
    "Rotator",
    "log_with_stacktrace",
    "logger",
    "logger_wraps",
    "patch_uvicorn_loggers",
    "setup_logging",
    "timer",
]

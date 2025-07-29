"""Logging setup for the package."""

import ast
import sys
import logging
from os import getenv
from pathlib import Path
from logging.handlers import RotatingFileHandler

import colorlog
from colorlog import ColoredFormatter


def _get_default_log_level(fallback=None):
    """Fail eval silently."""
    val = getenv("BB_LOG_LEVEL", "20")
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError) as e:
        print(f"[E] failed to eval `{val}` Error: {e}")
        return fallback


LOGGED_ONCE_MSGES = set()
DEFAULT_LOG_LEVEL = _get_default_log_level(fallback=logging.INFO)
_ROOT_LOGGER_NAME = __package__ or __name__
_LOG_MESSAGE_FMT_ = "%(asctime)s %(context)s [%(levelname).1s] %(message)s"
_LOG_CONSOLE_FMT_ = "%(log_color)s[%(levelname).1s] %(bold)s%(message)s %(reset)s::%(context)s::"

# fmt: off
_LOG_CONTEXT_CONF = {
    "processName"   : False,
    "process"       : False,
    "threadName"    : False,
    "thread"        : False,
    "pathname"      : False,
    "filename"      : False,
    "name"          : False, # {"prefix": "<", "suffix": "."},
    "module"        : {"prefix": "<", "suffix": ""},
    "lineno"        : {"prefix": ":", "suffix": "> "},
    "funcName"      : {},
    "__align"       : "<",
    "__pad_char"    : "-",
}# fmt: on


class LogContextFilter(logging.Filter):
    """Logging filter to add a padded call context location to each log record."""

    def __init__(self, *args, context_params: dict, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_params = context_params

    def filter(self, record: logging.LogRecord) -> bool:
        """Add a padded call context location to each log record."""
        context = ""
        for attr, conf in self.context_params.items():
            if isinstance(conf, dict):
                v = record.__getattribute__(attr)
                context += f"{conf.get('prefix', '')}{v}{conf.get('suffix', '')}"

        # oset = dict.fromkeys(a).keys()
        # context = ".".join(dict.fromkeys(context.split(".")).keys())
        # context.replace(".:",":")
        align = self.context_params.get("__align", "<")
        pad_char = self.context_params.get("__pad_char", " ")
        min_width = self.context_params.get("__min_width", 15)
        record.context = f"{context + ' ':{pad_char}{align}{min_width}}"
        return True


def log_once(logger_func, message: str) -> None:
    """Log a message only once."""
    if message not in LOGGED_ONCE_MSGES:
        LOGGED_ONCE_MSGES.add(message)
        logger_func(message)


def _is_writable(path: Path) -> bool:
    """Check if the path is writable (directory or existing file)."""
    try:
        if path.is_dir():
            test_file = path / ".write_test"
            test_file.touch()
            test_file.unlink()
        elif path.is_file():
            with path.open("a"):
                pass
    except (Exception,):
        return False
    else:
        return True


def get_logger(name: str, log_level: int = DEFAULT_LOG_LEVEL, max_file_size_mb: int = 1,
               )-> logging.Logger:
    """Returns a per-module logger that writes to its own file and propagates to the root logger."""
    is_root = name == _ROOT_LOGGER_NAME
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    # logger.debug("Logger [%s] initialized with level [%s]", name, logging.getLevelName(log_level))

    if not logger.handlers:
        file_formatter = logging.Formatter(
            _LOG_MESSAGE_FMT_,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        for candidate_dir in [Path.cwd() / "logs", Path.home() / f"{_ROOT_LOGGER_NAME}_logs"]:
            try:
                candidate_dir.mkdir(parents=True, exist_ok=True)
                if _is_writable(candidate_dir):
                    short_name = name.split(".", 1)[1] if "." in name else name
                    log_file = candidate_dir / f"{short_name}.log"
                    rotating_handler = logging.handlers.RotatingFileHandler(
                        log_file,
                        maxBytes=max_file_size_mb * 1024 * 1024,
                        backupCount=5,
                    )
                    rotating_handler.setFormatter(file_formatter)
                    rotating_handler.addFilter(LogContextFilter(context_params=_LOG_CONTEXT_CONF))
                    rotating_handler.setLevel(logging.DEBUG)
                    logger.addHandler(rotating_handler)
                    break
            except PermissionError as e:
                logger.warning(
                    "Logger [%s] file handler disabled: No writable directory found.",
                    name
                )
                logger.warning(
                    "Logger [%s] logging to console only. error: %s",
                    name, e
                )
            except (Exception,) as e:
                logger.warning(
                    "Logger [%s] file handler disabled. Failed to create log file: %s",
                    name, e
                )

        colorlog.default_log_colors.update({"DEBUG": "cyan"})
        if is_root:
            stream_handler = logging.StreamHandler(sys.__stdout__)
            stream_handler.setFormatter(
                ColoredFormatter(
                    _LOG_CONSOLE_FMT_,
                    defaults={"log_color": "", "bold": "", "reset": "", "context": ""},
                )
            )
            stream_handler.addFilter(LogContextFilter(context_params=_LOG_CONTEXT_CONF))
            stream_handler.setLevel(log_level)
            logger.addHandler(stream_handler)

    logger.propagate = not is_root  # Only propagate if not root
    return logger


"""
This is the root logger for the package. don't use it directly by importing it.
use the `get_logger(__name__)` function from this module instead.
"""
root_logger = get_logger(name=_ROOT_LOGGER_NAME, log_level=logging.DEBUG, max_file_size_mb=5)

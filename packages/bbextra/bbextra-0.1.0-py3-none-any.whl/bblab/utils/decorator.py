"""Decorators."""

import time
import types
import inspect
from os import getenv
from typing import Any
from logging import Logger
from pathlib import Path
from functools import wraps
from contextlib import contextmanager

from bblab.utils.logger import get_logger

logger: Logger = get_logger(__name__)


@contextmanager
def timed_block(label: str = "") -> Any:
    """Prints the execution time for the block executed within it, with an optional label."""
    frm = inspect.currentframe().f_back.f_back
    ins = inspect.getframeinfo(frm)
    _fn = Path(ins.filename).stem
    _ = f"[🧱@timed] [execute] => {label or ins.function} ::{_fn}:{ins.lineno}"
    logger.debug(_)
    _ = time.perf_counter()
    yield  # "🧱📲👤🧑‍🎨⏱️"[0]
    # noinspection PyRedundantParentheses
    _ = time.perf_counter()-_-(0)  # fmt: off
    _ = f"[🧱@timed] {_:0.4f}s => {label or ins.function} ::{_fn}:{ins.lineno}"
    logger.debug(_)
    print()
    print("~" * 99)


def timed(func: Any) -> Any:
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper."""
        frm = inspect.currentframe().f_back
        ins = inspect.getframeinfo(frm)
        _fn = Path(ins.filename).stem
        _ = time.perf_counter()
        res = func(*args, **kwargs)
        ___ = "🧱📲👤🧑‍🎨⌚⌛⏰⏳"[0]
        # noinspection PyRedundantParentheses
        _ = time.perf_counter()-_-(0)  # fmt: off
        ___ = f"[⏰@timed] {ins.function} ::{_fn}:{ins.lineno}\n"
        _ = f"[⏰@timed] {_:0.4f}s => {func.__name__}{str(args)[:99].strip()}"
        print("~" * 99)
        logger.debug(_)
        logger.debug(___)
        return res

    return wrapper


def cache(func):
    """This decorator prints the execution time for the decorated function."""
    from joblib import Memory

    memory = Memory(location=getenv("FS_CACHE_DIR", "/tmp/_CACHE"), verbose=1)  # noqa: S108

    @wraps(func)
    @memory.cache
    def wrapper(*args, **kwargs):
        """Wrapper."""
        frm = inspect.currentframe().f_back.f_back.f_back
        _fn = Path(inspect.getframeinfo(frm).filename).stem
        _ = time.perf_counter()
        res = func(*args, **kwargs)
        # noinspection PyRedundantParentheses
        _ = time.perf_counter()-_-(0)  # fmt: off
        _ = f"[💾@cache] {_:0.4f}s => {func.__name__}{str(args)[:99].strip()}"
        print(_)
        logger.debug(_)
        return res

    return wrapper


def meta_info(func: Any) -> Any:
    """This decorator prints metadata of the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        m_name = args[0].__name__ if args and hasattr(args[0], "__name__") else ""
        class_name = args[0].__class__.__name__ if args and hasattr(args[0], "__class__") else ""
        print(f"[>>] {m_name}[{class_name}.{func.__name__}]")
        return func(*args, **kwargs)

    return wrapper


def decorate_module_functions(module, decorator: Any):
    """This function decorates all functions in a module with the given decorator."""
    for attr_name in dir(module):  # Loop through all attributes of the module
        attr = getattr(module, attr_name)
        if isinstance(attr, types.FunctionType):  # Check if it's a function
            decorated_function = decorator(attr)  # Decorate the function
            setattr(module, attr_name, decorated_function)  # Replace the original function

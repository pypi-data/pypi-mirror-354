from __future__ import annotations
import functools


class DatabaseNotLoadedError(RuntimeError):
    """Raised when an operation is attempted on a closed database."""
    pass


def decorate_all_methods(decorator):
    """
    Class decorator factory that applies `decorator` to all methods
    of the class (excluding dunder methods).
    """
    def decorate(cls):
        for name, attr in cls.__dict__.items():
            if name.startswith("__"):
                continue
            if callable(attr):
                setattr(cls, name, decorator(attr))
        return cls

    return decorate


def check_db_open(fn):
    """
    Decorator that checks that a database is open.
    """
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        # Check inside database class
        if hasattr(self, "is_open"):
            if not self.is_open():
                raise DatabaseNotLoadedError(
                    f"{fn.__qualname__}: Database is not loaded. "
                    "Please open a database first."
                )

        # Check entities that reference a database instance
        if hasattr(self, "m_database"):
            if not self.m_database.is_open():
                raise DatabaseNotLoadedError(
                    f"{fn.__qualname__}: Database is not loaded. "
                    "Please open a database first."
                )

        return fn(self, *args, **kwargs)

    return wrapper

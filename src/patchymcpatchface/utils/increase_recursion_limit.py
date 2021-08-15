"""Context manager for increasing recursion limit temporarily"""
import sys
from contextlib import contextmanager

DEFAULT_RECURSION_LIMIT = 10 ** 6


@contextmanager
def temporary_increase_recursion_limit(increased_limit: int = DEFAULT_RECURSION_LIMIT):
    """Context manager for temporarily increasing recursion limit

    Args:
        increased_limit (int, optional): Maximum recursion limit to be set. Defaults to DEFAULT_RECURSION_LIMIT.
    """
    try:
        original_recursion_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(increased_limit)
        yield
    finally:
        sys.setrecursionlimit(original_recursion_limit)


def increase_recursion_limit(
    increased_limit: int = DEFAULT_RECURSION_LIMIT,
):
    """Increases recursion limit of system

    Args:
        increased_limit (int, optional): Maximum recursion limit to be set.
        Defaults to DEFAULT_RECURSION_LIMIT.
    """
    sys.setrecursionlimit(increased_limit)

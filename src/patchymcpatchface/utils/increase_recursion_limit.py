"""https://stackoverflow.com/questions/43689114/recursively-print-all-attributes-lists-dicts-etc-of-an-object-in-python"""  # pylint: disable=line-too-long


import sys
from functools import wraps
from typing import Callable, Union

DEFAULT_RECURSION_LIMIT = 10 ** 6


def wrapper_factory(
    func: Callable, new_limit: int, limit_is_temporary: bool = False
) -> Callable:
    """Factory function to generate wrapper that implements recursion limit increase

    Args:
        f (Callable): Callable to be wrapped
        new_limit (int): Number of max recursions
        limit_is_temporary (bool, optional): Is the limit increase temporary. Defaults to False.

    Returns:
        Callable: Wrapped function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        original_recursion_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(new_limit)
        result = func(*args, **kwargs)
        if limit_is_temporary:
            sys.setrecursionlimit(original_recursion_limit)
        return result

    return wrapper


def get_new_limit(arg: int) -> int:
    """Gets and validate new recursion limit from argument

    Args:
        arg (int): argument received by decorator call

    Raises:
        ValueError: If argument is not an integer

    Returns:
        int: new recursion limit value
    """
    new_limit = arg
    try:
        assert isinstance(new_limit, int)
    except AssertionError as err:
        raise ValueError(
            "an int should be provided as the value of max recursion depth!"
        ) from err

    return new_limit


def increase_recursion_permanently(arg: Union[Callable, int]) -> Callable:
    """Decorator that increases recursion limit permanently

    Args:
        arg (Union[Callable, int]): Callable if decorating without explicit recursion limit defined. Alternatively, use this decorator as function with new recursion limit defined

    Returns:
        Callabe: Wrapped function
    """
    if isinstance(arg, type(Callable)):
        func = arg
        wrapper = wrapper_factory(func=func, new_limit=DEFAULT_RECURSION_LIMIT)
        return wrapper

    new_limit = get_new_limit(arg)

    def inner(func: Callable) -> Callable:
        """Wrapped function with system limit increase

        Args:
            func (Callable): Original function

        Returns:
            Callable: Wrapped function
        """
        wrapper = wrapper_factory(func=func, new_limit=new_limit)
        return wrapper

    return inner


def increase_recursion_temporarily(arg: Union[Callable, int]) -> Callable:
    """Decorator that increases recursion limit permanently

    Args:
        arg (Union[Callable, int]): Callable if decorating without explicit recursion limit defined. Alternatively, use this decorator as function with new recursion limit defined

    Returns:
        Callabe: Wrapped function
    """
    if isinstance(arg, type(Callable)):
        wrapper = wrapper_factory(
            func=arg, new_limit=DEFAULT_RECURSION_LIMIT, limit_is_temporary=True
        )
        return wrapper

    new_limit = arg

    def inner(func):
        """Wrapped function with system limit increase

        Args:
            func (Callable): Original function

        Returns:
            Callable: Wrapped function
        """
        wrapper = wrapper_factory(
            func=func, new_limit=new_limit, limit_is_temporary=True
        )
        return wrapper

    return inner

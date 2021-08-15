import inspect as i
from enum import Enum, auto
from typing import Callable, List
from functools import wraps


def print_return(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(result)
        return result

    return wrapper


class ObjectTypes(Enum):
    MODULE = auto()
    CLASS = auto()
    METHOD = auto()
    FUNCTION = auto()
    GENERATORFUNCTION = auto()
    GENERATOR = auto()
    COROUTINEFUNCTION = auto()
    AWAITABLE = auto()
    ASYNCGENFUNCTION = auto()
    ASYNCGEN = auto()
    TRACEBACK = auto()
    FRAME = auto()
    CODE = auto()
    BUILTIN = auto()
    ROUTINE = auto()
    ABSTRACT = auto()
    METHODDESCRIPTOR = auto()
    DATADESCRIPTOR = auto()
    GETSETDESCRIPTOR = auto()
    MEMBERDESCRIPTOR = auto()


types: List[
    str
] = ObjectTypes._member_names_  # pylint: disable=protected-access,no-member


@print_return
def get_object_type(obj: object = 5):

    for type_ in types:
        inspect_function_name = f"is{type_.lower()}"
        if not hasattr(i, inspect_function_name):
            continue
        type_check = getattr(i, inspect_function_name)
        if type_check(obj):
            return type_

    return type(obj).__name__


if __name__ == "__main__":
    from icecream import ic

    get_object_type(None)
    get_object_type(ic)

    class Tester:
        pass

    get_object_type(Tester)
    get_object_type(get_object_type)
    # ic(OBJECT_TYPES._member_names_)
    # ic(OBJECT_TYPES._members_names_)

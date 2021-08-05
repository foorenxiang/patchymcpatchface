from test_value import test_value
from mypackage.foo import target_function


def foo_main():
    print(__name__)
    print("from mypackage.foo import target_function")
    print("Running target_function()")
    result = target_function()
    assert result == test_value
    return result

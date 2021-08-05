from test_value import test_value
from mypackage.foo import *


def foobar_main():
    print(__name__)
    print("from mypackage.foo import *")
    print("Running target_function()")
    result = target_function()
    assert result == test_value
    return result

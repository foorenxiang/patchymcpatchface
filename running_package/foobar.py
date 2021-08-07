"""from mypackage.foo module import all exported attributes (includes target function)"""
from test_value import TEST_VALUE
from mypackage.foo import *


def foobar_main():
    """function to test imported function"""
    print(__name__)
    print("from mypackage.foo import *")
    print("Running target_function()")
    result = target_function()
    assert result == TEST_VALUE
    return result

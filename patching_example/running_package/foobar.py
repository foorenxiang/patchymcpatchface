"""from patching_example.mypackage.foo module import all exported attributes (includes target function)"""
from patching_example.test_value import TEST_VALUE
from patching_example.mypackage.foo import *


def foobar_main():
    """function to test imported function"""
    print(__name__)
    print("from patching_example.mypackage.foo import *")
    print("Running target_function()")
    result = target_function()
    assert result == TEST_VALUE
    return result

"""from package_to_be_patched.foo module import target_function as function"""
from test_value import TEST_VALUE
from package_to_be_patched.foo import target_function


def foo_main():
    """function to test imported function"""
    print(__name__)
    print("from package_to_be_patched.foo import target_function")
    print("Running target_function()")
    result = target_function()
    assert result == TEST_VALUE
    return result

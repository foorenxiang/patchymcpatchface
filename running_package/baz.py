"""imports package_to_be_patched.foo module and runs target_function as its attribute"""
from test_value import TEST_VALUE
import package_to_be_patched.foo


def baz_main():
    """function to test imported function"""
    print(__name__)
    print("import package_to_be_patched.foo")
    print("Running package_to_be_patched.foo.target_function()")
    result = package_to_be_patched.foo.target_function()
    assert result == TEST_VALUE
    return result

"""imports package_to_be_patched package and runs target_function as its attribute"""
import package_to_be_patched
from test_value import TEST_VALUE


def bar_main():
    """function to test imported function"""
    print(__name__)
    print("import package_to_be_patched")
    print("Running package_to_be_patched.foo.target_function()")
    result = package_to_be_patched.foo.target_function()
    assert result == TEST_VALUE
    return result

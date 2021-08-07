"""imports patching_example.mypackage.foo module and runs target_function as its attribute"""
from patching_example.test_value import TEST_VALUE
import patching_example.mypackage.foo


def baz_main():
    """function to test imported function"""
    print(__name__)
    print("import patching_example.mypackage.foo")
    print("Running patching_example.mypackage.foo.target_function()")
    result = patching_example.mypackage.foo.target_function()
    assert result == TEST_VALUE
    return result

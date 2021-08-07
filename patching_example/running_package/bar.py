"""imports patching_example.mypackage package and runs target_function as its attribute"""
import patching_example.mypackage
from patching_example.test_value import TEST_VALUE


def bar_main():
    """function to test imported function"""
    print(__name__)
    print("import patching_example.mypackage")
    print("Running patching_example.mypackage.foo.target_function()")
    result = patching_example.mypackage.foo.target_function()
    assert result == TEST_VALUE
    return result

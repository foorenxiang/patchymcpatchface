"""imports mypackage.foo module and runs target_function as its attribute"""
from test_value import TEST_VALUE
import mypackage.foo


def baz_main():
    """function to test imported function"""
    print(__name__)
    print("import mypackage.foo")
    print("Running mypackage.foo.target_function()")
    result = mypackage.foo.target_function()
    assert result == TEST_VALUE
    return result

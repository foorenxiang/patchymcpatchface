"""imports mypackage package and runs target_function as its attribute"""
import mypackage
from test_value import TEST_VALUE


def bar_main():
    """function to test imported function"""
    print(__name__)
    print("import mypackage")
    print("Running mypackage.foo.target_function()")
    result = mypackage.foo.target_function()
    assert result == TEST_VALUE
    return result

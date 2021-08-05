import mypackage
from test_value import test_value


def bar_main():
    print(__name__)
    print("import mypackage")
    print("Running mypackage.foo.target_function()")
    result = mypackage.foo.target_function()
    assert result == test_value
    return result

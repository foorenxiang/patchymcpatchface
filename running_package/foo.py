from mypackage.foo import target_function


def foo_main():
    print(__name__)
    print("from mypackage.foo import target_function")
    print("Running target_function()")
    test_value = "I'm the patched function\n"
    result = target_function()
    assert result == test_value
    return result

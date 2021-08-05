import mypackage


def bar_main():
    print(__name__)
    print("import mypackage")
    print("Running mypackage.foo.target_function()")
    test_value = "I'm the patched function\n"
    result = mypackage.foo.target_function()
    assert result == test_value
    return result

import mypackage.foobar


def bazbar_main():
    print(__name__)
    print("import mypackage.foo")
    print("Running mypackage.foo.target_function()")
    result = mypackage.foobar.target_function2()
    assert result == "I'm the other patched function\n"
    return result

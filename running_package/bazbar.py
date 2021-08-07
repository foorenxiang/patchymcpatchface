"""imports mypackage.foo module and runs target_function2 as its attribute"""
import mypackage.foobar


def bazbar_main():
    """function to test imported function"""
    print(__name__)
    print("import mypackage.foo")
    print("Running mypackage.foo.target_function2()")
    result = mypackage.foobar.target_function2()
    assert result == "I'm the other patched function\n"
    return result

"""imports patching_example.mypackage.foo module and runs target_function2 as its attribute"""
import patching_example.mypackage.foobar


def bazbar_main():
    """function to test imported function"""
    print(__name__)
    print("import patching_example.mypackage.foo")
    print("Running patching_example.mypackage.foo.target_function2()")
    result = patching_example.mypackage.foobar.target_function2()
    assert result == "I'm the other patched function\n"
    return result

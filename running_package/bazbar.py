"""imports package_to_be_patched.foo module and runs target_function2 as its attribute"""
import package_to_be_patched.foobar


def bazbar_main():
    """function to test imported function"""
    print(__name__)
    print("import package_to_be_patched.foo")
    print("Running package_to_be_patched.foo.target_function2()")
    result = package_to_be_patched.foobar.target_function2()
    assert result == "I'm the other patched function\n"
    return result

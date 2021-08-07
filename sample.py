import sys
from test_value import test_value


def main():
    print("======Before patch:======\n")
    from mypackage.foo import target_function as target_function_direct

    assert target_function_direct() == "I'm the original function\n"
    from mypackage.foobar import target_function2

    assert target_function2() == "I'm the other original function\n"

    import patcher

    patcher

    # automatically patches from patch_manifest.py on project root on import
    from patcher import invoke_patch_hooks

    assert target_function2() == "I'm the other original function\n"
    import patcher

    print("======After patching just the first original function:======\n")

    filter_sys_modules = lambda filter_term: {
        key: value for key, value in sys.modules.items() if filter_term in key
    }

    print(filter_sys_modules("mypackage"))
    print(filter_sys_modules("patch_package"))

    print(__name__)
    print("Running target_function_direct()")
    target_function_direct()

    import mypackage

    print(__name__)
    print("Running mypackage.foo.target_function()")
    mypackage.foo.target_function()

    from running_package.foo import foo_main

    assert foo_main() == test_value

    from running_package.bar import bar_main

    assert bar_main() == test_value

    from running_package.baz import baz_main

    assert baz_main() == test_value

    from running_package.foobar import foobar_main

    assert foobar_main() == test_value

    from mypackage.foobar import target_function2

    print("The other original function should still be unpatched at this point")
    assert target_function2() == "I'm the other original function\n"

    # you can also import another patch module manifest placed elsewhere in your project
    from running_package.custom_patch_manifest import PATCH_MODULES

    # manually invoke your additional patch hooks. you can use this to control/delay patching
    invoke_patch_hooks(PATCH_MODULES)

    print("After patching the other original function")
    from running_package.bazbar import bazbar_main

    assert bazbar_main() == "I'm the other patched function\n"


if __name__ == "__main__":
    main()

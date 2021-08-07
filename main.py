import sys

from test_value import TEST_VALUE


def main():
    print("======Before patch:======\n")
    from package_to_be_patched.foo import target_function as target_function_direct

    assert target_function_direct() == "I'm the original function\n"
    from package_to_be_patched.foobar import target_function2

    assert target_function2() == "I'm the other original function\n"

    # automatically patches from patch_manifest.py on project root on import
    import patchymcpatchface as pf

    pf

    assert target_function2() == "I'm the other original function\n"

    print("======After patching just the first original function:======\n")

    filter_sys_modules = lambda filter_term: {
        key: value for key, value in sys.modules.items() if filter_term in key
    }

    print(filter_sys_modules("package_to_be_patched"))
    print(filter_sys_modules("patch_package"))

    print(__name__)
    print("Running target_function_direct()")
    target_function_direct()

    import package_to_be_patched

    print(__name__)
    print("Running package_to_be_patched.foo.target_function()")
    package_to_be_patched.foo.target_function()

    from running_package.foo import foo_main

    assert foo_main() == TEST_VALUE

    from running_package.bar import bar_main

    assert bar_main() == TEST_VALUE

    from running_package.baz import baz_main

    assert baz_main() == TEST_VALUE

    from running_package.foobar import foobar_main

    assert foobar_main() == TEST_VALUE

    from package_to_be_patched.foobar import target_function2

    print("The other original function should still be unpatched at this point")
    assert target_function2() == "I'm the other original function\n"

    # you can also import another patch module manifest placed elsewhere in your project
    from running_package.custom_patch_manifest import PATCH_MODULES

    # manually invoke your additional patch hooks. you can use this to control/delay patching
    pf.invoke_patch_hooks(PATCH_MODULES)

    print("After patching the other original function")
    from running_package.bazbar import bazbar_main

    assert bazbar_main() == "I'm the other patched function\n"


if __name__ == "__main__":
    main()

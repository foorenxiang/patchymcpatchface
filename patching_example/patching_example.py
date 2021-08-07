"""Patching example"""
import sys

from patching_example.test_value import TEST_VALUE


def main():
    """Patching example function"""
    print("======Before patch:======\n")
    from patching_example.mypackage.foo import target_function as target_function_direct

    assert target_function_direct() == "I'm the original function\n"
    from patching_example.mypackage.foobar import target_function2

    assert target_function2() == "I'm the other original function\n"

    # automatically patches from patch_manifest.py on project root on import
    import patchymcpatchface as pf

    pf

    assert target_function2() == "I'm the other original function\n"

    print("======After patching just the first original function:======\n")

    filter_sys_modules = lambda filter_term: {
        key: value for key, value in sys.modules.items() if filter_term in key
    }

    print(filter_sys_modules("patching_example.mypackage"))
    print(filter_sys_modules("patching_example.patch_package"))

    print(__name__)
    print("Running target_function_direct()")
    target_function_direct()

    import patching_example.mypackage

    print(__name__)
    print("Running patching_example.mypackage.foo.target_function()")
    patching_example.mypackage.foo.target_function()

    from patching_example.running_package.foo import foo_main

    assert foo_main() == TEST_VALUE

    from patching_example.running_package.bar import bar_main

    assert bar_main() == TEST_VALUE

    from patching_example.running_package.baz import baz_main

    assert baz_main() == TEST_VALUE

    from patching_example.running_package.foobar import foobar_main

    assert foobar_main() == TEST_VALUE

    from patching_example.mypackage.foobar import target_function2

    print("The other original function should still be unpatched at this point")
    assert target_function2() == "I'm the other original function\n"

    # you can also import another patch module manifest placed elsewhere in your project
    from patching_example.running_package.custom_patch_manifest import PATCH_MODULES

    # manually invoke your additional patch hooks. you can use this to control/delay patching
    pf.invoke_patch_hooks(PATCH_MODULES)

    print("After patching the other original function")
    from patching_example.running_package.bazbar import bazbar_main

    assert bazbar_main() == "I'm the other patched function\n"


if __name__ == "__main__":
    main()

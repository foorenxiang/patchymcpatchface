import sys
from patcher import apply_patches
from icecream import ic

apply_patches()
filter_sys_modules = lambda filter_term: {
    key: value for key, value in sys.modules.items() if filter_term in key
}


if __name__ == "__main__":
    test_value = "I'm the patched function\n"

    ic(filter_sys_modules("mypackage"))
    ic(filter_sys_modules("patch_package"))
    from mypackage.foo import target_function as target_function_direct

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

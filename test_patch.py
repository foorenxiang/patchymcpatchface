from patcher import invoke_patch_hooks
from test_value import test_value


def test_main():
    from main import main

    main()


def test_patching():
    invoke_patch_hooks()

    from mypackage.foo import target_function as target_function_direct

    assert target_function_direct() == test_value

    import mypackage

    assert mypackage.foo.target_function() == test_value

    from running_package.foo import foo_main

    assert foo_main() == test_value

    from running_package.bar import bar_main

    assert bar_main() == test_value

    from running_package.baz import baz_main

    assert baz_main() == test_value

    from running_package.foobar import foobar_main

    assert foobar_main() == test_value

    from running_package.bazbar import bazbar_main

    assert bazbar_main() == "I'm the other patched function\n"

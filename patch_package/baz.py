import sys


def patch_function():
    print("I'm the patched function\n")


def patch():
    patch_target = sys.modules["mypackage"].foo
    assert hasattr(
        patch_target, "target_function"
    ), "The module to be patched is no longer there"
    patch_target.target_function = patch_function

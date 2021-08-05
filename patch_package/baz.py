import sys


def patch_function():
    printout = "I'm the patched function\n"
    print(printout)
    return printout


def patch():
    patch_target = sys.modules["mypackage"].foo
    assert hasattr(
        patch_target, "target_function"
    ), "The module to be patched is no longer there"
    setattr(patch_target, "target_function", patch_function)

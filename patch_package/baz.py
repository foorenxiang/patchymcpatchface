import sys


def patch_function():
    print("I'm the patched function\n")


def patch():
    assert hasattr(sys.modules["mypackage"].foo, "target_function")
    # assert hasattr(
    #     sys.modules["mypackage"].non_existent_module, "target_function"
    # )  # this will throw attribute error
    # assert hasattr(
    #     sys.modules["mypackage"].foo, "non_existent_target_function"
    # )  # this will throw attribute error
    sys.modules["mypackage"].foo.target_function = patch_function

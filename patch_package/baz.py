import sys


def patch_function():
    print("I'm the patched function\n")


def patch():
    sys.modules["mypackage"].foo.target_function = patch_function

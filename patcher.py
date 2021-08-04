import sys
import mypackage.foo
from patch_package.baz import patch_function

mypackage


def patch():
    sys.modules["mypackage"].foo.target_function = "abracadabra"
    sys.modules["mypackage"].foo.target_function = 42
    sys.modules["mypackage"].foo.target_function = patch_function

from mypackage.foo import *


def foobar_main():
    print(__name__)
    print("from mypackage.foo import *")
    print("Running target_function()")
    target_function()

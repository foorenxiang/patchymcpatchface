from mypackage.foo import target_function


def foo_main():
    print(__name__)
    print("Running target_function()")
    target_function()

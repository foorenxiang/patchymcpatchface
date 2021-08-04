import mypackage.foo


def baz_main():
    print(__name__)
    print("Running mypackage.foo.target_function()")
    mypackage.foo.target_function()

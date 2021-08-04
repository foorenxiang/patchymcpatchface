def patch():
    import sys
    import mypackage.foo
    from patch_package.baz import patch_function

    mypackage

    # patching from the parent module is sufficient
    sys.modules["mypackage"].foo.target_function = patch_function

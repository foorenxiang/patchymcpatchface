def patch_function():
    printout = "I'm the other patched function\n"
    print(printout)
    return printout


def patch_hook():
    from patch_apply import patch_apply

    patch_apply("mypackage.foobar.target_function2", patch_function)

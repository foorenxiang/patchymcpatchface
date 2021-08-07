def patch_function():
    printout = "I'm the patched function\n"
    print(printout)
    return printout


def patch_hook():  # TODO: define this patch_hook (reserved function name) for patcher to pick up
    from patchymcpatchface import patch_apply

    patch_apply(
        "mypackage.foo.target_function", patch_function
    )  # TODO: put in the full module ancestry and the patch function as parameters

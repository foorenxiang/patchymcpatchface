"""Contains patch function for mypackage.foo.target_function"""
from patchymcpatchface import patch_apply


def patch_function():
    """Patch function"""
    printout = "I'm the patched function\n"
    print(printout)
    return printout


def patch_hook():  #  define this patch_hook (reserved function name) for patcher to pick up
    """Patch hook to be called by patchymcpatchface"""
    patch_apply(
        "mypackage.foo.target_function", patch_function
    )  #  put in the full module ancestry and the patch function as parameters

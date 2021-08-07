"""Contains patch function for package_to_be_patched.foo.target_function2"""
from patchymcpatchface import patch_apply


def patch_function():
    """Patch function"""
    printout = "I'm the other patched function\n"
    print(printout)
    return printout


def patch_hook():
    """Patch hook to be called by patchymcpatchface"""

    patch_apply("package_to_be_patched.foobar.target_function2", patch_function)

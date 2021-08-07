"""Module containing a target function to be patched"""


def target_function():
    """Target function to be patched"""
    printout = "I'm the original function\n"
    print(printout)
    return printout

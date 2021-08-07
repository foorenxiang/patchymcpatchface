"""Module containing a target function to be patched"""


def target_function2():
    """Target function to be patched"""
    printout = "I'm the other original function\n"
    print(printout)
    return printout

from patchymcpatchface import as_module

assert (
    as_module("src/patchymcpatchface/utils/increase_recursion_limit.py", "abc")
    == "src.patchymcpatchface.utils.increase_recursion_limit.abc"
)

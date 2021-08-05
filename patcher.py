import mypackage.foo
import patch_package.baz as baz

mypackage

patch_modules = [baz]


def apply_patches():
    [getattr(patch_module, "patch")() for patch_module in patch_modules]

from patch_manifest import PATCH_MODULES
from types import ModuleType


def _invoke_patch_hook(patch_module: ModuleType):
    patch_hook = "patch_hook"
    assert hasattr(
        patch_module, patch_hook
    ), f"{patch_module.__name__} does not have the patch hook defined!"
    getattr(patch_module, patch_hook)()


def _invoke_patch_hooks():
    [_invoke_patch_hook(module) for module in PATCH_MODULES]


# automatically apply patches when this library is imported
_invoke_patch_hooks()

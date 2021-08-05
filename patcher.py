from importlib import import_module
from collections import namedtuple
from types import ModuleType

# patch modules import
import patch_package.baz as baz

PatchMap = namedtuple("patch_module_map", ["target_module", "patch_module"])

patch_maps = [PatchMap("mypackage.foo", baz)]


def import_and_patch(target_module: str, patch_module: ModuleType):
    import_module(target_module)
    assert hasattr(
        patch_module, "patch"
    ), f"{patch_module.__name__} does not have the patch hook defined!"
    getattr(patch_module, "patch")()


def apply_patches():
    [import_and_patch(*patch_module_map) for patch_module_map in patch_maps]

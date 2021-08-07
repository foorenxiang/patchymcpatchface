"""patchymcpatchface inner guts"""
import sys
import os
from functools import lru_cache
from importlib import import_module
from types import ModuleType
import logging

sys.path.append(os.getcwd())
logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def patch_apply(target_object_ancestry: str, patch_object, debug=False):
    """Called by the patch hooks in the patch modules

    Args:
        target_object_ancestry (str): the reference to the original python object to be patched
        patch_object (Any): the object that will overwrite the original object, patching it
    """
    object_heritage = target_object_ancestry.split(".")
    package = object_heritage[0]
    anticipated_target_module_ancestry = ".".join(object_heritage[:-1])

    def resolve_and_import(module_string):
        try:
            import_module(module_string)
        except ModuleNotFoundError:
            if debug:
                print(f"{module_string} could not be imported")
            anticipated_target_module_ancestry = ".".join(module_string.split(".")[:-1])
            if debug:
                print(f"Trying {module_string}")
            if anticipated_target_module_ancestry == module_string:
                raise
            resolve_and_import(anticipated_target_module_ancestry)

    resolve_and_import(anticipated_target_module_ancestry)

    def assign_patch(obj, attr):
        try:
            next_attr = next(object_heritage_iter)
            assign_patch(getattr(obj, attr), next_attr)
        except StopIteration:
            object_parent = obj
            target_object = attr
            assert hasattr(
                object_parent, target_object
            ), f"{target_object} does not exist in {object_parent}!"
            setattr(object_parent, target_object, patch_object)

    object_heritage_iter = iter(object_heritage[1:])
    assign_patch(sys.modules[package], next(object_heritage_iter))


def _invoke_patch_hook(patch_module: ModuleType):
    """Calls the patch hook attribute inside the patch module

    Args:
        patch_module (ModuleType): The module containing the patch
    """
    patch_hook = "patch_hook"
    assert hasattr(
        patch_module, patch_hook
    ), f"{patch_module.__name__} does not have the patch hook defined!"
    getattr(patch_module, patch_hook)()


def invoke_patch_hooks(patch_modules=None):
    """Loops through all the patch modules imported to allow invoke_patch_hook to call their hook

    Args:
        PATCH_MODULES (list, optional): List of patch modules imported. Defaults to [].
    """
    if patch_modules:
        _ = [_invoke_patch_hook(module) for module in patch_modules]
        return
    logger.warning("No patch modules provided!")


try:
    from patch_manifest import PATCH_MODULES

    invoke_patch_hooks(PATCH_MODULES)
except ModuleNotFoundError:
    pass

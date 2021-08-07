import sys
import os
from functools import lru_cache
from importlib import import_module
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
            anticipated_target_module_ancestry = ".".join(module_string.split(".")[:-1])
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

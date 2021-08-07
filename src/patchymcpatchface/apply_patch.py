import sys
import os
from functools import lru_cache
from importlib import import_module
import logging
from typing import Union, Iterable, Tuple

sys.path.append(os.getcwd())
logger = logging.getLogger(__name__)


def patch_apply(
    target_object_ancestry: Union[str, Iterable[Tuple[object, str]]],
    patch_object: object,
):
    """Interface for patching objects

    Args:
        target_object_ancestry (Union[str, Iterable[object, str]]):
            Accepts two kinds of arguments:
            a) String containing the full ancestry of the target object
            e.g. my_target_package.my_target_module.target_object_to_be_patched
            b) An iterable with:
                Index 0: Parent object of the object to be patched
                Index 1: Name of target object to be patched, as a string

        patch_object (object): Object used to patch the target
    """
    if isinstance(target_object_ancestry, str):
        patch_apply_string(target_object_ancestry, patch_object)
        return
    if isinstance(target_object_ancestry, Iterable):
        patch_apply_object(*target_object_ancestry, patch_object)
        return


@lru_cache(maxsize=None)
def patch_apply_string(target_object_ancestry: str, patch_object):
    """Patches the target object
    Called by the patch hooks in the patch modules

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


def patch_apply_object(parent_object: object, target_object: str, patch_object: object):
    """Directly patches the parent object fed in

    Args:
        parent_object (object): parent object to be directly modified
        target_object (str): name of target object, to be used as attribute accessor of parent_object
        patch_object (object): object used to patch target object
    """
    assert hasattr(
        parent_object, target_object
    ), f"{repr(parent_object)} does not have attribute {target_object}!"
    setattr(parent_object, target_object, patch_object)

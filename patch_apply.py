from functools import lru_cache
import sys
from importlib import import_module


"""
# patch hook sample
def patch_hook():
    from patch_apply import patch_apply

    patch_apply("mypackage.foobar.target_function2", patch_function)
"""


@lru_cache(maxsize=None)
def patch_apply(target_object_ancestry: str, patch_object):
    object_heritage = target_object_ancestry.split(".")
    package = object_heritage[0]
    target_module_ancestry = ".".join(object_heritage[:-1])

    import_module(target_module_ancestry)

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

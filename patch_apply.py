import sys
from importlib import import_module


"""
# patch hook sample
def patch_hook():
    from patch_apply import patch_apply

    patch_apply("mypackage.foobar.target_function2", patch_function)
"""


def patch_apply(target_object: str, patch_object):
    object_heritage = target_object.split(".")
    target_module = ".".join(object_heritage[:-1])
    target_object = object_heritage[-1]

    import_module(target_module)

    object_heritage_iter = iter(object_heritage)

    def assign_patch(
        obj=sys.modules[next(object_heritage_iter)],
        attr: str = next(object_heritage_iter),
    ):
        try:
            assign_patch(getattr(obj, attr), next(object_heritage_iter))
        except StopIteration:
            assert hasattr(
                obj, attr
            ), f"{target_object} does not exist in {target_module}!"
            setattr(obj, attr, patch_object)

    assign_patch()

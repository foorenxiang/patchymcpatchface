from pathlib import Path
import sys


def as_module(relative_path: str, patch_object_in_module: str):
    assert isinstance(
        relative_path, str
    ), "'relative_path' argument should be provided as a string!"
    assert isinstance(
        patch_object_in_module, str
    ), "'patch_object_in_module' argument should be provided as a string!"
    system_parent_separator = "\\" if sys.platform.startswith("win") else "/"
    module_heritage = str(Path(relative_path)).replace(system_parent_separator, ".")[
        : -len(Path(relative_path).suffix)
    ]
    target = f"{module_heritage}.{patch_object_in_module}"
    return target

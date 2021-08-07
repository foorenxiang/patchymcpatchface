"""Contains a patchymcpatchface patch module manifest for custom invocation"""
#  import your patch modules here and document them in PATCH_MODULES below
from typing import List
from types import ModuleType
import patching_example.patch_package.baz as baz
import patching_example.patch_package.foobaz as foobaz

#  update this list with modules that contain patch_hook
PATCH_MODULES: List[ModuleType] = [
    baz,
    foobaz,
]

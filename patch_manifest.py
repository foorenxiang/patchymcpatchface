#  import your patch modules here and document them in PATCH_MODULES below
# this would be a default script
import patching_example.patch_package.baz as baz
from typing import List
from types import ModuleType

#  update this list with modules that contain patch_hook
PATCH_MODULES: List[ModuleType] = [
    baz,
]

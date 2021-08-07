"""Hooks definition"""

import sys
import os
from types import ModuleType
import logging

sys.path.append(os.getcwd())
logger = logging.getLogger(__name__)


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

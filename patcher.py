from types import ModuleType
from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)


def _invoke_patch_hook(patch_module: ModuleType):
    patch_hook = "patch_hook"
    assert hasattr(
        patch_module, patch_hook
    ), f"{patch_module.__name__} does not have the patch hook defined!"
    getattr(patch_module, patch_hook)()


def invoke_patch_hooks(PATCH_MODULES=[]):
    if PATCH_MODULES:
        [_invoke_patch_hook(module) for module in PATCH_MODULES]
        return
    logger.warning("No patch modules provided!")


def _patch_on_import():
    """Patch from default patch manifest module in project root if available, on module import"""
    if (Path(os.getcwd()) / "patch_manifest.py").exists():
        from patch_manifest import PATCH_MODULES

        invoke_patch_hooks(PATCH_MODULES)


_patch_on_import()

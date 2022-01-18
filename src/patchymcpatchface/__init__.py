"""patchymcpatchface inner guts"""
import sys
import os
import logging
from patchymcpatchface.hooks import invoke_patch_hooks
from patchymcpatchface.apply_patch import patch_apply
from patchymcpatchface.utils.as_module import as_module

__all__ = ["invoke_patch_hooks", "patch_apply", "as_module"]

sys.path.append(os.getcwd())
logger = logging.getLogger(__name__)

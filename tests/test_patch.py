"""Tests for patchymcpatchface"""
import sys
import os

sys.path.append(os.getcwd())
from patching_example import patching_example


def test_main():
    """Run sample as test, as it is inherently self testing"""

    patching_example.main()

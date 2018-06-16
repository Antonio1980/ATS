# !/usr/bin/env python
# -*- coding: utf8 -*-

import platform
from src.base.enums import OperationSystem


def detect_os():
    """
    Checks the Operational Sysytem.
    :return: String with OS name.
    """
    if _is_mac():
        return OperationSystem.DARWIN.value
    elif _is_win():
        return OperationSystem.WINDOWS.value
    elif _is_lin():
        return OperationSystem.LINUX.value
    else:
        raise Exception("The OS is not detected")


def _is_mac():
    return platform.system().lower() == OperationSystem.DARWIN.value


def _is_win():
    return platform.system().lower() == OperationSystem.WINDOWS.value


def _is_lin():
    return platform.system().lower() == OperationSystem.LINUX.value
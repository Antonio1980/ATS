# !/usr/bin/env python
# -*- coding: utf8 -*-

import platform
from src.base.enums import OperationSystem


def detect_os():
    if (is_mac()):
        return OperationSystem.MAC
    elif (is_win()):
        return OperationSystem.WINDOWS
    elif (is_lin()):
        return OperationSystem.LINUX
    else:
        raise Exception("The OS is not detected")


def is_mac():
    return platform.system().lower() == OperationSystem.DARWIN


def is_win():
    return platform.system().lower() == OperationSystem.WINDOWS


def is_lin():
    return platform.system().lower() == OperationSystem.LINUX




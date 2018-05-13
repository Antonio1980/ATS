# !/usr/bin/env python
# -*- coding: utf8 -*-

import platform


def detect_os():
    if (is_mac()):
        return "macintosh"
    elif (is_win()):
        return "windows"
    elif (is_lin()):
        return "linux"
    else:
        raise Exception("The OS not detected")


def is_mac():
    return platform.system().lower() == "darwin"


def is_win():
    return platform.system().lower() == "windows"


def is_lin():
    return platform.system().lower() == "linux"




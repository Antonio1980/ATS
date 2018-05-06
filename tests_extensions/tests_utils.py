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
    if platform.system().lower() == "darwin":
        return True


def is_win():
    if platform.system().lower() == "windows":
        return True


def is_lin():
    if platform.system().lower() == "linux":
        return True

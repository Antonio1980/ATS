"""
Author: Anton Shipulin.
Created: 01.08.2018
Version: 1.05
"""

from enum import Enum


class Browsers(Enum):
    CHROME = "chrome"
    IE = "ie"
    FIREFOX = "firefox"
    SAFARI = "safari"
    IE_EDGE = "ie_edge"


class OperationSystem(Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    MAC = "macintosh"
    DARWIN = "darwin"


class DriverHelper(Enum):
    ID = "id"
    XPATH = "xpath"
    CLASS_NAME = "class_name"
    NAME = "name"
    TAG_NAME = "tag_name"
    LINK_TEXT = "link_text"
    CSS_SELECTOR = "css_selector"
    PARTIAL_LINK_TEXT = "partial_link_text"

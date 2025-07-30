import swibots
from enum import Enum
from swibots.base import SwitchObject
from swibots.utils.types import JSONDict
from typing import Dict, Any


class ScreenType(Enum):
    BOTTOM = "bottom"
    SCREEN = "screen"


class TextSize(Enum):
    SMALL = "x"
    MEDIUM = "x_large"
    LARGE = "xx_large"
    BODY = "body"
    BOLD = "bold_body"
    MARKDOWN = "markdown"


class Expansion(Enum):
    DEFAULT = "default_expansion"
    # TODO: Remove FLEXIBLE, EXPAND
    FLEXIBLE = "flexible_expansion"
    EXPAND = "expanded_expansion"

    VERTICAL = "expanded_expansion"
    HORIZONTAL = "flexible_expansion"


class Component(SwitchObject):
    type = None


class Icon(Component):
    type = "icon"

    def __init__(
        self, url: str, dark_url: str = None, text: str = "", callback_data: str = None
    ):
        self.url = url
        self.dark_url = dark_url or url
        self.text = text
        self.callback_data = callback_data

    def to_json(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "name": self.url,
            "darkIcon": self.dark_url,
            "alt": self.text,
            "callbackData": self.callback_data,
        }


class Text(Component):
    type = "text"

    def __init__(
        self,
        text: str,
        size: TextSize = TextSize.BODY,
        opacity: float = 1,
        color: str = None,
        max_size: bool = None,
    ):
        self.text = text
        self.size = size
        self.opacity = opacity
        self.color = color
        self.max_size = max_size

    def to_json(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "text": self.text,
            "textType": self.size.value,
            "color": self.color,
            "mainAxisSize": "max" if self.max_size else "min",
        }


class Image(Component):
    type = "image"

    def __init__(
        self,
        url: str,
        callback_data: str = None,
        dark_url: str = None,
        max_size: bool = None,
    ):
        self.url = url
        self.callback_data = callback_data
        self.dark_url = dark_url or url
        self.max_size = max_size

    def to_json(self):
        data = {
            "type": self.type,
            "mediaUrl": self.url,
            "darkMediaUrl": self.dark_url,
            "mainAxisSize": "max" if self.max_size else "min",
        }
        if self.callback_data:
            data["callbackData"] = self.callback_data
        return data


class Spacer(Component):
    type = "spacer"

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def to_json(self):
        return {"type": self.type, "x": self.x, "y": self.y}


class Badge(Component):
    type = "badge"

    def __init__(self, text: str, background: str = None, text_color: str = None):
        self.text = text
        self.background = background
        self.text_color = text_color

    def to_json(self):
        return {
            "type": self.type,
            "text": self.text,
            "textColor": self.text_color,
            "background": self.background,
        }

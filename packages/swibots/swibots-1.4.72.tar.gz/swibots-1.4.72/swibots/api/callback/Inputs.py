from swibots.utils.types import JSONDict
from .types import Component, Icon
from typing import Optional, List

from enum import Enum


class KeyboardType(Enum):
    NUMBER = "number"
    TEXT = "text"
    EMAIL = "email"
    URL = "url"


class TextInput(Component):
    type = "input_box"

    def __init__(
        self,
        label: str,
        value: str = "",
        width: int = 0,
        placeholder: Optional[str] = "",
        callback_data: Optional[str] = "",
        keyboardType: KeyboardType = KeyboardType.TEXT,
        error: bool = False,
        error_text: Optional[str] = "",
        password: bool = False,
        right_icon: Optional[Icon] = None,
        left_icon: Optional[Icon] = None,
        multiline: bool = False,
        expanded: bool = False,
        max_size: bool = None,
    ):
        self.label = label
        self.width = width
        self.value = value
        self.placeholder = placeholder
        self.callback_data = callback_data
        self.keyboard_type = keyboardType
        self.error = error
        self.error_text = error_text
        self.password = password
        self.multiline = multiline
        self.expanded = expanded
        self.max_size = max_size

        if isinstance(right_icon, str):
            right_icon = Icon(right_icon)
        self.right_icon = right_icon

        if isinstance(left_icon, str):
            left_icon = Icon(left_icon)
        self.left_icon = left_icon

    def to_json(self):
        data = {
            "type": self.type,
            "label": self.label,
            "width": self.width,
            "value": self.value,
            "placeholder": self.placeholder,
            "callbackData": self.callback_data,
            "keyboardType": self.keyboard_type.value,
            "error": self.error,
            "errorText": self.error_text,
            "password": self.password,
        }
        if self.right_icon:
            data["rightIcon"] = self.right_icon.to_json()
        if self.left_icon:
            data["leftIcon"] = self.left_icon.to_json()
        if self.multiline:
            data["expansion"] = "flexible_expansion"
        elif self.expanded:
            data["expansion"] = "expanded_expansion"

        data["mainAxisSize"] = "max" if self.max_size else "min"
        return data


class FilePicker(Component):
    type = "file_picker"

    def __init__(
        self,
        callback_data: str,
        files_count: int = 1,
        mime_type: List[str] = ["png", "jpg", "jpeg", "webp"],
        max_size: bool = None,
    ):
        self.callback_data = callback_data
        self.files_count = files_count
        self.mime_type = mime_type
        self.max_size = max_size

    def to_json(self):
        return {
            "type": self.type,
            "callbackData": self.callback_data,
            "numberOfFiles": self.files_count,
            "mimeType": self.mime_type,
            "mainAxisSize": "max" if self.max_size else "min",
        }

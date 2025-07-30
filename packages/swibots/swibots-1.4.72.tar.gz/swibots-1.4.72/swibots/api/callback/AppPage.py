import swibots
from swibots.base import SwitchObject
from logging import getLogger
from swibots.utils.types import JSONDict
from .types import ScreenType, Component, Icon, Text
from typing import List, Optional, Dict, Any, Union
from .BottomBar import BottomBar
from .ListView import ListView

LOG = getLogger(__name__)


class AppBar(SwitchObject):
    def __init__(
        self,
        title: str = "App",
        subtitle: str = "",
        left_icon: Union[Icon, str] = Icon(
            "https://raw.githubusercontent.com/switchcollab/Switch-Bots-Python-Library/main/docs/static/img/logo.png"
        ),
        secondary_icon: Union[Icon, str] = None,
        tertiary_icon: Union[Icon, str] = "",
    ):
        self.title = title
        self.subtitle = subtitle

        if isinstance(left_icon, str):
            left_icon = Icon(left_icon)
        self.left_icon = left_icon

        if isinstance(secondary_icon, str):
            secondary_icon = Icon(secondary_icon)
        self.secondary_icon = secondary_icon

        if isinstance(tertiary_icon, str):
            tertiary_icon = Icon(tertiary_icon)
        self.tertiary_icon = tertiary_icon

    def to_json(self) -> JSONDict:
        data = {"title": self.title, "subtitle": self.subtitle}
        if self.left_icon:
            data["leftIcon"] = self.left_icon.to_json()
        if self.secondary_icon:
            data["secondaryIcon"] = self.secondary_icon.to_json()
        if self.tertiary_icon:
            data["tertiaryIcon"] = self.tertiary_icon.to_json()
        return data


class AppPage(SwitchObject):
    def __init__(
        self,
        app: "swibots.App" = None,
        screen: ScreenType = ScreenType.SCREEN,
        components: List[Component] = None,
        app_bar: AppBar = None,
        bottom_bar: BottomBar = None,
        show_continue: bool = True,
        back_action: str = None,
        disable_appbar: bool = False,
        max_size: bool = True,
        on_close: str = None,
        **kwargs
    ):
        super().__init__(app)
        self.type = "appPage"
        self.screen = screen
        self.back_action = back_action
        layouts = kwargs.get("layouts")
        self.components = components or []
        if layouts:
            self.components.extend(layouts)
        self.disable_appbar = disable_appbar
        self.app_bar = app_bar
        self.bottom_bar = bottom_bar
        self.show_continue = show_continue
        self.max_size = max_size
        self.on_close = on_close

    def to_json(self) -> JSONDict:
        components = []
        for component in self.components:

            if isinstance(component, ListView):
                if self.max_size != None:
                    component.max_size = self.max_size
                parsed = component.to_json_request()
                if isinstance(parsed, list):
                    components.extend(parsed)
                else:
                    components.append(parsed)
            elif isinstance(component, Component):
                componentJson = component.to_json()
                if self.max_size != None:
                    componentJson["mainAxisSize"] = "max" if self.max_size else "min"
                components.append(componentJson)
            elif isinstance(component, str):
                components.append(Text(component))

        data = {
            "type": self.type,
            "mode": self.screen.value,
            "components": components,
        }
        if not self.disable_appbar and self.app_bar:
            data["pageBar"] = self.app_bar.to_json()
        if self.bottom_bar:
            data.update(self.bottom_bar.to_json())
        if self.show_continue:
            data["showContinue"] = self.show_continue
        if self.back_action:
            data["pageId"] = self.back_action
        if self.on_close:
            data["onClose"] = self.on_close
        return data

    def from_json(self, data: dict) -> Any:
        if data is not None:
            self.screen = ScreenType(data.get("mode", "screen"))
            self.disable_appbar = data.get("disable_appbar", False)
            self.show_continue = data.get("showContinue", True)
            self.back_action = data.get("pageId")
            self.on_close = data.get("onClose")
            self.max_size = data.get("maxSize")
            self.app_bar = AppBar().from_json(data.get("pageBar"))
            self.bottom_bar = BottomBar().from_json(data)
            self.components = [
                Component.build_from_json(item) for item in data.get("components", [])
            ]

        return self

import json
from typing import Generic, List, Optional, TypeVar
import swibots
from swibots.utils.types import JSONDict


T = TypeVar("T")


class SwitchObject(Generic[T]):
    def __init__(self, app: "swibots.App" = None, **kwargs):
        self._app = app
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def app(self) -> "swibots.App":
        return self._app

    @classmethod
    def build_from_json(
        cls, data: Optional[JSONDict] = None, app: Optional["swibots.App"] = None
    ) -> Optional[T]:
        if data is None:
            return None
        return cls(app).from_json(data)

    @classmethod
    def build_from_json_list(
        cls, data: Optional[JSONDict], app: Optional["swibots.App"] = None
    ) -> List[T]:
        return [cls.build_from_json(item, app) for item in data]

    def to_json_request(self) -> JSONDict:
        return self.to_json()

    def to_json(self) -> JSONDict:
        return self.__dict__

    def from_json(self, data: Optional[JSONDict]) -> T:
        if data:
            for key, value in data.items():
                setattr(self, key, value)
        return self

    def update(self, data: Optional[JSONDict]) -> T:
        new_data = self.to_json()
        new_data.update(data)
        return self.__class__.build_from_json(new_data, self.app)

    def copy(self):
        """Create a copy of object"""
        return self.__class__.build_from_json(self.to_json(), self.app)

    def __repr__(self) -> str:
        filter_dict = {
            x: (
                y.to_json()
                if hasattr(y, "to_json")
                else (y if isinstance(y, (str, dict, int)) else str(y))
            )
            for x, y in self.__dict__.items()
            if y and x != "_app"
        }
        return f"{self.__class__.__name__} {json.dumps(filter_dict, indent=1)}"

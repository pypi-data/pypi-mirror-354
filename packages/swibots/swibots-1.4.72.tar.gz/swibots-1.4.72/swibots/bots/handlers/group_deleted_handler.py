from typing import TYPE_CHECKING, Optional, TypeVar
from swibots.api.chat.events import MessageEvent
from swibots.api.community.events import GroupDeletedEvent
from swibots.bots.filters.filter import Filter

from swibots.bots.handlers import BaseHandler
from swibots.bots import BotContext
from .event_handler import EventHandler
from swibots.types import EventType
from swibots.utils.types import HandlerCallback

if TYPE_CHECKING:
    pass

ResType = TypeVar("ResType")


class GroupDeletedHandler(EventHandler):
    def __init__(
        self,
        callback: HandlerCallback[BotContext[GroupDeletedEvent], ResType],
        filter: Optional[Filter] = None,
        **kwargs,
    ):
        super().__init__(EventType.COMMUNITY_GROUP_DELETE, callback, filter, **kwargs)

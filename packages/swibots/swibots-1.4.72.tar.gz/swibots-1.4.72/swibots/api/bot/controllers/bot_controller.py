import json
import logging
from typing import TYPE_CHECKING, List, Optional
from swibots.api.bot.models import BotInfo
from swibots.errors import SwitchError
from swibots.utils.types import JSONDict
from swibots.api.callback import AppPage

if TYPE_CHECKING:
    from swibots.api.bot import BotClient

log = logging.getLogger(__name__)

BASE_PATH = "/v1/bots"


class BotController:
    """Bot controller

    This controller is used to communicate with the bot endpoints.
    """

    def __init__(self, client: "BotClient"):
        self.client = client

    async def get_bot_info(self, bot_id: str) -> BotInfo:
        """Get bot info

        Parameters:
            bot_id (``str``): The bot id. Defaults to the current bot id.

        Returns:
            :obj:``~switch.api.bot.models.BotInfo``: The bot info
        """
        if bot_id is None:
            bot_id = self.client.user.id
        response = await self.client.get(BASE_PATH + "?botId=" + str(bot_id))
        return BotInfo.build_from_json(response.data)

    async def update_bot_info(self, bot_info: BotInfo) -> BotInfo:
        """Update bot info

        Parameters:
            bot_info (``~switch.api.bot.models.BotInfo``): The bot info to update

        Returns:
            :obj:``~switch.api.bot.models.BotInfo``: The bot info
        """
        data = bot_info.to_json_request()
        if "preview" in data:
            data["preview"] = json.dumps(data["preview"])
        response = await self.client.put(f"{BASE_PATH}/update", data=data)
        return BotInfo.build_from_json(response.data)

    async def delete_bot_info(self, bot_id: str) -> bool:
        """Delete bot info

        Parameters:
            bot_id (``str``): The bot id. Defaults to the current bot id.

        Returns:
            ``bool``: True if the bot was deleted
        """
        response = await self.client.delete(f"{BASE_PATH}/{bot_id}")
        return True

    async def answer_callback_query(
        self,
        callback_id: str,
        text: str,
        url: Optional[str] = None,
        message_id: Optional[int] = 0,
        show_alert: Optional[bool] = False,
        cache_time: Optional[int] = None,
        app_session_id: Optional[str] = None,
    ) -> bool:
        response = await self.client.post(
            f"{BASE_PATH}/callback/answer",
            data={
                "type": "callback",
                "callbackQueryId": callback_id,
                "messageId": str(message_id),
                "text": text,
                "url": url,
                "showAlerts": show_alert,
                "cacheTime": cache_time,
                "appSessionId": app_session_id,
            },
        )
        return response.data

    async def answer_ui_query(
        self, callback_id: str, message_id: int, callback: AppPage, app_session_id: str
    ) -> bool:
        default_bar = self.client.app.app_bar
        if not callback.app_bar and default_bar:
            callback.app_bar = default_bar
        data = callback.to_json_request()
        data.update(
            {
                "appSessionId": app_session_id,
                "callbackQueryId": callback_id,
                "messageId": message_id,
            }
        )
        response = await self.client.post(f"{BASE_PATH}/callback/answer", data=data)
        return response.data

    async def set_welcome(
        self,
        text: str = None,
        thumb: str = None,
        button: str = None,
        command: str = None,
    ):
        response = await self.client.post(
            f"{BASE_PATH}/set-intro-message",
            data={
                "botId": str(self.client.user.id),
                "welcomeImage": thumb,
                "welcomeText": text,
                "buttonName": button,
                "buttonCommand": command,
            },
        )
        return self.client.build_object(BotInfo, response.data)

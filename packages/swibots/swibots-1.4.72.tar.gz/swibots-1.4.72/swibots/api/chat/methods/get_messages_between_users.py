from typing import List
import swibots
from swibots.api.chat.models import Message


class GetMessagesBetweenUsers:
    async def get_messages_between_users(
        self: "swibots.ApiClient",
        other_user_id: int,
        user_id: int = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Message]:
        """Get messages between users

        Parameters:
            other_user_id (``int``): The other user id.
            user_id (``int``, *optional*): The user id. Defaults to the current user id.
            limit (``int``, *optional*): The maximum number of messages to retrieve. Defaults to 100.
            offset (``int``, *optional*): The offset. Defaults to 0.

        Returns:
            ``List[~switch.api.chat.models.Message]``: The messages

        Raises:
            ``~switch.error.SwitchError``: If the messages could not be retrieved

        This function does the same as :meth:`~switch.api.chat.controllers.MessageController.get_messages_between_users`.
        """
        return await self.chat_service.messages.get_messages_between_users(
            other_user_id, user_id, limit, offset
        )

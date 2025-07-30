from typing import Callable
import swibots
from swibots.bots.filters.filter import Filter


class OnChannelCreated:
    def on_channel_created(
        self: "swibots.Client" = None, filter: Filter = None
    ) -> Callable:
        """Decorator for handling channel creations."""

        def decorator(func: Callable) -> Callable:
            if isinstance(self, swibots.Client):
                self.add_handler(
                    swibots.bots.handlers.ChannelCreatedHandler(func, filter)
                )

            return func

        return decorator

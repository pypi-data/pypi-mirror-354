from typing import Callable, Optional
import swibots
from swibots.bots.filters.filter import Filter


class OnCommunityUpdated:
    def on_community_update(
        self: "swibots.Client" = None, filter: Optional[Filter] = None
    ) -> Callable:
        """Decorator for handling new commands."""

        def decorator(func: Callable) -> Callable:
            if isinstance(self, swibots.Client):
                self.add_handler(
                    swibots.bots.handlers.CommunityUpdatedHandler(func, filter)
                )

            return func

        return decorator

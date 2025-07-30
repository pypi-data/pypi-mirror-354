from typing import Callable, Optional
import swibots
from swibots.bots.filters.filter import Filter


class OnGroupCreated:
    def on_group_created(
        self: "swibots.Client" = None, filter: Optional[Filter] = None
    ) -> Callable:
        """Decorator for handling group creations."""

        def decorator(func: Callable) -> Callable:
            if isinstance(self, swibots.Client):
                self.add_handler(
                    swibots.bots.handlers.GroupCreatedHandler(func, filter)
                )

            return func

        return decorator

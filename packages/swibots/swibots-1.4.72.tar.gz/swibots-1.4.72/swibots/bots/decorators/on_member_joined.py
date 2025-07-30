from typing import Callable, Optional
import swibots
from swibots.bots.filters.filter import Filter


class OnMemberJoined:
    def on_member_joined(
        self: "swibots.Client" = None, filter: Optional[Filter] = None
    ) -> Callable:
        """Decorator for handling members joins."""

        def decorator(func: Callable) -> Callable:
            if isinstance(self, swibots.Client):
                self.add_handler(
                    swibots.bots.handlers.MemberJoinedHandler(func, filter)
                )

            return func

        return decorator

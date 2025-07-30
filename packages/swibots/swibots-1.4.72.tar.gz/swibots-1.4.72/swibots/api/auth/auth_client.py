from typing import Type, TypeVar
import swibots
from swibots.api.auth.models import AuthUser, AuthResult
from swibots.base import SwitchRestClient
from swibots.config import get_config


T = TypeVar("T", bound="swibots.AuthUser")


class AuthClient(SwitchRestClient):
    """Auth client

    This client is used to communicate with the auth service.

    Controllers:
        - :attr:`users`: :obj:`~switch.api.auth.controllers.UserController` : The users controller
    """

    def __init__(self, app: "swibots.App", base_url: str = None):
        """Initialize the auth client"""
        base_url = base_url or get_config()["AUTH_SERVICE"]["BASE_URL"]
        super().__init__(app, base_url)
        self._authorization = None

    def prepare_request_headers(self, headers: dict) -> dict:
        headers = super().prepare_request_headers(headers)
        if self.token is not None:
            headers["authtoken"] = f"{self.token}"
        return headers

    def get_me_sync(self, user_type: Type[T] = AuthUser) -> T:
        user_info = self.sync_get("/api/user").data
        return self.build_object(user_type, user_info)

    async def get_me(self, user_type: Type[T] = AuthUser) -> T:
        """Get the current user

        Parameters:
            user_type (``Type[T]``, *optional*): The user type to return. Defaults to :obj:`~switch.api.auth.models.AuthUser`.

        Returns:
            ``T``: The current user

        This functions does the same as :meth:`~switch.api.auth.controllers.UserController.me`.

        """
        response = await self.get("/api/user")
        return self.build_object(user_type, response.data)

    def login(self, email: str, password: str):
        response = self.sync_post(
            "/api/login", data={"email": email, "password": password}
        )
        return self.build_object(AuthResult, response.data)

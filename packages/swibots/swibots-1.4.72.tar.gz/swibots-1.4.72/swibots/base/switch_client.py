import json
from typing import List, Tuple, Type, TypeVar
import swibots, httpx
from swibots.errors import (
    NetworkError,
    UnAuthorized,
    InvalidRouteCall,
    BadRequest,
    ServerError,
)
from swibots.utils import RestClient
from swibots.utils.types import JSONDict
from swibots.base import RestResponse
from logging import getLogger

T = TypeVar("T", bound="swibots.SwitchObject")
LOG = getLogger(__name__)


class SwitchRestClient(RestClient):
    def __init__(
        self, app: "swibots.Client" = None, base_url: str = None, token: str = None
    ):
        super().__init__()
        self._app = app
        self._auth_token = token
        self._base_url = base_url

    @property
    def app(self) -> "swibots.Client":
        return self._app

    @app.setter
    def app(self, app: "swibots.Client"):
        self._app = app

    @property
    def token(self):
        return self._app.token

    @property
    def user(self) -> "swibots.AuthUser":
        return self._app.user

    @property
    def base_url(self, url: str):
        self._base_url = url

    @base_url.setter
    def base_url(self, url: str):
        self._base_url = url

    def build_object(self, obj_type: Type[T], data: JSONDict) -> T:
        return obj_type.build_from_json(data, self.app)

    def build_list(self, obj_type: Type[T], data: JSONDict) -> List[T]:
        return obj_type.build_from_json_list(data, self.app)

    def sync_post(self, url: str, data: dict = None, headers: dict = None):
        request = httpx.post(
            self._base_url + url,
            data=data,
            headers=self.prepare_request_headers(headers),
        )
        return self.parse_response((request.status_code, request.content))

    def sync_get(self, url: str, headers: dict = None) -> RestResponse[JSONDict]:
        request = httpx.get(
            self._base_url + url, headers=self.prepare_request_headers(headers)
        )
        return self.parse_response((request.status_code, request.content))

    async def get(
        self, url: str, data: dict = None, headers: dict = None
    ) -> RestResponse[JSONDict]:
        """See :meth:`BaseRequest.get`."""
        return await self.do_request(url, "GET", data, headers=headers)

    async def post(
        self,
        url: str,
        data: dict = None,
        form_data=None,
        files=None,
        headers: dict = None,
    ) -> RestResponse[JSONDict]:
        """See :meth:`BaseRequest.post`."""
        return await self.do_request(url, "POST", data, form_data, files, headers)

    async def put(
        self,
        url: str,
        data: dict = None,
        form_data=None,
        files=None,
        headers: dict = None,
    ) -> RestResponse[JSONDict]:
        """See :meth:`BaseRequest.put`."""
        return await self.do_request(url, "PUT", data, form_data, files, headers)

    async def delete(
        self, url: str, data: dict = None, headers: dict = None
    ) -> RestResponse[JSONDict]:
        """See :meth:`BaseRequest.delete`."""
        return await self.do_request(url, "DELETE", data, headers=headers)

    async def patch(
        self,
        url: str,
        data: dict = None,
        form_data=None,
        files=None,
        headers: dict = None,
    ) -> RestResponse[JSONDict]:
        """See :meth:`BaseRequest.patch`."""
        return await self.do_request(url, "PATCH", data, form_data, files, headers)

    async def head(
        self, url: str, data: dict = None, headers: dict = None
    ) -> RestResponse[JSONDict]:
        """See :meth:`BaseRequest.head`."""
        return await self.do_request(url, "HEAD", data, headers)

    async def options(
        self, url: str, data: dict = None, headers: dict = None
    ) -> RestResponse[JSONDict]:
        """See :meth:`BaseRequest.options`."""
        return await self.do_request(url, "OPTIONS", data, headers)

    def parse_response(self, response: Tuple[int, bytes]) -> RestResponse[JSONDict]:
        decoded_s = response[1].decode("utf-8", "replace")
        try:
            jsonObject = json.loads(decoded_s)
        except ValueError as exc:
            jsonObject = decoded_s

        response = RestResponse(jsonObject, response[0], {})
        if response.is_error:
            error = response.error_message
            if ":" in error:
                error = error.split(":", maxsplit=1)[-1].strip().replace("'", '"')
                try:
                    errorJson = json.loads(error)
                    error = errorJson["message"]
                    if errorJson.get("status") == "BAD_REQUEST":
                        raise BadRequest(error)
                except (KeyError, json.JSONDecodeError):
                    pass
            if response.status_code == 401:
                raise UnAuthorized(error)
            elif response.status_code == 404:
                raise InvalidRouteCall(error)
            elif response.status_code == 503:
                raise ServerError(error)
            raise NetworkError(error)
        return response

    def prepare_request_data(self, data: dict) -> dict:
        return super().prepare_request_data(data)

    def prepare_request_headers(self, headers: dict) -> dict:
        headers = super().prepare_request_headers(headers)
        if self.token is not None:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def do_request(
        self,
        path: str,
        method: str,
        data: dict = None,
        form_data=None,
        files=None,
        headers: dict = None,
    ) -> RestResponse[JSONDict]:
        data = self.prepare_request_data(data)
        headers = self.prepare_request_headers(headers)
        return self.parse_response(
            await RestClient.do_request(
                self,
                self._base_url + (path if path is not None else ""),
                method,
                data,
                form_data,
                files,
                headers,
            )
        )

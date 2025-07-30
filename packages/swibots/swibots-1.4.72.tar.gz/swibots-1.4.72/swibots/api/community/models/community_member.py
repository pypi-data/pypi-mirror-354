from typing import Optional, List
from swibots.utils.types import JSONDict
from swibots.base.switch_object import SwitchObject
from swibots.api.common.models import User
import swibots


class CommunityMember(SwitchObject):
    def __init__(
        self,
        app: "swibots.App" = None,
        admin: Optional[bool] = False,
        community_id: Optional[str] = None,
        enable_notification: Optional[bool] = None,
        id: Optional[int] = None,
        mute_channels: Optional[List[str]] = None,
        mute_groups: Optional[List[str]] = None,
        mute_notification: Optional[bool] = None,
        mute_period: Optional[str] = None,
        role_info: Optional[dict] = None,
        user_id: Optional[str] = None,
        user: Optional[User] = None,
        username: Optional[str] = None,
        request_status: Optional[str] = None,
        xp: Optional[int] = None,
        xp_spend: Optional[int] = None,
    ):
        super().__init__(app)

        self.admin = admin
        self.id = id
        self.enable_notification = enable_notification
        self.mute_notification = mute_notification
        self.community_id = community_id
        self.user_id = user_id
        self.mute_groups = mute_groups
        self.mute_channels = mute_channels
        self.mute_period = mute_period
        self.role_info = role_info
        self.user = user
        self.username = username
        self.xp = xp
        self.xp_spend = xp_spend
        self.request_status = request_status

    def to_json(self) -> JSONDict:
        return {
            "admin": self.admin,
            "communityId": self.community_id,
            "enableNotificationOnMentionAndPin": self.enable_notification,
            "id": self.id,
            "muteChannels": self.mute_channels,
            "muteGroups": self.mute_groups,
            "muteNotification": self.mute_notification,
            "mutePeriod": self.mute_period,
            "roleInfo": self.role_info,
            "userId": self.user_id,
            "userInfo": self.user.to_json() if self.user else None,
            "userName": self.username,
            "requestStatus": self.request_status,
            "xp": self.xp,
            "xpSpend": self.xp_spend,
        }

    def from_json(self, data: JSONDict = None) -> "CommunityMember":
        if data is not None:
            self.admin = data.get("admin")
            self.community_id = data.get("communityId")
            self.enable_notification = data.get("enableNotificationOnMentionAndPin")
            self.id = int(data.get("id") or 0)
            self.mute_channels = data.get("muteChannels")
            self.mute_groups = data.get("muteGroups")
            self.mute_notification = data.get("muteNotification")
            self.mute_period = data.get("mutePeriod")
            self.role_info = data.get("roleInfo")
            self.user_id = int(data.get("userId") or 0)
            self.username = data.get("userName")
            self.user = User.build_from_json(data.get("userInfo"), self.app)
            self.request_status = data.get("requestStatus")
            self.xp = data.get("xp")
            self.xp_spend = data.get("xp_spend")
        return self


class SearchResultUser(SwitchObject):
    def __init__(
        self,
        app: "swibots.App" = None,
        id: str = None,
        member_id: str = None,
        name: str = None,
        username: str = None,
        image_url: str = None,
        active: bool = None,
        deleted: bool = None,
        profile_colour: str = None,
        bot: bool = None,
    ):
        super().__init__(app)
        self.id = id
        self.member_id = member_id
        self.name = name
        self.username = username
        self.image_url = image_url
        self.active = active
        self.deleted = deleted
        self.profile_colour = profile_colour
        self.bot = bot

    def to_json(self) -> JSONDict:
        return {
            "id": self.id,
            "memberId": self.member_id,
            "name": self.name,
            "username": self.username,
            "imageUrl": self.image_url,
            "active": self.active,
            "deleted": self.deleted,
            "profileColour": self.profile_colour,
            "bot": self.bot,
        }

    def from_json(self, data: JSONDict = None) -> "SearchResultUser":
        if data is not None:
            self.id = data.get("id")
            self.member_id = data.get("memberId")
            self.name = data.get("name")
            self.username = data.get("username")
            self.image_url = data.get("imageUrl")
            self.active = data.get("active")
            self.deleted = data.get("deleted")
            self.profile_colour = data.get("profileColour")
            self.bot = data.get("bot")
        return self

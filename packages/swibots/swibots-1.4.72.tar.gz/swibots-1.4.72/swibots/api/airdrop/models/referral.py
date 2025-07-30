import swibots
from typing import Optional, Any
from swibots.base import SwitchObject
from swibots.api.common.models import User
from swibots.utils.types import JSONDict


class Referral(SwitchObject):
    def __init__(
        self,
        app: "swibots.App" = None,
        id: Optional[str] = None,
        reference_id: Optional[str] = None,
        reference_type: Optional[str] = None,
        referral_code_id: Optional[str] = None,
        refer_by: Optional[str] = None,
        refer_to: Optional[str] = None,
        status: Optional[str] = None,
        user: Optional[User] = None,
    ):
        super().__init__(app)
        self.id = id
        self.reference_id = reference_id
        self.refer_to = refer_to
        self.refer_by = refer_by
        self.referral_code_id = referral_code_id
        self.status = status
        self.user = user
        self.reference_type = reference_type

    def to_json(self) -> JSONDict:
        return {
            "id": self.id,
            "reference_id": self.reference_id,
            "refer_to": self.refer_to,
            "refer_by": self.refer_by,
            "referral_code_id": self.referral_code_id,
            "user": self.user.to_json() if self.user else None,
            "reference_type": self.reference_type,
            "status": self.status,
        }

    @classmethod
    def from_json(self, data: JSONDict = None) -> Any:
        if data:
            self.id = data.get("id")
            self.reference_id = data.get("reference_id")
            self.refer_to = data.get("refer_to")
            self.refer_by = data.get("refer_by")
            self.user = User.build_from_json(data.get("user"), self.app)
            self.referral_code_id = data.get("referral_code_id")
            self.reference_type = data.get("reference_type")
            self.status = data.get("status")
        return self

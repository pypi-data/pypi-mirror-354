import swibots
from typing import Optional, Union
from swibots.utils.types import JSONDict
from swibots.base.switch_object import SwitchObject
from swibots.types import GetMediaType


class Media(SwitchObject):
    def __init__(
        self,
        app: "swibots.App" = None,
        id: Optional[int] = None,
        caption: Optional[str] = None,
        checksum: Optional[str] = None,
        description: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        type_name: Optional[str] = None,
        source_id: Optional[bool] = None,
        media_type: Optional[Union[str, int]] = None,
        mime_type: Optional[str] = 0,
        file_name: Optional[bool] = None,
        file_size: Optional[bool] = None,
        url: Optional[bool] = None,
        owner_id: Optional[int] = None,
        owner_type: Optional[str] = None,
        premium: Optional[bool] = False,
    ):
        super().__init__(app)
        self.id = id
        self.caption = caption
        self.description = description
        self.checksum = checksum
        self.thumbnail_url = thumbnail_url
        self.source_id = source_id
        self.type_name = type_name
        self.media_type = media_type
        self.mime_type = mime_type
        self.file_name = file_name
        self.file_size = file_size
        self.owner_id = owner_id
        self.url = url
        self.owner_type = owner_type
        self.premium = premium

    @property
    def is_sticker(self) -> bool:
        return 200 <= (self.media_type) <= 202

    def to_form_data(self):
        return {
            "mediaInfo.caption": self.caption,
            "mediaInfo.description": self.description,
            "mediaInfo.checksum": self.checksum,
            "mediaInfo.fileName": self.file_name,
            "mediaInfo.fileSize": self.file_size,
            "mediaInfo.mimeType": self.mime_type,
            "mediaInfo.mediaType": self.media_type,
            "mediaInfo.url": self.url,
            "mediaInfo.thumbnailUrl": self.thumbnail_url,
            "mediaInfo.sourceUri": self.source_id,
            "mediaInfo.typeName": self.type_name,
            "mediaInfo.premium": self.premium,
        }

    def to_json(self) -> JSONDict:
        return {
            x: y
            for x, y in {
                "id": self.id,
                "caption": self.caption,
                "checksum": self.checksum,
                "description": self.description,
                "thumbnailUrl": self.thumbnail_url,
                "sourceUri": self.source_id,
                "mediaType": self.media_type,
                "mimeType": self.mime_type,
                "fileName": self.file_name,
                "fileSize": self.file_size,
                "typeName": self.type_name,
                "ownerId": self.owner_id,
                "ownerType": self.owner_type,
                "downloadUrl": self.url,
                "url": self.url,
                "premium": self.premium,
            }.items()
            if y
        }

    def from_json(self, data: Optional[JSONDict] = None) -> "Media":
        if data is not None:
            self.id = data.get("id")
            self.checksum = data.get("checksum")
            self.caption = data.get("caption")
            self.description = data.get("description")
            self.thumbnail_url = data.get("thumbnailUrl")
            self.source_id = data.get("sourceUri")
            self.media_type = data.get("mediaType")
            self.mime_type = data.get("mimeType")
            self.file_name = data.get("fileName")
            self.file_size = data.get("fileSize")
            self.url = data.get("downloadUrl")
            self.owner_id = data.get("ownerId")
            self.owner_type = data.get("ownerType")
            if isinstance(self.owner_id, str) and self.owner_id.isdigit():
                self.owner_id = int(self.owner_id)
            self.premium = data.get("premium", False)
        return self

    def to_update_request(self):
        return {
            "id": self.id,
            "checksum": self.checksum,
            "description": self.description,
            "thumbnailUrl": self.thumbnail_url,
            "sourceUri": self.source_id,
            "mediaType": GetMediaType(self.media_type),
            "mimeType": self.mime_type,
            "fileName": self.file_name,
            "fileSize": self.file_size,
            "url": self.url,
            "premium": self.premium,
        }

    async def edit(
        self,
        thumb_url: Optional[str] = None,
        url: Optional[str] = None,
        media_type: Optional[str] = None,
        file_name: Optional[str] = None,
        media: "Media" = None,
    ):
        """Update media Info

        Args:
          file_name: Caption of media
          media: Media: new media object
        """
        return await self.app.update_media_info(
            self.id,
            media=media,
            thumb_url=thumb_url,
            url=url,
            file_name=file_name,
            media_type=media_type,
        )

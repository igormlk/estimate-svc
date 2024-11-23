from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from utils.object_id import PydanticObjectId


class ServicePhotoType(Enum):
    OLD = "old"
    NEW = "new"


class PhotoType(Enum):
    VEHICLE = "vehicle"
    SERVICE = "service"


class Photo(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    filename: str
    path: Optional[str] = None
    order_id: str
    service_id: Optional[str] = None
    bucket: Optional[str] = None
    tenant_id: Optional[str] = None
    service_photo_type: Optional[ServicePhotoType] = None
    type: PhotoType

    class Config:
        use_enum_values = True

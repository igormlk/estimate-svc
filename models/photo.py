from typing import Optional

from pydantic import BaseModel

from schemas.photo import ServicePhotoType, PhotoType


class UploadServicePhotoDTO(BaseModel):
    filename: str
    order_id: str
    service_id: str
    tenant_id: str
    content: bytes
    service_photo_type: ServicePhotoType
    type: PhotoType

    class Config:
        use_enum_values = True


class UploadVehiclePhotoDTO(BaseModel):
    filename: str
    order_id: str
    tenant_id: str
    content: bytes
    type: PhotoType
    description: Optional[str] = None

    class Config:
        use_enum_values = True


class VehiclePhotoDTO(BaseModel):
    url: str
    order_id: str
    tenant_id: str
    type: PhotoType

    class Config:
        use_enum_values = True


class ServicePhotoDTO(BaseModel):
    url: str
    order_id: str
    service_id: str
    tenant_id: str
    type: PhotoType
    service_photo_type: ServicePhotoType

    class Config:
        use_enum_values = True

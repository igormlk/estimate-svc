from config import settings
from models.photo import UploadServicePhotoDTO, UploadVehiclePhotoDTO, VehiclePhotoDTO, ServicePhotoDTO
from schemas.photo import Photo


def map_service_to_photo(photo: UploadServicePhotoDTO, tenant_id: str) -> Photo:
    photo_entity = Photo.model_validate(photo.model_dump(), strict=False)

    photo_entity.tenant_id = tenant_id
    photo_entity.path = f'{tenant_id}/order/{photo.order_id}/service/{photo.service_id}/{photo.service_photo_type}/{photo.filename}'
    photo_entity.bucket = settings.BUCKET_PHOTO

    return photo_entity


def map_vehicle_to_photo(photo: UploadVehiclePhotoDTO, tenant_id: str) -> Photo:
    photo_entity = Photo.model_validate(photo.model_dump(), strict=False)

    photo_entity.tenant_id = tenant_id
    photo_entity.path = f'{tenant_id}/order/{photo.order_id}/vehicle/{photo.filename}'
    photo_entity.bucket = settings.BUCKET_PHOTO

    return photo_entity


def map_photo_to_vehicle_photo(photo: Photo, presign_link: str) -> VehiclePhotoDTO:
    return VehiclePhotoDTO(
        url=presign_link,
        order_id=photo.order_id,
        tenant_id=photo.tenant_id,
        type=photo.type,
    )


def map_photo_to_service_photo(photo: Photo, presign_link: str) -> ServicePhotoDTO:
    return ServicePhotoDTO(
        url=presign_link,
        order_id=photo.order_id,
        tenant_id=photo.tenant_id,
        type=photo.type,
        service_id=photo.service_id,
        service_photo_type=photo.service_photo_type
    )

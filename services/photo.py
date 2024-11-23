from typing import List

from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from crud.estimate import is_estimate_exists, is_service_exists
from crud.photo import upload_photo, persist_photo, find_service_photos, create_presign_link, find_vehicle_photos, \
    find_all_service_photos
from mappers.photo import map_service_to_photo, map_vehicle_to_photo, map_photo_to_vehicle_photo, \
    map_photo_to_service_photo
from models.photo import UploadServicePhotoDTO, UploadVehiclePhotoDTO, VehiclePhotoDTO, ServicePhotoDTO
from schemas.photo import Photo


async def upload_service_photo(photo: UploadServicePhotoDTO, tenant_id: str) -> Photo:
    if not await is_estimate_exists(photo.order_id):
        raise HTTPException(status_code=404, detail="Estimate does not exist")
    if not await is_service_exists(photo.order_id, photo.service_id):
        raise HTTPException(status_code=404, detail="Service does not exist")

    try:
        photo_entity = map_service_to_photo(photo, tenant_id)
        new_photo = await persist_photo(photo_entity)

        await upload_photo(new_photo.path, new_photo.bucket, photo.content)

        return new_photo
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Photo already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def upload_vehicle_photo(photo: UploadVehiclePhotoDTO, tenant_id: str) -> Photo:
    if not await is_estimate_exists(photo.order_id):
        raise HTTPException(status_code=404, detail="Estimate does not exist")

    try:
        photo_entity = map_vehicle_to_photo(photo, tenant_id)
        new_photo = await persist_photo(photo_entity)

        await upload_photo(new_photo.path, new_photo.bucket, photo.content)

        return new_photo
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Photo already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def list_service_photos(tenant_id: str, order_id: str, service_id: str) -> List[ServicePhotoDTO]:
    if not await is_estimate_exists(order_id):
        raise HTTPException(status_code=404, detail="Estimate does not exist")

    if not await is_service_exists(order_id, service_id):
        raise HTTPException(status_code=404, detail="Service does not exist")

    photos = await find_service_photos(tenant_id, order_id, service_id)

    async def map_photo(photo: Photo) -> ServicePhotoDTO:
        presign_link = await create_presign_link(photo.path, photo.bucket)
        return map_photo_to_service_photo(photo, presign_link)

    service_photos = [await map_photo(photo) for photo in photos]

    return service_photos


async def list_vehicle_photos(tenant_id: str, order_id: str) -> List[VehiclePhotoDTO]:
    if not await is_estimate_exists(order_id):
        raise HTTPException(status_code=404, detail="Estimate does not exist")

    photos = await find_vehicle_photos(tenant_id, order_id)

    async def map_photo(photo: Photo) -> VehiclePhotoDTO:
        presign_link = await create_presign_link(photo.path, photo.bucket)
        return map_photo_to_vehicle_photo(photo, presign_link)

    vehicle_photos = [await map_photo(photo) for photo in photos]

    return vehicle_photos


async def list_all_service_photos(tenant_id: str, order_id: str) -> List[ServicePhotoDTO]:
    if not await is_estimate_exists(order_id):
        raise HTTPException(status_code=404, detail="Estimate does not exist")

    photos = await find_all_service_photos(tenant_id, order_id)

    async def map_photo(photo: Photo) -> ServicePhotoDTO:
        presign_link = await create_presign_link(photo.path, photo.bucket)
        return map_photo_to_service_photo(photo, presign_link)

    service_photos = [await map_photo(photo) for photo in photos]

    return service_photos

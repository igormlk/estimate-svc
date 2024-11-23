from typing import List

import boto3

from config import settings
from database import database
from schemas.photo import Photo, PhotoType


async def persist_photo(photo: Photo) -> Photo:
    obj = photo.model_dump()
    await database["photo"].insert_one(obj)
    r = Photo.model_validate(obj)
    return r


async def upload_photo(path: str, bucket: str, content: bytes):
    # Create S3 service client
    svc = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_ENDPOINT_URL_S3
    )

    svc.put_object(Bucket=bucket, Key=path, Body=content)


async def create_presign_link(path: str, bucket: str) -> str:
    svc = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_ENDPOINT_URL_S3
    )

    url = svc.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': path},
        ExpiresIn=604800
    )

    return url


async def find_vehicle_photos(tenant_id: str, order_id: str) -> List[Photo]:
    photos = database["photo"].find({
        "$and": [
            {"tenant_id": tenant_id},
            {"order_id": order_id},
            {"type": PhotoType.VEHICLE.value}
        ]
    })

    return [Photo(**photo) for photo in await photos.to_list()]


async def find_all_service_photos(tenant_id: str, order_id: str) -> List[Photo]:
    photos = database["photo"].find({
        "$and": [
            {"tenant_id": tenant_id},
            {"order_id": order_id},
            {"type": PhotoType.SERVICE.value}
        ]
    })

    return [Photo(**photo) for photo in await photos.to_list()]


async def find_service_photos(tenant_id: str, order_id: str, service_id: str) -> List[Photo]:
    photos = database["photo"].find({
        "$and": [
            {"tenant_id": tenant_id},
            {"service_id": service_id},
            {"order_id": order_id},
            {"type": PhotoType.SERVICE.value}
        ]
    })

    return [Photo(**photo) for photo in await photos.to_list()]

from fastapi import APIRouter, Form, File, UploadFile, HTTPException, Depends

from models.photo import UploadServicePhotoDTO, UploadVehiclePhotoDTO
from schemas.photo import ServicePhotoType, PhotoType
from services.photo import upload_service_photo, upload_vehicle_photo, list_vehicle_photos, list_service_photos, \
    list_all_service_photos
from utils.jwt import get_current_tenant_id
from utils.log_middleware import logger as log

router = APIRouter(prefix="/v1/estimate", tags=["estimate"])


@router.put("/service/photo")
async def post_service_photo(
        order_id: str = Form(...),  # Obrigatório
        service_id: str = Form(...),  # Opcional
        file_type: ServicePhotoType = Form(...),  # Obrigatório, aceita apenas "old" ou "new"
        file: UploadFile = File(...),  # Arquivo obrigatório
        tenant_id: str = Depends(get_current_tenant_id)
):
    # Validação adicional se necessário
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, JPEG, or PNG allowed.")

    # Processar o arquivo aqui (salvar no sistema de arquivos, banco de dados, etc.)
    file_content = await file.read()

    uploaded_photo = UploadServicePhotoDTO(
        filename=file.filename,
        service_id=service_id,
        content=file_content,
        order_id=order_id,
        tenant_id=tenant_id,
        service_photo_type=file_type,
        type=PhotoType.SERVICE
    )

    new_photoo = await upload_service_photo(uploaded_photo, tenant_id)

    # Simulação de processamento
    await log.info(f"Received file: {file.filename}")
    await log.info(f"Content type: {file.content_type}")
    await log.info(f"Order ID: {order_id}")
    await log.info(f"Service ID: {service_id}")
    await log.info(f"File type: {file_type}")

    # Resposta simulada
    return {
        "message": "File uploaded successfully",
        "id": new_photoo.id.__str__(),
        "order_id": order_id,
        "service_id": service_id,
        "type": file_type,
        "filename": file.filename,
        "file_content_size": len(file_content)
    }


@router.put("/vehicle/photo")
async def post_vehicle_photo(
        order_id: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
        tenant_id: str = Depends(get_current_tenant_id)
):
    # Validação adicional se necessário
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, JPEG, or PNG allowed.")

    # Processar o arquivo aqui (salvar no sistema de arquivos, banco de dados, etc.)
    file_content = await file.read()

    uploaded_photo = UploadVehiclePhotoDTO(
        filename=file.filename,
        content=file_content,
        order_id=order_id,
        tenant_id=tenant_id,
        type=PhotoType.VEHICLE,
        description=description
    )

    new_photoo = await upload_vehicle_photo(uploaded_photo, tenant_id)

    # Simulação de processamento
    log.info(f"Received file: {file.filename}")
    log.info(f"Content type: {file.content_type}")
    log.info(f"Order ID: {order_id}")

    # Resposta simulada
    return {
        "message": "File uploaded successfully",
        "id": new_photoo.id.__str__(),
        "order_id": order_id,
        "filename": file.filename,
        "file_content_size": len(file_content)
    }


@router.get("/{order_id}/vehicle/photo")
async def get_vehicle_photos(tenant_id: str = Depends(get_current_tenant_id),
                             order_id: str = None):
    await log.info("listing vehicle photos")
    photos = await list_vehicle_photos(tenant_id, order_id)
    return photos


@router.get("/{order_id}/service/{service_id}/photo")
async def get_service_photos(tenant_id: str = Depends(get_current_tenant_id),
                             order_id: str = None,
                             service_id: str = None):
    await log.info("listing service photos")
    photos = await list_service_photos(tenant_id, order_id, service_id)
    return photos


@router.get("/{order_id}/service/photo")
async def get_all_service_photos(tenant_id: str = Depends(get_current_tenant_id),
                                 order_id: str = None):
    await log.info("listing all services")
    photos = await list_all_service_photos(tenant_id, order_id)
    return photos

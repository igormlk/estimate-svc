from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from crud.estimate import persist_estimate
from mappers.estimate import map_to_service_order
from models.estimate import ServiceOrderDTO
from schemas.estimate import ServiceOrder, Status


async def create_estimate(order: ServiceOrderDTO, tenant_id: str) -> ServiceOrder:
    order_entity = map_to_service_order(order, tenant_id)

    order_entity.status = Status.IN_PROGRESS.value

    try:
        result = await persist_estimate(order_entity)
        return result
    except DuplicateKeyError:
        # Captura erro de chave duplicada e retorna um status HTTP 400
        raise HTTPException(status_code=400, detail="Estimate already exists.")
    except Exception as e:
        # Captura outros erros e retorna um status HTTP 500 (erro interno)
        raise HTTPException(status_code=500, detail=str(e))

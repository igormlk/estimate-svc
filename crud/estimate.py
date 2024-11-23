from database import database
from schemas.estimate import ServiceOrder


async def persist_estimate(order_entity: ServiceOrder) -> ServiceOrder:
    result = await database["estimate"].insert_one(order_entity.model_dump())

    order_entity.id = str(result.inserted_id)

    return order_entity


async def is_estimate_exists(order_id: str) -> bool:
    result = await database["estimate"].find_one({"order_id": order_id})

    return result is not None

async def is_service_exists(order_id: str, service_id: str) -> bool:
    query = {
        "order_id": order_id,
        "service_order_items": {
            "$elemMatch": {"id": service_id}
        }
    }

    result = await database["estimate"].find_one(query)

    return result is not None
from models.estimate import ServiceOrderDTO, ServiceOrderResponseDTO
from schemas.estimate import ServiceOrder


def map_to_service_order(order: ServiceOrderDTO, tenant_id: str) -> ServiceOrder:
    service_order = ServiceOrder.model_validate(order.model_dump(), strict=False)
    service_order.tenant_id = tenant_id
    return service_order


def map_to_service_order_dto(order: ServiceOrder) -> ServiceOrderResponseDTO:
    return ServiceOrderResponseDTO.model_validate(order.model_dump(), strict=False)

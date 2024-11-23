from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from schemas.estimate import Status


# Modelo para os itens de serviço na ordem
class ServiceOrderItemDTO(BaseModel):
    id: str
    description: str
    value: float
    discount: float
    quantity: int
    type: str
    insurance_coverage: float
    total: float


# Modelo para informações do cliente
class CustomerDTO(BaseModel):
    name: str
    cpf: str
    phone: str
    email: str
    address: str


# Modelo para informações do veículo
class VehicleDTO(BaseModel):
    plate: str
    brand: str
    model: str
    year: str
    color: str
    fuel: str
    km: str
    chassi: str


# Modelo para a ordem de serviço completa
class ServiceOrderDTO(BaseModel):
    id: Optional[str] = None
    order_id: str
    service_order_items: List[ServiceOrderItemDTO]
    customer: CustomerDTO
    vehicle: VehicleDTO
    startAt: date
    endAt: date
    note: Optional[str]

class ServiceOrderResponseDTO(BaseModel):
    id: Optional[str] = None
    order_id: str
    service_order_items: List[ServiceOrderItemDTO]
    customer: CustomerDTO
    vehicle: VehicleDTO
    status: Status
    startAt: date
    endAt: date
    note: Optional[str]

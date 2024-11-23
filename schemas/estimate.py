from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from utils.object_id import PydanticObjectId


class ServiceOrderItem(BaseModel):
    id: str
    description: str
    value: float
    discount: float
    quantity: int
    type: str
    insurance_coverage: float
    total: float


# Modelo para informações do cliente
class Customer(BaseModel):
    name: str
    cpf: str
    phone: str
    email: str
    address: str


# Modelo para informações do veículo
class Vehicle(BaseModel):
    plate: str
    brand: str
    model: str
    year: str
    color: str
    fuel: str
    km: str
    chassi: str


class Status(Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"


# Modelo para a ordem de serviço completa
class ServiceOrder(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    order_id: str
    tenant_id: Optional[str] = None
    service_order_items: List[ServiceOrderItem]
    customer: Customer
    vehicle: Vehicle
    status: Optional[str] = None
    startAt: datetime
    endAt: datetime
    note: Optional[str] = None

    class Config:
        use_enum_values = True

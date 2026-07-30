from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List


class OrderStatus(Enum):
    PENDING = "Pendiente"
    PREPARING = "En preparación"
    READY = "Listo"
    DELIVERED = "Entregado"


class TeaSize(Enum):
    SMALL = "Pequeño"
    MEDIUM = "Mediano"
    LARGE = "Grande"


class SugarLevel(Enum):
    ZERO = "0%"
    FIFTY = "50%"
    HUNDRED = "100%"
    HUNDRED_FIFTY = "150%"


class IceLevel(Enum):
    NONE = "Sin hielo"
    LIGHT = "Poco hielo"
    NORMAL = "Normal"
    EXTRA = "Extra hielo"


@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    password: str
    created_at: datetime


@dataclass
class Tea:
    id: Optional[int]
    name: str
    price: float
    available: bool
    created_at: datetime


@dataclass
class Topping:
    id: Optional[int]
    name: str
    price: float
    stock: int
    available: bool


@dataclass
class CustomizedDrink:
    id: Optional[int]
    tea_id: int
    size: TeaSize
    sugar_level: SugarLevel
    ice_level: IceLevel
    toppings: List[Topping]
    price: float
    created_at: datetime


@dataclass
class Order:
    id: Optional[int]
    user_id: int
    items: List[dict]
    total_price: float
    status: OrderStatus
    payment_method: str
    payment_status: str
    order_number: str
    created_at: datetime
    updated_at: Optional[datetime]


@dataclass
class OrderStatusUpdate:
    id: Optional[int]
    order_id: int
    old_status: OrderStatus
    new_status: OrderStatus
    updated_at: datetime
    updated_by: int

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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
    id: int | None
    name: str
    email: str
    password: str
    created_at: datetime


@dataclass
class Tea:
    id: int | None
    name: str
    price: float
    available: bool
    created_at: datetime


@dataclass
class Topping:
    id: int | None
    name: str
    price: float
    stock: int
    available: bool


@dataclass
class CustomizedDrink:
    id: int | None
    tea_id: int
    size: TeaSize
    sugar_level: SugarLevel
    ice_level: IceLevel
    toppings: list[Topping]
    price: float
    created_at: datetime


@dataclass
class Order:
    id: int | None
    user_id: int
    items: list[dict]
    total_price: float
    status: OrderStatus
    payment_method: str
    payment_status: str
    order_number: str
    created_at: datetime
    updated_at: datetime | None


@dataclass
class OrderStatusUpdate:
    id: int | None
    order_id: int
    old_status: OrderStatus
    new_status: OrderStatus
    updated_at: datetime
    updated_by: int

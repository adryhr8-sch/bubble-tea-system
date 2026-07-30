from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
import random
import string

from .models import User, Tea, Topping, Order, OrderStatusUpdate
from .database import get_connection


class BaseRepository(ABC):
    @abstractmethod
    def save(self, entity):
        pass
    
    @abstractmethod
    def find_by_id(self, id: int):
        pass
    
    @abstractmethod
    def find_all(self):
        pass


class UserRepository(BaseRepository):
    def __init__(self):
        self._connection = get_connection
        self._id_counter = 1
    
    def save(self, user: User) -> User:
        if user.id is None:
            user.id = self._id_counter
            self._id_counter += 1
        self._users[user.id] = user
        return user
    
    def find_by_id(self, id: int) -> Optional[User]:
        return self._users.get(id)
    
    def find_all(self) -> List[User]:
        return list(self._users.values())
    
    def find_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None
    
    def exists_by_email(self, email: str) -> bool:
        return self.find_by_email(email) is not None


class TeaRepository(BaseRepository):
    def __init__(self):
        self._teas = {}
        self._id_counter = 1
    
    def save(self, tea: Tea) -> Tea:
        if tea.id is None:
            tea.id = self._id_counter
            self._id_counter += 1
        self._teas[tea.id] = tea
        return tea
    
    def find_by_id(self, id: int) -> Optional[Tea]:
        return self._teas.get(id)
    
    def find_all(self) -> List[Tea]:
        return list(self._teas.values())
    
    def find_by_name(self, name: str) -> Optional[Tea]:
        for tea in self._teas.values():
            if tea.name == name:
                return tea
        return None
    
    def exists_by_name(self, name: str) -> bool:
        return self.find_by_name(name) is not None


class ToppingRepository(BaseRepository):
    def __init__(self):
        self._toppings = {}
        self._id_counter = 1
    
    def save(self, topping: Topping) -> Topping:
        if topping.id is None:
            topping.id = self._id_counter
            self._id_counter += 1
        self._toppings[topping.id] = topping
        return topping
    
    def find_by_id(self, id: int) -> Optional[Topping]:
        return self._toppings.get(id)
    
    def find_all(self) -> List[Topping]:
        return list(self._toppings.values())
    
    def find_by_name(self, name: str) -> Optional[Topping]:
        for topping in self._toppings.values():
            if topping.name == name:
                return topping
        return None


class OrderRepository(BaseRepository):
    def __init__(self):
        self._orders = {}
        self._id_counter = 1
    
    def save(self, order: Order) -> Order:
        if order.id is None:
            order.id = self._id_counter
            self._id_counter += 1
            if not order.order_number:
                order.order_number = self._generate_order_number()
        self._orders[order.id] = order
        return order
    
    def _generate_order_number(self) -> str:
        prefix = "BT"
        timestamp = datetime.now().strftime("%Y%m%d")
        random_part = ''.join(random.choices(string.digits, k=6))
        return f"{prefix}{timestamp}{random_part}"
    
    def find_by_id(self, id: int) -> Optional[Order]:
        return self._orders.get(id)
    
    def find_all(self) -> List[Order]:
        return list(self._orders.values())
    
    def find_by_user(self, user_id: int) -> List[Order]:
        return [order for order in self._orders.values() if order.user_id == user_id]


class OrderStatusUpdateRepository(BaseRepository):
    def __init__(self):
        self._updates = {}
        self._id_counter = 1
    
    def save(self, update: OrderStatusUpdate) -> OrderStatusUpdate:
        if update.id is None:
            update.id = self._id_counter
            self._id_counter += 1
        self._updates[update.id] = update
        return update
    
    def find_by_id(self, id: int) -> Optional[OrderStatusUpdate]:
        return self._updates.get(id)
    
    def find_all(self) -> List[OrderStatusUpdate]:
        return list(self._updates.values())
    
    def find_by_order(self, order_id: int) -> List[OrderStatusUpdate]:
        return [update for update in self._updates.values() if update.order_id == order_id]

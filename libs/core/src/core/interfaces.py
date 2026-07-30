from abc import ABC, abstractmethod

from database.models import Tea, User


# Interfaz 1: Repositorio de Usuarios
class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass
    
    @abstractmethod
    def find_by_id(self, id: int) -> User | None:
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

# Interfaz 2: Procesador de Pagos
class IPaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

# Interfaz 3: Calculador de Precios / Promociones
class IPriceCalculator(ABC):
    @abstractmethod
    def calculate(self, tea: Tea, size: str, toppings: list) -> float:
        pass

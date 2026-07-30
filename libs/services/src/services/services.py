from typing import List
from datetime import datetime
import hashlib

from database.models import OrderStatusUpdate, User, Order, OrderStatus, Tea
from database.repositories import OrderRepository, ToppingRepository, OrderStatusUpdateRepository, TeaRepository
from core.interfaces import IUserRepository, IPaymentProcessor, IPriceCalculator
from core.exceptions import InvalidPasswordError, DuplicateEmailError, InsufficientStockError, DuplicateTeaError


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    def register_user(self, name: str, email: str, password: str) -> User:
        if len(password) < 8:
            raise InvalidPasswordError("La contraseña debe tener al menos 8 caracteres")
        if self.user_repo.exists_by_email(email):
            raise DuplicateEmailError("El correo ya está registrado")
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = User(id=None, name=name, email=email, password=hashed_password, created_at=datetime.now())
        return self.user_repo.save(user)


class StandardPriceCalculator(IPriceCalculator):
    def __init__(self, topping_repo: ToppingRepository):
        self.topping_repo = topping_repo

    def calculate(self, tea, size: str, toppings: List[str]) -> float:
        size_multipliers = {"Pequeño": 1.0, "Mediano": 1.3, "Grande": 1.6}
        multiplier = size_multipliers.get(size, 1.0)
        price = tea.price * multiplier
        
        for topping_name in toppings:
            topping = self.topping_repo.find_by_name(topping_name)
            if topping:
                price += topping.price
        return round(price, 2)


class TeaService:
    def __init__(self, tea_repo: TeaRepository):
        self.tea_repo = tea_repo
    
    def add_tea(self, name: str, price: float) -> Tea:
        if self.tea_repo.exists_by_name(name):
            raise DuplicateTeaError("La bebida ya existe")
        
        tea = Tea(
            id=None,
            name=name,
            price=price,
            available=True,
            created_at=datetime.now()
        )
        return self.tea_repo.save(tea)
    
    def update_price(self, tea_id: int, new_price: float) -> Tea:
        tea = self.tea_repo.find_by_id(tea_id)
        if not tea:
            raise ValueError("Bebida no encontrada")
        tea.price = new_price
        return self.tea_repo.save(tea)


class OrderService:
    def __init__(
        self, 
        order_repo: OrderRepository, 
        user_repo: IUserRepository,
        topping_repo: ToppingRepository,
        status_update_repo: OrderStatusUpdateRepository,
        price_calculator: IPriceCalculator
    ):
        self.order_repo = order_repo
        self.user_repo = user_repo
        self.topping_repo = topping_repo
        self.status_update_repo = status_update_repo
        self.price_calculator = price_calculator

    def update_order_status(self, order_id: int, new_status: OrderStatus, employee_id: int) -> Order:
        """
        Actualiza el estado de una orden y registra el cambio en el historial.
        """
        order = self.order_repo.find_by_id(order_id)
        if not order:
            raise ValueError("Pedido no encontrado")
        
        if order.status == new_status:
            raise ValueError("El pedido ya tiene ese estado")
        
        old_status = order.status
        order.status = new_status
        order.updated_at = datetime.now()
        
        # Registrar el historial del cambio de estado
        status_update = OrderStatusUpdate(
            id=None,
            order_id=order_id,
            old_status=old_status,
            new_status=new_status,
            updated_at=datetime.now(),
            updated_by=employee_id
        )
        self.status_update_repo.save(status_update)
        
        return self.order_repo.save(order)

    def create_order(
        self, 
        user_id: int, 
        items: List[dict], 
        payment_processor: IPaymentProcessor
    ) -> Order:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        if not items:
            raise ValueError("El carrito está vacío")
        
        total_price = 0
        validated_items = []
        
        for item in items:
            tea = item.get('tea')
            if not tea:
                raise ValueError("Bebida no válida")
            
            toppings = []
            for topping_name in item.get('toppings', []):
                topping = self.topping_repo.find_by_name(topping_name)
                if not topping or topping.stock <= 0:
                    raise InsufficientStockError(f"Topping no disponible: {topping_name}")
                toppings.append(topping)
                topping.stock -= 1
                self.topping_repo.save(topping)
            
            price = self.price_calculator.calculate(tea, item.get('size', 'Mediano'), [t.name for t in toppings])
            total_price += price
            
            validated_items.append({
                'tea': tea,
                'size': item.get('size', 'Mediano'),
                'sugar_level': item.get('sugar_level', '50%'),
                'ice_level': item.get('ice_level', 'Normal'),
                'toppings': toppings,
                'price': price
            })
        
        is_paid = payment_processor.process_payment(total_price)
        payment_status = "Aprobado" if is_paid else "Pendiente"

        order = Order(
            id=None,
            user_id=user_id,
            items=validated_items,
            total_price=total_price,
            status=OrderStatus.PENDING,
            payment_method=payment_processor.__class__,
            payment_status=payment_status,
            order_number="",
            created_at=datetime.now(),
            updated_at=None
        )
        
        return self.order_repo.save(order)

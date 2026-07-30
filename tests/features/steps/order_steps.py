from unittest.mock import MagicMock

from behave import given, step, then, when
from core.exceptions import PaymentRejectedError
from database.models import Tea
from database.repositories import (
    OrderRepository,
    OrderStatusUpdateRepository,
    ToppingRepository,
    UserRepository,
)
from services.payments import CardPaymentProcessor
from services.services import OrderService, StandardPriceCalculator


@given('que el cliente tiene productos en el carrito')
def step_customer_has_items_in_cart(context):
    context.user_id = 1
    context.cart_items = [
        {
            'tea': Tea(id=1, name="Matcha Latte", price=65.0, available=True, created_at=None),
            'size': "Grande",
            'sugar_level': "50%",
            'ice_level': "Normal",
            'toppings': []
        }
    ]
    
    context.order_repo = MagicMock(spec=OrderRepository)
    context.user_repo = MagicMock(spec=UserRepository)
    context.topping_repo = MagicMock(spec=ToppingRepository)
    context.status_update_repo = MagicMock(spec=OrderStatusUpdateRepository)
    context.price_calculator = StandardPriceCalculator(context.topping_repo)
    
    context.user_repo.find_by_id.return_value = MagicMock(id=1, name="Test User")
    
    context.order_service = OrderService(
        context.order_repo,
        context.user_repo,
        context.topping_repo,
        context.status_update_repo,
        context.price_calculator,
    )
    
    # Asegurar que payment_method esté definido
    context.payment_method = CardPaymentProcessor()  # Valor por defecto


@when('confirma el pedido')
def step_confirm_order(context):
    context.order_response = None
    context.exception = None
    try:
        # Asegurar que payment_method esté definido
        if not hasattr(context, 'payment_method'):
            context.payment_method = CardPaymentProcessor()
        
        context.order_response = context.order_service.create_order(
            context.user_id,
            context.cart_items,
            context.payment_method
        )
    except Exception as e:
        context.exception = e


@when('selecciona pago con tarjeta')
def step_select_card_payment(context):
    context.payment_method = CardPaymentProcessor()


@then('el sistema registra el pedido')
def step_system_registers_order(context):
    assert context.order_response is not None, "La orden no se creó correctamente"
    context.order_repo.save.assert_called_once()


@then('genera un número de orden')
def step_generates_order_number(context):
    assert context.order_response is not None, "No hay orden para generar número"
    assert context.order_response.order_number is not None
    assert context.order_response.order_number.startswith("BT")


@given('que el carrito está vacío')
def step_cart_is_empty(context):
    context.cart_items = []
    context.user_repo.find_by_id.return_value = MagicMock(id=1, name="Test User")


@when('intenta confirmar la compra')
def step_try_to_confirm_order(context):
    context.exception = None
    try:
        context.order_response = context.order_service.create_order(
            context.user_id,
            context.cart_items,
            "Tarjeta"
        )
    except ValueError as e:
        context.exception = e


@then('el sistema muestra "El carrito está vacío"')
def step_show_empty_cart_message(context):
    assert context.exception is not None
    assert isinstance(context.exception, ValueError)
    assert "carrito" in str(context.exception).lower()


@step('no genera ningún pedido')
def step_no_order_generated(context):
    context.order_repo.save.assert_not_called()


@when('el banco rechaza el pago')
def step_payment_rejected(context):
    context.payment_method = CardPaymentProcessor()
    context.exception = None
    context.payment_method._reject_payment = True
    
    try:
        context.order_response = context.order_service.create_order(
            context.user_id,
            context.cart_items,
            context.payment_method,
        )
    except PaymentRejectedError as e:
        context.exception = e


@then('el sistema muestra "Pago con tarjeta rechazado"')
def step_show_payment_rejected(context):
    assert context.exception is not None
    assert isinstance(context.exception, PaymentRejectedError)
    assert str(context.exception) == "Pago con tarjeta rechazado"


@step('el pedido no se registra')
def step_order_not_registered(context):
    context.order_repo.save.assert_not_called()

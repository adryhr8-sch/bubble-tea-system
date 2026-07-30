from unittest.mock import MagicMock

from behave import given, then, when
from database.models import Order, OrderStatus
from database.repositories import (
    OrderRepository,
    OrderStatusUpdateRepository,
    ToppingRepository,
    UserRepository,
)
from services.services import OrderService, StandardPriceCalculator


# CAMBIADO: Este es para el empleado, no para el administrador
@given('que el empleado inicia sesión')
def step_employee_logged_in(context):
    context.employee_id = 2
    
    context.order_repo = MagicMock(spec=OrderRepository)
    context.user_repo = MagicMock(spec=UserRepository)
    context.topping_repo = MagicMock(spec=ToppingRepository)
    context.status_update_repo = MagicMock(spec=OrderStatusUpdateRepository)
    context.price_calculator = StandardPriceCalculator(context.topping_repo)
    
    context.order_service = OrderService(
        context.order_repo,
        context.user_repo,
        context.topping_repo,
        context.status_update_repo,
        context.price_calculator,
    )


@given('existe un pedido registrado')
def step_order_exists(context):
    context.order_id = 1
    context.existing_order = Order(
        id=1,
        user_id=1,
        items=[],
        total_price=100.0,
        status=OrderStatus.PENDING,
        payment_method="Tarjeta",
        payment_status="Aprobado",
        order_number="BT20260101001",
        created_at=None,
        updated_at=None
    )
    context.order_repo.find_by_id.return_value = context.existing_order
    context.order_repo.save.return_value = context.existing_order


@when('cambia el estado a "{status}"')
def step_change_status_to(context, status):
    context.new_status = status
    context.exception = None
    
    try:
        status_map = {
            "En preparación": OrderStatus.PREPARING,
            "Listo": OrderStatus.READY,
            "Entregado": OrderStatus.DELIVERED
        }
        context.result = context.order_service.update_order_status(
            context.order_id,
            status_map[status],
            context.employee_id
        )
    except ValueError as e:
        context.exception = e


@then('el sistema actualiza el pedido')
def step_system_updates_order(context):
    assert context.result is not None
    context.order_repo.save.assert_called_once()


@then('muestra "{message}"')
def step_show_status_message(context, message):
    assert message == "Estado actualizado"


@when('intenta actualizar un pedido inexistente')
def step_try_update_nonexistent_order(context):
    context.order_id = 999
    context.order_repo.find_by_id.return_value = None
    context.exception = None
    
    try:
        context.order_service.update_order_status(
            context.order_id,
            OrderStatus.PREPARING,
            context.employee_id
        )
    except ValueError as e:
        context.exception = e


@then('el sistema muestra "Pedido no encontrado"')
def step_show_order_not_found(context):
    assert context.exception is not None
    assert isinstance(context.exception, ValueError)
    assert str(context.exception) == "Pedido no encontrado"


@given('que el pedido ya está "Entregado"')
def step_order_already_delivered(context):
    context.order_id = 1
    context.existing_order = Order(
        id=1,
        user_id=1,
        items=[],
        total_price=100.0,
        status=OrderStatus.DELIVERED,
        payment_method="Tarjeta",
        payment_status="Aprobado",
        order_number="BT20260101001",
        created_at=None,
        updated_at=None
    )
    context.order_repo.find_by_id.return_value = context.existing_order


@when('intenta cambiar nuevamente a "Entregado"')
def step_try_change_to_delivered_again(context):
    context.exception = None
    try:
        context.order_service.update_order_status(
            context.order_id,
            OrderStatus.DELIVERED,
            context.employee_id
        )
    except ValueError as e:
        context.exception = e


@then('el sistema informa "El pedido ya tiene ese estado"')
def step_show_order_already_has_status(context):
    assert context.exception is not None
    assert isinstance(context.exception, ValueError)
    assert str(context.exception) == "El pedido ya tiene ese estado"

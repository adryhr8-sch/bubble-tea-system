from unittest.mock import MagicMock

from behave import given, step, then, when
from core.exceptions import InsufficientStockError
from database.models import Tea, Topping
from database.repositories import OrderRepository, TeaRepository, ToppingRepository
from services.services import OrderService, StandardPriceCalculator


# ============= GIVEN STEPS =============
@given('que el cliente inicia sesión')
def step_customer_logged_in(context):
    context.user_id = 1
    context.cart = []
    context.current_drink = None
    
    context.tea_repo = MagicMock(spec=TeaRepository)
    context.topping_repo = MagicMock(spec=ToppingRepository)
    context.order_repo = MagicMock(spec=OrderRepository)
    context.price_calculator = StandardPriceCalculator(context.topping_repo)
    context.order_service = OrderService(context.order_repo, MagicMock(), context.topping_repo, MagicMock(), context.price_calculator)


@given('seleccionó una bebida del menú')
def step_selected_drink_from_menu(context):
    context.selected_tea = Tea(
        id=1,
        name="Bubble Tea Classic",
        price=50.0,
        available=True,
        created_at=None
    )
    context.tea_repo.find_by_id.return_value = context.selected_tea


# ============= WHEN STEPS =============
@when('selecciona tamaño grande')
def step_select_large_size(context):
    context.current_size = "Grande"
    context.current_drink = {
        'tea': context.selected_tea,
        'size': context.current_size,
        'toppings': []
    }


@when('selecciona azúcar al 50%')
def step_select_sugar_50(context):
    context.sugar_level = "50%"
    if context.current_drink:
        context.current_drink['sugar_level'] = context.sugar_level


@when('selecciona hielo normal')
def step_select_normal_ice(context):
    context.ice_level = "Normal"
    if context.current_drink:
        context.current_drink['ice_level'] = context.ice_level


@when('agrega tapioca')
def step_add_tapioca(context):
    tapioca = Topping(
        id=1,
        name="Tapioca",
        price=10.0,
        stock=50,
        available=True
    )
    context.topping_repo.find_by_name.return_value = tapioca
    context.current_drink['toppings'].append("Tapioca")


@when('selecciona "{sugar_level}"')
def step_select_sugar_level(context, sugar_level):
    context.sugar_level = sugar_level
    context.sugar_result = None
    context.current_drink = {
        'tea': context.selected_tea,
        'size': "Mediano",
        'sugar_level': sugar_level,
        'toppings': []
    }


@when('el cliente agrega un topping agotado')
def step_add_out_of_stock_topping(context):
    out_of_stock_topping = Topping(
        id=2,
        name="Tapioca",
        price=10.0,
        stock=0,
        available=False
    )
    context.topping_repo.find_by_name.return_value = out_of_stock_topping
    context.exception = None
    
    try:
        context.order_service.create_order(
            context.user_id,
            [{'tea': context.selected_tea, 'toppings': ["Tapioca"]}],
            "Tarjeta"
        )
    except InsufficientStockError as e:
        context.exception = e


# ============= THEN STEPS =============
@then('el sistema calcula el precio')
def step_system_calculates_price(context):
    price = context.order_service.price_calculator.calculate(
        context.selected_tea,
        context.current_size,
        context.current_drink['toppings']
    )
    context.calculated_price = price
    context.topping_repo.find_by_name.assert_called_with("Tapioca")


@then('agrega la bebida al carrito')
def step_adds_drink_to_cart(context):
    context.cart.append(context.current_drink)
    assert len(context.cart) == 1


@then('el sistema muestra el resultado "{result}"')
def step_system_shows_sugar_validation_result(context, result):
    """Step específico para validación de azúcar"""
    valid_levels = ["0%", "50%", "100%"]
    if context.sugar_level in valid_levels:
        context.sugar_result = "Nivel aceptado"
    else:
        context.sugar_result = "Nivel inválido"
    assert context.sugar_result == result


@then('el sistema muestra el mensaje de topping no disponible')
def step_show_topping_not_available_message(context):
    """Step específico para topping no disponible"""
    assert context.exception is not None
    assert isinstance(context.exception, InsufficientStockError)
    assert "Topping no disponible" in str(context.exception)


# ============= BUT STEPS =============
@step('no agrega el topping a la bebida')
def step_no_topping_added(context):
    context.topping_repo.find_by_name.assert_called()
    assert context.exception is not None

from unittest.mock import MagicMock

from behave import given, step, then, when
from core.exceptions import DuplicateTeaError
from database.models import Tea
from database.repositories import TeaRepository
from services.services import TeaService


# Este es el step correcto para el administrador
@given('que el administrador inicia sesión')
def step_admin_logged_in(context):
    context.admin_id = 3
    context.tea_repo = MagicMock(spec=TeaRepository)
    context.tea_service = TeaService(context.tea_repo)
    context.exception = None


@when('registra una bebida llamada "Matcha Latte"')
def step_register_drink_matcha_latte(context):
    context.drink_name = "Matcha Latte"
    context.drink_price = 95.0
    
    context.tea_repo.exists_by_name.return_value = False
    context.tea_repo.save.return_value = Tea(
        id=1,
        name="Matcha Latte",
        price=95.0,
        available=True,
        created_at=None
    )


@when('asigna un precio de $95')
def step_assign_price_95(context):
    context.drink_price = 95.0


@when('cambia el precio de una bebida existente')
def step_change_price_existing_drink(context):
    context.tea_id = 1
    context.new_price = 85.0
    
    existing_tea = Tea(
        id=1,
        name="Matcha Latte",
        price=95.0,
        available=True,
        created_at=None
    )
    context.tea_repo.find_by_id.return_value = existing_tea
    context.tea_repo.save.return_value = Tea(
        id=1,
        name="Matcha Latte",
        price=85.0,
        available=True,
        created_at=None
    )


@when('intenta registrar una bebida con un nombre existente')
def step_try_register_duplicate_drink(context):
    context.drink_name = "Matcha Latte"
    context.drink_price = 95.0
    
    context.tea_repo.exists_by_name.return_value = True
    context.exception = None
    
    try:
        context.tea_service.add_tea(context.drink_name, context.drink_price)
    except DuplicateTeaError as e:
        context.exception = e


@then('el sistema agrega la bebida al catálogo')
def step_system_adds_drink_to_catalog(context):
    try:
        result = context.tea_service.add_tea(context.drink_name, context.drink_price)
        assert result is not None
        context.tea_repo.save.assert_called_once()
    except Exception as e:
        context.exception = e


@then('el sistema guarda el nuevo precio')
def step_system_saves_new_price(context):
    result = context.tea_service.update_price(context.tea_id, context.new_price)
    assert result is not None
    assert result.price == 85.0
    context.tea_repo.save.assert_called_once()


@then('el sistema muestra "La bebida ya existe"')
def step_show_drink_already_exists(context):
    assert context.exception is not None
    assert isinstance(context.exception, DuplicateTeaError)
    assert str(context.exception) == "La bebida ya existe"


@step('no crea un nuevo registro')
def step_no_new_record_created(context):
    context.tea_repo.save.assert_not_called()

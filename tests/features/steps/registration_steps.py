from unittest.mock import MagicMock

from behave import given, step, then, when
from core.exceptions import DuplicateEmailError, InvalidPasswordError
from database.repositories import UserRepository
from services.services import UserService


# ============= GIVEN STEPS =============
@given('que el usuario se encuentra en la pantalla de registro')
def step_user_on_registration_screen(context):
    context.user_data = {}
    context.response = None
    context.exception = None
    # Configurar repositorio mock
    if not hasattr(context, 'user_repo'):
        context.user_repo = MagicMock(spec=UserRepository)
        context.user_service = UserService(context.user_repo)


# ============= WHEN STEPS =============
@when('ingresa un nombre válido')
def step_enter_valid_name(context):
    if not hasattr(context, 'user_data'):
        context.user_data = {}
    context.user_data['name'] = "Juan Perez"


@when('ingresa un correo no registrado')
def step_enter_unregistered_email(context):
    if not hasattr(context, 'user_data'):
        context.user_data = {}
    if not hasattr(context, 'user_repo'):
        context.user_repo = MagicMock(spec=UserRepository)
        context.user_service = UserService(context.user_repo)
    
    context.user_data['email'] = "juan@example.com"
    
    # Configurar mocks para correo no registrado
    context.user_repo.exists_by_email.return_value = False
    
    # Crear un usuario mock para el retorno
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.name = "Juan Perez"
    mock_user.email = "juan@example.com"
    context.user_repo.save.return_value = mock_user


@when('escribe una contraseña válida')
def step_enter_valid_password(context):
    if not hasattr(context, 'user_data'):
        context.user_data = {}
    context.user_data['password'] = "password123"


@when('el usuario ingresa un correo existente')
def step_enter_existing_email(context):
    if not hasattr(context, 'user_data'):
        context.user_data = {}
    if not hasattr(context, 'user_repo'):
        context.user_repo = MagicMock(spec=UserRepository)
        context.user_service = UserService(context.user_repo)
    
    context.user_data['email'] = "existing@example.com"
    # Configurar mock para correo existente
    context.user_repo.exists_by_email.return_value = True


@when('el usuario ingresa una contraseña de 5 caracteres')
def step_enter_short_password(context):
    if not hasattr(context, 'user_data'):
        context.user_data = {}
    if not hasattr(context, 'user_repo'):
        context.user_repo = MagicMock(spec=UserRepository)
        context.user_service = UserService(context.user_repo)
    
    context.user_data['password'] = "12345"
    context.user_data['email'] = "test@example.com"
    context.user_repo.exists_by_email.return_value = False


# ============= THEN STEPS =============
@then('el sistema crea la cuenta')
def step_system_creates_account(context):
    try:
        if not hasattr(context, 'user_service'):
            context.user_repo = MagicMock(spec=UserRepository)
            context.user_service = UserService(context.user_repo)
        
        # Llamar al servicio
        context.response = context.user_service.register_user(
            context.user_data['name'],
            context.user_data['email'],
            context.user_data['password']
        )
        # Verificar que se llamó a save
        context.user_repo.save.assert_called_once()
    except Exception as e:
        context.exception = e
        raise


@then('muestra el mensaje "Registro exitoso"')
def step_show_success_message(context):
    # Verificar que la respuesta no sea None
    assert context.response is not None, "La respuesta es None"
    # Verificar que el usuario se creó correctamente
    assert hasattr(context.response, 'name'), "La respuesta no tiene atributo 'name'"
    assert context.response.name == "Juan Perez", f"Expected 'Juan Perez', got '{context.response.name}'"
    assert context.response.email == "juan@example.com", f"Expected 'juan@example.com', got '{context.response.email}'"


@then('el sistema rechaza el registro')
def step_system_rejects_registration(context):
    try:
        if not hasattr(context, 'user_service'):
            context.user_repo = MagicMock(spec=UserRepository)
            context.user_service = UserService(context.user_repo)
        
        context.user_service.register_user(
            context.user_data.get('name', "Test"),
            context.user_data['email'],
            context.user_data.get('password', "password123")
        )
    except DuplicateEmailError as e:
        context.exception = e


@then('muestra el mensaje "El correo ya está registrado"')
def step_show_email_exists_message(context):
    assert context.exception is not None, "No se lanzó ninguna excepción"
    assert isinstance(context.exception, DuplicateEmailError), f"Expected DuplicateEmailError, got {type(context.exception)}"
    assert str(context.exception) == "El correo ya está registrado"


@then('el sistema muestra el mensaje "La contraseña debe tener al menos 8 caracteres"')
def step_show_password_too_short_message(context):
    try:
        if not hasattr(context, 'user_service'):
            context.user_repo = MagicMock(spec=UserRepository)
            context.user_service = UserService(context.user_repo)
        
        context.user_service.register_user(
            "Test User",
            context.user_data['email'],
            context.user_data['password']
        )
    except InvalidPasswordError as e:
        context.exception = e
    
    assert context.exception is not None, "No se lanzó ninguna excepción"
    assert isinstance(context.exception, InvalidPasswordError), f"Expected InvalidPasswordError, got {type(context.exception)}"
    assert str(context.exception) == "La contraseña debe tener al menos 8 caracteres"


# ============= BUT STEPS =============
@step('no crea una nueva cuenta')
def step_no_new_account_created(context):
    if hasattr(context, 'user_repo'):
        context.user_repo.save.assert_not_called()


@step('no registra al usuario')
def step_no_user_registered(context):
    if hasattr(context, 'user_repo'):
        context.user_repo.save.assert_not_called()

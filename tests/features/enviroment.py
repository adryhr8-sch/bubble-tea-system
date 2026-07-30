from unittest.mock import MagicMock

from services.services import UserService
from database.repositories import UserRepository


def before_scenario(context, scenario):
    """Configuración antes de cada escenario"""
    # Configurar para registration_steps
    if 'registro' in scenario.feature.name.lower() or 'registration' in scenario.feature.name.lower():
        context.user_repo = MagicMock(spec=UserRepository)
        context.user_service = UserService(context.user_repo)
        context.user_data = {}
        context.response = None
        context.exception = None
    
    # Configurar para customization_steps
    if 'personalización' in scenario.feature.name.lower() or 'customization' in scenario.feature.name.lower():
        context.cart = []
        context.current_drink = None
        # Los mocks específicos se crearán en cada step
    
    # Configurar para order_steps
    if 'pedido' in scenario.feature.name.lower() or 'order' in scenario.feature.name.lower():
        context.order_response = None
        context.exception = None
    
    # Configurar para order_management_steps
    if 'gestión' in scenario.feature.name.lower() or 'management' in scenario.feature.name.lower():
        context.exception = None
        context.result = None


def after_scenario(context, scenario):
    """Limpieza después de cada escenario"""
    pass

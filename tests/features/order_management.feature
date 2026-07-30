# features/order_management.feature
Feature: Gestión de pedidos
  Como empleado
  Quiero cambiar el estado del pedido
  Para informarle al cliente sobre el avance de su orden

  Background:
    Given que el empleado inicia sesión
    And existe un pedido registrado

  Scenario Outline: Cambio de estado
    When cambia el estado a "<estado>"
    Then el sistema actualiza el pedido
    And muestra "<mensaje>"
    
    Examples:
      | estado         | mensaje            |
      | En preparación | Estado actualizado |
      | Listo          | Estado actualizado |
      | Entregado      | Estado actualizado |

  Scenario: Pedido inexistente
    When intenta actualizar un pedido inexistente
    Then el sistema muestra "Pedido no encontrado"

  Scenario: Estado repetido
    Given que el pedido ya está "Entregado"
    When intenta cambiar nuevamente a "Entregado"
    Then el sistema informa "El pedido ya tiene ese estado"
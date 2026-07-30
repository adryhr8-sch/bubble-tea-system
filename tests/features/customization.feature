Feature: Personalización de bebidas
  Como cliente
  Quiero elegir el tamaño, el tipo de té y los toppings
  Para crear una bebida a mi gusto

  Background:
    Given que el cliente inicia sesión
    And seleccionó una bebida del menú

  Scenario: Personalización exitosa
    When selecciona tamaño grande
    And selecciona azúcar al 50%
    And selecciona hielo normal
    And agrega tapioca
    Then el sistema calcula el precio
    And agrega la bebida al carrito

  Scenario Outline: Validar nivel de azúcar
    When selecciona "<azúcar>"
    Then el sistema muestra el resultado "<resultado>"
    
    Examples:
      | azúcar | resultado      |
      | 0%     | Nivel aceptado |
      | 50%    | Nivel aceptado |
      | 100%   | Nivel aceptado |
      | 150%   | Nivel inválido |

  Scenario: Topping sin inventario
    When el cliente agrega un topping agotado
    Then el sistema muestra el mensaje de topping no disponible
    But no agrega el topping a la bebida
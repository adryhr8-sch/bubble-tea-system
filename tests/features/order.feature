Feature: Confirmación de pedido
  Como cliente
  Quiero confirmar mi compra
  Para recibir mi bebida

  Background:
    Given que el cliente tiene productos en el carrito

  Scenario: Pedido realizado correctamente
    When confirma el pedido
    And selecciona pago con tarjeta
    Then el sistema registra el pedido
    And genera un número de orden

  Scenario: Carrito vacío
    Given que el carrito está vacío
    When intenta confirmar la compra
    Then el sistema muestra "El carrito está vacío"
    And no genera ningún pedido

  Scenario: Pago rechazado
    When el banco rechaza el pago
    Then el sistema muestra "Pago con tarjeta rechazado"
    But el pedido no se registra
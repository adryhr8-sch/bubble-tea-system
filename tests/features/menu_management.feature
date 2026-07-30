# features/menu_management.feature
Feature: Administración del menú
  Como administrador
  Quiero agregar o modificar bebidas
  Para mantener actualizado el menú o catálogo

  Background:
    Given que el administrador inicia sesión

  Scenario: Agregar bebida
    When registra una bebida llamada "Matcha Latte"
    And asigna un precio de $95
    Then el sistema agrega la bebida al catálogo

  Scenario: Modificar precio
    When cambia el precio de una bebida existente
    Then el sistema guarda el nuevo precio

  Scenario: Bebida duplicada
    When intenta registrar una bebida con un nombre existente
    Then el sistema muestra "La bebida ya existe"
    But no crea un nuevo registro
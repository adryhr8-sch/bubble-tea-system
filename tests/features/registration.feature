Feature: Registro de clientes
  Como cliente
  Quiero crear una cuenta
  Para realizar pedidos y consultar mi historial de pedidos

  Background:
    Given que el usuario se encuentra en la pantalla de registro

  Scenario: Registro exitoso
    When ingresa un nombre válido
    And ingresa un correo no registrado
    And escribe una contraseña válida
    Then el sistema crea la cuenta
    And muestra el mensaje "Registro exitoso"

  Scenario: Correo ya registrado
    When el usuario ingresa un correo existente
    Then el sistema rechaza el registro
    And muestra el mensaje "El correo ya está registrado"
    But no crea una nueva cuenta

  Scenario: Contraseña demasiado corta
    When el usuario ingresa una contraseña de 5 caracteres
    Then el sistema muestra el mensaje "La contraseña debe tener al menos 8 caracteres"
    And no registra al usuario
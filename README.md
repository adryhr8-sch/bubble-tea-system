# Base de datos SQLite - Bubble Tea System

Archivo principal: `bubble_tea.db`

Tablas:
- users: 10 registros
- teas: 10 registros
- toppings: 10 registros
- orders: 10 registros
- order_items: 10 registros
- order_status_updates: 20 registros

Relaciones:
- users 1:N orders
- orders 1:N order_items
- teas 1:N order_items
- orders 1:N order_status_updates
- users 1:N order_status_updates

Índices incluidos en campos relevantes.



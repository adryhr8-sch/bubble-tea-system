PRAGMA foreign_keys = ON;

INSERT INTO users (name,email,password,created_at) VALUES
('Ana López','ana@gmail.com','12345678','2026-07-01 09:00:00'),
('Luis Hernández','luis@gmail.com','12345678','2026-07-02 09:15:00'),
('Carlos Martínez','carlos@gmail.com','12345678','2026-07-03 10:00:00'),
('María García','maria@gmail.com','12345678','2026-07-04 10:30:00'),
('Pedro Sánchez','pedro@gmail.com','12345678','2026-07-05 11:00:00'),
('Laura Torres','laura@gmail.com','12345678','2026-07-06 11:30:00'),
('Miguel Ramírez','miguel@gmail.com','12345678','2026-07-07 12:00:00'),
('José Flores','jose@gmail.com','12345678','2026-07-08 12:30:00'),
('Sofía Cruz','sofia@gmail.com','12345678','2026-07-09 13:00:00'),
('Elena Vargas','elena@gmail.com','12345678','2026-07-10 13:30:00');

INSERT INTO teas (name,price,available,created_at) VALUES
('Taro Milk Tea',75.00,1,'2026-07-01 08:00:00'),
('Matcha Latte',95.00,1,'2026-07-01 08:05:00'),
('Thai Tea',80.00,1,'2026-07-01 08:10:00'),
('Brown Sugar Milk Tea',90.00,1,'2026-07-01 08:15:00'),
('Classic Milk Tea',70.00,1,'2026-07-01 08:20:00'),
('Mango Tea',72.00,1,'2026-07-01 08:25:00'),
('Strawberry Tea',78.00,1,'2026-07-01 08:30:00'),
('Coconut Milk Tea',82.00,1,'2026-07-01 08:35:00'),
('Chocolate Milk Tea',88.00,1,'2026-07-01 08:40:00'),
('Passion Fruit Tea',76.00,1,'2026-07-01 08:45:00');

INSERT INTO toppings (name,price,stock,available) VALUES
('Tapioca',12.00,50,1),
('Popping Boba',15.00,45,1),
('Jelly de Mango',13.00,40,1),
('Jelly de Coco',13.00,35,1),
('Perlas de Fresa',16.00,30,1),
('Cheesecake',18.00,25,1),
('Crema Batida',10.00,60,1),
('Pudding',14.00,20,1),
('Aloe Vera',12.00,28,1),
('Fruta Fresca',20.00,18,1);

INSERT INTO orders
(user_id,total_price,status,payment_method,payment_status,order_number,created_at,updated_at) VALUES
(1,87.00,'Entregado','Tarjeta','Aprobado','BT202607010001','2026-07-11 09:00:00','2026-07-11 09:40:00'),
(2,107.00,'Entregado','Efectivo','Pendiente','BT202607010002','2026-07-11 10:00:00','2026-07-11 10:45:00'),
(3,108.00,'Listo','Tarjeta','Aprobado','BT202607010003','2026-07-12 11:00:00','2026-07-12 11:35:00'),
(4,102.00,'En preparación','Tarjeta','Aprobado','BT202607010004','2026-07-12 12:00:00','2026-07-12 12:20:00'),
(5,90.00,'Pendiente','Efectivo','Pendiente','BT202607010005','2026-07-13 13:00:00','2026-07-13 13:00:00'),
(6,106.00,'Entregado','Tarjeta','Aprobado','BT202607010006','2026-07-13 14:00:00','2026-07-13 14:50:00'),
(7,94.00,'Listo','Efectivo','Pendiente','BT202607010007','2026-07-14 15:00:00','2026-07-14 15:35:00'),
(8,112.00,'En preparación','Tarjeta','Aprobado','BT202607010008','2026-07-14 16:00:00','2026-07-14 16:25:00'),
(9,96.00,'Entregado','Tarjeta','Aprobado','BT202607010009','2026-07-15 17:00:00','2026-07-15 17:45:00'),
(10,102.00,'Pendiente','Efectivo','Pendiente','BT202607010010','2026-07-15 18:00:00','2026-07-15 18:00:00');

INSERT INTO order_items
(order_id,tea_id,size,sugar_level,ice_level,quantity,unit_price) VALUES
(1,1,'Mediano','50%','Normal',1,87.00),
(2,2,'Grande','50%','Normal',1,107.00),
(3,3,'Mediano','100%','Poco hielo',1,108.00),
(4,4,'Mediano','50%','Normal',1,102.00),
(5,5,'Mediano','0%','Normal',1,90.00),
(6,6,'Grande','50%','Extra hielo',1,106.00),
(7,7,'Mediano','50%','Normal',1,94.00),
(8,8,'Grande','100%','Poco hielo',1,112.00),
(9,9,'Mediano','50%','Normal',1,96.00),
(10,10,'Mediano','0%','Sin hielo',1,102.00);

INSERT INTO order_status_updates
(order_id,old_status,new_status,updated_at,updated_by) VALUES
(1,'Pendiente','En preparación','2026-07-11 09:15:00',1),
(2,'Pendiente','En preparación','2026-07-11 10:15:00',2),
(3,'Pendiente','En preparación','2026-07-12 11:10:00',3),
(4,'Pendiente','En preparación','2026-07-12 12:10:00',4),
(5,NULL,'Pendiente','2026-07-13 13:00:00',5),
(6,'Pendiente','En preparación','2026-07-13 14:15:00',6),
(7,'Pendiente','En preparación','2026-07-14 15:10:00',7),
(8,'Pendiente','En preparación','2026-07-14 16:10:00',8),
(9,'Pendiente','En preparación','2026-07-15 17:15:00',9),
(10,NULL,'Pendiente','2026-07-15 18:00:00',10);

INSERT INTO order_status_updates
(order_id,old_status,new_status,updated_at,updated_by) VALUES
(1,'En preparación','Listo','2026-07-11 09:30:00',1),
(1,'Listo','Entregado','2026-07-11 09:40:00',1),
(2,'En preparación','Listo','2026-07-11 10:35:00',2),
(2,'Listo','Entregado','2026-07-11 10:45:00',2),
(3,'En preparación','Listo','2026-07-12 11:35:00',3),
(6,'En preparación','Listo','2026-07-13 14:35:00',6),
(6,'Listo','Entregado','2026-07-13 14:50:00',6),
(7,'En preparación','Listo','2026-07-14 15:35:00',7),
(9,'En preparación','Listo','2026-07-15 17:35:00',9),
(9,'Listo','Entregado','2026-07-15 17:45:00',9);

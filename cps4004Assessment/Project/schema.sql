CREATE TABLE IF NOT EXISTS users (
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL UNIQUE,
password_hash TEXT NOT NULL,
role TEXT NOT NULL CHECK(role IN('admin', 'manager', 'warehouse_staff', 'driver'))
);

CREATE TABLE IF NOT EXISTS customers(
customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
phone TEXT,
email TEXT,
address TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS warehouses(
warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
location TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory_items(
item_id INTEGER PRIMARY KEY AUTOINCREMENT,
item_name TEXT NOT NULL,
description TEXT,
reorder_level INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS vehicles(
vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
registration_number TEXT NOT NULL UNIQUE,
capacity REAL NOT NULL,
maintenance_date TEXT,
availability_status TEXT NOT NULL CHECK (availability_status IN('Available', 'In Use', 'Under Maintenance'))
);

CREATE TABLE IF NOT EXISTS drivers(
driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
phone TEXT,
license_number TEXT NOT NULL UNIQUE,
shift_assignment TEXT NOT NULL CHECK (shift_assignment IN('Morning', 'Afternoon', 'Evening', 'Night'))
);

CREATE TABLE IF NOT EXISTS shipments(
shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
order_number TEXT NOT NULL UNIQUE,
sender_customer_id INTEGER NOT NULL,
receiver_customer_id INTEGER NOT NULL,
item_description TEXT NOT NULL,
assigned_driver_id INTEGER,
assigned_vehicle_id INTEGER,
delivery_status TEXT NOT NULL CHECK(delivery_status IN('Pending', 'In Transit', 'Delivered', 'Delayed', 'Returned')),
delivery_date TEXT,
route_details TEXT,
transport_cost REAL,
payment_status TEXT NOT NULL CHECK(payment_status IN('Unpaid', 'Paid', 'Refunded')),
FOREIGN KEY (sender_customer_id) REFERENCES customers(customer_id),
FOREIGN KEY (receiver_customer_id) REFERENCES customers(customer_id),
FOREIGN KEY (assigned_driver_id) REFERENCES drivers(driver_id),
FOREIGN KEY (assigned_vehicle_id) REFERENCES vehicles(vehicle_id)
);

CREATE TABLE IF NOT EXISTS warehouse_inventory(
inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
warehouse_id INTEGER NOT NULL,
item_id INTEGER NOT NULL,
quantity INTEGER NOT NULL,
item_location TEXT,
FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
FOREIGN KEY (item_id) REFERENCES inventory_items(item_id)
);

CREATE TABLE IF NOT EXISTS incidents(
incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
shipment_id INTEGER NOT NULL,
incident_type TEXT NOT NULL CHECK(incident_type IN('Delay', 'Route Change', 'Damaged Goods', 'Failed Delivery')),
description TEXT NOT NULL,
reported_at TEXT DEFAULT CURRENT_TIMESTAMP,
resolution_status TEXT NOT NULL CHECK(resolution_status IN('Open', 'In Progress', 'Resolved')),
FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id)
);

CREATE TABLE IF NOT EXISTS warehouse_activity(
activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
warehouse_id INTEGER NOT NULL,
item_id INTEGER NOT NULL,
activity_type TEXT NOT NULL CHECK(activity_type IN('Inbound', 'Outbound', 'Restock', 'Transfer')),
quantity INTEGER NOT NULL,
activity_date TEXT DEFAULT CURRENT_TIMESTAMP,
notes TEXT,
FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
FOREIGN KEY (item_id) REFERENCES inventory_items(item_id)
);

CREATE TABLE IF NOT EXISTS audit_log(
log_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
action TEXT NOT NULL,
table_name TEXT NOT NULL,
record_id INTEGER NOT NULL,
action_time TEXT DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users(user_id)
);
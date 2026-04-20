import sqlite3

conn = sqlite3.connect("northshore.db")
cur = conn.cursor()

cur.execute("PRAGMA foreign_keys = ON")
with open("schema.sql", "r", encoding="utf-8") as file:
    schema_sql = file.read()

cur.executescript(schema_sql)

print("Database created successfully")

users = [
    ("admin", "admin123", "admin"),
    ("manager", "manager123", "manager"),
    ("warehouse_staff", "staff123", "warehouse_staff"),
    ("driver", "driver123", "driver"),
]

for row in users:
    cur.execute("INSERT OR IGNORE INTO users(username, password_hash, role) VALUES (?, ?, ?)", row)

customers = [
    ("John Smith", "+442079460000", "johnsmith@gmail.com", "London, Baker Street 221B"),
    ("Amazon UK", "+4416183856274", "amazonsupply@amazon.co.uk", "Manchester, Warehouse District 12")
]
for customer in customers:
    cur.execute("INSERT OR IGNORE INTO customers(name, phone, email, address) VALUES (?, ?, ?, ?)", customer)

shipments = [
    ("ORD001", 2, 1, "Kitchen equipment", "Pending", "Unpaid")
]

for shipment in shipments:
    cur.execute("INSERT OR IGNORE INTO shipments(order_number, sender_customer_id, receiver_customer_id, item_description, delivery_status, payment_status) VALUES (?, ?, ?, ?, ?, ?)", shipment)
    cur.execute("UPDATE shipments SET assigned_driver_id = 1, assigned_vehicle_id = 1 WHERE order_number = ?", (shipment[0], ))


drivers = [
    ("Steve Rogers", "+4483249514", "3858385838285748", "Afternoon"),
    ("Anthony Stark", "+4478886251", "4848281929485750", "Evening"),
    ("Stephen Strange", "+4483441211", "4828919385658385", "Night")
]
for driver in drivers:
    cur.execute("INSERT OR IGNORE INTO drivers(name, phone, license_number, shift_assignment) VALUES (?, ?, ?, ?)", driver)

vehicles = [
    ("F235PD", 500, "2026-04-15", "Available"),
    ("S540FS", 1000, "2025-12-10", "Under Maintenance"),
    ("O204PA", 1500, "2026-01-05", "In Use")
]
for vehicle in vehicles:
    cur.execute("INSERT OR IGNORE INTO vehicles(registration_number, capacity, maintenance_date, availability_status) VALUES (?, ?, ?, ?)", vehicle)

incidents = [
    (1, "Delay", "Busy traffic", "Resolved")
]
for incident in incidents:
    cur.execute("INSERT OR IGNORE INTO incidents(shipment_id, incident_type, description, resolution_status) VALUES (?, ?, ?, ?)", incident)

warehouses = [
    ("London Hub", "London, United Kingdom"),
    ("Manchester Hub", "Manchester, United Kingdom")
]
for warehouse in warehouses:
    cur.execute("INSERT OR IGNORE INTO warehouses(name, location) VALUES (?, ?)", warehouse)

inventory = [
    ("Electronics", "Personal computer", 10),
    ("Kitchen equipment", "Plates", 500),
    ("Furniture", "Double bed", 20),
    ("Alcohol", "Whiskey (Jameson)", 100)
]

for item in inventory:
    cur.execute("INSERT OR IGNORE INTO inventory_items(item_name, description, reorder_level) VALUES (?, ?, ?)", item)

warehouse_inventory_data = [
    (1, 1, 32, "Zone A"),
    (1, 2, 2200, "Zone F"),
    (2, 3, 23, "Zone B"),
    (2, 4, 132, "Zone C")
]
for data in warehouse_inventory_data:
    cur.execute("INSERT OR IGNORE INTO warehouse_inventory(warehouse_id, item_id, quantity, item_location) VALUES (?, ?, ?, ?)", data)

activity = [
    (1, 1, "Inbound", 5, "5 additional personal computers"),
    (1, 2, "Outbound", 300, "A delivery to local restaurant in London"),
    (2, 3, "Transfer", 20, "Transfer of equipment to London Hub")
]
for activities in activity:
    cur.execute("INSERT OR IGNORE INTO warehouse_activity(warehouse_id, item_id, activity_type, quantity, notes) VALUES (?, ?, ?, ?, ?)", activities)


conn.commit()


conn.close()


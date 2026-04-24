import tkinter as tk
from tkinter import ttk
import sqlite3
from security import verify_user, log_login_attempt, hash_password

root = tk.Tk()
root.withdraw()
root.title("Northshore Logistics System")
root.geometry("900x600")
root.minsize(700,500)
title_label = tk.Label(root, text="Northshore Logistics Management System", font=("Arial", 18, "bold"))
title_label.pack(pady=20)


def role_access(role):
    if role == "admin":
        users_button.config(state="normal")
        customers_button.config(state="normal")
        shipments_button.config(state="normal")
        warehouse_inventory_button.config(state="normal")
        drivers_button.config(state="normal")
        vehicles_button.config(state="normal")
        inventory_button.config(state="normal")
        reports_button.config(state="normal")
        audit_button.config(state="normal")
        warehouses_button.config(state="normal")
        incidents_button.config(state="normal")
        warehouse_activity_button.config(state="normal")
    elif role == "manager":
        users_button.config(state="disabled")
        customers_button.config(state="normal")
        shipments_button.config(state="normal")
        warehouse_inventory_button.config(state="normal")
        drivers_button.config(state="normal")
        vehicles_button.config(state="normal")
        inventory_button.config(state="normal")
        reports_button.config(state="normal")
        audit_button.config(state="disabled")
        warehouses_button.config(state="normal")
        incidents_button.config(state="normal")
        warehouse_activity_button.config(state="normal")
    elif role == "warehouse_staff":
        users_button.config(state="disabled")
        customers_button.config(state="normal")
        shipments_button.config(state="normal")
        warehouse_inventory_button.config(state="normal")
        drivers_button.config(state="disabled")
        vehicles_button.config(state="disabled")
        inventory_button.config(state="normal")
        reports_button.config(state="normal")
        audit_button.config(state="disabled")
        warehouses_button.config(state="disabled")
        incidents_button.config(state="disabled")
        warehouse_activity_button.config(state="normal")
    elif role == "driver":
        users_button.config(state="disabled")
        customers_button.config(state="disabled")
        shipments_button.config(state="normal")
        warehouse_inventory_button.config(state="disabled")
        drivers_button.config(state="disabled")
        vehicles_button.config(state="disabled")
        inventory_button.config(state="disabled")
        reports_button.config(state="disabled")
        audit_button.config(state="disabled")
        warehouses_button.config(state="disabled")
        incidents_button.config(state="normal")
        warehouse_activity_button.config(state="disabled")

def open_login_window():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("900x600")

    login_label = tk.Label(login_window, text="Login to your account", font=("Arial", 18, "bold"))
    login_label.pack(pady=20)
    login_frame = tk.Frame(login_window)
    login_frame.pack(pady=20)

    username = tk.Label(login_frame, text="Username:", font=("Arial", 16, "bold"))
    username.grid(row=0, column=0, pady=10, padx=10)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, pady=10, padx=10)

    password = tk.Label(login_frame, text="Password:", font=("Arial", 16, "bold"))
    password.grid(row=1, column=0, pady=10, padx=10)
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, pady=10, padx=10)

    login_status = tk.Label(login_window, text="", font=("Arial", 12, "bold"))
    login_status.pack(pady=20)

    def verify_login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            log_login_attempt(username, "LOGIN_EMPTY_FIELDS")
            login_status.config(text="Please enter your username and password.", fg="red")
        else:
            role = verify_user(username, password)
            if role:
                log_login_attempt(username, "LOGIN_SUCCESS")
                login_status.config(text=f"Login Successful: {role}", fg="green")
                role_access(role)
                root.deiconify()
                login_window.destroy()
            else:
                log_login_attempt(username, "LOGIN_FAILED")
                login_status.config(text="Invalid username or password", fg="red")


    verify_login_button = tk.Button(login_window, text="Verify Login", width=20, height=2, command=verify_login)
    verify_login_button.pack(pady=20)


def logout():
    users_button.config(state="disabled")
    customers_button.config(state="disabled")
    shipments_button.config(state="disabled")
    warehouse_inventory_button.config(state="disabled")
    drivers_button.config(state="disabled")
    vehicles_button.config(state="disabled")
    inventory_button.config(state="disabled")
    reports_button.config(state="disabled")
    audit_button.config(state="disabled")
    warehouses_button.config(state="disabled")
    incidents_button.config(state="disabled")
    warehouse_activity_button.config(state="disabled")

    root.withdraw()
    open_login_window()


def open_users_window():
    users_window = tk.Toplevel(root)
    users_window.title("Users")
    users_window.geometry("900x600")

    users_title = tk.Label(users_window, text="Users Management", font=("Arial", 16, "bold"))
    users_title.pack(pady=20)
    users_frame = tk.Frame(users_window)
    users_frame.pack(pady=20)

    roles = ['admin', 'manager', 'warehouse_staff', 'driver']

    users_username = tk.Label(users_frame, text="Username:", font=("Arial", 12, "bold"))
    users_username.grid(row=0, column=0, pady=10, padx=10)
    users_username_entry = tk.Entry(users_frame)
    users_username_entry.grid(row=0, column=1, pady=10, padx=10)

    users_password = tk.Label(users_frame, text="Password:", font=("Arial", 12, "bold"))
    users_password.grid(row=1, column=0, pady=10, padx=10)
    users_password_entry = tk.Entry(users_frame, show="*")
    users_password_entry.grid(row=1, column=1, pady=10, padx=10)

    users_role = tk.Label(users_frame, text="Role:", font=("Arial", 12, "bold"))
    users_role.grid(row=2, column=0, pady=10, padx=10)
    users_role_combobox = ttk.Combobox(users_frame, values=roles)
    users_role_combobox.grid(row=2, column=1, pady=10, padx=10)

    users_status = tk.Label(users_window, text="", font=("Arial", 12, "bold"))
    users_status.pack(pady=20)

    def add_user():
        username = users_username_entry.get()
        password = users_password_entry.get()
        role = users_role_combobox.get()

        if not username or not password or not role:
            users_status.config(text="Username, Password or Role not defined", fg="red")
        else:
            conn = sqlite3.connect("northshore.db")
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO users(username, password_hash, role) VALUES (?, ?, ?)", (username, hash_password(password), role))
            conn.commit()
            conn.close()
            users_status.config(text="User added successfully", fg="green")
            users_username_entry.delete(0, tk.END)
            users_password_entry.delete(0, tk.END)
            users_role_combobox.set("")

    def view_users():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        users_text.delete("1.0", tk.END)
        cur.execute("SELECT user_id, username, role FROM users")
        users = cur.fetchall()
        conn.close()
        for user in users:
            users_text.insert(tk.END, f"\n\nUser ID: {user[0]}\nUsername: {user[1]}\nRole: {user[2]}\n")




    add_user_button = tk.Button(users_window, text="Add User", width=20, height=2, command=add_user)
    add_user_button.pack(pady=20)

    view_users_button = tk.Button(users_window, text="View Users", width=20, height=2, command=view_users)
    view_users_button.pack(pady=20)

    users_label = tk.Label(users_window, text="Users:", font=("Arial", 12, "bold"))
    users_label.pack(pady=20)
    users_text = tk.Text(users_window)
    users_text.pack(pady=20)

def open_customers_window():
    customers_window = tk.Toplevel(root)
    customers_window.title("Customers")
    customers_window.geometry("900x600")

    customers_title = tk.Label(customers_window, text="Customer Management", font=("Arial", 16, "bold"))
    customers_title.pack(pady=20)
    customers_frame = tk.Frame(customers_window)
    customers_frame.pack(pady=20)

    name = tk.Label(customers_frame, text="Name:", font=("Arial", 12, "bold"))
    name.grid(row=0, column=0, pady=10, padx=10)
    name_entry = tk.Entry(customers_frame)
    name_entry.grid(row=0, column=1)

    phone = tk.Label(customers_frame, text="Phone:", font=("Arial", 12, "bold"))
    phone.grid(row=1, column=0, pady=10, padx=10)
    phone_entry = tk.Entry(customers_frame)
    phone_entry.grid(row=1, column=1)

    email = tk.Label(customers_frame, text="Email:", font=("Arial", 12, "bold"))
    email.grid(row=2, column=0, pady=10, padx=10)
    email_entry = tk.Entry(customers_frame)
    email_entry.grid(row=2, column=1)

    address = tk.Label(customers_frame, text="Address:", font=("Arial", 12, "bold"))
    address.grid(row=3, column=0, pady=10, padx=10)
    address_entry = tk.Entry(customers_frame)
    address_entry.grid(row=3, column=1)

    status_label = tk.Label(customers_window, text="", font=("Arial", 12, "bold"))
    status_label.pack(pady=20)


    def add_customer():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()


        if not name or not phone or not email or not address:
            status_label.config(text="Name, Phone, Email or Address not defined", fg="red")

        else:
            conn = sqlite3.connect("northshore.db")
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO customers(name, phone, email, address) VALUES(?,?,?,?)",(name, phone, email, address))
            conn.commit()
            conn.close()
            status_label.config(text="Customer added successfully", fg="green")
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)

    def view_customers():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        customers_text.delete("1.0", tk.END)
        cur.execute("SELECT * FROM customers")
        customers = cur.fetchall()
        for customer in customers:
            customers_text.insert(tk.END, f"\n\n ID: {customer[0]}\n Name: {customer[1]}\n Phone: {customer[2]}\n Email: {customer[3]}\n Address: {customer[4]}")
        conn.close()



    add_customer_button = tk.Button(customers_window, text="Add Customer", width=20, height=2, command=add_customer)
    add_customer_button.pack(pady=10)

    view_customers_button = tk.Button(customers_window, text="View Customers", width=20, height=2, command=view_customers)
    view_customers_button.pack(pady=10)

    customer_label = tk.Label(customers_window, text="Customers:", font=("Arial", 12, "bold"))
    customer_label.pack(pady=20)
    customers_text = tk.Text(customers_window)
    customers_text.pack(pady=20)

def open_warehouses_window():
    warehouses_window = tk.Toplevel(root)
    warehouses_window.title("Warehouses")
    warehouses_window.geometry("900x600")

    warehouses_title = tk.Label(warehouses_window, text="Warehouses Management", font=("Arial", 16, "bold"))
    warehouses_title.pack(pady=20)
    warehouses_frame = tk.Frame(warehouses_window)
    warehouses_frame.pack(pady=20)

    warehouse_name = tk.Label(warehouses_frame, text="Warehouse Name:", font=("Arial", 12, "bold"))
    warehouse_name.grid(row=0, column=0, pady=10, padx=10)
    warehouse_name_entry = tk.Entry(warehouses_frame)
    warehouse_name_entry.grid(row=0, column=1)

    warehouse_location = tk.Label(warehouses_frame, text="Warehouse Location:", font=("Arial", 12, "bold"))
    warehouse_location.grid(row=1, column=0, pady=10, padx=10)
    warehouse_location_entry = tk.Entry(warehouses_frame)
    warehouse_location_entry.grid(row=1, column=1)

    warehouse_status = tk.Label(warehouses_window, text="", font=("Arial", 12, "bold"))
    warehouse_status.pack(pady=20)

    def add_warehouse():
        name = warehouse_name_entry.get()
        location = warehouse_location_entry.get()

        if not name or not location:
            warehouse_status.config(text="Warehouse name or location not defined", fg="red")
        else:
            conn = sqlite3.connect("northshore.db")
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO warehouses(name, location) VALUES(?,?)", (name, location))
            conn.commit()
            conn.close()
            warehouse_status.config(text="Warehouse added successfully", fg="green")
            warehouse_name_entry.delete(0, tk.END)
            warehouse_location_entry.delete(0, tk.END)

    def view_warehouses():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        warehouse_text.delete("1.0", tk.END)
        cur.execute("SELECT * FROM warehouses")
        warehouses = cur.fetchall()
        conn.close()
        for warehouse in warehouses:
            warehouse_text.insert(tk.END, f"\n\n Warehouse ID: {warehouse[0]}\nWarehouse Name: {warehouse[1]}\nWarehouse Location: {warehouse[2]}\n")


    add_warehouse_button = tk.Button(warehouses_window, text="Add Warehouse", width=20, height=2, command=add_warehouse)
    add_warehouse_button.pack(pady=10)

    view_warehouses_button = tk.Button(warehouses_window, text="View Warehouses", width=20, height=2, command=view_warehouses)
    view_warehouses_button.pack(pady=10)

    warehouse_label = tk.Label(warehouses_window, text="Warehouse:", font=("Arial", 12, "bold"))
    warehouse_label.pack(pady=20)
    warehouse_text = tk.Text(warehouses_window)
    warehouse_text.pack(pady=20)


def open_shipments_window():
    shipments_window = tk.Toplevel(root)
    shipments_window.title("Shipments")
    shipments_window.geometry("900x600")

    shipments_title = tk.Label(shipments_window, text="Shipments Management", font=("Arial", 16, "bold"))
    shipments_title.pack(pady=20)

    shipments_frame = tk.Frame(shipments_window)
    shipments_frame.pack(pady=20)

    conn = sqlite3.connect("northshore.db")
    cur = conn.cursor()
    cur.execute("SELECT customer_id, name FROM customers")
    customers = cur.fetchall()
    conn.close()
    customers_data = []
    for customer in customers:
        customers_data.append(f"{customer[0]} - {customer[1]}")

    delivery_statuses = ["Pending", "In Transit", "Delivered", "Delayed", "Returned"]
    payment_statuses = ["Unpaid", "Paid", "Refunded"]

    order_number = tk.Label(shipments_frame, text="Order number:", font=("Arial", 12, "bold"))
    order_number.grid(row=0, column=0, pady=10)
    order_number_entry = tk.Entry(shipments_frame)
    order_number_entry.grid(row=0, column=1)

    sender_title = tk.Label(shipments_frame, text="Sender:", font=("Arial", 12, "bold"))
    sender_title.grid(row=1, column=0, pady=10, padx=10)
    sender_combobox = ttk.Combobox(shipments_frame, values=customers_data, state="readonly")
    sender_combobox.grid(row=1, column=1)
    sender_combobox.grid(row=1, column=1, pady=10, padx=10)

    receiver_title = tk.Label(shipments_frame, text="Receiver:", font=("Arial", 12, "bold"))
    receiver_title.grid(row=2, column=0, pady=10, padx=10)
    receiver_combobox = ttk.Combobox(shipments_frame, values=customers_data, state="readonly")
    receiver_combobox.grid(row=2, column=1, pady=10, padx=10)


    item_description = tk.Label(shipments_frame, text="Item description:", font=("Arial", 12, "bold"))
    item_description.grid(row=3, column=0, pady=10)
    item_description_entry = tk.Entry(shipments_frame)
    item_description_entry.grid(row=3, column=1)

    status = tk.Label(shipments_frame, text="Delivery status:", font=("Arial", 12, "bold"))
    status.grid(row=4, column=0, pady=10, padx=10)
    status_combobox = ttk.Combobox(shipments_frame, values=delivery_statuses, state="readonly")
    status_combobox.grid(row=4, column=1, pady=10, padx=10)

    payment = tk.Label(shipments_frame, text="Payment status:", font=("Arial", 12, "bold"))
    payment.grid(row=5, column=0, pady=10, padx=10)
    payment_combobox = ttk.Combobox(shipments_frame, values=payment_statuses, state="readonly")
    payment_combobox.grid(row=5, column=1, pady=10, padx=10)

    shipment_status_label = tk.Label(shipments_window, text="", font=("Arial", 16, "bold"))
    shipment_status_label.pack(pady=20)

    def add_shipment():
        order = order_number_entry.get()
        sender = sender_combobox.get()
        receiver = receiver_combobox.get()
        description = item_description_entry.get()
        status = status_combobox.get()
        payment = payment_combobox.get()

        if not order or not sender or not receiver or not description or not status or not payment:
            shipment_status_label.config(text="Order number, sender, receiver, description, delivery or payment status not defined", fg="red")
        else:
            sender_id = int(sender.split(" - ")[0])
            receiver_id = int(receiver.split(" - ")[0])
            conn = sqlite3.connect("northshore.db")
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO shipments(order_number, sender_customer_id, receiver_customer_id, item_description, delivery_status, payment_status) VALUES(?,?,?,?,?,?)",(order, sender_id, receiver_id, description, status, payment))
            conn.commit()
            conn.close()
            shipment_status_label.config(text="Shipment added successfully", fg="green")
            order_number_entry.delete(0, tk.END)
            sender_combobox.set("")
            receiver_combobox.set("")
            item_description_entry.delete(0, tk.END)
            status_combobox.set("")
            payment_combobox.set("")

    def view_shipments():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        shipments_text.delete("1.0", tk.END)
        cur.execute('''
        SELECT 
            s.order_number,
            sender.name, 
            receiver.name, 
            s.item_description,
            s.delivery_status,
            s.payment_status
        FROM shipments s
        JOIN customers sender
             ON s.sender_customer_id = sender.customer_id
        JOIN customers receiver
             ON s.receiver_customer_id = receiver.customer_id
        ''')
        shipments = cur.fetchall()
        conn.close()
        for shipment in shipments:
            shipments_text.insert(tk.END, f"\n\nOrder number: {shipment[0]}\nSender: {shipment[1]}\nReceiver: {shipment[2]}\nDescription: {shipment[3]}\nDelivery status: {shipment[4]}\nPayment status: {shipment[5]}\n\n")


    add_shipment_button = tk.Button(shipments_window, text="Add Shipment", width=20, height=2, command=add_shipment)
    add_shipment_button.pack(pady=10)

    view_shipments_button = tk.Button(shipments_window, text="View Shipments", width=20, height=2, command=view_shipments)
    view_shipments_button.pack(pady=10)

    shipments_label = tk.Label(shipments_window, text="Shipments:", font=("Arial", 12, "bold"))
    shipments_label.pack(pady=20)
    shipments_text = tk.Text(shipments_window)
    shipments_text.pack(pady=20)

def open_warehouse_inventory_window():
    warehouse_inventory_window = tk.Toplevel(root)
    warehouse_inventory_window.title("Warehouse Inventory")
    warehouse_inventory_window.geometry("900x600")

    warehouse_inventory_title = tk.Label(warehouse_inventory_window, text="Warehouse Inventory Management", font=("Arial", 16, "bold"))
    warehouse_inventory_title.pack(pady=20)
    warehouse_inventory_frame = tk.Frame(warehouse_inventory_window)
    warehouse_inventory_frame.pack(pady=20)

    conn = sqlite3.connect("northshore.db")
    cur = conn.cursor()
    cur.execute("SELECT warehouse_id, name FROM warehouses")
    warehouse_rows = cur.fetchall()
    cur.execute("SELECT item_id, item_name FROM inventory_items")
    item_rows = cur.fetchall()
    conn.close()
    warehouse_options = []
    for warehouse in warehouse_rows:
        warehouse_options.append(f"{warehouse[0]} - {warehouse[1]}")
    item_options = []
    for item in item_rows:
        item_options.append(f"{item[0]} - {item[1]}")

    warehouse_name = tk.Label(warehouse_inventory_frame, text="Warehouse:", font=("Arial", 12, "bold"))
    warehouse_name.grid(row=0, column=0, pady=10, padx=10)
    warehouse_combobox = ttk.Combobox(warehouse_inventory_frame, values=warehouse_options, state="readonly")
    warehouse_combobox.grid(row=0, column=1, pady=10, padx=10)

    item_name = tk.Label(warehouse_inventory_frame, text="Item:", font=("Arial", 12, "bold"))
    item_name.grid(row=1, column=0, pady=10, padx=10)
    item_combobox = ttk.Combobox(warehouse_inventory_frame, values=item_options, state="readonly")
    item_combobox.grid(row=1, column=1, pady=10, padx=10)

    warehouse_quantity = tk.Label(warehouse_inventory_frame, text="Quantity:", font=("Arial", 12, "bold"))
    warehouse_quantity.grid(row=2, column=0, pady=10, padx=10)
    quantity_entry = tk.Entry(warehouse_inventory_frame)
    quantity_entry.grid(row=2, column=1, pady=10, padx=10)

    item_location = tk.Label(warehouse_inventory_frame, text="Location:", font=("Arial", 12, "bold"))
    item_location.grid(row=3, column=0, pady=10, padx=10)
    location_entry = tk.Entry(warehouse_inventory_frame)
    location_entry.grid(row=3, column=1, pady=10, padx=10)

    warehouse_inventory_status = tk.Label(warehouse_inventory_window, text="", font=("Arial", 12, "bold"))
    warehouse_inventory_status.pack(pady=20)

    def add_inventory_record():
        warehouse_value = warehouse_combobox.get()
        item_value = item_combobox.get()
        quantity_text = quantity_entry.get()
        item_location = location_entry.get()

        if not warehouse_value or not item_value or not quantity_text or not item_location:
            warehouse_inventory_status.config(text="Warehouse, Item, Quantity or Location not defined", fg="red")
        else:
            try:
                warehouse_id = int(warehouse_value.split(" - ")[0])
                item_id = int(item_value.split(" - ")[0])
                quantity = int(quantity_text)

                conn = sqlite3.connect("northshore.db")
                cur = conn.cursor()
                cur.execute("INSERT OR IGNORE INTO warehouse_inventory(warehouse_id, item_id, quantity, item_location) VALUES (?,?,?,?)", (warehouse_id, item_id, quantity, item_location))
                conn.commit()
                conn.close()
                warehouse_inventory_status.config(text="Inventory record added successfully", fg="green")
                warehouse_combobox.set("")
                item_combobox.set("")
                quantity_entry.delete(0, tk.END)
                location_entry.delete(0, tk.END)
            except ValueError:
                warehouse_inventory_status.config(text="Quantity must be a whole number", fg="red")

    def view_inventory_records():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        warehouse_inventory_text.delete("1.0", tk.END)
        cur.execute('''
        SELECT
         wi.inventory_id,
         w.name,
         i.item_name,
         wi.quantity,
         wi.item_location
        FROM warehouse_inventory wi
         JOIN warehouses w ON wi.warehouse_id = w.warehouse_id
         JOIN inventory_items i ON wi.item_id = i.item_id
        ''')
        records = cur.fetchall()
        conn.close()
        for record in records:
            warehouse_inventory_text.insert(tk.END, f"\n\nInventory ID: {record[0]}\nWarehouse: {record[1]}\nItem: {record[2]}\n Quantity: {record[3]}\nItem Location: {record[4]}\n")


    add_inventory_button = tk.Button(warehouse_inventory_window, text="Add Inventory Record", width=20, height=2, command=add_inventory_record)
    add_inventory_button.pack(pady=20)

    view_inventory_button = tk.Button(warehouse_inventory_window, text="View Inventory Records", width=20, height=2, command=view_inventory_records)
    view_inventory_button.pack(pady=20)

    warehouse_inventory_label = tk.Label(warehouse_inventory_window, text="Warehouse Inventory Records:", font=("Arial", 12, "bold"))
    warehouse_inventory_label.pack(pady=20)
    warehouse_inventory_text = tk.Text(warehouse_inventory_window)
    warehouse_inventory_text.pack(pady=20)


def open_drivers_window():
    drivers_window = tk.Toplevel(root)
    drivers_window.title("Drivers")
    drivers_window.geometry("900x600")

    drivers_title = tk.Label(drivers_window, text="Drivers Management", font=("Arial", 16, "bold"))
    drivers_title.pack(pady=20)
    drivers_frame = tk.Frame(drivers_window)
    drivers_frame.pack(pady=20)

    driver_name = tk.Label(drivers_frame, text="Name:", font=("Arial", 12, "bold"))
    driver_name.grid(row=0, column=0)
    driver_name_entry = tk.Entry(drivers_frame)
    driver_name_entry.grid(row=0, column=1)

    driver_phone = tk.Label(drivers_frame, text="Phone:", font=("Arial", 12, "bold"))
    driver_phone.grid(row=1, column=0)
    driver_phone_entry = tk.Entry(drivers_frame)
    driver_phone_entry.grid(row=1, column=1)

    license_number = tk.Label(drivers_frame, text="Licence Number:", font=("Arial", 12, "bold"))
    license_number.grid(row=2, column=0)
    license_number_entry = tk.Entry(drivers_frame)
    license_number_entry.grid(row=2, column=1)

    assignment = ['Morning', 'Afternoon', 'Evening', 'Night']

    shift_assignment = tk.Label(drivers_frame, text="Shift Assignment:", font=("Arial", 12, "bold"))
    shift_assignment.grid(row=3, column=0)
    shift_assignment_combobox = ttk.Combobox(drivers_frame, values=assignment, state="readonly")
    shift_assignment_combobox.grid(row=3, column=1)

    driver_status = tk.Label(drivers_window, text="", font=("Arial", 12, "bold"))
    driver_status.pack(pady=20)

    def add_driver():
        driver_name = driver_name_entry.get()
        driver_phone = driver_phone_entry.get()
        license_number = license_number_entry.get()
        shift_assignment = shift_assignment_combobox.get()

        if not driver_name or not driver_phone or not license_number or not shift_assignment:
            driver_status.config(text="Name, phone, license number or shift assignment not defined", fg="red")
        else:
            conn = sqlite3.connect("northshore.db")
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO drivers(name, phone, license_number, shift_assignment) VALUES(?,?,?,?)", (driver_name, driver_phone, license_number, shift_assignment))
            conn.commit()
            conn.close()
            driver_status.config(text="Driver added successfully", fg="green")
            driver_name_entry.delete(0, tk.END)
            driver_phone_entry.delete(0, tk.END)
            license_number_entry.delete(0, tk.END)
            shift_assignment_combobox.set("")

    def view_drivers():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        drivers_text.delete("1.0", tk.END)
        cur.execute("SELECT * FROM drivers")
        drivers = cur.fetchall()
        conn.close()
        for driver in drivers:
            drivers_text.insert(tk.END, f"\n\nDriver ID: {driver[0]}\nDriver Name: {driver[1]}\nDriver Phone: {driver[2]}\nLicence Number: {driver[3]}\nShift Assignment: {driver[4]}\n")

    add_driver_button = tk.Button(drivers_window, text="Add Driver", width=20, height=2, command=add_driver)
    add_driver_button.pack(pady=10)

    view_drivers_button = tk.Button(drivers_window, text="View Drivers", width=20, height=2, command=view_drivers)
    view_drivers_button.pack(pady=10)

    drivers_label = tk.Label(drivers_window, text="Drivers:", font=("Arial", 12, "bold"))
    drivers_label.pack(pady=20)
    drivers_text = tk.Text(drivers_window)
    drivers_text.pack(pady=20)


def open_vehicles_window():
    vehicles_window = tk.Toplevel(root)
    vehicles_window.title("Vehicles")
    vehicles_window.geometry("900x600")

    vehicles_title = tk.Label(vehicles_window, text="Vehicles Management", font=("Arial", 16, "bold"))
    vehicles_title.pack(pady=20)
    vehicles_frame = tk.Frame(vehicles_window)
    vehicles_frame.pack(pady=20)

    registration_number = tk.Label(vehicles_frame, text="Registration Number:", font=("Arial", 12, "bold"))
    registration_number.grid(row=0, column=0)
    registration_number_entry = tk.Entry(vehicles_frame)
    registration_number_entry.grid(row=0, column=1)

    capacity = tk.Label(vehicles_frame, text="Capacity:", font=("Arial", 12, "bold"))
    capacity.grid(row=1, column=0)
    capacity_entry = tk.Entry(vehicles_frame)
    capacity_entry.grid(row=1, column=1)

    maintenance_date = tk.Label(vehicles_frame, text="Maintenance Date:", font=("Arial", 12, "bold"))
    maintenance_date.grid(row=2, column=0)
    maintenance_date_entry = tk.Entry(vehicles_frame)
    maintenance_date_entry.grid(row=2, column=1)

    availability_status = ['Available', 'In Use', 'Under Maintenance']

    availability_status_label = tk.Label(vehicles_frame, text="Availability Status:", font=("Arial", 12, "bold"))
    availability_status_label.grid(row=3, column=0)
    availability_status_combobox = ttk.Combobox(vehicles_frame, values=availability_status, state="readonly")
    availability_status_combobox.grid(row=3, column=1)

    vehicle_status = tk.Label(vehicles_window, text="", font=("Arial", 12, "bold"))
    vehicle_status.pack(pady=20)

    def add_vehicle():
        registration_number = registration_number_entry.get()
        capacity = capacity_entry.get()
        maintenance_date = maintenance_date_entry.get()
        availability_status = availability_status_combobox.get()

        if not registration_number or not capacity or not maintenance_date or not availability_status:
            vehicle_status.config(text="Registration number, capacity, maintenance date or availability status not defined", fg="red")
        else:
            conn = sqlite3.connect("northshore.db")
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO vehicles(registration_number, capacity, maintenance_date, availability_status) VALUES(?,?,?,?)", (registration_number, capacity, maintenance_date, availability_status))
            conn.commit()
            conn.close()
            vehicle_status.config(text="Vehicle added successfully", fg="green")
            registration_number_entry.delete(0, tk.END)
            capacity_entry.delete(0, tk.END)
            maintenance_date_entry.delete(0, tk.END)
            availability_status_combobox.set("")

    def view_vehicles():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        vehicles_text.delete("1.0", tk.END)
        cur.execute("SELECT * FROM vehicles")
        vehicles = cur.fetchall()
        conn.close()
        for vehicle in vehicles:
            vehicles_text.insert(tk.END, f"\n\nVehicle ID: {vehicle[0]}\nRegistration Number: {vehicle[1]}\nCapacity: {vehicle[2]}\nMaintenance Date: {vehicle[3]}\nAvailability Status: {vehicle[4]}\n")



    add_vehicle_button = tk.Button(vehicles_window, text="Add Vehicle", width=20, height=2, command=add_vehicle)
    add_vehicle_button.pack(pady=10)

    view_vehicles_button = tk.Button(vehicles_window, text="View Vehicles", width=20, height=2, command=view_vehicles)
    view_vehicles_button.pack(pady=10)

    vehicles_label = tk.Label(vehicles_window, text="Vehicles:", font=("Arial", 12, "bold"))
    vehicles_label.pack(pady=20)
    vehicles_text = tk.Text(vehicles_window)
    vehicles_text.pack(pady=20)

def open_inventory_window():
    inventory_window = tk.Toplevel(root)
    inventory_window.title("Inventory")
    inventory_window.geometry("900x600")

    inventory_title = tk.Label(inventory_window, text="Inventory Management", font=("Arial", 16, "bold"))
    inventory_title.pack(pady=20)
    inventory_frame = tk.Frame(inventory_window)
    inventory_frame.pack(pady=20)

    item_name = tk.Label(inventory_frame, text="Item Name:", font=("Arial", 12, "bold"))
    item_name.grid(row=0, column=0)
    item_name_entry = tk.Entry(inventory_frame)
    item_name_entry.grid(row=0, column=1)

    description = tk.Label(inventory_frame, text="Description:", font=("Arial", 12, "bold"))
    description.grid(row=1, column=0)
    description_entry = tk.Entry(inventory_frame)
    description_entry.grid(row=1, column=1)

    reorder_level = tk.Label(inventory_frame, text="Reorder Level:", font=("Arial", 12, "bold"))
    reorder_level.grid(row=2, column=0)
    reorder_level_entry = tk.Entry(inventory_frame)
    reorder_level_entry.grid(row=2, column=1)

    inventory_status = tk.Label(inventory_window, text="", font=("Arial", 12, "bold"))
    inventory_status.pack(pady=20)

    def add_item():
        item_name = item_name_entry.get()
        description = description_entry.get()
        reorder_level = reorder_level_entry.get()

        if not item_name or not description or not reorder_level:
            inventory_status.config(text="Item name, description or reorder level not defined", fg="red")
        else:
            try:
                reorder_level = int(reorder_level)
                conn = sqlite3.connect("northshore.db")
                cur = conn.cursor()
                cur.execute("INSERT OR IGNORE INTO inventory_items(item_name, description, reorder_level) VALUES(?,?,?)",(item_name, description, reorder_level))
                conn.commit()
                conn.close()
                inventory_status.config(text="Item added successfully", fg="green")
                item_name_entry.delete(0, tk.END)
                description_entry.delete(0, tk.END)
                reorder_level_entry.delete(0, tk.END)
            except ValueError:
                inventory_status.config(text="Reorder level must be a whole number", fg="red")

    def view_items():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        inventory_text.delete("1.0", tk.END)
        cur.execute("SELECT * FROM inventory_items")
        items = cur.fetchall()
        conn.close()
        for item in items:
            inventory_text.insert(tk.END, f"\n\nItem ID: {item[0]}\nItem Name: {item[1]}\nDescription: {item[2]}\nReorder Level: {item[3]}\n")

    add_item_button = tk.Button(inventory_window, text="Add Item", width=20, height=2, command=add_item)
    add_item_button.pack(pady=10)

    view_items_button = tk.Button(inventory_window, text="View Items", width=20, height=2, command=view_items)
    view_items_button.pack(pady=10)

    inventory_label = tk.Label(inventory_window, text="Items:", font=("Arial", 12, "bold"))
    inventory_label.pack(pady=20)
    inventory_text = tk.Text(inventory_window)
    inventory_text.pack(pady=20)


def open_reports_window():
    reports_window = tk.Toplevel(root)
    reports_window.title("Reports")
    reports_window.geometry("900x600")

    reports_title = tk.Label(reports_window, text="Reports", font=("Arial", 16, "bold"))
    reports_title.pack(pady=20)
    reports_frame = tk.Frame(reports_window)
    reports_frame.pack(pady=20)
    report_text = tk.Text(reports_window)
    report_text.pack(pady=20)

    def shipment_report():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        report_text.delete("1.0", tk.END)
        cur.execute("SELECT delivery_status, COUNT(*) FROM shipments GROUP BY delivery_status")
        shipments = cur.fetchall()
        conn.close()
        report_text.insert(tk.END, "Shipment Status Report \n\n")
        for shipment in shipments:
            report_text.insert(tk.END, f"{shipment[0]}: {shipment[1]}\n\n")

    def drivers_report():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        report_text.delete("1.0", tk.END)
        cur.execute("SELECT name, phone, shift_assignment FROM drivers")
        drivers = cur.fetchall()
        conn.close()
        report_text.insert(tk.END, "Drivers Report \n\n")
        for driver in drivers:
            report_text.insert(tk.END, f"Name: {driver[0]}\n\n Phone: {driver[1]}\n\n Assignment: {driver[2]}\n\n")

    def vehicles_report():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        report_text.delete("1.0", tk.END)
        cur.execute("SELECT registration_number, capacity, availability_status FROM vehicles")
        vehicles = cur.fetchall()
        conn.close()
        report_text.insert(tk.END, "Vehicles Report \n\n")
        for vehicle in vehicles:
            report_text.insert(tk.END, f"Registration number: {vehicle[0]}\n\n Capacity: {vehicle[1]}\n\n Status: {vehicle[2]}\n\n")

    def inventory_report():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        report_text.delete("1.0", tk.END)
        cur.execute("SELECT item_name, description, reorder_level FROM inventory_items")
        items = cur.fetchall()
        conn.close()
        report_text.insert(tk.END, "Inventory Report \n\n")
        for item in items:
            report_text.insert(tk.END, f"\nItem name: {item[0]}\n\nDescription: {item[1]}\n\nReorder level: {item[2]}\n\n")


    shipment_report_button = tk.Button(reports_frame, text="Shipment Report", width=20, height=2, command=shipment_report)
    shipment_report_button.grid(row=0,column=0, pady=10, padx=10)

    drivers_report_button = tk.Button(reports_frame, text="Drivers Report", width=20, height=2, command=drivers_report)
    drivers_report_button.grid(row=0, column=1, pady=10, padx=10)

    vehicles_report_button = tk.Button(reports_frame, text="Vehicles Report", width=20, height=2, command=vehicles_report)
    vehicles_report_button.grid(row=1, column=0, pady=10, padx=10)

    inventory_report_button = tk.Button(reports_frame, text="Inventory Report", width=20, height=2, command=inventory_report)
    inventory_report_button.grid(row=1, column=1, pady=10, padx=10)

def open_incidents_window():
    incidents_window = tk.Toplevel(root)
    incidents_window.title("Incidents")
    incidents_window.geometry("900x600")

    incidents_title = tk.Label(incidents_window, text="Incidents Management", font=("Arial", 16, "bold"))
    incidents_title.pack(pady=20)
    incidents_frame = tk.Frame(incidents_window)
    incidents_frame.pack(pady=20)

    conn = sqlite3.connect("northshore.db")
    cur = conn.cursor()
    cur.execute("SELECT shipment_id, order_number FROM shipments")
    incidents = cur.fetchall()
    conn.close()
    incidents_data = []
    for incident in incidents:
        incidents_data.append(f"{incident[0]} - {incident[1]}")

    incident_types = ['Delay', 'Route Change', 'Damaged Goods', 'Failed Delivery']
    status = ['Open', 'In Progress', 'Resolved']

    shipment_id = tk.Label(incidents_frame, text="Shipment ID:", font=("Arial", 12, "bold"))
    shipment_id.grid(row=0, column=0, pady=10, padx=10)
    shipment_id_combobox = ttk.Combobox(incidents_frame, values=incidents_data, state="readonly")
    shipment_id_combobox.grid(row=0, column=1)

    incident_type = tk.Label(incidents_frame, text="Incident Type:", font=("Arial", 12, "bold"))
    incident_type.grid(row=1, column=0, pady=10, padx=10)
    incident_type_combobox = ttk.Combobox(incidents_frame, values=incident_types, state="readonly")
    incident_type_combobox.grid(row=1, column=1)

    incident_description = tk.Label(incidents_frame, text="Description:", font=("Arial", 12, "bold"))
    incident_description.grid(row=2, column=0, pady=10, padx=10)
    incident_description_entry = tk.Entry(incidents_frame)
    incident_description_entry.grid(row=2, column=1)

    resolution_status = tk.Label(incidents_frame, text="Resolution Status:", font=("Arial", 12, "bold"))
    resolution_status.grid(row=3, column=0, pady=10, padx=10)
    resolution_status_combobox = ttk.Combobox(incidents_frame, values=status, state="readonly")
    resolution_status_combobox.grid(row=3, column=1)

    incident_status = tk.Label(incidents_window, text="", font=("Arial", 12, "bold"))
    incident_status.pack(pady=20)

    def add_incident():
        id = shipment_id_combobox.get()
        type = incident_type_combobox.get()
        description = incident_description_entry.get()
        resolution_status = resolution_status_combobox.get()

        if not id or not type or not description or not resolution_status:
            incident_status.config(text="Shipment ID, Incident Type, Description and Resolution Status not defined", fg="red")
        else:
            shipment_id = int(id.split()[0])
            conn = sqlite3.connect("northshore.db")
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO incidents(shipment_id, incident_type, description, resolution_status) VALUES (?, ?, ?, ?)", (shipment_id, type, description, resolution_status))
            conn.commit()
            conn.close()
            incident_status.config(text="Incident added successfully", fg="green")
            shipment_id_combobox.set("")
            incident_type_combobox.set("")
            incident_description_entry.delete(0, tk.END)
            resolution_status_combobox.set("")

    def view_incidents():
        conn = sqlite3.connect("northshore.db")
        cur = conn.cursor()
        incident_text.delete("1.0", tk.END)
        cur.execute("SELECT * FROM incidents")
        incidents = cur.fetchall()
        conn.close()
        for incident in incidents:
            incident_text.insert(tk.END, f"\n\nIncident ID: {incident[0]}\nShipment ID: {incident[1]}\nIncident Type: {incident[2]}\nDescription: {incident[3]}\nReported at: {incident[4]}\nResolution Status: {incident[5]}\n")

    add_incident_button = tk.Button(incidents_window, text="Add Incident", width=20, height=2, command=add_incident)
    add_incident_button.pack(pady=20)

    view_incidents_button = tk.Button(incidents_window, text="View Incidents", width=20, height=2, command=view_incidents)
    view_incidents_button.pack(pady=20)

    incident_label = tk.Label(incidents_window, text="Incidents:", font=("Arial", 12, "bold"))
    incident_label.pack(pady=20)
    incident_text = tk.Text(incidents_window)
    incident_text.pack(pady=20)

def open_audit_log_window():
    audit_log_window = tk.Toplevel(root)
    audit_log_window.title("Audit Log")
    audit_log_window.geometry("900x600")

    audit_title = tk.Label(audit_log_window, text="Audit Log", font=("Arial", 18, "bold"))
    audit_title.pack(pady=20)
    audit_text = tk.Text(audit_log_window)
    audit_text.pack(pady=20)

    conn = sqlite3.connect('northshore.db')
    cur = conn.cursor()
    cur.execute("SELECT action, table_name, record_id, action_time FROM audit_log ORDER BY action_time DESC")
    logs = cur.fetchall()
    conn.close()
    for log in logs:
        audit_text.insert(tk.END, f"\n\nAction: {log[0]}\nTable: {log[1]}\nRecordID: {log[2]}\nTime: {log[3]}\n{'-'*40}\n\n")

def open_warehouse_activity_window():
    warehouse_activity_window = tk.Toplevel(root)
    warehouse_activity_window.title("Warehouse Activity")
    warehouse_activity_window.geometry("900x600")

    warehouse_activity_title = tk.Label(warehouse_activity_window, text="Warehouse Activity Management", font=("Arial", 18, "bold"))
    warehouse_activity_title.pack(pady=20)
    warehouse_activity_frame = tk.Frame(warehouse_activity_window)
    warehouse_activity_frame.pack(pady=20)

    conn = sqlite3.connect('northshore.db')
    cur = conn.cursor()
    cur.execute("SELECT warehouse_id, name FROM warehouses")
    activity = cur.fetchall()
    cur.execute("SELECT item_id, item_name FROM inventory_items")
    items = cur.fetchall()
    conn.close()
    warehouses = []
    for activities in activity:
        warehouses.append(f"{activities[0]} - {activities[1]}")
    inventories = []
    for item in items:
        inventories.append(f"{item[0]} - {item[1]}")

    activity_type = ['Inbound', 'Outbound', 'Restock', 'Transfer']

    warehouse_id = tk.Label(warehouse_activity_frame, text="Warehouse ID:", font=("Arial", 12, "bold"))
    warehouse_id.grid(row=0, column=0, pady=10, padx=10)
    warehouse_combobox = ttk.Combobox(warehouse_activity_frame, values=warehouses, state="readonly")
    warehouse_combobox.grid(row=0, column=1)

    item_activity = tk.Label(warehouse_activity_frame, text="Item ID:", font=("Arial", 12, "bold"))
    item_activity.grid(row=1, column=0, pady=10, padx=10)
    item_combobox = ttk.Combobox(warehouse_activity_frame, values=inventories, state="readonly")
    item_combobox.grid(row=1, column=1)

    warehouse_activity_type = tk.Label(warehouse_activity_frame, text="Activity Type:", font=("Arial", 12, "bold"))
    warehouse_activity_type.grid(row=2, column=0, pady=10, padx=10)
    warehouse_activity_combobox = ttk.Combobox(warehouse_activity_frame, values=activity_type, state="readonly")
    warehouse_activity_combobox.grid(row=2, column=1)

    warehouse_quantity = tk.Label(warehouse_activity_frame, text="Quantity:", font=("Arial", 12, "bold"))
    warehouse_quantity.grid(row=3, column=0, pady=10, padx=10)
    warehouse_quantity_entry = tk.Entry(warehouse_activity_frame)
    warehouse_quantity_entry.grid(row=3, column=1)

    warehouse_notes = tk.Label(warehouse_activity_frame, text="Notes:", font=("Arial", 12, "bold"))
    warehouse_notes.grid(row=4, column=0, pady=10, padx=10)
    warehouse_notes_entry = tk.Entry(warehouse_activity_frame)
    warehouse_notes_entry.grid(row=4, column=1)

    warehouse_activity_status = tk.Label(warehouse_activity_window, text="", font=("Arial", 12, "bold"))
    warehouse_activity_status.pack(pady=20)

    def add_activity():
        warehouse_id = warehouse_combobox.get()
        item_id = item_combobox.get()
        activity_type = warehouse_activity_combobox.get()
        quantity = warehouse_quantity_entry.get()
        notes = warehouse_notes_entry.get()

        if not warehouse_id or not item_id or not activity_type or not quantity or not notes:
            warehouse_activity_status.config(text="Warehouse ID, Item ID, Activity Type, Quantity or Notes not defined", fg="red")
        else:
            try:
                warehouse_id = int(warehouse_id.split(" - ")[0])
                item_id = int(item_id.split(" - ")[0])
                quantity = int(quantity)

                conn = sqlite3.connect('northshore.db')
                cur = conn.cursor()
                cur.execute("INSERT OR IGNORE INTO warehouse_activity(warehouse_id, item_id, activity_type, quantity, notes) VALUES(?,?,?,?,?)", (warehouse_id, item_id, activity_type, quantity, notes))
                conn.commit()
                conn.close()
                warehouse_activity_status.config(text="Warehouse Activity successfully added", fg="green")
                warehouse_combobox.set("")
                item_combobox.set("")
                warehouse_activity_combobox.set("")
                warehouse_quantity_entry.delete(0, tk.END)
                warehouse_notes_entry.delete(0, tk.END)
            except ValueError:
                warehouse_activity_status.config(text="Quantity must be a whole number", fg="red")

    def view_activity():
        conn = sqlite3.connect('northshore.db')
        cur = conn.cursor()
        warehouse_activity_text.delete("1.0", tk.END)
        cur.execute('''
        SELECT 
         wa.activity_id,
         w.name,
         i.item_name,
         wa.activity_type,
         wa.quantity,
         wa.activity_date,
         wa.notes
        FROM warehouse_activity wa
        JOIN warehouses w
         ON wa.warehouse_id = w.warehouse_id
        JOIN inventory_items i
         ON wa.item_id = i.item_id
        ''')
        activities = cur.fetchall()
        conn.close()
        for activity in activities:
            warehouse_activity_text.insert(tk.END, f"\n\nActivity ID: {activity[0]}\nWarehouse: {activity[1]}\nItem: {activity[2]}\n Activity Type: {activity[3]}\nQuantity: {activity[4]}\nActivity Date: {activity[5]}\nNotes: {activity[6]}\n")

    add_activity_button = tk.Button(warehouse_activity_window, text="Add Activity", width=20, height=2, command=add_activity)
    add_activity_button.pack(pady=20)

    view_activity_button = tk.Button(warehouse_activity_window, text="View Activity", width=20, height=2, command=view_activity)
    view_activity_button.pack(pady=20)

    warehouse_activity_label = tk.Label(warehouse_activity_window, text="Warehouse Activity:", font=("Arial", 12, "bold"))
    warehouse_activity_label.pack(pady=20)
    warehouse_activity_text = tk.Text(warehouse_activity_window)
    warehouse_activity_text.pack(pady=20)


button_frame = tk.Frame(root)
button_frame.pack(pady=20)

users_button = tk.Button(button_frame, text="Users", width=20, height=2, command=open_users_window)
users_button.grid(row=0, column=0, padx=10, pady=10)

customers_button = tk.Button(button_frame, text="Customers", width=20, height=2, command=open_customers_window)
customers_button.grid(row=0, column=1, padx=10, pady=10)

warehouses_button = tk.Button(button_frame, text="Warehouses", width=20, height=2, command=open_warehouses_window)
warehouses_button.grid(row=1, column=0, padx=10, pady=10)

shipments_button = tk.Button(button_frame, text="Shipments", width=20, height=2, command=open_shipments_window)
shipments_button.grid(row=1, column=1, padx=10, pady=10)

warehouse_inventory_button = tk.Button(button_frame, text="Warehouse Inventory", width=20, height=2, command=open_warehouse_inventory_window)
warehouse_inventory_button.grid(row=2, column=0, padx=10, pady=10)

drivers_button = tk.Button(button_frame, text="Drivers", width=20, height=2, command=open_drivers_window)
drivers_button.grid(row=2, column=1, padx=10, pady=10)

vehicles_button = tk.Button(button_frame, text="Vehicles", width=20, height=2, command=open_vehicles_window)
vehicles_button.grid(row=3, column=0, padx=10, pady=10)

inventory_button = tk.Button(button_frame, text="Inventory", width=20, height=2, command=open_inventory_window)
inventory_button.grid(row=3, column=1, padx=10, pady=10)

reports_button = tk.Button(button_frame, text="Reports", width=20, height=2, command=open_reports_window)
reports_button.grid(row=4, column=0, padx=10, pady=10)

incidents_button = tk.Button(button_frame, text="Incidents", width=20, height=2, command=open_incidents_window)
incidents_button.grid(row=4, column=1, padx=10, pady=10)

warehouse_activity_button = tk.Button(button_frame, text="Warehouse Activity", width=20, height=2, command=open_warehouse_activity_window)
warehouse_activity_button.grid(row=5, column=0, padx=10, pady=10)

audit_button = tk.Button(button_frame, text="Audit Log", width=20, height=2, command=open_audit_log_window)
audit_button.grid(row=5, column=1, padx=10, pady=10)

logout_button = tk.Button(root, text="Logout", width=15, height=2, command=logout)
logout_button.pack(pady=20)

users_button.config(state="disabled")
customers_button.config(state="disabled")
shipments_button.config(state="disabled")
warehouse_inventory_button.config(state="disabled")
drivers_button.config(state="disabled")
vehicles_button.config(state="disabled")
inventory_button.config(state="disabled")
reports_button.config(state="disabled")
audit_button.config(state="disabled")

open_login_window()

root.mainloop()


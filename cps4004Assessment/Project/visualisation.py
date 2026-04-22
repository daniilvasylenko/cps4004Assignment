import tkinter as tk
from tkinter import ttk
import sqlite3

root = tk.Tk()
root.title("Northshore Logistics System")
root.geometry("900x600")
root.minsize(700,500)
title_label = tk.Label(root, text="Northshore Logistics Management System", font=("Arial", 18, "bold"))
title_label.pack(pady=20)

def open_customers_window():
    customers_window = tk.Toplevel(root)
    customers_window.title("Customers")
    customers_window.geometry("700x500")

    customers_title = tk.Label(customers_window, text="Customer Management", font=("Arial", 16, "bold"))
    customers_title.pack(pady=20)
    customers_frame = tk.Frame(customers_window)
    customers_frame.pack(pady=20)

    name = tk.Label(customers_frame, text="Name:", font=("Arial", 12, "bold"))
    name.grid(row=0, column=0, pady=10)
    name_entry = tk.Entry(customers_frame)
    name_entry.grid(row=0, column=1)

    phone = tk.Label(customers_frame, text="Phone:", font=("Arial", 12, "bold"))
    phone.grid(row=1, column=0, pady=10)
    phone_entry = tk.Entry(customers_frame)
    phone_entry.grid(row=1, column=1)

    email = tk.Label(customers_frame, text="Email:", font=("Arial", 12, "bold"))
    email.grid(row=2, column=0, pady=10)
    email_entry = tk.Entry(customers_frame)
    email_entry.grid(row=2, column=1)

    address = tk.Label(customers_frame, text="Address:", font=("Arial", 12, "bold"))
    address.grid(row=3, column=0, pady=10)
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
    sender_combobox = ttk.Combobox(shipments_frame, values=customers_data)
    sender_combobox.grid(row=1, column=1, pady=10, padx=10)

    receiver_title = tk.Label(shipments_frame, text="Receiver:", font=("Arial", 12, "bold"))
    receiver_title.grid(row=2, column=0, pady=10, padx=10)
    receiver_combobox = ttk.Combobox(shipments_frame, values=customers_data)
    receiver_combobox.grid(row=2, column=1, pady=10, padx=10)


    item_description = tk.Label(shipments_frame, text="Item description:", font=("Arial", 12, "bold"))
    item_description.grid(row=3, column=0, pady=10)
    item_description_entry = tk.Entry(shipments_frame)
    item_description_entry.grid(row=3, column=1)

    status = tk.Label(shipments_frame, text="Delivery status:", font=("Arial", 12, "bold"))
    status.grid(row=4, column=0, pady=10, padx=10)
    status_combobox = ttk.Combobox(shipments_frame, values=delivery_statuses)
    status_combobox.grid(row=4, column=1, pady=10, padx=10)

    payment = tk.Label(shipments_frame, text="Payment status:", font=("Arial", 12, "bold"))
    payment.grid(row=5, column=0, pady=10, padx=10)
    payment_combobox = ttk.Combobox(shipments_frame, values=payment_statuses)
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
            sender_name, 
            receiver_name, 
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
            shipments_text.insert(tk.END, f"\n\n Order number: {shipment[0]}\n Sender: {shipment[1]}\n Receiver: {shipment[2]}\n Description: {shipment[3]}\n Delivery status: {shipment[4]}\n Payment status: {shipment[5]}\n\n")


    add_shipment_button = tk.Button(shipments_window, text="Add Shipment", width=20, height=2, command=add_shipment)
    add_shipment_button.pack(pady=10)

    view_shipments_button = tk.Button(shipments_window, text="View Shipments", width=20, height=2, command=view_shipments)
    view_shipments_button.pack(pady=10)

    shipments_label = tk.Label(shipments_window, text="Shipments:", font=("Arial", 12, "bold"))
    shipments_label.pack(pady=20)
    shipments_text = tk.Text(shipments_window)
    shipments_text.pack(pady=20)

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
    shift_assignment_combobox = ttk.Combobox(drivers_frame, values=assignment)
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
            drivers_text.insert(tk.END, f"\n\n Driver ID: {driver[0]}\n Driver Name: {driver[1]}\n Driver Phone: {driver[2]}\n Licence Number: {driver[3]}\n Shift Assignment: {driver[4]}\n")

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
    availability_status_combobox = ttk.Combobox(vehicles_frame, values=availability_status)
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
            vehicles_text.insert(tk.END, f"\n\n Vehicle ID: {vehicle[0]}\n Registration Number: {vehicle[1]}\n Capacity: {vehicle[2]}\n Maintenance Date: {vehicle[3]}\n Availability Status: {vehicle[4]}\n")



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
            inventory_text.insert(tk.END, f"\n\n Item ID: {item[0]}\n Item Name: {item[1]}\n Description: {item[2]}\n Reorder Level: {item[3]}\n")

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
            report_text.insert(tk.END, f"Item name: {item[0]}\n\n Description: {item[1]}\n\n Reorder level: {item[2]}\n\n")


    shipment_report_button = tk.Button(reports_frame, text="Shipment Report", width=20, height=2, command=shipment_report)
    shipment_report_button.grid(row=0,column=0, pady=10, padx=10)

    drivers_report_button = tk.Button(reports_frame, text="Drivers Report", width=20, height=2, command=drivers_report)
    drivers_report_button.grid(row=0, column=1, pady=10, padx=10)

    vehicles_report_button = tk.Button(reports_frame, text="Vehicles Report", width=20, height=2, command=vehicles_report)
    vehicles_report_button.grid(row=1, column=0, pady=10, padx=10)

    inventory_report_button = tk.Button(reports_frame, text="Inventory Report", width=20, height=2, command=inventory_report)
    inventory_report_button.grid(row=1, column=1, pady=10, padx=10)






button_frame = tk.Frame(root)
button_frame.pack(pady=20)

customers_button = tk.Button(button_frame, text="Customers", width=20, height=2, command=open_customers_window)
customers_button.grid(row=0, column=0, padx=10, pady=10)

shipments_button = tk.Button(button_frame, text="Shipments", width=20, height=2, command=open_shipments_window)
shipments_button.grid(row=0, column=1, padx=10, pady=10)

drivers_button = tk.Button(button_frame, text="Drivers", width=20, height=2, command=open_drivers_window)
drivers_button.grid(row=1, column=0, padx=10, pady=10)

vehicles_button = tk.Button(button_frame, text="Vehicles", width=20, height=2, command=open_vehicles_window)
vehicles_button.grid(row=1, column=1, padx=10, pady=10)

inventory_button = tk.Button(button_frame, text="Inventory", width=20, height=2, command=open_inventory_window)
inventory_button.grid(row=2, column=0, padx=10, pady=10)

reports_button = tk.Button(button_frame, text="Reports", width=20, height=2, command=open_reports_window)
reports_button.grid(row=2, column=1, padx=10, pady=10)



root.mainloop()


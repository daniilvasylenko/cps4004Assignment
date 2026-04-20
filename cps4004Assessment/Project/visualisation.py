import tkinter as tk
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
    name = tk.Label(customers_frame, text="Name:", font=("Arial", 16, "bold"))
    name.grid(row=0, column=0, pady=10)
    name_entry = tk.Entry(customers_frame)
    name_entry.grid(row=0, column=1)
    phone = tk.Label(customers_frame, text="Phone:", font=("Arial", 16, "bold"))
    phone.grid(row=1, column=0, pady=10)
    phone_entry = tk.Entry(customers_frame)
    phone_entry.grid(row=1, column=1)
    email = tk.Label(customers_frame, text="Email:", font=("Arial", 16, "bold"))
    email.grid(row=2, column=0, pady=10)
    email_entry = tk.Entry(customers_frame)
    email_entry.grid(row=2, column=1)
    address = tk.Label(customers_frame, text="Address:", font=("Arial", 16, "bold"))
    address.grid(row=3, column=0, pady=10)
    address_entry = tk.Entry(customers_frame)
    address_entry.grid(row=3, column=1)

    def add_customer():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        if not name or not phone or not email or not address:
            print("Name, Phone, Email or Address not defined")
        else:
            conn = sqlite3.connect("northshore.db")
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO customers(name, phone, email, address) VALUES(?,?,?,?)",(name, phone, email, address))
            conn.commit()
            conn.close()
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)


    add_customer_button = tk.Button(customers_window, text="Add Customer", command=add_customer)
    add_customer_button.pack(pady=10)




button_frame = tk.Frame(root)
button_frame.pack(pady=20)

customers_button = tk.Button(button_frame, text="Customers", width=20, height=2, command=open_customers_window)
customers_button.grid(row=0, column=0, padx=10, pady=10)

shipments_button = tk.Button(button_frame, text="Shipments", width=20, height=2)
shipments_button.grid(row=0, column=1, padx=10, pady=10)

drivers_button = tk.Button(button_frame, text="Drivers", width=20, height=2)
drivers_button.grid(row=1, column=0, padx=10, pady=10)

vehicles_button = tk.Button(button_frame, text="Vehicles", width=20, height=2)
vehicles_button.grid(row=1, column=1, padx=10, pady=10)

inventory_button = tk.Button(button_frame, text="Inventory", width=20, height=2)
inventory_button.grid(row=2, column=0, padx=10, pady=10)

reports_button = tk.Button(button_frame, text="Reports", width=20, height=2)
reports_button.grid(row=2, column=1, padx=10, pady=10)



root.mainloop()


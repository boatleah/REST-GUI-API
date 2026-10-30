# app.py

#2. create the main window
import tkinter as tk
from tkinter import ttk, messagebox
import json
import urllib.request   # part of stdlib; no external libs needed

API_URL = "http://localhost:5000/submit"

root = tk.Tk()
root.title("Purchase Form")

# 3. adding the form elements(control-widgets)
# ---------- FORM VARIABLES ----------
product_id_var = tk.StringVar()
description_var = tk.StringVar()
price_var = tk.StringVar()
name_var = tk.StringVar()
email_var = tk.StringVar()
online = tk.BooleanVar()

# ---------- LAYOUT ----------
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Product ID
ttk.Label(frame, text="Product ID:").grid(column=0, row=0, sticky=tk.W)
product_id_entry = ttk.Entry(frame, width=30, textvariable=product_id_var)
product_id_entry.grid(column=1, row=0)

# Description
ttk.Label(frame, text="Description:").grid(column=0, row=1, sticky=tk.W)
description_entry = ttk.Entry(frame, width=30, textvariable=description_var)
description_entry.grid(column=1, row=1)

# Price
ttk.Label(frame, text="Price ($):").grid(column=0, row=2, sticky=tk.W)
price_entry = ttk.Entry(frame, width=30, textvariable=price_var)
price_entry.grid(column=1, row=2)

# Name
ttk.Label(frame, text="Name:").grid(column=0, row=3, sticky=tk.W)
name_entry = ttk.Entry(frame, width=30, textvariable=name_var)
name_entry.grid(column=1, row=3)

# Email
ttk.Label(frame, text="Email:").grid(column=0, row=4, sticky=tk.W)
email_entry = ttk.Entry(frame, width=30, textvariable=email_var)
email_entry.grid(column=1, row=4)

# Online checkbox
online_cb = ttk.Checkbutton(
    frame,
    text="Online purchase (uncheck for in-store)",
    variable=online
)
online_cb.grid(columnspan=2, row=5, sticky=tk.W)

# Submit button
submit_btn = ttk.Button(frame, text="Submit", command=lambda: submit_form())
submit_btn.grid(row=6, columnspan=2, pady=(10, 0))


#4, Local validation
def validate() -> bool:
    """Return True if all fields are valid; otherwise show an error."""
    if not product_id_var.get().strip():
        messagebox.showerror("Validation Error", "Product ID cannot be empty.")
        return False

    if not description_var.get().strip():
        messagebox.showerror("Validation Error", "Description cannot be empty.")
        return False

    try:
        price = float(price_var.get().strip())
    except ValueError:
        messagebox.showerror("Validation Error", "Price must be a number.")
        return False
    if price < 0 or price > 1000:
        messagebox.showerror("Validation Error", "Price must be between $0 and $1000.00.")
        return False

    if not name_var.get().strip():
        messagebox.showerror("Validation Error", "Name cannot be empty.")
        return False

    email = email_var.get().strip()
    if not email or "@" not in email:
        messagebox.showerror("Validation Error", "Enter a valid email address.")
        return False

    return True

#5. Convert Form Data to JSON
def collect_data() -> dict:
    """Return a dictionary that represents the form."""
    return {
        "product_id": product_id_var.get().strip(),
        "description": description_var.get().strip(),
        "price": float(price_var.get().strip()),
        "name": name_var.get().strip(),
        "email": email_var.get().strip(),
        "online": online.get()
    }

#6. Post the JSON to the API and validate
def submit_form() -> None:
    if not validate():
        return  # abort if validation failed

    payload = collect_data()
    json_payload = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=json_payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
        messagebox.showinfo("Success", f"Server replied: {result}")
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        messagebox.showerror("API Error", f"{e.code} – {error_msg}")
    except Exception as exc:
        messagebox.showerror("Connection Error", str(exc))

if __name__ == "__main__":
    root.mainloop()
"""
Add Product Page - Form to add new products
"""

import tkinter as tk
from tkinter import messagebox
import pandas as pd
from config.styles import *
from ui.widgets import create_page_header, create_form_field


def show_add_product(content_frame, agent, fonts):
    """Display add product page"""
    # Clear content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Page header
    create_page_header(content_frame, "Add New Product", fonts)

    # Content
    content = tk.Frame(content_frame, bg=BG)
    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Form
    form = tk.Frame(content, bg=CARD_BG)
    form.pack(fill=tk.X)

    fields = {}
    items = [
        ("Product ID *", "id"),
        ("Product Name *", "name"),
        ("Initial Stock *", "stock"),
        ("Daily Demand *", "demand")
    ]

    for idx, (label, key) in enumerate(items):
        entry = create_form_field(form, label, key, idx, fonts)
        fields[key] = entry

    form.columnconfigure(1, weight=1)

    # Buttons
    buttons = tk.Frame(content, bg=BG)
    buttons.pack(fill=tk.X, pady=(20, 0))

    def add_product():
        try:
            pid = fields['id'].get().strip()
            name = fields['name'].get().strip()
            stock = int(fields['stock'].get())
            demand = int(fields['demand'].get())

            if not pid or not name:
                messagebox.showerror("Error", "Fill all required fields!")
                return

            if not agent.df.empty and pid in agent.df["Product ID"].values:
                messagebox.showerror("Error", f"ID '{pid}' already exists!")
                return

            new_df = pd.DataFrame([{
                "Product ID": pid,
                "Product Name": name,
                "Stock": stock,
                "Daily Demand": demand
            }])
            agent.df = pd.concat([agent.df, new_df], ignore_index=True)
            agent._save_data()

            messagebox.showinfo("Success", f"✓ '{name}' added!")
            show_add_product(content_frame, agent, fonts)

        except ValueError:
            messagebox.showerror("Error", "Stock & Demand must be numbers!")

    tk.Button(
        buttons,
        text="✓ Add Product",
        font=fonts['header'],
        bg=SUCCESS,
        fg="white",
        width=20,
        command=add_product,
        cursor="hand2",
        border=0,
        activebackground="#059669"
    ).pack(side=tk.LEFT, ipady=8, ipadx=15)

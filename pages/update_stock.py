"""
Update Stock Page - Form to update product stock levels
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config.styles import *
from ui.widgets import create_page_header


def show_update_stock(content_frame, agent, fonts):
    """Display update stock page"""
    # Clear content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Page header
    create_page_header(content_frame, "Update Stock", fonts)

    # Content
    content = tk.Frame(content_frame, bg=BG)
    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    if agent.df.empty:
        tk.Label(
            content,
            text="No products! Add one first.",
            font=fonts['header'],
            bg=BG,
            fg=TEXT_LIGHT
        ).pack(pady=20)
        return

    # Form
    form = tk.Frame(content, bg=CARD_BG)
    form.pack(fill=tk.X)

    tk.Label(
        form,
        text="Select Product *",
        font=fonts['normal'],
        bg=CARD_BG,
        fg=TEXT
    ).grid(row=0, column=0, sticky="w", padx=20, pady=10)

    product_var = tk.StringVar()
    options = [
        f"{row['Product Name']} (ID: {row['Product ID']}) - Stock: {row['Stock']}"
        for _, row in agent.df.iterrows()
    ]
    combo = ttk.Combobox(
        form,
        textvariable=product_var,
        values=options,
        width=55,
        state="readonly",
        font=fonts['normal']
    )
    combo.grid(row=0, column=1, padx=20, pady=10, sticky="ew", ipady=6)

    tk.Label(
        form,
        text="New Stock *",
        font=fonts['normal'],
        bg=CARD_BG,
        fg=TEXT
    ).grid(row=1, column=0, sticky="w", padx=20, pady=10)

    stock_entry = tk.Entry(form, font=fonts['normal'], width=40, border=1, relief=tk.SOLID)
    stock_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew", ipady=6)

    form.columnconfigure(1, weight=1)

    # Buttons
    buttons = tk.Frame(content, bg=BG)
    buttons.pack(fill=tk.X, pady=(20, 0))

    def update():
        try:
            if not product_var.get():
                messagebox.showerror("Error", "Select a product!")
                return

            pid = product_var.get().split("(ID: ")[1].split(")")[0]
            new_stock = int(stock_entry.get())

            idx = agent.df[agent.df["Product ID"] == pid].index[0]
            agent.df.at[idx, "Stock"] = new_stock
            agent._save_data()

            messagebox.showinfo("Success", "✓ Stock updated!")
            show_update_stock(content_frame, agent, fonts)

        except ValueError:
            messagebox.showerror("Error", "Stock must be a number!")

    tk.Button(
        buttons,
        text="✓ Update Stock",
        font=fonts['header'],
        bg=SECONDARY,
        fg="white",
        width=20,
        command=update,
        cursor="hand2",
        border=0,
        activebackground="#1d4ed8"
    ).pack(side=tk.LEFT, ipady=8, ipadx=15)

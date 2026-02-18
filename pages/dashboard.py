"""
Dashboard Page - Overview with metrics and table
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config.styles import *
from ui.widgets import create_page_header, create_metric_card


def show_dashboard(content_frame, agent, fonts):
    """Display dashboard page"""
    # Clear content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Page header
    create_page_header(content_frame, "Dashboard Overview", fonts)

    # Content
    content = tk.Frame(content_frame, bg=BG)
    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    if agent.df.empty:
        tk.Label(
            content, 
            text="No products yet. Add a product to get started!", 
            font=fonts['header'], 
            bg=BG, 
            fg=TEXT_LIGHT
        ).pack(pady=20)
        return

    # Metrics row
    metrics = tk.Frame(content, bg=BG)
    metrics.pack(fill=tk.X, pady=(0, 30))

    total = len(agent.df)
    stock = int(agent.df["Stock"].sum())
    low = int((agent.df["Stock"] < agent.low_limit).sum())

    create_metric_card(metrics, "Total Products", total, SECONDARY, fonts)
    create_metric_card(metrics, "Total Stock", stock, SUCCESS, fonts)
    create_metric_card(metrics, "Low Stock Items", low, DANGER, fonts)

    # Table and buttons section
    table_section = tk.Frame(content, bg=BG)
    table_section.pack(fill=tk.BOTH, expand=True)

    tk.Label(
        table_section, 
        text="Inventory Table", 
        font=fonts['header'], 
        bg=BG, 
        fg=TEXT
    ).pack(anchor=tk.W, pady=(0, 10))

    # Table frame (takes available space)
    table_frame = tk.Frame(table_section, bg=CARD_BG, relief=tk.FLAT, bd=1)
    table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

    tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Stock", "Demand"), height=10, show="headings")
    for col in ("ID", "Name", "Stock", "Demand"):
        tree.heading(col, text=col)
        tree.column(col, width=200)

    for _, row in agent.df.iterrows():
        tree.insert("", tk.END, values=(row["Product ID"], row["Product Name"], row["Stock"], row["Daily Demand"]))

    tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Button section below table
    button_frame = tk.Frame(table_section, bg=BG)
    button_frame.pack(fill=tk.X, pady=(10, 0))

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Alert", "Please select a product to delete")
            return
        
        try:
            item = tree.item(selected[0])
            product_id = str(item['values'][0]).strip()
            product_name = str(item['values'][1]).strip()
            
            if messagebox.askyesno("Confirm Delete", f"Delete '{product_name}' (ID: {product_id})?"):
                if agent.delete_product(product_id):
                    messagebox.showinfo("Success", f"Product '{product_name}' deleted successfully!")
                    show_dashboard(content_frame, agent, fonts)
                else:
                    messagebox.showerror("Error", f"Failed to delete product. ID: {product_id}")
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {str(e)}")
    
    delete_btn = tk.Button(
        button_frame,
        text="🗑️  Delete Selected",
        command=delete_selected,
        bg=DANGER,
        fg="white",
        font=fonts['normal'],
        padx=20,
        pady=10,
        relief=tk.FLAT,
        cursor="hand2",
        activebackground="#dc2626"
    )
    delete_btn.pack(side=tk.LEFT, padx=5, pady=5)

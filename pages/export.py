"""
Export Page - Export data to CSV
"""

import tkinter as tk
from tkinter import messagebox
from config.styles import *
from ui.widgets import create_page_header


def show_export(content_frame, agent, fonts):
    """Display export page"""
    # Clear content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Page header
    create_page_header(content_frame, "Export Data", fonts)

    # Content
    content = tk.Frame(content_frame, bg=BG)
    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    if agent.df.empty:
        tk.Label(
            content,
            text="No data to export!",
            font=fonts['header'],
            bg=BG,
            fg=TEXT_LIGHT
        ).pack(pady=20)
        return

    # Info card
    card = tk.Frame(content, bg=CARD_BG)
    card.pack(fill=tk.X)

    tk.Label(
        card,
        text="Export Inventory Data",
        font=fonts['header'],
        bg=CARD_BG,
        fg=TEXT
    ).pack(anchor=tk.W, padx=20, pady=(20, 10))

    tk.Label(
        card,
        text="Export your inventory data to a CSV file for use in Excel, analysis tools, or backup purposes.",
        font=fonts['normal'],
        bg=CARD_BG,
        fg=TEXT_LIGHT,
        wraplength=500,
        justify=tk.LEFT
    ).pack(anchor=tk.W, padx=20, pady=(0, 20))

    # Buttons
    buttons = tk.Frame(content, bg=BG)
    buttons.pack(fill=tk.X, pady=(20, 0))

    def export():
        try:
            agent.export_data()
            messagebox.showinfo("Success", "✓ Data exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")

    tk.Button(
        buttons,
        text="💾 Export to CSV",
        font=fonts['normal'],
        bg=SUCCESS,
        fg="white",
        padx=20,
        pady=10,
        command=export,
        cursor="hand2",
        relief=tk.FLAT,
        activebackground="#059669"
    ).pack(side=tk.LEFT, padx=5, pady=5)

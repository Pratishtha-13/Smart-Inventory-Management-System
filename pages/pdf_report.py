"""
PDF Report Page - Generate PDF reports
"""

import tkinter as tk
from tkinter import messagebox
from config.styles import *
from ui.widgets import create_page_header


def show_pdf_report(content_frame, agent, fonts):
    """Display PDF report page"""
    # Clear content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Page header
    create_page_header(content_frame, "Generate PDF Report", fonts)

    # Content
    content = tk.Frame(content_frame, bg=BG)
    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    if agent.df.empty:
        tk.Label(
            content,
            text="No data to report!",
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
        text="About PDF Report",
        font=fonts['header'],
        bg=CARD_BG,
        fg=TEXT
    ).pack(anchor=tk.W, padx=20, pady=(20, 10))

    tk.Label(
        card,
        text="Generate a detailed PDF report of your current inventory status, including all products, stock levels, and demand forecasts.",
        font=fonts['normal'],
        bg=CARD_BG,
        fg=TEXT_LIGHT,
        wraplength=500,
        justify=tk.LEFT
    ).pack(anchor=tk.W, padx=20, pady=(0, 20))

    # Buttons
    buttons = tk.Frame(content, bg=BG)
    buttons.pack(fill=tk.X, pady=(20, 0))

    def generate():
        try:
            agent.generate_pdf_report()
            messagebox.showinfo("Success", "✓ PDF generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")

    tk.Button(
        buttons,
        text="📄 Generate Report",
        font=fonts['normal'],
        bg=SECONDARY,
        fg="white",
        padx=20,
        pady=10,
        command=generate,
        cursor="hand2",
        relief=tk.FLAT,
        activebackground="#2563eb"
    ).pack(side=tk.LEFT, padx=5, pady=5)

"""
Shared UI Components and Utilities
"""

import tkinter as tk
import pandas as pd
from config.styles import *


def create_metric_card(parent, title, value, color, fonts):
    """Create a metric card with colored bar"""
    card = tk.Frame(parent, bg=CARD_BG, relief=tk.FLAT, bd=1)
    card.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

    bar = tk.Frame(card, bg=color, width=5)
    bar.pack(side=tk.LEFT, fill=tk.Y)

    info = tk.Frame(card, bg=CARD_BG)
    info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)

    tk.Label(info, text=title, font=fonts['normal'], bg=CARD_BG, fg=TEXT_LIGHT).pack(anchor=tk.W)
    tk.Label(info, text=str(value), font=fonts['large'], bg=CARD_BG, fg=color).pack(anchor=tk.W, pady=(5, 0))


def create_page_header(parent, title, fonts):
    """Create page header"""
    header = tk.Frame(parent, bg=CARD_BG)
    header.pack(fill=tk.X, padx=20, pady=(20, 10))
    tk.Label(header, text=title, font=fonts['title'], bg=CARD_BG, fg=TEXT).pack(anchor=tk.W)


def create_form_field(parent, label, key, row, fonts, width=40):
    """Create a form input field with label"""
    tk.Label(parent, text=label, font=fonts['normal'], bg=CARD_BG, fg=TEXT).grid(
        row=row, column=0, sticky="w", padx=20, pady=10
    )
    entry = tk.Entry(parent, font=fonts['normal'], width=width, border=1, relief=tk.SOLID)
    entry.grid(row=row, column=1, padx=20, pady=10, sticky="ew", ipady=6)
    return entry


def clear_frame(frame):
    """Clear all widgets from frame"""
    for widget in frame.winfo_children():
        widget.destroy()

"""
Sidebar Component - Navigation Menu
Left side panel with menu items and logout button
"""

import tkinter as tk
from config.styles import *


class Sidebar:
    """Application sidebar with navigation"""
    
    def __init__(self, parent, menu_items, logout_callback, fonts):
        """Create sidebar with menu"""
        self.sidebar = tk.Frame(parent, bg=CARD_BG, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Menu title
        title = tk.Frame(self.sidebar, bg=CARD_BG, height=50)
        title.pack(fill=tk.X)
        title.pack_propagate(False)
        tk.Label(
            title, 
            text="Navigation", 
            font=fonts['header'], 
            bg=CARD_BG, 
            fg=TEXT
        ).pack(pady=15)

        # Menu items
        for label, callback in menu_items:
            btn = tk.Button(
                self.sidebar, 
                text=label, 
                font=fonts['normal'], 
                bg=CARD_BG, 
                fg=TEXT,
                anchor=tk.W, 
                command=callback, 
                cursor="hand2", 
                border=0,
                activebackground=BG, 
                activeforeground=PRIMARY
            )
            btn.pack(fill=tk.X, padx=10, pady=5, ipady=8)

        # Separator
        separator = tk.Frame(self.sidebar, bg=BORDER, height=1)
        separator.pack(fill=tk.X, padx=10, pady=10)

        # Logout button
        logout_btn = tk.Button(
            self.sidebar, 
            text="🚪 Logout", 
            font=fonts['normal'], 
            bg=DANGER, 
            fg="white",
            command=logout_callback, 
            cursor="hand2", 
            border=0, 
            activebackground="#dc2626"
        )
        logout_btn.pack(fill=tk.X, padx=10, pady=10, ipady=8)

"""
Header Component - Fixed at top
Always visible, shows title and user info
"""

import tkinter as tk
from config.styles import *


class Header:
    """Application header"""
    
    def __init__(self, parent, username, fonts):
        """Create fixed header"""
        self.header = tk.Frame(parent, bg=PRIMARY, height=70)
        self.header.pack(fill=tk.X)
        self.header.pack_propagate(False)

        content = tk.Frame(self.header, bg=PRIMARY)
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        tk.Label(
            content, 
            text="📦 Smart Inventory System", 
            font=fonts['title'], 
            bg=PRIMARY, 
            fg="white"
        ).pack(anchor=tk.W, side=tk.LEFT)

        tk.Label(
            content, 
            text=f"User: {username}", 
            font=fonts['normal'], 
            bg=PRIMARY, 
            fg="#e0e7ff"
        ).pack(anchor=tk.E, side=tk.RIGHT)

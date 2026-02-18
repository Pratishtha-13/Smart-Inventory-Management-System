"""
Smart Inventory Management System
Main Entry Point - Launch the application
"""

import tkinter as tk
from ui.app import InventoryUI


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryUI(root)
    root.mainloop()

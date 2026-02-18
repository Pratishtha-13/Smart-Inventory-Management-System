"""
Main Application UI Class
Orchestrates all UI components and page navigation
"""

import tkinter as tk
from tkinter import messagebox
from config.styles import get_fonts, PRIMARY, SECONDARY, BG, CARD_BG, TEXT, TEXT_LIGHT, DANGER
from ui.header import Header
from ui.sidebar import Sidebar
from ui.widgets import clear_frame
from pages.dashboard import show_dashboard
from pages.add_product import show_add_product
from pages.update_stock import show_update_stock
from pages.ai_insights import show_ai_recommendations
from pages.pdf_report import show_pdf_report
from pages.export import show_export
from final_smart_inventory_agent import InventoryAgent


class InventoryUI:
    """Main Application UI"""

    def __init__(self, root):
        self.root = root
        self.root.title("Smart Inventory Management System")
        self.root.geometry("1400x750")
        self.root.config(bg="white")

        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.agent = None
        self.content_frame = None
        self.fonts = get_fonts()

        # Show login
        self._show_login()

    # ==================== LOGIN ====================
    def _show_login(self):
        """Show login screen"""
        clear_frame(self.root)

        main_frame = tk.Frame(self.root, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel with branding
        left = tk.Frame(main_frame, bg=PRIMARY)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(left, text="📦", font=self.fonts['branding'], bg=PRIMARY, fg="white").pack(pady=(60, 20))
        tk.Label(left, text="Smart Inventory", font=self.fonts['login_title'], bg=PRIMARY, fg="white").pack()
        tk.Label(left, text="Management System", font=self.fonts['normal'], bg=PRIMARY, fg="#e0e7ff").pack(pady=(0, 200))

        # Right panel with login form
        right = tk.Frame(main_frame, bg=BG)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        card = tk.Frame(right, bg=CARD_BG)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=380, height=420)

        tk.Label(card, text="Welcome Back", font=self.fonts['login_title'], bg=CARD_BG, fg=TEXT).pack(pady=(30, 10))
        tk.Label(card, text="Sign in to your account", font=self.fonts['small'], bg=CARD_BG, fg=TEXT_LIGHT).pack(pady=(0, 30))

        tk.Label(card, text="Username", font=self.fonts['normal'], bg=CARD_BG, fg=TEXT).pack(anchor=tk.W, padx=30, pady=(0, 5))
        user_entry = tk.Entry(card, font=self.fonts['normal'], width=35, border=1, relief=tk.SOLID)
        user_entry.pack(padx=30, pady=(0, 20), ipady=8)
        user_entry.insert(0, "admin")

        tk.Label(card, text="Password", font=self.fonts['normal'], bg=CARD_BG, fg=TEXT).pack(anchor=tk.W, padx=30, pady=(0, 5))
        pwd_entry = tk.Entry(card, font=self.fonts['normal'], width=35, show="•", border=1, relief=tk.SOLID)
        pwd_entry.pack(padx=30, pady=(0, 30), ipady=8)
        pwd_entry.insert(0, "admin123")

        def handle_login():
            if user_entry.get() == "admin" and pwd_entry.get() == "admin123":
                self.agent = InventoryAgent(file_path="inventory.csv", low_limit=10)
                self.agent.user = "admin"
                self._create_main_layout()
            else:
                messagebox.showerror("Error", "Invalid credentials!")

        tk.Button(
            card,
            text="Sign In",
            font=self.fonts['header'],
            bg=SECONDARY,
            fg="white",
            width=32,
            command=handle_login,
            cursor="hand2",
            border=0,
            activebackground="#2563eb"
        ).pack(padx=30, ipady=8)

        tk.Label(card, text="Demo: admin / admin123", bg=CARD_BG, fg="#9ca3af", font=self.fonts['small']).pack(pady=20)

    # ==================== MAIN LAYOUT ====================
    def _create_main_layout(self):
        """Create main layout: Header + Sidebar + Content"""
        clear_frame(self.root)

        main = tk.Frame(self.root, bg="white")
        main.pack(fill=tk.BOTH, expand=True)

        # Fixed Header
        Header(main, self.agent.user, self.fonts)

        # Body: Sidebar + Content
        body = tk.Frame(main, bg=BG)
        body.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        menu_items = [
            ("📊 Dashboard", lambda: show_dashboard(self.content_frame, self.agent, self.fonts)),
            ("➕ Add Product", lambda: show_add_product(self.content_frame, self.agent, self.fonts)),
            ("🔄 Update Stock", lambda: show_update_stock(self.content_frame, self.agent, self.fonts)),
            ("🤖 AI Insights", lambda: show_ai_recommendations(self.content_frame, self.agent, self.fonts)),
            ("📄 PDF Report", lambda: show_pdf_report(self.content_frame, self.agent, self.fonts)),
            ("💾 Export CSV", lambda: show_export(self.content_frame, self.agent, self.fonts)),
        ]
        Sidebar(body, menu_items, self._show_login, self.fonts)

        # Content Area
        self.content_frame = tk.Frame(body, bg=BG)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Show dashboard by default
        show_dashboard(self.content_frame, self.agent, self.fonts)

"""
Final Smart Inventory Management Agent
A pure Python CLI-based inventory management system with AI decision-making
"""

import pandas as pd
import os
from datetime import datetime
from typing import Optional, List
import getpass

# Try to import reportlab for PDF generation
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class InventoryAgent:
    """AI-powered inventory management system"""

    def __init__(self, file_path: str = "inventory.csv", low_limit: int = 10):
        self.file_path = file_path
        self.low_limit = low_limit
        self.df = self._load_data()
        self.user = None
        self.logged_in = False

    def _load_data(self) -> pd.DataFrame:
        """Load inventory from CSV or create empty file"""
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=["Product ID", "Product Name", "Stock", "Daily Demand"])
            df.to_csv(self.file_path, index=False)
            return df
        return pd.read_csv(self.file_path)

    def _save_data(self):
        """Save inventory to CSV"""
        self.df.to_csv(self.file_path, index=False)

    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)

    def print_divider(self):
        """Print divider line"""
        print("-" * 60)

    # ==================== AUTHENTICATION ====================
    def login(self) -> bool:
        """User login function"""
        self.print_header("🔐 LOGIN")
        print("\nDefault credentials: username='admin', password='admin123'")

        for attempt in range(3):
            username = input("\nUsername: ").strip()
            password = getpass.getpass("Password: ")

            if username == "admin" and password == "admin123":
                self.user = username
                self.logged_in = True
                print(f"\n✅ Welcome, {username}!")
                return True
            else:
                remaining = 2 - attempt
                if remaining > 0:
                    print(f"❌ Invalid credentials. {remaining} attempt(s) remaining.")
                else:
                    print("❌ Login failed. Too many attempts.")
                    return False
        return False

    # ==================== DASHBOARD ====================
    def show_dashboard(self):
        """Display inventory dashboard"""
        self.print_header("📊 DASHBOARD")

        if self.df.empty:
            print("\nNo products in inventory. Add a product to get started!")
            return

        total_products = len(self.df)
        total_stock = int(self.df["Stock"].sum())
        low_stock_items = int((self.df["Stock"] < self.low_limit).sum())

        print(f"\n📦 Total Products: {total_products}")
        print(f"📚 Total Stock: {total_stock} units")
        print(f"⚠️  Low Stock Items: {low_stock_items}")

        self.print_divider()
        print("\n📋 INVENTORY TABLE:")
        print(self.df.to_string(index=False))

    # ==================== ADD PRODUCT ====================
    def add_product(self):
        """Add new product to inventory"""
        self.print_header("➕ ADD PRODUCT")

        product_id = input("\nProduct ID: ").strip()
        if not product_id:
            print("❌ Product ID cannot be empty.")
            return

        product_name = input("Product Name: ").strip()
        if not product_name:
            print("❌ Product Name cannot be empty.")
            return

        try:
            stock = int(input("Initial Stock: "))
            demand = int(input("Daily Demand: "))
        except ValueError:
            print("❌ Stock and Demand must be numbers.")
            return

        # Check for duplicate ID
        if not self.df.empty and product_id in self.df["Product ID"].values:
            print(f"❌ Product ID '{product_id}' already exists!")
            return

        new_product = pd.DataFrame([{
            "Product ID": product_id,
            "Product Name": product_name,
            "Stock": stock,
            "Daily Demand": demand
        }])

        self.df = pd.concat([self.df, new_product], ignore_index=True)
        self._save_data()
        print(f"\n✅ Product '{product_name}' added successfully!")

    # ==================== DELETE PRODUCT ====================
    def delete_product(self, product_id: str) -> bool:
        """Delete product by ID"""
        try:
            product_id = str(product_id).strip()
            if self.df.empty:
                return False
            
            # Check if product exists
            if product_id not in self.df["Product ID"].values:
                return False
            
            # Delete the product
            self.df = self.df[self.df["Product ID"] != product_id].reset_index(drop=True)
            self._save_data()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False

    # ==================== UPDATE STOCK ====================
    def update_stock(self):
        """Update product stock"""
        self.print_header("🔄 UPDATE STOCK")

        if self.df.empty:
            print("\n❌ No products in inventory. Please add a product first.")
            return

        print("\nAvailable Products:")
        for idx, (_, row) in enumerate(self.df.iterrows(), 1):
            print(f"  {idx}. {row['Product Name']} (ID: {row['Product ID']}) - Current Stock: {row['Stock']}")

        try:
            choice = int(input("\nSelect product number: ")) - 1
            if choice < 0 or choice >= len(self.df):
                print("❌ Invalid selection.")
                return

            row = self.df.iloc[choice]
            print(f"\n📦 Updating '{row['Product Name']}'")
            print(f"   Current Stock: {row['Stock']}")

            new_stock = int(input("New Stock: "))
            self.df.at[choice, "Stock"] = new_stock
            self._save_data()
            print(f"\n✅ Stock updated successfully!")

        except ValueError:
            print("❌ Invalid input.")

    # ==================== AI RECOMMENDATIONS ====================
    def get_ai_recommendations(self):
        """Get AI-powered inventory recommendations"""
        self.print_header("🤖 AI AGENT RECOMMENDATIONS")

        if self.df.empty:
            print("\nNo products to analyze. Add products first!")
            return

        print("\n" + "=" * 60)
        for idx, (_, row) in enumerate(self.df.iterrows(), 1):
            product_name = row["Product Name"]
            stock = row["Stock"]
            demand = row["Daily Demand"]
            week_forecast = demand * 7

            # AI Decision Logic
            priority_score = (demand * 2) - stock

            if stock < self.low_limit:
                status = "🔴 HIGH RISK"
                recommendation = "URGENT: Reorder immediately!"
            elif priority_score > 0:
                status = "🟡 MEDIUM RISK"
                recommendation = "Monitor stock closely. Plan to reorder soon."
            else:
                status = "🟢 SAFE"
                recommendation = "Stock levels are healthy. Continue monitoring."

            print(f"\n{idx}. {product_name}")
            self.print_divider()
            print(f"   Current Stock: {stock} units")
            print(f"   Daily Demand: {demand} units")
            print(f"   7-Day Forecast: {week_forecast} units")
            print(f"   Priority Score: {priority_score}")
            print(f"   Status: {status}")
            print(f"   Recommendation: {recommendation}")

        print("\n" + "=" * 60)

    # ==================== PDF REPORT ====================
    def generate_pdf_report(self):
        """Generate PDF inventory report"""
        self.print_header("📄 GENERATE PDF REPORT")

        if not HAS_REPORTLAB:
            print("\n⚠️  reportlab is not installed.")
            print("Install it with: pip install reportlab")
            return

        if self.df.empty:
            print("\n❌ No products to report. Add products first!")
            return

        try:
            filename = f"inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf = canvas.Canvas(filename, pagesize=A4)

            # Header
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(50, 800, "INVENTORY MANAGEMENT REPORT")
            pdf.setFont("Helvetica", 10)
            pdf.drawString(50, 780, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Content
            y = 750
            pdf.setFont("Helvetica-Bold", 11)

            for _, row in self.df.iterrows():
                pdf.drawString(50, y, f"Product: {row['Product Name']} (ID: {row['Product ID']})")
                y -= 15
                pdf.setFont("Helvetica", 10)
                pdf.drawString(60, y, f"Stock: {row['Stock']} | Daily Demand: {row['Daily Demand']}")
                y -= 15
                y -= 5

                if y < 50:
                    pdf.showPage()
                    y = 800

            pdf.save()
            print(f"\n✅ Report generated: {filename}")

        except Exception as e:
            print(f"\n❌ Error generating PDF: {e}")

    # ==================== EXPORT DATA ====================
    def export_data(self):
        """Export inventory to CSV"""
        self.print_header("💾 EXPORT DATA")

        if self.df.empty:
            print("\n❌ No data to export.")
            return

        filename = f"inventory_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.df.to_csv(filename, index=False)
        print(f"\n✅ Data exported to: {filename}")

    # ==================== MAIN MENU ====================
    def show_menu(self):
        """Display main menu"""
        print("\n" + "=" * 60)
        print("  SMART INVENTORY MANAGEMENT SYSTEM")
        print("=" * 60)
        print(f"  Logged in as: {self.user}")
        print("=" * 60)
        print("\n1. 📊 Dashboard")
        print("2. ➕ Add Product")
        print("3. 🔄 Update Stock")
        print("4. 🤖 AI Recommendations")
        print("5. 📄 Generate PDF Report")
        print("6. 💾 Export Data")
        print("7. 🚪 Logout")
        print("8. ❌ Exit")
        print("-" * 60)

    def run(self):
        """Main application loop"""
        self.clear_screen()
        print("\n🎯 SMART INVENTORY MANAGEMENT AGENT")
        print("AI-Driven Warehouse Decision System\n")

        # Login
        if not self.login():
            print("\n❌ Authentication failed. Exiting...")
            return

        # Main loop
        while True:
            self.clear_screen()
            self.show_menu()

            choice = input("\nEnter your choice (1-8): ").strip()

            if choice == "1":
                self.show_dashboard()
            elif choice == "2":
                self.add_product()
            elif choice == "3":
                self.update_stock()
            elif choice == "4":
                self.get_ai_recommendations()
            elif choice == "5":
                self.generate_pdf_report()
            elif choice == "6":
                self.export_data()
            elif choice == "7":
                print("\n👋 Logging out...")
                self.logged_in = False
                if self.login():
                    continue
                else:
                    break
            elif choice == "8":
                print("\n✅ Thank you for using Smart Inventory Agent. Goodbye!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")

            input("\nPress Enter to continue...")


# ==================== MAIN ====================
if __name__ == "__main__":
    agent = InventoryAgent(file_path="inventory.csv", low_limit=10)
    agent.run()

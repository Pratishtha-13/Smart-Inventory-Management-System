"""
Color Scheme and Fonts Configuration
Centralized styling for the entire application
"""

from tkinter import font

# ==================== COLORS ====================
PRIMARY = "#1e3a8a"           # Dark Blue - Main color
SECONDARY = "#3b82f6"         # Sky Blue - Accents
SUCCESS = "#10b981"           # Green - Success/Add
WARNING = "#f59e0b"           # Amber - Warning
DANGER = "#ef4444"            # Red - Danger/Delete
BG = "#f9fafb"                # Light Gray - Background
CARD_BG = "white"             # White - Cards
TEXT = "#1f2937"              # Dark Gray - Text
TEXT_LIGHT = "#6b7280"        # Medium Gray - Subtle text
BORDER = "#e5e7eb"            # Light Border

# ==================== FONTS ====================
def get_fonts():
    """Get all font objects"""
    return {
        'title': font.Font(family="Segoe UI", size=16, weight="bold"),
        'header': font.Font(family="Segoe UI", size=11, weight="bold"),
        'normal': font.Font(family="Segoe UI", size=10),
        'small': font.Font(family="Segoe UI", size=9),
        'large': font.Font(family="Segoe UI", size=20, weight="bold"),
        'branding': font.Font(family="Segoe UI", size=80),
        'login_title': font.Font(family="Segoe UI", size=16, weight="bold"),
    }

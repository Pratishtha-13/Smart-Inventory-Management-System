"""
AI Insights Page - AI recommendations and analysis
"""

import tkinter as tk
from tkinter import ttk
from config.styles import *
from ui.widgets import create_page_header


def show_ai_recommendations(content_frame, agent, fonts):
    """Display AI insights page"""
    # Clear content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Page header
    create_page_header(content_frame, "AI Insights & Recommendations", fonts)

    # Content
    content = tk.Frame(content_frame, bg=BG)
    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    if agent.df.empty:
        tk.Label(
            content,
            text="No products to analyze!",
            font=fonts['header'],
            bg=BG,
            fg=TEXT_LIGHT
        ).pack(pady=20)
        return

    # Scrollable area
    canvas_frame = tk.Frame(content, bg=BG)
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(canvas_frame, bg=BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=BG)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for _, row in agent.df.iterrows():
        _create_ai_card(scroll_frame, row, agent, fonts)

    canvas.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")


def _create_ai_card(parent, row, agent, fonts):
    """Create AI insight card"""
    stock = row["Stock"]
    demand = row["Daily Demand"]
    forecast = demand * 7
    score = (demand * 2) - stock

    if stock < agent.low_limit:
        status, color, rec = "🔴 HIGH RISK", DANGER, "URGENT: Reorder immediately!"
    elif score > 0:
        status, color, rec = "🟡 MEDIUM RISK", WARNING, "Monitor stock. Plan to reorder soon."
    else:
        status, color, rec = "🟢 SAFE", SUCCESS, "Stock is healthy."

    card = tk.Frame(parent, bg=CARD_BG, relief=tk.FLAT, bd=1)
    card.pack(fill=tk.X, pady=10)

    bar = tk.Frame(card, bg=color, height=4)
    bar.pack(fill=tk.X)

    info = tk.Frame(card, bg=CARD_BG)
    info.pack(fill=tk.X, padx=20, pady=(15, 10))

    tk.Label(
        info,
        text=row['Product Name'],
        font=fonts['header'],
        bg=CARD_BG,
        fg=TEXT,
        anchor=tk.W
    ).pack(side=tk.LEFT, fill=tk.X, expand=True)

    tk.Label(
        info,
        text=status,
        font=fonts['normal'],
        bg=CARD_BG,
        fg=color
    ).pack(side=tk.RIGHT)

    details_text = f"Stock: {stock} | Demand: {demand}/day | 7-Day: {forecast} | Score: {score}"
    tk.Label(
        card,
        text=details_text,
        font=fonts['normal'],
        bg=CARD_BG,
        fg=TEXT_LIGHT,
        anchor=tk.W
    ).pack(anchor="w", padx=20, pady=(0, 10))

    rec_frame = tk.Frame(card, bg="#f3f4f6")
    rec_frame.pack(fill=tk.X, padx=0)
    tk.Label(
        rec_frame,
        text=f"💡 {rec}",
        font=fonts['normal'],
        bg="#f3f4f6",
        fg=TEXT,
        anchor=tk.W
    ).pack(anchor="w", padx=20, pady=10)

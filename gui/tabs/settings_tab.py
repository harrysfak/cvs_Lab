"""
Settings Tab Module
Handles processing settings (date, time, product, filters)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random
import sys
import os
from datetime import datetime

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import config


class SettingsTab:
    """Tab για ρυθμίσεις επεξεργασίας"""

    def __init__(self, parent, app_reference):
        """
        Args:
            parent: Parent notebook
            app_reference: Reference to main app
        """
        self.app = app_reference
        self.frame = ttk.Frame(parent, padding="20")
        self._setup_ui()

    def _setup_ui(self):
        """Δημιουργία UI"""
        # Date
        date_frame = ttk.LabelFrame(self.frame, text="📅 Ημερομηνία", padding="15")
        date_frame.pack(fill=tk.X, pady=10)

        ttk.Label(date_frame, text="Ημερομηνία (DD-MM):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(date_frame, width=20)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(date_frame, text="📆 Από Πρωτόκολλο", command=self.set_analysis_day).grid(row=0, column=2)

        # Time
        time_frame = ttk.LabelFrame(self.frame, text="🕐 Ώρα", padding="15")
        time_frame.pack(fill=tk.X, pady=10)

        ttk.Label(time_frame, text="Ώρα (HH:MM):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.time_entry = ttk.Entry(time_frame, width=20)
        self.time_entry.insert(0, config.DEFAULT_TIME)
        self.time_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(
            time_frame,
            text="🕐 Random (10:00-12:00)",
            command=self.set_random_hour
        ).grid(row=0, column=2, padx=5)

        # Product
        product_frame = ttk.LabelFrame(self.frame, text="📦 Προϊόν", padding="15")
        product_frame.pack(fill=tk.X, pady=10)

        ttk.Label(product_frame, text="Όνομα:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.product_entry = ttk.Entry(product_frame, width=30)
        self.product_entry.insert(0, config.DEFAULT_PRODUCT)
        self.product_entry.grid(row=0, column=1, padx=10, pady=5)

        # Filter
        filter_frame = ttk.LabelFrame(self.frame, text="🔧 Φίλτρα", padding="15")
        filter_frame.pack(fill=tk.X, pady=10)

        self.drop_zero_var = tk.BooleanVar(value=getattr(config, 'DROP_ZERO_NUTRIENTS', True))
        ttk.Checkbutton(
            filter_frame,
            text="Αφαίρεση γραμμών με Fat=Protein=Lactose=0",
            variable=self.drop_zero_var
        ).pack(anchor=tk.W, pady=5)

    def set_analysis_day(self):
        """Set ημερομηνία από protocol"""
        if not self.app.csv_first_4 or len(self.app.csv_first_4) < 4:
            messagebox.showwarning("Προειδοποίηση", "Φορτώστε πρώτα αρχείο")
            return

        anal_day = f"{self.app.csv_first_4[0:2]}-{self.app.csv_first_4[2:4]}"
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, anal_day)
        self.app.logger.info(f"📅 Ημερομηνία: {anal_day}")

    def set_random_hour(self):
        """Random ώρα 10:00-12:00"""
        hour = random.randint(10, 11)
        minute = random.randint(0, 59)
        random_time = f"{hour:02d}:{minute:02d}"

        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, random_time)
        self.app.logger.info(f"🕐 Random ώρα: {random_time}")

    def get_date(self):
        """Returns date value"""
        return self.date_entry.get().strip()

    def get_time(self):
        """Returns time value"""
        return self.time_entry.get().strip()

    def get_product(self):
        """Returns product name"""
        return self.product_entry.get().strip()

    def get_drop_zero(self):
        """Returns drop_zero_nutrients setting"""
        return self.drop_zero_var.get()

    def get_frame(self):
        """Returns the frame"""
        return self.frame
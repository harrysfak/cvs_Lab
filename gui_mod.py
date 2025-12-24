"""
CSV Lab - GUI Application (Modular Architecture)
Windows Edition v1.3 - Complete Module Separation
"""
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import core modules

# Import modules

from gui.telemetry import UsageTelemetry
from gui.config_edit import ConfigEditor
from gui.stats_wind import UsageStatsWindow
from gui.set_wind import SettingsWindow
from gui.log import UILogger


# Import tab modules
from gui.tabs import LoadTab, SettingsTab, ProcessTab, ResultsTab

import config


class CSVLabGUI:
    """Κύρια κλάση GUI εφαρμογής (Modular)"""

    def __init__(self, root):
        self.root = root
        self.root.title("CSV Lab - Σύστημα Επεξεργασίας CSV")
        self.root.geometry("1000x750")

        # Center window
        self._center_window()

        # Core components
        self.telemetry = UsageTelemetry()
        self.telemetry.record_session_start()
        self.config_editor = ConfigEditor()

        # Data variables
        self.excel_df = None
        self.csv_first_4 = None
        self.dash_part = None
        self.processed_df = None
        self.processing_start_time = None

        # Setup UI
        self._setup_ui()

        # Initialize tabs (after UI setup)
        self._setup_tabs()

        # Initial log
        self.log("✅ CSV Lab εκκίνησε επιτυχώς!")
        self.log(f"📁 Φάκελος εργασίας: {config.BASE_PATH}")

    def _center_window(self):
        """Κεντράρει το παράθυρο"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _setup_ui(self):
        """Δημιουργία UI structure"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', padx=10, pady=15)
        header_frame.pack(fill=tk.X)

        # Title
        title_frame = tk.Frame(header_frame, bg='#2c3e50')
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            title_frame,
            text="🥛 CSV Lab - Σύστημα Επεξεργασίας CSV 🥛",
            font=("Segoe UI", 18, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(anchor=tk.W)

        tk.Label(
            title_frame,
            text="Windows Edition - v1.3 (Modular Architecture)",
            font=("Segoe UI", 9),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(anchor=tk.W)

        # Header buttons
        buttons_frame = tk.Frame(header_frame, bg='#2c3e50')
        buttons_frame.pack(side=tk.RIGHT)

        tk.Button(
            buttons_frame,
            text="⚙️ Ρυθμίσεις",
            command=self._open_settings,
            bg='#3498db',
            fg='white',
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=5,
            cursor='hand2',
            relief=tk.RAISED
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons_frame,
            text="📊 Στατιστικά",
            command=self._open_stats,
            bg='#27ae60',
            fg='white',
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=5,
            cursor='hand2',
            relief=tk.RAISED
        ).pack(side=tk.LEFT, padx=5)

        # Notebook
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 10])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ---- Log Tab (central) ----
        log_frame = ttk.Frame(self.notebook, padding="10")
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            state=tk.DISABLED,
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.notebook.add(log_frame, text="🧾 Logs")

        # Status bar
        status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_bar = tk.Label(
            status_frame,
            text="Έτοιμο",
            anchor=tk.W,
            bg='#34495e',
            fg='white',
            padx=10,
            font=("Segoe UI", 9)
        )
        self.status_bar.pack(fill=tk.X)

        "==========================="

        # ---- Central logger instance ----
        self.logger = UILogger(self.log_text, status_label=self.status_bar)



    def _setup_tabs(self):
        """Δημιουργία tabs από modules"""
        # Create tab instances (passing self as reference)
        self.load_tab = LoadTab(self.notebook, self)
        self.settings_tab = SettingsTab(self.notebook, self)
        self.process_tab = ProcessTab(self.notebook, self)
        self.results_tab = ResultsTab(self.notebook, self)

        # Add tabs to notebook
        self.notebook.add(self.load_tab.get_frame(), text="📂 1. Φόρτωση")
        self.notebook.add(self.settings_tab.get_frame(), text="⚙️ 2. Ρυθμίσεις")
        self.notebook.add(self.process_tab.get_frame(), text="⚡ 3. Επεξεργασία")
        self.notebook.add(self.results_tab.get_frame(), text="✅ 4. Αποτελέσματα")

    def _open_settings(self):
        """Άνοιγμα Settings Window"""
        SettingsWindow(self.root, self.config_editor)

    def _open_stats(self):
        """Άνοιγμα Usage Stats Window"""
        UsageStatsWindow(self.root, self.telemetry)

    def log(self, message):
        # backward-compatible shortcut
        self.logger.info(message)

    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)


def run_gui():
    """Εκτέλεση GUI"""
    root = tk.Tk()

    # Windows DPI awareness
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    app = CSVLabGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
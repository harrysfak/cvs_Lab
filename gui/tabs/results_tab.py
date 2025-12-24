"""
Results Tab Module
Displays processing results and provides output actions
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import config


class ResultsTab:
    """Tab για αποτελέσματα"""

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
        self.results_text = scrolledtext.ScrolledText(
            self.frame, height=20, state=tk.DISABLED, font=("Consolas", 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=10)

        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            button_frame,
            text="📁 Άνοιγμα Φακέλου",
            command=self.open_output_folder
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="📄 Άνοιγμα Αρχείου",
            command=self.open_final_file
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="🔄 Reset",
            command=self.reset
        ).pack(side=tk.LEFT, padx=5)

    def show_results(self, final_path):
        """Εμφάνιση αποτελεσμάτων"""
        results = f"""
✅ ΕΠΙΤΥΧΙΑ!

📄 Αρχείο: {final_path}
📊 Δείγματα: {len(self.app.processed_df)}
        """

        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)
        self.results_text.config(state=tk.DISABLED)

        # Switch to results tab
        self.app.notebook.select(3)

        messagebox.showinfo(
            "Επιτυχία",
            f"Ολοκληρώθηκε!\n\nΔείγματα: {len(self.app.processed_df)}"
        )

    def open_output_folder(self):
        import os
        import subprocess
        from tkinter import messagebox

        path = getattr(self.app, "last_output_path", None)

        if not path or not os.path.exists(path):
            messagebox.showwarning("Προειδοποίηση", "Δεν υπάρχει παραγόμενο αρχείο.")
            return

        folder = os.path.dirname(path)
        subprocess.Popen(f'explorer "{folder}"')


    def open_final_file(self):
        import os
        from tkinter import messagebox

        path = getattr(self.app, "last_output_path", None)

        if not path or not os.path.exists(path):
            messagebox.showwarning("Σφάλμα", "Δεν υπάρχει παραγόμενο αρχείο για άνοιγμα.")
            return

        os.startfile(path)  # Windows   

    def reset(self):
        """Reset"""
        # Reset main app data
        self.app.excel_df = None
        self.app.csv_first_4 = None
        self.app.dash_part = None
        self.app.processed_df = None

        # Reset tabs
        self.app.load_tab.reset()

        # Clear results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)

        # Switch to load tab
        self.app.notebook.select(0)
        self.app.logger.info("🔄 Reset εφαρμογής")

    def get_frame(self):
        """Returns the frame"""
        return self.frame
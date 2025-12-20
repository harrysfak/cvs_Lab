import tkinter as tk
from tkinter import ttk, scrolledtext


class UsageStatsWindow:
    """Παράθυρο για Usage Statistics"""

    def __init__(self, parent, telemetry):
        self.window = tk.Toplevel(parent)
        self.window.title("Στατιστικά Χρήσης")
        self.window.geometry("600x500")
        self.window.transient(parent)

        self.telemetry = telemetry

        self._setup_ui()
        self._center_window()

    def _center_window(self):
        """Κεντράρει το παράθυρο"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def _setup_ui(self):
        """Δημιουργία UI"""
        # Header
        header = tk.Frame(self.window, bg='#27ae60', padx=15, pady=10)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="📊 Στατιστικά Χρήσης",
            font=("Segoe UI", 14, "bold"),
            bg='#27ae60',
            fg='white'
        ).pack(anchor=tk.W)

        tk.Label(
            header,
            text="Usage & Maintenance Info",
            font=("Segoe UI", 9),
            bg='#27ae60',
            fg='white'
        ).pack(anchor=tk.W)

        # Stats display
        stats_frame = ttk.Frame(self.window, padding="20")
        stats_frame.pack(fill=tk.BOTH, expand=True)

        summary = self.telemetry.get_summary()

        stats_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    ΣΤΑΤΙΣΤΙΚΑ ΧΡΗΣΗΣ                             ║
╚══════════════════════════════════════════════════════════════════╝

📊 ΣΥΝΟΛΙΚΑ:
   • Συνολικά Αρχεία: {summary['total_files']}
   • Συνολικές Sessions: {summary['total_sessions']}

📅 ΠΕΡΙΟΔΟΣ:
   • Σήμερα: {summary['today_files']} αρχεία
   • Αυτή την Εβδομάδα: {summary['week_files']} αρχεία

🕐 ΧΡΟΝΙΚΑ:
   • Πρώτη Χρήση: {summary['first_used'][:10] if summary['first_used'] else 'N/A'}
   • Τελευταία Χρήση: {summary['last_used'][:10] if summary['last_used'] else 'N/A'}

⚠️ ERRORS:
   • Πρόσφατα Σφάλματα: {summary['recent_errors']}

╔══════════════════════════════════════════════════════════════════╗
ℹ️  Τα δεδομένα αποθηκεύονται τοπικά για maintenance purposes
╚══════════════════════════════════════════════════════════════════╝
        """

        text_widget = scrolledtext.ScrolledText(
            stats_frame,
            height=20,
            state=tk.DISABLED,
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        text_widget.pack(fill=tk.BOTH, expand=True)

        text_widget.config(state=tk.NORMAL)
        text_widget.insert(1.0, stats_text)
        text_widget.config(state=tk.DISABLED)

        # Button
        ttk.Button(
            stats_frame,
            text="❌ Κλείσιμο",
            command=self.window.destroy
        ).pack(pady=10)

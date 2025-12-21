"""
CSV Lab - GUI με Settings Window και Usage Telemetry
Windows Version - Simple Professional Enhancements
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, BooleanVar
import threading
import os
import sys
from datetime import datetime
import subprocess
import random

# Προσθήκη του parent directory στο path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules
from modules.data_loader import DataLoader
from modules.data_processor import process_data
from modules.time_handler import TimeHandler, MetadataGenerator
from modules.zero_manager import prepare_zero_data
from modules.output_generator import generate_output
from modules.missing_row import MissingRowHandler
from gui.missing_aa_dialog import ask_values_for_missing_aa
from gui.telemetry import UsageTelemetry
from gui.config_edit import ConfigEditor
from gui.stats_wind import UsageStatsWindow
from gui.set_wind import SettingsWindow
import config


class CSVLabGUI:
    """Κύρια κλάση GUI εφαρμογής"""
    drop_zero_var: BooleanVar

    def __init__(self, root):
        self.root = root
        self.root.title("CSV Lab - Σύστημα Επεξεργασίας CSV")
        self.root.geometry("1000x750")

        # Windows-specific: Center window
        self._center_window()

        # Telemetry & Config
        self.telemetry = UsageTelemetry()
        self.telemetry.record_session_start()

        self.config_editor = ConfigEditor()

        # Μεταβλητές
        self.excel_df = None
        self.csv_first_4 = None
        self.dash_part = None
        self.processed_df = None
        self.processing_start_time = None

        self._setup_ui()

        # Log initial message
        self._log("✅ CSV Lab εκκίνησε επιτυχώς!")
        self._log(f"📁 Φάκελος εργασίας: {config.BASE_PATH}")

    def _center_window(self):
        """Κεντράρει το παράθυρο στην οθόνη"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _setup_ui(self):
        """Δημιουργία UI components"""

        # Header με χρώμα
        header_frame = tk.Frame(self.root, bg='#2c3e50', padx=10, pady=15)
        header_frame.pack(fill=tk.X)

        # Title on left
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
            text="Windows Edition - v1.3 (με Usage Tracking)",
            font=("Segoe UI", 9),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(anchor=tk.W)

        # Buttons on right
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

        # Notebook για tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 10])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabs
        self._create_load_tab()
        self._create_settings_tab()
        self._create_process_tab()
        self._create_results_tab()

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

    def _open_settings(self):
        """Άνοιγμα Settings Window"""
        SettingsWindow(self.root, self.config_editor)

    def _open_stats(self):
        """Άνοιγμα Usage Stats Window"""
        UsageStatsWindow(self.root, self.telemetry)

    def _create_load_tab(self):
        """Tab για φόρτωση δεδομένων"""
        load_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(load_frame, text="📂 1. Φόρτωση")

        # File selection
        file_frame = ttk.LabelFrame(load_frame, text="Επιλογή Αρχείου", padding="15")
        file_frame.pack(fill=tk.X, pady=10)

        ttk.Label(file_frame, text="Αρ. Πρωτοκόλλου:", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )

        self.protocol_entry = ttk.Entry(file_frame, width=30, font=("Consolas", 10))
        self.protocol_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(file_frame, text="📥 Φόρτωση", command=self._load_file).grid(
            row=0, column=2, padx=5
        )

        ttk.Button(file_frame, text="🔍 Αναζήτηση", command=self._browse_file).grid(
            row=0, column=3, padx=5
        )

        # File info
        info_frame = ttk.LabelFrame(load_frame, text="Πληροφορίες Αρχείου", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.file_info_text = scrolledtext.ScrolledText(
            info_frame, height=12, state=tk.DISABLED, font=("Consolas", 9), wrap=tk.WORD
        )
        self.file_info_text.pack(fill=tk.BOTH, expand=True)

    def _create_settings_tab(self):
        """Tab για ρυθμίσεις επεξεργασίας"""
        settings_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(settings_frame, text="⚙️ 2. Ρυθμίσεις")

        # Date
        date_frame = ttk.LabelFrame(settings_frame, text="📅 Ημερομηνία", padding="15")
        date_frame.pack(fill=tk.X, pady=10)

        ttk.Label(date_frame, text="Ημερομηνία (DD-MM):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(date_frame, width=20)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(date_frame, text="📆 Σήμερα", command=self._set_analysis_day).grid(row=0, column=2)

        # Time
        time_frame = ttk.LabelFrame(settings_frame, text="🕐 Ώρα", padding="15")
        time_frame.pack(fill=tk.X, pady=10)

        ttk.Label(time_frame, text="Ώρα (HH:MM):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.time_entry = ttk.Entry(time_frame, width=20)
        self.time_entry.insert(0, config.DEFAULT_TIME)
        self.time_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(
            time_frame,
            text="🕐 Random Hour (10:00 - 12:00)",
            command=self._set_random_hour
        ).grid(row=0, column=2, padx=5)

        # Product
        product_frame = ttk.LabelFrame(settings_frame, text="📦 Προϊόν", padding="15")
        product_frame.pack(fill=tk.X, pady=10)

        ttk.Label(product_frame, text="Όνομα:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.product_entry = ttk.Entry(product_frame, width=30)
        self.product_entry.insert(0, config.DEFAULT_PRODUCT)
        self.product_entry.grid(row=0, column=1, padx=10, pady=5)

        # Filter
        filter_frame = ttk.LabelFrame(settings_frame, text="🔧 Φίλτρα", padding="15")
        filter_frame.pack(fill=tk.X, pady=10)

        self.drop_zero_var = tk.BooleanVar(value=getattr(config, 'DROP_ZERO_NUTRIENTS', True))
        ttk.Checkbutton(
            filter_frame,
            text="Αφαίρεση γραμμών με Fat=Protein=Lactose=0",
            variable=self.drop_zero_var
        ).pack(anchor=tk.W, pady=5)

    def _create_process_tab(self):
        """Tab για επεξεργασία"""
        process_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(process_frame, text="⚡ 3. Επεξεργασία")

        # Process button
        self.process_btn = tk.Button(
            process_frame,
            text="▶️ ΕΚΤΕΛΕΣΗ",
            command=self._start_processing,
            font=("Segoe UI", 14, "bold"),
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=15,
            cursor='hand2'
        )
        self.process_btn.pack(pady=20)

        # Progress
        self.progress = ttk.Progressbar(process_frame, mode='indeterminate', length=500)
        self.progress.pack(pady=10)

        # Log
        log_frame = ttk.LabelFrame(process_frame, text="Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=15, state=tk.DISABLED, font=("Consolas", 9), wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def _create_results_tab(self):
        """Tab για αποτελέσματα"""
        results_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(results_frame, text="✅ 4. Αποτελέσματα")

        self.results_text = scrolledtext.ScrolledText(
            results_frame, height=20, state=tk.DISABLED, font=("Consolas", 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=10)

        # Buttons
        button_frame = ttk.Frame(results_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="📁 Φάκελος", command=self._open_output_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📄 Αρχείο", command=self._open_final_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Reset", command=self._reset).pack(side=tk.LEFT, padx=5)

    def _fill_missing_aa_in_df(self):
        if self.excel_df is None:
            return True  # τίποτα να κάνουμε

        # provider που ανοίγει popup για κάθε λείπον aa
        def provider(aa):
            return ask_values_for_missing_aa(self.root, aa, MissingRowHandler.validate_input)

        df2 = MissingRowHandler.insert_missing_aa_rows(self.excel_df, provider)

        # Αν ακυρώσει ο χρήστης, insert_missing_aa_rows επιστρέφει το ίδιο df (rollback)
        if df2 is self.excel_df:
            return False

        self.excel_df = df2
        return True

    def _load_file(self):
        """Φόρτωση αρχείου"""
        protocol = self.protocol_entry.get().strip()
        if not protocol:
            messagebox.showwarning("Προειδοποίηση", "Εισάγετε αριθμό πρωτοκόλλου")
            return

        try:
            loader = DataLoader()
            excel_file = os.path.join(loader.base_path, f"{protocol}.xlsx")

            if not os.path.exists(excel_file):
                messagebox.showerror("Σφάλμα", f"Αρχείο δεν βρέθηκε: {excel_file}")
                return

            import pandas as pd
            import re

            dash_regx = r"(-\d+)"
            result = re.search(dash_regx, protocol)

            if not result or len(protocol) < 4 or not protocol[:4].isdigit():
                messagebox.showerror("Σφάλμα", "Μη έγκυρος αριθμός")
                return

            self.excel_df = pd.read_excel(excel_file)
            self.csv_first_4 = protocol[:4]
            self.dash_part = result.group()
            ok = self._fill_missing_aa_in_df()
            if not ok:
                messagebox.showinfo("Ακύρωση", "Ακυρώθηκε η συμπλήρωση των missing a/a. Δεν έγινε φόρτωση.")
                self.excel_df = None
                return

            info = f"""
Αρχείο: {protocol}.xls
Γραμμές: {len(self.excel_df)}
Στήλες: {', '.join(self.excel_df.columns.tolist())}
            """

            self.file_info_text.config(state=tk.NORMAL)
            self.file_info_text.delete(1.0, tk.END)
            self.file_info_text.insert(1.0, info)
            self.file_info_text.config(state=tk.DISABLED)

            self._log(f"✅ Φορτώθηκε: {protocol}.xls ({len(self.excel_df)} γραμμές)")
            messagebox.showinfo("Επιτυχία", f"Φορτώθηκε: {len(self.excel_df)} γραμμές")

        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            self._log(f"❌ {str(e)}")

    def _browse_file(self):
        """Αναζήτηση αρχείου"""
        filename = filedialog.askopenfilename(
            title="Επιλογή Αρχείου",
            filetypes=[("Excel files", "*.xls *.xlsx"), ("All files", "*.*")]
        )
        if filename:
            protocol = os.path.splitext(os.path.basename(filename))[0]
            self.protocol_entry.delete(0, tk.END)
            self.protocol_entry.insert(0, protocol)
            self._load_file()

    def _set_analysis_day(self):
        if not self.csv_first_4 or len(self.csv_first_4) < 4:
            messagebox.showwarning("Προειδοποίηση", "Δεν υπάρχει έγκυρος Αρ. Πρωτοκολλου (π.χ. 10102010-10)")
            return

        anal_day = f"{self.csv_first_4[0:2]}-{self.csv_first_4[2:4]}"
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, anal_day)
        self._log(f"📅 Ημερομηνία: {anal_day}")

    def _set_random_hour(self):
        """
        Θέτει τυχαία ώρα μεταξύ 10:00 και 12:00
        """
        hour = random.randint(10, 11)  # 10 ή 11
        minute = random.randint(0, 59)  # 00–59

        random_time = f"{hour:02d}:{minute:02d}"

        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, random_time)

        self._log(f"🕐 Random ώρα: {random_time}")

    def _start_processing(self):
        """Έναρξη επεξεργασίας"""
        if self.excel_df is None:
            messagebox.showwarning("Προειδοποίηση", "Φορτώστε αρχείο")
            return

        if not self.date_entry.get().strip():
            messagebox.showwarning("Προειδοποίηση", "Εισάγετε ημερομηνία")
            return

        self.process_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.processing_start_time = datetime.now()

        thread = threading.Thread(target=self._process_data)
        thread.daemon = True
        thread.start()

    def _process_data(self):
        """Επεξεργασία"""
        try:
            self._log("⚡ Έναρξη...")

            self.processed_df = process_data(self.excel_df)

            time_handler = TimeHandler(len(self.processed_df))
            date = self.date_entry.get().strip()
            initial_time = self.time_entry.get().strip()

            parsed_date = datetime.strptime(date, "%d-%m")
            formatted_date = parsed_date.replace(year=datetime.now().year).strftime("%d/%m/%Y")

            sample_ids = time_handler.generate_sample_ids(self.csv_first_4, self.dash_part)
            sample_times, zero_times = time_handler.generate_sample_times(initial_time)

            metadata = MetadataGenerator.generate_metadata(len(self.processed_df), formatted_date)
            metadata['sample_ids'] = sample_ids
            metadata['sample_times'] = sample_times
            metadata['zero_times'] = zero_times

            zero_dfs = prepare_zero_data(len(self.processed_df), formatted_date, zero_times)
            final_path = generate_output(
                self.processed_df,
                metadata,
                zero_dfs,
                drop_zero_nutrients=self.drop_zero_var.get()
            )

            # Calculate duration
            duration = (datetime.now() - self.processing_start_time).total_seconds()

            # Record telemetry
            filename = f"{self.csv_first_4}{self.dash_part}"
            self.telemetry.record_file_processed(filename, len(self.processed_df), duration)

            self._log(f"✅ ΕΠΙΤΥΧΙΑ! ({duration:.1f}s)")
            self.root.after(0, self._show_results, final_path)

        except Exception as e:
            self.telemetry.record_error(str(e))
            self._log(f"❌ {str(e)}")
            self.root.after(0, messagebox.showerror, "Σφάλμα", str(e))
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.process_btn.config(state=tk.NORMAL))

    def _show_results(self, final_path):
        """Εμφάνιση αποτελεσμάτων"""
        results = f"""
✅ ΕΠΙΤΥΧΙΑ!

📄 Αρχείο: {final_path}
📊 Δείγματα: {len(self.processed_df)}
        """

        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)
        self.results_text.config(state=tk.DISABLED)

        self.notebook.select(3)
        messagebox.showinfo("Επιτυχία", f"Ολοκληρώθηκε!\n\nΔείγματα: {len(self.processed_df)}")

    def _open_output_folder(self):
        """Άνοιγμα φακέλου"""
        folder = os.path.dirname(config.FINAL_OUTPUT_PATH)
        if os.path.exists(folder):
            subprocess.Popen(f'explorer "{folder}"')

    def _open_final_file(self):
        """Άνοιγμα αρχείου"""
        if os.path.exists(config.FINAL_OUTPUT_PATH):
            os.startfile(config.FINAL_OUTPUT_PATH)

    def _reset(self):
        """Reset"""
        self.excel_df = None
        self.protocol_entry.delete(0, tk.END)
        self.file_info_text.config(state=tk.NORMAL)
        self.file_info_text.delete(1.0, tk.END)
        self.file_info_text.config(state=tk.DISABLED)
        self.notebook.select(0)

    def _log(self, message):
        """Log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"

        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

        self.status_bar.config(text=message)


def run_gui():
    """Εκτέλεση GUI"""
    root = tk.Tk()

    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    app = CSVLabGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()

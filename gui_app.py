"""
GUI Εφαρμογή με Tkinter για επεξεργασία δεδομένων γάλακτος
Windows Version - Optimized για Windows 10/11
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
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
import config


class MilkDataProcessorGUI:
    """Κύρια κλάση GUI εφαρμογής - Windows Edition"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Smart CSV Lab Manager")
        self.root.geometry("1000x750")
        
        # Windows-specific: Center window
        self._center_window()
        
        # Set icon (optional - προσθέστε αν έχετε .ico)
        self.root.iconbitmap(config.APP_ICON)
        
        # Μεταβλητές
        self.excel_df = None
        self.csv_first_4 = None
        self.dash_part = None
        self.processed_df = None
        
        self._setup_ui()
        
        # Log initial message
        self._log("✅ Εφαρμογή εκκίνησε επιτυχώς!")
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
        header_frame = tk.Frame(self.root, bg=config.BG_COLORS, padx=10, pady=15)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(
            header_frame,
            text="Smart CSV Lab Manager",
            font=("Segoe UI", 40, "bold"),
            bg=config.BG_COLORS,
            fg='white'
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Windows Edition - v1.0",
            font=("Segoe UI", 20),
            bg=config.BG_COLORS,
            fg='#ecf0f1'

        )
        subtitle_label.pack()

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

        # Status bar με χρώμα
        status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_bar = tk.Label(
            status_frame,
            text="Έτοιμο",
            anchor=tk.W,
            bg='#34495e',
            fg='white',
            padx=10,
            font=("Segoe UI",10)
        )
        self.status_bar.pack(fill=tk.X)

    def _create_load_tab(self):
        """Tab για φόρτωση δεδομένων"""
        load_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(load_frame, text="📂 1. Φόρτωση Δεδομένων")

        # File selection
        file_frame = ttk.LabelFrame(load_frame, text="Επιλογή Αρχείου", padding="15")
        file_frame.pack(fill=tk.X, pady=10)

        ttk.Label(
            file_frame, 
            text="Αρ. Πρωτοκόλλου:",
            font=("Segoe UI", 10)
        ).grid(row=0, column=0, sticky=tk.W, pady=5)

        self.protocol_entry = ttk.Entry(file_frame, width=30, font=("Consolas", 10))
        self.protocol_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Button(
            file_frame,
            text="📥 Φόρτωση Αρχείου",
            command=self._load_file
        ).grid(row=0, column=2, padx=5)
        
        ttk.Button(
            file_frame,
            text="🔍 Αναζήτηση...",
            command=self._browse_file
        ).grid(row=0, column=3, padx=5)
        
        # Current folder button
        ttk.Button(
            file_frame,
            text="📁 Άνοιγμα Φακέλου CSV",
            command=self._open_csv_folder
        ).grid(row=1, column=2, columnspan=2, pady=10, sticky=tk.E)
        
        # File info
        info_frame = ttk.LabelFrame(load_frame, text="Πληροφορίες Αρχείου", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.file_info_text = scrolledtext.ScrolledText(
            info_frame,
            height=12,
            state=tk.DISABLED,
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        self.file_info_text.pack(fill=tk.BOTH, expand=True)
    
    def _create_settings_tab(self):
        """Tab για ρυθμίσεις"""
        settings_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(settings_frame, text="⚙️ 2. Ρυθμίσεις")
        
        # Date settings
        date_frame = ttk.LabelFrame(settings_frame, text="📅 Ημερομηνία Ανάλυσης", padding="15")
        date_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(date_frame, text="Ημερομηνία (DD-MM):", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.date_entry = ttk.Entry(date_frame, width=20, font=("Consolas", 10))
        self.date_entry.insert(-1,  f"")
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(
            date_frame,
            text="📆 AUTO - Ημερομηνία",
            command=self._set_analysis_day
        ).grid(row=0, column=2, padx=5)

        # Time settings
        time_frame = ttk.LabelFrame(settings_frame, text="🕐 Αρχική Ώρα", padding="15")
        time_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(time_frame, text="Ώρα (HH:MM):", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )

        self.time_entry = ttk.Entry(time_frame, width=20, font=("Consolas", 10))
        self.time_entry.insert(0, config.DEFAULT_TIME)
        self.time_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(
            time_frame,
            text="🕐 Random Hour (10:00 - 12:00)",
            command=self._set_random_hour
        ).grid(row=0, column=2, padx=5)

        # Product settings
        product_frame = ttk.LabelFrame(settings_frame, text="📦 Προϊόν", padding="15")
        product_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(product_frame, text="Όνομα Προϊόντος:", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.product_entry = ttk.Entry(product_frame, width=30, font=("Segoe UI", 10))
        self.product_entry.insert(0, config.DEFAULT_PRODUCT)
        self.product_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Zero Nutrient Filter settings
        filter_frame = ttk.LabelFrame(settings_frame, text="🔧 Φίλτρα Δεδομένων", padding="15")
        filter_frame.pack(fill=tk.X, pady=10)
        
        self.drop_zero_var = tk.BooleanVar(value=getattr(config, 'DROP_ZERO_NUTRIENTS', True))
        
        zero_check = ttk.Checkbutton(
            filter_frame,
            text="Αφαίρεση γραμμών με Fat=Protein=Lactose=0",
            variable=self.drop_zero_var
        )
        zero_check.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Info label
        info_label = ttk.Label(
            filter_frame,
            text="ℹ️  Αφαιρεί αυτόματα γραμμές όπου όλα τα θρεπτικά συστατικά είναι μηδέν",
            font=("Segoe UI", 8),
            foreground="gray"
        )
        info_label.grid(row=1, column=0, sticky=tk.W, padx=20)
    
    def _create_process_tab(self):
        """Tab για επεξεργασία"""
        process_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(process_frame, text="⚡ 3. Επεξεργασία")
        
        # Info box
        info_text = """
        Πατήστε το κουμπί για να ξεκινήσει η επεξεργασία.
        Η διαδικασία περιλαμβάνει:
        
        ✓ Καθαρισμό δεδομένων
        ✓ Υπολογισμούς TS και SNF
        ✓ Δημιουργία timestamps
        ✓ Ενσωμάτωση zero calibration
        ✓ Εξαγωγή τελικού CSV
        """
        
        info_label = tk.Label(
            process_frame,
            text=info_text,
            justify=tk.LEFT,
            font=("Segoe UI", 10),
            bg='#ecf0f1',
            padx=20,
            pady=15
        )
        info_label.pack(fill=tk.X, pady=10)
        
        # Process button - μεγάλο και εμφανές
        self.process_btn = tk.Button(
            process_frame,
            text="▶️ ΕΚΤΕΛΕΣΗ ΕΠΕΞΕΡΓΑΣΙΑΣ",
            command=self._start_processing,
            font=("Segoe UI", 14, "bold"),
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=15,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3
        )
        self.process_btn.pack(pady=20)
        
        # Progress
        ttk.Label(
            process_frame, 
            text="Πρόοδος:", 
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W, pady=5)
        
        self.progress = ttk.Progressbar(
            process_frame,
            mode='indeterminate',
            length=500
        )
        self.progress.pack(pady=10)
        
        # Log
        log_frame = ttk.LabelFrame(process_frame, text="Αρχείο Καταγραφής", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            state=tk.DISABLED,
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def _create_results_tab(self):
        """Tab για αποτελέσματα"""
        results_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(results_frame, text="✅ 4. Αποτελέσματα")
        
        # Results info
        info_frame = ttk.LabelFrame(results_frame, text="Πληροφορίες Εξόδου", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(
            info_frame,
            height=18,
            state=tk.DISABLED,
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        button_frame = ttk.Frame(results_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="📁 Άνοιγμα Φακέλου",
            command=self._open_output_folder
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="📄 Άνοιγμα Αρχείου",
            command=self._open_final_file
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="🔄 Νέα Επεξεργασία",
            command=self._reset
        ).pack(side=tk.LEFT, padx=5)
    
    def _load_file(self):
        """Φόρτωση αρχείου από αριθμό πρωτοκόλλου"""
        protocol = self.protocol_entry.get().strip()
        
        if not protocol:
            messagebox.showwarning("Προειδοποίηση", "Παρακαλώ εισάγετε αριθμό πρωτοκόλλου")
            return
        
        self._log("🔍 Αναζήτηση αρχείου...")
        
        try:
            loader = DataLoader()
            excel_file = os.path.join(loader.csv_path, f"{protocol}.xls")
            
            if not os.path.exists(excel_file):
                messagebox.showerror("Σφάλμα", f"Το αρχείο δεν βρέθηκε:\n{excel_file}")
                self._log(f"❌ Αρχείο δεν βρέθηκε: {protocol}.xls")
                return
            
            import pandas as pd
            import re
            
            # Parse protocol
            dash_regx = r"(-\d+)"
            result = re.search(dash_regx, protocol)
            
            if not result or len(protocol) < 4 or not protocol[:4].isdigit():
                messagebox.showerror("Σφάλμα", "Μη έγκυρος αριθμός πρωτοκόλλου")
                return
            
            self.excel_df = pd.read_excel(excel_file)
            self.csv_first_4 = protocol[:4]
            self.dash_part = result.group()
            
            # Update file info
            self._update_file_info()
            self._log(f"✅ Φορτώθηκε: {protocol}.xls ({len(self.excel_df)} γραμμές)")
            
            messagebox.showinfo("Επιτυχία", f"Το αρχείο φορτώθηκε επιτυχώς!\n\nΓραμμές: {len(self.excel_df)}")
            
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία φόρτωσης:\n{str(e)}")
            self._log(f"❌ Σφάλμα: {str(e)}")
    
    def _browse_file(self):
        """Αναζήτηση αρχείου με file dialog"""
        initial_dir = config.CSV_PATH if os.path.exists(config.CSV_PATH) else os.path.expanduser("~")
        
        filename = filedialog.askopenfilename(
            title="Επιλογή Αρχείου Excel",
            initialdir=initial_dir,
            filetypes=[
                ("Excel files", "*.xls *.xlsx"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            base_name = os.path.basename(filename)
            protocol = os.path.splitext(base_name)[0]
            self.protocol_entry.delete(0, tk.END)
            self.protocol_entry.insert(0, protocol)
            self._load_file()
    
    def _open_csv_folder(self):
        """Ανοίγει τον φάκελο CSV στον Explorer"""
        if os.path.exists(config.CSV_PATH):
            subprocess.Popen(f'explorer "{config.CSV_PATH}"')
            self._log(f"📁 Άνοιξε ο φάκελος: {config.CSV_PATH}")
        else:
            messagebox.showwarning("Προειδοποίηση", f"Ο φάκελος δεν υπάρχει:\n{config.CSV_PATH}")
    
    def _update_file_info(self):
        """Ενημέρωση πληροφοριών αρχείου"""
        if self.excel_df is None:
            return
        
        info = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    ΠΛΗΡΟΦΟΡΙΕΣ ΑΡΧΕΙΟΥ                           ║
╚══════════════════════════════════════════════════════════════════╝

📋 Βασικά Στοιχεία:
   • Πρώτα 4 ψηφία: {self.csv_first_4}
   • Dash part: {self.dash_part}
   • Συνολικές γραμμές: {len(self.excel_df)}
   • Στήλες: {len(self.excel_df.columns)}

📊 Ονόματα Στηλών:
   {', '.join(self.excel_df.columns.tolist())}

📈 Πρώτες 5 Γραμμές:
{self.excel_df.head().to_string()}
        """
        
        self.file_info_text.config(state=tk.NORMAL)
        self.file_info_text.delete(1.0, tk.END)
        self.file_info_text.insert(1.0, info)
        self.file_info_text.config(state=tk.DISABLED)

    def _set_analysis_day(self):
        if not self.csv_first_4 or len(self.csv_first_4) < 4:
            messagebox.showwarning("Προειδοποίηση", "Δεν υπάρχει έγκυρος Αρ. Πρωτοκολλου (π.χ. 10102010-10)")
            return

        anal_day = f"{self.csv_first_4[0:2]}-{self.csv_first_4[2:4]}"
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, anal_day)
        self._log(f"📅 Ημερομηνία: {anal_day}")

    import random

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
        """Έναρξη επεξεργασίας σε ξεχωριστό thread"""
        if self.excel_df is None:
            messagebox.showwarning("Προειδοποίηση", "Παρακαλώ φορτώστε πρώτα ένα αρχείο")
            return
        
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        
        if not date:
            messagebox.showwarning("Προειδοποίηση", "Παρακαλώ εισάγετε ημερομηνία")
            return
        
        # Disable button
        self.process_btn.config(state=tk.DISABLED, bg='#95a5a6')
        
        # Start processing
        self.progress.start()
        thread = threading.Thread(target=self._process_data)
        thread.daemon = True
        thread.start()
    
    def _process_data(self):
        """Επεξεργασία δεδομένων"""
        try:
            self._log("⚡ Έναρξη επεξεργασίας...")
            
            # Process
            self._log("🔄 Επεξεργασία DataFrame...")
            
            # Χρήση του drop_zero_nutrients flag από το GUI
            drop_zero = self.drop_zero_var.get()
            self._log(f"   Zero Nutrient Filter: {'ΕΝΕΡΓΟ' if drop_zero else 'ΑΝΕΝΕΡΓΟ'}")
            
            self.processed_df = process_data(self.excel_df, drop_zero_nutrients=drop_zero)
            
            # Metadata
            self._log("📝 Δημιουργία μεταδεδομένων...")
            time_handler = TimeHandler(len(self.processed_df))
            
            date = self.date_entry.get().strip()
            initial_time = self.time_entry.get().strip()
            
            parsed_date = datetime.strptime(date, "%d-%m")
            current_year = datetime.now().year
            full_date = parsed_date.replace(year=current_year)
            formatted_date = full_date.strftime("%d/%m/%Y")
            
            sample_ids = time_handler.generate_sample_ids(self.csv_first_4, self.dash_part)
            sample_times, zero_times = time_handler.generate_sample_times(initial_time)
            
            metadata = MetadataGenerator.generate_metadata(len(self.processed_df), formatted_date)
            metadata['sample_ids'] = sample_ids
            metadata['sample_times'] = sample_times
            metadata['zero_times'] = zero_times
            
            # Zero data
            self._log("🔧 Προετοιμασία zero data...")
            zero_dfs = prepare_zero_data(
                len(self.processed_df),
                formatted_date,
                zero_times
            )
            
            # Output
            self._log("📤 Δημιουργία τελικού output...")
            final_path = generate_output(self.processed_df, metadata, zero_dfs)
            
            self._log(f"✅ ΕΠΙΤΥΧΙΑ! Αρχείο: {final_path}")
            
            # Update results
            self.root.after(0, self._show_results, final_path)
            
        except Exception as e:
            self._log(f"❌ ΣΦΑΛΜΑ: {str(e)}")
            self.root.after(0, messagebox.showerror, "Σφάλμα", str(e))
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.process_btn.config(state=tk.NORMAL, bg='#27ae60'))
    
    def _show_results(self, final_path):
        """Εμφάνιση αποτελεσμάτων"""
        results = f"""
╔══════════════════════════════════════════════════════════════════╗
║              ΕΠΕΞΕΡΓΑΣΙΑ ΟΛΟΚΛΗΡΩΘΗΚΕ ΕΠΙΤΥΧΩΣ! ✅              ║
╚══════════════════════════════════════════════════════════════════╝

📄 Τελικό Αρχείο:
   {final_path}

📊 Στατιστικά:
   • Συνολικά δείγματα: {len(self.processed_df)}
   • Zero blocks: {len(self.processed_df) // config.BATCH_SIZE}
   • Συνολικές γραμμές output: {len(self.processed_df) + (len(self.processed_df) // config.BATCH_SIZE) * config.ZERO_BLOCK_ROWS}

🎯 Το αρχείο είναι έτοιμο για χρήση!

💡 Συμβουλές:
   • Ανοίξτε το αρχείο με Excel
   • Ελέγξτε τα δεδομένα πριν τη χρήση
   • Κρατήστε backup του original αρχείου
        """
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)
        self.results_text.config(state=tk.DISABLED)
        
        # Switch to results tab
        self.notebook.select(3)
        
        messagebox.showinfo(
            "Επιτυχία",
            f"Η επεξεργασία ολοκληρώθηκε!\n\n"
            f"Δείγματα: {len(self.processed_df)}\n"
            f"Αρχείο: final.csv"
        )
    
    def _open_output_folder(self):
        """Άνοιγμα φακέλου εξόδου"""
        folder = os.path.dirname(config.FINAL_OUTPUT_PATH)
        if os.path.exists(folder):
            subprocess.Popen(f'explorer "{folder}"')
            self._log(f"📁 Άνοιξε ο φάκελος output")
        else:
            messagebox.showwarning("Προειδοποίηση", "Ο φάκελος δεν υπάρχει ακόμα")
    
    def _open_final_file(self):
        """Άνοιγμα τελικού αρχείου"""
        if os.path.exists(config.FINAL_OUTPUT_PATH):
            os.startfile(config.FINAL_OUTPUT_PATH)
            self._log(f"📄 Άνοιξε το αρχείο: final.csv")
        else:
            messagebox.showwarning("Προειδοποίηση", "Το αρχείο δεν έχει δημιουργηθεί ακόμα")
    
    def _reset(self):
        """Reset εφαρμογής"""
        response = messagebox.askyesno(
            "Επιβεβαίωση",
            "Είστε σίγουροι ότι θέλετε να κάνετε reset;\n"
            "Θα χαθούν όλα τα φορτωμένα δεδομένα."
        )
        
        if not response:
            return
        
        self.excel_df = None
        self.csv_first_4 = None
        self.dash_part = None
        self.processed_df = None
        
        self.protocol_entry.delete(0, tk.END)
        
        self.file_info_text.config(state=tk.NORMAL)
        self.file_info_text.delete(1.0, tk.END)
        self.file_info_text.config(state=tk.DISABLED)
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        self.notebook.select(0)
        self._log("🔄 Εφαρμογή επαναφέρθηκε")
    
    def _log(self, message):
        """Καταγραφή μηνύματος"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.status_bar.config(text=message)


def run_gui():
    """Εκτέλεση GUI εφαρμογής"""
    root = tk.Tk()
    
    # Windows-specific optimizations
    try:
        # Enable DPI awareness for Windows
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = MilkDataProcessorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()

"""
Process Tab Module
Handles data processing and logging
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
import os
from datetime import datetime

import pandas as pd

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from modules.data_processor import process_data
from modules.time_handler import TimeHandler, MetadataGenerator
from modules.zero_manager import prepare_zero_data
from modules.output_generator import generate_output
from modules.missing_row import MissingRowHandler
from gui.missing_aa_dialog import ask_values_for_missing_aa


class ProcessTab:
    """Tab για επεξεργασία"""

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
        # Process button
        self.process_btn = tk.Button(
            self.frame,
            text="▶️ ΕΚΤΕΛΕΣΗ",
            command=self.start_processing,
            font=("Segoe UI", 14, "bold"),
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=15,
            cursor='hand2'
        )
        self.process_btn.pack(pady=20)

        # Progress
        self.progress = ttk.Progressbar(self.frame, mode='indeterminate', length=500)
        self.progress.pack(pady=10)

        # LOG LABELS
        self.status_label = tk.Label(
            self.frame,
            text="Αναμονή για εκτέλεση",
            fg="#555",
            font=("Segoe UI", 10)
        )
        self.status_label.pack(pady=10)

    def set_status(self, text, color="#555"):
        def ui():
            self.status_label.config(text=text, fg=color)
            self.app.update_status(text)
            self.app.log(text)

        self.app.root.after(0, ui)

    def start_processing(self):
        """Έναρξη επεξεργασίας"""
        if self.app.excel_df is None:
            messagebox.showwarning("Προειδοποίηση", "Φορτώστε αρχείο")
            return

        if not self.app.settings_tab.get_date():
            messagebox.showwarning("Προειδοποίηση", "Εισάγετε ημερομηνία")
            return

        self.process_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.app.processing_start_time = datetime.now()

        thread = threading.Thread(target=self._process_data)
        thread.daemon = True
        thread.start()

    def _handle_missing_aa_ui(self, missing_list):
        # value_provider για τον handler σου
        def value_provider(aa: int):
            return ask_values_for_missing_aa(self.app.root, aa, MissingRowHandler.validate_input)

        old_df = self.app.excel_df
        new_df = MissingRowHandler.insert_missing_aa_rows(old_df, value_provider, col="a/a")

        # Cancel => rollback => ο handler επιστρέφει το ίδιο df object
        if new_df is old_df:
            self.set_status("⛔ Ακυρώθηκε η συμπλήρωση. Δεν συνεχίζω.", "#c0392b")
            return

        self.app.excel_df = new_df
        self.set_status("✅ Συμπληρώθηκαν τα missing a/a. Ξεκινάω ξανά...", "#27ae60")

        # ξαναξεκίνα processing (σε thread)
        self.process_btn.config(state=tk.DISABLED)
        self.progress.start()
        t = threading.Thread(target=self._process_data, daemon=True)
        t.start()

    def _process_data(self):
        # =================================================
        # 📊 Έλεγχος επαναλαμβανόμενων γραμμών (replicates)
        # =================================================
        try:
            aa_col = "a/a"
            df = self.app.excel_df

            if aa_col in df.columns:
                aa_numeric = pd.to_numeric(df[aa_col], errors="coerce").dropna()

                if not aa_numeric.empty:
                    last_aa = int(aa_numeric.max())
                    total_rows = len(df)
                    repeats = total_rows - last_aa

                    if repeats > 0:
                        self.app.logger.info(
                            f"🔁 Επαναλαμβανόμενες γραμμές: {repeats} "
                            f"(τελευταίο a/a={last_aa}, σύνολο γραμμών={total_rows})"
                        )
                    else:
                        self.app.logger.info(
                            f"✅ Καμία επαναλαμβανόμενη γραμμή "
                            f"(τελευταίο a/a={last_aa}, σύνολο γραμμών={total_rows})"
                        )
        except Exception as e:
            self.app.logger.warn(f"⚠️ Αδυναμία υπολογισμού επαναλαμβανόμενων: {e}")

        # =================
        # ΑΡΧΗ ΕΠΕΞΕΡΓΑΣΙΑΣ
        # =================

        try:
            self.set_status("⚡ Έναρξη επεξεργασίας...", "#2980b9")

            self.set_status("🔍 Έλεγχος για missing a/a...", "#2980b9")
            missing_rows = MissingRowHandler.find_missing_aa_rows(self.app.excel_df)

            if missing_rows:
                self.app.logger.warn(f"⚠️ Λείπουν a/a: {missing_rows}")
                self.set_status("⛔ Λείπουν a/a – συμπλήρωσέ τα για να συνεχίσω.", "#c0392b")

                # σταμάτα UI indicators τώρα
                self.app.root.after(0, self.progress.stop)
                self.app.root.after(0, lambda: self.process_btn.config(state=tk.NORMAL))

                # άνοιξε διαλόγους στο UI thread
                self.app.root.after(0, self._handle_missing_aa_ui, missing_rows)
                return

            # Μόνο αν ΔΕΝ υπάρχουν missing συνεχίζεις
            self._continue_processing()
            self.set_status("✅ Ολοκληρώθηκε!", "#27ae60")

        except Exception as e:
            self.app.telemetry.record_error(str(e))
            self.app.logger.error(f"❌ {str(e)}")
            self.set_status(f"❌ Σφάλμα: {e}", "#c0392b")
            self.app.root.after(0, messagebox.showerror, "Σφάλμα", str(e))

        finally:
            self.app.root.after(0, self.progress.stop)
            self.app.root.after(0, lambda: self.process_btn.config(state=tk.NORMAL))

    def _continue_processing(self):
        """Συνέχεια επεξεργασίας"""
        try:
            # ΒΗΜΑ 2: Επεξεργασία (ΧΩΡΙΣ drop_zero)
            self.app.logger.info("⚙️ Επεξεργασία δεδομένων...")
            temp_df = process_data(self.app.excel_df)

            # ΒΗΜΑ 3: DROP_ZERO_NUTRIENTS στο τέλος
            if self.app.settings_tab.get_drop_zero():
                self.app.logger.info("🧹 Εφαρμογή DROP_ZERO_NUTRIENTS...")
                before_count = len(temp_df)
                temp_df = temp_df[
                    ~((temp_df['Fat'] == 0) &
                      (temp_df['Protein'] == 0) &
                      (temp_df['Lactose'] == 0))
                ].reset_index(drop=True)
                after_count = len(temp_df)
                removed = before_count - after_count
                self.app.logger.info(f"  🗑️ Αφαιρέθηκαν {removed} γραμμές")

            self.app.processed_df = temp_df

            # ΒΗΜΑ 4: Metadata
            self.app.logger.info("🕐 Δημιουργία timestamps...")
            time_handler = TimeHandler(len(self.app.processed_df))
            date = self.app.settings_tab.get_date()
            initial_time = self.app.settings_tab.get_time()

            parsed_date = datetime.strptime(date, "%d-%m")
            formatted_date = parsed_date.replace(year=datetime.now().year).strftime("%d/%m/%Y")

            sample_ids = time_handler.generate_sample_ids(self.app.csv_first_4, self.app.dash_part)
            sample_times, zero_times = time_handler.generate_sample_times(initial_time)

            # ΒΗΜΑ 5: Generate output
            self.app.logger.info("📝 Δημιουργία metadata...")
            metadata = MetadataGenerator.generate_metadata(len(self.app.processed_df), formatted_date)
            metadata["protocol_number"] = self.app.protocol_number
            metadata['sample_ids'] = sample_ids
            metadata['sample_times'] = sample_times
            metadata['zero_times'] = zero_times

            self.app.logger.info(f"📦 Product: {self.app.settings_tab.get_product()}")

            self.app.logger.info("0️⃣ Προετοιμασία zero data...")
            zero_dfs = prepare_zero_data(len(self.app.processed_df), formatted_date, zero_times)

            self.app.logger.info("💾 Δημιουργία τελικού αρχείου...")
            final_path = generate_output(self.app.processed_df, metadata, zero_dfs)
            self.app.last_output_path = final_path

            # Telemetry
            duration = (datetime.now() - self.app.processing_start_time).total_seconds()
            filename = f"{self.app.csv_first_4}{self.app.dash_part}"
            self.app.telemetry.record_file_processed(filename, len(self.app.processed_df), duration)

            self.app.logger.info(f"✅ ΕΠΙΤΥΧΙΑ! ({duration:.1f}s)")
            self.app.root.after(0, self.app.results_tab.show_results, final_path)

        except Exception as e:
            self.app.telemetry.record_error(str(e))
            self.app.logger.error(f"❌ {str(e)}")
            self.app.root.after(0, messagebox.showerror, "Σφάλμα", str(e))
        finally:
            self.app.root.after(0, self.progress.stop)
            self.app.root.after(0, lambda: self.process_btn.config(state=tk.NORMAL))

    def get_frame(self):
        """Returns the frame"""
        return self.frame

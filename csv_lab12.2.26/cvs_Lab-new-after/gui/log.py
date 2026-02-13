# gui/log.py
from datetime import datetime
import tkinter as tk

class UILogger:
    def __init__(self, text_widget: tk.Text, status_label=None):
        self.text = text_widget
        self.status = status_label

    def _write(self, level: str, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] [{level}] {msg}\n"

        def ui():
            self.text.config(state=tk.NORMAL)
            self.text.insert(tk.END, line)
            self.text.see(tk.END)
            self.text.config(state=tk.DISABLED)
            if self.status:
                self.status.config(text=msg)

        # ασφαλές και για threads
        self.text.after(0, ui)

    def info(self, msg): self._write("INFO", msg)
    def warn(self, msg): self._write("WARN", msg)
    def error(self, msg): self._write("ERROR", msg)
    

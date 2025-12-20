import tkinter as tk
from tkinter import ttk, messagebox

class MissingAADialog(tk.Toplevel):
    def __init__(self, parent, aa, validator_func):
        super().__init__(parent)
        self.title(f"Συμπλήρωση γραμμής για a/a = {aa}")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.aa = aa
        self.validator = validator_func
        self.result = None

        self.fat_var = tk.StringVar()
        self.protein_var = tk.StringVar()
        self.lactose_var = tk.StringVar()
        self.fpd_var = tk.StringVar()

        self._build_ui()
        self._center(parent)
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _build_ui(self):
        container = ttk.Frame(self, padding=12)
        container.grid(row=0, column=0)

        ttk.Label(container, text=f"Λείπει το a/a = {self.aa}", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        ttk.Label(container, text="Fat:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        fat_entry = ttk.Entry(container, textvariable=self.fat_var, width=18)
        fat_entry.grid(row=1, column=1, sticky="w", pady=4)

        ttk.Label(container, text="Protein:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
        ttk.Entry(container, textvariable=self.protein_var, width=18).grid(row=2, column=1, sticky="w", pady=4)

        ttk.Label(container, text="Lactose:").grid(row=3, column=0, sticky="e", padx=(0, 8), pady=4)
        ttk.Entry(container, textvariable=self.lactose_var, width=18).grid(row=3, column=1, sticky="w", pady=4)

        ttk.Label(container, text="FPD (≤0):").grid(row=4, column=0, sticky="e", padx=(0, 8), pady=4)
        ttk.Entry(container, textvariable=self.fpd_var, width=18).grid(row=4, column=1, sticky="w", pady=4)

        btns = ttk.Frame(container)
        btns.grid(row=5, column=0, columnspan=2, sticky="e", pady=(12, 0))

        ttk.Button(btns, text="Cancel", command=self._on_cancel).pack(side="right", padx=6)
        ttk.Button(btns, text="OK", command=self._on_ok).pack(side="right")

        fat_entry.focus_set()

    def _center(self, parent):
        self.update_idletasks()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()

        w = self.winfo_width()
        h = self.winfo_height()

        x = px + (pw // 2) - (w // 2)
        y = py + (ph // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _on_ok(self):
        values = {}
        for field, var in [
            ("fat", self.fat_var),
            ("proteine", self.protein_var),
            ("lactose ", self.lactose_var),
            ("freeze point", self.fpd_var),
        ]:
            raw = var.get().strip().replace(",", ".")
            ok, parsed, err = self.validator(raw, field)
            if not ok:
                messagebox.showerror("Σφάλμα τιμής", err, parent=self)
                return
            values[field] = parsed

        self.result = values
        self.destroy()

    def _on_cancel(self):
        self.result = None
        self.destroy()


def ask_values_for_missing_aa(parent, aa, validator_func):
    dlg = MissingAADialog(parent, aa, validator_func)
    parent.wait_window(dlg)
    return dlg.result

import pandas as pd
import numpy as np


class MissingRowHandler:
    """Συμπληρώνει τα κενά της αυξουσας σειράς 'a/a' με manual input από χρήστη."""

    # ---------- CORE: FIND MISSING a/a ----------

    @staticmethod
    def find_missing_aa_numbers(df, col="a/a"):
        """
        Βρίσκει ποια a/a λείπουν από την αυξουσα σειρά.
        Παράδειγμα: [1,2,4,7] -> [3,5,6]
        """
        if df is None or col not in df.columns:
            return []

        aa = pd.to_numeric(df[col], errors="coerce").dropna()
        if aa.empty:
            return []

        aa_int = aa.astype(int)
        aa_sorted_unique = sorted(set(aa_int.tolist()))
        if len(aa_sorted_unique) < 2:
            return []

        start, end = aa_sorted_unique[0], aa_sorted_unique[-1]
        expected = set(range(start, end + 1))
        missing = sorted(expected - set(aa_sorted_unique))
        return missing

    # ---------- CREATE ROW FROM USER INPUT ----------

    @staticmethod
    def create_manual_row(user_input):
        """
        Δημιουργεί νέα γραμμή από user input.
        user_input dict:
            {"aa": int, "Fat": float, "Protein": float, "Lactose": float, "FPD": float}
        """
        new_row = {
            "a/a": user_input.get("aa", ""),
            "fat": float(user_input.get("fat", 0.0)),
            "proteine": float(user_input.get("proteine", 0.0)),
            "lactose ": float(user_input.get("lactose ", 0.0)),
            "freeze point": float(user_input.get("freeze point", 0.0)),
        }

        new_row.update(MissingRowHandler._calculate_auto_fields(new_row))
        return new_row

    @staticmethod
    def _calculate_auto_fields(row):
        """
        Υπολογίζει αυτόματα TS και SNF.
        """
        fat = float(row.get("fat", 0.0))
        protein = float(row.get("proteine", 0.0))
        lactose = float(row.get("lactose ", 0.0))
        fpd = float(row.get("freeze point", 0.0))

        return {
            "freeze point": fpd,
        }

    # ---------- VALIDATION ----------
    @staticmethod
    def validate_input(value, field_name):
        try:
            parsed = float(str(value).strip().replace(",", "."))

            # 1) Ειδικός κανόνας για FPD
            if field_name == "freeze point":
                if parsed > 0:
                    return False, None, "FPD πρέπει να είναι ≤ 0"
                return True, parsed, ""

            # 2) Γενικός κανόνας για όλα τα άλλα (μη αρνητικά)
            if parsed < 0:
                return False, None, f"{field_name} δεν μπορεί να είναι αρνητικό"

            if field_name == "fat" and parsed > 10:
                return False, None, "Fat είναι πολύ υψηλό (>10%)"
            if field_name == "proteine" and parsed > 6:
                return False, None, "Protein είναι πολύ υψηλό (>6%)"
            if field_name == "lactose " and parsed > 8:
                return False, None, "Lactose είναι πολύ υψηλό (>8%)"

            return True, parsed, ""

        except (ValueError, TypeError):
            return False, None, f"Μη έγκυρη τιμή για {field_name}"

    # ---------- INSERT MISSING ROWS (CANCEL = ROLLBACK) ----------

    @staticmethod
    def insert_missing_aa_rows(df, value_provider, col="a/a"):
        """
        Συμπληρώνει τα κενά a/a με νέες γραμμές.

        value_provider: function(aa:int) -> dict {"Fat","Protein","Lactose","FPD"} ή None αν Cancel

        Cancel σε οποιοδήποτε popup => επιστρέφει το αρχικό df (rollback).
        """
        if df is None or col not in df.columns:
            return df

        missing = MissingRowHandler.find_missing_aa_numbers(df, col)
        if not missing:
            return df

        new_rows = []
        for aa in missing:
            user_vals = value_provider(aa)

            # Cancel => ΣΤΑΜΑΤΑΜΕ ΟΛΑ (rollback)
            if user_vals is None:
                return df

            user_vals = dict(user_vals)  # ασφάλεια
            user_vals["aa"] = aa

            row = MissingRowHandler.create_manual_row(user_vals)

            # φτιάχνουμε row με ΟΛΑ τα columns του df (ό,τι λείπει -> NaN)
            full = {c: np.nan for c in df.columns}
            full.update(row)
            new_rows.append(full)

        out = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

        s = pd.to_numeric(out[col], errors="coerce")
        s = s.replace([np.inf, -np.inf], np.nan)
        out[col] = s.astype("Int64")  # <-- δέχεται NA
        out = out.sort_values(col, kind="mergesort", na_position="last").reset_index(drop=True)

        return out

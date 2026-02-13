"""
Module για την επεξεργασία και καθαρισμό δεδομένων DataFrame
Windows Version - Updated με Zero Nutrient Filter
"""
import pandas as pd
from typing import List, Optional

# Import config με fallback
try:
    from . import config
except ImportError:
    import config


class DataProcessor:
    """Κλάση για την επεξεργασία δεδομένων γάλακτος"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
    
    def initial_filtering(self) -> pd.DataFrame:
        """
        Εκτελεί αρχικό καθαρισμό και φιλτράρισμα του DataFrame
        
        Returns:
            pd.DataFrame: Καθαρισμένο DataFrame
        """
        # Αφαίρεση περιττής στήλης μετά το 'a/a'
        self._remove_column_after_aa()
        
        # Καθαρισμός whitespace από ονόματα στηλών
        self.df.columns = self.df.columns.str.strip()
        
        # Διαγραφή περιττών στηλών
        self._remove_unnecessary_columns()
        
        # Αφαίρεση duplicates
        self.df = self.df.drop_duplicates()
        
        # Καθαρισμός NaN σειρών στο a/a
        self.df = self.df.dropna(subset=["a/a"])
        
        # Reset index
        self.df = self.df.reset_index(drop=True)
        
        # Μετατροπή a/a σε integer
        self.df["a/a"] = self.df["a/a"].astype(int)
        
        # Μετονομασίες στηλών
        self.df = self.df.rename(columns=config.COLUMN_RENAMES)
        dupes = self.df.columns[self.df.columns.duplicated()].tolist()
        print("DUPLICATE COLS:", dupes)

        print(f"✅ Αρχικό filtering ολοκληρώθηκε. Σύνολο γραμμών: {len(self.df)}")
        return self.df
    

    def _remove_column_after_aa(self):
        """Διαγράφει τη στήλη αμέσως μετά το 'a/a' ΜΟΝΟ αν είναι άχρηστη."""
        cols = self.df.columns.tolist()
        if "a/a" not in cols:
            return

        idx = cols.index("a/a")
        if idx + 1 >= len(cols):
            return

        col_to_delete = cols[idx + 1]

        # ✅ Προστασία: ΜΗΝ σβήνεις χρήσιμες στήλες
        protected = {"Fat", "Protein", "Lactose", "FPD", "freeze point", "proteine", "fat", "lactose"}
        if col_to_delete.strip() in protected:
            # Είναι χρήσιμη → μην την πειράξεις
            return

        self.df = self.df.drop(columns=[col_to_delete])
        print(f"Η στήλη '{col_to_delete}' διαγράφηκε.")

    def _remove_unnecessary_columns(self):
        """Διαγράφει περιττές στήλες"""
        cols_to_delete = [col for col in config.COLS_TO_DELETE if col in self.df.columns]
        if cols_to_delete:
            self.df = self.df.drop(columns=cols_to_delete)
            print(f"Διαγράφηκαν στήλες: {cols_to_delete}")
    
    def format_decimals(self, two_dec_cols: List[str] = None, 
                       four_dec_cols: List[str] = None) -> pd.DataFrame:
        """
        Μορφοποιεί δεκαδικά ψηφία και ελέγχει για σφάλματα
        
        Args:
            two_dec_cols: Στήλες με 2 δεκαδικά
            four_dec_cols: Στήλες με 4 δεκαδικά
            
        Returns:
            pd.DataFrame: Μορφοποιημένο DataFrame
        """
        two_dec_cols = two_dec_cols or config.TWO_DECIMAL_COLS
        four_dec_cols = four_dec_cols or config.FOUR_DECIMAL_COLS
        
        # Μορφοποίηση
        for col in two_dec_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                self.df[col] = self.df[col].apply(lambda x: self._smart_format(x, 2))
        
        for col in four_dec_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                self.df[col] = self.df[col].apply(lambda x: self._smart_format(x, 4))
        
        # Έλεγχος δεκαδικών
        self._validate_decimals(two_dec_cols, 2)
        self._validate_decimals(four_dec_cols, 4)
        
        return self.df
    
    @staticmethod
    def _smart_format(x, decimals: int) -> str:
        """Μορφοποιεί αριθμό με καθορισμένα δεκαδικά"""
        if pd.isna(x):
            return x
        try:
            x = float(x)
            return f"{x:.{decimals}f}".rstrip("0").rstrip(".")
        except (ValueError, TypeError):
            return x
    
    @staticmethod
    def _count_decimals(x) -> int:
        """Μετρά τα δεκαδικά ψηφία μιας τιμής"""
        if pd.isna(x):
            return 0
        s = str(x)
        if "." in s:
            return len(s.split(".")[1])
        return 0
    
    def _validate_decimals(self, columns: List[str], max_decimals: int):
        """Ελέγχει αν οι στήλες τηρούν τα όρια δεκαδικών"""
        decimal_errors = []
        
        for col in columns:
            if col not in self.df.columns:
                continue
            
            for idx, val in self.df[col].items():
                decs = self._count_decimals(val)
                if decs > max_decimals:
                    decimal_errors.append(
                        f"Στήλη '{col}', γραμμή {idx}, τιμή {val} "
                        f"έχει {decs} δεκαδικά (max {max_decimals})"
                    )
        
        if not decimal_errors:
            print(f"✅ Όλες οι στήλες τηρούν σωστά τα όρια {max_decimals} δεκαδικών.")
        else:
            print(f"❌ Βρέθηκαν {len(decimal_errors)} σφάλματα δεκαδικών:")
            for err in decimal_errors[:5]:  # Εμφάνιση μόνο 5 πρώτων
                print(f"  {err}")
            if len(decimal_errors) > 5:
                print(f"  ... και {len(decimal_errors) - 5} ακόμα σφάλματα")
    
    def calculate_derived_values(self) -> pd.DataFrame:
        """
        Υπολογίζει παράγωγες τιμές (TS, SNF)
        
        Returns:
            pd.DataFrame: DataFrame με νέες στήλες
        """
        # Υπολογισμός TS (Total Solids)
        self.df['TS'] = (
            self.df['Fat'].astype(float) + 
            self.df['Protein'].astype(float) + 
            self.df['Lactose'].astype(float)
        ).round(2)
        
        # Υπολογισμός SNF (Solids Non-Fat)
        self.df['SNF'] = (
            self.df['Protein'].astype(float) + 
            self.df['Lactose'].astype(float) + 
            0.7
        ).round(2)
        
        print("✅ Υπολογίστηκαν TS και SNF")
        return self.df
    
    def get_processed_data(self) -> pd.DataFrame:
        """Επιστρέφει το επεξεργασμένο DataFrame"""
        return self.df


def process_data(excel_df: pd.DataFrame) -> pd.DataFrame:
    """
    Wrapper function για πλήρη επεξεργασία δεδομένων
    
    Args:
        excel_df: Το αρχικό DataFrame από το Excel
        drop_zero_nutrients: Αν None, χρησιμοποιεί την τιμή από config
        
    Returns:
        pd.DataFrame: Πλήρως επεξεργασμένο DataFrame
    """

    
    processor = DataProcessor(excel_df)
    
    # Βασική επεξεργασία
    processor.initial_filtering()

    
    # Συνέχεια επεξεργασίας
    processor.format_decimals()
    processor.calculate_derived_values()
    
    return processor.get_processed_data()


if __name__ == "__main__":
    # Test του module
    print("=" * 70)
    print("TEST: Data Processor Module με Zero Nutrient Filter")
    print("=" * 70)
    
    # Δημιουργία test data
    import pandas as pd

    test_df = pd.DataFrame({
        "a/a": [1, 2, 3, 4, 5],
        "Unnamed: 1": ["", "", "", "", ""],  # άχρηστη
        "Fat": [3.5, 0, 3.7, 0, 3.8],
        "Protein": [3.2, 0, 3.4, 3.5, 3.6],
        "Lactose": [4.8, 0, 5.0, 0, 5.1],
        "freeze point": [0.520, 0.521, 0.522, 0.523, 0.524],
    })

    print("\nΑρχικά δεδομένα:")
    print(test_df)
    
    print("\n" + "=" * 70)
    result = process_data(test_df, drop_zero_nutrients=True)
    
    print("\n" + "=" * 70)
    print("Τελικά δεδομένα:")
    print(result)

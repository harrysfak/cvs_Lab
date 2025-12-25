import os
from pathlib import Path

# Φάκελος ρίζας project (ένα επίπεδο πάνω από το /gui, /modules κλπ)
APP_PATH = Path(__file__).resolve().parent  # αν το config.py είναι στη ρίζα
# αν το config.py είναι μέσα σε /gui τότε θες:.parent.parent
# Βασικά paths
BASE_PATH = r"C:/excel"

# output folder μέσα στο project (ασφαλές default)
OUTPUT_PATH = r"C:/excel"

# Files/folders
PARTS_PATH = APP_PATH / "parts"
ZERO_PATH = APP_PATH / "zero" / "zero.xlsx"
FINAL_OUTPUT_PATH = OUTPUT_PATH + "\\" + "final.csv"

ZERO_REMOTE_URL = (
    "https://qhlpulnlyvarhmckbelq.supabase.co/"
    "storage/v1/object/public/zero/zero.xlsx"
)

APP_ICON = "assets\\ico\\icon2.ico"

# αν κάπου θες string και όχι Path:
# str(FINAL_OUTPUT_PATH)


# ============================================================
# ΠΑΡΑΜΕΤΡΟΙ ΕΠΕΞΕΡΓΑΣΙΑΣ
# ============================================================

# Στήλες για έλεγχο δεκαδικών
TWO_DECIMAL_COLS = ["Fat", "Protein", "Lactose"]
FOUR_DECIMAL_COLS = ["FPD"]

# Στήλες προς διαγραφή
COLS_TO_DELETE = ["PH", "syal", "som cells", "water", "omx", "antibiotics"]

# Αφαίρεση γραμμών με μηδενικά nutrients
DROP_ZERO_NUTRIENTS = True

# Μετονομασίες στηλών
COLUMN_RENAMES = {
    'proteine': 'Protein',
    'fat': 'Fat',
    'lactose': 'Lactose',
    'freeze point': 'FPD'
}

# ============================================================
# ΠΑΡΑΜΕΤΡΟΙ ΧΡΟΝΙΣΜΟΥ
# ============================================================

BATCH_SIZE = 87
T_SAMPLE_INCREMENT = 45
T_ZERO_INCREMENT = 20
ZERO_BLOCK_ROWS = 8  # Γραμμές ανά zero block
ZERO_ROW_INDEX = [1, 2, 3, 4, 5, 6, 7, 9]  # Indices για update timestamps

# ============================================================
# ΠΡΟΕΠΙΛΕΓΜΕΝΕΣ ΤΙΜΕΣ
# ============================================================

DEFAULT_PRODUCT = "AIG NEWXX"
DEFAULT_TIME = "11:00"
DEFAULT_REP = 1

# ============================================================
# ΣΕΙΡΑ ΣΤΗΛΩΝ ΓΙΑ ΤΕΛΙΚΟ OUTPUT
# ============================================================

TARGET_COLUMN_ORDER = [
    'Sample Id', 'Rep #', 'Product', 'Fat', 'Protein',
    'Lactose', 'FPD', 'TS', 'SNF', 'Date', 'Time', 'Remark'
]

# ============================================================
# ΠΑΡΑΜΕΤΡΟΙ GUI
# ============================================================

BG_COLORS = "#131D1C"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def validate_config():
    """Ελέγχει αν οι βασικές διαδρομές υπάρχουν"""
    print("Έλεγχος διαδρομών...")

    if not os.path.exists(BASE_PATH):
        print(f"❌ Το BASE_PATH δεν υπάρχει: {BASE_PATH}")
        print(f"   Δημιουργία φακέλου...")
        try:
            os.makedirs(BASE_PATH, exist_ok=True)
            print(f"✅ Δημιουργήθηκε: {BASE_PATH}")
        except Exception as e:
            print(f"❌ Αποτυχία δημιουργίας: {e}")
            return False
    else:
        print(f"✅ BASE_PATH υπάρχει: {BASE_PATH}")

    return True


def create_directory_structure():
    """Δημιουργεί τη δομή φακέλων αν δεν υπάρχει"""
    print("\nΔημιουργία δομής φακέλων...")

    directories = [
        BASE_PATH,
        PARTS_PATH,
        os.path.dirname(ZERO_PATH)
    ]

    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✅ Δημιουργήθηκε: {directory}")
            except Exception as e:
                print(f"❌ Αποτυχία δημιουργίας {directory}: {e}")
        else:
            print(f"ℹ️  Υπάρχει ήδη: {directory}")


def print_config():
    """Εμφανίζει την τρέχουσα ρύθμιση"""
    print("\n" + "=" * 70)
    print("ΡΥΘΜΙΣΕΙΣ ΣΥΣΤΗΜΑΤΟΣ")

    print("=" * 70)

    print(f"APP_ICON:          {APP_ICON}")
    print(f"BASE_PATH:         {BASE_PATH}")
    print(f"PARTS_PATH:        {PARTS_PATH}")
    print(f"ZERO_PATH:         {ZERO_PATH}")
    print(f"FINAL_OUTPUT_PATH: {FINAL_OUTPUT_PATH}")
    print("=" * 70)
    print(f"BATCH_SIZE:        {BATCH_SIZE} δείγματα")
    print(f"T_SAMPLE_INC:      {T_SAMPLE_INCREMENT} δευτερόλεπτα")
    print(f"T_ZERO_INC:        {T_ZERO_INCREMENT} δευτερόλεπτα")
    print(f"DEFAULT_PRODUCT:   {DEFAULT_PRODUCT}")
    print("=" * 70)


if __name__ == "__main__":
    print_config()

    if validate_config():
        print("\n✅ Οι ρυθμίσεις είναι έγκυρες!")
        create_directory_structure()
        print("\n✅ Η δομή φακέλων είναι έτοιμη!")
    else:
        print("\n❌ Υπάρχουν προβλήματα με τις ρυθμίσεις.")

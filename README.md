# Σύστημα Επεξεργασίας Δεδομένων Γάλακτος

Εφαρμογή σε Python για καθαρισμό, μορφοποίηση και παραγωγή τελικού CSV από αρχεία Excel εργαστηρίου, με ενδιάμεσα zero calibration blocks.

## Περιεχόμενα
- [Λειτουργίες](#λειτουργίες)
- [Απαιτήσεις](#απαιτήσεις)
- [Εγκατάσταση](#εγκατάσταση)
- [Ρυθμίσεις](#ρυθμίσεις)
- [Εκτέλεση](#εκτέλεση)
- [Δομή φακέλων](#δομή-φακέλων)
- [Σημειώσεις](#σημειώσεις)

## Λειτουργίες
- Φόρτωση Excel αρχείων από προκαθορισμένο φάκελο.
- Καθαρισμός και μετασχηματισμός δεδομένων (μετονομασίες, έλεγχοι δεκαδικών, υπολογισμός TS/SNF).
- Προαιρετικό φιλτράρισμα γραμμών με μηδενικές τιμές (Fat/Protein/Lactose).
- Δημιουργία χρονικών metadata και sample IDs.
- Εισαγωγή zero calibration blocks.
- Παραγωγή τελικού CSV.

## Απαιτήσεις
- Python 3.9+
- Βιβλιοθήκες:
  - `pandas`
  - `openpyxl`
  - `xlrd`
  - `numpy`
  - `requests`

## Εγκατάσταση
### Windows (One-Click)
1. Κάντε διπλό κλικ στο `install_one_click.bat`.
2. Περιμένετε να ολοκληρωθεί η εγκατάσταση.
3. Εκτελέστε:
   - `run_gui.bat` για GUI, ή
   - `python main.py` για CLI (μέσα από το `.venv`).

> Το script δημιουργεί `.venv`, εγκαθιστά τις βιβλιοθήκες και τρέχει το `config.py`.

### Χειροκίνητα (Windows/macOS/Linux)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> Αν δεν υπάρχει `requirements.txt`, εγκαταστήστε τα packages χειροκίνητα:
```bash
pip install pandas openpyxl xlrd numpy requests
```

## Ρυθμίσεις
Οι βασικές ρυθμίσεις βρίσκονται στο `config.py`:
- `BASE_PATH`: ρίζα φακέλων δεδομένων (Windows path).
- `CSV_PATH`: φάκελος εισόδου Excel.
- `ZERO_PATH`: θέση του zero.xlsx.
- `FINAL_OUTPUT_PATH`: τελικό CSV.
- `DROP_ZERO_NUTRIENTS`: ενεργοποίηση/απενεργοποίηση φίλτρου μηδενικών.

Για δημιουργία δομής φακέλων:
```bash
python config.py
```

## Εκτέλεση
Κύρια εκτέλεση:
```bash
python main.py
```

Θα ζητηθεί:
1. Αρ. πρωτοκόλλου εργαστηρίου (π.χ. `1234-56`).
2. Ημερομηνία ανάλυσης (DD-MM).
3. Αρχική ώρα (HH:MM) ή Enter για προεπιλογή.

Το τελικό αρχείο θα αποθηκευτεί στο `FINAL_OUTPUT_PATH`.

## Δομή φακέλων
```
.
├── main.py
├── config.py
├── modules/
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── time_handler.py
│   ├── zero_manager.py
│   ├── zero_loader.py
│   └── output_generator.py
├── CSV/
│   ├── <excel files>
│   ├── parts/
│   └── zero/
└── README.md
```

## Σημειώσεις
- Το πρόγραμμα είναι προσανατολισμένο σε Windows paths. Αν εκτελείτε σε άλλο OS, ενημερώστε το `BASE_PATH` στο `config.py`.
- Το `zero.xlsx` κατεβαίνει αυτόματα αν δεν υπάρχει τοπικά (Supabase URL στο `config.py`).

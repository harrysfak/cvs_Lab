import os
import requests
# Import config με fallback
try:
    from . import config
except ImportError:
    import config


def ensure_zero_file():
    """
    Ελέγχει αν υπάρχει το zero.xlsx.
    Αν δεν υπάρχει → το κατεβάζει από Supabase.
    """
    zero_path = config.ZERO_PATH
    zero_dir = os.path.dirname(zero_path)

    # Αν υπάρχει, τελειώσαμε
    if os.path.exists(zero_path):
        return zero_path

    # Αν δεν υπάρχει → download
    os.makedirs(zero_dir, exist_ok=True)

    print("⬇️  Κατέβασμα zero.xlsx από Supabase...")

    r = requests.get(config.ZERO_REMOTE_URL, timeout=10)
    r.raise_for_status()

    with open(zero_path, "wb") as f:
        f.write(r.content)

    print("✅ zero.xlsx αποθηκεύτηκε")
    return zero_path

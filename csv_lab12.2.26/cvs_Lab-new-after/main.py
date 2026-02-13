"""
Κύριο script για την επεξεργασία δεδομένων γάλακτος
Windows Version
"""
import sys
import os

# Προσθήκη του parent directory στο path για σωστά imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_loader import load_data
from modules.data_processor import process_data
from modules.time_handler import generate_time_metadata
from modules.zero_manager import prepare_zero_data
from modules.output_generator import generate_output


def print_header(text):
    """Τυπώνει formatted header"""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def main():
    """Κύρια συνάρτηση εκτέλεσης"""
    
    print_header("ΣΥΣΤΗΜΑ ΕΠΕΞΕΡΓΑΣΙΑΣ ΔΕΔΟΜΕΝΩΝ ΓΑΛΑΚΤΟΣ - WINDOWS")
    
    try:
        # Βήμα 1: Φόρτωση δεδομένων
        print_header("ΒΗΜΑ 1/5: Φόρτωση δεδομένων από Excel")
        excel_df, csv_first_4, dash_part = load_data()
        print()
        
        # Βήμα 2: Επεξεργασία δεδομένων
        print_header("ΒΗΜΑ 2/5: Επεξεργασία και καθαρισμός δεδομένων")
        processed_df = process_data(excel_df)
        print()
        
        # Βήμα 3: Δημιουργία μεταδεδομένων και χρονικών δεδομένων
        print_header("ΒΗΜΑ 3/5: Δημιουργία μεταδεδομένων")
        metadata = generate_time_metadata(
            len(processed_df), 
            csv_first_4, 
            dash_part
        )
        print()
        
        # Βήμα 4: Προετοιμασία zero data
        print_header("ΒΗΜΑ 4/5: Προετοιμασία zero calibration data")
        zero_dfs = prepare_zero_data(
            len(processed_df),
            metadata['date'][0],
            metadata['zero_times']
        )
        print()
        
        # Βήμα 5: Δημιουργία τελικού output
        print_header("ΒΗΜΑ 5/5: Δημιουργία τελικού output")
        final_path = generate_output(processed_df, metadata, zero_dfs)
        print()
        
        # Επιτυχής ολοκλήρωση
        print_header("ΕΠΕΞΕΡΓΑΣΙΑ ΟΛΟΚΛΗΡΩΘΗΚΕ ΕΠΙΤΥΧΩΣ!")
        print(f"\n📄 Τελικό αρχείο: {final_path}")
        print(f"\n💡 Συμβουλή: Ανοίξτε το αρχείο με Excel ή Notepad++")
        print()
        
        # Προσφορά για άνοιγμα του φακέλου
        try:
            response = input("Θέλετε να ανοίξετε το φάκελο με το αρχείο; (y/n): ")
            if response.lower() == 'y':
                import subprocess
                folder = os.path.dirname(final_path)
                subprocess.Popen(f'explorer "{folder}"')
                print("✅ Ο φάκελος άνοιξε!")
        except Exception as e:
            print(f"⚠️  Δεν μπόρεσε να ανοίξει ο φάκελος: {e}")
        
        return final_path
        
    except FileNotFoundError as e:
        print(f"\n❌ ΣΦΑΛΜΑ: Το αρχείο δεν βρέθηκε")
        print(f"   {e}")
        return None
    except ValueError as e:
        print(f"\n❌ ΣΦΑΛΜΑ: Μη έγκυρη τιμή")
        print(f"   {e}")
        return None
    except KeyboardInterrupt:
        print("\n\n⚠️  Η επεξεργασία ακυρώθηκε από τον χρήστη.")
        return None
    except Exception as e:
        print(f"\n❌ ΑΠΡΟΣΔΟΚΗΤΟ ΣΦΑΛΜΑ: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║          ΣΥΣΤΗΜΑ ΕΠΕΞΕΡΓΑΣΙΑΣ ΔΕΔΟΜΕΝΩΝ ΓΑΛΑΚΤΟΣ                ║")
    print("║                      Windows Edition                              ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    
    result = main()
    
    print("\n" + "=" * 70)
    if result:
        print("🎉 Το πρόγραμμα ολοκληρώθηκε με επιτυχία!")
    else:
        print("⚠️  Το πρόγραμμα τερματίστηκε με σφάλματα.")
    print("=" * 70)
    
    input("\nΠατήστε Enter για έξοδο...")

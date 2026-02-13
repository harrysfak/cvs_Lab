"""
Module για τη διαχείριση χρονικών δεδομένων και μεταδεδομένων δειγμάτων
"""
import datetime
import random
from typing import List, Tuple
# Import config με fallback
try:
    from . import config
except ImportError:
    import config


class TimeHandler:
    """Κλάση για τη διαχείριση χρονικών δεδομένων"""
    
    def __init__(self, num_samples: int):
        self.num_samples = num_samples
    
    def get_analysis_date(self) -> str:
        """
        Ζητά από το χρήστη την ημερομηνία ανάλυσης
        
        Returns:
            str: Ημερομηνία σε μορφή DD/MM/YYYY
        """
        while True:
            date_input = input('Εισαγετε την ημερομηνία ανάλυσης (DD-MM): ')
            try:
                parsed_date = datetime.datetime.strptime(date_input, "%d-%m")
                current_year = datetime.datetime.now().year
                full_date = parsed_date.replace(year=current_year)
                formatted_date = full_date.strftime("%d/%m/%Y")
                print(f"✅ Ημερομηνία: {formatted_date}")
                return formatted_date
            except ValueError:
                print("❌ Λάθος format. Χρησιμοποιήστε DD-MM (π.χ. 01-12)")
    
    def get_initial_time(self) -> str:
        """
        Ζητά από το χρήστη την αρχική ώρα ή χρησιμοποιεί προεπιλογή
        
        Returns:
            str: Ώρα σε μορφή HH:MM
        """
        user_time_input = input(
            f"Δώσε αρχική ώρα ή πάτα Enter για προεπιλογή ({config.DEFAULT_TIME}): "
        )
        
        if not user_time_input:
            random_minutes = random.randint(1, 50)
            default_time = datetime.time(11, random_minutes)
            time_str = default_time.strftime("%H:%M")
            print(f"✅ Χρησιμοποιείται προεπιλεγμένη ώρα: {time_str}")
            return time_str
        
        try:
            if ":" in user_time_input:
                dt = datetime.datetime.strptime(user_time_input, "%H:%M")
            else:
                dt = datetime.datetime.strptime(user_time_input, "%H%M")
            
            time_str = dt.strftime("%H:%M")
            print(f"✅ Αρχική ώρα: {time_str}")
            return time_str
        except ValueError:
            print(f"❌ Λάθος μορφή. Χρησιμοποιείται προεπιλογή: {config.DEFAULT_TIME}")
            return config.DEFAULT_TIME
    
    def generate_sample_ids(self, csv_first_4: str, dash_part: str) -> List[str]:
        """
        Δημιουργεί Sample IDs για όλα τα δείγματα
        
        Args:
            csv_first_4: Τα πρώτα 4 ψηφία
            dash_part: Το τμήμα με παύλα
            
        Returns:
            List[str]: Λίστα με Sample IDs
        """
        sample_ids = [
            f"{csv_first_4}{dash_part} {i+1}" 
            for i in range(self.num_samples)
        ]
        print(f"✅ Δημιουργήθηκαν {len(sample_ids)} Sample IDs")
        return sample_ids
    
    def generate_sample_times(self, initial_time: str) -> Tuple[List[str], List[str]]:
        """
        Δημιουργεί χρονικά timestamps για δείγματα και zero blocks
        
        Args:
            initial_time: Αρχική ώρα σε μορφή HH:MM
            
        Returns:
            Tuple[List[str], List[str]]: (sample_times, zero_times)
        """
        current_time = datetime.datetime.strptime(
            initial_time, "%H:%M"
        ).replace(year=2000, month=1, day=1)
        
        sample_times = []
        zero_times = []
        
        num_full_batches = self.num_samples // config.BATCH_SIZE
        remaining_samples = self.num_samples % config.BATCH_SIZE
        
        # Επεξεργασία πλήρων batches
        for _ in range(num_full_batches):
            # Χρόνοι για δείγματα
            for _ in range(config.BATCH_SIZE):
                current_time += datetime.timedelta(seconds=config.T_SAMPLE_INCREMENT)
                sample_times.append(current_time.strftime("%H:%M"))
            
            # Χρόνοι για zero block
            for _ in range(config.ZERO_BLOCK_ROWS):
                current_time += datetime.timedelta(seconds=config.T_ZERO_INCREMENT)
                zero_times.append(current_time.strftime("%H:%M"))
        
        # Επεξεργασία υπολοίπων δειγμάτων
        for _ in range(remaining_samples):
            current_time += datetime.timedelta(seconds=config.T_SAMPLE_INCREMENT)
            sample_times.append(current_time.strftime("%H:%M"))
        
        print(f"✅ Δημιουργήθηκαν {len(sample_times)} sample times και "
              f"{len(zero_times)} zero times")
        
        return sample_times, zero_times


class MetadataGenerator:
    """Κλάση για τη δημιουργία μεταδεδομένων"""
    
    @staticmethod
    def generate_metadata(num_samples: int, date: str) -> dict:
        """
        Δημιουργεί όλα τα μεταδεδομένα για τα δείγματα
        
        Args:
            num_samples: Αριθμός δειγμάτων
            date: Ημερομηνία ανάλυσης
            
        Returns:
            dict: Dictionary με metadata
        """
        return {
            'product': [config.DEFAULT_PRODUCT] * num_samples,
            'rep': [config.DEFAULT_REP] * num_samples,
            'date': [date] * num_samples,
            'remark': [""] * num_samples
        }


def generate_time_metadata(df_length: int, csv_first_4: str, 
                          dash_part: str) -> dict:
    """
    Wrapper function για δημιουργία όλων των χρονικών μεταδεδομένων
    
    Args:
        df_length: Αριθμός γραμμών στο DataFrame
        csv_first_4: Πρώτα 4 ψηφία
        dash_part: Dash part
        
    Returns:
        dict: Dictionary με όλα τα μεταδεδομένα
    """
    time_handler = TimeHandler(df_length)
    
    # Λήψη ημερομηνίας και ώρας
    date = time_handler.get_analysis_date()
    initial_time = time_handler.get_initial_time()
    
    # Δημιουργία IDs και χρόνων
    sample_ids = time_handler.generate_sample_ids(csv_first_4, dash_part)
    sample_times, zero_times = time_handler.generate_sample_times(initial_time)
    
    # Δημιουργία υπόλοιπων metadata
    metadata = MetadataGenerator.generate_metadata(df_length, date)
    
    return {
        'sample_ids': sample_ids,
        'sample_times': sample_times,
        'zero_times': zero_times,
        **metadata
    }


if __name__ == "__main__":
    # Test του module
    print("Testing TimeHandler...")
    handler = TimeHandler(100)
    date = handler.get_analysis_date()
    initial_time = handler.get_initial_time()
    sample_ids = handler.generate_sample_ids("1234", "-56")
    sample_times, zero_times = handler.generate_sample_times(initial_time)
    print(f"Sample IDs: {len(sample_ids)}")
    print(f"Sample times: {len(sample_times)}")
    print(f"Zero times: {len(zero_times)}")

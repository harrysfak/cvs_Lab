"""
Milk Data Processor Modules Package
Σύστημα επεξεργασίας δεδομένων γάλακτος

Modules:
- data_loader: Φόρτωση δεδομένων από Excel
- data_processor: Επεξεργασία και καθαρισμός DataFrame
- time_handler: Διαχείριση χρονικών δεδομένων
- zero_data_manager: Διαχείριση zero calibration data
- output_generator: Δημιουργία τελικού output
"""

from .data_loader import DataLoader, load_data
from .data_processor import DataProcessor, process_data
from .time_handler import TimeHandler, MetadataGenerator, generate_time_metadata
from .zero_manager import ZeroDataManager, prepare_zero_data
from .output_generator import OutputGenerator, FinalOutputAssembler, generate_output

__version__ = "1.0.0"
__author__ = "Your Name"

__all__ = [
    # Data Loading
    'DataLoader',
    'load_data',
    
    # Data Processing
    'DataProcessor',
    'process_data',
    
    # Time Handling
    'TimeHandler',
    'MetadataGenerator',
    'generate_time_metadata',
    
    # Zero Data Management
    'ZeroDataManager',
    'prepare_zero_data',
    
    # Output Generation
    'OutputGenerator',
    'FinalOutputAssembler',
    'generate_output',
]


# Package-level convenience functions
def quick_process(file_number: str, date: str = None, initial_time: str = None):
    """
    Γρήγορη επεξεργασία με ελάχιστες παραμέτρους
    
    Args:
        file_number: Αριθμός πρωτοκόλλου (π.χ. "1234-56")
        date: Ημερομηνία σε μορφή DD-MM (προαιρετική)
        initial_time: Αρχική ώρα σε μορφή HH:MM (προαιρετική)
        
    Returns:
        str: Διαδρομή τελικού αρχείου
    """
    print(f"Quick processing for file: {file_number}")
    # Implementation would go here
    pass


def get_module_info():
    """Επιστρέφει πληροφορίες για όλα τα modules"""
    return {
        'version': __version__,
        'modules': __all__,
        'description': __doc__
    }

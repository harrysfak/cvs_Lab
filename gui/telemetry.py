import os
import datetime
from datetime import *
import json

class UsageTelemetry:
    """Κλάση για tracking usage statistics (local only - για maintenance)"""

    def __init__(self):
        self.telemetry_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'usage_stats.json'
        )
        self.stats = self._load_stats()

    def _load_stats(self):
        """Φορτώνει τα statistics από το αρχείο"""
        if os.path.exists(self.telemetry_file):
            try:
                with open(self.telemetry_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._create_default_stats()
        return self._create_default_stats()

    def _create_default_stats(self):
        """Δημιουργεί default structure"""
        return {
            'total_files_processed': 0,
            'total_sessions': 0,
            'last_used': None,
            'first_used': datetime.now().isoformat(),
            'processing_history': [],
            'errors': [],
            'app_version': 'v1.3'
        }

    def _save_stats(self):
        """Αποθηκεύει τα statistics"""
        try:
            with open(self.telemetry_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=4)
        except Exception as e:
            print(f"Warning: Could not save telemetry: {e}")

    def record_session_start(self):
        """Καταγράφει έναρξη session"""
        self.stats['total_sessions'] += 1
        self.stats['last_used'] = datetime.now().isoformat()
        self._save_stats()

    def record_file_processed(self, filename, samples_count, duration_seconds=None):
        """Καταγράφει επεξεργασία αρχείου"""
        self.stats['total_files_processed'] += 1

        record = {
            'timestamp': datetime.now().isoformat(),
            'filename': filename,
            'samples': samples_count,
            'duration_sec': duration_seconds
        }

        self.stats['processing_history'].append(record)

        # Keep only last 100 records
        if len(self.stats['processing_history']) > 100:
            self.stats['processing_history'] = self.stats['processing_history'][-100:]

        self._save_stats()

    def record_error(self, error_message):
        """Καταγράφει σφάλμα"""
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'error': str(error_message)[:200]  # Limit size
        }

        self.stats['errors'].append(error_record)

        # Keep only last 50 errors
        if len(self.stats['errors']) > 50:
            self.stats['errors'] = self.stats['errors'][-50:]

        self._save_stats()

    def get_summary(self):
        """Επιστρέφει summary statistics"""
        today = datetime.now().date()

        # Count today's files
        today_files = sum(
            1 for record in self.stats['processing_history']
            if datetime.fromisoformat(record['timestamp']).date() == today
        )

        # Count this week's files
        from datetime import timedelta
        week_ago = today - timedelta(days=7)
        week_files = sum(
            1 for record in self.stats['processing_history']
            if datetime.fromisoformat(record['timestamp']).date() >= week_ago
        )

        return {
            'total_files': self.stats['total_files_processed'],
            'total_sessions': self.stats['total_sessions'],
            'today_files': today_files,
            'week_files': week_files,
            'last_used': self.stats['last_used'],
            'first_used': self.stats['first_used'],
        'recent_errors': len(self.stats['errors'])
        }

"""
Tabs Module
Contains all tab components for the main application
"""

from .load_tab import LoadTab
from .settings_tab import SettingsTab
from .process_tab import ProcessTab
from .results_tab import ResultsTab

__all__ = [
    'LoadTab',
    'SettingsTab',
    'ProcessTab',
    'ResultsTab'
]
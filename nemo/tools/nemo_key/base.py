"""
NemoKey - Base class for all hotkey implementations

Every key (RIGHT SHIFT, RIGHT ALT, etc.) extends this base class.
Provides lifecycle hooks: on_press, on_hold, on_release, on_execute
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import time


class NemoKey(ABC):
    """Abstract base class for all Nemo hotkeys"""
    
    def __init__(self, key_name: str, key_combo: str, description: str):
        """
        Initialize a Nemo key
        
        Args:
            key_name: Display name (e.g., "Speech-to-Text")
            key_combo: Keyboard combo (e.g., "right shift")
            description: What this key does
        """
        self.key_name = key_name
        self.key_combo = key_combo
        self.description = description
        self.enabled = True
        self.config = {}
        self.last_execution_time = 0
        self.execution_count = 0
    
    @abstractmethod
    def on_press(self) -> None:
        """Called when key is first pressed"""
        pass
    
    @abstractmethod
    def on_hold(self, duration: float) -> None:
        """Called while key is held down (duration in seconds)"""
        pass
    
    @abstractmethod
    def on_release(self, total_duration: float) -> Any:
        """Called when key is released (total_duration in seconds)"""
        pass
    
    def execute(self) -> Any:
        """Execute key logic (wrapper for lifecycle)"""
        self.execution_count += 1
        self.last_execution_time = time.time()
        return None
    
    def enable(self) -> None:
        """Enable this key"""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable this key"""
        self.enabled = False
    
    def set_config(self, config_dict: Dict[str, Any]) -> None:
        """Update key configuration"""
        self.config.update(config_dict)
    
    def get_status(self) -> Dict[str, Any]:
        """Return key status information"""
        return {
            'name': self.key_name,
            'combo': self.key_combo,
            'enabled': self.enabled,
            'executions': self.execution_count,
            'last_executed': self.last_execution_time,
        }
    
    def __repr__(self):
        return f"<NemoKey {self.key_name} ({self.key_combo})>"

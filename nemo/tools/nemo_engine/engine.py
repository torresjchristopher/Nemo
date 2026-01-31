"""
NemoEngine - Core orchestrator and hotkey registry

Manages all keys, handles keyboard events, routes to appropriate key handlers.
This is the heart of Nemo - PUBLIC and auditable.
"""

from typing import Dict, List, Optional, Callable
from ..nemo_key import NemoKey


class NemoEngine:
    """
    Main Nemo orchestrator
    
    - Registers and manages all hotkeys
    - Routes keyboard events to appropriate keys
    - Maintains global configuration
    """
    
    def __init__(self):
        """Initialize Nemo engine"""
        self.keys: Dict[str, NemoKey] = {}
        self.enabled = True
        self.version = "1.0.0"
        self.global_config = {}
    
    def register_key(self, key: NemoKey) -> None:
        """
        Register a hotkey
        
        Args:
            key: NemoKey instance to register
        """
        self.keys[key.key_combo] = key
        print(f"[NEMO] Registered: {key.key_name} ({key.key_combo})")
    
    def unregister_key(self, key_combo: str) -> bool:
        """Unregister a hotkey"""
        if key_combo in self.keys:
            del self.keys[key_combo]
            return True
        return False
    
    def get_key(self, key_combo: str) -> Optional[NemoKey]:
        """Get a registered key"""
        return self.keys.get(key_combo)
    
    def get_all_keys(self) -> List[NemoKey]:
        """Get all registered keys"""
        return list(self.keys.values())
    
    def enable_all(self) -> None:
        """Enable all keys"""
        self.enabled = True
        for key in self.keys.values():
            key.enable()
    
    def disable_all(self) -> None:
        """Disable all keys"""
        self.enabled = False
        for key in self.keys.values():
            key.disable()
    
    def enable_key(self, key_combo: str) -> bool:
        """Enable a specific key"""
        key = self.get_key(key_combo)
        if key:
            key.enable()
            return True
        return False
    
    def disable_key(self, key_combo: str) -> bool:
        """Disable a specific key"""
        key = self.get_key(key_combo)
        if key:
            key.disable()
            return True
        return False
    
    def on_key_press(self, key_combo: str) -> None:
        """Handle key press event"""
        key = self.get_key(key_combo)
        if key and key.enabled and self.enabled:
            key.on_press()
    
    def on_key_hold(self, key_combo: str, duration: float) -> None:
        """Handle key hold event"""
        key = self.get_key(key_combo)
        if key and key.enabled and self.enabled:
            key.on_hold(duration)
    
    def on_key_release(self, key_combo: str, total_duration: float):
        """Handle key release event"""
        key = self.get_key(key_combo)
        if key and key.enabled and self.enabled:
            return key.on_release(total_duration)
        return None
    
    def get_status(self) -> dict:
        """Return Nemo engine status"""
        return {
            'version': self.version,
            'enabled': self.enabled,
            'keys_registered': len(self.keys),
            'keys': [k.get_status() for k in self.keys.values()],
        }
    
    def __repr__(self):
        return f"<NemoEngine v{self.version} - {len(self.keys)} keys>"

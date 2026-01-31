"""
KeyboardListener - Hotkey detection and routing

Detects hotkey combinations (RIGHT SHIFT, RIGHT ALT, RIGHT ALT + LEFT/RIGHT/UP)
Routes events to NemoEngine for key lifecycle management.
"""

import keyboard
import threading
import time
from typing import Dict, Callable, Optional
from nemo.tools import NemoEngine


class KeyboardListener:
    """
    System-level keyboard listener for Nemo hotkeys
    
    Detects:
    - RIGHT SHIFT (single key)
    - RIGHT ALT (single key)
    - RIGHT ALT + LEFT (combo)
    - RIGHT ALT + RIGHT (combo)
    - RIGHT ALT + UP (combo)
    
    Routes to NemoEngine for handling.
    """
    
    def __init__(self, engine: NemoEngine):
        """
        Initialize keyboard listener
        
        Args:
            engine: NemoEngine instance to route events to
        """
        self.engine = engine
        self.listening = False
        self.thread = None
        
        # Track key states (for combo detection)
        self.right_shift_pressed = False
        self.right_alt_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        
        # Track press times (for duration calculation)
        self.key_press_times: Dict[str, float] = {}
        self.combo_start_time: Optional[float] = None
    
    def start(self) -> None:
        """Start listening for hotkeys"""
        if self.listening:
            return
        
        self.listening = True
        print("[KEYBOARD] Listener started")
        
        # Hook keyboard events
        keyboard.on_press(self._on_key_press)
        keyboard.on_release(self._on_key_release)
    
    def stop(self) -> None:
        """Stop listening"""
        self.listening = False
        keyboard.unhook_all()
        print("[KEYBOARD] Listener stopped")
    
    def _on_key_press(self, event) -> None:
        """Handle key press event"""
        if not self.listening:
            return
        
        key = event.name.lower()
        
        # Track individual keys
        if key == 'right shift':
            self.right_shift_pressed = True
            self.key_press_times['right shift'] = time.time()
            self.engine.on_key_press('right shift')
        
        elif key == 'right alt':
            self.right_alt_pressed = True
            self.key_press_times['right alt'] = time.time()
            self.combo_start_time = time.time()
        
        # Combo modifier keys (when right alt is held)
        elif self.right_alt_pressed:
            if key == 'left':
                self.left_pressed = True
                self.key_press_times['right alt + left'] = time.time()
                self.engine.on_key_press('right alt + left')
            
            elif key == 'right':
                self.right_pressed = True
                self.key_press_times['right alt + right'] = time.time()
                self.engine.on_key_press('right alt + right')
            
            elif key == 'up':
                self.up_pressed = True
                self.key_press_times['right alt + up'] = time.time()
                self.engine.on_key_press('right alt + up')
    
    def _on_key_release(self, event) -> None:
        """Handle key release event"""
        if not self.listening:
            return
        
        key = event.name.lower()
        
        # RIGHT SHIFT release
        if key == 'right shift' and self.right_shift_pressed:
            self.right_shift_pressed = False
            duration = time.time() - self.key_press_times.get('right shift', time.time())
            self.engine.on_key_release('right shift', duration)
            del self.key_press_times['right shift']
        
        # RIGHT ALT release (may have combos)
        elif key == 'right alt' and self.right_alt_pressed:
            self.right_alt_pressed = False
            
            # Check which combo was active
            if self.left_pressed:
                self.left_pressed = False
                duration = time.time() - self.key_press_times.get('right alt + left', time.time())
                self.engine.on_key_release('right alt + left', duration)
                del self.key_press_times['right alt + left']
            
            elif self.right_pressed:
                self.right_pressed = False
                duration = time.time() - self.key_press_times.get('right alt + right', time.time())
                self.engine.on_key_release('right alt + right', duration)
                del self.key_press_times['right alt + right']
            
            elif self.up_pressed:
                self.up_pressed = False
                duration = time.time() - self.key_press_times.get('right alt + up', time.time())
                self.engine.on_key_release('right alt + up', duration)
                del self.key_press_times['right alt + up']
            
            else:
                # Solo RIGHT ALT
                duration = time.time() - self.key_press_times.get('right alt', time.time())
                self.engine.on_key_release('right alt', duration)
            
            del self.key_press_times['right alt']
            self.combo_start_time = None
        
        # Combo key releases (left/right/up)
        elif key == 'left' and self.left_pressed:
            self.left_pressed = False
        
        elif key == 'right' and self.right_pressed:
            self.right_pressed = False
        
        elif key == 'up' and self.up_pressed:
            self.up_pressed = False
    
    def get_status(self) -> dict:
        """Return listener status"""
        return {
            'listening': self.listening,
            'keys_pressed': {
                'right_shift': self.right_shift_pressed,
                'right_alt': self.right_alt_pressed,
                'left': self.left_pressed,
                'right': self.right_pressed,
                'up': self.up_pressed,
            }
        }

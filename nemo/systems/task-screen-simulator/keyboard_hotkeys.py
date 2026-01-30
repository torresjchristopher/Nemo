"""
Keyboard hotkeys using `keyboard` library for better Windows system-level capture.

The pynput library has issues capturing some keys like RIGHT SHIFT on Windows.
The `keyboard` library has better access to system hotkeys.
"""

import logging
import threading
import time
from typing import Optional, Callable, Dict
from dataclasses import dataclass
from enum import Enum

try:
    import keyboard
except ImportError:
    keyboard = None


class HotkeyMode(Enum):
    """Hotkey activation mode."""
    TAP = "tap"
    HOLD = "hold"


@dataclass
class HotkeyEvent:
    """A hotkey event."""
    name: str  # "tts", "gemini", "rewind", "forward"
    mode: HotkeyMode
    timestamp: float


class KeyboardHotkeyListener:
    """
    Listen for hotkeys using the `keyboard` library.
    Better system-level access on Windows than pynput.
    """
    
    TAP_THRESHOLD_MS = 200
    
    def __init__(self):
        """Initialize hotkey listener."""
        self.logger = logging.getLogger(__name__)
        
        if keyboard is None:
            self.logger.warning("keyboard library not installed")
            return
        
        # Callbacks
        self.callbacks: Dict[str, Callable[[HotkeyEvent], None]] = {
            'tts_tap': None,
            'tts_hold': None,
            'gemini_tap': None,
            'gemini_hold': None,
            'rewind': None,
            'forward': None,
        }
        
        # Key press tracking
        self.key_press_times: Dict[str, float] = {}
        self.running = False
        self.listen_thread: Optional[threading.Thread] = None
        
    def register_callback(self, action: str, callback: Callable[[HotkeyEvent], None]):
        """Register callback for hotkey action."""
        if action in self.callbacks:
            self.callbacks[action] = callback
            self.logger.info(f"Registered hotkey callback: {action}")
        else:
            self.logger.warning(f"Unknown hotkey action: {action}")
    
    def start(self):
        """Start listening for hotkeys."""
        if self.running or keyboard is None:
            return
        
        self.running = True
        self.logger.info("Starting keyboard hotkey listener")
        
        try:
            # Register hotkeys using keyboard library
            # RIGHT SHIFT for TTS
            keyboard.on_press_key('shift', self._on_right_shift_press, suppress=False)
            keyboard.on_release_key('shift', self._on_right_shift_release, suppress=False)
            
            # RIGHT ALT for Gemini (alt_r)
            keyboard.on_press_key('alt', self._on_right_alt_press, suppress=False)
            keyboard.on_release_key('alt', self._on_right_alt_release, suppress=False)
            
            # Arrow keys for rewind/forward
            keyboard.on_press_key('left', self._on_left_arrow, suppress=False)
            keyboard.on_press_key('right', self._on_right_arrow, suppress=False)
            
            self.logger.info("Keyboard hotkeys registered")
            
        except Exception as e:
            self.logger.error(f"Failed to register hotkeys: {e}")
            self.running = False
    
    def stop(self):
        """Stop listening for hotkeys."""
        self.running = False
        if keyboard is not None:
            try:
                keyboard.unhook_all()
            except:
                pass
        self.logger.info("Keyboard hotkey listener stopped")
    
    def _on_right_shift_press(self, event):
        """Handle RIGHT SHIFT press."""
        if not self.running:
            return
        
        # Check if it's actually RIGHT SHIFT (not left shift)
        if event.name == 'shift right' or (hasattr(event, 'is_keypad') and not event.is_keypad):
            print("[DEBUG] RIGHT SHIFT PRESSED", flush=True)
            self.key_press_times['tts'] = time.time()
    
    def _on_right_shift_release(self, event):
        """Handle RIGHT SHIFT release."""
        if not self.running or 'tts' not in self.key_press_times:
            return
        
        if event.name == 'shift right' or (hasattr(event, 'is_keypad') and not event.is_keypad):
            press_time = self.key_press_times.pop('tts', time.time())
            duration_ms = (time.time() - press_time) * 1000
            
            print(f"[DEBUG] RIGHT SHIFT RELEASED after {duration_ms:.0f}ms", flush=True)
            
            # Trigger callback
            if duration_ms < self.TAP_THRESHOLD_MS:
                self._trigger_callback('tts_tap')
            else:
                self._trigger_callback('tts_hold')
    
    def _on_right_alt_press(self, event):
        """Handle RIGHT ALT press."""
        if not self.running:
            return
        
        if event.name == 'alt right':
            print("[DEBUG] RIGHT ALT PRESSED", flush=True)
            self.key_press_times['gemini'] = time.time()
    
    def _on_right_alt_release(self, event):
        """Handle RIGHT ALT release."""
        if not self.running or 'gemini' not in self.key_press_times:
            return
        
        if event.name == 'alt right':
            press_time = self.key_press_times.pop('gemini', time.time())
            duration_ms = (time.time() - press_time) * 1000
            
            print(f"[DEBUG] RIGHT ALT RELEASED after {duration_ms:.0f}ms", flush=True)
            
            # Trigger callback
            if duration_ms < self.TAP_THRESHOLD_MS:
                self._trigger_callback('gemini_tap')
            else:
                self._trigger_callback('gemini_hold')
    
    def _on_left_arrow(self, event):
        """Handle LEFT ARROW for rewind (if RIGHT ALT held)."""
        if not self.running or 'gemini' not in self.key_press_times:
            return
        
        if event.name == 'left':
            print("[DEBUG] LEFT ARROW + RIGHT ALT (REWIND)", flush=True)
            self._trigger_callback('rewind')
    
    def _on_right_arrow(self, event):
        """Handle RIGHT ARROW for forward (if RIGHT ALT held)."""
        if not self.running or 'gemini' not in self.key_press_times:
            return
        
        if event.name == 'right':
            print("[DEBUG] RIGHT ARROW + RIGHT ALT (FORWARD)", flush=True)
            self._trigger_callback('forward')
    
    def _trigger_callback(self, action: str):
        """Trigger a registered callback."""
        callback = self.callbacks.get(action)
        if callback is None:
            print(f"[DEBUG] No callback for {action}", flush=True)
            return
        
        try:
            event = HotkeyEvent(
                name=action,
                mode=HotkeyMode.TAP if 'tap' in action else HotkeyMode.HOLD,
                timestamp=time.time()
            )
            callback(event)
        except Exception as e:
            self.logger.error(f"Error in hotkey callback {action}: {e}")
            import traceback
            traceback.print_exc()


__all__ = ['KeyboardHotkeyListener', 'HotkeyEvent', 'HotkeyMode']

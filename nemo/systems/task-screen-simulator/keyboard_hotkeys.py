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

# Import v3 rewind engine for keystroke tracking
try:
    from .rewind_engine_v3 import RewindEngineV3, get_rewind_engine
except ImportError:
    RewindEngineV3 = None
    get_rewind_engine = None


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
            'tts_hold_start': None,
            'tts_hold_end': None,
            'gemini_tap': None,
            'gemini_hold_start': None,
            'gemini_hold_end': None,
            'rewind_start': None,  # RIGHT ALT + LEFT - start rewinding
            'rewind_stop': None,   # RIGHT ALT released - stop rewinding
            'forward': None,
            'agent_synthesis': None,  # RIGHT ALT + UP ARROW
        }
        
        # Key press tracking
        self.key_press_times: Dict[str, float] = {}
        self.keys_currently_held: set = set()  # Track held keys for combos
        self.running = False
        self.listen_thread: Optional[threading.Thread] = None
        self._rewind_start_time = None
        
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
            # Use keyboard.hook() to detect key press/release for hold behavior
            keyboard.hook(self._on_keyboard_event)
            
            self.logger.info("Keyboard hotkeys registered")
            print("[SUCCESS] Keyboard hotkeys registered!", flush=True)
            
        except Exception as e:
            self.logger.error(f"Failed to register hotkeys: {e}")
            print(f"[ERROR] Hotkey registration failed: {e}", flush=True)
            self.running = False
    
    def _on_keyboard_event(self, event):
        """Handle all keyboard events to detect press/release."""
        if not self.running:
            return
        
        # Track key press/release
        key_name = event.name.lower() if hasattr(event, 'name') else str(event)
        
        # TRACK ALL KEYS FOR REWIND (pre-computes reverse instructions)
        if get_rewind_engine is not None and event.event_type == 'down':
            rewind = get_rewind_engine()
            rewind.track_keystroke(key_name)
        
        if event.event_type == 'down':
            # Debounce: ignore repeat events, only fire on first press
            if key_name not in self.key_press_times:
                self.key_press_times[key_name] = time.time()
                self.keys_currently_held.add(key_name)
                
                # RIGHT SHIFT pressed
                if key_name == 'right shift':
                    print("[DEBUG] RIGHT SHIFT PRESSED (DOWN)", flush=True)
                    self._trigger_callback('tts_hold_start')
                
                # RIGHT ALT pressed (check for combos)
                elif key_name == 'right alt':
                    print("[DEBUG] RIGHT ALT PRESSED (DOWN)", flush=True)
                    self._trigger_callback('gemini_hold_start')
                    # Start rewind if needed
                    if get_rewind_engine:
                        rewind = get_rewind_engine()
                        self._rewind_start_time = time.time()
                
                # Check for RIGHT ALT + arrow combos
                elif key_name == 'left' and 'right alt' in self.keys_currently_held:
                    print("[DEBUG] RIGHT ALT + LEFT ARROW - REWIND START!", flush=True)
                    self._trigger_callback('rewind_start')
                
                elif key_name == 'right' and 'right alt' in self.keys_currently_held:
                    print("[DEBUG] RIGHT ALT + RIGHT ARROW - FORWARD!", flush=True)
                    self._trigger_callback('forward')
                
                # NEW: RIGHT ALT + UP ARROW for agent synthesis
                elif key_name == 'up' and 'right alt' in self.keys_currently_held:
                    print("[DEBUG] RIGHT ALT + UP ARROW - AGENT SYNTHESIS", flush=True)
                    self._trigger_callback('agent_synthesis')
        
        elif event.event_type == 'up':
            # Track key release
            if key_name in self.keys_currently_held:
                self.keys_currently_held.discard(key_name)
            
            # RIGHT SHIFT released
            if key_name == 'right shift' and 'right shift' in self.key_press_times:
                held_time = time.time() - self.key_press_times['right shift']
                del self.key_press_times['right shift']
                print(f"[DEBUG] RIGHT SHIFT RELEASED (UP, held {held_time:.2f}s)", flush=True)
                self._trigger_callback('tts_hold_end')
            
            # RIGHT ALT released
            elif key_name == 'right alt' and 'right alt' in self.key_press_times:
                held_time = time.time() - self.key_press_times['right alt']
                del self.key_press_times['right alt']
                print(f"[DEBUG] RIGHT ALT RELEASED (UP, held {held_time:.2f}s)", flush=True)
                self._trigger_callback('gemini_hold_end')
                self._trigger_callback('rewind_stop')
            
            # LEFT ARROW released (stop rewind)
            elif key_name == 'left' and 'right alt' in self.keys_currently_held:
                # Rewind is still active while RIGHT ALT is held
                pass
    
    def stop(self):
        """Stop listening for hotkeys."""
        self.running = False
        if keyboard is not None:
            try:
                keyboard.unhook_all()
            except:
                pass
        self.logger.info("Keyboard hotkey listener stopped")
    
    def _on_right_shift_press(self):
        """Handle RIGHT SHIFT press."""
        if not self.running:
            return
        
        print("[DEBUG] RIGHT SHIFT PRESSED", flush=True)
        self._trigger_callback('tts_tap')
    
    def _on_right_alt_press(self):
        """Handle RIGHT ALT press."""
        if not self.running:
            return
        
        print("[DEBUG] RIGHT ALT PRESSED", flush=True)
        self._trigger_callback('gemini_tap')
    
    def _on_left_arrow(self):
        """Handle LEFT ARROW for rewind (with RIGHT ALT)."""
        if not self.running:
            return
        
        print("[DEBUG] REWIND (RIGHT ALT + LEFT)", flush=True)
        self._trigger_callback('rewind')
    
    def _on_right_arrow(self):
        """Handle RIGHT ARROW for forward (with RIGHT ALT)."""
        if not self.running:
            return
        
        print("[DEBUG] FORWARD (RIGHT ALT + RIGHT)", flush=True)
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

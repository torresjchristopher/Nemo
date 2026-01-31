"""
REWIND ENGINE v3 - Pre-Computed Reverse Instructions

ARCHITECTURE:
Each keystroke is tracked WITH its pre-computed reverse instruction.
On RIGHT ALT + LEFT held, fire reverse instructions in reverse order.
Maintains 5-minute rolling window of keystrokes.

Every key press has an inverse. We compute it immediately.
When rewind fires, we just execute the pre-computed stack in reverse.
"""

from collections import deque
from typing import Tuple, Optional, List
import keyboard
import time

class KeystrokeEvent:
    """
    A single keystroke with its pre-computed reverse instruction.
    """
    
    def __init__(self, key: str):
        self.key = key
        self.timestamp = time.time()
        self.reverse_instruction = self._derive_reverse(key)
    
    def _derive_reverse(self, key: str) -> Tuple[str, Optional[int]]:
        """
        Derive the reverse instruction for this keystroke.
        Returns: (action, args)
        
        This is the INTELLIGENCE - understanding what reverses what.
        """
        
        # REVERSE INSTRUCTION DICTIONARY
        reverse_map = {
            # Single character typing
            'a': ('backspace', 1),
            'b': ('backspace', 1),
            'c': ('backspace', 1),
            'd': ('backspace', 1),
            'e': ('backspace', 1),
            'f': ('backspace', 1),
            'g': ('backspace', 1),
            'h': ('backspace', 1),
            'i': ('backspace', 1),
            'j': ('backspace', 1),
            'k': ('backspace', 1),
            'l': ('backspace', 1),
            'm': ('backspace', 1),
            'n': ('backspace', 1),
            'o': ('backspace', 1),
            'p': ('backspace', 1),
            'q': ('backspace', 1),
            'r': ('backspace', 1),
            's': ('backspace', 1),
            't': ('backspace', 1),
            'u': ('backspace', 1),
            'v': ('backspace', 1),
            'w': ('backspace', 1),
            'x': ('backspace', 1),
            'y': ('backspace', 1),
            'z': ('backspace', 1),
            
            # Numbers
            '0': ('backspace', 1),
            '1': ('backspace', 1),
            '2': ('backspace', 1),
            '3': ('backspace', 1),
            '4': ('backspace', 1),
            '5': ('backspace', 1),
            '6': ('backspace', 1),
            '7': ('backspace', 1),
            '8': ('backspace', 1),
            '9': ('backspace', 1),
            
            # Symbols
            ' ': ('backspace', 1),  # Space
            '!': ('backspace', 1),
            '@': ('backspace', 1),
            '#': ('backspace', 1),
            '$': ('backspace', 1),
            '%': ('backspace', 1),
            '^': ('backspace', 1),
            '&': ('backspace', 1),
            '*': ('backspace', 1),
            '(': ('backspace', 1),
            ')': ('backspace', 1),
            '-': ('backspace', 1),
            '_': ('backspace', 1),
            '=': ('backspace', 1),
            '+': ('backspace', 1),
            '[': ('backspace', 1),
            ']': ('backspace', 1),
            '{': ('backspace', 1),
            '}': ('backspace', 1),
            ';': ('backspace', 1),
            ':': ('backspace', 1),
            "'": ('backspace', 1),
            '"': ('backspace', 1),
            ',': ('backspace', 1),
            '<': ('backspace', 1),
            '.': ('backspace', 1),
            '>': ('backspace', 1),
            '/': ('backspace', 1),
            '?': ('backspace', 1),
            '\\': ('backspace', 1),
            '|': ('backspace', 1),
            '`': ('backspace', 1),
            '~': ('backspace', 1),
            
            # Navigation
            'right': ('left', 1),
            'left': ('right', 1),
            'up': ('down', 1),
            'down': ('up', 1),
            
            # Deletion
            'backspace': ('undo', None),  # Use Ctrl+Z
            'delete': ('undo', None),
            
            # Editing
            'enter': ('undo', None),  # Line break - use Ctrl+Z
            'tab': ('backspace_spaces', 4),
            
            # Undo/Redo
            'ctrl+z': ('redo', None),  # Reverse of undo is redo
            'ctrl+y': ('undo', None),  # Reverse of redo is undo
        }
        
        return reverse_map.get(key, ('noop', None))
    
    def __repr__(self):
        reverse_action, args = self.reverse_instruction
        return f"Key({self.key}) → Reverse({reverse_action})"


class RewindEngineV3:
    """
    Pre-computed reverse instruction rewind engine.
    
    Maintains a 5-minute rolling window of keystrokes.
    Each keystroke has its reverse pre-computed.
    On RIGHT ALT + LEFT held, fires reverses in reverse order.
    """
    
    # 5 minutes at ~200 WPM = ~1667 keystrokes, let's do 5000 to be safe
    MAX_HISTORY = 5000
    
    def __init__(self):
        # Stack of KeystrokeEvent objects
        self.keystroke_stack = deque(maxlen=self.MAX_HISTORY)
        self.rewinding = False
        self.rewind_index = 0  # How many we've reversed
    
    def track_keystroke(self, key: str):
        """
        Track a keystroke. Pre-computes its reverse immediately.
        """
        if key in ('right shift', 'right alt', 'escape', 'f1', 'f2', 'f3', 'f4', 'f5'):
            return  # Ignore hotkeys and special keys
        
        event = KeystrokeEvent(key)
        self.keystroke_stack.append(event)
        # print(f"[TRACK] {event} | Stack: {len(self.keystroke_stack)}")
    
    def rewind_continuous(self, duration_seconds: float = None):
        """
        CONTINUOUS REWIND: Execute reverse instructions until duration ends or stack empty.
        
        Called while RIGHT ALT + LEFT is HELD.
        Fires one reverse instruction per call for smooth animation.
        
        Args:
            duration_seconds: How long to rewind (None = rewind all)
        """
        if not self.keystroke_stack:
            return False  # Nothing to rewind
        
        if not self.rewinding:
            self.rewinding = True
            self.rewind_index = 0
            print(f"[REWIND] Starting - {len(self.keystroke_stack)} keystrokes to reverse")
        
        # Pop one keystroke from top
        if len(self.keystroke_stack) > 0:
            event = self.keystroke_stack.pop()
            reverse_action, args = event.reverse_instruction
            
            # Execute the reverse
            self._execute_reverse_action(reverse_action, args)
            self.rewind_index += 1
            
            # print(f"[REWIND] {self.rewind_index}: {event.key} → {reverse_action}")
            return True
        
        return False
    
    def rewind_stop(self):
        """Stop rewinding"""
        if self.rewinding:
            print(f"[REWIND] Stopped after {self.rewind_index} reversals")
            self.rewinding = False
    
    def _execute_reverse_action(self, action: str, args: Optional[int]):
        """
        Execute a single reverse action.
        
        Called for each keystroke during rewind.
        """
        try:
            if action == 'backspace':
                for _ in range(args or 1):
                    keyboard.press_and_release('backspace')
            
            elif action == 'left':
                for _ in range(args or 1):
                    keyboard.press_and_release('left')
            
            elif action == 'right':
                for _ in range(args or 1):
                    keyboard.press_and_release('right')
            
            elif action == 'up':
                for _ in range(args or 1):
                    keyboard.press_and_release('up')
            
            elif action == 'down':
                for _ in range(args or 1):
                    keyboard.press_and_release('down')
            
            elif action == 'backspace_spaces':
                for _ in range(args or 4):
                    keyboard.press_and_release('backspace')
            
            elif action == 'undo':
                keyboard.hotkey('ctrl', 'z')
            
            elif action == 'redo':
                keyboard.hotkey('ctrl', 'y')
            
            # 'noop' does nothing
        
        except Exception as e:
            print(f"[REWIND ERROR] {action}: {e}")
    
    def get_stack_size(self) -> int:
        """Current stack size"""
        return len(self.keystroke_stack)
    
    def get_stack_info(self) -> str:
        """Get human-readable stack info"""
        size = len(self.keystroke_stack)
        recent = list(self.keystroke_stack)[-10:] if self.keystroke_stack else []
        recent_str = ' → '.join([f"{e.key}" for e in recent])
        return f"Size: {size}, Recent: [{recent_str}]"


# Global instance
_rewind_engine = RewindEngineV3()


def get_rewind_engine() -> RewindEngineV3:
    """Get the global rewind engine instance"""
    return _rewind_engine

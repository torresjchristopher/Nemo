"""
REWIND ENGINE v2 - Ultra-Lightweight Screen State Rewind

ARCHITECTURE:
- Track ONLY reversible keystrokes (typing, navigation, delete)
- Store as simple tuples (action, data) to minimize memory
- Read stack BACKWARDS and execute inverses in real-time
- NO delays, NO logging, NO overhead

When RIGHT ALT + LEFT pressed:
  1. Reverse through keystroke stack
  2. Execute inverse commands immediately
  3. Screen visually rewinds
"""

from collections import deque
from typing import Tuple, Optional, List
import keyboard
import time

# REVERSE INSTRUCTION MAP - Ultra-minimal, O(1) lookup
REVERSE_MAP = {
    # (action) -> (reverse_action, args)
    ('type',): ('backspace', 1),           # Delete typed char
    ('del',): ('backspace_undo', None),   # Use Ctrl+Z to restore deleted
    ('backspace',): ('backspace_undo', None),  # Use Ctrl+Z
    ('right',): ('left', 1),               # Undo navigation right
    ('left',): ('right', 1),               # Undo navigation left
    ('up',): ('down', 1),                  # Undo navigation up
    ('down',): ('up', 1),                  # Undo navigation down
    ('enter',): ('backspace_undo', None), # Undo line break (Ctrl+Z)
    ('tab',): ('backspace_tab', None),    # Delete tab/spaces
    ('ctrl+z',): ('ctrl+y', None),        # Redo (reverse undo)
    ('ctrl+y',): ('ctrl+z', None),        # Undo (reverse redo)
}


class RewindEngine:
    """
    Ultra-lightweight rewind that tracks and reverses keystrokes.
    Designed for MAXIMUM SPEED with MINIMAL memory footprint.
    """
    
    MAX_HISTORY = 5000  # Keep ~5 seconds of typing at 1000 WPM
    
    def __init__(self):
        # Use deque for O(1) append/pop
        self.stack = deque(maxlen=self.MAX_HISTORY)
        self.rewinding = False
        self.last_char = None  # For deleted char recovery
    
    def track(self, key: str):
        """
        Track a keystroke. Called by keyboard listener.
        ULTRA-FAST - only 2 operations.
        
        Args:
            key: Key name ('a', 'right', 'backspace', etc.)
        """
        # Ignore hotkey and non-reversible keys
        if key in ('right shift', 'right alt', 'escape', 'f1', 'f2', 'f3', 'f4', 'f5'):
            return
        
        # Store only what's reversible
        if key in REVERSE_MAP:
            self.stack.append((key,))
            self.last_char = key if len(key) == 1 else None
    
    def rewind_execute(self):
        """
        REWIND: Execute inverse instructions in reverse order.
        THIS IS THE MAGIC - screen visually rewinds!
        
        CRITICAL: Ultra-fast execution, no delays
        """
        if self.rewinding or not self.stack:
            return
        
        self.rewinding = True
        start_time = time.perf_counter()
        ops_executed = 0
        
        # Execute inverses without ANY delays
        while self.stack:
            action = self.stack.pop()
            reverse = REVERSE_MAP.get(action)
            
            if not reverse:
                continue
            
            reverse_action, args = reverse
            
            # Execute the inverse IMMEDIATELY
            self._execute_inverse(reverse_action, args)
            ops_executed += 1
        
        elapsed = time.perf_counter() - start_time
        print(f"[REWIND] Executed {ops_executed} inverse ops in {elapsed*1000:.1f}ms")
        self.rewinding = False
    
    def _execute_inverse(self, action: str, args: Optional[int]):
        """
        Execute inverse command. NO DELAYS.
        
        Directly press keys - let OS handle rendering.
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
            
            elif action == 'backspace_tab':
                # Delete tab (usually 4 spaces)
                for _ in range(4):
                    keyboard.press_and_release('backspace')
            
            elif action == 'backspace_undo':
                # For delete/backspace/enter, use Ctrl+Z
                keyboard.hotkey('ctrl', 'z')
            
            elif action == 'ctrl+y':
                keyboard.hotkey('ctrl', 'y')
            
            elif action == 'ctrl+z':
                keyboard.hotkey('ctrl', 'z')
        
        except Exception as e:
            print(f"[REWIND ERROR] {action}: {e}")
    
    def forward_execute(self):
        """
        FORWARD: Execute predicted next actions.
        Not implemented yet - saves for progress key.
        """
        pass
    
    def get_size(self) -> int:
        """Current stack size (for debugging)"""
        return len(self.stack)
    
    def clear(self):
        """Clear all tracked keystrokes"""
        self.stack.clear()


# Global instance
_rewind_engine = RewindEngine()


def get_rewind_engine() -> RewindEngine:
    """Get the global rewind engine instance"""
    return _rewind_engine


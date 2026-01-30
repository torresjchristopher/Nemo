#!/usr/bin/env python3
"""
Quick test script for keyboard library hotkey detection.
Run this to test if RIGHT SHIFT is detected.
"""

import keyboard
import time
from threading import Thread

print("🎤 Nemo Keyboard Hotkey Test")
print("=" * 50)
print("Press RIGHT SHIFT to test...")
print("Press ESC to quit\n")

def on_right_shift():
    print("\n✓ RIGHT SHIFT DETECTED!")
    print("🔊 Speech-to-Text mode activated")
    time.sleep(0.5)

def on_right_alt():
    print("\n✓ RIGHT ALT DETECTED!")
    print("🎤 Gemini Voice AI activated")
    time.sleep(0.5)

try:
    # Register hotkeys
    keyboard.add_hotkey('shift_r', on_right_shift)
    keyboard.add_hotkey('alt_r', on_right_alt)
    keyboard.add_hotkey('esc', lambda: exit_app())
    
    def exit_app():
        print("\n\nShutting down...")
        exit(0)
    
    # Keep listening
    print("Listening... (Press ESC to exit)\n")
    keyboard.wait()
    
except Exception as e:
    print(f"Error: {e}")
    print("\nNote: keyboard library requires admin privileges on Windows")
    print("Try running PowerShell as Administrator")

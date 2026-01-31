"""
AudioCapture Tool - Microphone input abstraction

Public tool for any key that needs audio input:
- RIGHT SHIFT (speech-to-text)
- RIGHT ALT (Gemini voice input)
"""

from typing import Optional, Callable


class AudioCapture:
    """Handle microphone input for keys"""
    
    def __init__(self, energy_threshold: int = 300, timeout: int = 5):
        """
        Initialize audio capture
        
        Args:
            energy_threshold: Microphone sensitivity (lower = more sensitive)
            timeout: Recording timeout in seconds
        """
        self.energy_threshold = energy_threshold
        self.timeout = timeout
        self.recording = False
    
    def start_recording(self) -> None:
        """Start listening for audio"""
        self.recording = True
    
    def stop_recording(self) -> Optional[str]:
        """Stop listening and return transcript (if STT)"""
        self.recording = False
        return None
    
    def is_recording(self) -> bool:
        """Check if currently recording"""
        return self.recording
    
    def set_energy_threshold(self, threshold: int) -> None:
        """Adjust microphone sensitivity"""
        self.energy_threshold = threshold
    
    def get_status(self) -> dict:
        """Return audio capture status"""
        return {
            'recording': self.recording,
            'energy_threshold': self.energy_threshold,
            'timeout': self.timeout,
        }

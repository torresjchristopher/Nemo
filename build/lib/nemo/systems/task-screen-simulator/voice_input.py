"""
Voice Input Engine: Speech-to-text with live transcription and highlighted text reading.

Handles:
1. Highlighted text detection and reading aloud
2. Microphone listening with real-time speech-to-text
3. On-screen live transcription display
4. Data flow to Nemo for reverse processing and progression
"""

import threading
import queue
import logging
from typing import Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
import platform
import subprocess

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import pyperclip
except ImportError:
    pyperclip = None

# Import TTSEngine - try multiple ways to handle module loading
try:
    from .tts_engine import TTSEngine
except (ImportError, ValueError):
    # Fallback for when loaded via importlib
    try:
        import importlib.util
        from pathlib import Path
        spec = importlib.util.spec_from_file_location(
            "tts_engine_fallback",
            str(Path(__file__).parent / "tts_engine.py")
        )
        if spec and spec.loader:
            tts_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tts_module)
            TTSEngine = tts_module.TTSEngine
        else:
            raise ImportError("Could not load tts_engine")
    except:
        # If all else fails, define a minimal stub
        class TTSEngine:
            def speak(self, text, blocking=True):
                pass


class VoiceInputMode(Enum):
    """Voice input mode."""
    SPEECH_TO_TEXT = "stt"  # Listen to mic and transcribe
    READ_HIGHLIGHTED = "read"  # Read selected text aloud


@dataclass
class VoiceInputConfig:
    """Configuration for voice input engine."""
    mic_timeout: float = 5.0  # Seconds to listen
    phrase_time_limit: float = 15.0  # Max phrase length
    language: str = "en-US"
    energy_threshold: int = 4000  # Mic sensitivity
    show_partial: bool = True  # Show partial transcription in real-time


class VoiceInputEngine:
    """
    Handles voice input with dual modes:
    - Read highlighted text aloud
    - Listen to mic and transcribe to live display
    """

    def __init__(self, config: Optional[VoiceInputConfig] = None, 
                 tts_engine: Optional[TTSEngine] = None,
                 transcription_callback: Optional[Callable[[str, bool], None]] = None):
        """
        Initialize voice input engine.
        
        Args:
            config: Voice input configuration
            tts_engine: TTS engine for reading highlighted text
            transcription_callback: Callback for transcription updates
                - Called with (text, is_final) where is_final=True means complete phrase
        """
        self.config = config or VoiceInputConfig()
        self.logger = logging.getLogger(__name__)
        self.tts_engine = tts_engine or TTSEngine()
        self.transcription_callback = transcription_callback
        
        # Speech recognition setup
        self.recognizer = None
        self.microphone = None
        self._init_recognizer()
        
        # Thread management
        self.current_task: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.transcription_queue = queue.Queue()
        
    def _init_recognizer(self):
        """Initialize speech recognizer."""
        if sr is None:
            self.logger.warning("SpeechRecognition library not installed. Voice input disabled.")
            return
        
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = self.config.energy_threshold
            
            # List available microphones
            try:
                mics = sr.Microphone.list_microphone_indexes()
                self.logger.info(f"Available microphones: {len(mics)}")
            except:
                pass
            
            # Try to use default microphone
            self.microphone = sr.Microphone()
            self.logger.info("Speech recognizer initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize speech recognizer: {e}")
            self.recognizer = None
    
    def read_highlighted_text(self) -> bool:
        """
        Read currently highlighted/selected text aloud.
        
        Attempts to get selected text from clipboard using Ctrl+C copy.
        
        Returns:
            True if text was found and read, False otherwise
        """
        try:
            # Get selected text from clipboard
            selected_text = self._get_selected_text()
            
            if not selected_text or not selected_text.strip():
                self.logger.debug("No highlighted text found")
                return False
            
            self.logger.info(f"Reading highlighted text: {selected_text[:100]}")
            
            # Speak the text
            self.tts_engine.speak(selected_text, blocking=False)
            
            # Notify via callback if available
            if self.transcription_callback:
                self.transcription_callback(f"[READING] {selected_text[:100]}", True)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error reading highlighted text: {e}")
            return False
    
    def _get_selected_text(self) -> Optional[str]:
        """
        Get currently selected/highlighted text from active window.
        
        Uses platform-specific methods to capture selected text.
        """
        try:
            if pyperclip is None:
                return None
            
            # Save current clipboard
            try:
                original_clipboard = pyperclip.paste()
            except:
                original_clipboard = ""
            
            # Copy selected text to clipboard
            if platform.system() == 'Windows':
                subprocess.run(['powershell', '-Command', '$null'], 
                             capture_output=True, timeout=1)
                # Simulate Ctrl+C to copy
                import ctypes
                from ctypes import wintypes
                
                # Get foreground window
                user32 = ctypes.windll.user32
                hwnd = user32.GetForegroundWindow()
                
                # Send Ctrl+C
                user32.PostMessageA(hwnd, 0x0100, 0x43, 0)  # WM_KEYDOWN, 'C'
                user32.PostMessageA(hwnd, 0x0100, 0xA2, 0)  # WM_KEYDOWN, CTRL
                
                import time
                time.sleep(0.1)
                
                # Get clipboard content
                selected_text = pyperclip.paste()
                
                # Restore clipboard
                try:
                    pyperclip.copy(original_clipboard)
                except:
                    pass
                
                return selected_text if selected_text != original_clipboard else None
            
            # For non-Windows, just return None for now
            return None
            
        except Exception as e:
            self.logger.debug(f"Could not get selected text: {e}")
            return None
    
    def listen_and_transcribe(self) -> bool:
        """
        Listen to microphone and transcribe speech to text in real-time.
        
        Returns:
            True if transcription started, False otherwise
        """
        if self.recognizer is None or self.microphone is None:
            self.logger.warning("Speech recognizer not initialized")
            return False
        
        # Stop any existing transcription
        self.stop_event.set()
        
        # Reset and start new transcription
        self.stop_event.clear()
        self.current_task = threading.Thread(
            target=self._transcribe_worker,
            daemon=True
        )
        self.current_task.start()
        
        return True
    
    def _transcribe_worker(self):
        """Worker thread for speech-to-text transcription."""
        try:
            with self.microphone as source:
                self.logger.info("Listening for speech...")
                
                # Notify that listening started
                if self.transcription_callback:
                    self.transcription_callback("[LISTENING...]", False)
                
                # Listen with timeout
                audio = self.recognizer.listen(
                    source,
                    timeout=self.config.mic_timeout,
                    phrase_time_limit=self.config.phrase_time_limit
                )
            
            # Show processing state
            if self.transcription_callback:
                self.transcription_callback("[TRANSCRIBING...]", False)
            
            # Try multiple speech recognition backends
            text = self._recognize_speech(audio)
            
            if text:
                self.logger.info(f"Transcribed: {text}")
                
                # Final transcription
                if self.transcription_callback:
                    self.transcription_callback(text, True)
                
                # Queue for Nemo processing
                self.transcription_queue.put({
                    'text': text,
                    'complete': True,
                    'mode': VoiceInputMode.SPEECH_TO_TEXT
                })
            else:
                if self.transcription_callback:
                    self.transcription_callback("[NO SPEECH DETECTED]", True)
        
        except sr.UnknownValueError:
            self.logger.warning("Could not understand audio")
            if self.transcription_callback:
                self.transcription_callback("[COULD NOT UNDERSTAND]", True)
        
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition service error: {e}")
            if self.transcription_callback:
                self.transcription_callback(f"[ERROR: {str(e)[:50]}]", True)
        
        except Exception as e:
            self.logger.error(f"Transcription error: {e}")
            if self.transcription_callback:
                self.transcription_callback(f"[ERROR: {str(e)[:50]}]", True)
    
    def _recognize_speech(self, audio) -> Optional[str]:
        """
        Recognize speech from audio using available backends.
        
        Tries multiple recognition services in order of preference.
        """
        try:
            # Try Google Speech Recognition (free, no key needed)
            return self.recognizer.recognize_google(audio, language=self.config.language)
        
        except sr.UnknownValueError:
            self.logger.warning("Google: Could not understand audio")
        except sr.RequestError as e:
            self.logger.warning(f"Google: {e}")
        
        try:
            # Fallback: Try Sphinx (offline)
            return self.recognizer.recognize_sphinx(audio)
        except:
            self.logger.warning("Sphinx recognition failed")
        
        return None
    
    def get_transcription(self, timeout: float = 0.1) -> Optional[dict]:
        """
        Get next transcription result from queue without blocking.
        
        Returns:
            Dict with 'text', 'complete', 'mode' or None if no result
        """
        try:
            return self.transcription_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def stop(self):
        """Stop voice input engine."""
        self.stop_event.set()
        if self.current_task and self.current_task.is_alive():
            self.current_task.join(timeout=2.0)
        self.logger.info("Voice input engine stopped")


def smart_right_shift_action(tts_engine: TTSEngine, 
                            transcription_callback: Optional[Callable] = None) -> Optional[str]:
    """
    Smart RIGHT SHIFT action:
    1. If text is highlighted → Read it aloud
    2. If no text highlighted → Listen to mic and transcribe
    
    Args:
        tts_engine: TTS engine instance
        transcription_callback: Callback for transcription updates
    
    Returns:
        Transcribed text if speech-to-text was performed, None if reading highlighted
    """
    voice_engine = VoiceInputEngine(
        tts_engine=tts_engine,
        transcription_callback=transcription_callback
    )
    
    # Try to read highlighted text first
    if voice_engine.read_highlighted_text():
        return None
    
    # No highlighted text, so listen to microphone
    voice_engine.listen_and_transcribe()
    return None  # Result will come through callback


__all__ = [
    'VoiceInputEngine',
    'VoiceInputConfig', 
    'VoiceInputMode',
    'smart_right_shift_action',
]

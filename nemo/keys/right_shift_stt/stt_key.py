"""
STTKey - Speech-to-Text Implementation

RIGHT SHIFT hotkey - Hold to record, release to transcribe.
Ideal for: Quick note capture, dictation, hands-free text input.

Uses:
- AudioCapture tool (microphone handling)
- speech_recognition (multiple STT engines)
"""

from nemo.tools import NemoKey, AudioCapture
import speech_recognition as sr
from typing import Optional


class STTKey(NemoKey):
    """
    Speech-to-Text Key
    
    Hold RIGHT SHIFT to record audio and transcribe to text.
    Release to insert transcript at cursor position.
    """
    
    def __init__(self):
        super().__init__(
            key_name="Speech-to-Text",
            key_combo="right shift",
            description="Hold to record and transcribe speech"
        )
        self.audio = AudioCapture(energy_threshold=300, timeout=5)
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = False
        
        # Recording state
        self.recording = False
        self.transcript = None
        self.confidence = 0.0
    
    def on_press(self) -> None:
        """Called when RIGHT SHIFT pressed"""
        self.audio.start_recording()
        self.recording = True
        self.transcript = None
        self.confidence = 0.0
    
    def on_hold(self, duration: float) -> None:
        """Called while RIGHT SHIFT held (track duration)"""
        # Optional: Show recording indicator
        if duration > 4.5:
            # Almost at timeout limit
            pass  # Could warn user
    
    def on_release(self, total_duration: float) -> Optional[str]:
        """Called when RIGHT SHIFT released - transcribe and insert"""
        self.audio.stop_recording()
        self.recording = False
        
        if total_duration < 0.3:
            # Too short, ignore
            return None
        
        # Transcribe using multiple engines
        transcript = self._transcribe()
        
        if transcript and self.confidence >= 0.80:
            # High confidence - insert directly
            self._insert_text(transcript)
            return transcript
        elif transcript:
            # Low confidence - notify user
            self._notify_low_confidence(transcript)
            return transcript
        else:
            # No speech detected
            return None
    
    def _transcribe(self) -> Optional[str]:
        """Transcribe audio using fallback engines"""
        try:
            # Try Google Speech Recognition (online, accurate)
            transcript = self._try_google()
            if transcript:
                self.confidence = 0.95
                return transcript
        except:
            pass
        
        try:
            # Fall back to Sphinx (offline, less accurate)
            transcript = self._try_sphinx()
            if transcript:
                self.confidence = 0.75
                return transcript
        except:
            pass
        
        try:
            # Final fallback: Bing (online, reliable)
            transcript = self._try_bing()
            if transcript:
                self.confidence = 0.90
                return transcript
        except:
            pass
        
        self.confidence = 0.0
        return None
    
    def _try_google(self) -> Optional[str]:
        """Try Google Speech Recognition"""
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=5)
            text = self.recognizer.recognize_google(audio, language='en-US')
            return text
        except:
            return None
    
    def _try_sphinx(self) -> Optional[str]:
        """Try Sphinx (offline)"""
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=5)
            text = self.recognizer.recognize_sphinx(audio)
            return text
        except:
            return None
    
    def _try_bing(self) -> Optional[str]:
        """Try Microsoft Bing Speech Recognition"""
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=5)
            text = self.recognizer.recognize_bing(audio, language='en-US')
            return text
        except:
            return None
    
    def _insert_text(self, text: str) -> None:
        """Insert transcribed text at cursor position"""
        import keyboard
        # Type the text character by character
        keyboard.write(text, interval=0.01)
    
    def _notify_low_confidence(self, transcript: str) -> None:
        """Notify user of low confidence transcription"""
        print(f"[STT] Low confidence ({self.confidence:.1%}): {transcript}")
        print("[STT] Text NOT inserted. Review manually or re-record.")
    
    def get_status(self) -> dict:
        """Return status"""
        status = super().get_status()
        status.update({
            'recording': self.recording,
            'last_confidence': self.confidence,
            'last_transcript': self.transcript,
        })
        return status
